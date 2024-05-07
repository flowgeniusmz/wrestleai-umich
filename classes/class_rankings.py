import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from tempfile import NamedTemporaryFile

class WrestlerRankingsScraper():
    def __init__(self):
        self.url = 'https://www.wrestlestat.com/d1/rankings/overview'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
        }

    #@st.cache_data
    def scrape(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to get data: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        weight_classes = soup.find_all('div', class_='col-12 col-md-6 col-xl-4')
        data = []

        for weight_class in weight_classes:
            weight = weight_class.find('h3').text.strip()
            rows = weight_class.find_all('tr')

            for row in rows:
                rank = row.find('span', class_='font-weight-bold').text.strip()
                name_link = row.find('a')
                name = name_link.text.strip()
                year_record = row.find('small').text.strip()
                team_link = row.find('td', class_='align-middle text-truncate').find_next_sibling('td').find('a')
                team = team_link.text.strip()
                team_rank = team_link.text.strip().split('#')[1]

                data.append([weight, rank, name, year_record, team, team_rank])

        return pd.DataFrame(data, columns=['Weight Class', 'Rank', 'Wrestler Name', 'Year and Record', 'Team', 'Team Rank'])

# # Usage:
# rankings_scraper = WrestlerRankingsScraper()
# df_rankings = rankings_scraper.scrape()
# if df_rankings is not None:
#     print(df_rankings)