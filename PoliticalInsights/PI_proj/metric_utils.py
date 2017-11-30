import pandas as pd
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from collections import OrderedDict

class effectiveness():

    def generate_plot(self, df, mid):
        if mid in list(df.id):
            row_index = df.id == mid
            df.loc[row_index, 'size'] = 200
            
            congresses = [115] # using this structure in case we want
                               # to expand back to 113th (if applicable) 
            chamber = sorted(df[df.id == mid].chamber.unique())[0]
            
            # Loop through every applicable congress for the given mid
            for congress in congresses:
                # Filter the dataframe to only the data we want to plot
                temp_df = df[(df.congress == congress) & (df.chamber == chamber) & (df.bi_sponsor_count != 0)]
                #member_index = np.where(temp_df.id == mid)[0][0]
                colors = []
                for i in range(len(temp_df.color)):
                    if list(temp_df.id)[i] == mid:
                        colors.append('green')
                    else:
                        colors.append(list(temp_df.color)[i])
                
                '''
                fig=Figure()
                ax=fig.add_subplot(111)
                ax.scatter(temp_df.sponsor_rank, temp_df.cosponsor_rank, color=colors, s=temp_df['size'])
                plt.xlabel('sponsorship rank')
                plt.ylabel('cosponsorship rank')
                ax.set_xlim([0,max(temp_df.sponsor_rank)+2])
                ax.invert_xaxis()
                ax.set_ylim([0,max(temp_df.cosponsor_rank)+2])
                ax.invert_yaxis()
                plt.title('Effectiveness Rankings')
                return fig
                '''
                
                # Build the plots
                plt.figure(figsize=(4, 4))
                
                #plt.subplot(221)
                plt.scatter(temp_df.sponsor_rank, temp_df.cosponsor_rank, color=colors, s=temp_df['size'])
                plt.xlabel('Sponsorship rank')
                plt.ylabel('Co-sponsorship rank')
                ax = plt.gca()
                ax.set_xlim([0,max(temp_df.sponsor_rank)+2])
                ax.invert_xaxis()
                ax.set_ylim([0,max(temp_df.cosponsor_rank)+2])
                ax.invert_yaxis()
                #plt.title('%s %s Effectiveness Rankings' %(congress, chamber))
                plt.title('Effectiveness Rankings')
                
                plt.tight_layout()
                fig_exp = "Effectiveness is an indication of how successful members are at writing bills that go on to become law. \
Being ranked #1 would mean that the member sponsors or cosponsors bills that make it further along in the legislative \
process, on average, than the rest of the members in his or her caucus. This figure shows the member's effectiveness both \
as a bills sponsor (horizontal axis) and cosponsor (vertical axis)"
                
                return {'fig': plt.figure(), 'fig_explanation': fig_exp}
                
    def key_stats(self, df, mid):
        if mid in list(df.id):
            
            chamber = sorted(df[df.id == mid].chamber.unique())[0]
            party = sorted(df[df.id == mid].party.unique())[0]
            
            # Filter the dataframe
            temp_df = df[(df.congress == 115) & (df.chamber == chamber) & (df.party == party)]
            
            name = list(temp_df[temp_df.id == mid].name)[0]
            
            s_rank = list(temp_df[temp_df.id == mid].sponsor_rank)[0]
            s_count = list(temp_df[temp_df.id == mid].sponsor_count)[0]
            c_rank = list(temp_df[temp_df.id == mid].cosponsor_rank)[0]
            c_count = list(temp_df[temp_df.id == mid].cosponsor_count)[0]
            
            out_of = len(temp_df)
            s_count_percentile = len(temp_df[temp_df.sponsor_count < s_count]) * 1.0 / out_of
            c_count_percentile = len(temp_df[temp_df.cosponsor_count < c_count]) * 1.0 / out_of
            
            out_dict = OrderedDict()
            out_dict['stat1'] = {'stat': '%s' %s_count, 'stat_explanation': 'Bills sponsored'}
            out_dict['stat2'] = {'stat': '%s out of %s' %(s_rank, out_of), 'stat_explanation': 'Sponsorship effectiveness compared to own party'}
            out_dict['stat3'] = {'stat': '%s' %c_count, 'stat_explanation': 'Bills cosponsored'}
            out_dict['stat4'] = {'stat': '%s out of %s' %(c_rank, out_of), 'stat_explanation': 'Cosponsorship effectiveness compared to own party'}
            
            return out_dict
            

