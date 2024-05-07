import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_wrestling_data():
    url = 'https://www.wrestlestat.com/d1/rankings/overview'  # Ensure this URL is correct for the rankings page

    # Headers to mimic a web browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to get data: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Prepare to collect all wrestlers' data across all weight classes
    weight_classes = soup.find_all('div', class_='col-12 col-md-6 col-xl-4')
    data = []

    # Iterate through each weight class section
    for weight_class in weight_classes:
        weight = weight_class.find('h3').text.strip()  # Extract weight class from the header
        rows = weight_class.find_all('tr')

        # Extract data for each wrestler in the weight class
        for row in rows:
            rank = row.find('span', class_='font-weight-bold').text.strip()
            name_link = row.find('a')
            name = name_link.text.strip()
            year_record = row.find('small').text.strip()
            team_link = row.find('td', class_='align-middle text-truncate').find_next_sibling('td').find('a')
            team = team_link.text.strip()
            team_rank = team_link.text.strip().split('#')[1]

            data.append([weight, rank, name, year_record, team, team_rank])

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=['Weight Class', 'Rank', 'Wrestler Name', 'Year and Record', 'Team', 'Team Rank'])

    # Save DataFrame to CSV
    csv_file = 'docs/data/wrestler_rankings.csv'
    df.to_csv(csv_file, index=False)
    print(f"Data saved to {csv_file}")

# Call the function
scrape_wrestling_data()
