import streamlit as st
import cv2
import base64
from io import BytesIO
from PIL import Image

class VideoProcessor:
    def __init__(self, video_file):
        self.video_file = video_file

    def extract_frames(self, frame_interval=50):
        # Open video file
        video = cv2.VideoCapture(self.video_file.name)
        frames = []
        success, image = video.read()
        count = 0

        while success:
            if count % frame_interval == 0:
                # Convert frame to RGB (OpenCV uses BGR by default)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                frames.append(image_rgb)
            success, image = video.read()
            count += 1

        video.release()
        return frames

    def encode_frames_base64(self, frames):
        encoded_frames = []

        for frame in frames:
            pil_image = Image.fromarray(frame)
            buffered = BytesIO()
            pil_image.save(buffered, format="JPEG")
            encoded_frame = base64.b64encode(buffered.getvalue()).decode('utf-8')
            encoded_frames.append(encoded_frame)

        return encoded_frames

    def create_prompt_message(self, prompt, encoded_frames):
        content = [{"type": "text", "text": prompt}]
        for encoded_frame in encoded_frames:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_frame}"
                }
            })

        prompt_message = {
            "role": "user",
            "content": content
        }

        return prompt_message

# Streamlit app
st.title("Video Frame Extractor")

uploaded_video = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

if uploaded_video is not None:
    processor = VideoProcessor(uploaded_video)
    
    st.write("Extracting frames from video...")
    frames = processor.extract_frames(frame_interval=50)
    
    st.write("Encoding frames to base64...")
    encoded_frames = processor.encode_frames_base64(frames)
    
    prompt = st.text_input("Enter a prompt for the video:")
    if prompt:
        prompt_message = processor.create_prompt_message(prompt, encoded_frames)
        st.write("Prompt message object:")
        st.json(prompt_message)
