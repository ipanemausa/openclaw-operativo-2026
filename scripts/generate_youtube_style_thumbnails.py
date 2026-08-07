import os
import sys
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("====================================================================")
print(" 🎨 GENERADOR DE THUMBNAILS ÚNICOS YOUTUBE B2B (PILLOW HIGH-RES 1280x720)")
print("====================================================================")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
THUMB_DIR = PUBLIC_DIR / "thumbnails"
THUMB_DIR.mkdir(parents=True, exist_ok=True)

THUMBNAIL_SPECS = [
    {
        "id": "jack-ma-style-b2b-master",
        "file": "thumb_jack_ma_b2b.png",
        "avatar": "avatars/negro.png",
        "badge": "🌌 JACK MA B2B",
        "badge_bg": (212, 175, 106),
        "title_top": "IA EMPRESARIAL B2B",
        "title_bot": "AUTOMATIZACIÓN $0",
        "bg_color": (15, 12, 28)
    },
    {
        "id": "agencia-b2b-intro",
        "file": "thumb_agencia_ai.png",
        "avatar": "avatars/dorado.png",
        "badge": "🚀 AGENCIA IA B2B",
        "badge_bg": (132, 204, 22),
        "title_top": "ASESORÍA & AGENTES",
        "title_bot": "CRECIMIENTO ESCALABLE",
        "bg_color": (10, 25, 15)
    },
    {
        "id": "real-estate-ai",
        "file": "thumb_real_estate_ai.png",
        "avatar": "avatars/blanco.png",
        "badge": "🏢 REAL ESTATE IA",
        "badge_bg": (56, 189, 248),
        "title_top": "CITAS 24/7 EN VIVO",
        "title_bot": "FILTRO DE LEADS",
        "bg_color": (10, 20, 35)
    },
    {
        "id": "servicios-profesionales-ai",
        "file": "thumb_servicios_salud.png",
        "avatar": "avatars/azul.png",
        "badge": "💼 SALUD & SERVICIOS",
        "badge_bg": (129, 140, 248),
        "title_top": "AGENDAS AUTÓNOMAS",
        "title_bot": "ATENCIÓN MÉDICA & LEGAL",
        "bg_color": (15, 15, 35)
    },
    {
        "id": "guillermo-940f-master",
        "file": "thumb_guillermo_940f.png",
        "avatar": "avatars/dorado.png",
        "badge": "🏆 MASTER 940 FRAMES",
        "badge_bg": (245, 158, 11),
        "title_top": "GUILLERMO AI STUDIO",
        "title_bot": "AUDIO BROADCAST 48kHz",
        "bg_color": (30, 20, 10)
    },
    {
        "id": "talk-grow-educational",
        "file": "thumb_claude_7hacks.png",
        "avatar": "avatars/negro.png",
        "badge": "💡 7 HACKS CLAUDE",
        "badge_bg": (168, 85, 247),
        "title_top": "CLAUDE 4.6 PROMPT",
        "title_bot": "TELEPROMPTER 3D",
        "bg_color": (25, 10, 35)
    },
    {
        "id": "yt-special-claude-master",
        "file": "thumb_youtube_masterclass.png",
        "avatar": "avatars/blanco.png",
        "badge": "🔴 MASTERCLASS 30M",
        "badge_bg": (239, 68, 68),
        "title_top": "CURSO DE AGENTES",
        "title_bot": "RAG VECTORIAL 768-DIM",
        "bg_color": (35, 10, 15)
    },
    {
        "id": "podcast",
        "file": "thumb_podcast_ecosistema.png",
        "avatar": "avatars/azul.png",
        "badge": "🎙️ PODCAST AI",
        "badge_bg": (6, 182, 212),
        "title_top": "ECOSISTEMA ILIMITADO",
        "title_bot": "AUTOMATIZACIÓN GLOBAL",
        "bg_color": (10, 30, 35)
    },
    {
        "id": "tutorial",
        "file": "thumb_tutorial_hb18k.png",
        "avatar": "avatars/dorado.png",
        "badge": "📹 TUTORIAL APP HB",
        "badge_bg": (234, 179, 8),
        "title_top": "MANEJO PASO A PASO",
        "title_bot": "WHATSAPP & INVENTARIO",
        "bg_color": (30, 25, 10)
    },
    {
        "id": "qa-english",
        "file": "thumb_qa_english_rag.png",
        "avatar": "avatars/rojo.png",
        "badge": "🇺🇸 ENGLISH DEMO",
        "badge_bg": (236, 72, 153),
        "title_top": "7 Q&A ARCHITECTURE",
        "title_bot": "MULTIMODAL RAG DEMO",
        "bg_color": (35, 10, 25)
    },
    {
        "id": "showcase-18k",
        "file": "thumb_showcase_18k.png",
        "avatar": "avatars/verde.png",
        "badge": "✨ SHOWCASE 18K",
        "badge_bg": (16, 185, 129),
        "title_top": "JOYERÍA FINA 18K",
        "title_bot": "CIERRE COMERCIAL $0",
        "bg_color": (10, 30, 20)
    },
    {
        "id": "tiktok-viral",
        "file": "thumb_tiktok_viral.png",
        "avatar": "avatars/studio_mic.png",
        "badge": "📱 TIKTOK VIRAL",
        "badge_bg": (244, 63, 94),
        "title_top": "FORMATO VERTICAL 9:16",
        "title_bot": "CAMPAÑAS PUBLICITARIAS",
        "bg_color": (35, 15, 20)
    }
]

