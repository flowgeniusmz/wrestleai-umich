import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_wrestler_data():
    url = 'https://www.wrestlestat.com/team/40/michigan/profile'

    # Set headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to get data: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Assuming the table has the class 'table-responsive'
    table = soup.find('div', class_='table-responsive')
    if not table:
        print("No table found")
        return

    headers = [th.text.strip() for th in table.find('thead').find_all('th')]
    rows = []
    for tr in table.find('tbody').find_all('tr'):
        cols = tr.find_all('td')
        row_data = [col.text.strip() for col in cols]
        rows.append(row_data)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(rows, columns=headers)

    # Save DataFrame to CSV
    csv_file = 'docs/data/wrestler_tournament_data.csv'
    df.to_csv(csv_file, index=False)
    print(f"Data saved to {csv_file}")

# Call the function
scrape_wrestler_data()
