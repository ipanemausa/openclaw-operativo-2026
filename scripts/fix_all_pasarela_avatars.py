"""
==============================================================================
OPENCLAW 2026 — MOTOR DE ESTANDARIZACIÓN TOTAL DE LA PASARELA DE AVATARES
==============================================================================
1. Inpainting y limpieza profunda de todas las imágenes de avatar (borrado de "HB Jewelry"
   y parches rectangulares flotantes).
2. Generación y aplicación de variantes de color auténticas de polo/camiseta:
   - negro: Camiseta / Polo Negro con bordado Oro Satinado
   - azul: Polo Azul Marino con bordado Oro Satinado
   - blanco: Polo Blanco Premium con bordado Oro/Plata
   - verde: Polo Verde Esmeralda con bordado Oro Satinado
   - rojo: Polo Rojo Ejecutivo con bordado Oro Satinado
   - dorado: Polo Dorado / Negro VIP con bordado Oro Satinado
   - studio_mic: Guillermo de pie con micrófono boom de estudio
   - desk_mic: Guillermo sentado en escritorio de estudio
3. Bordado en relieve real (efecto tela con hilos dorados, bisel y sombra proyectada).
4. Distribución simultánea en openclaw-operativo-2026 y hb-jewelry.
==============================================================================
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT_OPERATIVO = Path(r"C:\Users\ipane\openclaw-operativo-2026")
ROOT_HB = Path(r"C:\openclaw\hb-jewelry")

SRC_MASTER = ROOT_HB / "public" / "avatar_pro.png"
SRC_STUDIO = ROOT_HB / "public" / "avatars" / "studio_mic.png"
SRC_DESK = ROOT_HB / "public" / "avatars" / "desk_mic.png"

TARGET_DIRS = [
    ROOT_HB / "public" / "avatars",
    ROOT_HB / "public",
    ROOT_OPERATIVO / "frontend" / "public" / "avatars",
    ROOT_OPERATIVO / "frontend" / "public",
    ROOT_OPERATIVO / "frontend" / "dist" / "avatars",
    ROOT_OPERATIVO / "frontend" / "dist",
    ROOT_OPERATIVO / "assets",
    ROOT_OPERATIVO / "runtime"
]

def clean_and_stamp_embroidery(img: Image.Image, badge_coords=(585, 625), scale=1.0, is_white_shirt=False) -> Image.Image:
    """Borra el logo viejo e inyecta el bordado oficial en relieve de HB.OS."""
    img = img.convert("RGBA")
    bx, by = badge_coords
    
    # 1. Inpainting suave del área del pecho
    pixels = img.load()
    ref_x = max(20, bx - 60)
    for y in range(max(0, by - 25), min(img.height, by + 75)):
        for x in range(max(0, bx - 30), min(img.width, bx + 170)):
            r, g, b, a = pixels[ref_x, y]
            if a > 80:
                pixels[x, y] = (r, g, b, a)

    crop_box = (max(0, bx - 35), max(0, by - 30), min(img.width, bx + 180), min(img.height, by + 85))
    smoothed = img.crop(crop_box).filter(ImageFilter.GaussianBlur(radius=1.2))
    img.paste(smoothed, crop_box)

    # 2. Capa de Bordado en Relieve Real
    badge_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(badge_layer)

    f_size_hbos = int(24 * scale)
    f_size_sub = int(12 * scale)
    try:
        font_hbos = ImageFont.truetype("arialbd.ttf", f_size_hbos)
        font_sub = ImageFont.truetype("arialbd.ttf", f_size_sub)
    except Exception:
        font_hbos = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Colores según fondo
    shadow_col = (0, 0, 0, 230) if not is_white_shirt else (80, 80, 90, 180)
    highlight_col = (255, 248, 200, 255) if not is_white_shirt else (255, 255, 255, 255)
    gold_col = (232, 192, 70, 255) if not is_white_shirt else (180, 140, 40, 255)
    sub_col = (110, 220, 195, 255) if not is_white_shirt else (20, 140, 120, 255)

    # A. Micro-sombra de oclusión
    b_draw.text((bx + 1, by + 2), "HB.OS", font=font_hbos, fill=shadow_col)
    b_draw.text((bx + 1, by + int(25 * scale)), "SOVEREIGN AI", font=font_sub, fill=shadow_col)

    # B. Bisel / Relieve superior
    b_draw.text((bx - 1, by - 1), "HB.OS", font=font_hbos, fill=highlight_col)
    b_draw.text((bx - 1, by + int(23 * scale)), "SOVEREIGN AI", font=font_sub, fill=highlight_col)

    # C. Hilo de seda bordado principal
    b_draw.text((bx, by), "HB.OS", font=font_hbos, fill=gold_col)
    b_draw.text((bx, by + int(24 * scale)), "SOVEREIGN AI", font=font_sub, fill=sub_col)

    return Image.alpha_composite(img, badge_layer)

def colorize_shirt(img: Image.Image, tint_rgb, shirt_box=(380, 520, 860, 950)) -> Image.Image:
    """Aplica un tinte de color realista respetando las luces y pliegues naturales de la tela."""
    img = img.convert("RGBA")
    crop = img.crop(shirt_box)
    
    # Crear máscara de tinte
    tint_layer = Image.new("RGBA", crop.size, (*tint_rgb, 90))
    blended_crop = Image.alpha_composite(crop.convert("RGBA"), tint_layer)
    
    # Ajuste de contraste para que la tela conserve relieve
    enhancer = ImageEnhance.Contrast(blended_crop.convert("RGB"))
    blended_crop = enhancer.enhance(1.15).convert("RGBA")
    
    img.paste(blended_crop, shirt_box)
    return img

def process_all_pasarela():
    print("=" * 70)
    print("  [PASARELA] ESTANDARIZACIÓN INTEGRAL DE AVATARES HB.OS 2026")
    print("=" * 70)

    # Cargar bases
    base_master = Image.open(SRC_MASTER) if SRC_MASTER.exists() else None
    base_studio = Image.open(SRC_STUDIO) if SRC_STUDIO.exists() else None
    base_desk = Image.open(SRC_DESK) if SRC_DESK.exists() else None

    if not base_master:
        print(f"[ERROR] No se encontró {SRC_MASTER}")
        return

    avatar_catalog_map = {}

    # 1. Master Principal & Polo Negro
    print("  -> Generando Master Principal & Polo Negro...")
    master_clean = clean_and_stamp_embroidery(base_master, badge_coords=(585, 628), scale=1.0)
    avatar_catalog_map["negro.png"] = master_clean
    avatar_catalog_map["avatar_pro.png"] = master_clean

    # 2. Studio Mic (De Pie)
    if base_studio:
        print("  -> Generando Guillermo Studio Mic...")
        # En studio_mic el pecho está en x ~ 530, y ~ 275 (escala menor porque está de pie cuerpo entero)
        studio_clean = clean_and_stamp_embroidery(base_studio, badge_coords=(540, 275), scale=0.7)
        avatar_catalog_map["studio_mic.png"] = studio_clean

    # 3. Desk Mic (Sentado)
    if base_desk:
        print("  -> Generando Guillermo Desk Mic...")
        desk_clean = clean_and_stamp_embroidery(base_desk, badge_coords=(600, 580), scale=0.9)
        avatar_catalog_map["desk_mic.png"] = desk_clean

    # 4. Variantes Cromáticas de Polo (Azul, Blanco, Verde, Rojo, Dorado)
    print("  -> Generando Polo Azul Marino...")
    azul_shirt = colorize_shirt(base_master, (25, 60, 150))
    avatar_catalog_map["azul.png"] = clean_and_stamp_embroidery(azul_shirt, badge_coords=(585, 628), scale=1.0)

    print("  -> Generando Polo Verde Esmeralda...")
    verde_shirt = colorize_shirt(base_master, (15, 110, 65))
    avatar_catalog_map["verde.png"] = clean_and_stamp_embroidery(verde_shirt, badge_coords=(585, 628), scale=1.0)

    print("  -> Generando Polo Rojo Ejecutivo...")
    rojo_shirt = colorize_shirt(base_master, (140, 20, 25))
    avatar_catalog_map["rojo.png"] = clean_and_stamp_embroidery(rojo_shirt, badge_coords=(585, 628), scale=1.0)

    print("  -> Generando Polo Blanco Premium...")
    blanco_shirt = colorize_shirt(base_master, (180, 185, 195))
    avatar_catalog_map["blanco.png"] = clean_and_stamp_embroidery(blanco_shirt, badge_coords=(585, 628), scale=1.0, is_white_shirt=True)

    print("  -> Generando Polo Dorado VIP...")
    dorado_shirt = colorize_shirt(base_master, (150, 120, 30))
    avatar_catalog_map["dorado.png"] = clean_and_stamp_embroidery(dorado_shirt, badge_coords=(585, 628), scale=1.0)

    # 5. Guardar en todas las rutas operativas
    for target_dir in TARGET_DIRS:
        target_dir.mkdir(parents=True, exist_ok=True)
        for filename, img in avatar_catalog_map.items():
            # Si el target_dir termina en 'avatars', guardamos todos los nombres
            # Si es la raíz 'public', guardamos solo avatar_pro.png
            if "avatars" in target_dir.parts:
                out_path = target_dir / filename
                img.save(out_path, "PNG")
            elif filename == "avatar_pro.png":
                out_path = target_dir / filename
                img.save(out_path, "PNG")

    print("\n" + "=" * 70)
    print("  [OK] PASARELA DE AVATARES 100% ESTANDARIZADA Y ACTUALIZADA")
    print("=" * 70)

if __name__ == "__main__":
    process_all_pasarela()
