import sys
import random
from PIL import Image, ImageDraw, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def create_cosmic_space_background(width=1920, height=1080, output_path=r"C:\openclaw\hb-jewelry\public\cosmic_space_bg.png"):
    # 1. Crear lienzo de fondo azul oscuro/púrpura galáctico
    img = Image.new("RGB", (width, height), color=(8, 10, 24))
    draw = ImageDraw.Draw(img)

    # 2. Agregar gradiente de nebulosa central
    for r in range(500, 0, -5):
        alpha = int((1 - r / 500) * 80)
        color = (25 + int(r * 0.1), 15 + int(r * 0.05), 60 + int(r * 0.2))
        draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], fill=color)

    # 3. Dibujar 400 estrellas brillantes y destellos cósmicos
    random.seed(2026)
    for _ in range(400):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.choice([1, 1, 2, 2, 3])
        brightness = random.randint(180, 255)
        
        # Color de estrella (Blanco, Azul neón, Dorado soft)
        star_color = random.choice([
            (brightness, brightness, brightness),
            (100, 200, 255),
            (255, 215, 100)
        ])
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=star_color)

    # 4. Difuminado de nebulosa suave
    img = img.filter(ImageFilter.GaussianBlur(1))
    
    # Redibujar destellos nítidos sobre la nebulosa
    draw = ImageDraw.Draw(img)
    for _ in range(80):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(255, 255, 255))

    img.save(output_path)
    print(f"✅ Fondo Espacial Cósmico Generado: {output_path}")

if __name__ == "__main__":
    create_cosmic_space_background()
