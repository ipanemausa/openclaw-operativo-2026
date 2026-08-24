"""
==============================================================================
HB.OS (OPERATING SYSTEM) — MOTOR DE NARRACIÓN UNIVERSAL EXPRESIVA (GUILLERMO)
==============================================================================
Dirección Automática de Narración Emocional (CERO Lectura Plana):
Formatos soportados:
  - 'podcast': Barítono cálido, pausas reflexivas de 500ms, tono íntimo.
  - 'video_youtube': Dinámico, ganchos de asombro, aceleraciones y silencios.
  - 'masterclass': Autoridad docente, realce de definiciones y preguntas retóricas.
  - 'conferencia': Tono épico estilo Jensen Huang, pausas dramáticas de 700ms.
  - 'entrevista': Espontáneo, cadencia conversacional orgánica.
==============================================================================
"""

import os
import sys
import json
import time
import re
import hashlib
import requests
import subprocess
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

SAMPLE_AUDIO = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"
VOICE_CACHE_DIR = ROOT / "runtime" / "universal_voice_cache"
VOICE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = ROOT / "runtime" / "guillermo_voice_clone_config.json"

# Matriz de Parámetros Prosódicos por Formato
FORMAT_PROSODY_MATRIX = {
    "podcast": {
        "stability": 0.45,
        "similarity_boost": 0.90,
        "style": 0.25,
        "pause_comma_ms": 300,
        "pause_period_ms": 600,
        "use_speaker_boost": True
    },
    "video_youtube": {
        "stability": 0.42,
        "similarity_boost": 0.92,
        "style": 0.35,
        "pause_comma_ms": 250,
        "pause_period_ms": 500,
        "use_speaker_boost": True
    },
    "masterclass": {
        "stability": 0.48,
        "similarity_boost": 0.92,
        "style": 0.30,
        "pause_comma_ms": 350,
        "pause_period_ms": 650,
        "use_speaker_boost": True
    },
    "conferencia": {
        "stability": 0.44,
        "similarity_boost": 0.94,
        "style": 0.40,
        "pause_comma_ms": 400,
        "pause_period_ms": 800,
        "use_speaker_boost": True
    },
    "entrevista": {
        "stability": 0.40,
        "similarity_boost": 0.88,
        "style": 0.20,
        "pause_comma_ms": 200,
        "pause_period_ms": 450,
        "use_speaker_boost": True
    }
}

