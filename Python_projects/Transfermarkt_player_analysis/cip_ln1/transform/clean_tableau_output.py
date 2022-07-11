""" Answers to ETL process plan questions
1. Are there particular player performance statistics that correlate strongly with player market value?
2. Do the performance statistics that most influence player value vary from league to league?
3. Is there a correlation between a team’s market value and their total point tally for a season?
"""
import pandas as pd

merged_df = pd.read_csv('../data/fbref_transfermarkt_merged/fbref_transfermarkt_merged.csv', sep=";")
print(merged_df.shape)
print(merged_df.columns)

# Reorder the columns
merged_df = merged_df[['Rk', 'Player', 'Nation', 'Age', 'Squad', 'Comp', 'played_two_leagues', 'Marktvalue',
     'Min', 'Gls', 'Ast', 'xG', 'npxG', 'xA', 'SCA', 'PassLive_SCA','PassDead_SCA','Drib_SCA',
     'Sh_SCA', 'Fld_SCA', 'Def_SCA', 'GCA', 'PassLive_GCA', 'PassDead_GCA', 'Drib_GCA',
     'Sh_GCA','Fld_GCA', 'Def_GCA', 'OG_GCA', 'Tkl', 'TklW', 'Press', 'Succ_Press', 'Blocks',
     'Int', 'Tkl+Int', 'Clr', 'Cmp_Pass', 'Att_Pass', 'TotPrgDist_Pass', '#Prog_Pass',
     'Live_Touches', 'Att_Drib', 'Oppon_Drib', 'TotDist_Carried', 'TotPrgDist_Carried', 'Recep', 'Att_Recep']]

# Check if there is any duplicated cases (same player name and same age)
print(merged_df[merged_df.duplicated(subset=['Player', 'Age'], keep=False)])

# 30 unmatched rows remained after we joined two datasets. These unmatched players have no marktvalue.
# We will check and delete the players who don't have a marktvalue.
print(merged_df[merged_df['Marktvalue'].isnull()].iloc[:, [2, 8]])
print(merged_df['Marktvalue'].isna().sum())

merged_df = merged_df.dropna(subset=['Marktvalue'], inplace=False)
print(merged_df['Marktvalue'].isna().sum())

"""
There are some players whom marktvalue is 0. We had a close look to these players to understand
why their marktvalue is 0. It seems that in general, transfermarkt didnot calculated any marketvalue 
if the player played less than 100 mins. We will check this assumption here.
"""
print(merged_df[merged_df['Marktvalue'] == 0].loc[:, ['Player', 'Min']])
print(merged_df[merged_df['Marktvalue'] == 0].shape)

"""
There are 50 players whom marktvalue is 0. Most of them played less than 100 minutes within the season.
But there are some exceptions. 13 players have not a valid marktvalue,
although played more than 100 minutes within the season:
"""
print(merged_df[(merged_df['Marktvalue'] == 0) & (merged_df['Min'] > 100)].loc[:, ['Player', 'Min']])
print(merged_df[(merged_df['Marktvalue'] == 0) & (merged_df['Min'] > 100)].shape)

""""
It would be wrong to adjust a marketvalue to those players
and they comprise of the less than 2% of whole dataset.
Therefore, these players will be deleted
"""
merged_df = merged_df[merged_df['Marktvalue'] != 0]

#adding Player id into Dataframe
merged_df.insert(0, 'Player_id', range(1, len(merged_df)+1))

print(merged_df.shape, end='\n\n')

print('*'*100, end='\n\n')

merged_df.to_csv('../data/fbref_transfermarkt_merged/final_merged.csv', index=False)
