import streamlit as st
from config import sessionstates as ss

ss.initialize_session_states()

st.title("WrestleAI")
a = st.button("click")
if a:
    st.switch_page(page="pages/1_Home_🏠.py")



