"""
==============================================================================
OPENCLAW 2026 — EXTRACTOR DE TRANSPARENCIA PURA & COMPOSICIÓN SIDERAL
==============================================================================
Convierte capturas en PNG 100% Transparentes mediante:
1. Luma-Key Dinámico: Elimina fondos oscuros/negros de las capturas.
2. Feathering Elíptico 360°: Elimina completamente cualquier borde rectangular.
3. Preservación de Color Vibrante: Mantiene proteínas 3D, moléculas y texto en Full Color.
==============================================================================
"""

import os
import numpy as np
from pathlib import Path
from PIL import Image, ImageFilter

ROOT = Path(__file__).parent.parent
CAPTURES_DIR = ROOT / "capturas_recientes"
TRANSPARENT_PNG_DIR = ROOT / "capturas_recientes" / "pure_transparent_png"
TRANSPARENT_PNG_DIR.mkdir(parents=True, exist_ok=True)

def extract_pure_transparency(img_path: Path, target_w=960, target_h=540) -> Path:
    """
    Extrae la transparencia pura de una captura, eliminando bordes y fondos.
    """
    im = Image.open(img_path).convert("RGBA")
    im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Convertir a numpy para procesamiento vectorial de canales
    arr = np.array(im, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    
    # Calcular luminancia perceptual
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    
    # 1. Luma-Key Adaptativo: Los fondos negros/oscuros se convierten en transparencia gradual
    # Umbral de corte de negros (< 25 = 0% opacidad, > 90 = 100% opacidad)
    luma_alpha = np.clip((luminance - 20.0) / 70.0, 0.0, 1.0) * 255.0
    
    # 2. Máscara Elíptica Radial 360° (Para garantizar CERO bordes rectangulares)
    y_coords, x_coords = np.ogrid[:target_h, :target_w]
    center_y, center_x = target_h / 2.0, target_w / 2.0
    
    # Radio normalizado elíptico
    norm_x = (x_coords - center_x) / (target_w * 0.45)
    norm_y = (y_coords - center_y) / (target_h * 0.45)
    dist_sq = norm_x**2 + norm_y**2
    
    # Gradiente radial suave en bordes externos
    radial_mask = np.clip(1.0 - (dist_sq - 0.45) / 0.55, 0.0, 1.0)
    radial_mask = radial_mask * 255.0
    
    # 3. Fusión de Alpha: Mínimo entre Luma-Key y Máscara Radial
    final_alpha = np.minimum(luma_alpha, radial_mask)
    
    # Reforzar elementos brillantes para que no se vuelvan transparentes
    saturation = np.max(arr[:, :, :3], axis=2) - np.min(arr[:, :, :3], axis=2)
    colored_boost = np.clip(saturation / 30.0, 0.0, 1.0)
    final_alpha = np.maximum(final_alpha, colored_boost * radial_mask)
    
    arr[:, :, 3] = np.clip(final_alpha, 0.0, 255.0)
    
    # Convertir de vuelta a PIL y suavizar bordes alpha
    result = Image.fromarray(arr.astype(np.uint8), "RGBA")
    
    # Guardar PNG transparente puro
    out_file = TRANSPARENT_PNG_DIR / (img_path.stem + "_pure_trans.png")
    result.save(out_file, format="PNG", optimize=True)
    return out_file

def process_all_to_pure_transparency():
    all_files = sorted(list(CAPTURES_DIR.glob("Screenshot 2026-08-24*.png")))
    print(f"[TRANSPARENCIA PURA] Procesando {len(all_files)} capturas...")
    
    processed = []
    for f in all_files:
        out = extract_pure_transparency(f)
        processed.append(out)
        
    print(f"[OK] {len(processed)} imágenes transformadas a PNG transparente puro sin bordes.")
    return processed

if __name__ == "__main__":
    process_all_to_pure_transparency()
