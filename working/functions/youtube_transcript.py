from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract, YouTube


def get_transcript(video_url):
    video_id = extract.video_id(video_url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    print(transcript)
    corpus = ""
    for element in transcript:
        text = element["text"].replace("\n", " ")
        corpus += text + " "

    return corpus


def get_metadata(video_url):
    """
    Returns the metadata of the given youtube video url
    """
    # channel_name = extract.channel_name(video_url)
    yt_object = YouTube(video_url)
    author = yt_object.author
    keywords = yt_object.keywords
    length = yt_object.length
    views = yt_object.views
    description = yt_object.description
    return author, keywords, length, views, description

a = get_transcript("https://www.youtube.com/watch?v=JLFPJQ6A2as")
print(a)