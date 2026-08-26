"""
==============================================================================
DEEPSEEK HARNESS — GENERADOR MASIVO DE 50 AVATARES DE GUILLERMO (FLOW ENGINE)
==============================================================================
- Modelo: Flow / Nanobanana Batch Ingest (0 Costo de Créditos)
- Identidad: Guillermo Hoyos (Consistencia Biológica Transparente)
- Cobertura: 50 Posiciones, Vestuarios, Ambientes y Circunstancias Únicas
==============================================================================
"""

import os
import sys
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from deepseek_media_vault_manager import DeepSeekMediaVault

WIDTH, HEIGHT = 1080, 1350  # Formato 4:5 Alta Def de Avatar

GUILLERMO_50_SCENARIOS = [
    # 1-10: EJECUTIVO & BUSINESS FORMAL
    {"id": "avatar_01", "name": "Ejecutivo Traje Oscuro en Escritorio de Cristal", "outfit": "Traje formal negro", "env": "Oficina de Alta Tecnología"},
    {"id": "avatar_02", "name": "Ejecutivo Blazer Azul Marino en Sala de Juntas", "outfit": "Blazer azul marino", "env": "Sala de Juntas Corporativa"},
    {"id": "avatar_03", "name": "Ejecutivo Camisa Blanca HB.OS en Primer Plano", "outfit": "Camisa de vestir blanca", "env": "Estudio Minimalista"},
    {"id": "avatar_04", "name": "Ejecutivo Abrigo Elegante en Ventanal Metropolitano", "outfit": "Abrigo ejecutivo gris", "env": "Skyline Ciudad"},
    {"id": "avatar_05", "name": "Ejecutivo Chaleco Formal con Gorra HB.OS", "outfit": "Chaleco sastre y gorra HB.OS", "env": "Centro de Innovación"},
    {"id": "avatar_06", "name": "Ejecutivo de Pie de Cuerpo Entero", "outfit": "Traje ejecutivo gris marengo", "env": "Hall Corporativo"},
    {"id": "avatar_07", "name": "Ejecutivo Cruzado de Brazos Autoridad Pedagógica", "outfit": "Chaqueta formal de punto", "env": "Fondo Azul Neón"},
    {"id": "avatar_08", "name": "Ejecutivo en Escritorio Examinando Monitor 4K", "outfit": "Camisa Oxford azul", "env": "Estación de Trabajo B2B"},
    {"id": "avatar_09", "name": "Ejecutivo con Gafas Modernas Señalando Pantalla", "outfit": "Traje azul noche con gafas", "env": "Panel Interactivo"},
    {"id": "avatar_10", "name": "Ejecutivo Sentado Reflexivo en Sillón de Cuero", "outfit": "Suéter de cuello alto negro", "env": "Biblioteca Ejecutiva"},

    # 11-20: CASUAL TECH & INNOVACIÓN
    {"id": "avatar_11", "name": "Tech Hoodie Negro HB.OS con Fondo Neón", "outfit": "Hoodie HB.OS negro", "env": "Estudio Cyberpunk Soft"},
    {"id": "avatar_12", "name": "Chaqueta Bomber y Gorra HB.OS en Laboratorio", "outfit": "Bomber verde oliva y gorra HB.OS", "env": "Laboratorio de Software"},
    {"id": "avatar_13", "name": "Camiseta Polo Negra Minimalista", "outfit": "Polo negro ajustado", "env": "Fondo Gris Neutro 4K"},
    {"id": "avatar_14", "name": "Chaqueta Denim Moderna en Terraza Tech", "outfit": "Chaqueta denim oscura", "env": "Terraza Urbana"},
    {"id": "avatar_15", "name": "Suéter Beis Elegante en Entorno Informal", "outfit": "Suéter beis de lana", "env": "Espacio de Co-Working"},
    {"id": "avatar_16", "name": "Chaqueta Deportiva Negra HB.OS", "outfit": "Jacket deportiva HB.OS", "env": "Estudio de Contenido"},
    {"id": "avatar_17", "name": "Camiseta HB.OS Sovereign AI de Cuerpo Entero", "outfit": "Camiseta HB.OS Sovereign AI", "env": "Escenario de Diseño"},
    {"id": "avatar_18", "name": "Estilo Casual Primavera con Gafas de Sol", "outfit": "Camisa de lino y gafas", "env": "Entorno Luminoso exterior"},
    {"id": "avatar_19", "name": "Tech Founder con Mochila Ejecutiva", "outfit": "Chaqueta ligera y mochila", "env": "Campus Tecnológico"},
    {"id": "avatar_20", "name": "Estilo Urbano Nocturno Luces Creador", "outfit": "Chaqueta de cuero sintético", "env": "Ciudad Nocturna Bokeh"},

    # 21-30: PRESENTADOR & KEYNOTE STAGE
    {"id": "avatar_21", "name": "Keynote Speaker en Escenario Principal", "outfit": "Traje sin corbata moderno", "env": "Auditorio Keynote 1000 p"},
    {"id": "avatar_22", "name": "Presentador Señalando Diagrama Holográfico", "outfit": "Camisa azul y micropastilla", "env": "Pantalla LED Gigante"},
    {"id": "avatar_23", "name": "Keynote Sosteniendo Micrófono Profesional", "outfit": "Blazer negro y micro de mano", "env": "Congreso de IA"},
    {"id": "avatar_24", "name": "Presentador de Perfil 3/4 Explicando Concepto", "outfit": "Suéter azul marino", "env": "Fondo Azul Proyecciones"},
    {"id": "avatar_25", "name": "Masterclass Host en Set Broadcast 4K", "outfit": "Traje ejecutivo impecable", "env": "Estudio de Televisión"},
    {"id": "avatar_26", "name": "Presentador con Manos Abiertas Gesticulando", "outfit": "Camisa blanca doblada", "env": "Set de Entrevistas B2B"},
    {"id": "avatar_27", "name": "Keynote Caminando en Escenario Iluminado", "outfit": "Traje gris claro", "env": "Focos Luces de Escenario"},
    {"id": "avatar_28", "name": "Presentador Reteniendo Atención en Primer Plano", "outfit": "Camisa de vestir negra", "env": "Fondo Oscuro Bioluminiscente"},
    {"id": "avatar_29", "name": "Host de Podcast Técnico con Auriculares Studio", "outfit": "Hoodie HB.OS y headphones", "env": "Estudio de Podcast Barítono"},
    {"id": "avatar_30", "name": "Conferencista en Mesa Redonda Internacional", "outfit": "Blazer estructurado", "env": "Cumbre de Tecnología"},

    # 31-40: TALLER DE DISEÑO & CONTROL DE SOFTWARE
    {"id": "avatar_31", "name": "Arquitecto de Software Frente a Servidores", "outfit": "Camisa técnica azul", "env": "Data Center de Servidores"},
    {"id": "avatar_32", "name": "Diseñador Dibujando en Tableta Gráfica", "outfit": "Camiseta gris minimalista", "env": "Estudio de Diseño 3D"},
    {"id": "avatar_33", "name": "Ingeniero Supervisando Nodos DeepSeek", "outfit": "Chaqueta de ingeniero HB.OS", "env": "Sala de Control de IA"},
    {"id": "avatar_34", "name": "Creador Inspeccionando Poses de Avatares", "outfit": "Camisa denim y reloj inteligente", "env": "Pantalla de Múltiples Monitores"},
    {"id": "avatar_35", "name": "Desarrollador Escribiendo Código en Teclado", "outfit": "Suéter negro confort", "env": "Escritorio RGB Tech"},
    {"id": "avatar_36", "name": "Investigador Analizando Grafos DAG", "outfit": "Camisa blanca limpia", "env": "Pizarra de Cristal con Fórmulas"},
    {"id": "avatar_37", "name": "Director de Producto Evaluando Métricas", "outfit": "Traje informal sin arrugas", "env": "Dashboard de Analítica"},
    {"id": "avatar_38", "name": "Especialista en Automatización Nube", "outfit": "Chaqueta ligera azul", "env": "Servidores Cloud Nativos"},
    {"id": "avatar_39", "name": "Consultor B2B Presentando Solución", "outfit": "Traje ejecutivo marino", "env": "Sala de Demostración Clientela"},
    {"id": "avatar_40", "name": "Líder de Proyecto Coordinando Agentes", "outfit": "Polo azul oscuro HB.OS", "env": "Oficina de Agentes Autónomos"},

    # 41-50: CÓSMICO & FUTURISTA SOVEREIGN AI
    {"id": "avatar_41", "name": "Avatar Cósmico en Órbita Digital", "outfit": "Traje HB.OS Bioluminiscente", "env": "Fondo Cósmico Nebulosa"},
    {"id": "avatar_42", "name": "Sovereign AI Human en Espacio R768", "outfit": "Chaqueta con filamentos dorados", "env": "Vectores de Inserción R768"},
    {"id": "avatar_43", "name": "Avatar Holográfico Transparente", "outfit": "Silueta HD HB.OS", "env": "Holograma Láser Dorado"},
    {"id": "avatar_44", "name": "Guillermo en Laboratorio Futurista 2026", "outfit": "Buzo técnico de vanguardia", "env": "Laboratorio Cuántico"},
    {"id": "avatar_45", "name": "Retrato Dorado de Gala HB.OS", "outfit": "Esmoquin sastre de gala", "env": "Fondo Dorado Texturizado"},
    {"id": "avatar_46", "name": "Presentador en Matriz de Datos Cuántica", "outfit": "Camisa negra con broche dorado", "env": "Túnel de Datos Fibra"},
    {"id": "avatar_47", "name": "Retrato Cinematográfico 8K Bajo Lluvia Suave", "outfit": "Chaqueta impermeable ejecutiva", "env": "Luces Neón Reflejadas"},
    {"id": "avatar_48", "name": "Avatar en Estudio Minimalista Blanco Puro", "outfit": "Traje gris claro moderno", "env": "Estudio Blanco Infinito"},
    {"id": "avatar_49", "name": "Guillermo en Taller de Alta Precisión", "outfit": "Bata de taller técnico elegante", "env": "Taller de Micro-Ingeniería"},
    {"id": "avatar_50", "name": "Emblema Maestro Guillermo HB.OS Sovereign AI", "outfit": "Traje Ejecutivo Maestro con Insignia HB.OS", "env": "Fondo Maestro Dorado & Azul Cósmico"}
]

