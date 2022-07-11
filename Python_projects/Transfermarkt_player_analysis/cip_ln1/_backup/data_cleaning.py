import pandas as pd
from unidecode import unidecode

df = pd.read_csv("../data/fbref/fbref_player_statistics.csv", index_col=0, encoding="utf-8")

spec_chars = ["de", "eng", "fr", "it"]
for char in spec_chars:
    if char.startswith("d") or char.endswith("a"):
        df['Comp'] = df['Comp'].str[3:]
    else:
        df['Comp'] = df['Comp'].str.replace(char, ' ')

df["Squad"] = df["Squad"].apply(unidecode)
df["Player"] = df["Player"].apply(unidecode)


df.to_csv("_test.csv")
