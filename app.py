import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """
    You are Yotube video summarizer. You will be taking the transcript text
    and summarizing the entire video and providing the important summary in points
    using maximum 500 words. The transcript text is : 
"""

def get_transcript_from_yt(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
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

text= get_transcript_from_yt("https://www.youtube.com/watch?v=HFfXvfFe9F8")
print(generate_summary(text))

st.title("Youtube Text Transcriber and Summarizer")
yt_link = st.text_input("Enter Youtube Video URL : ")

if yt_link:
    video_id = yt_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Transcribed Text"):
    transcript_text=get_transcript_from_yt(yt_link)

    if transcript_text:
        st.markdown("## Transcript:")
        st.write(transcript_text)
if st.button("Get Detailed Summary"):
    transcript_text=get_transcript_from_yt(yt_link)

    if transcript_text:
        summary=generate_summary(transcript_text)
        st.markdown("## Detailed Notes:")
        st.write(summary)

# "conda activate venv/" :- in cmd