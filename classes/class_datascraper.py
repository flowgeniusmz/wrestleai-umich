import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from tempfile import NamedTemporaryFile
import os

def create_temp_file(suffix=".csv"):
    """
    Create a named temporary file that persists until manually deleted.
    Returns the file handle and the file path.
    
    :param suffix: String, the file extension to use for the temporary file.
    :return: tuple(file object, file path)
    """
    # Create a named temporary file
    temp_file = NamedTemporaryFile(delete=False, suffix=suffix, mode='w+', encoding='utf-8')
    return temp_file, temp_file.name



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
# team_scraper = TeamScraper('https://www.wrestlestat.com/team/40/michigan/profile')
# df_team = team_scraper.scrape()
# if df_team is not None:
#     print(df_team)



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



class TeamRosterScraper:
    def __init__(self):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
        }
        # Setting up the temporary file
        self.temp_file = NamedTemporaryFile(delete=False, suffix='.csv', mode='w+', dir='./temp')

    def scrape(self):
        # Ensure we start with a fresh temporary file for each scrape
        self.temp_file.close()
        os.unlink(self.temp_file.name)
        self.temp_file = NamedTemporaryFile(delete=False, suffix='.csv', mode='w+', dir='./temp')

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
        df.to_csv(self.temp_file.name, index=False)
        print(f"Data saved to {self.temp_file.name}")
        return df

    def __del__(self):
        # Ensure to clean up the temporary file
        os.unlink(self.temp_file.name)

#Example usage:
url = 'https://www.wrestlestat.com/team/40/michigan/profile'  # Adjust the URL to the correct team page
roster_scraper = TeamRosterScraper()
df_roster = roster_scraper.scrape()
if df_roster is not None:
    print(df_roster)