cosmic_bg_path = PUBLIC_DIR / "cosmic_space_bg.png"
base_bg = None
if cosmic_bg_path.exists():
    try:
        base_bg = Image.open(cosmic_bg_path).convert("RGBA").resize((1280, 720))
    except Exception:
        base_bg = None

for spec in THUMBNAIL_SPECS:
    # 1. Crear Canvas 1280x720
    canvas = Image.new("RGBA", (1280, 720), spec["bg_color"] + (255,))
    
    if base_bg:
        # Overlay espacial con tinte de color de tema
        bg_layer = base_bg.copy()
        tint = Image.new("RGBA", (1280, 720), spec["bg_color"] + (180,))
        bg_layer = Image.alpha_composite(bg_layer, tint)
        canvas.paste(bg_layer, (0, 0))

    draw = ImageDraw.Draw(canvas)

    # 2. Cargar y posicionar Avatar a la izquierda
    avatar_path = PUBLIC_DIR / spec["avatar"]
    if not avatar_path.exists():
        avatar_path = PUBLIC_DIR / "avatar_transparent.png"
        
    if avatar_path.exists():
        try:
            av_img = Image.open(avatar_path).convert("RGBA")
            # Resize avatar a altura ~680px manteniendo aspecto
            aspect = av_img.width / av_img.height
            new_h = 680
            new_w = int(new_h * aspect)
            av_img = av_img.resize((new_w, new_h), Image.LANCZOS)
            
            # Glow Aura detrás del avatar
            aura = Image.new("RGBA", (new_w + 100, new_h + 100), (0, 0, 0, 0))
            aura_draw = ImageDraw.Draw(aura)
            aura_draw.ellipse([50, 50, new_w + 50, new_h + 50], fill=spec["badge_bg"] + (100,))
            aura = aura.filter(ImageFilter.GaussianBlur(40))
            
            canvas.paste(aura, (20, 10), aura)
            canvas.paste(av_img, (70, 40), av_img)
        except Exception as e:
            print(f"Error procesando avatar {spec['avatar']}: {e}")

    # 3. Dibujar Tipografía y Badges de YouTube
    # Try loading default font
    try:
        font_large = ImageFont.truetype("arial.ttf", 52)
        font_badge = ImageFont.truetype("arialbd.ttf", 26)
        font_medium = ImageFont.truetype("arialbd.ttf", 38)
    except Exception:
        font_large = font_badge = font_medium = ImageFont.load_default()

    # Badge Top (Pill Box)
    bx1, by1 = 580, 140
    bx2, by2 = 1180, 200
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=12, fill=spec["badge_bg"] + (230,), outline=(255, 255, 255, 200), width=2)
    draw.text((bx1 + 20, by1 + 10), spec["badge"], fill=(255, 255, 255), font=font_badge)

    # Título Principal (Línea 1 - Dorado/Amarillo con Sombra)
    tx, ty = 580, 240
    # Shadow
    draw.text((tx + 3, ty + 3), spec["title_top"], fill=(0, 0, 0, 230), font=font_large)
    draw.text((tx, ty), spec["title_top"], fill=(255, 215, 0), font=font_large)

    # Título Sub (Línea 2 - Blanco Neón)
    ty2 = 320
    draw.text((tx + 3, ty2 + 3), spec["title_bot"], fill=(0, 0, 0, 230), font=font_medium)
    draw.text((tx, ty2), spec["title_bot"], fill=(255, 255, 255), font=font_medium)

    # Badge de Marca Inferior ("HB JEWELRY 18K • 1080p HD")
    draw.rectangle([580, 410, 1180, 414], fill=spec["badge_bg"])
    draw.text((580, 430), "HB JEWELRY 18K • OPENCLAW 2026.7.1", fill=(180, 180, 180), font=font_badge)

    # 4. Guardar PNG en thumbnails/
    out_file = THUMB_DIR / spec["file"]
    canvas.convert("RGB").save(out_file, "PNG", quality=95)
    print(f"✅ Thumbnail YouTube Creado Exitosamente: {spec['file']}")

print("🎨 ¡Los 12 Thumbnails Únicos de YouTube han sido generados limpiamente!")