class bipartisanship():

    def generate_plot(self, df, mid):
        if mid in list(df.id):
            row_index = df.id == mid
            df.loc[row_index, 'size'] = 200
            
            congresses = [115] # using this structure in case we want
                               # to expand back to 113th (if applicable) 
            chamber = sorted(df[df.id == mid].chamber.unique())[0]
            
            # Loop through every applicable congress for the given mid
            for congress in congresses:
                # Filter the dataframe to only the data we want to plot
                temp_df = df[(df.congress == congress) & (df.chamber == chamber) & (df.bi_sponsor_count != 0)]
                #member_index = np.where(temp_df.id == mid)[0][0]
                colors = []
                for i in range(len(temp_df.color)):
                    if list(temp_df.id)[i] == mid:
                        colors.append('green')
                    else:
                        colors.append(list(temp_df.color)[i])
                
                # Build the plots
                
                fig = plt.figure(figsize=(6,4))
                ax = fig.add_subplot(1,1,1)
                
                #plt.figure(figsize=(4, 4))
                
                red = temp_df[temp_df.color == 'red']
                blue = temp_df[temp_df.color == 'blue']
                ax.hist(red.bi_pct*100, color='Red', alpha=0.5)
                ax.hist(blue.bi_pct*100, color='Blue', alpha=0.5)
                plt.xlabel('portion of bills sponsored w/bipartisan support')
                plt.ylabel('# of bills')
                pct = list(temp_df[temp_df.id == mid]['bi_pct'])[0] * 100
                ax.axvline(pct, color='green', linewidth=5)
                
                fmt = '%.0f%%' # tick format
                xticks = mtick.FormatStrFormatter(fmt)
                ax.get_xaxis().set_major_formatter(xticks)
                
                plt.title('Bipartisanship Comparison')
                
                plt.tight_layout()
                
                fig_exp = "This Bipartisanship figure indicates the degree to which a member sponsors legislation that garners \
cosponsorship support from members of the opposite party. The blue and red sections show the distribution for democrats and republicans, respectively. \
The solid line shows where this particular member falls in their party's distribution. For this analysis, a bill is considered to have bipartisan \
support if at least 25% of its cosponsors were members from a party different from the sponsor's party."
                
                return {'fig': plt.figure(), 'fig_explanation': fig_exp}
                
    def key_stats(self, df, mid):
        if mid in list(df.id):
            
            chamber = sorted(df[df.id == mid].chamber.unique())[0]
            party = sorted(df[df.id == mid].party.unique())[0]
            
            # Filter the dataframe
            temp_df = df[(df.congress == 115) & (df.chamber == chamber) & (df.party == party)]
            
            name = list(temp_df[temp_df.id == mid].name)[0]
            
            bi_pct = list(temp_df[temp_df.id == mid].bi_pct)[0]
            out_of = len(temp_df)
            bi_pct_percentile = len(temp_df[temp_df.bi_pct < bi_pct]) * 1.0 / out_of
            
            out_dict = OrderedDict()
            out_dict['stat1'] = {'stat': '%s%%' %round(bi_pct*100), 'stat_explanation': 'Percentage of sponsored bills that gained bipartisan cosponsorship'}
            out_dict['stat2'] = {'stat': '%s%%' %round(bi_pct_percentile*100), 'stat_explanation': 'Percentage of own party out-performed in this metric'}
            
            return out_dict
        
