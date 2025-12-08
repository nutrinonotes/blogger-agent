import os, requests
from src.config import ELEVENLABS_API_KEY

def synthesize_tts_elevenlabs(text, out_path):
    # NOTE: Placeholder - adapt per vendor's API docs
    url = "https://api.elevenlabs.io/v1/text-to-speech/your_voice_id"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    data = {"text": text}
    resp = requests.post(url, json=data, headers=headers, stream=True)
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return out_path