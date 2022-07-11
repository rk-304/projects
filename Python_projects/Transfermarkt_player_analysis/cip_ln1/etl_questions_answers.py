""" Answers to ETL process plan questions
1. Are there particular player performance statistics that correlate strongly with player market value?
2. Do the performance statistics that most influence player value vary from league to league?
3. Is there a correlation between a team’s market value and their total point tally for a season?
"""
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

merged_df = pd.read_csv('./data/fbref_transfermarkt_merged/final_merged.csv', sep=",")

"""1. Are there particular player performance statistics that correlate strongly with player market value?
"""
print('Questions')
print('1. Are there particular player performance statistics that correlate strongly with player market value?',
      end='\n\n')

# Correlation analysis
# Select the performance statistics and marktvalue columns

df_numeric = merged_df.iloc[:, 8:]
marktvalue= df_numeric.iloc[:, 0]
performance_stats = df_numeric.iloc[:, 1:]
print(marktvalue.shape)
print(performance_stats.shape)

# Correlation between marktvalue and all other performance statistics
corr_with_marktvalue = performance_stats.corrwith(marktvalue)
print(corr_with_marktvalue.sort_values(ascending=False), end='\n\n')
# top 5 is Att_Recep, GCA, PassLive_GCA, Recep, xA

# Corr Heatmap
corr = df_numeric.corr()
sns.set_style(style="white")
corr = df_numeric.corr().round(1)
mask = np.triu(np.ones_like(corr, dtype=bool), 1)

fig, axs = plt.subplots(figsize=(50, 50))
sns.heatmap(
    data=corr,
    mask=mask,
    annot=False,
    vmin=-1,
    vmax=1,
    center=0,
    cmap='RdBu_r',
    square=True,
    cbar_kws={"shrink": 1}, )
plt.show()
fig.savefig("Correlation_heatmap_Q1.png")

"""2. Do the performance statistics that most influence player value vary from league to league?
"""
print('2. Do the performance statistics that most influence player value vary from league to league?',
      end='\n\n')

leagues = ['La Liga', 'Premier League', 'Ligue 1', 'Serie A', 'Bundesliga']
for league in leagues:
    performance_stats = merged_df[merged_df['Comp'] == league].iloc[:, 9:]
    marktvalue = merged_df[merged_df['Comp'] == league]['Marktvalue']
    corr_with_marktvalue = performance_stats.corrwith(marktvalue)
    print(league, ':')
    print(corr_with_marktvalue.sort_values(ascending=False)[:5], end='\n\n')

"""3. Is there a correlation between a team’s market value and their total point tally for a season?
"""
df = pd.read_csv('data/transfermarkt/teams_points_marketvalue_cleaned.csv')

# Correlation Heatmap
sns.set_style(style="white")
corr = df.corr().round(1)
mask = np.triu(np.ones_like(corr, dtype=bool), 1)

fig, axs = plt.subplots(figsize=(50, 50))
sns.heatmap(
    data=corr,
    mask=mask,
    annot=True,
    vmin=-1,
    vmax=1,
    center=0,
    cmap='RdBu_r',
    square=True,
    cbar_kws={"shrink": 1}, )
plt.savefig('Heatmap.png')
#plt.show()

# Scatter
fig = px.scatter(df, y='points', x='marktvalue', color='league', hover_data=['team'])
fig.show()
fig.write_html("Scatter_plot.html")