class financials():
    
    def fin_plot(self,df1,REP_ID):
        #make dictionary
        
        import pandas as pd
        import matplotlib.pyplot as plt
        from collections import defaultdict

        #make dictionary
        c_dict = defaultdict(dict)

        for rows in range(0,len(df1)):
            name_ = df1[3][rows]
            party_ = u"{}".format(df1[4][rows])
            status_ = df1[5][rows]
            id_ = df1[0][rows]
            total_from_individuals_ = df1[8][rows]
            total_from_pacs_ = df1[9][rows]
            c_dict[id_] = {'party':party_, 'status':status_, 
                   'name': name_, 'id':id_, 'total_from_individuals':total_from_individuals_,
                  'total_from_pacs':total_from_pacs_,
                  'donor_ratio': round(float(total_from_individuals_+1)/float(total_from_pacs_+1),2),
                  'explanation': "When conducting their campaigns, representatives accept donations from both private individuals as well as Political Action Committees (PACS), organizations that collect financial contributions from their members and use the funds to aid or hinder candidate campaigns, or legislation. The metric shows the number of individual donor dollars per $1 donated by PACS.The filled circle shows PAC donor dollars versus  individual donor dollars given to your representative's campaign, colored by political party affiliation."
                  }
            
        # print c_dict[REP_ID], "\n"

        ids = [i for i in c_dict.keys()]
        for ii in ids:
            if ii == REP_ID:
                if c_dict[str(ii)]['party'] == u'DEM':
                    plt.scatter(c_dict[str(ii)]['total_from_individuals'],c_dict[str(ii)]['total_from_pacs'],s=100,c='b',edgecolors='w',zorder=10)
                elif c_dict[str(ii)]['party'] == u'REP':
                    plt.scatter(c_dict[str(ii)]['total_from_individuals'],c_dict[str(ii)]['total_from_pacs'],s=100,c='r',edgecolors='w',zorder=10)
                else:
                    plt.scatter(c_dict[str(ii)]['total_from_individuals'],c_dict[str(ii)]['total_from_pacs'],s=100,c='g',edgecolors='w',zorder=10)

            else:
                if c_dict[str(ii)]['party'] == u'DEM':
                    plt.scatter(c_dict[str(ii)]['total_from_individuals'],c_dict[str(ii)]['total_from_pacs'],s=100,color='w',edgecolors='b')
                elif c_dict[str(ii)]['party'] == u'REP':
                    plt.scatter(c_dict[str(ii)]['total_from_individuals'],c_dict[str(ii)]['total_from_pacs'],s=100,color='w',edgecolors='r')
                else:
                    plt.scatter(c_dict[str(ii)]['total_from_individuals'],c_dict[str(ii)]['total_from_pacs'],s=100,color='w',edgecolors='g')

            plt.title(str(c_dict[REP_ID]['name']) + " CAMPAIGN CONTRIBUTIONS")
            plt.xlabel("Total ($) From Individuals")
            
            plt.ticklabel_format(style='plain', axis='y')
            plt.ticklabel_format(style='plain', axis='x')
            
            #adding 10%
            plt.xlim([(-df1[8].max()*0.1),df1[8].max()+(df1[8].max()*0.1)])
            plt.ylim([(-df1[9].max()*0.1),df1[9].max()+(df1[9].max()*0.1)])

            #Creating our line
            slope = df1[9].max()/df1[8].max()
            x_0 = 0
            y_0 = 0
            x_1 = df1[8].max()
            y_1 = slope*(x_1 - x_0) + y_0
            plt.plot([x_0, x_1], [y_0, y_1], linewidth=0.5,c='black') 
            plt.ylabel("Total ($) From PACS");
        #plt.figure(figsize=(4, 4))
        #plt.show();
        # plt.savefig('findata.png');

        fig_dict = {'fig': plt.figure(), 'fig_explanation': c_dict[REP_ID]['explanation']}
        quick_stat_dict = {'total_from_individuals': {'stat':total_from_individuals_, 'stat_explanation': "Total from individuals"},
                           'total_from_pacs': {'stat':total_from_pacs_, 'stat_explanation': "Total from PACS"},
                           'donor_ratio': {'stat':round(float(total_from_individuals_+1)/float(total_from_pacs_+1),2), 'stat_explanation': "Donor ratio"}}
        return {'fig_dict': fig_dict, 'quick_stat_dict': quick_stat_dict}


