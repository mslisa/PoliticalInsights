import pandas as pd
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

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
                
                return plt.figure()
                
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
            
            return {'name': name, 'sponsor_effectiveness_rank': s_rank, 'cosponsor_effectiveness_rank': c_rank, 'out_of': out_of,
                    'sponsor_count': s_count, 'sponsor_count_percentile': s_count_percentile,
                    'cosponsor_count': c_count, 'cosponsor_count_percentile': c_count_percentile}
            
            

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
                
                return plt.figure()
                
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
            
            return {'name': name, 'bipartisan_percentage': bi_pct, 'out_of': out_of, 'bipartisan_percentile': bi_pct_percentile}
        
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
                          'total_from_pacs':total_from_pacs_}


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
            plt.ylabel("Total ($) From PACS")
	#plt.figure(figsize=(4,4))
        #plt.show();
        #plt.savefig('findata1.png')
        return plt.figure()

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

        print "Public Perception of ", df_t.loc[df_t['id'] == REP_ID, 'name'].item(), "\t ", str(df_t.loc[df_t['id'] == REP_ID, 'twitter_handle'].item()), "\n"
        print "*"*75,"\n"
        print "Total Tweets: ", df_t.loc[df_t['id'] == REP_ID, 'total_tweets'].item(), "\t Positive Tweets: ", df_t.loc[df_t['id'] == REP_ID, 'pos_tweets'].item(), "\t Negative Tweets: ", df_t.loc[df_t['id'] == REP_ID, 'neg_tweets'].item(),"\n"

        print "*"*75,"\n"
        
        topics_list = [
        'Agriculture and Food [127]', 'Animals [52]','Armed Forces and National Security [664]','Arts, Culture, Religion [33]',
        'Civil Rights and Liberties, Minority Issues [111]',
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

        if not topics_dict:
            print ("\nTrending Topics: Variety \n")
            print ("(Twitter data on this representative is limited or non existent.)")
        else:
            print ("\nTrending Topics: \n")
            i = 1
            for key in sorted(topics_dict.iterkeys()):
                print i," - ", key.title(), ": ", sum(topics_dict[key].values()),"tweet(s)."
                i += 1


        #word cloud portion!

        wordcloud = WordCloud().generate(text)
        wordcloud = WordCloud(max_font_size=50).generate(text)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        # plt.show();
        # plt.savefig('word_cloud.png');
        return plt.figure()

if __name__ == "__main__":
    main()
