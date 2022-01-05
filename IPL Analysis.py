#!/usr/bin/env python
# coding: utf-8

# ##### we all watch cricket generally and we all know the Indian premier league (IPL) is the biggest cricket league in the world. Let’s perform the data analysis of IPL with the data of IPL matches from 2008 to 2020. Grab a cup of coffee and let’s begin the hack.
# 
# # Analysis of IPL Data
#    We will go through these main steps for this project:
#    - Import libraries
#    - Load the data
#    - Analyse the data

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as mlt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


matches  = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')


# 

# In[3]:


matches.head(2)


# In[4]:


deliveries.head(2)


# # Some Cleaning and Transforming Data

# In[5]:


matches.drop(['umpire3'], axis=1, inplace=True)  #since all the values are NaN.
deliveries.fillna(0, inplace = True) #filling all NaN the values with 0.


# In[6]:


matches.head(1)  #we can see umpire3 col has been droped from table.


# In[7]:


deliveries.head(1)  # NaN values are filled with 0 in tables.


# In[8]:


#replacing team name with their abbervations in both the files.

matches.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors'],
                
                ['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW'],inplace=True)

deliveries.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW'],inplace=True)


# In[9]:


matches.head(1)


# In[10]:


deliveries.tail(1)


# #### Some basic Analysis

# In[11]:


print('Matches Players:-',matches.shape[0])
print('\n Matches played at Venue:-', matches['venue'].unique())
print('\n Teams:-',matches['team1'].unique())


# In[12]:


print('Total matches played:-',matches['city'].nunique())
print('Total Umpires:-',matches['umpire1'].nunique())


# In[13]:


print((matches['player_of_match'].value_counts()).idxmax(),':Has most of the Player of the Matches Awards')
print((matches['winner'].value_counts()).idxmax(), ': Has most of the of the Matches Wins.')


# In[14]:


df = matches.iloc[[matches['win_by_runs'].idxmax()]]
print('Match with highest run margin win.')
print('Royal Challengers Banglore defeated Gujarat Lions with highest run difference.')
df[['season','date','team1','team2','winner','win_by_runs']]


# In[15]:


df = matches.iloc[[matches['win_by_wickets'].idxmax()]]
print('Match win highest wickets in hand win.')
print('Deccan Chargers defeated Mumbai Indians with highest wickets in hand.')
df[['season','date','team1','team2','winner','win_by_wickets']]


# #### TOSS DECISION

# In[16]:


print('Toss Decision in percentage:',matches['toss_decision'].value_counts()/577*100)


# #### TOSS DECISION ACROSS SEASONS

# In[17]:


sns.countplot(x='season',hue='toss_decision',data=matches)
mlt.show()


# #### MAXIMUM TOSS WINNERS

# In[18]:


ax=matches['toss_winner'].value_counts().plot.bar(width=0.8)
for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x()+0.15, p.get_height()+1))
mlt.show()


# Mumbai Indians seem to be very lucky having the higest win in tosses follwed by Kolkata Knight Riders.Pune Supergiants have the lowest wins as they have played the lowest matches also. This does not show the higher chances of winning the toss as the number of matches played by each team is uneven.
# 

# In[19]:


w=matches['toss_winner'].value_counts()
m=pd.concat([matches['team1'],matches['team2']]).value_counts()
ax=(w/m*100).sort_values().plot.bar(width=0.8,color='#232323')
for p in ax.patches:                       #used to display the values on the top of the bar
    ax.annotate('{:.2f}%'.format(p.get_height()), (p.get_x(), p.get_height()+1),fontsize=9)
mlt.show()


# Now we can see that the chance for winning a toss is highset for DC and it is lowest for PW.

# #### IS TOSS WINNING ALSO A MATCH

# In[20]:


df=matches[matches['toss_winner']==matches['winner']]
slices=[len(df),(577-len(df))]
labels=['yes','no']
mlt.pie(slices,labels=labels,startangle=90,shadow=True,explode=(0,0),autopct='%1.1f%%')
fig = mlt.gcf()
fig.set_size_inches(5,5)
mlt.show()


# Thus the toss winner is not necessarily the match winner. The match winning probablity for toss winnong team is about 50%-50%.

# #### MATCHES PLAYED IN EACH SEASON

# In[21]:


sns.countplot(x='season',data=matches,palette="Set1")  #countplot automatically counts the frequency of an item
print('2011, 2012, 2013 had more teams then other IPL seasons.')


# #### RUNS ACROSS EACH SEASONS

# In[22]:


batsmen = matches[['id','season']].merge(deliveries, left_on = 'id', right_on = 'match_id', how = 'left').drop('id', axis = 1)
#merging the matches and delivery dataframe by referencing the id and match_id columns respectively
season=batsmen.groupby(['season'])['total_runs'].sum()
season.plot()
mlt.show()


# There was a decline in total runs from 2008 to 2009.But there after there was a substantial increase in runs in every season until 2013, but from next season there was a slump in the total runs.

# #### MAXIMUM MEN OF THE MACTHES

# In[23]:


ax = matches['player_of_match'].value_counts().head(10).plot.bar(width=.8, color='red')  #counts the values corresponding 
# to each batsman and then filters out the top 10 batsman and then plots a bargraph 
ax.set_xlabel('player_of_match') 
ax.set_ylabel('count')
for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x()+0.15, p.get_height()+0.25))
mlt.show()
print('Universal Boss reaches the hight of sky.')


# #### WINNER OF EACH SEASONS

# In[24]:


for i in range(2008,2017):
    df=((matches[matches['season']==i]).iloc[-1]) 
    print(df[[1,10]])


# #### MATCHES WON  BY EACH TEAMS

# In[25]:


sns.countplot(x='winner', data=matches)
mlt.xticks(rotation='vertical')
mlt.show()


# Mumbai Indians has won maximum matches.

# #### TEAM1 vs TEAM2
#      - MI vs KKR

# In[26]:


mt1=matches[((matches['team1']=='MI')|(matches['team2']=='MI'))&((matches['team1']=='KKR')|(matches['team2']=='KKR'))]
sns.countplot(x='season', hue='winner', data=mt1)
mlt.xticks(rotation='vertical')
mlt.show()


# MI have defeated KKR in 13 out of 18 matches played between them.Only in the year 2014, KKR won both the matches.Thus in a MI vs KKR match, we know on whom should we bet upon.
# Similar comparisions can be done between any two teams, we just need to change the team names.
# One thing to notice is that MI and KKR have never played against each other in any qualifiers or finals as both of them have played only 2 matches every year, those being the group stage matches.

# #### 200+ SCORES

# In[27]:


high_scores=deliveries.groupby(['match_id', 'inning','batting_team','bowling_team'])['total_runs'].sum().reset_index() 
#reset_index() converts the obtained series into a dataframe
high_scores.nlargest(10,'total_runs')
#nlargest is used to sort the given column


# #### HIGHEST TEAM SCORES IN EACH SEASONS

# In[28]:


high=deliveries.groupby(['match_id', 'inning','batting_team'])['total_runs'].sum().reset_index()
high.set_index(['match_id'],inplace=True)
high['total_runs'].max()
high.columns
high=high.rename(columns={'total_runs':'count'})
high=high[high['count']>200].groupby(['inning','batting_team']).count()
high.T  #transpose


# RCB leads the list with highest number of 200+ scores, maybe due to the Gayle,Kohli,De-Villiers factor.The number of 200+ scores is high in innings 1. This is an indication that if a team scores 200+ in 1st innings, chances of winning is high for them, as in innings 2 very few teams have 200+ score and they may or maynot chase down the target score.

# In[29]:


high_scores=deliveries.groupby(['match_id', 'inning','batting_team','bowling_team'])['total_runs'].sum().reset_index()
high_scores1=high_scores[high_scores['inning']==1]
high_scores2=high_scores[high_scores['inning']==2]
high_scores1=high_scores1.merge(high_scores2[['match_id','inning', 'total_runs']], on='match_id')
high_scores1.rename(columns={'inning_x':'inning_1','inning_y':'inning_2','total_runs_x':'inning1_runs','total_runs_y':'inning2_runs'},inplace=True)
high_scores1=high_scores1[high_scores1['inning1_runs']>=200]
high_scores1['is_score_chased']=1
high_scores1['is_score_chased'] = np.where(high_scores1['inning1_runs']<=high_scores1['inning2_runs'],'yes', 'no')
high_scores1.head(20)


# #### CHANCES OF CHASING 200+ TARGET

# In[30]:


slices=high_scores1['is_score_chased'].value_counts().reset_index().is_score_chased
list(slices)
labels=['target not chased','target chased']
mlt.pie(slices,labels=labels,colors=['#1f2ff3', '#0fff00'],startangle=90,shadow=True,explode=(0,0.1),autopct='%1.1f%%')
fig = mlt.gcf()
fig.set_size_inches(6,6)
mlt.show()


# It seems to be clear that team batting first and scoring 200+ runs, has a very high probablity of winning the match.
# 
# 

# #### TOP 20 BATSMEN

# In[31]:


max_runs=deliveries.groupby(['batsman'])['batsman_runs'].sum()
ax=max_runs.sort_values(ascending=False)[:10].plot.bar(width=0.8,color='Red')
for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x()+0.1, p.get_height()+1),fontsize=11)
mlt.show()


# Virat Kohli has highest total runs across all seasons. Raina is just few runs behind with the second spot
# 
# 

# #### MAXIMUM SIXES

# In[32]:


ax=deliveries[deliveries['batsman_runs']==6].batsman.value_counts()[:10].plot.bar(width=0.8,color='Green')
for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x(), p.get_height()+10))
mlt.show()


# Chris Gayle, the Big Jamaican leads here by a huge margin followed by Rohit Sharma.
# 
# 

# #### TOP INDIVIDUALS SCORES

# In[33]:


top_scores = deliveries.groupby(["match_id", "batsman","batting_team"])["batsman_runs"].sum().reset_index()
top_scores.sort_values('batsman_runs', ascending=0).head(15)


# Not only Gayle but there are many RCB players on the top scores list. Looks like RCB is a very formidable batting side.

# In[34]:


a=batsmen.groupby(['season','batsman'])['batsman_runs'].sum().reset_index()
a=a.groupby(['season','batsman'])['batsman_runs'].sum().unstack().T
a['Total']=a.sum(axis=1)
a=a.sort_values(by='Total',ascending=0)[:5]
a.drop('Total',axis=1,inplace=True)
a.T.plot()
mlt.show()


# In 2016 RCB skipper Virat Kholi scored 4 centuries in a season at total of 973 runs.Virat Kohli's form looks to be improving season by season and it went up very high in the last season. Gayle's form improved in seasons 3-4 but it went down in further seasons. Thus Gayle's form is pretty unpredictable in a season. Other batsman's form looks to slump a bit but recovers in further season.

# ### TOP BOWLERS

# #### HIGHEST WICKET TAKER

# In[35]:


dismissal_kinds = ["bowled", "caught", "lbw", "stumped", "caught and bowled", "hit wicket"]  #since run-out is not creditted to the bowler
ct=deliveries[deliveries["dismissal_kind"].isin(dismissal_kinds)]
ax=ct['bowler'].value_counts()[:10].plot.bar(width=0.8,color='Green')
for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x()+0.10, p.get_height()+1))
mlt.show()


# Lasith Malinga leads the chart, thanks to his unpredictable bowling action. Other bowlers have a very small wicket margin between them.

# #### EXTRA

# In[37]:


extras=deliveries[['wide_runs','bye_runs','legbye_runs','noball_runs']].sum()
sizes=[5161,680,3056,612]
mlt.pie(sizes, labels=['wide_runs','bye_runs','legbye_runs','noball_runs'],
        colors=['Yellow', '#1f2ff3', '#0fff00', 'Red'],explode=(0,0,0,0),autopct='%1.1f%%', shadow=True, startangle=90)
mlt.title("Percentage of Extras")
fig = mlt.gcf()
fig.set_size_inches(6,6)
mlt.plot()
mlt.show()


# #### HOW DO WICKETS HAS BEEN FALL

# In[39]:


dismiss=["run out","bowled", "caught", "lbw", "stumped", "caught and bowled", "hit wicket"]
ct=deliveries[deliveries["dismissal_kind"].isin(dismiss)]
ax=ct.dismissal_kind.value_counts()[:10].plot.bar(width=0.8,color='#005566')
for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x()+0.1, p.get_height()+1))
mlt.show()


# #### TEAM WITH MAXIMUN SIXES

# In[41]:


ax=deliveries[deliveries['batsman_runs']==6].batting_team.value_counts().plot.bar(width=0.8,color='Green')
for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x(), p.get_height()+10))
mlt.show()


# RCB-RCB everywhere. Here too RCB leads with a big margin.

# In[ ]:




