import urllib.request
import json
from pathlib import Path

env_file = Path("C:/Users/ipane/.openclaw-master.env")
env_dict = {}
for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env_dict[k.strip()] = v.strip().strip('"').strip("'")

print("=== ESTADO DE ENDPOINTS CLOUD ===")

# 1. DeepSeek
dk = env_dict.get("DEEPSEEK_API_KEY", "")
try:
    req = urllib.request.Request("https://api.deepseek.com/models", headers={"Authorization": f"Bearer {dk}"})
    with urllib.request.urlopen(req, timeout=5) as r:
        print("  [OK] DeepSeek Cloud API: ACTIVA Y OPERACIONAL (Ultra-Rápida)")
except Exception as e:
    print(f"  [ERROR] DeepSeek Cloud API: {e}")

# 2. Gemini
gk = env_dict.get("GEMINI_API_KEY", "") or env_dict.get("GOOGLE_API_KEY", "")
try:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={gk}"
    with urllib.request.urlopen(url, timeout=5) as r:
        print("  [OK] Google Gemini Cloud API: ACTIVA Y OPERACIONAL")
except Exception as e:
    print(f"  [ERROR] Google Gemini Cloud API: {e}")

# 3. Anthropic
ak = env_dict.get("ANTHROPIC_API_KEY", "")
print(f"  [*] Anthropic Key: {'Configurada' if len(ak) > 10 else 'No configurada'}")

print("=================================")
