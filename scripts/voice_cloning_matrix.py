#!/usr/bin/env python3
"""
==============================================================================
🎭 OPENCLAW 2026 — VOICE CLONING MATRIX v1.0 (XTTS-v2 & GPU NVIDIA)
==============================================================================
Sistema integral de clonación de voz con XTTS-v2 para OpenClaw / HB App.
Modos:
  1. Interfaz Web Interactiva (Gradio): http://localhost:7860
  2. Motor Programático Autónomo para Pipelines de Video 1080p
==============================================================================
"""

import os
import sys
import torch
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
DEFAULT_OUTPUT_DIR = ROOT / "runtime" / "voice_outputs"
DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_REFERENCE_VOICE = ROOT / "audio" / "guillermo_voice_reference.wav"

try:
    from TTS.api import TTS
except ImportError:
    TTS = None

try:
    import gradio as gr
except ImportError:
    gr = None

class VoiceCloningMatrix:
    """Sistema de clonación de voz basado en XTTS v2 con aceleración GPU NVIDIA"""
    
    def __init__(self, output_dir: Path = DEFAULT_OUTPUT_DIR):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        self.tts = None
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n[INIT] 🔧 CONFIGURACION VOICE CLONING MATRIX:")
        print(f"   Dispositivo: {self.device.upper()}")
        if self.device == "cuda":
            print(f"   GPU Detectada: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        else:
            print(f"   [AVISO] GPU no disponible. Ejecutando en CPU.")
        print(f"   Modelo Base: XTTS-v2 Multilingual (17 Idiomas)")
        print(f"   Directorio de Salida: {self.output_dir}")
        
    def cargar_modelo(self) -> bool:
        """Carga el modelo XTTS v2 en memoria/VRAM"""
        if TTS is None:
            print("[ERROR] 'coqui-tts' no esta instalado. Instala con: pip install coqui-tts")
            return False

        if self.tts is None:
            print("\n[CARGA] 📡 Inicializando pesos neuronales de XTTS-v2 en VRAM...")
            try:
                self.tts = TTS(
                    model_name=self.model_name,
                    gpu=True if self.device == "cuda" else False,
                    progress_bar=False
                )
                print("[OK] ✅ Modelo XTTS-v2 cargado exitosamente en VRAM.")
                return True
            except Exception as e:
                print(f"[ERROR] ❌ Error al cargar modelo: {e}")
                return False
        return True
    
    def clonar_voz(self, texto: str, audio_referencia: str, idioma: str = "es", 
                   aplicar_dsp_48k: bool = True) -> str:
        """
        Clona la voz de Guillermo y genera audio con acabado Broadcast.
        
        Args:
            texto: Texto a sintetizar
            audio_referencia: Ruta a archivo WAV de referencia (10-30 seg limpios)
            idioma: Codigo de idioma ('es', 'en', 'fr', 'de', 'it', 'pt', etc.)
            aplicar_dsp_48k: Si True, aplica cadena FFmpeg (48kHz, -16 LUFS EBU R128)
        
        Returns:
            Ruta absoluta al archivo de audio masterizado generado
        """
        if not self.cargar_modelo():
            return None
        
        if not texto.strip():
            print("[WARN] ⚠️ Texto vacio.")
            return None
        
        if not audio_referencia or not os.path.exists(audio_referencia):
            print(f"[WARN] ⚠️ Archivo de referencia no encontrado: {audio_referencia}")
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_wav = self.output_dir / f"cloned_{idioma}_{timestamp}_raw.wav"
            master_aac = self.output_dir / f"cloned_{idioma}_{timestamp}_master_48k.aac"
            
            print(f"\n[SINTESIS] 🎙️ Inferencia XTTS-v2...")
            print(f"   Idioma: {idioma.upper()}")
            print(f"   Referencia: {audio_referencia}")
            print(f"   Texto: '{texto[:80]}...'")
            
            # Inferencia Zero-Shot
            self.tts.tts_to_file(
                text=texto,
                speaker_wav=audio_referencia,
                language=idioma,
                file_path=str(raw_wav)
            )
            
            if not aplicar_dsp_48k:
                return str(raw_wav)

            # Masterizacion DSP Broadcast OpenClaw (48kHz, -16 LUFS EBU R128)
            eq_chain = (
                "highpass=f=80,"
                "equalizer=f=220:t=q:w=1.2:g=2.5,"
                "equalizer=f=3500:t=q:w=1.0:g=3.0,"
                "compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-2:soft-knee=6,"
                "loudnorm=I=-16:TP=-1.5:LRA=11:dual_mono=false"
            )
            cmd = [
                "ffmpeg", "-y", "-i", str(raw_wav),
                "-af", eq_chain,
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                str(master_aac)
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            print(f"   [OK] ✅ Master Broadcast 48kHz generado: {master_aac}")
            return str(master_aac)
            
        except Exception as e:
            print(f"[ERROR] ❌ Error en sintesis: {e}")
            return None
    
    def listar_idiomas(self) -> dict:
        return {
            "es": "Español",
            "en": "English",
            "fr": "Français",
            "de": "Deutsch",
            "it": "Italiano",
            "pt": "Português",
            "pl": "Polski",
            "tr": "Türkçe",
            "ru": "Русский",
            "nl": "Nederlands",
            "cs": "Čeština",
            "ar": "العربية",
            "zh-cn": "中文",
            "ja": "日本語",
            "hu": "Magyar",
            "ko": "한국어",
            "hi": "हिन्दी"
        }
    
    def obtener_info_sistema(self) -> str:
        info = f"🖥️ SISTEMA OPENCLAW VOICE CLONING MATRIX\n"
        info += f"───────────────────────────────────────\n"
        info += f"Dispositivo: {self.device.upper()}\n"
        info += f"PyTorch: {torch.__version__}\n"
        if self.device == "cuda":
            info += f"GPU: {torch.cuda.get_device_name(0)}\n"
            info += f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB\n"
            info += f"CUDA: {torch.version.cuda}\n"
        info += f"Modelo: XTTS-v2 Multilingual (Zero-Shot)\n"
        info += f"Calibracion: R^768 / -16 LUFS Broadcast (48kHz)\n"
        info += f"Estado: Listo para Produccion Audiovisual\n"
        return info

def crear_interfaz_gradio():
    """Crea la interfaz Web interactiva de Gradio"""
    if gr is None:
        print("[ERROR] 'gradio' no esta instalado. Instala con: pip install gradio")
        return None

    matrix = VoiceCloningMatrix()
    matrix.cargar_modelo()
    
    idiomas = matrix.listar_idiomas()
    idiomas_list = [f"{code} - {name}" for code, name in idiomas.items()]
    
    def procesar_clonacion(audio_ref, texto, idioma_selec):
        if audio_ref is None:
            return None, "❌ Sube un archivo de audio de referencia (WAV de 10-30 seg)"
        
        codigo_idioma = idioma_selec.split(" - ")[0]
        resultado = matrix.clonar_voz(
            texto=texto,
            audio_referencia=audio_ref,
            idioma=codigo_idioma,
            aplicar_dsp_48k=True
        )
        
        if resultado:
            return resultado, "✅ Audio masterizado 48kHz generado exitosamente con tu voz real"
        else:
            return None, "❌ Error durante el proceso de clonación"
    
    with gr.Blocks(title="OpenClaw Voice Cloning Matrix", theme=gr.themes.Soft()) as interfaz:
        gr.Markdown("""
        # 🎭 OPENCLAW 2026 — VOICE CLONING MATRIX v1.0
        ### Estudio Autónomo de Clonación de Voz Real (XTTS-v2 en GPU NVIDIA)
        
        ⚡ **Capacidades:**
        - Clonación Zero-Shot con solo **10 a 30 segundos** de audio de referencia.
        - Soporte para **17 idiomas** con preservación de identidad vocal (Cross-Lingual).
        - Salida masterizada en **48kHz Estéreo (-16 LUFS EBU R128)** para videos 1080p.
        """)
        
        with gr.Group():
            info_text = gr.Textbox(value=matrix.obtener_info_sistema(), label="📊 Estado del Hardware y Modelo", lines=7, interactive=False)
        
        with gr.Row():
            with gr.Column():
                audio_input = gr.Audio(type="filepath", label="🎙️ Audio de Referencia de Guillermo (WAV 10-30s)")
                idioma_input = gr.Dropdown(choices=idiomas_list, value="es - Español", label="🌍 Idioma de Salida")
                texto_input = gr.Textbox(label="📝 Guion / Texto a Sintetizar", placeholder="Escribe el texto de la masterclass...", lines=5)
                generar_btn = gr.Button("🚀 CLONAR VOZ & GENERAR MASTER BROADCAST", variant="primary", size="lg")
            
            with gr.Column():
                audio_output = gr.Audio(label="🎵 Audio Masterizado (48kHz, -16 LUFS)", type="filepath")
                status_output = gr.Textbox(label="Estado del Pipeline", interactive=False, lines=3)
        
        generar_btn.click(
            fn=procesar_clonacion,
            inputs=[audio_input, texto_input, idioma_input],
            outputs=[audio_output, status_output]
        )
        
    return interfaz

if __name__ == "__main__":
    print("=" * 70)
    print("  OPENCLAW 2026: VOICE CLONING MATRIX (XTTS-v2)")
    print("=" * 70)
    
    if gr is not None:
        app = crear_interfaz_gradio()
        if app:
            print("\n🚀 Servidor Gradio listo en: http://localhost:7860")
            app.launch(server_name="0.0.0.0", server_port=7860, share=False)
    else:
        print("[INFO] Modo Headless (sin Gradio). Usa la clase VoiceCloningMatrix en tus scripts.")
