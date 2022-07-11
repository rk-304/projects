""" Cleaning process
1. 5 .csv files were copied from fbref.com
2. Select columns
3. Clean in two steps
4. Merge dfs
5. Save to .cvs
"""
import pandas as pd
import numpy as np
from collections import Counter
from functools import reduce

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

""" Load
Performance statistics from fbref.com are available in 5 separate csv files. 
Below we load them as dfs and name them.
"""

overall = pd.read_csv("../data/fbref/standard_stats.csv", header=[0, 1], sep=";", engine='python')
chance_creation = pd.read_csv("../data/fbref/goal_and_shot.csv", header=[0, 1], sep=";", engine='python')
defense = pd.read_csv("../data/fbref/defensive_actions.csv", header=[0, 1], sep=";", engine='python')
passing = pd.read_csv("../data/fbref/player_passing.csv", header=[0, 1], sep=";", engine='python')
possession = pd.read_csv("../data/fbref/player_possession.csv", header=[0, 1], sep=";", engine='python')

""" Column selection 
driven by domain knowledge + aggregation enabling (total columns reduced from 118 to 45)
overall: Unnamed: Player, Nation, Pos, Age; Playing Time: Min; Performance, Performance: Gls, Ast; Expected: take All
per 90 Minutes: ignore All
chance_creation: SCA: SCA; SCA Types: take ALL; GCA: GCA; GCA Types: take All
defense: Vs Dribbles: ignore ALL; Tackles: Tkl, TklW; Pressures: Press, Succ; Blocks: Blocks, Int, Clr, Err
passing: Total: Cmp, Att, PrgDist; Long: Prog
possession: Touches: Live; Dribbles: Att, #Pl; Carries: TotDist, PrgDist; Receiving: Targ,Rec
"""

overall_subset = overall[
    [('Unnamed: 0_level_0', 'Rk'), ('Unnamed: 1_level_0', 'Player'), ('Unnamed: 2_level_0', 'Nation'),
     ('Unnamed: 3_level_0', 'Pos'), ('Unnamed: 4_level_0','Squad'), ('Unnamed: 5_level_0', 'Comp'),
     ('Unnamed: 6_level_0', 'Age'), ('Playing Time', 'Min'), ('Performance', 'Gls'), ('Performance', 'Ast'),
     ('Expected', 'xG'), ('Expected', 'npxG'), ('Expected', 'xA')]]

chance_creation_subset = chance_creation[
    [('SCA', 'SCA'), ('SCA Types', 'PassLive'), ('SCA Types', 'PassDead'), ('SCA Types', 'Drib'),
     ('SCA Types', 'Sh'), ('SCA Types', 'Fld'), ('SCA Types', 'Def'), ('GCA', 'GCA'), ('GCA Types', 'PassLive'),
     ('GCA Types', 'PassDead'), ('GCA Types', 'Drib'), ('GCA Types', 'Sh'), ('GCA Types', 'Fld'),
     ('GCA Types', 'Def'), ('GCA Types', 'OG')]]

defense_subset = defense[
    [('Tackles', 'Tkl'), ('Tackles', 'TklW'), ('Pressures', 'Press'), ('Pressures', 'Succ'), ('Blocks', 'Blocks'),
     ('Unnamed: 28_level_0', 'Int'), ('Unnamed: 29_level_0', 'Tkl+Int'), ('Unnamed: 30_level_0', 'Clr')]]

passing_subset = passing[
    [('Total', 'Cmp'), ('Total', 'Att'), ('Total', 'PrgDist'), ('Unnamed: 30_level_0', 'Prog')]]

possession_subset = possession[
    [('Touches', 'Live'), ('Dribbles', 'Att'), ('Dribbles', '#Pl'), ('Carries', 'TotDist'),
     ('Carries', 'PrgDist'), ('Receiving', 'Targ'), ('Receiving', 'Rec')]]

""" Merge
Combine the reduce and lambda functions to merge all 5 subset dfs in one go
"""
data_frames = [overall_subset, chance_creation_subset, defense_subset, passing_subset, possession_subset]
merged = reduce(
    lambda left, right: pd.merge(
        left,
        right[right.columns.difference(left.columns)],
        left_index=True, right_index=True), data_frames)

""" Cleaning
"""

merged[('Unnamed: 1_level_0', 'Player')] = merged[('Unnamed: 1_level_0', 'Player')].str.split('\\', expand=True)[1]
merged[('Unnamed: 1_level_0', 'Player')] = merged[('Unnamed: 1_level_0', 'Player')].str.replace("-", " ")
merged[('Unnamed: 2_level_0', 'Nation')] = merged[('Unnamed: 2_level_0', 'Nation')].str.split(' ', expand=True)[1]
merged[('Unnamed: 3_level_0', 'Pos')] = merged[('Unnamed: 3_level_0', 'Pos')].str[0:2]

# Changing Age from float to int64
merged[('Unnamed: 6_level_0', 'Age')].fillna(0, inplace=True)  # else you cannot conver to int due to NA values
merged[('Unnamed: 6_level_0', 'Age')] = merged[('Unnamed: 6_level_0', 'Age')].astype(np.int64)

# Changing Squad from Object to String type to facilitate groupby sum of duplicates
merged[('Unnamed: 5_level_0', 'Comp')] = merged[('Unnamed: 5_level_0', 'Comp')].astype(str)

# Cleaning lower characters from league names
spec_chars = ["de", "eng", "fr", "it"]
for char in spec_chars:
    if char.startswith("d") or char.endswith("a"):
        merged[('Unnamed: 5_level_0', 'Comp')] = merged[('Unnamed: 5_level_0', 'Comp')].str[3:]
    else:
        merged[('Unnamed: 5_level_0', 'Comp')] = merged[('Unnamed: 5_level_0', 'Comp')].str.replace(char, ' ')

