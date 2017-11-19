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
                plt.xlabel('sponsorship rank')
                plt.ylabel('cosponsorship rank')
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