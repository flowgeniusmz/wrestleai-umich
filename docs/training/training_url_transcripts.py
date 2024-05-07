from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract, YouTube
import pandas as pd


original_path = "docs/training_urls.csv"
final_path = "docs/training_transcripts.csv"

df_training = pd.read_csv(original_path)
urls = df_training['video_url']
transcript_data = []


def get_transcript(video_url):
    video_id = extract.video_id(video_url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript

def get_clean_transcript(transcript):
    corpus = ""
    for element in transcript:
        text = element["text"].replace("\n", " ")
        corpus += text + " "
    return corpus 

def get_transcripts_data(video_urls):
    for video_url in video_urls:
        try:
            transcript = get_transcript(video_url=video_url)
            clean_transcript = get_clean_transcript(transcript=transcript)
            new_row = {
                "video_url": video_url,
                "transcript": transcript,
                "clean_transcript": clean_transcript
            }
            transcript_data.append(new_row)
        except Exception as e:
            print(f"Error with {video_url}: {e}")
    df_transcripts = pd.DataFrame(transcript_data)
    return df_transcripts

df = get_transcripts_data(video_urls=urls)
print(df)
df.to_csv(final_path)

# def get_transcript_original(video_url):
#     video_id = extract.video_id(video_url)
#     transcript = YouTubeTranscriptApi.get_transcript(video_id)
#     print(transcript)
#     corpus = ""
#     for element in transcript:
#         text = element["text"].replace("\n", " ")
#         corpus += text + " "

#     return corpus