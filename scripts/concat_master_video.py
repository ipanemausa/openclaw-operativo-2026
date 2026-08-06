import sys
import os
import glob
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

lipsync_dir = Path(r"C:\openclaw\output\lipsync")
vids = sorted(lipsync_dir.rglob("*.mp4"))
print(f"Encontrados {len(vids)} fragmentos de video MP4.")

list_file = lipsync_dir / "concat_all.txt"
with open(list_file, "w", encoding="utf-8") as f:
    for v in vids:
        # Usar slashes para evitar problemas de escape en FFmpeg
        clean_path = str(v).replace("\\", "/")
        f.write(f"file '{clean_path}'\n")

out_video = Path(r"C:\openclaw\hb-jewelry\public\videos\guillermo_940f_master.mp4")
out_video.parent.mkdir(parents=True, exist_ok=True)

cmd = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", str(list_file),
    "-c", "copy",
    str(out_video)
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    size_mb = out_video.stat().st_size / (1024 * 1024)
    print(f"✅ VIDEO MAESTRO COMPLETADO: {out_video} ({size_mb:.2f} MB)")
else:
    print(f"❌ Error en FFmpeg concat:\n{res.stderr[-400:]}")