class twitter_stuff():
    
    def twitter(self,df_t,REP_ID):
        
        import re, string
        import pandas as pd
        from IPython.display import Image
        from wordcloud import WordCloud
        from nltk.corpus import stopwords
        import matplotlib.pyplot as plt
        from collections import defaultdict

        
        #Converting rep_id to name for twitter query

        #print "Public Perception of ", df_t.loc[df_t['id'] == REP_ID, 'name'].item(), "\t ", str(df_t.loc[df_t['id'] == REP_ID, 'twitter_handle'].item()), "\n"
        #print "*"*75,"\n"
#         print "Total Tweets: ", df_t.loc[df_t['id'] == REP_ID, 'total_tweets'].item(), "\t Positive Tweets: ", df_t.loc[df_t['id'] == REP_ID, 'pos_tweets'].item(), "\t Negative Tweets: ", df_t.loc[df_t['id'] == REP_ID, 'neg_tweets'].item(),"\n"

#         print "*"*75,"\n"
        
        
        
        topics_list = [
        'Agriculture and Food [127]', 'Animals [52]','Armed Forces and National Security [664]','Arts, Culture, Religion [33]',
        'Civil Rights and Liberties, Minority Issues [111]',
        'Commerce [155]','Congress [306]','Crime and Law Enforcement [445]','Economics and Public Finance [96]',
        'Education [308]','Emergency Management [103]','Energy [212]',
        'Environmental Protection [195]','Families [44]','Finance and Financial Sector [270]',
        'Foreign Trade and International Finance [55]','Government Operations and Politics [573]',
        'Health [791]','Housing and Community Development [80]','Immigration [222]',
        'International Affairs [475]','Labor and Employment [214]','Law [74]',
        'Native Americans [106]','Public Lands and Natural Resources [439]','Science, Technology, Communications [180]',
        'Social Sciences and History [4]','Social Welfare [97]','Sports and Recreation [44]',
        'Taxation [647]','Transportation and Public Works [249]','Water Resources Development [46]']

        #cleaning up topics
        topics_ = [str(item).split("[")[0] for item in topics_list]

        stop_words = set(stopwords.words( 'english' ))

        # #Adding some interesting topics
        topics_.insert(0,"Democrat")
        topics_.insert(0,"Republican")
        topics_.insert(0,str(df_t.loc[df_t['id'] == REP_ID, 'twitter_handle'].item()))

        #making dictionary to keep track of the topics being discussed online
        topics_dict = defaultdict(dict)

        #cleaning text

        text = df_t.loc[df_t['id'] == REP_ID, 'tweet_text'].item().replace("u'",'').lower()
        text = ' '.join([str(i).strip("'[]") for i in text.split(",")])
        
        #adding hashtags to topics!
        for word in text.split():
            if ("#" in word):
                topics_.insert(0,str(word))
        
        #removing some stuff
        for word in text.split():
            if ("@" not in word) and ("\u" not in word) and ("https" not in word) and ("rt" not in word) and ("retweet" not in word):
                next
            else:
                text = text.replace(word,"")
        
        text_list = list(text.split("  "))

        #organizing text
        topic_string = [str(i).lower() for i in topics_]


        for item in topic_string:
            for i in text_list:
                if i in item:
                    if len(i)>2:
                        if i not in stop_words:
                            try:
                                if topics_dict[item][i]:
                                    topics_dict[item][i] += 1  
                                else:
                                    topics_dict[item][i] = 1
                            except:
                                topics_dict[item][i] = 1                      

        ##Topic Summary

        ''' if not topics_dict:
            print ("\nTrending Topics: Variety \n")
            print ("(Twitter data on this representative is limited or non existent.)")
        else:
            print ("\nTrending Topics: \n")
            for i, key in enumerate(sorted(topics_dict, key=topics_dict.get, reverse=True)):
                print i," - ", key.title(), ": ", sum(topics_dict[key].values()),"tweet(s)." '''
                
        #metrics dictionary output
        tweet_metrics = defaultdict(dict)
        
        tweet_metrics[REP_ID] = {'name':str(df_t.loc[df_t['id'] == REP_ID, 'name'].item()),
                                 'twitter_handle':str(df_t.loc[df_t['id'] == REP_ID, 'twitter_handle'].item()),
                                 'total_tweets':df_t.loc[df_t['id'] == REP_ID, 'total_tweets'].item(),
                                 'pos_tweets': df_t.loc[df_t['id'] == REP_ID, 'pos_tweets'].item(),
                                 'neg_tweets': df_t.loc[df_t['id'] == REP_ID, 'neg_tweets'].item(),
                                'topics': list(sorted(topics_dict.iterkeys()))}
        
        #print "\n", tweet_metrics[REP_ID], "\n"
        


        #word cloud portion!

        wordcloud = WordCloud().generate(text)
        wordcloud = WordCloud(max_font_size=50).generate(text)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        #plt.show()
        # plt.savefig('word_cloud.png');

        fig_dict = {'fig': plt.figure(), 'fig_explanation': c_dict[REP_ID]['explanation']}
        quick_stat_dict = {'total_tweets': {'stat':df_t.loc[df_t['id'] == REP_ID, 'total_tweets'].item(), 'stat_explanation': "Total tweet count"},
                           'pos_tweets': {'stat':df_t.loc[df_t['id'] == REP_ID, 'pos_tweets'].item(), 'stat_explanation': "Positive tweet count"},
                           'neg_tweets': {'stat':df_t.loc[df_t['id'] == REP_ID, 'neg_tweets'].item(), 'stat_explanation': "Negative tweet count"},
                           'neg_tweets': {'stat':df_t.loc[df_t['id'] == REP_ID, 'neg_tweets'].item(), 'stat_explanation': "Negative tweet count"},
                           'topics': {'stat':", ".join(sorted(topics_dict, key=topics_dict.get, reverse=True)[5]), 'stat_explanation': "Top five topics"}}
        return {'fig_dict': fig_dict, 'quick_stat_dict': quick_stat_dict}
    
