import os
import sys
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("====================================================================")
print(" 🌌 JACK MA STYLE CINEMATIC ENGINE — FONDO ESPACIAL + AVATAR IZQUIERDA")
print("====================================================================")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
OUT_DIR = PUBLIC_DIR / "videos" / "jack_ma_style"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── REGLAS DEL ESTILO JACK MA ────────────────────────────────────────────────
JACK_MA_CONFIG = {
    "avatar_position": "left", # Avatar en la esquina izquierda
    "avatar_shape": "circular_gold_border",
    "background": "cinematic_space_landscape_loop", # Fondo de paisajes/espacio en movimiento
    "subtitles_style": {
        "mode": "line_by_line", # Texto sale línea por línea
        "active_word_highlight": True, # Se subraya únicamente la palabra activa
        "previous_word_fade": True, # La palabra anterior desvanece su color
        "font_size": 28,
        "active_color": "#FFD700", # Dorado brillante / Neón activo
        "inactive_color": "#FFFFFF" # Blanco estándar
    }
}

config_file = OUT_DIR / "jack_ma_style_config.json"
with open(config_file, "w", encoding="utf-8") as f:
    json.dump(JACK_MA_CONFIG, f, indent=2, ensure_ascii=False)

print(f"✅ Configuración Estilo Jack Ma guardada en: {config_file}")
print("📌 Avatar: LADO IZQUIERDO | Fondo: Paisaje/Espacio Móvil HD | Subtítulos: Subrayado Dinámico Palabra por Palabra")
