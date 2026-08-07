import os
import sys
import asyncio
import subprocess
import shutil
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("====================================================================")
print(" 🎬 TEST RENDER: TELEPROMPTER DERECHO (x: 850px, y: 280px, Font 54pt)")
print("====================================================================")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
OUT_DIR = PUBLIC_DIR / "videos" / "youtube_masterclass"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MASTERCLASS_TOPICS = [
    {
        "id": 1,
        "title_es": "Módulo 1: Revolución IA Empresarial",
        "title_en": "Module 1: Enterprise AI Revolution",
        "phrases_es": [
            "Bienvenidos a este análisis estratégico.",
            "Examinaremos la infraestructura de IA B2B.",
            "Sustituimos licencias de pago mensual",
            "por agentes autónomos en tu servidor.",
            "Cero fricción operativa y máximo control."
        ],
        "phrases_en": [
            "Welcome to this executive briefing.",
            "We analyze B2B AI Infrastructure.",
            "Replacing legacy SaaS subscriptions",
            "with on-premise autonomous agents.",
            "Zero operational friction and total sovereignty."
        ]
    },
    {
        "id": 2,
        "title_es": "Módulo 2: Los 4 Pilares de la Empresa",
        "title_en": "Module 2: 4 Universal Enterprise Pillars",
        "phrases_es": [
            "Toda empresa sólida tiene 4 pilares:",
            "Marketing, Ventas, Logística y Finanzas.",
            "Conectamos un motor RAG de 768 dimensiones",
            "para responder con datos exactos",
            "sin inventar información."
        ],
        "phrases_en": [
            "Every enterprise rests on 4 pillars:",
            "Marketing, Sales, Logistics, and Finance.",
            "Connecting a 768-dimensional RAG vector engine",
            "for exact data retrieval",
            "without AI hallucinations."
        ]
    },
    {
        "id": 3,
        "title_es": "Módulo 3: Privacidad Meta y WhatsApp $0",
        "title_en": "Module 3: Meta Privacy & $0 WhatsApp",
        "phrases_es": [
            "Con la actualización reciente de Meta,",
            "tus clientes usan tu Alias empresarial.",
            "Protegemos el número telefónico privado",
            "mediante el token encriptado BSUID.",
            "Respuestas automáticas 24/7 sin costo por mensaje."
        ],
        "phrases_en": [
            "Leveraging Meta's newest update,",
            "clients connect via your business handle.",
            "We safeguard private phone numbers",
            "using encrypted BSUID tokens.",
            "24/7 automated responses at zero cost."
        ]
    },
    {
        "id": 4,
        "title_es": "Módulo 4: Fábrica Audiovisual Local 1080p",
        "title_en": "Module 4: Local 1080p AI Video Factory",
        "phrases_es": [
            "Procesamos video en micro-lotes de 15 frames",
            "asistidos por restauración facial GFPGAN.",
            "Generamos avatares HD con voz 48kHz",
            "sin pagar APIs en la nube",
            "ni costos por minuto de render."
        ],
        "phrases_en": [
            "Processing video in 15-frame micro-batches",
            "enhanced by GFPGAN facial restoration.",
            "Generating 1080p avatars with 48kHz audio",
            "bypassing cloud API fees",
            "and zero per-minute rendering costs."
        ]
    },
    {
        "id": 5,
        "title_es": "Módulo 5: Arquitectura MCP & Docker Toolkit",
        "title_en": "Module 5: MCP & Docker Toolkit Standard",
        "phrases_es": [
            "Con el estándar Model Context Protocol",
            "y Docker Desktop MCP Toolkit,",
            "nuestros agentes leen bases PostgreSQL",
            "y repositorios GitHub de forma segura",
            "dentro de contenedores aislados."
        ],
        "phrases_en": [
            "Using Model Context Protocol",
            "and Docker Desktop MCP Toolkit,",
            "agents query PostgreSQL databases",
            "and GitHub repositories securely",
            "within isolated container environments."
        ]
    },
    {
        "id": 6,
        "title_es": "Módulo 6: Plan de Acción v2.0-stable",
        "title_en": "Module 6: v2.0-stable Turnkey Roadmap",
        "phrases_es": [
            "El futuro es desplegar tu propio ecosistema.",
            "Toda la infraestructura está blindada",
            "bajo la versión v2.0-stable,",
            "respaldada en GitHub y Google Drive 5TB,",
            "lista para despliegue inmediato."
        ],
        "phrases_en": [
            "The future lies in proprietary AI ecosystems.",
            "Our complete architecture is locked",
            "under release tag v2.0-stable,",
            "backed up to GitHub and 5TB Google Drive,",
            "ready for turnkey enterprise deployment."
        ]
    }
]

import edge_tts

