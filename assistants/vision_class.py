import streamlit as st
import cv2
import base64
import numpy as np
from openai import OpenAI
import shutil
import tempfile

class VideoAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def read_video(self, video_file):
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
            shutil.copyfileobj(video_file, tmpfile)
            tmpfile_path = tmpfile.name
        
        # Convert the uploaded file to a cv2.VideoCapture object
        video = cv2.VideoCapture(tmpfile_path)
        return video

    def extract_frames(self, video, start_frame, end_frame):
        # Extract frames from the video within a specified range
        base64_frames = []
        current_frame = 0
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            if start_frame <= current_frame <= end_frame:
                _, buffer = cv2.imencode('.jpg', frame)
                base64_frames.append(base64.b64encode(buffer).decode('utf-8'))
            current_frame += 1
            if current_frame > end_frame:
                break
        video.release()
        return base64_frames

    def generate_description(self, frames):
        # Generate a description of the video using selected frames
        prompt_messages = [
            {
                "role": "user",
                "content": [
                    "These are frames from a video that I want to upload. Generate a compelling description that I can upload along with the video.",
                    *map(lambda x: {"image": x, "resize": 768}, frames),
                ],
            },
        ]
        params = {
            "model": "gpt-4-vision-preview",
            "messages": prompt_messages,
            "max_tokens": 200,
        }
        result = self.client.chat.completions.create(**params)
        return result.choices[0].message.content

def main():
    st.title("Video Analyzer App")
    video_file = st.file_uploader("Upload a video", type=['mp4', 'avi', 'mov'])
    api_key = st.secrets["openai"]["api_key"]
    analyzer = VideoAnalyzer(api_key=api_key)

    if video_file is not None:
        start_frame = st.number_input('Start Frame', min_value=0, value=0)
        end_frame = st.number_input('End Frame', min_value=0, value=50)
        if st.button('Analyze Video'):
            with st.spinner('Analyzing video...'):
                video = analyzer.read_video(video_file)
                frames = analyzer.extract_frames(video, start_frame, end_frame)
                description = analyzer.generate_description(frames)
                st.write(description)

if __name__ == "__main__":
    main()
