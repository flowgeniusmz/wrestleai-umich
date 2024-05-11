import streamlit as st
from pytube import YouTube, extract
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd



class YouTubeAssistant():
    def __init__(self):
        self.get_video_urls()
        
    def get_video_urls(self):
        video_url_path = "links.csv"
        df_video_urls = pd.read_csv(filepath_or_buffer=video_url_path)
        print(df_video_urls)
        
yt = YouTubeAssistant()