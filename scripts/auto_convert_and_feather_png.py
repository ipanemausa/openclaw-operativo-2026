"""
==============================================================================
OPENCLAW 2026 — PROTOCOLO DE INGESTA AUTOMÁTICA PNG & FUNDIDO SIDERAL
==============================================================================
Convierte automáticamente cualquier imagen capturada a PNG 32-bit con canal
Alpha y aplica máscara de desvanecimiento radial (Feathering 24px) para fusión
cósmica sin bordes duros (Full Color + Transparencia Orgánica).
==============================================================================
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).parent.parent
CAPTURES_DIR = ROOT / "capturas_recientes"
PROCESSED_PNG_DIR = ROOT / "capturas_recientes" / "png_holographic"
PROCESSED_PNG_DIR.mkdir(parents=True, exist_ok=True)

def process_image_to_holographic_png(image_path: Path, target_w=960, target_h=540, feather_radius=24) -> Path:
    """
    Convierte una captura a PNG 32-bit con canal Alpha y bordes desvanecidos suaves.
    """
    im = Image.open(image_path).convert("RGBA")
    
    # Redimensionar manteniendo aspecto panorámico 16:9
    im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Crear máscara de transparencia suave (Feathering radial/borde)
    mask = Image.new("L", (target_w, target_h), 0)
    draw = ImageDraw.Draw(mask)
    
    margin = feather_radius * 2
    # Dibujar rectángulo interior
    draw.rectangle([margin, margin, target_w - margin, target_h - margin], fill=255)
    
    # Aplicar desenfoque gaussiano para crear transición suave hacia la transparencia
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather_radius))
    
    # Aplicar la máscara al canal alpha de la imagen
    im.putalpha(mask)
    
    # Guardar en formato PNG transparente
    out_name = image_path.stem + "_holographic.png"
    out_path = PROCESSED_PNG_DIR / out_name
    im.save(out_path, format="PNG", optimize=True)
    return out_path

def batch_process_all_captures():
    """Procesa en lote todas las capturas de la carpeta capturas_recientes."""
    all_files = list(CAPTURES_DIR.glob("Screenshot*.png")) + list(CAPTURES_DIR.glob("*.jpg")) + list(CAPTURES_DIR.glob("*.jpeg"))
    print(f"[PROTOCOLO PNG] Procesando {len(all_files)} capturas a formato Holográfico PNG...")
    
    processed = []
    for f in sorted(all_files):
        if "holographic" in f.name:
            continue
        out_p = process_image_to_holographic_png(f)
        processed.append(out_p)
        
    print(f"[OK] {len(processed)} imágenes convertidas a PNG con canal Alpha y bordes suaves.")
    return processed

if __name__ == "__main__":
    batch_process_all_captures()
