import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from tempfile import NamedTemporaryFile


class TeamScraper():
    def __init__(self):
        self.url = 'https://www.wrestlestat.com/team/40/michigan/profile'
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
        table = soup.find('div', class_='table-responsive')
        if not table:
            print("No table found")
            return None

        headers = [th.text.strip() for th in table.find('thead').find_all('th')]
        rows = [[td.text.strip() for td in tr.find_all('td')] for tr in table.find('tbody').find_all('tr')]
        return pd.DataFrame(rows, columns=headers)




# # Usage:
# team_scraper = TeamScraper()
# df_team = team_scraper.scrape()
# if df_team is not None:
#     print(df_team)