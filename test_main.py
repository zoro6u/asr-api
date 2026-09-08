from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


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
    with open("test.wav", "rb") as f:
        response = client.post(
            "/transcribe/",
            files={"file": ("test.wav", f, "audio/wav")},
        )
    assert response.status_code == 200
    body = response.json()
    assert "job_id" in body
    assert body["status"] == "processing"