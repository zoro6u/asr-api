# Speech-to-Text API

A FastAPI service that transcribes audio files to text using OpenAI's Whisper model.

## Requirements

- Python 3.10+
- ffmpeg (`sudo dnf install ffmpeg-free` on Fedora)

## Installation

```bash
git clone git@github.com:zoro6u/asr-api.git
cd asr-api
python3 -m venv venv
source venv/bin/activate
pip install "fastapi[standard]" python-multipart
pip install transformers torch
```

## Usage

```bash
fastapi dev main.py
```

Then open `http://127.0.0.1:8000/docs` to try the API.

## Example

```bash
curl -X POST http://127.0.0.1:8000/transcribe/ \
  -F 'file=@test.wav;type=audio/wav'
```

Response:

```json
{"text": " Hi, good afternoon. My name is Muhammad and I live in Rwanda , How are you and how is your family"}
```

## Limitations

- Uses `whisper-tiny`, the smallest Whisper model — fast but less accurate than larger variants
- Runs on CPU only, "Better than nothing LOL".
- Transcription takes roughly 9x the audio duration (~90s for a 10s clip).
- Job state is kept in memory, so it is lost when the server restartsز

## API

### `POST /transcribe/`
Upload an audio file. Returns immediately with a job ID.

```json
{"job_id": "abc-123", "status": "processing"}
```

### `GET /status/{job_id}`
Check the job. Returns `processing`, `done` (with `text`), or `failed`.

```json
{"status": "done", "text": " Hi, good afternoon..."}
```

## Deployment

The service is containerized and runs anywhere Docker is available:

```bash
docker build -t asr-api .
docker run -p 8000:8000 asr-api
```

Note: transcription runs as a background task after the HTTP response is
returned, so the platform must keep the container's CPU running between
requests. Serverless platforms that throttle CPU after the response will
not work with this design.