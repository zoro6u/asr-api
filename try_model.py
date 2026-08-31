from transformers import pipeline

print("Loading model...")
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")

print("Transcribing...")
result = pipe("test.wav")

print(result)