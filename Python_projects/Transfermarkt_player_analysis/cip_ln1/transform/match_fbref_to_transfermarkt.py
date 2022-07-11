"""
Syncs column names from fbref to match those of transfermarkt
"""
import pandas as pd
from difflib import get_close_matches

'''# Intermediate Cleaning Step
Even after cleaning the transfermarkt player names for special characters in tableau the left join operation, 
where the left df is the fbref dataset, we get 169 mismatched names in the fbref data. 

Upon close inspection in Tableau We realize the issue for many of this mismatches is that player names are often 
reported with shorter versions of their name in one data set vs the other, or with middle name vs no middle names in the other.

Due to the diversity of discrepancies in names, the best solution is to perform fuzzy matching. Tableau is reportedly 
poor at this task and thus we decided to perform this intermediate cleaning step in python before returning to Tableau 
to perform the final join between the fbref and transfermarkt data sets.

We use fuzzy matching to find and replace the fbref player name with its trasnfermarkt player name equivalent if possible.
After we import the new fbref table with the more harmonized player names back into Tableau to perform the final merge.'''

# Loading Transfermarkt data cleaned in Tableau + fbref data cleaned in pycharm
transfermarkt_df = pd.read_csv('../data/transfermarkt/transfermarkt_player_marketvalue_cleaned.csv')
fbref_df = pd.read_csv('../data/fbref/fbref_player_statistics.csv')

# Using fuzzy matching to replace player names in fbref data with transfermarkt variation if available
harmonized_names = []
matched_pairs = dict() #to control quality of match and effects of varying cutoff param we create matched_pairs dic + a no_match list
no_match = []
for i in fbref_df['Player']:
    close_match = get_close_matches(word=i, possibilities=transfermarkt_df['Player'], n=1, cutoff=.6)
    if close_match:
        matched_pairs[i] = close_match[0]
        harmonized_names.append(close_match[0])
    else:
        no_match.append(i)
        harmonized_names.append(i)

# Controlling quality of match
print(len(matched_pairs))

# show inexact matches.
sortedDict = dict(sorted(matched_pairs.items(), key=lambda x: x[0].lower()))
i = 0
for k, v in sortedDict.items():
    if k != v:
        print('{}:{}'.format(k, v))
        i += 1
print("# of inexact matches: " + str(i))

# using inexact matches dict to manually create list 'wrong_matches'. We will then replace the player name in fbref
# if a close match was found in the transfermarkt player names, which is not in the wrong_matches list.

wrong_matches = [
    'Alejandro Baena', 'Alejandro Blesa', 'Anderson Lima', 'Antonio Cortes', 'Baba Rahman', 'Cauly Oliveira Souza',
    'Churripi', 'Dalbert Henrique', 'Danilo Larangeira', 'Edmilson Indjai', 'Espeto', 'Ezequiel Avila',
     'Felipe dal Belo', 'Fernando Marcal', 'Fernando Nino', 'Fernando', 'Gabriel Dos Santos', 'Gleison Bremer',
     'Jonny Castro', 'Jose Holebas', 'Kike', 'Lee Kangin', 'Louis Beyer', 'Mathias Jorgensen', 'Moanes Dabour',
     'Nico Ribaudo', 'Obite NDicka', 'Opoku Ampomah', 'Raphael Dias Belloli', 'Raul', 'Thiago Alcantara'
     'Thomas Doyle', 'Victor Perea', 'Vitorino Hilton', 'Yoel']

j = -1
for i in fbref_df['Player']:
    j += 1
    if i not in wrong_matches:
        fbref_df.loc[(fbref_df.Player == i), 'Player'] = harmonized_names[j]

#drop index wrongly taken as column
fbref_df.drop('Unnamed: 0', axis=1, inplace=True)

# Saving Player name harmonized fb_ref data frame to csv
fbref_df.to_csv('../data/fbref/fbref_player_statistics_fuzzy.csv')
