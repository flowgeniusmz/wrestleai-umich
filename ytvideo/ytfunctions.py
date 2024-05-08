import streamlit as st
import pandas as pd
from pytube import YouTube, extract
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi

audio_path = st.secrets.pathconfig.ytaudio
video_path = st.secrets.pathconfig.ytvideo
transcript_path = st.secrets.pathconfig.yttranscript
url_path = st.secrets.pathconfig.ytvideourls

df_urls = pd.read_csv(url_path)
urls = df_urls['url']



def download_ytvideo(url):
    try:
        yt = YouTube(url)
        file = yt.streams.first()
        audio = yt.streams.filter(only_audio=True).first()
        file.download(video_path)
        audio.download(audio_path)
        
    except Exception as e:
        print(e)

for url in urls:
    download_ytvideo(url)
   