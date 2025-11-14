# bullet_points.py
import json
import os
import google.generativeai as genai

DB_PATH = "database.json"

# Initialize DB if not present
if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w") as f:
        json.dump({}, f, indent=4)

def load_db():
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

def generate_bullet_points(text: str):
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = (
        "Convert the following text into concise bullet points. "
        "Only include key ideas, not unnecessary lines.\n\n"
        f"{text}"
    )

    response = model.generate_content(prompt)
    return response.text

def save_video_data(video_id: str, transcript: str, summary: str, bullets: str):
    db = load_db()
    db[video_id] = {
        "transcript": transcript,
        "summary": summary,
        "bullet_points": bullets
    }
    save_db(db)

def get_saved_video(video_id: str):
    db = load_db()
    return db.get(video_id, None)
