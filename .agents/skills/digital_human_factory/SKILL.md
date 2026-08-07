---
name: digital_human_factory
description: Enterprise Autonomic Digital Human & Video Factory for OpenClaw v2026.7.1. Single-sentence intent routing, DaVinci Resolve Scripting API, 1080p real studio human video, Edge-TTS FM broadcast audio, and YouTube practice word-karaoke subtitles.
---

# 🎬 SKILL MAESTRA: Enterprise Digital Human & Video Factory (OpenClaw 2026.7.1)

## 📌 Visión de Ejecución Cero-Fricción ("Una Sola Frase y Ya")
Esta Skill sintetiza el motor de producción audiovisual y avatares digitales de OpenClaw. Permite que el sistema intercepte comandos breves en lenguaje natural (ejemplo: *"Crea un video educativo sobre la nueva colección"*) y ejecute autónomamente la producción, ecualización, subtitulado, ensamblado en DaVinci Resolve / FFmpeg y despliegue en la nube sin requerir intervención técnica del usuario.

---

## 🏛️ Arquitectura Integrada en 4 Capas de Producción

### 🖼️ CAPA 1: Fondo Gradiente 3D HSL & Depth Blur Studio
* **Iluminación Dinámica:** Bokeh 3D HSL con profundidad focal en resolución 1080p (1920x1080 para YouTube / 1080x1920 para TikTok/Reels).
* **Entorno de Marca:** Identidad corporativa HB Jewelry con badge flotante sin sobreposición de títulos.

### 👤 CAPA 2: Avatar Humano Real / PNG Transparente (Composición Cero-Bordes)
* **PNG Transparente (`avatar_transparent.png`):** Se fusiona directamente sobre el fondo espacial HSL con escalado Lanczos y sombra paralela de profundidad, garantizando **cero bordes de tarjeta ni cortes de imagen pegada**.
* **Avatar Completo con Fondo (`avatars/dorado.png`):** Se renderiza automáticamente a **100% Pantalla Completa (1920x1080 Cover Aspect Ratio)** con movimiento `zoompan` continuo, eliminando cualquier corte o franja lateral.
* **Fisiología Humana:** Parpadeo natural, respiración orgánica y postura real, eliminando totalmente el efecto de foto 2D flotante.
* **Inferencia Neural Complementaria:** Integración con **SadTalker 3DMM** / **DaVinci Resolve Scripting** para sincronización labial exacta cuando se requiere animación desde foto base.

### ✍️ CAPA 3: Teleprompter Bilingüe con Resaltado Palabra por Palabra (YouTube Practice Sync)
* **Cadencia Pausada (Zero Estrés):** Ritmo de lectura ajustado a **10-12 caracteres por segundo** con pausas respiratorias de 0.8s entre frases.
* **Resaltado Dinámico Karaoke:** La palabra activa hablada se ilumina en **Verde Neón (`#84cc16`)** sobre un fondo de alto contraste, las palabras pasadas se tornan en **Dorado HB (`#d4af6a`)** y las futuras se mantienen en blanco suave (`#e2e8f0`).
* **Traducción Automática en Tiempo Real:** Columna o recuadro inferior sincronizado en inglés para práctica de idiomas y alcance internacional.

### 🎙️ CAPA 4: Voz Real Ecualizada en Estudio FM Broadcast (48kHz Stereo)
* **Motor de Síntesis Neural:** Edge-TTS `es-MX-JorgeNeural` (Español) y `en-US-GuyNeural` (Inglés), ajustados a un tono amigable, pausado y de alta autoridad.
* **Cadena de Ecualización FM Broadcast (FFmpeg / DaVinci Fairlight):**
  - **Pasa-Altos:** 75 Hz (eliminación de ruidos subsónicos)
  - **Realce de Pecho:** 250 Hz (+3.0 dB de calidez vocal)
  - **Claridad de Inflexión:** 3.2 kHz (+3.5 dB de nitidez tímbrica)
  - **Compresión Vocal:** Ataque rápido 0.02s, decaimiento 0.2s
  - **Normalización de Loudness:** EBU R128 a **-14 LUFS** exactos.

---

## ⚡ Comandos de Ejecución Unificada

### 1. Ejecución Autónoma por Intención (Python Master Engine)
```bash
python scripts/generate_real_video_composite.py
```

### 2. Producción con Inferencia SadTalker 3D (Si se usa foto base)
```bash
python scripts/hb_video_factory.py --audio "speech.wav" --image "avatar_pro.png"
```

### 3. Pipeline de Despliegue en la Nube y Cierre DAG
```bash
powershell -ExecutionPolicy Bypass -File .\scripts\pipeline-cierre.ps1
```

---

## 🔍 Matriz de Diagnóstico y Calidad (Checklist de Validación)

| Aspecto | Estado Esperado | Verificación |
| :--- | :--- | :--- |
| **Movimiento Corporal** | Torso, postura, brazos y respiración real en estudio | ✅ Verificado (`showcase_human_loop.mp4`) |
| **Cadencia Vocal** | Pausada, amigable y convincente (Zero Estrés) | ✅ Verificado (-6% velocidad + 0.8s pausas) |
| **Audio Vocal** | Voz clara y cálida 48kHz sin silencios ni ruidos | ✅ Verificado (FM Broadcast EBU R128 -14 LUFS) |
| **Subtítulos** | Resaltado palabra por palabra (Verde/Dorado) | ✅ Verificado (Word Karaoke Sync) |
| **Despliegue CDN** | Hosting en vivo en Firebase + Backup Google Drive 5TB | ✅ Verificado (`pipeline-cierre.ps1`) |
