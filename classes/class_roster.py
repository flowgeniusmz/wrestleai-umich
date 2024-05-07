import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from tempfile import NamedTemporaryFile


class TeamRosterScraper:
    def __init__(self):
        self.url = 'https://www.wrestlestat.com/team/40/michigan/profile'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
        }
      

    def scrape(self):
        # Ensure we start with a fresh temporary file for each scrape
        

        # Fetch the page
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to get data: {response.status_code}")
            return None

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='table table-sm table-hover table-striped')
        if not table:
            print("No table found")
            return None

        # Extract data
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]
        rows = []
        for tr in table.find('tbody').find_all('tr'):
            cols = [td.text.strip() for td in tr.find_all('td')]
            rows.append(cols)

        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers)
        return df
        

   

# #Example usage:
# url = 'https://www.wrestlestat.com/team/40/michigan/profile'  # Adjust the URL to the correct team page
# roster_scraper = TeamRosterScraper()
# df_roster = roster_scraper.scrape()
# if df_roster is not None:
#     print(df_roster)