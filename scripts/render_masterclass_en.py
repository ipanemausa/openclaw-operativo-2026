"""
render_masterclass_en.py — Re-render 6 English blocks + concatenate ES & EN
Runs after block_6_es.mp4 is complete.
"""
import os, sys, asyncio, subprocess, shutil, logging
import edge_tts
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [EN-ENGINE] %(message)s")
logger = logging.getLogger("en_engine")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
OUT_DIR = PUBLIC_DIR / "videos" / "youtube_30min_masterclass"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SPACE_NEBULA_BG = PUBLIC_DIR / "cosmic_space_smooth.png"
AVATAR_IMAGE    = PUBLIC_DIR / "avatar_transparent.png"

MODULES = [
    {"id":1,"script_en":"Welcome to the HB Jewelry OpenClaw 2026 Executive Masterclass. In this strategic briefing we examine how to transform your enterprise sales operations by replacing recurring SaaS fees with on-premise autonomous agents."},
    {"id":2,"script_en":"Every luxury jewelry or professional service business rests on four pillars: Marketing, Sales, Logistics, and Finance. We connect a 768-dimensional RAG vector engine for exact data retrieval without AI hallucinations."},
    {"id":3,"script_en":"The largest bottleneck in B2B sales is delayed first response time. Our autonomous bot qualifies leads in under ten seconds, schedules meetings on your calendar, and executes catalog closes with zero per-message cost."},
    {"id":4,"script_en":"We guarantee complete technological sovereignty. All inventory data, client records, and financial history automatically back up in real-time via our DAG pipeline with rclone to 5 Terabyte Google Drive."},
    {"id":5,"script_en":"Through the B2B Juan Pe Advisor agent, we calculate revenue leakage from delayed responses and budget objections. We demonstrate how to elevate close rates from 12 percent to 22 percent in 30 days."},
    {"id":6,"script_en":"We conclude with the implementation roadmap to scale your jewelry or professional service business to an international standard without operational friction. Thank you for joining us in this OpenClaw 2026 analysis."},
]

def generate_ass(text, duration, out_ass):
    words = text.split()
    word_dur = int((duration * 1000) / max(len(words), 1) / 10)
    k_text = "".join([f"{{\\k{word_dur}}}{w} " for w in words])
    content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Center,Arial Black,58,&H00FFFFFF,&H0000C5FF,&H00000000,&H80000000,-1,0,0,0,105,100,2,0,1,4,3,5,300,300,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.50,0:{int(duration//60):02d}:{duration%60:05.2f},Center,,0,0,0,,,{{\\pos(960,880)}}{k_text.strip()}
"""
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(content)

async def render_en_blocks():
    logger.info("Rendering 6 EN blocks with Edge-TTS + FFmpeg...")
    block_files = []
    for mod in MODULES:
        mid = mod["id"]
        script = mod["script_en"]
        mp3 = OUT_DIR / f"mod_{mid}_en.mp3"
        wav = OUT_DIR / f"mod_{mid}_en.wav"
        ass = OUT_DIR / f"mod_{mid}_en.ass"
        out = OUT_DIR / f"block_{mid}_en.mp4"

        # TTS
        comm = edge_tts.Communicate(script, "en-US-GuyNeural", rate="-2%", pitch="+0Hz")
        await comm.save(str(mp3))

        # MP3 -> PCM WAV
        subprocess.run(["ffmpeg","-y","-i",str(mp3),"-ar","48000","-ac","2",str(wav)], capture_output=True)

        # Duration
        probe = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                                "-of","default=noprintwrappers=1:nokey=1",str(wav)], capture_output=True, text=True)
        try:
            dur = float(probe.stdout.strip())
        except:
            dur = 18.0

        total_frames = int(dur * 30) + 15
        generate_ass(script, dur, ass)
        ass_clean = str(ass).replace("\\","/").replace(":","\\:")

        filter_graph = (
            f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
            f"zoompan=z='min(zoom+0.0006\\,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1920x1080:fps=30[bg];"
            f"[1:v]scale=680:960:flags=lanczos,unsharp=5:5:1.2:5:5:1.2[avatar];"
            f"[bg][avatar]overlay=10:120[base];"
            f"[base]subtitles='{ass_clean}'[outv]"
        )

        cmd = [
            "ffmpeg","-y",
            "-loop","1","-t",f"{dur:.2f}","-i",str(SPACE_NEBULA_BG),
            "-loop","1","-t",f"{dur:.2f}","-i",str(AVATAR_IMAGE),
            "-i",str(wav),
            "-filter_complex",filter_graph,
            "-map","[outv]","-map","2:a",
            "-af","loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p",
            "-movflags","+faststart",
            "-c:a","aac","-b:a","256k","-ar","48000","-ac","2",
            str(out)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            mb = out.stat().st_size / 1024 / 1024
            logger.info(f"[OK] Block {mid} EN — {dur:.1f}s — {mb:.1f}MB")
            block_files.append(out)
        else:
            logger.error(f"[FAIL] Block {mid} EN: {res.stderr[-300:]}")

    return block_files

def concatenate(lang, block_files, out_name):
    concat_txt = OUT_DIR / f"concat_masterclass_{lang}.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for bf in block_files:
            f.write(f"file '{str(bf).replace(chr(92), '/')}'\n")
    out_mp4 = OUT_DIR / out_name
    pub_mp4 = PUBLIC_DIR / out_name
    r = subprocess.run([
        "ffmpeg","-y","-f","concat","-safe","0",
        "-i",str(concat_txt),"-c","copy",str(out_mp4)
    ], capture_output=True, text=True)
    if r.returncode == 0 and out_mp4.exists():
        shutil.copy(out_mp4, pub_mp4)
        mb = out_mp4.stat().st_size / 1024 / 1024
        logger.info(f"[DONE] {lang.upper()} masterclass: {pub_mp4} ({mb:.1f}MB)")
    else:
        logger.error(f"[FAIL] Concat {lang}: {r.stderr[-300:]}")

async def main():
    print("=" * 65)
    print("OPENCLAW MASTERCLASS RENDER — EN BLOCKS + FINAL CONCAT")
    print("=" * 65)

    # 1. Render EN blocks
    en_blocks = await render_en_blocks()

    # 2. Concatenate EN
    if len(en_blocks) == 6:
        concatenate("en", en_blocks, "youtube_30min_masterclass_en_1080p.mp4")

    # 3. Concatenate ES (bloques 1-6 ya existen)
    es_blocks = [OUT_DIR / f"block_{i}_es.mp4" for i in range(1, 7)]
    all_es_ready = all(f.exists() and f.stat().st_size > 100_000_000 for f in es_blocks)
    if all_es_ready:
        concatenate("es", es_blocks, "youtube_30min_masterclass_full_1080p.mp4")
        logger.info("[DONE] ES masterclass concatenated from existing blocks.")
    else:
        missing = [f.name for f in es_blocks if not f.exists() or f.stat().st_size < 100_000_000]
        logger.warning(f"ES blocks not ready yet: {missing}. Run after block_6_es.mp4 completes.")

    # 4. DISPARO AUTOMÁTICO AL PIPELINE MAESTRO (Firebase -> Git -> Rclone)
    print("=" * 65)
    print("🚀 RENDER FINALIZADO: DISPARANDO PIPELINE DE DEPLOY (FIREBASE+RCLONE)")
    print("=" * 65)
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", r"C:\Users\ipane\openclaw-operativo-2026\scripts\pipeline-cierre.ps1"], check=False)

if __name__ == "__main__":
    asyncio.run(main())
