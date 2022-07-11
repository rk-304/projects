""" Scraping process
This script scrapes the player marektvalue
1. Get each league link
2. Get each team within a league
3. Get each player within a team
"""
import csv
import re
import requests
import time
from bs4 import BeautifulSoup
from typing import Dict

myheaders: Dict[str, str] = {
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
        print(i)
    time.sleep(1)

# 2. Get all links team links
all_leagues_team_links, all_leagues_team_names = [], []
for url in league_links:
    league_page = requests.get(url, headers=myheaders)
    soup = BeautifulSoup(league_page.content, 'lxml')
    table = soup.find("div", {"id": "yw1"})
    row = table.select(".odd, .even")
    team_links = []
    team_names = []
    for i in range(len(row)):
        link = http + row[i].find_all("td")[3].find_all("a", href=True, text=True)[0]['href']
        team_links.append(link)
        name = row[i].find_all("td")[3].find_all("a", href=True, text=True)[0]['title']
        team_names.append(name)
        time.sleep(1)
    print(url)
    all_leagues_team_links.append(team_links)
    all_leagues_team_names.append(team_names)
    time.sleep(1)

leagues_teams = dict(zip(leagues, all_leagues_team_names))
leagues_links2 = dict(zip(leagues, all_leagues_team_links))

# 3. Get each player row
csv_file = open("../data/transfermarkt/transfermarkt_player_marketvalue.csv", "w", newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Player", "Marktvalue", "Age", "Team", "League"])
for i in leagues:
    for j in range(len(leagues_teams[i])):
        link = leagues_links2[i][j]
        team_page = requests.get(link, headers=myheaders)
        soup = BeautifulSoup(team_page.content, 'lxml')
        table=soup.find("div", {"id": "yw1"})
        row = table.select(".odd, .even")
        for k in range(len(row)):
            Player = row[k].find("tr").find_all("a", href=True, text=True)[0]['title'].replace("-", " ")
            Marktvalue = row[k].find_all("td", class_="rechts hauptlink")[0].get_text()
            birthdate = row[k].find("td", class_="zentriert", string=re.compile('\(')).get_text()
            Age = birthdate.split('(')[1][:2]
            Team = leagues_teams[i][j]
            League = i
            player_row = [Player, Marktvalue, Age, Team, League]
            csv_writer.writerow(player_row)
        print(j)
        time.sleep(1)
csv_file.close()
