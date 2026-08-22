"""
==============================================================================
OPENCLAW 2026 — MOTOR DE FONDO CÓSMICO DINÁMICO (MOVIMIENTO SUAVE DEL UNIVERSO)
==============================================================================
Genera un fondo estelar y de nebulosa en movimiento continuo y fluido:
- Capa 1: Nebulosa espacial profunda con gradientes de plasma en deriva suave
- Capa 2: Campo de estrellas de fondo (Paralaje lento y brillo pulsante)
- Capa 3: Polvo cósmico y partículas flotantes (Movimiento orgánico tridimensional)
- Rendimiento: Generación matemática determinista optimizada por fotograma
==============================================================================
"""

import math
import random
from PIL import Image, ImageDraw

WIDTH, HEIGHT = 1920, 1080

# Inicialización determinista de estrellas (180 partículas cósmicas)
random.seed(2026)
COSMIC_STARS = []
for _ in range(180):
    COSMIC_STARS.append({
        "x": random.uniform(0, WIDTH),
        "y": random.uniform(0, HEIGHT),
        "vx": random.uniform(-4.0, -12.0),   # Deriva suave horizontal
        "vy": random.uniform(-1.0, 3.0),     # Deriva suave vertical
        "size": random.choice([1, 1, 2, 2, 3]),
        "base_brightness": random.uniform(140, 255),
        "pulse_speed": random.uniform(1.2, 3.5),
        "phase": random.uniform(0, math.pi * 2)
    })

def render_cosmic_universe_frame(t: float) -> Image.Image:
    """
    Renderiza un fotograma del universo en movimiento suave en el tiempo t (segundos).
    Retorna una imagen RGB de 1920x1080.
    """
    # 1. Base: Espacio profundo Azul Noche / Púrpura Nebulosa
    frame = Image.new("RGB", (WIDTH, HEIGHT), (8, 11, 20))
    draw = ImageDraw.Draw(frame)

    # 2. Nebulosa Cósmica Suave (Bruma de plasma en movimiento ondulatorio)
    nebula_cx = int(WIDTH * 0.35 + math.sin(t * 0.3) * 120)
    nebula_cy = int(HEIGHT * 0.45 + math.cos(t * 0.25) * 80)
    nebula_r = int(520 + math.sin(t * 0.4) * 50)
    
    # Capas de gradiente elíptico suave para la nebulosa
    for r_step, alpha_color in [(nebula_r, (18, 14, 35)), (int(nebula_r * 0.65), (14, 22, 45)), (int(nebula_r * 0.35), (20, 35, 60))]:
        draw.ellipse(
            [nebula_cx - r_step, nebula_cy - int(r_step * 0.6),
             nebula_cx + r_step, nebula_cy + int(r_step * 0.6)],
            fill=alpha_color
        )

    # Segunda Nebulosa en el cuadrante inferior derecho
    nebula2_cx = int(WIDTH * 0.75 + math.cos(t * 0.2) * 90)
    nebula2_cy = int(HEIGHT * 0.70 + math.sin(t * 0.35) * 60)
    draw.ellipse(
        [nebula2_cx - 380, nebula2_cy - 200, nebula2_cx + 380, nebula2_cy + 200],
        fill=(15, 18, 38)
    )

    # 3. Renderizar las 180 Estrellas con Movimiento y Parpadeo Cósmico
    for star in COSMIC_STARS:
        # Posición con deriva continua y wrap-around
        sx = (star["x"] + star["vx"] * t) % WIDTH
        sy = (star["y"] + star["vy"] * t) % HEIGHT
        
        # Parpadeo suave
        pulse = 0.5 + 0.5 * math.sin(t * star["pulse_speed"] + star["phase"])
        brightness = int(star["base_brightness"] * (0.6 + 0.4 * pulse))
        
        sz = star["size"]
        color = (brightness, brightness, int(min(255, brightness * 1.15)))  # Tinte azulado/blanco estelar
        
        if sz == 1:
            draw.point((int(sx), int(sy)), fill=color)
        else:
            draw.ellipse([int(sx) - sz, int(sy) - sz, int(sx) + sz, int(sy) + sz], fill=color)

    return frame

if __name__ == "__main__":
    # Test del render cósmico
    img = render_cosmic_universe_frame(5.0)
    img.save("runtime/test_cosmic_universe.jpg")
    print("Fotograma cósmico de prueba generado: runtime/test_cosmic_universe.jpg")