async def build_subtitle_and_audio(lang="es"):
    print(f"\n🎙️ Generando Audios y Subtítulos Frase por Frase ({lang.upper()})...")
    audio_files = []
    ass_events = []
    
    current_time_sec = 0.8
    
    for mod_idx, topic in enumerate(MASTERCLASS_TOPICS):
        phrases = topic["phrases_es"] if lang == "es" else topic["phrases_en"]
        voice_id = "es-MX-JorgeNeural" if lang == "es" else "en-US-GuyNeural"
        
        for p_idx, phrase in enumerate(phrases):
            aud_path = OUT_DIR / f"phrase_{lang}_{mod_idx+1}_{p_idx+1}.mp3"
            
            if not aud_path.exists():
                try:
                    comm = edge_tts.Communicate(phrase, voice_id, rate="-2%", pitch="+0Hz")
                    await comm.save(str(aud_path))
                except Exception:
                    pass
                    
            audio_files.append(aud_path)
            
            probe = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprintwrappers=1:nokey=1", str(aud_path)
            ], capture_output=True, text=True)
            try:
                dur_sec = float(probe.stdout.strip())
            except Exception:
                dur_sec = 2.5
                
            end_time_sec = current_time_sec + dur_sec
            
            m_start = f"{int(current_time_sec//3600)}:{int((current_time_sec%3600)//60):02d}:{current_time_sec%60:05.2f}"
            m_end = f"{int(end_time_sec//3600)}:{int((end_sec%3600)//60):02d}:{end_sec%60:05.2f}" if 'end_sec' in locals() else f"{int(end_time_sec//3600)}:{int((end_time_sec%3600)//60):02d}:{end_time_sec%60:05.2f}"
            
            words = phrase.split()
            word_dur_ms = int((dur_sec * 1000) / max(len(words), 1) / 10)
            karaoke_text = "".join([f"{{\\k{word_dur_ms}}}{w} " for w in words])
            
            # Posición en el cuadrante superior derecho (x: 820px, y: 320px)
            ass_events.append(f"Dialogue: 0,{m_start},{m_end},ShortPhraseStyle,,0,0,0,,{{\\pos(1280,360)}}{karaoke_text.strip()}")
            current_time_sec = end_time_sec + 0.3

    concat_list = OUT_DIR / f"concat_{lang}_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for a_file in audio_files:
            f.write(f"file '{str(a_file).replace('\\', '/')}'\n")
            
    full_audio = OUT_DIR / f"full_masterclass_{lang}_voice.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:a", "libmp3lame", "-b:a", "256k",
        str(full_audio)
    ], capture_output=True, text=True)
    
    # Escribir archivo .ass con pos(1280,360) para posición fija exacta en la MITAD DERECHA
    ass_file = OUT_DIR / f"masterclass_{lang}_short_phrases.ass"
    ass_header = f"""[Script Info]
Title: Short Phrase Teleprompter Text Right Side ({lang})
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ShortPhraseStyle,Montserrat,54,&H00FFFFFF,&H0000D7FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,3,2,5,100,100,100,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(ass_events))
        
    print(f"✅ Audio Continuo Ensamblado: {full_audio}")
    print(f"📝 Subtítulos Teleprompter Derecho (.ass): {ass_file}")
    
    return full_audio, ass_file

async def render_all_masters():
    cosmic_bg = PUBLIC_DIR / "cosmic_space_bg.png"
    avatar_img = PUBLIC_DIR / "avatar_transparent.png"
    if not avatar_img.exists():
        avatar_img = PUBLIC_DIR / "avatars" / "dorado.png"

    for lang in ["es", "en"]:
        full_audio, ass_file = await build_subtitle_and_audio(lang)
        
        out_mp4 = OUT_DIR / f"youtube_30min_masterclass_{'full' if lang=='es' else 'en'}_1080p.mp4"
        root_mp4 = PUBLIC_DIR / f"youtube_30min_masterclass_{'full' if lang=='es' else 'en'}_1080p.mp4"
        
        ass_clean = str(ass_file).replace("\\", "/").replace(":", "\\:")
        
        filter_graph = (
            f"[0:v]zoompan=z='min(zoom+0.0006,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30[bg_zoom];"
            f"[1:v]scale=720:980:flags=lanczos,unsharp=5:5:1.2:5:5:1.2[avatar_left];"
            f"[bg_zoom][avatar_left]overlay=60:60[base];"
            f"[base]subtitles='{ass_clean}'[outv]"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(cosmic_bg),
            "-loop", "1", "-i", str(avatar_img),
            "-i", str(full_audio),
            "-filter_complex", filter_graph,
            "-map", "[outv]",
            "-map", "2:a",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", "-shortest",
            "-c:a", "aac", "-b:a", "256k",
            str(out_mp4)
        ]
        
        print(f"⚙️ Compilando Video Maestro 4 Capas con Teleprompter Derecho {{\\pos(1280,360)}} ({lang.upper()})...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        if res.returncode == 0:
            shutil.copy(out_mp4, root_mp4)
            size_mb = out_mp4.stat().st_size / (1024 * 1024)
            print(f" ✅ VIDEO MAESTRO GENERADO EXITOSAMENTE ({lang.upper()}): {out_mp4} ({size_mb:.2f} MB)")
            print(f" ✅ COPIA EN RAÍZ PÚBLICA: {root_mp4}")
        else:
            print(f"❌ Error compilando video ({lang.upper()}):\n{res.stderr[-600:]}")

asyncio.run(render_all_masters())
print("\n🎬 ¡PROCESO CON TELEPROMPTER DERECHO EXACTO {pos(1280,360)} COMPLETADO!")
