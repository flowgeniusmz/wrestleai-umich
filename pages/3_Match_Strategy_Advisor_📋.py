import streamlit as st
from config import pagesetup as ps, sessionstates as ss
import cv2
import tempfile
import numpy as np
import os


# 0. Set page config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
page = 2
ps.master_page_display_styled_popmenu_pop(varPageNumber=page)


def get_frame(cap, frame_number):
    """Seek to the specified frame number and return the frame."""
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    else:
        frame = None  # None indicates an invalid frame
    return frame
st.title('Video Analysis')

video_file_buffer = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi", "mkv"])
if video_file_buffer is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file_buffer.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if 'frame_range' not in st.session_state or not st.session_state.frame_range:
        st.session_state.frame_range = (0, min(10, total_frames - 1))

    frame_range = st.slider(
        'Select Frame Range',
        0, total_frames - 1,
        st.session_state.frame_range,
        key='frame_range'
    )

    # Display selected frame range and surrounding frames
    col1, col2, col3, col4 = st.columns(4)
    frames_to_display = [
        (frame_range[0] - 1, "Frame Before Start"),
        (frame_range[0], "Start Frame"),
        (frame_range[1], "End Frame"),
        (frame_range[1] + 1, "Frame After End")
    ]

    for i, (frame_index, label) in enumerate(frames_to_display):
        with [col1, col2, col3, col4][i]:
            if 0 <= frame_index < total_frames:
                frame = get_frame(cap, frame_index)
                if frame is not None:
                    st.image(frame)
                    st.caption(f"{label} {frame_index}")
                else:
                    st.write("No frame available")
            else:
                st.write("No frame available")

    # Extract and download video segment
    if st.button("Download Video Segment"):
        # Setting up video writer
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0])
        output_file_path = tempfile.mktemp(suffix='.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(output_file_path, fourcc, out_fps, (frame_width, frame_height))

        for _ in range(frame_range[0], frame_range[1] + 1):
            ret, frame = cap.read()
            if ret:
                out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))  # Writing frame to output file

        out.release()
        cap.release()

        # Download link
        with open(output_file_path, 'rb') as f:
            st.download_button('Download Video Segment', f, file_name='video_segment.mp4')

        os.remove(output_file_path)  # Clean up temporary file
else:
    st.text("Please upload a video file to proceed.")
