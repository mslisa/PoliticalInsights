import re
import numpy as np
import pandas as pd
import json
import os
import shutil
import urllib
import zipfile
from collections import defaultdict
import requests
from keys import Keys

propublica_api_key = Keys.ProPublica()
google_api_key = Keys.Google()

###############################################################################
#
# Function Section
#
###############################################################################

# Note: These functions will manipulate files in the local file structure based on the location of this file
# Please inspect the code prior to running to make sure you're OK with what's about to happen.
# All combined, the 113th, 114th, and 115th congress data load will take up a little over a 1GB

def fetch_and_extract(congress, folderstring):
    '''
    function to perform the following:
        download specified bulk data file from propublica
        unzip
        remove .zip file
        shuffle around folders a little bit (their folder structure is silly)
    '''
    url = 'https://s3.amazonaws.com/pp-projects-static/congress/bills/%s.zip' %congress
    destination_folder = folderstring + '/' + congress
    print "downloading %s.zip. the next few steps will take a minute or two. please talk amongst yourselves." %congress
    urllib.urlretrieve(url, destination_folder + '/%s.zip' %congress)
    print '%s.zip downloaded. unzipping.' %congress
    with zipfile.ZipFile(destination_folder + '/%s.zip' %congress, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)
    print '%s bulk data extracted. Removing .zip file.' %congress
    os.remove(destination_folder + '/%s.zip' %congress)
    print 'simplifying folder structure.'
    shutil.move(destination_folder + '/congress/data/%s/bills/' %congress, destination_folder)
    shutil.rmtree(destination_folder + '/congress')
    print 'data load for congressional session %s is complete. I knew we could do it!' %congress
    print ''

def bulk_update():
    '''
    function to be used with fetch_and_extract to ensure we have
    date in place for 113th, 114th, and 115th congresses
    '''
    # Check for expected folder structure
    if 'Data' in list(os.listdir('./')):
        print 'found ./Data'
    else:
        os.mkdir('./Data')
        print 'created ./Data'
    if 'ProPublicaBulk' in list(os.listdir('./Data/')):
        print 'found ./Data/ProPublicaBulk'
    else:
        os.mkdir('./Data/ProPublicaBulk')
        print 'created ./Data/ProPublicaBulk'

    # Fetch bulk data for 113th congress if needed
    if '113' in list(os.listdir(folderstring)):
        print 'found ./Data/ProPublicaBulk/113'
    else:
        os.mkdir(folderstring + '/113')
        print 'created ./Data/ProPublicaBulk/113'
        fetch_and_extract('113', folderstring)

    # Fetch bulk data for 114th congress if needed
    if '114' in list(os.listdir(folderstring)):
        print 'found ./Data/ProPublicaBulk/114'
    else:
        os.mkdir(folderstring + '/114')
        print 'created ./Data/ProPublicaBulk/114'
        fetch_and_extract('114', folderstring)

    # Fetch bulk data for 115th congress.
    # This one is current, so it's getting updated a lot
    # This function assume it needs to be refreshed
    if '115' in list(os.listdir(folderstring)):
        print 'removing ./Data/ProPublicaBulk/115'
        shutil.rmtree('./Data/ProPublicaBulk/115')
    os.mkdir(folderstring + '/115')
    print 'created ./Data/ProPublicaBulk/115'
    fetch_and_extract('115', folderstring)
    
def all_senators(congress="115", key=propublica_api_key):
    # Simple function to collect all senators
    # Uses ProPublica Congress API
    # 115th Congress by default
    url = "https://api.propublica.org/congress/v1/{congress}/senate/members.json".replace("{congress}", congress)
    header = {"X-API-Key": key}
    response = requests.get(url, headers=header)
    data = response.json()
    return data
    
def all_reps(congress="115", key=propublica_api_key):
    # Simple function to collect all representatives
    # Uses ProPublica Congress API
    # 115th Congress by default
    url = "https://api.propublica.org/congress/v1/{congress}/house/members.json".replace("{congress}", congress)
    header = {"X-API-Key": key}
    response = requests.get(url, headers=header)
    data = response.json()
    return data
    
