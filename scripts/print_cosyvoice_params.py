import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from gradio_client import Client
import json

c = Client("FunAudioLLM/Fun-CosyVoice3-0.5B", verbose=False)
info = c.view_api(print_info=False, return_format="dict")
params = info.get("named_endpoints", {}).get("/generate_audio", {}).get("parameters", [])
for p in params:
    print(f"Name: {p.get('parameter_name')} | Type: {p.get('type')}")
