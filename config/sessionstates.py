import streamlit as st

def initialize_session_states():
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [{"role": "assistant", "content": "Welcome to WrestleAI! How can I assist you?"}]
        st.session_state.image_paths = ["images/header.png", "images/header1.png", "images/header2.png", "images/header4.png"]