#!/usr/bin/env python3
"""
====================================================================
 HB JEWELRY — RESTORE PRISTINE AUTHENTIC GUILLERMO AVATARS
 Version: 2026.7.1
====================================================================
 Restaura todas las imágenes del catálogo de avatares utilizando
 100% las fotografías de estudio auténticas y prístinas de Guillermo AI
 (avatar_pro.png, studio_mic.png, desk_mic.png, poster_podcast.png)
 sin ningún filtro u overlay extraño sobre su rostro o cuerpo.
"""

import os
import sys
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def restore_pristine_avatars():
    base_dir = r"C:\openclaw\hb-jewelry"
    frontend_dir = r"C:\Users\ipane\openclaw-operativo-2026\frontend"

    avatar_pro = os.path.join(base_dir, "public", "avatar_pro.png")
    studio_mic = os.path.join(base_dir, "public", "avatars", "studio_mic.png")
    desk_mic = os.path.join(base_dir, "public", "avatars", "desk_mic.png")
    poster_podcast = os.path.join(base_dir, "public", "posters", "poster_podcast.png")

    target_mapping = {
        "negro.png": avatar_pro,
        "blanco.png": studio_mic,
        "azul.png": desk_mic,
        "dorado.png": poster_podcast,
        "rojo.png": studio_mic,
        "verde.png": avatar_pro
    }

    # Restaurar en c:\openclaw\hb-jewelry\public\avatars
    dest_avatars = os.path.join(base_dir, "public", "avatars")
    for name, src in target_mapping.items():
        if os.path.exists(src):
            dst = os.path.join(dest_avatars, name)
            shutil.copy2(src, dst)
            print(f"-> Copiado {os.path.basename(src)} -> {name}")

    # Restaurar en c:\Users\ipane\openclaw-operativo-2026\frontend\public\avatars
    dest_frontend_avatars = os.path.join(frontend_dir, "public", "avatars")
    if os.path.exists(dest_frontend_avatars):
        for name, src in target_mapping.items():
            if os.path.exists(src):
                dst = os.path.join(dest_frontend_avatars, name)
                shutil.copy2(src, dst)
                print(f"-> Copiado {os.path.basename(src)} -> {name}")

if __name__ == "__main__":
    restore_pristine_avatars()
