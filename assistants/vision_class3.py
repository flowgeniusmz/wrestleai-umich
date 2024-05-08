import streamlit as st
import cv2
import base64
import numpy as np
import tempfile
import shutil
from openai import OpenAI

class VideoAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=st.secrets.openai.api_key)

    def read_video(self, video_file):
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
            shutil.copyfileobj(video_file, tmpfile)
            tmpfile_path = tmpfile.name
        st.write("Temporary file created at:", tmpfile_path)  # Debug output
        # Convert the uploaded file to a cv2.VideoCapture object
        video = cv2.VideoCapture(tmpfile_path)
        return video, tmpfile_path

    def extract_frame(self, video, frame_number):
        # Extract a specific frame from the video
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = video.read()
        if success:
            return frame
        return None

    def generate_description(self, frame):
        # Generate a description of the single frame
        _, buffer = cv2.imencode('.jpg', frame)
        base64_frame = base64.b64encode(buffer).decode('utf-8')
        st.write("Base64 preview of frame (first 100 chars):", base64_frame[:100])  # Debug output
        prompt_messages = [{
            "role": "user",
            "content": "This is a frame from a video. Generate a compelling description for it.",
            "image": {"image": base64_frame, "resize": 768}
        }]
        params = {
            "model": "gpt-4-turbo",
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
        video, tmpfile_path = analyzer.read_video(video_file)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        st.write("Total frames in video:", total_frames)  # Debug output
        frame_number = st.slider("Select Frame", 0, total_frames - 1)
        frame = analyzer.extract_frame(video, frame_number)
        
        if frame is not None:
            st.image(frame, caption=f"Frame {frame_number}")
            if st.button('Generate Description'):
                with st.spinner('Generating description...'):
                    description = analyzer.generate_description(frame)
                    st.write(description)
        else:
            st.error("Failed to extract frame. Please try another frame.")

        # Cleanup: remove the temporary file
        if tmpfile_path:
            os.remove(tmpfile_path)

if __name__ == "__main__":
    main()
