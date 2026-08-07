import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("====================================================================")
print(" 🌙 GENERADOR DE FONDO CÓSMICO: LUNA REALISTA + ESTRELLAS TITILANDO + AURA PURPURA")
print("====================================================================")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
MOON_BG_PNG = PUBLIC_DIR / "moon_cosmic_space.png"

# 1. Dibujar Imagen de Luna Realista + Círculo Morado Elegante
img = Image.new("RGBA", (1920, 1080), (8, 6, 18, 255))
draw = ImageDraw.Draw(img)

# Círculo Morado Elegante con Aura Difuminada en el Centro/Derecha
aura = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
aura_draw = ImageDraw.Draw(aura)

# Círculo morado principal
aura_draw.ellipse([640, 100, 1540, 1000], fill=(129, 90, 248, 220))
# Aura brillante dorada exterior
aura_draw.ellipse([600, 60, 1580, 1040], fill=(212, 175, 106, 60))
aura = aura.filter(ImageFilter.GaussianBlur(35))

img = Image.alpha_composite(img, aura)

# Luna Realista en el cuadrante superior derecho
moon_img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
moon_draw = ImageDraw.Draw(moon_img)
# Luna plateada con cráteres sutiles
moon_draw.ellipse([1400, 100, 1680, 380], fill=(240, 243, 246, 240), outline=(212, 175, 106, 180), width=3)
# Sombra de fase lunar
moon_draw.ellipse([1450, 100, 1730, 380], fill=(129, 90, 248, 120))
moon_img = moon_img.filter(ImageFilter.GaussianBlur(4))

img = Image.alpha_composite(img, moon_img)
img.convert("RGB").save(MOON_BG_PNG, "PNG")
print(f"✅ Fondo de Luna y Círculo Morado Generado: {MOON_BG_PNG}")

# 2. Generar Video de Estrellas Titilando (Twinkling Stars) usando FFmpeg Noise
MOON_TWINKLE_MP4 = PUBLIC_DIR / "moon_twinkle_space_bg.mp4"

cmd = [
    "ffmpeg", "-y",
    "-loop", "1", "-i", str(MOON_BG_PNG),
    "-f", "lavfi", "-i", "nullsrc=s=1920x1080:d=10",
    "-filter_complex",
    "[1:v]noise=alls=20:allf=t+u,format=gray,gblur=sigma=1.2[stars];"
    "[stars]colorchannelmixer=rr=0.8:gg=0.8:bb=1.0[blue_stars];"
    "[0:v][blue_stars]blend=all_mode='screen':all_opacity=0.35,zoompan=z='min(zoom+0.0005,1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=300:s=1920x1080:fps=30[outv]",
    "-map", "[outv]",
    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
    str(MOON_TWINKLE_MP4)
]

print("⚙️ Compilando Video de Fondo Cósmico en Tiempo Real (Luna + Estrellas Titilando + Círculo Morado)...")
res = subprocess.run(cmd, capture_output=True, text=True)

if res.returncode == 0:
    size_mb = MOON_TWINKLE_MP4.stat().st_size / (1024 * 1024)
    print(f" ✅ VIDEO DE FONDO LUNA TITILANTE CREADO: {MOON_TWINKLE_MP4} ({size_mb:.2f} MB)")
else:
    print(f"❌ Error creando video de fondo:\n{res.stderr[-600:]}")
