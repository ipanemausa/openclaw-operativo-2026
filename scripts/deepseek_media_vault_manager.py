"""
==============================================================================
DEEPSEEK HARNESS — VEHÍCULO MAESTRO DE ARCHIVO & GESTIÓN MULTIMEDIA (V4/V5)
==============================================================================
- Regla Inmutable: Cero mezcla de frames o proyectos.
- Cada video posee su propio Namespace Aislado en runtime/media_vault/<project_slug>/
- Cada proyecto registra su manifiesto estructurado manifest.json
- Limpieza previa obligatoria de temporales por proyecto antes del renderizado.
==============================================================================
"""

import os
import sys
import shutil
import json
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
VAULT_DIR = ROOT / "runtime" / "media_vault"
VAULT_DIR.mkdir(parents=True, exist_ok=True)

class DeepSeekMediaVault:
    def __init__(self, project_slug: str, title: str, category: str = "Masterclass"):
        self.project_slug = project_slug
        self.title = title
        self.category = category
        self.project_dir = VAULT_DIR / project_slug
        self.frames_dir = self.project_dir / "frames"
        self.audio_dir = self.project_dir / "audio"
        self.output_dir = self.project_dir / "output"
        self.manifest_path = self.project_dir / "manifest.json"

    def initialize_clean_workspace(self):
        """Limpia de forma aislada y rigurosa el workspace del proyecto sin afectar otros videos."""
        if self.project_dir.exists():
            print(f"[VAULT] Limpiando workspace previo del proyecto: {self.project_slug}")
            try:
                shutil.rmtree(self.project_dir, ignore_errors=True)
            except Exception as e:
                print(f"[VAULT] Aviso en limpieza previa: {e}")
        
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.frames_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"[VAULT] Workspace aislado listo en: {self.project_dir}")

    def save_manifest(self, video_filename: str, duration_sec: float, frames_count: int, modules: list):
        """Registra el manifiesto JSON inmutable del proyecto."""
        manifest_data = {
            "project_slug": self.project_slug,
            "title": self.title,
            "category": self.category,
            "created_at": datetime.now().isoformat(),
            "video_path": str(self.output_dir / video_filename),
            "duration_sec": duration_sec,
            "frames_count": frames_count,
            "modules": modules,
            "status": "COMPLETED",
            "provider": "DeepSeek Harness Media Engine V5"
        }
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2, ensure_ascii=False)
        print(f"[VAULT] Manifiesto guardado en: {self.manifest_path}")

    def launch_video(self, video_filename: str):
        """Abre el video del proyecto verificado mediante el reproductor nativo del sistema."""
        video_path = self.output_dir / video_filename
        if not video_path.exists():
            print(f"[ERROR] El archivo de video no existe: {video_path}")
            return False
        
        print(f"[VAULT] Abriendo video del proyecto: {self.title}")
        print(f"        Ruta: {video_path}")
        
        if sys.platform == "win32":
            subprocess.run(["cmd", "/c", "start", "", str(video_path)], check=True)
        return True

if __name__ == "__main__":
    print("[VAULT] DeepSeek Media Vault Engine operativo.")
