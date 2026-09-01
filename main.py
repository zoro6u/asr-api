from fastapi import FastAPI, UploadFile, HTTPException
import tempfile
import os
from transformers import pipeline

app = FastAPI()

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")
@app.post("/transcribe/")
def transcribe(file: UploadFile):
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Not an audio file")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(file.file.read())
        path = tmp.name

    try:
        result = pipe(path)
    finally:
        os.remove(path)

    return {"text": result["text"]}