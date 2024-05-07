import streamlit as st
from classes.class_datascraper import TeamRosterScraper, TeamScraper, WrestlerRankingsScraper

def initialize_session_states():
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [{"role": "assistant", "content": "Welcome to WrestleAI! How can I assist you?"}]
        st.session_state.image_paths = ["images/2f3aaec0065b11e28b0122000a1e9b8c_7.png", "images/153398ec3601a31fe8b61761d6a43f26_1024x1024 (1).png", "images/wsi-imageoptim-highcrotchtakedownfeatureimage.png"]
    
    if "scraper_data_loaded" not in st.session_state:
        st.session_state.scraper_data_loaded = False
        st.session_state.team_roster_scraper = TeamRosterScraper()
        st.session_state.team_scraper = TeamScraper()
        st.session_state.ranking_scraper = WrestlerRankingsScraper()
        st.session_state.df_team_roster = st.session_state.team_roster_scraper.scrape()
        st.session_state.df_team = st.session_state.team_scraper.scrape()
        st.session_state.df_rankings = st.session_state.ranking_scraper.scrape()
        st.session_state.scraper_data_loaded = True

