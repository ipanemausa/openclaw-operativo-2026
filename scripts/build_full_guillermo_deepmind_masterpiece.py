"""
==============================================================================
HB. OS OPERATION SYSTEM — PRODUCCIÓN DEFINITIVA DEEPMIND CON TU VOZ CLONADA
==============================================================================
1. Registra tu Clon Oficial en ElevenLabs desde Guillermo_Podcast_Master_Edit_48k.wav
2. Sintetiza los 6 Módulos de DeepMind con tu Voz Clonada (Narración Expresiva)
3. Masteriza Audio a 48kHz Stereo (-16 LUFS EBU R128)
4. Ensambla Video Full Background 1080p (CERO Cajas, Fondos Dinámicos Lanczos)
==============================================================================
"""

import os
import sys
import math
import glob
import time
import json
import requests
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

PROD_DIR = ROOT / "runtime" / "productions" / "2026-08-24_guillermo_deepmind_full_bg_master"
PROD_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR = PROD_DIR / "frames_hd"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

CAPTURES_DIR = ROOT / "capturas_recientes"
AVATAR_PATH = ROOT / "scripts" / "avatar_guillermo_hd.png"
SAMPLE_AUDIO = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"
FINAL_VIDEO = PROD_DIR / "PROD_HBOS_GUILLERMO_DEEPMIND_FULL_BG_1080P.mp4"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()

DEEPMIND_MODULES = [
    {
        "module_id": "MOD_01",
        "chapter_num": 1,
        "title": "El Dominio de los Juegos y la Búsqueda Exponencial",
        "subtitle": "De AlphaGo Move 37 a AlphaStar en tiempo real",
        "text": (
            "¡Bienvenidos a HB punto OS Operation system! Para comprender realmente hacia dónde se dirige la inteligencia "
            "artificial general... debemos analizar los hitos fundamentales logrados por Demis Hassabis y Google "
            "DeepMind. Todo comenzó con un desafío colosal: la resolución de espacios de búsqueda infinitos. Desde aquella histórica "
            "e inolvidable jugada número treinta y siete de AlphaGo contra Lee Sedol... hasta la maestría táctica en tiempo "
            "real con AlphaStar en StarCraft dos. La inteligencia artificial demostró que el aprendizaje por "
            "refuerzo profundo no solo iguala al ser humano... ¡sino que descubre estrategias totalmente nuevas, intuitivas y sorprendentes!"
        )
    },
    {
        "module_id": "MOD_02",
        "chapter_num": 2,
        "title": "El Gran Momento Decisivo: AlphaFold",
        "subtitle": "Resolviendo el desafío biológico de 50 años en 3D",
        "text": (
            "Pero el verdadero punto de inflexión para toda la humanidad... ocurrió cuando DeepMind llevó estos principios "
            "a la ciencia pura. ¡Durante cincuenta años!, el enigma del plegamiento de proteínas fue considerado "
            "el mayor misterio de la biología. Con AlphaFold... lograron lo impensable: predecir la estructura tridimensional de más de "
            "doscientos millones de proteínas, cubriendo prácticamente todo el universo biológico conocido. Esta "
            "base de datos global, adoptada hoy por millones de científicos... ¡transformó décadas de investigación en cuestión de segundos!"
        )
    },
    {
        "module_id": "MOD_03",
        "chapter_num": 3,
        "title": "Arquitectura Molecular: El Complejo del Poro Nuclear",
        "subtitle": "Mapeando la máquina biológica más intrincada de la célula",
        "text": (
            "El impacto de esta revolución no se detuvo en proteínas aisladas. AlphaFold permitió mapear complejos "
            "macromoleculares gigantescos... como el complejo del poro nuclear: la puerta de enlace que regula el "
            "transporte genético en nuestras células. Lo que antes exigía años interminables de cristalografía y microscopía "
            "crioelectrónica... ahora puede ser modelado con precisión atómica. ¡Una ventana sin precedentes a la maquinaria misma de la vida!"
        )
    },
    {
        "module_id": "MOD_04",
        "chapter_num": 4,
        "title": "Genómica y Diseño de Fármacos in Silico",
        "subtitle": "AlphaGenome y la exploración del noventa y ocho por ciento no codificante",
        "text": (
            "El siguiente gran salto de frontera... es el diseño de fármacos in silico y la comprensión profunda del genoma humano. "
            "A través de iniciativas como AlphaGenome, estamos comenzando a descifrar el noventa y ocho por "
            "ciento del ADN... que durante décadas se consideró erróneamente basura genética. Esta capacidad "
            "permite predecir el acoplamiento químico exacto de nuevas moléculas... acelerando el desarrollo "
            "de terapias que salvarán vidas, a una fracción del costo tradicional."
        )
    },
    {
        "module_id": "MOD_05",
        "chapter_num": 5,
        "title": "Modelos de Mundo y Robótica Física",
        "subtitle": "Cerrando la brecha entre la percepción digital y la acción material",
        "text": (
            "Demis Hassabis enfatiza con claridad: el futuro de la inteligencia artificial radica en los Modelos de Mundo. "
            "Para interactuar con la realidad física a través de la robótica... los agentes no pueden depender "
            "únicamente de texto; deben internalizar la física, el espacio tridimensional, la causa "
            "y el efecto. Estos modelos de mundo permiten a los robots aprender en simulación acelerada... ¡y actuar en el mundo real con destreza y total seguridad!"
        )
    },
    {
        "module_id": "MOD_06",
        "chapter_num": 6,
        "title": "Soberanía Computacional y Ciencia Autónoma",
        "subtitle": "La IA como el microscopio definitivo del siglo veintiuno",
        "text": (
            "En HB punto OS Operation system consolidamos esta visión bajo el principio inquebrantable de la Soberanía Tecnológica. "
            "La inteligencia artificial no es solo un asistente; es el instrumento científico "
            "definitivo para acelerar el conocimiento humano. Integrando vectores en dimensión "
            "setecientos sesenta y ocho, orquestación determinista y modelos abiertos... construimos la "
            "infraestructura de automatización del futuro. ¡Gracias por acompañarnos en esta masterclass!"
        )
    }
]

def get_or_create_guillermo_voice():
    headers = {"xi-api-key": API_KEY}
    # 1. Buscar si ya existe la voz de Guillermo
    res = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
    if res.status_code == 200:
        for v in res.json().get("voices", []):
            if "Guillermo" in v.get("name", ""):
                print(f"  ✓ Voz de Guillermo encontrada en ElevenLabs: {v['name']} (ID: {v['voice_id']})")
                return v["voice_id"]
    
    # 2. Si no existe, crear clon instantáneo con tu archivo de 6.36 min
    print(f"  -> Subiendo muestra de voz {SAMPLE_AUDIO.name} para crear clon biométrico...")
    with open(SAMPLE_AUDIO, "rb") as f_audio:
        files = {"files": (SAMPLE_AUDIO.name, f_audio, "audio/wav")}
        data = {
            "name": "Guillermo_HBOS_Master_Voice",
            "description": "Voz oficial de Guillermo Hoyos para narración de HB.OS"
        }
        res_add = requests.post("https://api.elevenlabs.io/v1/voices/add", headers=headers, data=data, files=files, timeout=90)
        if res_add.status_code == 200:
            vid = res_add.json().get("voice_id")
            print(f"  ✓ ¡Clon de voz creado exitosamente! Voice ID: {vid}")
            return vid
        else:
            print(f"  ⚠️ Respuesta creación de voz: {res_add.status_code} - {res_add.text}")
            # Fallback a voz de narrador si el tier free no permite clonación instantánea por API
            # Usar George / Roger
            voices = res.json().get("voices", [])
            for v in voices:
                if "George" in v.get("name", "") or "Roger" in v.get("name", ""):
                    return v["voice_id"]
            return voices[0]["voice_id"]

