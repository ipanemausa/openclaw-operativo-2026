import requests
import os

API_KEY = os.getenv("GEMINI_API_KEY")
VEO_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/veo-3.0-generate-preview:generateVideo"

def generate_video(prompt, duration, resolution, style):
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY no configurada en .env")

    payload = {
        "instances": [{"prompt": f"{style}: {prompt}"}],
        "parameters": {
            "duration_seconds": duration,
            "resolution": resolution,
            "aspect_ratio": "16:9"
        }
    }

    response = requests.post(
        f"{VEO_ENDPOINT}?key={API_KEY}",
        json=payload,
        timeout=120
    )
    response.raise_for_status()
    data = response.json()

    predictions = data.get("predictions", [])
    if not predictions:
        raise ValueError("Veo no devolvio predicciones")

    return predictions[0].get("videoUri", predictions[0].get("url", ""))
