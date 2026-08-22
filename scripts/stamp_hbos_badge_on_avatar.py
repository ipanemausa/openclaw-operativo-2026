"""
==============================================================================
OPENCLAW 2026 — ESTAMPADOR DE INSIGNIA HB.OS EN EL AVATAR DE GUILLERMO
==============================================================================
Coloca la insignia oficial HB.OS en la camisa del avatar con acabado dorado
y tipografía nítida sobre el PNG transparente de alta resolución.
==============================================================================
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
AVATAR_SRC = ROOT / "assets" / "avatar_transparent.png"
AVATAR_OUT_ASSETS = ROOT / "assets" / "avatar_transparent_hbos.png"
AVATAR_OUT_DIST = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"

def stamp_hbos_badge():
    print("=" * 60)
    print("  [BADGE] ESTAMPANDO INSIGNIA OFICIAL HB.OS EN LA CAMISA DEL AVATAR")
    print("=" * 60)

    if not AVATAR_SRC.exists():
        print(f"[ERROR] Archivo no encontrado: {AVATAR_SRC}")
        return False

    img = Image.open(AVATAR_SRC).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Fuentes
    try:
        font_hbos = ImageFont.truetype("arialbd.ttf", 26)
        font_sub = ImageFont.truetype("arialbd.ttf", 14)
    except Exception:
        font_hbos = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Coordenadas del pecho izquierdo (lado derecho para el espectador o lado izquierdo anatómico)
    # Pecho izquierdo anatómico: x ~ 570-690, y ~ 640-720
    badge_x = 580
    badge_y = 660
    badge_w = 140
    badge_h = 55

    # 1. Fondo del parche/insignia bordada (Gris antracita elegante con borde dorado fino)
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=8,
        fill=(18, 22, 32, 230),
        outline=(212, 175, 55, 240),
        width=2
    )

    # 2. Texto Principal "HB.OS" en Oro Brillante
    draw.text((badge_x + 18, badge_y + 8), "HB.OS", font=font_hbos, fill=(255, 220, 80, 255))

    # 3. Sub-etiqueta "SOVEREIGN AI" en cian sutil
    draw.text((badge_x + 20, badge_y + 36), "SOVEREIGN AI", font=font_sub, fill=(100, 220, 180, 230))

    # Guardar en assets y en frontend/dist
    img.save(AVATAR_OUT_ASSETS, "PNG")
    img.save(AVATAR_OUT_DIST, "PNG")

    print("\n" + "=" * 60)
    print("  [OK] AVATAR ACTUALIZADO CON LA INSIGNIA OFICIAL HB.OS")
    print(f"  Ruta Assets: {AVATAR_OUT_ASSETS}")
    print(f"  Ruta Dist:   {AVATAR_OUT_DIST}")
    print("=" * 60)

    return True

if __name__ == "__main__":
    stamp_hbos_badge()
