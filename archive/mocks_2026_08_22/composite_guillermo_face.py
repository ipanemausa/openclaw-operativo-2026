#!/usr/bin/env python3
"""
====================================================================
 HB JEWELRY — GUILLERMO AUTHENTIC FACE BLENDER
 Version: 2026.7.1
====================================================================
 Transplanta el rostro 100% real de Guillermo AI (avatar_pro.png)
 sobre todos los cuerpos de la colección 3D (Polo Negro, Polo Blanco, etc.)
 usando difuminado de bordes Alpha y ajuste de tono.
"""

import os
import sys
from PIL import Image, ImageFilter, ImageEnhance

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def blend_guillermo_face(target_png_path: str):
    pro_path = r"C:\openclaw\hb-jewelry\public\avatar_pro.png"
    if not os.path.exists(pro_path) or not os.path.exists(target_png_path):
        print(f"⚠️ Archivo no encontrado: {target_png_path}")
        return

    # Cargar rostro auténtico de Guillermo (avatar_pro)
    pro_img = Image.open(pro_path).convert("RGBA")
    target_img = Image.open(target_png_path).convert("RGBA")

    # Crop región del rostro auténtico de Guillermo en avatar_pro (x1, y1, x2, y2)
    # En 1024x1024, el rostro de Guillermo está en (360, 200, 660, 460)
    face_crop = pro_img.crop((360, 200, 660, 460))

    # Crear máscara de difuminado ovalada para suavizar bordes (Feathering)
    mask = Image.new("L", face_crop.size, 0)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(mask)
    # Dibujar elipse con margen para desvanecido
    draw.ellipse((15, 15, face_crop.width - 15, face_crop.height - 15), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(12))

    # Posición donde colocar el rostro de Guillermo en los cuerpos 3D
    dest_x = 360
    dest_y = 200

    target_img.paste(face_crop, (dest_x, dest_y), mask)
    
    # Guardar en PNG sin pérdidas
    target_img.save(target_png_path, "PNG")
    print(f"-> Rostro de Guillermo colocado exitosamente en: {os.path.basename(target_png_path)}")

if __name__ == "__main__":
    avatars_dir = r"C:\openclaw\hb-jewelry\public\avatars"
    for name in ["negro.png", "blanco.png", "azul.png", "dorado.png", "rojo.png", "verde.png"]:
        path = os.path.join(avatars_dir, name)
        blend_guillermo_face(path)
        
    frontend_avatars_dir = r"C:\Users\ipane\openclaw-operativo-2026\frontend\public\avatars"
    if os.path.exists(frontend_avatars_dir):
        for name in ["negro.png", "blanco.png", "azul.png", "dorado.png", "rojo.png", "verde.png"]:
            path = os.path.join(frontend_avatars_dir, name)
            blend_guillermo_face(path)
