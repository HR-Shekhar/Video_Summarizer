import whisper

# Load the Whisper model once
model = whisper.load_model("base")  
# tiny / base / small / medium / large

def convert_video_to_text(video_path):
    try:
        result = model.transcribe(video_path)
        text = result["text"].strip()
        return text if text else "No speech detected."
    except Exception as e:
        return f"Error during transcription: {e}"