class contact():
    
    
    def contact_card(self,json_file,REP_ID):
        import json
        
        with open(json_file) as json_data:
            d = json.load(json_data)

        quick_stat_dict = {}
        # quick_stat_dict['website'] = {'stat': 'Website', 'stat_explanation': '<a href={}>{}</a>'.format(d[REP_ID]['Website'], d[REP_ID]['Website'])}
        # quick_stat_dict['Fax'] = {'stat': 'Fax', 'stat_explanation': d[REP_ID]['Fax']}
        # quick_stat_dict['Office'] = {'stat': 'Office', 'stat_explanation': d[REP_ID]['Office']}
        # quick_stat_dict['Contact Form'] = {'stat': 'Contact Form', 'stat_explanation': d[REP_ID]['Contact Form']}
        # quick_stat_dict['Phone'] = {'stat': 'Phone', 'stat_explanation': d[REP_ID]['Phone']}
        # quick_stat_dict['Facebook'] = {'stat': 'Facebook', 'stat_explanation': '<a href={}>{}</a>'.format(d[REP_ID]['Facebook'], d[REP_ID]['Facebook'])}
        # quick_stat_dict['Twitter'] = {'stat': 'Twitter', 'stat_explanation': '<a href={}>{}</a>'.format(d[REP_ID]['Twitter'], d[REP_ID]['Twitter'])}

        for contact_type, contact_path in d[REP_ID].items():
            quick_stat_dict[contact_type] = {'stat': contact_type, 'stat_explanation': contact_path}

        return quick_stat_dict
       

if __name__ == "__main__":
    main()
