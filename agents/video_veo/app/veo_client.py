import requests
import os
import time

API_KEY = os.getenv("GEMINI_API_KEY")
VEO_BASE = "https://generativelanguage.googleapis.com/v1beta"
VEO_MODEL = "models/veo-3.1-generate-preview"

def generate_video(prompt, duration, resolution, style):
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY no configurada")

    # Paso 1 — iniciar operacion larga
    response = requests.post(
        f"{VEO_BASE}/{VEO_MODEL}:predictLongRunning?key={API_KEY}",
        json={
            "instances": [{"prompt": f"{style}: {prompt}"}],
            "parameters": {
                "durationSeconds": duration,
                "aspectRatio": "16:9"
            }
        },
        timeout=30
    )
    response.raise_for_status()
    operation = response.json()
    operation_name = operation.get("name")
    if not operation_name:
        raise ValueError(f"No se obtuvo nombre de operacion: {operation}")

    # Paso 2 — polling hasta completar
    for i in range(24):
        time.sleep(5)
        poll = requests.get(
            f"{VEO_BASE}/{operation_name}?key={API_KEY}",
            timeout=30
        )
        poll.raise_for_status()
        result = poll.json()
        if result.get("done"):
            predictions = result.get("response", {}).get("predictions", [])
            if not predictions:
                raise ValueError(f"Sin predicciones: {result}")
            return predictions[0].get("videoUri", predictions[0].get("gcsUri", "sin-url"))
    raise ValueError("Timeout esperando video de Veo")