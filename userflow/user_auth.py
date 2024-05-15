import streamlit as st
from supabase import create_client, Client
import re
from openai import OpenAI

class User():
    def __init__(self):
        self.Client = create_client(supabase_url=st.secrets.supabase.url, supabase_key=st.secrets.supabase.api_key_admin)
        self.table = st.secrets.supabase.users_table
        self.username_column = st.secrets.supabase.username_column
        self.password_column = st.secrets.supabase.password_column
        self.vstoreid_column = st.secrets.supabase.vstoreid_column
        self.threadid_column = st.secrets.supabase.threadid_column
        self.userrole_column = st.secrets.supabase.userrole_column
    
    def check_existing_user(self, username, password):
        select_string = f"{self.username_column}, {self.password_column}, {self.vstoreid_column}, {self.threadid_column}, {self.userrole_column}"
        response = self.Client.table(self.table).select(select_string).eq(self.username_column, username).eq(self.password_column, password).execute()
        data = response.data
        if data and len(data) > 0:
            user_exists = True
            user_data = data[0]
        else:
            user_exists = False
            user_data = {}
        return user_exists, user_data

    def add_new_user(self, username, password):
        self.get_new_thread_vector_id(username=username)
        auth_data = {self.username_column: username, self.password_column: password, self.vstoreid_column: self.vectorstoreid, self.threadid_column: self.thread_id}
        try:
            response = self.Client.table(self.table).insert(auth_data).execute()
            data = response.data
            if data and len(data) > 0:
                user_data = data[0]
            else:
                user_data = {}
        except Exception as e:
            print(f"Error: {e}")
            user_data = {}
        return user_data
    
    def get_new_thread_vector_id(self, username):
        self.oai_client = OpenAI(api_key=st.secrets.openai.api_key)
        self.thread = self.oai_client.beta.threads.create()
        self.thread_id = self.thread.id
        self.vectorstore = self.oai_client.beta.vector_stores.create(name=f"WrestleAI - {username}")
        self.vectorstoreid = self.vectorstore.id
        

# Example usage
username = "test2111"
password = "test111"
user = User()

# Add new user
new_user_data = user.add_new_user(username, password)
print(new_user_data)

# Check existing user
user_exists, user_data = user.check_existing_user(username, password)
print(user_exists)
print(user_data)