def build_bill_dict(congress="115"):
    '''
    use os.walk to crawl the folder structure and combine the data from each bill into a common dict
    '''
    out_dict = {}
    for bt in bill_types:
        out_dict[bt] = {}
        for b in list(os.walk("./data/ProPublicaBulk/%s/bills/%s" %(congress,bt)))[0][1]:
            if "data.json" in os.listdir("./data/ProPublicaBulk/%s/bills/%s/%s/" %(congress,bt,b)):
                with open("./data/ProPublicaBulk/%s/bills/%s/%s/data.json" %(congress,bt,b)) as file:
                    data = json.load(file)
                out_dict[bt][b] = data
    return out_dict

def score_bill(b):
    '''
    Simple function to calculate a bill's score based on how far it got
    in the legislative process. 
    
    Resolutions and Joint Resolutions receive greater weight than 
    concurrent and simple resolutions because of their more stringent
    path to success. (simple and concurrent are currently excluded)
    '''
    statuses = b['statuses']
    count = len(statuses)
    for i in range(1,(count+1)):
        status = statuses[-i]
        if "ENACTED" in status:
            return status_scores['enacted']
        elif "PASSED:BILL" in status:
            return status_scores['passed']
        elif "PASS_BACK" in status:
            return status_scores['pass_back']
        elif "PASS_OVER" in status:
            return status_scores['pass_over']
        elif "REPORTED" in status:
            return status_scores['reported']
        elif "REFERRED" in status:
            return status_scores['referred']
        elif "PASSED:CONCURRENTRES" in status:
            return status_scores['passed_conres']
        elif "PASSED:SIMPLERES" in status:
            return status_scores['passed_simpleres']
        
        else:
            pass
    return 0

def distribute_scores(b, chamber):
    '''
    apply a particular bill's score to the associated sponsors and cosponsors
    '''
    sponsor_id = b['sponsor']['bioguide_id']
    sponsor_score = b['score'] * 1.0

    cosponsors=[]
    for csp in b['cosponsors']:
        cosponsors.append(csp['bioguide_id'])
    cosponsor_count = len(cosponsors)
    cosponsor_score = sponsor_score

    if chamber == 's':
        if sponsor_id in senators:
            senators[sponsor_id]['bill_scores'].append(sponsor_score)
            senators[sponsor_id]['sponsor_scores'].append(sponsor_score)
        for co in cosponsors:
            if co in senators:
                senators[co]['bill_scores'].append(cosponsor_score)
                senators[co]['cosponsor_scores'].append(cosponsor_score)

    if chamber == 'h':
        if sponsor_id in representatives:
            representatives[sponsor_id]['bill_scores'].append(sponsor_score)
            representatives[sponsor_id]['sponsor_scores'].append(sponsor_score)
        for co in cosponsors:
            if co in representatives:
                representatives[co]['bill_scores'].append(cosponsor_score)
                representatives[co]['cosponsor_scores'].append(cosponsor_score)
                
def distribute_subjects(b, chamber):
    '''
    add each subject for a particular bill to the rep's subject lists
    
    written to be very similar to distribute_scores for ease of use
    '''
    
    if 'subjects_top_term' in b.keys():
        primary_subject = b['subjects_top_term']
    else:
        primary_subject = ''
    
    sponsor_id = b['sponsor']['bioguide_id']
    
    cosponsors=[]
    for csp in b['cosponsors']:
        cosponsors.append(csp['bioguide_id'])
    cosponsor_count = len(cosponsors)
    
    if chamber == 's':
        if sponsor_id in senators:
            senators[sponsor_id]['sponsor_subjects'][primary_subject] += 1
        for co in cosponsors:
            if co in senators:
                senators[co]['cosponsor_subjects'][primary_subject] += 1

    if chamber == 'h':
        if sponsor_id in representatives:
            representatives[sponsor_id]['sponsor_subjects'][primary_subject] += 1
        for co in cosponsors:
            if co in representatives:
                representatives[co]['cosponsor_subjects'][primary_subject] += 1
                
