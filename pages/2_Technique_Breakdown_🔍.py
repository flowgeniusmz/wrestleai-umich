import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from classes import vision_class as vcls


# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 1
ps.master_page_display_styled_popmenu_pop(varPageNumber=page)

vasst1 = vcls.VisionAssistant()

maincontainer = ps.container_styled2(varKey="afadsf")
with maincontainer:
    chatcontainer = st.container(height=400, border=True)
promptcontainer = st.container(height=100, border=False)

with chatcontainer:
    for msg in st.session_state.chat_messages:
        with st.chat_message(name=msg['role']):
            st.markdown(body=msg['content'])

with promptcontainer:
    if prompt := st.chat_input(placeholder="Enter your question here"):
        st.session_state.chat_messages.append({"role": "user", "content": "prompt"})
        with chatcontainer:
            with st.chat_message("user"):
                st.markdown(prompt)
        vasst1.get_content(prompt=prompt, image_paths=st.session_state.image_paths)
        response = vasst1.assistant_response
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        with chatcontainer:
            with st.chat_message(name="assistant"):
                st.markdown(response)
