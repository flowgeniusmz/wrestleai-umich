import streamlit as st
from config import pagesetup as ps, sessionstates as ss
import cv2
import base64
from io import BytesIO
from PIL import Image
from tempfile import NamedTemporaryFile
from openai import OpenAI
import time

client = OpenAI(api_key=st.secrets.openai.api_key)

# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 8
ps.master_page_display_styled_popmenu_pop(varPageNumber=page)


base64frames = []
uploadedvideo = st.file_uploader("Upload a video", type=['mov', 'wav', 'mp4', 'mp3'])
if uploadedvideo is not None:
    tfile = NamedTemporaryFile(suffix=".mp4", delete=False)
    tfile.write(uploadedvideo.read())
    tfile.flush()
    videopath = tfile.name
    
    video = cv2.VideoCapture(videopath)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64_image = base64.b64encode(buffer).decode("utf-8")
        base64frames.append(base64_image)
        
    video.release()
    tfile.close()
    
    st.write(f"Total frames: {total_frames}")
    st.write(f"Extracted frames: {len(base64frames)}")

    prompt = "Evaluate the image from a wrestling match. Identify any moves, counter attacks being performed. Provide feedback for the wrestlers. The final output should be a list of all the moves and feedback."
    prompt_messages =[
                {"type": "text", "text": f"{prompt}"},
                *[
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    for base64_image in base64frames[101:109:1]
                ]
            ]
      
    thread = client.beta.threads.create()
    threadid = thread.id
    assistantid = "asst_6RShUuwI4l765033O9PpHjDV"
    message = client.beta.threads.messages.create(role="user", content=prompt_messages, thread_id=threadid)
    run = client.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid)
    while run.status != "completed":
        time.sleep(2)
        st.toast("still processinig")
        run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadid)
        if run.status == "completed":
            st.toast("complete")
            tm = client.beta.threads.messages.list(thread_id=threadid, run_id=run.id, order="desc")
            print(tm)
            for m in tm:
                if m.role == "assistant":
                    st.markdown(m.content[0].text.value)
    
    #st.write("Prompt Messages:")
    #st.json(prompt_messages)

    #print(prompt_messages)