def aggregate_scores_by_person(person):
    person['sponsor_count'] = len(person['sponsor_scores'])
    if person['sponsor_count'] != 0:
        person['sponsor_mean'] = np.mean(person['sponsor_scores'])
    else:
        person['sponsor_mean'] = 0.0
    person['sponsor_status_counts'] = {x: len([i for i in person['sponsor_scores'] if i == status_scores[x]]) for x in status_scores}
    
    person['cosponsor_count'] = len(person['cosponsor_scores'])
    if person['cosponsor_count'] != 0:
        person['cosponsor_mean'] = np.mean(person['cosponsor_scores'])
    else:
        person['cosponsor_mean'] = 0.0
    person['cosponsor_status_counts'] = {x: len([i for i in person['cosponsor_scores'] if i == status_scores[x]]) for x in status_scores}
    

def aggregate_subjects_by_person(person):
    ss = person['sponsor_subjects']
    s_top5 = sorted(ss, key=ss.__getitem__, reverse=True)[:5]
    person['top_sponsor_subjects'] = [(x, ss[x]) for x in s_top5]
    # makes a column per 
    for i, x in enumerate(s_top5):
        person['top_sponsor_subjects_' + str(i) + "_text"] = x
        person['top_sponsor_subjects_' + str(i) + "_count"] = ss[x]
    
    cs = person['cosponsor_subjects']
    c_top5 = sorted(cs, key=cs.__getitem__, reverse=True)[:5]
    person['top_cosponsor_subjects'] = [(x, cs[x]) for x in c_top5]
    for i, x in enumerate(c_top5):
        person['top_cosponsor_subjects_' + str(i) + "_text"] = x
        person['top_cosponsor_subjects_' + str(i) + "_count"] = cs[x]
    
def ppp(bill, bipart_threshold=.25):
    '''
    The Partisanship Pants Party helper function!
    
    Populates the partisanship dictionary, part_dict
    
    Brick Tamland: Excuse me, Veronica? 
    Veronica Corningstone: Yes? What is it, Brick? 
    Brick Tamland: I would like to extend to you an invitation to the pants party. 
    Veronica Corningstone: Excuse me? 
    Brick Tamland: [struggling] The... party. With the... with the pants. Party with pants? 
    Veronica Corningstone: Brick, are you saying that there's a party in your pants and that I'm invited? 
    Brick Tamland: That's it. 
    Veronica Corningstone: Did Brian tell you to say this, Brick? 
    Brick Tamland: No. Yes. He did. 
    Veronica Corningstone: Okay. No. I don't want to go to a party in your pants. 
    Brick Tamland: Very well. Ian, would you like to go to a party in my pants? 
    Ian: No, Brick. 
    Brick Tamland: All right. Let's go. 
    '''
    sponsor_id = bill['sponsor']['bioguide_id']
    sponsor_party = party_lookup[sponsor_id]
    current_sponsor = sponsor_id in part_dict 
        # as in current member of congress
    co_same = 0
    co_diff = 0
    
    for csp in bill['cosponsors']:
        cosponsor_id = csp['bioguide_id']
        cosponsor_party = party_lookup[cosponsor_id]
        current_cosponsor = cosponsor_id in part_dict
            # as in current member of congress
        if current_cosponsor:
            part_dict[cosponsor_id]['as_cosponsor']['count'] += 1
        if (cosponsor_party in left and sponsor_party in left) or (cosponsor_party in right and sponsor_party in right):
            co_same += 1
            if current_cosponsor:
                part_dict[cosponsor_id]['as_cosponsor']['sponsor_same'] += 1
            if current_sponsor:
                part_dict[sponsor_id]['as_sponsor']['cosponsor_same'] += 1
        else:
            co_diff += 1
            if current_cosponsor:
                part_dict[cosponsor_id]['as_cosponsor']['sponsor_different'] += 1
            if current_sponsor:
                part_dict[sponsor_id]['as_sponsor']['cosponsor_different'] += 1
    
    if current_sponsor:
        part_dict[sponsor_id]['as_sponsor']['count'] += 1
        if len(bill['cosponsors']) > 0:
            if co_diff * 1.0 / (co_diff + co_same) > bipart_threshold:
                part_dict[sponsor_id]['as_sponsor']['bipartisan_support'] += 1
    
    
###############################################################################
#
# Actually Do Stuff
#
###############################################################################

folderstring = './Data/ProPublicaBulk'

# Ensure this function call is not commented out if you want updates to happen
#bulk_update()

