import os, sys, math, json, asyncio, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

ROOT = Path(__file__).parent.parent
SPEAKER_WAV = ROOT / 'runtime' / 'guillermo_podcast_master' / 'Guillermo_Podcast_Master_Edit_48k.wav'
PROD_DIR = ROOT / 'runtime' / 'productions' / '2026-08-24_deepmind_hassabis_HBOS_v2'
PROD_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR = PROD_DIR / 'frames_v2'
FRAMES_DIR.mkdir(parents=True, exist_ok=True)
CAPTURES_DIR = ROOT / 'capturas_recientes'
WIDTH, HEIGHT = 1920, 1080
FPS = 25
print('OK')
