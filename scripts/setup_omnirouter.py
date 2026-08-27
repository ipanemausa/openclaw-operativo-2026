import os
import requests
import json
import time

OMNIROUTER_URL = os.getenv("OMNIROUTER_URL", "http://localhost:11434")
ADMIN_PASSWORD = os.getenv("OMNIROUTER_PASSWORD", "change_me")

def setup_providers():
    print(f"[*] Conectando con OmniRouter en {OMNIROUTER_URL}...")
    headers = {"Authorization": f"Bearer {ADMIN_PASSWORD}", "Content-Type": "application/json"}
    
    # 1. Configurar Groq (Tier 1 Rápido)
    groq_key = os.getenv("GROQ_API_KEY", "")
    if groq_key:
        print("[+] Configurando proveedor: Groq...")
        requests.post(f"{OMNIROUTER_URL}/api/providers", headers=headers, json={
            "name": "groq", "type": "api", "key": groq_key
        })
        
    # 2. Configurar OpenRouter (Tier 2 Hub)
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
    if openrouter_key:
        print("[+] Configurando proveedor: OpenRouter...")
        requests.post(f"{OMNIROUTER_URL}/api/providers", headers=headers, json={
            "name": "openrouter", "type": "api", "key": openrouter_key
        })
        
    # 3. Proveedores recomendados: Nvidia NIM & Orca (Casos 3 del video)
    nvidia_key = os.getenv("NVIDIA_NIM_API_KEY", "")
    if nvidia_key:
        print("[+] Configurando proveedor: Nvidia NIM...")
        requests.post(f"{OMNIROUTER_URL}/api/providers", headers=headers, json={
            "name": "nvidia_nim", "type": "api", "key": nvidia_key
        })

def setup_combos():
    print("[*] Creando combinaciones de enrutamiento (Combos)...")
    headers = {"Authorization": f"Bearer {ADMIN_PASSWORD}", "Content-Type": "application/json"}
    
    # Combo Best Free
    requests.post(f"{OMNIROUTER_URL}/api/combos", headers=headers, json={
        "name": "combo-best-free",
        "description": "El mejor modelo gratuito disponible de cualquier proveedor",
        "routing_strategy": "priority",
        "models": [
            {"provider": "nvidia_nim", "model": "meta/llama3-70b-instruct"},
            {"provider": "openrouter", "model": "google/gemini-2.0-flash-001"}
        ]
    })
    
    # Combo DeepSeek Free
    requests.post(f"{OMNIROUTER_URL}/api/combos", headers=headers, json={
        "name": "combo-deepseek-free",
        "description": "Enrutamiento estricto a DeepSeek gratuito",
        "routing_strategy": "priority",
        "models": [
            {"provider": "openrouter", "model": "deepseek/deepseek-chat:free"},
            {"provider": "groq", "model": "deepseek-r1-distill-llama-70b"}
        ]
    })
    print("[+] Combos configurados exitosamente.")

if __name__ == "__main__":
    time.sleep(2) # Esperar a que levante el contenedor
    setup_providers()
    setup_combos()
    print("[✓] OmniRouter Configurado para el Ecosistema OpenClaw 2026.")
