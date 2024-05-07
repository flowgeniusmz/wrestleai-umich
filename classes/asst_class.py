import streamlit as st
from openai import OpenAI
import streamlit as st


class WrestleAssistant():
    def __init__(self):
        self.get_client()
        self.get_assistant()
        self.get_thread()
        self.initialize_messages()

    def get_client(self):
        self.client = OpenAI(api_key=st.secrets.openai.api_key)
    
    def get_assistant(self):
        self.assistant_id = st.secrets.openai.assistant_id
        self.assistant = self.client.beta.assistants.retrieve(assistant_id=self.assistant_id)
    
    def get_thread(self):
        self.thread = self.client.beta.threads.create()
        self.thread_id = self.thread.id

    def initialize_messages(self):
        self.display_messages = []
        self.prompt_messages = []
        self.response_messages = []
        self.thread_messages = None

    def add_display_message(self, role, prompt):
        self.display_messages.append({"role": role, "content": prompt})
        if role == "user":
            self.prompt_messages.append({"role": role, "content": prompt})
        elif role == "assistant":
            self.response_messages.append({"role": role, "content": prompt})
    
    def create_thread_message(self, role, content):
        self.thread_message = self.client.beta.threads.messages.create(thread_id=self.thread_id, content=content, role=role)
        self.thread_message_id = self.thread_message.id

    def create_run(self):
        self.run = self.client.beta.threads.runs.create(thread_id=self.thread_id, assistant_id=self.assistant_id)
        self.run_id = self.run.id
        self.run_status = self.run.status
        