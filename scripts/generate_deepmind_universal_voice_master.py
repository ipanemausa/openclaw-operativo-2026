"""
==============================================================================
HB. OS OPERATION SYSTEM — DEEPMIND MASTERCLASS (UNIVERSAL VOICE CLONE ENGINE)
==============================================================================
- Guion: 6 Módulos Google DeepMind & Demis Hassabis (AlphaGo, AlphaFold, Poro Nuclear, etc.)
- Narrador: Guillermo Hoyos (Inyección Universal de Clon de Voz)
- Branding: HB. OS Operation system · Sovereign AI
- Video: 1080p HD Cristalino con B-Roll Lanczos y Avatar Transparente
==============================================================================
"""

import os
import sys
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from universal_voice_narrator_hbos import HBOSUniversalVoiceEngine

PROD_DIR = ROOT / "runtime" / "productions" / "2026-08-24_deepmind_universal_voice_master"
PROD_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR = PROD_DIR / "frames_hd"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)
CAPTURES_DIR = ROOT / "capturas_recientes"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

DEEPMIND_MODULES = [
    {
        "module_id": "MOD_01",
        "chapter_num": 1,
        "title": "El Dominio de los Juegos y la Búsqueda Exponencial",
        "subtitle": "De AlphaGo y la jugada Move 37 a AlphaStar en tiempo real",
        "capture_start": 1,
        "capture_end": 8,
        "text": (
            "Bienvenidos a HB punto OS Operating System. Para comprender hacia dónde se dirige la inteligencia "
            "artificial general, debemos analizar los hitos fundamentales logrados por Demis Hassabis y Google "
            "DeepMind. Todo comenzó con la resolución de espacios de búsqueda complejos. Desde la histórica "
            "jugada número treinta y siete de AlphaGo contra Lee Sedol, hasta la maestría táctica en tiempo "
            "real con AlphaStar en StarCraft dos, la inteligencia artificial demostró que el aprendizaje por "
            "refuerzo profundo no solo iguala al ser humano, sino que descubre estrategias totalmente nuevas "
            "e intuitivas."
        )
    },
    {
        "module_id": "MOD_02",
        "chapter_num": 2,
        "title": "El Gran Momento Decisivo: AlphaFold",
        "subtitle": "Resolviendo el desafío biológico de 50 años en 3D",
        "capture_start": 9,
        "capture_end": 16,
        "text": (
            "Pero el verdadero punto de inflexión para la humanidad ocurrió cuando DeepMind llevó estos principios "
            "a la ciencia pura. Durante cincuenta años, el problema del plegamiento de proteínas fue considerado "
            "el mayor enigma biológico. Con AlphaFold, lograron predecir la estructura tridimensional de más de "
            "doscientos millones de proteínas, cubriendo prácticamente todo el universo proteico conocido. Esta "
            "base de datos global, adoptada hoy por millones de investigadores, transformó décadas de trabajo "
            "experimental en segundos computacionales."
        )
    },
    {
        "module_id": "MOD_03",
        "chapter_num": 3,
        "title": "Arquitectura Molecular: El Complejo del Poro Nuclear",
        "subtitle": "Mapeando la máquina biológica más intrincada de la célula",
        "capture_start": 17,
        "capture_end": 22,
        "text": (
            "El alcance de esta tecnología no se limitó a proteínas aisladas. AlphaFold permitió mapear complejos "
            "macromoleculares gigantescos como el complejo del poro nuclear, la puerta de enlace que regula el "
            "transporte genético en nuestras células. Lo que antes requería años de cristalografía de rayos X y "
            "microscopía crioelectrónica, ahora puede ser modelado con precisión atómica, abriendo una ventana "
            "sin precedentes a la maquinaria fundamental de la vida."
        )
    },
    {
        "module_id": "MOD_04",
        "chapter_num": 4,
        "title": "Genómica y Diseño de Fármacos in Silico",
        "subtitle": "AlphaGenome y la exploración del noventa y ocho por ciento no codificante",
        "capture_start": 23,
        "capture_end": 28,
        "text": (
            "El siguiente gran salto es el diseño de fármacos in silico y la comprensión del genoma humano. "
            "A través de iniciativas como AlphaGenome, estamos comenzando a descifrar el noventa y ocho por "
            "ciento del ADN que anteriormente se consideraba no codificante o basura genética. Esta capacidad "
            "permite predecir el acoplamiento químico directo de moléculas candidatas, acelerando el desarrollo "
            "de terapias personalizadas para enfermedades complejas a una fracción del costo tradicional."
        )
    },
    {
        "module_id": "MOD_05",
        "chapter_num": 5,
        "title": "Modelos de Mundo y Robótica Física",
        "subtitle": "Cerrando la brecha entre la percepción digital y la acción material",
        "capture_start": 29,
        "capture_end": 34,
        "text": (
            "Demis Hassabis enfatiza que el futuro de la inteligencia artificial radica en los Modelos de Mundo. "
            "Para interactuar con el entorno físico a través de la robótica, los agentes no pueden depender "
            "únicamente de patrones textuales; deben internalizar la física, el espacio tridimensional, la causa "
            "y el efecto. Estos modelos de mundo permiten a los robots aprender tareas complejas en simulación "
            "y ejecutarlas en el mundo real con destreza y seguridad."
        )
    },
    {
        "module_id": "MOD_06",
        "chapter_num": 6,
        "title": "Soberanía Computacional y Ciencia Autónoma",
        "subtitle": "La IA como el microscopio definitivo del siglo veintiuno",
        "capture_start": 35,
        "capture_end": 40,
        "text": (
            "En HB punto OS Operating System consolidamos esta visión bajo el principio de la Soberanía Tecnológica. "
            "La inteligencia artificial no es solo un asistente conversacional; es el instrumento científico "
            "definitivo para acelerar el descubrimiento humano. Integrando vectores en espacio de dimensión "
            "setecientos sesenta y ocho, orquestación determinista y modelos abiertos, construimos la "
            "infraestructura de automatización del futuro. Gracias por acompañarnos en este recorrido por la "
            "frontera del conocimiento."
        )
    }
]

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def render_deepmind_masterclass():
    print("=" * 75)
    print("  HB.OS — MOTOR DE NARRACIÓN UNIVERSAL (PRODUCCIÓN DEEPMIND MASTER)")
    print("=" * 75)

    voice_engine = HBOSUniversalVoiceEngine()

    # 1. Narrar cada módulo con el clon de Guillermo
    for mod in DEEPMIND_MODULES:
        mod_audio = PROD_DIR / f"{mod['module_id']}_guillermo_voice.aac"
        voice_engine.narrate_script(mod["text"], mod_audio)
        mod["audio_file"] = str(mod_audio)
        mod["duration"] = get_audio_duration(mod_audio)

    # 2. Ensamblar pista continua
    pause_file = PROD_DIR / "pause_1s.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.0", "-c:a", "aac", "-b:a", "256k", str(pause_file)
    ]
    subprocess.run(cmd_pause, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    manifest_path = PROD_DIR / "concat_audio.txt"
    with open(manifest_path, "w", encoding="utf-8") as f:
        for mod in DEEPMIND_MODULES:
            f.write(f"file '{Path(mod['audio_file']).as_posix()}'\n")
            f.write(f"file '{pause_file.as_posix()}'\n")

    master_audio = PROD_DIR / "PROD_HBOS_DEEPMIND_AUDIO_MASTER.aac"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(manifest_path), "-c", "copy", str(master_audio)], check=True)
    total_dur = get_audio_duration(master_audio)
    print(f"  ✓ Soundtrack Maestro generado por tu clon: {total_dur:.2f}s ({total_dur/60:.2f} min)")

if __name__ == "__main__":
    render_deepmind_masterclass()
