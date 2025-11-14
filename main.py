from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, HttpUrl
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import os
from dotenv import load_dotenv
from bullet_points import generate_bullet_points, save_video_data, get_saved_video
from utils import get_youtube_video_id
from video_converter import convert_video_to_text

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

def fetch_transcript(url: str):
    try:
        transcript_list = YouTubeTranscriptApi().fetch(get_youtube_video_id(url))
        full_transcript = " ".join([t.text for t in transcript_list])
        return full_transcript
    except Exception as e:
        return f"Error: {str(e)}"

def summarize_text(text: str):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(f"Summarize this text:\n\n{text}")
        return response.text
    except Exception as e:
        return f"Error during summarization: {str(e)}"

@app.post("/transcript")
def get_transcript(req: VideoRequest):
    transcript = fetch_transcript(req.url)
    summary = summarize_text(transcript)
    return {"transcript": transcript, "summary": summary}

@app.post("/bullet_points")
def create_bullet_points(req: VideoRequest):
    video_id = get_youtube_video_id(req.url)

    transcript = fetch_transcript(req.url)
    summary = summarize_text(transcript)
    bullets = generate_bullet_points(summary)

    save_video_data(video_id, transcript, summary, bullets)

    return {
        "video_id": video_id,
        "bullet_points": bullets
    }

@app.post("/video_summary")
async def summarize_video(file: UploadFile = File(...)):
    # create a folder to store temp uploaded files
    os.makedirs("uploads", exist_ok=True)

    # correct absolute path
    file_path = os.path.join("uploads", file.filename)

    # save the uploaded file bytes
    with open(file_path, "wb") as f:
        f.write(await file.read())

    print("Saved file at:", os.path.abspath(file_path))  # Debug line

    # now Whisper can read REAL file
    transcript = convert_video_to_text(os.path.abspath(file_path))

    # summarize
    summary = summarize_text(transcript)

    # bullet points
    bullets = generate_bullet_points(summary)

    # optional: clean up file
    # os.remove(file_path)

    return {
        "transcript": transcript,
        "summary": summary,
        "bullet_points": bullets
    }
