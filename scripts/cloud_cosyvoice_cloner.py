"""
=============================================================================
OPENCLAW 2026 — COSYVOICE 3 CLOUD GPU INFERENCE (ALIBABA / FUNAUDIOLLM)
=============================================================================
Envía la muestra real de Guillermo ('audio/guillermo_voice_reference.wav')
y el texto técnico de investigación al modelo oficial CosyVoice en Cloud GPU.
=============================================================================
"""

import os
import sys
import shutil
from pathlib import Path
from gradio_client import Client, handle_file

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "audio"
REFERENCE_VOICE = AUDIO_DIR / "guillermo_voice_reference.wav"
FINAL_OUTPUT = AUDIO_DIR / "GUILLERMO_COSYVOICE_MASTER_CLOUD_GPU.wav"

TEXT_TO_CLONE = (
    "En las últimas horas, los análisis de frontera confirman un giro histórico en la inteligencia artificial global. "
    "Mientras los modelos cerrados tradicionales alcanzaban techos de cómputo y altos costos de inferencia, "
    "arquitecturas abiertas como DeepSeek-R1 y Kimi K3 han demostrado que la compresión matemática del KV-Cache "
    "y la atención latente multi-cabeza superan en densidad computacional a cualquier API cerrada. "
    "En OpenClaw no dependemos de proveedores externos; construimos sistemas soberanos donde el control del dato, "
    "la gobernanza vectorial y la voz auténtica pertenecen exclusivamente al creador."
)

def run_cosyvoice_cloud():
    print("=" * 65)
    print("  OPENCLAW 2026 — CLONACIÓN NEURAL EN CLOUD GPU (COSYVOICE)")
    print("=" * 65)
    print(f"[*] Archivo de referencia: {REFERENCE_VOICE}")
    
    space_name = "FunAudioLLM/Fun-CosyVoice3-0.5B"
    try:
        print(f"[*] Conectando con {space_name}...")
        client = Client(space_name, verbose=False)
        api_info = client.view_api(return_format="dict")
        endpoints = list(api_info.get("named_endpoints", {}).keys())
        print(f"[*] Endpoints disponibles en CosyVoice: {endpoints}")

        print(f"[*] Enviando muestra real de Guillermo a CosyVoice 3 Cloud GPU...")
        result = client.predict(
            tts_text=TEXT_TO_CLONE,
            mode_value="zero_shot",
            prompt_text="Bienvenidos a OpenClaw 2026. Esta es mi voz real para el sistema operativo.",
            prompt_wav_upload=handle_file(str(REFERENCE_VOICE)),
            prompt_wav_record=None,
            instruct_text="You are a helpful assistant. Please say a sentence in a very soft voice.<|endofprompt|>",
            seed=42,
            stream=False,
            ui_lang="En",
            api_name="/generate_audio"
        )
        print(f"[*] Respuesta de CosyVoice Cloud GPU: {result}")
        if result and os.path.exists(result):
            shutil.copy(result, str(FINAL_OUTPUT))
            print(f"\n[ÉXITO TOTAL] Audio de Guillermo clonado con CosyVoice en Cloud GPU:")
            print(f"👉 {FINAL_OUTPUT} ({FINAL_OUTPUT.stat().st_size / 1024:.2f} KB)")
        else:
            print("[WARN] Respuesta inesperada:", result)

    except Exception as e:
        print(f"[ERROR] Falló CosyVoice Cloud: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_cosyvoice_cloud()
