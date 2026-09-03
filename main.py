from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
import tempfile
import os
import uuid
from transformers import pipeline

app = FastAPI()

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")

jobs = {}


def run_transcription(job_id: str, path: str):
    try:
        result = pipe(path)
        jobs[job_id] = {"status": "done", "text": result["text"]}
    except Exception as e:
        jobs[job_id] = {"status": "failed", "error": str(e)}
    finally:
        os.remove(path)


@app.post("/transcribe/")
def transcribe(file: UploadFile, background_tasks: BackgroundTasks):
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Not an audio file")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(file.file.read())
        path = tmp.name

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing", "text": None}

    background_tasks.add_task(run_transcription, job_id, path)

    return {"job_id": job_id, "status": "processing"}


@app.get("/status/{job_id}")
def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]