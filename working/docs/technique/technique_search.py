import streamlit as st
import pandas as pd
from tavily import TavilyClient

# Initialize Tavily client
client = TavilyClient(api_key=st.secrets.tavily.api_key)
path = st.secrets.pathconfig.techniquepath

# Read the CSV file
try:
    df = pd.read_csv(filepath_or_buffer=path)
    print(df)
except Exception as e:
    print(f"Failed to read CSV: {e}")

# Process each row
for index, row in df.iterrows():
    search_query = row['search_query']
    try:
        data = client.search(query=search_query, search_depth="advanced", include_raw_content=True, include_answer=True)
        
        # Assuming 'results' contains a list of dictionaries with the search results
        for i in range(5):  # Example for up to 5 results
            if i < len(data['results']):
                result = data['results'][i]
                df.loc[index, f'result{i+1}_title'] = result.get('title', '')
                df.loc[index, f'result{i+1}_url'] = result.get('url', '')
                df.loc[index, f'result{i+1}_content'] = result.get('content', '')
                df.loc[index, f'result{i+1}_rawcontent'] = result.get('raw_content', '')
                df.loc[index, f'result{i+1}_score'] = result.get('score', '')
            else:
                df.loc[index, f'result{i+1}_title'] = None
                df.loc[index, f'result{i+1}_url'] = None
                df.loc[index, f'result{i+1}_content'] = None
                df.loc[index, f'result{i+1}_rawcontent'] = None
                df.loc[index, f'result{i+1}_score'] = None
        print(f"Row {index} completed successfully.")
    except Exception as e:
        print(f"ERROR in row {index}: {e}")

# Optionally, save the updated DataFrame back to a CSV file
df.to_csv("docs/technique.csv", index=False)
