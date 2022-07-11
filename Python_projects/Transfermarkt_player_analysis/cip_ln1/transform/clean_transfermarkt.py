"""
Cleans scraped data from transfermarkt
"""
import pandas as pd
import re
from unidecode import unidecode

"""Clean the scraped marketvalues from scrape_transfermarkt.py"""

# Load
df2 = pd.read_csv("../data/transfermarkt/transfermarkt_player_marketvalue.csv", encoding="utf-8")

# Clean
df2.reset_index()
df2["Player"] = df2["Player"].apply(unidecode)
df2["Team"] = df2["Team"].apply(unidecode)
df2["Marktvalue"]= df2["Marktvalue"].apply(unidecode)

df2['Player'] = df2['Player'].apply(lambda text: re.sub('-', ' ', text))
df2['Marktvalue'] = df2['Marktvalue'].apply(lambda text: re.sub('-', '0', text))
df2['Marktvalue'] = df2['Marktvalue'].apply(lambda text: re.sub('EUR', '', text))
df2['Marktvalue'] = df2['Marktvalue'].apply(lambda text: re.sub('Th.', '000', text))
df2['Marktvalue'] = df2['Marktvalue'].apply(lambda text: re.sub('m', '0.000', text))
df2['Marktvalue'] = df2['Marktvalue'].str.replace('.', '', regex=False)
df2['Player'] = df2['Player'].str.replace("'" ,'', regex=False)
df2['Marktvalue'].astype(int)

#Save
df2.to_csv("../data/transfermarkt/transfermarkt_player_marketvalue_cleaned.csv", index=False)


"""Clean the scraped points and marketvalues from scrape_team_pts_mvalue.py"""

# Load
teams_points_value = pd.read_csv('../data/transfermarkt/teams_points_marketvalue.csv')

# Clean
teams_points_value['marktvalue'] = teams_points_value['marktvalue'].apply(lambda text: re.sub('-', '0', text))
teams_points_value['marktvalue'] = teams_points_value['marktvalue'].apply(lambda text: re.sub('€', '', text))
teams_points_value['marktvalue'] = teams_points_value['marktvalue'].apply(lambda text: re.sub('bn', '0.000.000', text))
teams_points_value['marktvalue'] = teams_points_value['marktvalue'].apply(lambda text: re.sub('m', '0.000', text))
teams_points_value['marktvalue'] = teams_points_value['marktvalue'].str.replace('.', '', regex=False)

teams_points_value['marktvalue'] = teams_points_value['marktvalue'].astype('int')
teams_points_value['points'] = teams_points_value['points'].astype('int')

# adding Team_id column
teams_points_value.insert(0, 'Team_id', range(1, len(teams_points_value)+1))

# Save
teams_points_value.to_csv('../data/transfermarkt/teams_points_marketvalue_cleaned.csv', index=False)

