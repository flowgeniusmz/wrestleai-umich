import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
import pandas as pd
import os
from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeAssistant():
    def __init__(self):
        self.get_paths()
        self.get_video_list()
        #self.get_content()
        
    
    def get_paths(self):
        self.video_link_path = "master/data/youtube_links.csv" 
        self.audio_path = "master/media/audio/"
        self.video_path = "master/media/video/"
        self.transcript_path = "master/media/transcript/"
        
    def get_video_list(self):
        self.df_video_urls = pd.read_csv(filepath_or_buffer=self.video_link_path)
        self.video_urls = self.df_video_urls['url']
        self.video_ids = self.df_video_urls['id']
        self.video_file_names = []
        self.audio_file_names = []
        
    def get_content(self):
        for video_url in self.video_urls:
            self.get_content_video(url=video_url)
            #self.get_content_audio(url=video_url)
        self.df_video_urls['video_file_name'] = self.video_file_names
        #self.df_video_urls['audio_file_name'] = self.audio_file_names
            
    def get_content_video(self, url):
        try:
            yt_video = YouTube(url)
            video_content = yt_video.streams.first()
            video_file = video_content.download(self.video_path)
            self.video_file_names.append(video_file)
        except Exception as e:
            print(f"Error downloading video {url}: {str(e)}")
            self.video_file_names.append(None)
        
    def get_content_audio(self, url):
        try:
            yt_audio = YouTube(url)
            audio_content = yt_audio.streams.filter(only_audio=True).first()
            temp_audio_file = audio_content.download(self.audio_path)
            # Convert to mp3
            audio_file = AudioSegment.from_file(temp_audio_file, format="mp4")
            new_file_path = self.audio_path + + yt_audio.title + '.mp3'
            audio_file.export(new_file_path, format="mp3")
            os.remove(temp_audio_file)
            self.audio_file_names.append(new_file_path)
        except Exception as e:
            print(f"Error downloading audio {url}: {str(e)}")
            self.audio_file_names.append(None)
    
    def get_content_transcripts(self):
       
        for video_id in self.video_ids:
            try:
                # Attempt to fetch the transcript for the given video ID
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = ""

                # Concatenate all text from the transcript
                for item in transcript_list:
                    transcript_text += item['text'] + " "

                # Define the path for the transcript file
                transcript_filename = os.path.join(self.transcript_path, f"{video_id}.txt")

                # Write the transcript to a file
                with open(transcript_filename, 'w', encoding='utf-8') as file:
                    file.write(transcript_text)
                print(f"Transcript saved for video ID {video_id}")

            except Exception as e:
                print(f"Error retrieving transcript for video ID {video_id}: {str(e)}")
                # Optionally, handle specific exceptions like `TranscriptsDisabled` or `NoTranscriptFound`
            

# Create instance and run
a = YouTubeAssistant()
#a.get_content_transcripts()
a.get_content()