""" Removing level 0 column names and renaming level 1 column names to avoid confusion
to avoid naming conflict during rename procedure (many level 1 columns have same name and its not possible to input
multiindex column names into the rename function), we have to make sure each columnname name is unique before renaming
by combining level 0 and level 1 column names.
"""
merged.columns = merged.columns.to_flat_index()

# Follow the steps below to automate the renaming procedure
dic = {
    "('GCA Types', 'Def')":'Def_GCA',
    "('GCA Types', 'Drib')":'Drib_GCA',
    "('GCA Types', 'Fld')":'Fld_GCA',
    "('GCA Types', 'OG')":'OG_GCA',
    "('GCA Types', 'PassDead')":"PassDead_GCA",
    "('GCA Types', 'PassLive')":'PassLive_GCA',
    "('GCA Types', 'Sh')":'Sh_GCA',
    "('SCA Types', 'Def')":'Def_SCA',
    "('SCA Types', 'Drib')":'Drib_SCA',
    "('SCA Types', 'Fld')":'Fld_SCA',
    "('SCA Types', 'PassDead')":'PassDead_SCA',
    "('SCA Types', 'PassLive')":'PassLive_SCA',
    "('SCA Types', 'Sh')":'Sh_SCA',
    "('Pressures', 'Succ')":'Succ_Press',
    "('Total', 'Att')":'Att_Pass',
    "('Total', 'Cmp')": 'Cmp_Pass',
    "('Total', 'PrgDist')":'TotPrgDist_Pass',
    "('Unnamed: 30_level_0', 'Prog')":'#Prog_Pass',
    "('Carries', 'PrgDist')":'TotPrgDist_Carried',
    "('Carries', 'TotDist')":'TotDist_Carried',
    "('Dribbles', '#Pl')":'Oppon_Drib',
    "('Dribbles', 'Att')":'Att_Drib',
    "('Receiving', 'Rec')":'Recep',
    "('Receiving', 'Targ')":'Att_Recep',
    "('Touches', 'Live')": 'Live_Touches'}

cols_flat = list(merged.columns)
cols_new = []
for i in cols_flat:
    if str(i) in dic:
        cols_new.append(dic[str(i)])
    else:
        cols_new.append(i[1])

renaming_dict = dict(zip(cols_flat, cols_new))
merged.rename(columns=renaming_dict, inplace=True)

# There are two kinds of duplicates on player (name) column.
# 1. Different players with the same name (age & nation are different). This kind of name duplicates will be kept.
print(merged[merged.duplicated('Player', keep=False)].iloc[6:8, :7])
# 2. Player changing squads mid season (age & nation are same). These duplicates will be removed
print(merged[merged.duplicated(subset=['Player', 'Age', 'Nation'], keep=False)].iloc[:4, :7])

# The code below confirms that all the duplicated rows we are dealing with are due to a player changing squads mid season
print(Counter(merged.duplicated(subset=['Player', 'Age', 'Nation'])))
print(Counter(merged.duplicated(subset=['Player', 'Age', 'Nation', 'Squad'])))

# Check for missing values in age and nation columns
print('whole dataset')
print('# missing values in age column: ' + str(merged['Age'].isna().sum()))
print('# missing values in nation column: ' + str(merged['Nation'].isna().sum()))
print('duplicated cases')
print('# missing values in nation column: ' +
      str(merged[merged.duplicated(subset=['Player', 'Age'], keep=False)]['Nation'].isna().sum()))

# Filling missing value in Nation column with NotKnown.
merged['Nation'] = merged['Nation'].fillna("NotKnown")

"""
because of our target analysis (realtionships between a players performance stats and his market value) we want to have
each individual player stats aggregated always into a single row instead of spread across two because of the two clubs
a player played for.
look at a and b output dfs to understand better how the code below works
"""

a = merged.groupby(by=['Player', 'Nation', 'Age']).agg({'Squad': ' / '.join, 'Comp': ' / '.join}, )
b = merged.groupby(by=['Player', 'Nation', 'Age']).sum()
merged_clean = pd.merge(a, b, on=['Player', 'Nation', 'Age'], how='inner')

# Bring table back to original order
merged_clean = merged_clean.reset_index().sort_values('Rk')
merged_clean.index = pd.RangeIndex(start=0, stop=2613, step=1)
print(merged_clean.shape)

# ## recode league column in aggregated rows.
print("Before recoding")
print(merged_clean.iloc[[46, 136, 47], [0, 4]])

# Players that changed club mid season but stayed in the same league have now under comp the same league twice
# Separated by a /. This is redundant info, thus the code below removes the duplicated league after the / for those cases
merged_clean['Comp'] = np.where((merged_clean['Comp'].str.contains("/")) &
          (merged_clean['Comp'].str.split('/', expand=True)[0].str.strip() ==
           merged_clean['Comp'].str.split('/', expand=True)[1].str.strip()),
         merged_clean['Comp'].str.split('/', expand=True)[0], merged_clean['Comp']
        )

print("After recoding")
print(merged_clean.iloc[[46, 136, 47], [0, 4]])

"""
we flag the players which played in two different leagues within the same season. We will not use
them in our analysis because they are a negligible amount of observations (64 out ofm roughly 3000 observations)
and make the task of answering our question regarding differences among the value attached to certain peformance metrics
across leagues significantly more complex to answer.
"""

merged_clean['played_two_leagues'] = np.where(merged_clean['Comp'].str.contains("/"), True, False)
print("# players played in two different leagues: " + str(sum(merged_clean['played_two_leagues'])))
print(merged_clean.shape)

# Save
merged_clean.to_csv('../data/fbref/fbref_player_statistics.csv')
