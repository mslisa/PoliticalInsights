import requests
import re


class ProPublica():

    api_key = 'ODFvfKwCNwTHCbQQf4a3fmCkdW0qU0GnKKpHCe8q'
    
    def all_senators(self, congress='115'):
        # Simple function to collect all senators
        # Uses ProPublica Congress API
        # 115th Congress by default        
        url = "https://api.propublica.org/congress/v1/{congress}/senate/members.json".replace("{congress}", congress)
        header = {"X-API-Key": self.api_key}
        response = requests.get(url, headers=header)
        data = response.json()
        return data['results'][0]['members']
        
    def all_reps(self, congress="115"):
        # Simple function to collect all representatives
        # Uses ProPublica Congress API
        # 115th Congress by default
        url = "https://api.propublica.org/congress/v1/{congress}/house/members.json".replace("{congress}", congress)
        header = {"X-API-Key": self.api_key}
        response = requests.get(url, headers=header)
        data = response.json()
        return data['results'][0]['members']
        
        
class Google():

    api_key = 'AIzaSyAMNlvrMsN-mlVz3_u2bPoaWNG_XhzAs-Y'
    
    def clean_name(self, name):
        return re.sub("\s[A-Za-z](.)?\s", " ", name)
        
    def reps_from_address(self, address):
        address = address.replace(' ','%20')
        url = "https://www.googleapis.com/civicinfo/v2/representatives?key=%s&address=%s" %(self.api_key, address)
        response = requests.get(url)
        data = response.json()
        sen1 = data['officials'][2]
        sen2 = data['officials'][3]
        rep = data['officials'][4]
        return [sen1, sen2, rep]

    def ids_from_address(self, address):
        address = address.replace(' ','%20')
        id_lookup = {}
        pp=ProPublica()
        senators = pp.all_senators()
        reps = pp.all_reps()
        
        for chamber in [senators, reps]:
            for p in chamber:
                member_id = p['id']
                t = p['twitter_account']
                f = p['facebook_account']
                y = p['youtube_account']
                if str(t) != 'null':
                    id_lookup[t] = member_id
                if str(f) != 'null':
                    id_lookup[f] = member_id
                if str(y) != 'null':
                    id_lookup[y] = member_id
                id_lookup[p['url']] = member_id      
        
        my_reps = self.reps_from_address(address)
        
        sen1 = my_reps[0]
        sen2 = my_reps[1]
        rep = my_reps[2]
        
        for u in sen1['urls']:
            if u in id_lookup:
                sen1_id = id_lookup[u]
            if u + '/' in id_lookup:
                sen1_id = id_lookup[u + '/']
        for channel in sen1['channels']:
            temp_id = channel['id']
            if temp_id in id_lookup:
                sen1_id = id_lookup[temp_id]
        
        for u in sen2['urls']:
            if u in id_lookup:
                sen2_id = id_lookup[u]
            if u + '/' in id_lookup:
                sen2_id = id_lookup[u + '/']
        for channel in sen2['channels']:
            temp_id = channel['id']
            if temp_id in id_lookup:
                sen2_id = id_lookup[temp_id]
                
        for u in rep['urls']:
            if u in id_lookup:
                rep_id = id_lookup[u]
            if u + '/' in id_lookup:
                rep_id = id_lookup[u + '/']
        for channel in rep['channels']:
            temp_id = channel['id']
            if temp_id in id_lookup:
                rep_id = id_lookup[temp_id]
        
        img = Images()
        sen1_img = img.image_url(sen1_id)
        sen2_img = img.image_url(sen2_id)
        rep_img = img.image_url(rep_id)
        
        return {'senate':{sen1_id: {'name': my_reps[0]['name'], 'img_url': sen1_img}, 
                          sen2_id: {'name': my_reps[1]['name'], 'img_url': sen2_img}}, 
                'house':{rep_id: {'name': my_reps[2]['name'], 'img_url': rep_img}}}
        
class Images():

    url = 'https://github.com/unitedstates/images/blob/gh-pages/congress/225x275/{id}.jpg?raw=true'
    
    def image_url(self, id):
        return self.url.replace('{id}',id)