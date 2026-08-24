"""
==============================================================================
HB.OS — LIMPIEZA AUTOMÁTICA DE CC (CLOSED CAPTIONS) EN CAPTURAS DEEPMIND
==============================================================================
Procesa todas las capturas de DeepMind del 24 de agosto y:
1. Elimina automáticamente la franja inferior donde vienen los subtítulos incrustados de YouTube.
2. Aplica re-escalado con filtro Lanczos en alta definición (1920x1080 / 1060x596).
3. Guarda las imágenes 100% limpias y listas en 'capturas_recientes/deepmind_clean_no_cc/'.
==============================================================================
"""

import os
import sys
import glob
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CAPTURES_DIR = ROOT / "capturas_recientes"
CLEAN_DIR = CAPTURES_DIR / "deepmind_clean_no_cc"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

def auto_clean_captures():
    files = sorted(glob.glob(str(CAPTURES_DIR / "Screenshot 2026-08-24*.png")))
    print("=" * 75)
    print("  HB.OS — PROCESADOR AUTOMÁTICO DE LIMPIEZA DE SUBTÍTULOS CC")
    print("=" * 75)
    print(f"  Encontradas {len(files)} capturas de DeepMind para procesar...\n")

    cleaned_count = 0
    for idx, f in enumerate(files):
        try:
            im = Image.open(f).convert("RGB")
            w, h = im.size
            # Recortar zona de video limpia: 70px arriba (titulo/tabs), 220px abajo (CC de youtube y barra de control), 60px laterales
            im_cropped = im.crop((60, 70, w - 60, h - 220))

            # Escalar a proporción 16:9 limpia en HD (1920x1080)
            im_clean_hd = im_cropped.resize((1920, 1080), Image.Resampling.LANCZOS)
            
            out_name = f"deepmind_clean_{idx+1:02d}.png"
            out_path = CLEAN_DIR / out_name
            im_clean_hd.save(out_path, quality=98)
            cleaned_count += 1
            print(f"  ✓ [{idx+1:02d}/{len(files)}] Limpia y sin CC: {out_name}")
        except Exception as e:
            print(f"  ❌ Error procesando {f}: {e}")

    print("\n" + "=" * 75)
    print(f"  🏆 {cleaned_count} CAPTURAS DE DEEPMIND 100% LIMPIAS GENERADAS EN:")
    print(f"  📁 {CLEAN_DIR}")
    print("=" * 75)

if __name__ == "__main__":
    auto_clean_captures()
