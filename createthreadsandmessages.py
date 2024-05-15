import streamlit as st
from openai import OpenAI
import requests
import json



client = OpenAI(api_key=st.secrets.openai.api_key)
assistantid = "asst_SRpP0yzUuXeRkLeXrMVbGyJM"
thread1_id_odds = "thread_jJBoOwjSlCvhaVOOhuljJmhq"
thread2_id_events = "thread_W8AlCe0GTlOOEovY1gGtApab"


content1 = """**** NEXT STEP: ANALYZE ODDS.JSON FILE USING THE FOLLOWING INSTRUCTIONS ****
# Converting JSON Data into a Flat DataFrame and Searching for Keywords

## Instructions

1. **Load the JSON Data**: Read the JSON data into a Python dictionary.
2. **Flatten the Data**: Extract relevant data from nested structures and organize it into a flat structure.
3. **Convert to DataFrame**: Use pandas to convert the flat structure into a DataFrame.
4. **Keyword Search**: Implement a function to search for keywords across all columns in the DataFrame.

## Pseudocode

### Load JSON Data:
1. Import necessary libraries.
2. Read the JSON file.

### Flatten the Data:
1. Initialize a list to store flattened data.
2. Loop through the nested structures to extract relevant fields.

### Convert to DataFrame:
1. Convert the list of flattened data into a pandas DataFrame.

### Keyword Search:
1. Define a function that takes a DataFrame and a list of keywords.
2. Search for keywords across all columns in the DataFrame.
3. Return rows containing the keywords.

## Python Code

```python
import json
import pandas as pd

# Step 1: Load JSON Data
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Step 2: Flatten the Data
def flatten_data(data):
    flat_data = []
    for event in data['eventGroup']['events']:
        event_id = event['eventId']
        event_name = event['name']
        event_start_date = event['startDate']
        team1_name = event['team1']['name']
        team2_name = event['team2']['name']
        
        for offer_category in data['eventGroup']['offerCategories']:
            for subcategory in offer_category['offerSubcategoryDescriptors']:
                for offer_list in subcategory['offerSubcategory']['offers']:
                    for offer in offer_list:
                        for outcome in offer['outcomes']:
                            flat_data.append({
                                'event_id': event_id,
                                'event_name': event_name,
                                'event_start_date': event_start_date,
                                'team1_name': team1_name,
                                'team2_name': team2_name,
                                'offer_category': offer_category['name'],
                                'offer_subcategory': subcategory['name'],
                                'offer_label': offer['label'],
                                'outcome_label': outcome['label'],
                                'odds_american': outcome['oddsAmerican'],
                                'odds_decimal': outcome['oddsDecimal'],
                                'odds_fractional': outcome['oddsFractional'],
                                'participant': outcome.get('participant', ''),
                                'line': outcome.get('line', '')
                            })
    return flat_data

# Step 3: Convert to DataFrame
def create_dataframe(flat_data):
    df = pd.DataFrame(flat_data)
    return df

# Step 4: Keyword Search
def search_keywords(df, keywords):
    mask = pd.concat([df[col].astype(str).str.contains('|'.join(keywords), case=False, na=False) for col in df], axis=1).any(axis=1)
    return df[mask]

# Main function to execute the steps
def main(file_path, keywords):
    data = load_json(file_path)
    flat_data = flatten_data(data)
    df = create_dataframe(flat_data)
    result_df = search_keywords(df, keywords)
    return result_df

# Example usage
file_path = '/mnt/data/odds.json'
keywords = ['Hurricanes', 'Rangers', 'Over', 'Under']

result_df = main(file_path, keywords)
print(result_df)
```

# Detailed Explanation

## Load JSON Data
The `load_json` function reads the JSON file and returns the data as a dictionary.

## Flatten the Data
The `flatten_data` function navigates through nested structures in the JSON, extracting relevant fields and appending them to a list of dictionaries.

## Convert to DataFrame
The `create_dataframe` function converts the list of dictionaries into a pandas DataFrame.

## Keyword Search
The `search_keywords` function searches for keywords across all columns of the DataFrame and returns the rows where any column contains the keywords.

## Main Function
The `main` function integrates all steps, loading the data, flattening it, creating a DataFrame, and performing the keyword search. The final result is a DataFrame containing rows with the specified keywords.

"""


