"""
==============================================================================
OPENCLAW 2026 — MOTOR DE BORDADO DE ALTA RESOLUCIÓN PARA AVATAR DE GUILLERMO
==============================================================================
1. Toma el avatar prístino.
2. Inpaintea la zona de "HB Jewelry" (x: 570-730, y: 610-660) con la textura y
   gradiente exacto del algodón negro de la camiseta.
3. Genera un bordado en relieve real con textura de hilos dorados, micro-sombra y bisel.
==============================================================================
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
BASE_PRO = Path(r"C:\openclaw\hb-jewelry\public\avatar_pro.png")
SRC_TRANS = ROOT / "frontend" / "public" / "avatar_transparent.png"
if not SRC_TRANS.exists():
    SRC_TRANS = ROOT / "assets" / "avatar_transparent.png"

OUT_ASSETS = ROOT / "assets" / "avatar_transparent_hbos.png"
OUT_DIST = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"
OUT_FRONTEND_PUB = ROOT / "frontend" / "public" / "avatars" / "avatar_transparent.png"
OUT_RUNTIME = ROOT / "runtime" / "avatar_pristine_hbos.png"

def perfect_embroidery_stamp():
    # Cargamos avatar base transparente
    img = Image.open(SRC_TRANS).convert("RGBA")
    
    # Coordenadas exactas del texto antiguo "HB Jewelry"
    # x: 570 a 730, y: 605 a 665
    draw = ImageDraw.Draw(img)
    
    # 1. Inpainting de tela negra: muestreamos píxeles adyacentes de la camiseta
    for y in range(600, 720):
        for x in range(560, 750):
            # Muestrear color de tela 30px a la izquierda
            ref_x = max(520, x - 50)
            r, g, b, a = img.getpixel((ref_x, y))
            if a > 100: # Si es tela
                img.putpixel((x, y), (r, g, b, a))

    # Suavizado sutil de la zona inpaintada para homogeneizar el grano
    crop_box = (550, 595, 760, 725)
    chest_crop = img.crop(crop_box).filter(ImageFilter.GaussianBlur(radius=1.2))
    img.paste(chest_crop, crop_box)

    # 2. Capa de Bordado en Relieve Real (Hilo de seda dorado sobre tela)
    badge_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(badge_layer)

    try:
        font_hbos = ImageFont.truetype("arialbd.ttf", 25)
        font_sub = ImageFont.truetype("arialbd.ttf", 12)
    except Exception:
        font_hbos = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    text_x = 590
    text_y = 628

    # A. Micro-sombra profunda de los hilos sobre la tela (Oclusión ambiental)
    b_draw.text((text_x + 1, text_y + 2), "HB.OS", font=font_hbos, fill=(0, 0, 0, 240))
    b_draw.text((text_x + 1, text_y + 26), "SOVEREIGN AI", font=font_sub, fill=(0, 0, 0, 240))

    # B. Bisel / Brillo especular superior (Luz sobre el borde del hilo bordado)
    b_draw.text((text_x - 1, text_y - 1), "HB.OS", font=font_hbos, fill=(255, 248, 200, 255))
    b_draw.text((text_x - 1, text_y + 23), "SOVEREIGN AI", font=font_sub, fill=(220, 255, 245, 255))

    # C. Hilo de bordado principal en Oro Satinado (#E5C158) y Cian Esmeralda (#6EDCC3)
    b_draw.text((text_x, text_y), "HB.OS", font=font_hbos, fill=(232, 192, 70, 255))
    b_draw.text((text_x, text_y + 24), "SOVEREIGN AI", font=font_sub, fill=(110, 220, 195, 255))

    # Fusión
    final_avatar = Image.alpha_composite(img, badge_layer)

    # Guardar en todas las rutas operativas
    for p in [OUT_ASSETS, OUT_DIST, OUT_FRONTEND_PUB, OUT_RUNTIME, ROOT / "assets" / "avatar_transparent.png"]:
        p.parent.mkdir(parents=True, exist_ok=True)
        final_avatar.save(p, "PNG")

    print("[FINAL OK] Avatar restaurado y bordado HB.OS integrado en relieve sin rastros del logo viejo.")

if __name__ == "__main__":
    perfect_embroidery_stamp()
