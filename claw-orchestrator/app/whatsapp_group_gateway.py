"""
=============================================================================
OPENCLAW 2026 — WHATSAPP GROUP GATEWAY (MOCK)
=============================================================================
Este script actúa como el gateway para escuchar un grupo de WhatsApp
usando una librería Open-Source (ej. Baileys / whatsapp-web.js).
Cuando recibe un mensaje, lo inyecta en el Swarm Orchestrator.
=============================================================================
"""

import time
from swarm_orchestrator import swarm

def mock_whatsapp_listener():
    print("📱 Iniciando WhatsApp Gateway (Modo QR Local)...")
    print("📱 Conectado al grupo: 'Junta Directiva IA'")
    
    # Simulacion de mensajes recibidos en un grupo de WhatsApp
    mensajes_simulados = [
        {"sender": "ipane", "text": "Hola a todos, ¿cómo va el día?"},
        {"sender": "ipane", "text": "Por favor @ventas dame el reporte de cierre."},
        {"sender": "ipane", "text": "Tengo este documento sensible, @ollama haz un resumen de los riesgos legales."},
    ]
    
    for msg in mensajes_simulados:
        print(f"\n[GRUPO WHATSAPP] {msg['sender']}: {msg['text']}")
        # Inyectar al Swarm Orchestrator
        respuesta = swarm.process_message(msg['text'], sender=msg['sender'])
        print(f"[RESPUESTA WHATSAPP] => {respuesta}")
        time.sleep(2)

if __name__ == "__main__":
    mock_whatsapp_listener()
