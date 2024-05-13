import streamlit as st
import pytube
from googleapiclient.discovery import build
import json
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled


youtube = build('youtube', 'v3', developerKey=st.secrets.googleconfig.google_api_key)


def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([item['text'] for item in transcript_list])
        return transcript
    except TranscriptsDisabled:
        return "Transcript not available"
    
def search_wrestling_videos(query, max_results):
    search_request = youtube.search().list(
        q=query,
        part = 'snippet',
        maxResults = max_results,
        type='video'
    )
    
    search_response = search_request.execute()
    #print(search_response)
    
    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

    videos_request = youtube.videos().list(
        id=','.join(video_ids),
        part='id, snippet,contentDetails,statistics'
    )
    videos_response = videos_request.execute()
    #print(videos_response)
    videos = []
    
    for item in videos_response.get('items', []):
        video_data = {
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'channel': item['snippet']['channelTitle'],
            'publish_date': item['snippet']['publishedAt'],
            'duration': item['contentDetails']['duration'],
            'view_count': item['statistics']['viewCount'],
            'like_count': item['statistics'].get('likeCount'),
            'dislike_count': item['statistics'].get('dislikeCount'),
            'comment_count': item['statistics'].get('commentCount'),
            'tags': item['snippet'].get('tags', []),
            'video_id': item['id'],
            'transcript': get_transcript(video_id=item['id'])
            }
        videos.append(video_data)
    
    return videos

videos = search_wrestling_videos('hasan yazdani', 10)
print(json.dumps(videos, indent=4))