""" Scrape Team Points and Marketvalue
This script gets the data to answer question 3.
It gets the points and the marketvalue of each team.

1. Get link of each league
2. Loop to each team in the league and save to df
3. Clean values with regex
4. Save to .csv
"""
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

myheaders = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \ '
        'AppleWebKit/537.36 (KHTML, like Gecko) \ '
        'Chrome/84.0.4147.89 Safari/537.36', }

url: str = "https://www.transfermarkt.com/wettbewerbe/europa"
http: str = "https://www.transfermarkt.com"

html_page = requests.get(url, headers=myheaders)
soup = BeautifulSoup(html_page.content, 'lxml')

# 1. Get the link for each league
leagues = ["Premier League", "Serie A", "LaLiga", "Bundesliga", "Ligue 1"]
row = soup.find("div", class_="responsive-table").find_all("td", class_="hauptlink")
saison = "/plus/?saison_id=2019"
league_links = []
for i in range(1, 20, 2):
    if row[i].find_all("a", href=True, text=True)[0].get_text() in leagues:
        name = row[i].find_all("a", href=True, text=True)[0].get_text()
        link = http + row[i].find_all("a", href=True, text=True)[0]['href'] + saison
        league_links.append(link)
    time.sleep(1)

leagues_dict = dict(zip(leagues, league_links))

# 2. Save the name, point and transfermarkt value of each team
all_leagues_team_names, all_leagues_team_marketvalues, all_leagues_team_names_2, all_leagues_team_points = \
    [], [], [], []

all_leagues = {}
for league, url in leagues_dict.items():
    league_page = requests.get(url, headers=myheaders)
    soup = BeautifulSoup(league_page.content, 'lxml')
    table = soup.find("div", {"id": "yw1"})
    row = table.select(".odd, .even")
    team_names = []
    team_marketvalue = []
    for i in range(len(row)):
        name = row[i].find_all("td")[0].find("img")["alt"]
        value = row[i].find_all("td")[8].text
        team_marketvalue.append(value)
        team_names.append(name)
        time.sleep(1)
    all_leagues_team_marketvalues.extend(team_marketvalue)
    all_leagues_team_names.extend(team_names)

    table_2 = soup.find("div", {"class": "box tab-print"}).find("div", {"class": "responsive-table"})
    row_2 = table_2.find("tbody").find_all("tr")
    team_names_2 = []
    team_points = []
    for i in range(len(row_2)):
        name_2 = row_2[i].find_all("td")[1].find("img")["alt"]
        points = row_2[i].find_all("td")[5].text
        team_names_2.append(name_2)
        team_points.append(points)
    all_leagues_team_names_2.extend(team_names_2)
    all_leagues_team_points.extend(team_points)
    all_leagues[league] = team_names
    time.sleep(1)

# Create df
team_marktvalue_tuple = list(zip(all_leagues_team_names, all_leagues_team_marketvalues))
team_points_tuple = list(zip(all_leagues_team_names_2, all_leagues_team_points))

# Create dataframe for each tuple lists and merge the dataframes.
m_df = pd.DataFrame(team_marktvalue_tuple, columns=["team", "marktvalue"])
p_df = pd.DataFrame(team_points_tuple, columns=["team", "points"])
teams_points_value = pd.merge(m_df, p_df, on="team")

# Add league information into dataframe
l_pd = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in all_leagues.items()]))
l_pd = pd.melt(l_pd, var_name='league', value_name='team')
teams_points_value = pd.merge(teams_points_value, l_pd, on="team")

# Save
teams_points_value.to_csv('../data/transfermarkt/teams_points_marketvalue.csv', index=False)