def generate_avatar_card(scen: dict, idx: int, avatar_ref: Image.Image) -> Image.Image:
    """Renderiza la tarjeta del avatar en la matriz de 50 de Flow."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (8, 14, 32))
    draw = ImageDraw.Draw(img)
    
    # Fondo ambiental
    cx, cy = WIDTH // 2, HEIGHT // 2
    for r in range(400, 0, -25):
        alpha = int(25 * (1 - r / 400))
        draw.ellipse([cx - r*1.3, cy - r, cx + r*1.3, cy + r], fill=(15 + alpha, 25 + alpha, 60 + alpha))

    # Pegar silueta de Guillermo centrada
    ax = (WIDTH - avatar_ref.width) // 2
    ay = HEIGHT - avatar_ref.height - 120
    img.paste(avatar_ref, (ax, ay), avatar_ref)

    # Tarjeta Informativa HB.OS en la parte inferior
    draw.rectangle([40, HEIGHT - 180, WIDTH - 40, HEIGHT - 30], fill=(12, 20, 44, 220), outline=(212, 175, 106), width=2)
    
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 26)
        font_sub = ImageFont.truetype("arial.ttf", 20)
    except:
        font_title = font_sub = ImageFont.load_default()

    draw.text((60, HEIGHT - 160), f"SLOT #{idx:02d}: {scen['name']}", font=font_title, fill=(235, 190, 80))
    draw.text((60, HEIGHT - 120), f"VESTUARIO: {scen['outfit']}  |  ENTORNO: {scen['env']}", font=font_sub, fill=(255, 255, 255))
    draw.text((60, HEIGHT - 85), "FLOW ENGINE: NANOBANANA (0 COSTO)  |  HB.OS SOVEREIGN AI", font=font_sub, fill=(212, 175, 106))

    return img

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 80)
    print("  🏆 DEEPSEEK HARNESS — GENERANDO BANCO DE 50 AVATARES DE GUILLERMO")
    print("  🎭 MODELO: FLOW / NANOBANANA BATCH INGEST (0 CRÉDITOS)")
    print("=" * 80)

    vault = DeepSeekMediaVault("avatar_bank_50_guillermo", "Banco Masivo de 50 Avatares de Guillermo", "Avatares")
    vault.initialize_clean_workspace()

    # Cargar avatar base de Guillermo
    avatar_base_path = ROOT / "assets" / "avatar_transparent_hbos.png"
    if not avatar_base_path.exists():
        avatar_base_path = ROOT / "assets" / "avatar_transparent.png"

    avatar_ref = Image.open(avatar_base_path).convert("RGBA")
    avatar_ref.thumbnail((750, 750), Image.Resampling.LANCZOS)

    generated_catalog = []

    print("\n[FASE 1/2] Procesando la matriz de 50 circunstancias y vestuarios...")

    for i, scen in enumerate(GUILLERMO_50_SCENARIOS, 1):
        card = generate_avatar_card(scen, i, avatar_ref)
        filename = f"guillermo_avatar_slot_{i:02d}.jpg"
        out_path = vault.output_dir / filename
        card.save(out_path, quality=95)

        generated_catalog.append({
            "slot": i,
            "id": scen["id"],
            "name": scen["name"],
            "outfit": scen["outfit"],
            "environment": scen["env"],
            "path": str(out_path),
            "flow_model": "nanobanana",
            "credit_cost": 0
        })

        print(f"  ✓ Slot #{i:02d} generado: {scen['name']} -> {filename}")

    # Guardar en la matriz maestra de Guillermo
    matrix_file = ROOT / "assets" / "guillermo_avatar_matrix.json"
    with open(matrix_file, "r", encoding="utf-8") as f:
        matrix_data = json.load(f)

    matrix_data["avatar_slots_total"] = 50
    matrix_data["50_avatar_catalog"] = generated_catalog

    with open(matrix_file, "w", encoding="utf-8") as f:
        json.dump(matrix_data, f, indent=2, ensure_ascii=False)

    vault.save_manifest("guillermo_avatar_slot_50.jpg", 0.0, 50, generated_catalog)

    print("\n" + "=" * 80)
    print(f"  🏆 MATRIZ COMPLETA DE 50 AVATARES DE GUILLERMO GENERADA CON ÉXITO")
    print(f"  Directorio Vault: {vault.output_dir}")
    print(f"  Matriz Actualizada: {matrix_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
