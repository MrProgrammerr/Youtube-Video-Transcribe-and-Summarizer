import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """
    You are Yotube video summarizer. You will be taking the transcript text
    and summarizing the entire video and providing the important summary in points
    using maximum 500 words. The transcript text is : 
"""

def extract_youtube_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed_url.path == '/watch':
            video_id = parse_qs(parsed_url.query).get('v')
            if video_id:
                return video_id[0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    elif parsed_url.hostname in ['youtu.be']:
        return parsed_url.path[1:]
    return None

def get_transcript_from_yt(video_id):
    try:
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id, languages=('en',))
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e


def generate_summary(transcribed_text):
    model=genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcribed_text)
    return response.text


st.title("Youtube Text Transcriber and Summarizer")
yt_link = st.text_input("Enter Youtube Video URL : ")
video_id = ""

if yt_link:
    video_id = extract_youtube_video_id(yt_link)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Transcribed Text"):
    transcript_text=get_transcript_from_yt(video_id)
    if transcript_text:
        st.markdown("## Transcript:")
        st.write(transcript_text)
if st.button("Get Detailed Summary"):
    transcript_text=get_transcript_from_yt(video_id)
    summary=generate_summary(transcript_text)
    if transcript_text:
        st.markdown("## Detailed Notes:")
        st.write(summary)

# "conda activate venv/" :- in cmd
# "python -m streamlit run app.py"