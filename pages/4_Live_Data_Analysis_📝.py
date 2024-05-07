import streamlit as st
from config import pagesetup as ps, sessionstates as ss


# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 3
ps.master_page_display_styled_popmenu_pop(varPageNumber=page)


background_container = ps.container_styled2(varKey="adfds")
with background_container:
    main_container = st.container(border=True)
    with main_container:
        section_tabs = st.tabs(tabs=st.secrets.tabconfig.data_sections)
        with section_tabs[0]:
            summary_container = st.container(border=False, height=200)
            detail_container = st.container(border=True, height=500)
            with detail_container:
                detail_tabs = st.tabs(tabs=st.secrets.tabconfig.wrestler_data)
        with section_tabs[1]:
            filter_container = st.container(border=True, height=200)
            dataframe_container = st.container(border=True, height=500)
            with dataframe_container:
                df_rankings = st.dataframe(st.session_state.df_rankings, use_container_width=True, hide_index=True)