class HBOSUniversalVoiceEngine:
    """Motor de Inyección Universal de Voz Expresiva de Guillermo para HB.OS"""

    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
        self.voice_id = self._load_or_register_voice_clone()

    def _load_or_register_voice_clone(self) -> str:
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    vid = cfg.get("voice_id")
                    if vid:
                        return vid
            except Exception:
                pass

        if not self.api_key:
            return ""

        headers = {"xi-api-key": self.api_key}
        try:
            res = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers, timeout=10)
            if res.status_code == 200:
                voices = res.json().get("voices", [])
                for v in voices:
                    if "Guillermo" in v.get("name", ""):
                        vid = v["voice_id"]
                        self._save_voice_id(vid)
                        return vid

            if SAMPLE_AUDIO.exists():
                print(f"[HB.OS] Registrando clon biométrico oficial desde: {SAMPLE_AUDIO.name}...")
                with open(SAMPLE_AUDIO, "rb") as f:
                    files = {"files": (SAMPLE_AUDIO.name, f, "audio/wav")}
                    data = {
                        "name": "Guillermo_HBOS_Universal_Voice",
                        "description": "Voz oficial de Guillermo Hoyos para narración universal HB.OS"
                    }
                    res_add = requests.post("https://api.elevenlabs.io/v1/voices/add", headers=headers, data=data, files=files, timeout=60)
                    if res_add.status_code == 200:
                        vid = res_add.json().get("voice_id")
                        self._save_voice_id(vid)
                        print(f"[HB.OS] ¡Clon de Guillermo registrado! Voice ID: {vid}")
                        return vid
        except Exception as e:
            print(f"[HB.OS] Error en registro de voz: {e}")

        return ""

    def _save_voice_id(self, voice_id: str):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "voice_id": voice_id,
                "voice_name": "Guillermo_HBOS_Universal_Voice",
                "sample_reference": str(SAMPLE_AUDIO),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }, f, indent=2)

    def format_expressive_script(self, raw_text: str, mode: str = "masterclass") -> str:
        """Enriquece el guion con puntuación prosódica teatral y pausas de respiración."""
        text = raw_text.strip()
        # Enfatizar acápites reflexivos
        text = re.sub(r'\s+—\s+', '... — ', text)
        text = re.sub(r'(\bPor lo tanto\b|\bSin embargo\b|\bEn consecuencia\b|\bEn efecto\b),', r'\1...', text)
        return text

    def apply_fm_broadcast_dsp(self, input_audio: Path, output_audio: Path):
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
            "ffmpeg", "-y", "-i", str(input_audio),
            "-af", eq_chain,
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            str(output_audio)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    def narrate_script(self, text: str, output_aac: Path, mode: str = "masterclass", language: str = "es") -> Path:
        """
        Narra CUALQUIER texto con la voz de Guillermo aplicando el modo de narración emocional.
        
        Args:
            text: Guion a narrar
            output_aac: Ruta de salida (48kHz Stereo)
            mode: 'podcast' | 'video_youtube' | 'masterclass' | 'conferencia' | 'entrevista'
            language: 'es' | 'en' | 'zh'
        """
        cfg = FORMAT_PROSODY_MATRIX.get(mode, FORMAT_PROSODY_MATRIX["masterclass"])
        expressive_text = self.format_expressive_script(text, mode=mode)
        
        text_hash = hashlib.md5(f"{expressive_text}_{mode}".encode("utf-8")).hexdigest()[:10]
        temp_mp3 = VOICE_CACHE_DIR / f"raw_narration_{mode}_{language}_{text_hash}.mp3"
        output_aac = Path(output_aac)
        output_aac.parent.mkdir(parents=True, exist_ok=True)

        if not self.api_key:
            print("\n" + "=" * 75)
            print("  ❌ [BLOQUEO AGENTS.md] ELEVENLABS_API_KEY no configurada.")
            print("  Por regla de blindaje inmutable, el sistema NO usa voces sintéticas planas.")
            print("  -> Configura tu clave en: C:\\Users\\ipane\\.openclaw-master.env")
            print("=" * 75)
            sys.exit(1)

        if not self.voice_id:
            self.voice_id = self._load_or_register_voice_clone()

        print(f"\n[HB.OS NARRACIÓN] Modo: {mode.upper()} | Clon Voice ID: {self.voice_id}")
        print(f"  Estabilidad: {cfg['stability']} | Estilo Teatral: {cfg['style']}")

        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {"xi-api-key": self.api_key, "Content-Type": "application/json"}
        payload = {
            "text": expressive_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": cfg["stability"],
                "similarity_boost": cfg["similarity_boost"],
                "style": cfg["style"],
                "use_speaker_boost": cfg["use_speaker_boost"]
            }
        }

        t0 = time.time()
        res = requests.post(tts_url, json=payload, headers=headers, timeout=60)
        if res.status_code != 200:
            print(f"❌ Error ElevenLabs: HTTP {res.status_code} - {res.text}")
            sys.exit(1)

        with open(temp_mp3, "wb") as f_out:
            f_out.write(res.content)

        elapsed = time.time() - t0
        print(f"  ✓ Narración generada en {elapsed:.2f}s")
        self.apply_fm_broadcast_dsp(temp_mp3, output_aac)
        return output_aac

if __name__ == "__main__":
    engine = HBOSUniversalVoiceEngine()
    print("HBOS Universal Voice Engine (Expressive Narration) Listo.")
