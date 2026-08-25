import os
import json
import urllib.request
from pathlib import Path

env_file = Path("C:/Users/ipane/.openclaw-master.env")
if not env_file.exists():
    print("Master env not found")
    exit(1)

env_dict = {}
for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env_dict[k.strip()] = v.strip().strip('"').strip("'")

api_key = env_dict.get("ELEVENLABS_API_KEY", "")
if not api_key:
    print("No ELEVENLABS_API_KEY found")
    exit(1)

req = urllib.request.Request("https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": api_key})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        voices = data.get("voices", [])
        print(f"Total voices available: {len(voices)}")
        for v in voices:
            print(f"ID: {v.get('voice_id')} | Name: {v.get('name')} | Category: {v.get('category')}")
except Exception as e:
    print("Error querying ElevenLabs:", e)