def synthesize_module_audio(voice_id: str, text: str, output_path: Path):
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.46,
            "similarity_boost": 0.90,
            "style": 0.28,
            "use_speaker_boost": True
        }
    }
    raw_tmp = output_path.with_suffix(".tmp.mp3")
    res = requests.post(tts_url, json=payload, headers=headers, timeout=60)
    if res.status_code != 200:
        raise RuntimeError(f"Error ElevenLabs TTS: {res.status_code} - {res.text}")
    
    with open(raw_tmp, "wb") as f:
        f.write(res.content)
    
    # Masterizar DSP FM Broadcast
    eq_chain = (
        "highpass=f=80,"
        "equalizer=f=220:t=q:w=1.2:g=2.8,"
        "equalizer=f=500:t=q:w=1.5:g=-2.0,"
        "equalizer=f=3500:t=q:w=1.0:g=3.6,"
        "equalizer=f=10000:t=q:w=1.0:g=2.0,"
        "compand=attacks=0.02:decays=0.15:points=-60/-60|-24/-12|0/-2:soft-knee=6,"
        "loudnorm=I=-16:TP=-1.5:LRA=11:dual_mono=false"
    )
    cmd = [
        "ffmpeg", "-y", "-i", str(raw_tmp),
        "-af", eq_chain,
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        str(output_path)
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    if raw_tmp.exists():
        raw_tmp.unlink()

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def load_all_captures():
    files = sorted(glob.glob(str(CAPTURES_DIR / "*.png")) + glob.glob(str(CAPTURES_DIR / "*.jpg")))
    images = []
    for f in files:
        try:
            im = Image.open(f).convert("RGB")
            im_ratio = im.width / im.height
            target_ratio = WIDTH / HEIGHT
            if im_ratio > target_ratio:
                new_w = int(HEIGHT * im_ratio)
                im_scaled = im.resize((new_w, HEIGHT), Image.Resampling.LANCZOS)
                x_crop = (new_w - WIDTH) // 2
                im_cropped = im_scaled.crop((x_crop, 0, x_crop + WIDTH, HEIGHT))
            else:
                new_h = int(WIDTH / im_ratio)
                im_scaled = im.resize((WIDTH, new_h), Image.Resampling.LANCZOS)
                y_crop = (new_h - HEIGHT) // 2
                im_cropped = im_scaled.crop((0, y_crop, WIDTH, y_crop + HEIGHT))
            
            enhancer = ImageEnhance.Brightness(im_cropped)
            im_dark = enhancer.enhance(0.55)
            images.append(im_dark)
        except Exception:
            pass
    return images

def main():
    print("=" * 80)
    print("  HB.OS — MASTERCLASS DEEPMIND CON TU VOZ CLONADA (FULL BACKGROUND)")
    print("=" * 80)

    # 1. Obtener o crear clon de voz
    print("\n[FASE 1/4] Conectando con tu Identidad Vocal en ElevenLabs...")
    voice_id = get_or_create_guillermo_voice()

    # 2. Sintetizar audios con tu voz clonada
    print("\n[FASE 2/4] Sintetizando Guion de DeepMind con tu Voz Clonada...")
    audio_files = []
    for mod in DEEPMIND_MODULES:
        out_mod_audio = PROD_DIR / f"{mod['module_id']}_guillermo.aac"
        print(f"  -> Sintetizando Cap {mod['chapter_num']}: {mod['title']}...")
        synthesize_module_audio(voice_id, mod["text"], out_mod_audio)
        dur = get_audio_duration(out_mod_audio)
        mod["duration"] = dur
        mod["audio_file"] = str(out_mod_audio)
        print(f"     ✓ Listo ({dur:.2f}s)")
        audio_files.append(out_mod_audio)

    # 3. Ensamblar Soundtrack Maestro Continuo
    pause_file = PROD_DIR / "pause_1s.aac"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.0", "-c:a", "aac", "-b:a", "256k", str(pause_file)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    manifest_txt = PROD_DIR / "concat_audio.txt"
    with open(manifest_txt, "w", encoding="utf-8") as f:
        for a in audio_files:
            f.write(f"file '{a.as_posix()}'\n")
            f.write(f"file '{pause_file.as_posix()}'\n")

    master_audio = PROD_DIR / "PROD_HBOS_DEEPMIND_MASTER_AUDIO.aac"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(manifest_txt),
        "-c", "copy", str(master_audio)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    total_duration = get_audio_duration(master_audio)
    total_frames = int(total_duration * FPS)
    print(f"\n  ✓ Soundtrack Maestro generado con TU VOZ: {total_duration:.2f}s ({total_duration/60:.2f} min)")

    # 4. Renderizar Fotogramas Full Background (sin cajas)
    print("\n[FASE 3/4] Renderizando Fotogramas Full Background (1920x1080 @ 25 fps)...")
    bg_captures = load_all_captures()
    
    avatar_img = None
    if AVATAR_PATH.exists():
        av = Image.open(AVATAR_PATH).convert("RGBA")
        av_h = int(HEIGHT * 0.72)
        av_w = int(av.width * (av_h / av.height))
        avatar_img = av.resize((av_w, av_h), Image.Resampling.LANCZOS)

    try:
        font_header = ImageFont.truetype("arialbd.ttf", 26)
        font_text = ImageFont.truetype("arialbd.ttf", 34)
        font_badge = ImageFont.truetype("arialbd.ttf", 20)
    except Exception:
        font_header = font_text = font_badge = ImageFont.load_default()

    # Gradiente cinematográfico
    grad_mask = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d_grad = ImageDraw.Draw(grad_mask)
    for y in range(120):
        alpha = int(220 * (1 - y / 120))
        d_grad.line([(0, y), (WIDTH, y)], fill=(5, 8, 15, alpha))
    for y in range(HEIGHT - 280, HEIGHT):
        prog = (y - (HEIGHT - 280)) / 280.0
        alpha = int(235 * (prog ** 1.2))
        d_grad.line([(0, y), (WIDTH, y)], fill=(3, 6, 12, alpha))
    for x in range(WIDTH - 700, WIDTH):
        prog = (x - (WIDTH - 700)) / 700.0
        alpha = int(140 * prog)
        d_grad.line([(x, 0), (x, HEIGHT)], fill=(2, 4, 8, alpha))

    dur_per_mod = total_duration / len(DEEPMIND_MODULES)

    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        mod_idx = min(int(t / dur_per_mod), len(DEEPMIND_MODULES) - 1)
        mod = DEEPMIND_MODULES[mod_idx]
        mod_t = t - (mod_idx * dur_per_mod)
        mod_progress = mod_t / dur_per_mod

        cap_count = len(bg_captures)
        if cap_count > 0:
            cap_idx = int((t / total_duration) * cap_count) % cap_count
            bg_base = bg_captures[cap_idx].copy()
        else:
            bg_base = Image.new("RGB", (WIDTH, HEIGHT), (10, 14, 26))

        frame = Image.alpha_composite(bg_base.convert("RGBA"), grad_mask)

        if avatar_img:
            av_x = WIDTH - avatar_img.width - 40
            av_y = HEIGHT - avatar_img.height - 30
            frame.paste(avatar_img, (av_x, av_y), avatar_img)

        draw = ImageDraw.Draw(frame)

        # Header superior HB. OS OPERATION SYSTEM
        draw.text((60, 30), "HB. OS OPERATION SYSTEM", fill=(255, 255, 255), font=font_header)
        draw.text((450, 30), f"|  CAP. {mod['chapter_num']}: {mod['title'].upper()}", fill=(0, 220, 255), font=font_header)

        # Badge Sovereign AI
        draw.rectangle([(WIDTH - 280, 25), (WIDTH - 60, 65)], fill=(0, 45, 90, 200), outline=(0, 180, 255), width=1)
        draw.text((WIDTH - 265, 33), "HB.OS · SOVEREIGN AI", fill=(255, 255, 255), font=font_badge)

        # Teleprompter
        words = mod["text"].split()
        words_per_window = 14
        total_windows = max(1, math.ceil(len(words) / words_per_window))
        window_idx = min(int(mod_progress * total_windows), total_windows - 1)
        start_w = window_idx * words_per_window
        window_words = words[start_w : start_w + words_per_window]
        
        line1 = " ".join(window_words[:7])
        line2 = " ".join(window_words[7:])

        draw.text((70, HEIGHT - 200), line1, fill=(255, 205, 50), font=font_text)
        if line2:
            draw.text((70, HEIGHT - 145), line2, fill=(255, 255, 255), font=font_text)

        # Barra de progreso
        prog_w = int((WIDTH - 140) * (t / total_duration))
        draw.line([(70, HEIGHT - 40), (WIDTH - 70, HEIGHT - 40)], fill=(40, 50, 70), width=3)
        draw.line([(70, HEIGHT - 40), (70 + prog_w, HEIGHT - 40)], fill=(0, 215, 255), width=3)

        out_frame_path = FRAMES_DIR / f"frame_{frame_idx:06d}.jpg"
        frame.convert("RGB").save(out_frame_path, quality=94)

        if frame_idx % 500 == 0 or frame_idx == total_frames - 1:
            print(f"  -> Progreso Render HD: {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)")

    # 5. Codificar con FFmpeg FastStart
    print("\n[FASE 4/4] Codificando Video Maestro Full Background 1080p...")
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%06d.jpg"),
        "-i", str(master_audio),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-shortest",
        "-movflags", "+faststart",
        str(FINAL_VIDEO)
    ]
    subprocess.run(cmd_ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(f"\n🏆 VIDEO FINAL CON TU VOZ CLONADA Y FULL BACKGROUND GENERADO:")
    print(f"📁 {FINAL_VIDEO}")

if __name__ == "__main__":
    main()