for cngrss in ['115','114','113']:

    # Extract member data from API call
    s_data = all_senators(cngrss)["results"][0]["members"]
    h_data = all_reps(cngrss)["results"][0]["members"]

    # Build dictionaries for all current senators and reps
    senators = {}
    representatives = {}
    relevant_keys = ["first_name", "last_name", "party", "state", 
                     "total_votes", "votes_with_party_pct", "dw_nominate",
                     "missed_votes_pct", "seniority"]

    for member in s_data:
        senators[member["id"]] = {}
        for key in relevant_keys:
            if key in member.keys():
                senators[member["id"]][key] = member[key]
            else:
                senators[member["id"]][key] = "NA"
            
    for member in h_data:
        representatives[member["id"]] = {}
        for key in relevant_keys:
            if key in member.keys():
                representatives[member["id"]][key] = member[key]
            else:
                representatives[member["id"]][key] = "NA"
                
    # Bulk data is separated into different folders where each
    # folder represents a different type of bill (house resolution, 
    # senate joint resolution, etc.)

    #Only uncomment one of the following 2 lines:

    bill_types = os.listdir("./data/ProPublicaBulk/115/bills") # This line includes all bill types
    #bill_types = ['hjres', 'hr', 's', 'sjres'] # This line restricts bill types to those that can become law

    #This dict defines how much each "farthest reached status" is worth for scoring
    status_scores = {'enacted':10,    # Bill becomes law
                     'passed':7,      # Bill sent to president for signature
                     'pass_back':5,   # The bill has passed each chamber at least once
                     'pass_over':4,   # The bill has passed at least one chamber
                     'reported':2,    # The bill has been "reported out of committee"
                     'referred':1,    # At least they tried to do *something*, but didn't make it out of committee
                     'passed_conres':3.5,
                     'passed_simpleres':2.5}    
                 

    # Define and populate dictionaries for bills in each congress
    c_dict = build_bill_dict(cngrss)

    congresses = [c_dict]

    # Define a place to stack individual bill scores
    # Must be in place before running distribute_scores()!
    # Also add a place to accumulate bill subjects
    for s in senators.keys():
        senators[s]['bill_scores'] = []
        senators[s]['sponsor_scores'] = []
        senators[s]['cosponsor_scores'] = []
        senators[s]['sponsor_subjects'] = defaultdict(int)
        senators[s]['cosponsor_subjects'] = defaultdict(int)
    for r in representatives.keys():
        representatives[r]['bill_scores'] = []
        representatives[r]['sponsor_scores'] = []
        representatives[r]['cosponsor_scores'] = []
        representatives[r]['sponsor_subjects'] = defaultdict(int)
        representatives[r]['cosponsor_subjects'] = defaultdict(int)
    
    #Gonna need this later...
    party_lookup = {}
    for c in [cngrss]:
    #for c in ['113','114','115']:
        for member in all_senators(congress=c)["results"][0]["members"]:
            party_lookup[member['id']] = member['party']
        for member in all_reps(congress=c)["results"][0]["members"]:
            party_lookup[member['id']] = member['party']
    
    # As of right now, there are only Democrats, Republicans, and Independents in Congress
    # None in the House, 2 in the Senate
    # Both Independents in the Senate caucus with the Democrats
    # So for this purpose, they are considered to be the "same"
    left = ['D','I']
    right = ['R']

    part_dict = {}

    for s in senators.keys():
        part_dict[s] = {'as_sponsor': {'count': 0,
                                       'cosponsor_same': 0,
                                       'cosponsor_different': 0,
                                       'bipartisan_support': 0},
                        'as_cosponsor': {'count': 0,
                                         'sponsor_same': 0,
                                         'sponsor_different': 0},
                        'chamber': 'Senate',
                        'party': senators[s]['party'],
                        'name': senators[s]['first_name'] + ' ' + senators[s]['last_name']
                        }
        
    for r in representatives.keys():
        part_dict[r] = {'as_sponsor': {'count': 0,
                                       'cosponsor_same': 0,
                                       'cosponsor_different': 0,
                                       'bipartisan_support': 0},
                        'as_cosponsor': {'count': 0,
                                         'sponsor_same': 0,
                                         'sponsor_different': 0},
                        'chamber': 'House',
                        'party': representatives[r]['party'],
                        'name': representatives[r]['first_name'] + ' ' + representatives[r]['last_name']
                        }   
        
    # Loop through every bill in each congress
    # For each bill, build a list of statuses, in order
    # While we're there, score the bill too
    # And may as well distribute the scores too...

    # Yes, it's a quadruple for loop, but it's still fast. Trust me!

    for c in congresses:
        for bt in bill_types:
            for b in c[bt].keys():
                c[bt][b]['statuses'] = []
                for a in c[bt][b]['actions']:
                    if 'status' in a.keys():
                        c[bt][b]['statuses'].append(a['status'])
                
                c[bt][b]['score'] = score_bill(c[bt][b])
                
                distribute_scores(c[bt][b], bt[0])
                distribute_subjects(c[bt][b], bt[0])
                
                # call the helper function created above to populate the partisanship dictionary
                ppp(c[bt][b])
                
    for s in senators:
        aggregate_scores_by_person(senators[s])
    for r in representatives:
        aggregate_scores_by_person(representatives[r])
        
    for s in senators:
        aggregate_subjects_by_person(senators[s])
    for r in representatives:
        aggregate_subjects_by_person(representatives[r])
            
    # gather up all the average scores to normalize by party
    # nomenclature example: senate republican sponsor = srs
    srs_scores = []
    src_scores = []
    sds_scores = []
    sdc_scores = []

    hrs_scores = []
    hrc_scores = []
    hds_scores = []
    hdc_scores = []

    for s in senators:
        sp_mean = senators[s]['sponsor_mean']
        co_mean = senators[s]['cosponsor_mean']
        
        if senators[s]['party'] == 'R':
            srs_scores.append(sp_mean)
            src_scores.append(co_mean)
        else:
            sds_scores.append(sp_mean)
            sdc_scores.append(co_mean)
            
    for r in representatives:
        sp_mean = representatives[r]['sponsor_mean']
        co_mean = representatives[r]['cosponsor_mean']
        
        if representatives[r]['party'] == 'R':
            hrs_scores.append(sp_mean)
            hrc_scores.append(co_mean)
        else:
            hds_scores.append(sp_mean)
            hdc_scores.append(co_mean)
            
    # Denominators!

    srs_max = max(srs_scores)
    src_max = max(src_scores)
    sds_max = max(sds_scores)
    sdc_max = max(sdc_scores)

    hrs_max = max(hrs_scores)
    hrc_max = max(hrc_scores)
    hds_max = max(hds_scores)
    hdc_max = max(hdc_scores)

    # Let's do more loops. This time to capture the normalized average scores
    # and each person's rank relative to the applicable group

    for s in senators:
        sp_mean = senators[s]['sponsor_mean']
        co_mean = senators[s]['cosponsor_mean']
        
        if senators[s]['party'] == 'R':
            senators[s]['sponsor_normalized'] = sp_mean / srs_max
            senators[s]['sponsor_rank'] = len([i for i in srs_scores if i > sp_mean]) + 1
            senators[s]['cosponsor_normalized'] = co_mean / src_max
            senators[s]['cosponsor_rank'] = len([i for i in src_scores if i > co_mean]) + 1
        else:
            senators[s]['sponsor_normalized'] = sp_mean / sds_max
            senators[s]['sponsor_rank'] = len([i for i in sds_scores if i > sp_mean]) + 1
            senators[s]['cosponsor_normalized'] = co_mean / sdc_max
            senators[s]['cosponsor_rank'] = len([i for i in sdc_scores if i > co_mean]) + 1
            
    for r in representatives:
        sp_mean = representatives[r]['sponsor_mean']
        co_mean = representatives[r]['cosponsor_mean']
        
        
        if representatives[r]['party'] == 'R':
            representatives[r]['sponsor_normalized'] = sp_mean / hrs_max
            representatives[r]['sponsor_rank'] = len([i for i in hrs_scores if i > sp_mean]) + 1
            representatives[r]['cosponsor_normalized'] = co_mean / hrc_max
            representatives[r]['cosponsor_rank'] = len([i for i in hrc_scores if i > co_mean]) + 1
        else:
            representatives[r]['sponsor_normalized'] = sp_mean / hds_max
            representatives[r]['sponsor_rank'] = len([i for i in hds_scores if i > sp_mean]) + 1
            representatives[r]['cosponsor_normalized'] = co_mean / hdc_max
            representatives[r]['cosponsor_rank'] = len([i for i in hdc_scores if i > co_mean]) + 1
            
    # looping again, this time to fold in the partisanship figures
    
    for s in senators:
        senators[s]['bi_sponsor_count'] = part_dict[s]['as_sponsor']['count']
        senators[s]['bi_sponsor_bi'] = part_dict[s]['as_sponsor']['bipartisan_support']
        
    for r in representatives:
        representatives[r]['bi_sponsor_count'] = part_dict[r]['as_sponsor']['count']
        representatives[r]['bi_sponsor_bi'] = part_dict[r]['as_sponsor']['bipartisan_support']
    
    # prep to build pandas dataframe for output file

    fields = ['party', 
              'state', 
              'total_votes',
              'votes_with_party_pct',
              'dw_nominate',
              'missed_votes_pct',
              'seniority',
              'cosponsor_count', 
              'cosponsor_normalized', 
              'cosponsor_rank', 
              'sponsor_count',
              'sponsor_normalized',
              'sponsor_rank',
              'bi_sponsor_count',
              'bi_sponsor_bi',
              'top_sponsor_subjects',
              'top_sponsor_subjects_1_text',
              'top_sponsor_subjects_1_count',
              'top_sponsor_subjects_2_text',
              'top_sponsor_subjects_2_count',
              'top_sponsor_subjects_3_text',
              'top_sponsor_subjects_3_count',
              'top_sponsor_subjects_4_text',
              'top_sponsor_subjects_4_count',
              'top_sponsor_subjects_5_text',
              'top_sponsor_subjects_5_count',
              'top_cosponsor_subjects'
              'top_cosponsor_subjects_1_text',
              'top_cosponsor_subjects_1_count',
              'top_cosponsor_subjects_2_text',
              'top_cosponsor_subjects_2_count',
              'top_cosponsor_subjects_3_text',
              'top_cosponsor_subjects_3_count',
              'top_cosponsor_subjects_4_text',
              'top_cosponsor_subjects_4_count',
              'top_cosponsor_subjects_5_text',
              'top_cosponsor_subjects_5_count',]

    senate_rows_list = []
    house_rows_list = []

    for s in senators:
        row_dict = {'id': s, 'name': senators[s]['first_name'] + ' ' + senators[s]['last_name']}
        for f in fields:
            row_dict[f] = senators[s][f]
        senate_rows_list.append(row_dict)
            
    for r in representatives:
        row_dict = {'id': r, 'name': representatives[r]['first_name'] + ' ' + representatives[r]['last_name']}
        for f in fields:
            row_dict[f] = representatives[r][f]
        house_rows_list.append(row_dict)
        
    senators_df = pd.DataFrame(senate_rows_list).set_index('id')
    representatives_df = pd.DataFrame(house_rows_list).set_index('id')

    senators_df['color'] = senators_df['party'].map(lambda x: {'R': 'red', 'D': 'blue', 'I': 'blue'}[x])
    representatives_df['color'] = representatives_df['party'].map(lambda x: {'R': 'red', 'D': 'blue', 'I': 'blue'}[x])
    
    senators_df['size'] = 20
    representatives_df['size'] = 20
    
    senators_df['bi_pct'] = senators_df.bi_sponsor_bi * 1.0 / senators_df.bi_sponsor_count
    representatives_df['bi_pct'] = representatives_df.bi_sponsor_bi * 1.0 / representatives_df.bi_sponsor_count
    
    senators_df['chamber'] = 'senate'
    representatives_df['chamber'] = 'house'
    
    senators_df['congress'] = cngrss
    representatives_df['congress'] = cngrss

    if 'final_out_df' in locals():
        final_out_df = pd.concat([final_out_df, senators_df, representatives_df])
    else:
        final_out_df = pd.concat([senators_df, representatives_df])
    
    #senators_df.to_csv('%s_senator_effectiveness.csv' %cngrss, encoding='utf-8')
    #representatives_df.to_csv('%s_house_effectiveness.csv' %cngrss, encoding='utf-8')

final_out_df.to_csv('effectiveness.csv', encoding='utf-8')