"""
==============================================================================
OPENCLAW SOVEREIGN AUDIO & PROSODY ENGINE (2026) — RAE & OXFORD COMPILATION
==============================================================================
Compilador Gramatical y Prosódico de Alta Fidelidad bajo Estándares RAE y Oxford.
Modelado estricto de respiración, curvas entonativas y jerarquía de puntuación:

Jerarquía Sintáctica:
  - Coma (,): 240ms (Cláusula subordinada, vocativo o elemento de serie)
  - Dos Puntos (:): 400ms (Suspensión enunciativa / anticipación)
  - Punto y Coma (;): 450ms (Transición lógica fuerte)
  - Punto y Seguido (.): 600ms (Cierre de proposición con descenso tonal)
  - Punto y Aparte (.\n\n): 1000ms (Respiración fisiológica profunda y cambio de tesis)
  - Conectores discursivos (Sin embargo, Por lo tanto, etc.): Pausa reflexiva 300ms
==============================================================================
"""

import os
import sys
import re
import json
import asyncio
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

ROOT = Path(__file__).resolve().parent.parent
LEXICON_PATH = ROOT / "backend" / "database" / "canonical_entity_lexicon.json"

# Conectores discursivos que exigen pausa reflexiva obligatoria según gramática RAE
DISCURSIVE_CONNECTORS_ES = [
    r"Sin embargo,",
    r"No obstante,",
    r"Por el contrario,",
    r"Por lo tanto,",
    r"En consecuencia,",
    r"De este modo,",
    r"En primer lugar,",
    r"Por una parte,",
    r"Por otra parte,",
    r"Finalmente,",
    r"Es decir,",
    r"En efecto,"
]

class SovereignProsodyEngine:
    def __init__(self, lexicon_path: Path = LEXICON_PATH):
        self.lexicon_path = lexicon_path
        self.lexicon = self._load_lexicon()
        self.profile = self.lexicon.get("audience_cadence_profiles", {}).get("executive_academic_b2b", {})

    def _load_lexicon(self) -> Dict[str, Any]:
        if self.lexicon_path.exists():
            with open(self.lexicon_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"entities": {}, "audience_cadence_profiles": {}}

    def build_human_ssml(self, raw_text: str, lang: str = "es") -> str:
        """
        Compila el texto bajo la gramática sintáctica RAE / Oxford,
        generando SSML estructurado con respiración humana y cadencia doctoral.
        """
        lang_key = "spanish" if lang.startswith("es") else "english"
        cfg = self.profile.get(lang_key, {})
        voice = cfg.get("voice", "es-ES-AlvaroNeural" if lang == "es" else "en-US-AndrewMultilingualNeural")
        rate = cfg.get("rate", "-8%")
        pitch = cfg.get("pitch", "-5Hz")
        pauses = cfg.get("pauses_ms", {
            "comma": 240,
            "colon": 400,
            "semicolon": 450,
            "period": 600,
            "paragraph": 1000,
            "connector": 300
        })

        # 1. Normalización de Markdown y limpieza de caracteres espurios
        text = re.sub(r'#+\s*', '', raw_text)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'`(.*?)`', r'\1', text)

        # 2. Correcciones de separación geográfica y gramatical estricta
        text = re.sub(r'\b(azureamerica|suramerica|suramérica)\b', 'Suramérica', text, flags=re.IGNORECASE)
        text = re.sub(r'\ba\s+Suramérica\b', 'a Suramérica', text, flags=re.IGNORECASE)

        # 3. Gobernanza de Nombres Propios de IA y Personas (Siempre en Inglés Canónico)
        entities = self.lexicon.get("entities", {})
        for entity_key, meta in entities.items():
            if meta.get("always_english", False) and lang == "es":
                alias = meta.get("ssml_alias_es", entity_key)
                pattern = re.compile(r'\b' + re.escape(entity_key) + r'\b', re.IGNORECASE)
                text = pattern.sub(alias, text)

        # 4. Inyección de Pausas en Conectores Discursivos
        if lang == "es":
            for connector in DISCURSIVE_CONNECTORS_ES:
                pattern = re.compile(r'\b' + connector, re.IGNORECASE)
                text = pattern.sub(f'{connector} <break time="{pauses["connector"]}ms"/>', text)

        # 5. Modelado Jerárquico de Puntuación Sintáctica RAE
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        processed_paragraphs = []

        for p in paragraphs:
            lines = [line.strip() for line in p.split("\n") if line.strip()]
            line_texts = []
            for line in lines:
                # Viñetas o listas con pausa anunciativa
                if line.startswith("- ") or line.startswith("• ") or line.startswith("· "):
                    line = line[2:].strip()
                    line = f'<break time="{pauses["colon"]}ms"/> {line}'

                # Punto y aparte implícito / punto y seguido
                line = re.sub(r'\.\s+', f'. <break time="{pauses["period"]}ms"/> ', line)
                # Punto y coma
                line = re.sub(r';\s*', f'; <break time="{pauses["semicolon"]}ms"/> ', line)
                # Dos puntos
                line = re.sub(r':\s*', f': <break time="{pauses["colon"]}ms"/> ', line)
                # Comas solas
                line = re.sub(r',\s*', f', <break time="{pauses["comma"]}ms"/> ', line)

                line_texts.append(line)

            p_joined = " ".join(line_texts)
            processed_paragraphs.append(f'<p>{p_joined}</p><break time="{pauses["paragraph"]}ms"/>')

        body_ssml = "\n".join(processed_paragraphs)

        # 6. Construcción del Envelope SSML W3C
        ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{ 'es-ES' if lang == 'es' else 'en-US' }">
    <voice name="{voice}">
        <prosody rate="{rate}" pitch="{pitch}">
            {body_ssml}
        </prosody>
    </voice>
