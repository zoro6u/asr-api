import io
import struct

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def make_silent_wav(seconds=1, sample_rate=16000):
    n = seconds * sample_rate
    data = b"\x00\x00" * n
    header = b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVE"
    header += b"fmt " + struct.pack(
        "<IHHIIHH", 16, 1, 1, sample_rate, sample_rate * 2, 2, 16
    )
    header += b"data" + struct.pack("<I", len(data))
    return header + data


def test_status_unknown_job():
    response = client.get("/status/does-not-exist")
    assert response.status_code == 404


def test_rejects_non_audio_file():
    response = client.post(
        "/transcribe/",
        files={"file": ("test.txt", b"not audio", "text/plain")},
    )
    assert response.status_code == 400


def test_accepts_audio_and_returns_job_id():
    wav = make_silent_wav()
    response = client.post(
        "/transcribe/",
        files={"file": ("test.wav", io.BytesIO(wav), "audio/wav")},
    )
    assert response.status_code == 200
    body = response.json()
    assert "job_id" in body
    assert body["status"] == "processing"