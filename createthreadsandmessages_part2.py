import requests
import json
from openai import OpenAI
import tempfile
import os
import streamlit as st
import time

# Initialize the OpenAI client
client  = OpenAI(api_key=st.secrets.openai.api_key)

assistantid = "asst_SRpP0yzUuXeRkLeXrMVbGyJM"
thread1_id_odds = "thread_jJBoOwjSlCvhaVOOhuljJmhq"
message1_id_odds = "msg_Hqi9SYM9gkN5ZNkEpYT9ZthU"
thread2_id_events = "thread_W8AlCe0GTlOOEovY1gGtApab"
message2_id_events = "msg_qadGyFtLbziki9pYPReh0qry"
tools = [{"type": "code_interpreter"}]
fileids = []

request_headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br'
}
odds_url_path = "https://sportsbook-nash-usil.draftkings.com/sites/US-IL-SB/api/v5/eventgroups/42133?format=json"
events_url_path = "https://sportsbook.draftkings.com/sites/US-IL-SB/api/sportsdata/v1/sports/3/events.json"

# Function to create and write to a temporary file
def create_write_tempfile(suffix, data):
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode='w', encoding='utf-8') as temp_file:
        if suffix == '.json':
            json.dump(data, temp_file)
        else:
            temp_file.write(data)
        temp_file.flush()
        temp_file_path = temp_file.name
        return temp_file_path

# Function to upload the temporary file to OpenAI and return the file ID
def create_openai_file(file_path):
    with open(file_path, "rb") as f:
        openai_file = client.files.create(file=f, purpose='assistants')
    file_id = openai_file.id
    fileids.append(file_id)
    return file_id

# Function to create tools resources
def create_tools_resources():
    toolresources = {"code_interpreter": {"file_ids": fileids}}
    return toolresources

# Function to create attachments for a message
def create_attachments(file_ids, tool_list):
    attachments = [
        {
            "file_id": file_ids,
            "tools": tool_list
        }
    ]
    return attachments

# Fetching the odds data
odds_response = requests.get(url=odds_url_path, headers=request_headers)
odds_data = odds_response.json()

# Creating a temporary file for the odds data
tfile_path = create_write_tempfile('.json', odds_data)

# Uploading the temporary file to OpenAI and getting the file ID
oai_file_id = create_openai_file(file_path=tfile_path)

# Creating a user message with the file attached
user_message1_odds = client.beta.threads.messages.create(
    role="user",
    thread_id=thread1_id_odds,
    content="User Request: Bruins Panthers NHL Game Odds; Attached Files: odds.json",
    attachments=create_attachments(file_ids=oai_file_id, tool_list=tools)
)

# Print the responses for verification
print(f'Temporary JSON file created at: {tfile_path}')
print(f'OpenAI file ID: {oai_file_id}')
print(user_message1_odds)

run1 = client.beta.threads.runs.create(thread_id=thread1_id_odds, assistant_id=assistantid)
while run1.status != 'completed':
    time.sleep(3)
    run1 = client.beta.threads.runs.retrieve(run_id=run1.id, thread_id=thread1_id_odds)
    if run1.status == "completed":
        thread_message_list = client.beta.threads.messages.list(thread_id=thread1_id_odds, run_id=run1.id)
        for thread_message in thread_message_list:
            if thread_message.role == "assistant":
                print(thread_message.content[0].text.value)

# # Repeat the process for events data
# events_response = requests.get(url=events_url_path, headers=request_headers)
# events_data = events_response.json()
# events_tfile_path = create_write_tempfile('.json', events_data)
# events_oai_file_id = create_openai_file(file_path=events_tfile_path)

# # Creating a user message with the events file attached
# user_message2_events = openai.Message.create(
#     role="user",
#     thread_id=thread2_id_events,
#     content="User Request: NHL Events Data; Attached Files: events.json",
#     attachments=create_attachments(file_ids=fileids, tool_list=tools)
# )

# # Print the responses for verification
# print(f'Temporary JSON file created at: {events_tfile_path}')
# print(f'OpenAI file ID: {events_oai_file_id}')
# print(user_message2_events)