content2 = """**** NEXT STEP: ANALYZE EVENTS.JSON FILE USING THE FOLLOWING INSTRUCTIONS ****
## Converting JSON Data from `events.json` into a Flat DataFrame and Searching for Keywords

### Instructions
1. **Load the JSON Data**: Read the JSON data into a Python dictionary.
2. **Flatten the Data**: Extract relevant data from nested structures and organize it into a flat structure.
3. **Convert to DataFrame**: Use pandas to convert the flat structure into a DataFrame.
4. **Keyword Search**: Implement a function to search for keywords across all columns in the DataFrame.

### Pseudocode

1. **Load JSON Data**:
   - Import necessary libraries.
   - Read the JSON file.
2. **Flatten the Data**:
   - Initialize a list to store flattened data.
   - Loop through the nested structures to extract relevant fields.
3. **Convert to DataFrame**:
   - Convert the list of flattened data into a pandas DataFrame.
4. **Keyword Search**:
   - Define a function that takes a DataFrame and a list of keywords.
   - Search for keywords across all columns in the DataFrame.
   - Return rows containing the keywords.

### Python Code

```python
import json
import pandas as pd

# Step 1: Load JSON Data
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Step 2: Flatten the Data
def flatten_data(data):
    flat_data = []
    for event in data['events']:
        event_id = event['eventId']
        event_name = event['name']
        event_start_time = event['startTime']
        away_team_name = event['awayTeam']['name']
        home_team_name = event['homeTeam']['name']
        status = event['status']
        score_away = event['score']['awayTeamScore']
        score_home = event['score']['homeTeamScore']
        
        flat_data.append({
            'event_id': event_id,
            'event_name': event_name,
            'event_start_time': event_start_time,
            'away_team_name': away_team_name,
            'home_team_name': home_team_name,
            'status': status,
            'score_away': score_away,
            'score_home': score_home
        })
        
        if 'venue' in event['eventDetails']:
            venue_name = event['eventDetails']['venue'].get('name', '')
            venue_city = event['eventDetails']['venue'].get('city', '')
            venue_state = event['eventDetails']['venue'].get('state', '')
            flat_data[-1].update({
                'venue_name': venue_name,
                'venue_city': venue_city,
                'venue_state': venue_state
            })
        
        # Add player details if available
        if 'awayTeamGameInfo' in event['eventDetails']:
            away_goalie_info = event['eventDetails']['awayTeamGameInfo'].get('goalie', {})
            if away_goalie_info:
                flat_data[-1].update({
                    'away_goalie_name': away_goalie_info.get('name', ''),
                    'away_goalie_position': away_goalie_info.get('playerDetails', {}).get('position', ''),
                    'away_goalie_jersey_number': away_goalie_info.get('playerDetails', {}).get('jerseyNumber', '')
                })
                
        if 'homeTeamGameInfo' in event['eventDetails']:
            home_goalie_info = event['eventDetails']['homeTeamGameInfo'].get('goalie', {})
            if home_goalie_info:
                flat_data[-1].update({
                    'home_goalie_name': home_goalie_info.get('name', ''),
                    'home_goalie_position': home_goalie_info.get('playerDetails', {}).get('position', ''),
                    'home_goalie_jersey_number': home_goalie_info.get('playerDetails', {}).get('jerseyNumber', '')
                })
        
    return flat_data

# Step 3: Convert to DataFrame
def create_dataframe(flat_data):
    df = pd.DataFrame(flat_data)
    return df

# Step 4: Keyword Search
def search_keywords(df, keywords):
    mask = pd.concat([df[col].astype(str).str.contains('|'.join(keywords), case=False, na=False) for col in df], axis=1).any(axis=1)
    return df[mask]

# Main function to execute the steps
def main(file_path, keywords):
    data = load_json(file_path)
    flat_data = flatten_data(data)
    df = create_dataframe(flat_data)
    result_df = search_keywords(df, keywords)
    return result_df

# Example usage
file_path = '/mnt/data/events.json'  # Replace with your file path
keywords = ['Coyotes', 'Kings', 'Final', 'Toronto']

result_df = main(file_path, keywords)
print(result_df)
```
# Detailed Explanation

## Load JSON Data
- The `load_json` function reads the JSON file and returns the data as a dictionary.

## Flatten the Data
- The `flatten_data` function navigates through nested structures in the JSON, extracting relevant fields and appending them to a list of dictionaries.
- It includes handling of optional fields like `venue`, `awayTeamGameInfo`, and `homeTeamGameInfo` if they exist.

## Convert to DataFrame
- The `create_dataframe` function converts the list of dictionaries into a pandas DataFrame.

## Keyword Search
- The `search_keywords` function searches for keywords across all columns of the DataFrame and returns the rows where any column contains the keywords.

## Main Function
- The `main` function integrates all steps, loading the data, flattening it, creating a DataFrame, and performing the keyword search.
- The final result is a DataFrame containing rows with the specified keywords.

"""

message1 = client.beta.threads.messages.create(role="assistant", thread_id=thread1_id_odds, content=content1)
message2 = client.beta.threads.messages.create(role="assistant", thread_id=thread2_id_events, content=content2)
print(message1.id)
print(message2.id)
# client.beta.threads.messages.delete(message_id="msg_IRLwkk7bAQ1rogOdggsRWA7k", thread_id=thread1_id_odds)
# client.beta.threads.messages.delete(message_id="msg_Wmo25Hd8v9hIn12AXyOomzW4", thread_id=thread2_id_events)