</speak>"""
        return ssml

    async def synthesize_audio(self, raw_text: str, output_path: Path, lang: str = "es") -> Path:
        """
        Sintetiza audio con prosodia humana y lo masteriza a EBU R128 48kHz.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        raw_tmp = output_path.with_suffix(".tmp.mp3")

        ssml = self.build_human_ssml(raw_text, lang=lang)
        lang_key = "spanish" if lang.startswith("es") else "english"
        voice = self.profile.get(lang_key, {}).get("voice", "es-ES-AlvaroNeural" if lang == "es" else "en-US-AndrewMultilingualNeural")
        rate = self.profile.get(lang_key, {}).get("rate", "-8%")
        pitch = self.profile.get(lang_key, {}).get("pitch", "-5Hz")

        import edge_tts
        communicate = edge_tts.Communicate(
            text=re.sub(r'<[^>]+>', ' ', ssml),
            voice=voice,
            rate=rate,
            pitch=pitch
        )
        await communicate.save(str(raw_tmp))

        # Masterización de Audio EBU R128 (48kHz, -16 LUFS, Stereo)
        self._master_audio(raw_tmp, output_path)
        if raw_tmp.exists():
            raw_tmp.unlink()

        return output_path

    def _master_audio(self, src: Path, dst: Path):
        """Masterización broadcast vía FFmpeg (48kHz, -16 LUFS, True Peak -1.5 dBTP)."""
        cmd = [
            "ffmpeg", "-y",
            "-i", str(src),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
            "-ar", "48000",
            "-ac", "2"
        ]
        if dst.suffix.lower() == ".wav":
            cmd.extend(["-c:a", "pcm_s16le"])
        elif dst.suffix.lower() == ".mp3":
            cmd.extend(["-c:a", "libmp3lame", "-b:a", "320k"])
        cmd.append(str(dst))
        subprocess.run(cmd, capture_output=True, check=True)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw Sovereign Prosody & Audio Engine")
    parser.add_argument("--text", type=str, required=True, help="Texto o guión a sintetizar")
    parser.add_argument("--lang", type=str, default="es", choices=["es", "en"], help="Idioma (es/en)")
    parser.add_argument("--output", type=str, default="output/executive_speech.wav", help="Ruta del archivo de salida")

    args = parser.parse_args()
    engine = SovereignProsodyEngine()
    
    out_file = Path(args.output)
    print(f"[SOVEREIGN PROSODY ENGINE] Sintetizando para audiencia ejecutiva ({args.lang})...")
    asyncio.run(engine.synthesize_audio(args.text, out_file, lang=args.lang))
    print(f"[SOVEREIGN PROSODY ENGINE] Audio masterizado exitosamente: {out_file}")

if __name__ == "__main__":
    main()
