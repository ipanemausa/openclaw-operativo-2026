# 🎭 PASARELA DE AVATARES HB.OS — MASTER PACK 2026
**Proyecto:** HB Jewelry & HB.OS Sovereign AI Operating System  
**Identidad Maestro:** Guillermo Hoyos  
**CDN Base Producción:** `https://hb-jewelry-cloud-2026-2dff9.web.app/`  
**Fecha:** 2026-08-29  

---

## 1. 🔍 AUDITORÍA Y ESTADO DE LA APP

| Pregunta / Verificación | Respuesta Técnica Verificada |
|---|---|
| **¿Qué muestra la página principal?** | Muestra el **Dashboard Corporativo HB.OS** directamente (`openclaw-ui`), con métricas en tiempo real, monitoreo de agentes, gráficos de rendimiento y panel de control central. |
| **¿Hay pantalla de login?** | No hay pantalla de bloqueo de login activa por defecto; la sesión entra directo al panel operativo. |
| **¿Quiénes son los avatares?** | **100% de la pasarela actual corresponde a Guillermo Hoyos** (Avatar Oficial / Fundador). **Alejandro Torres no está en la base de datos** de esta versión. |
| **¿Las imágenes son personas reales o logotipos?** | Son **fotografías reales en alta definición de Guillermo Hoyos**, procesadas con transparencia alfa pura y logotipo oficial `HB.OS` bordado en la camiseta. |

---

## 2. 🌐 URLs PÚBLICAS DIRECTAS PARA HEYGEN / D-ID / DEEPSEEK

Puedes copiar y pegar estas URLs directamente en el navegador, en **[HeyGen](https://app.heygen.com/) (Avatar → Upload)** o compartirlas a **DeepSeek**:

| ID Avatar | Nombre / Pose | URL Pública CDN (Firebase Hosting) |
|---|---|---|
| `avatar_master` | **Guillermo — Master Pro HD** | `https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/avatar_pro.png` |
| `avatar_transp` | **Guillermo — Transparente Puro** | `https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/avatar_transparent.png` |
| `studio_mic` | **Guillermo — De Pie con Micrófono Boom** | `https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/studio_mic.png` |
| `desk_mic` | **Guillermo — Sentado en Escritorio con Micrófono** | `https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/desk_mic.png` |
| `azul` | **Guillermo — Polo Azul Marino** | `https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/azul.png` |
| `blanco` | **Guillermo — Polo Blanco Premium** | `https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/blanco.png` |
| `verde` | **Guillermo — Polo Verde Esmeralda (Thumbs Up)** | `https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/verde.png` |
| `rojo` | **Guillermo — Polo Rojo Dinámico (Señalando)** | `https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/rojo.png` |
| `dorado` | **Guillermo — Polo Dorado / Negro VIP** | `https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/dorado.png` |
| `frame_gold` | **Marco Holográfico / Gold Badge** | `https://hb-jewelry-cloud-2026-2dff9.web.app/avatar_frame.png` |

---

## 3. 💻 RUTAS LOCALES EN TU PC (DISCO DURO)

Para subida manual directa desde tu explorador de archivos:

```text
C:\Users\ipane\openclaw-operativo-2026\frontend\public\avatars\avatar_pro.png
C:\Users\ipane\openclaw-operativo-2026\frontend\public\avatars\avatar_transparent.png
C:\Users\ipane\openclaw-operativo-2026\frontend\public\avatars\studio_mic.png
C:\Users\ipane\openclaw-operativo-2026\frontend\public\avatars\desk_mic.png
C:\Users\ipane\openclaw-operativo-2026\frontend\public\avatars\azul.png
C:\Users\ipane\openclaw-operativo-2026\frontend\public\avatars\blanco.png
C:\Users\ipane\openclaw-operativo-2026\frontend\public\avatars\verde.png
C:\Users\ipane\openclaw-operativo-2026\frontend\public\avatars\rojo.png
C:\Users\ipane\openclaw-operativo-2026\frontend\public\avatars\dorado.png
```

---

## 4. 📦 PAYLOAD JSON COMPLETO (COMPATIBLE CON DEEPSEEK)

```json
{
  "system": "HB.OS (OPERATING SYSTEM) · SOVEREIGN AI",
  "version": "2026.7.1",
  "cdn_root": "https://hb-jewelry-cloud-2026-2dff9.web.app/",
  "primary_subject": {
    "name": "Guillermo Hoyos",
    "role": "Founder & Executive Presenter",
    "biometric_voice_profile": "guillermo_voice_studio_master_48k",
    "voice_standard": "48kHz Stereo EBU R128 (-16 LUFS)"
  },
  "avatars": [
    {
      "id": "avatar_pro",
      "label": "Guillermo — Master Pro HD",
      "pose": "Full body standing, corporate pose",
      "apparel": "Black polo with embroidered Gold HB.OS emblem, blue jeans",
      "url": "https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/avatar_pro.png",
      "local_path": "frontend/public/avatars/avatar_pro.png"
    },
    {
      "id": "avatar_transparent",
      "label": "Guillermo — Transparente Broadcast",
      "pose": "Full body front, 100% pure transparent alpha",
      "apparel": "Black polo with embroidered Gold HB.OS emblem",
      "url": "https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/avatar_transparent.png",
      "local_path": "frontend/public/avatars/avatar_transparent.png"
    },
    {
      "id": "studio_mic",
      "label": "Guillermo — Estudio Boom Mic",
      "pose": "Standing with articulating boom microphone",
      "apparel": "Black polo with embroidered Gold HB.OS emblem, blue jeans, white sneakers",
      "url": "https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/studio_mic.png",
      "local_path": "frontend/public/avatars/studio_mic.png"
    },
    {
      "id": "desk_mic",
      "label": "Guillermo — Mesa Ejecutiva Podcast",
      "pose": "Seated at tech desk with studio mic",
      "apparel": "Black polo with embroidered Gold HB.OS emblem",
      "url": "https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/desk_mic.png",
      "local_path": "frontend/public/avatars/desk_mic.png"
    },
    {
      "id": "azul",
      "label": "Guillermo — Azul Marino",
      "pose": "Explanatory relaxed pose",
      "apparel": "Navy blue polo with embroidered Gold HB.OS emblem",
      "url": "https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/azul.png",
      "local_path": "frontend/public/avatars/azul.png"
    },
    {
      "id": "blanco",
      "label": "Guillermo — Blanco Premium",
      "pose": "Hands in pockets, confident posture",
      "apparel": "White premium polo with embroidered Gold HB.OS emblem",
      "url": "https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/blanco.png",
      "local_path": "frontend/public/avatars/blanco.png"
    },
    {
      "id": "verde",
      "label": "Guillermo — Verde Esmeralda",
      "pose": "Thumbs-up positive reinforcement pose",
      "apparel": "Emerald green polo with embroidered Gold HB.OS emblem",
      "url": "https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/verde.png",
      "local_path": "frontend/public/avatars/verde.png"
    },
    {
      "id": "rojo",
      "label": "Guillermo — Rojo Dinámico",
      "pose": "Pointing forward engaging audience",
      "apparel": "Dynamic red polo with embroidered Gold HB.OS emblem",
      "url": "https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/rojo.png",
      "local_path": "frontend/public/avatars/rojo.png"
    },
    {
      "id": "dorado",
      "label": "Guillermo — VIP Gold",
      "pose": "Welcoming open-arms posture",
      "apparel": "VIP Gold/Black polo with oversized Gold HB.OS emblem",
      "url": "https://hb-jewelry-cloud-2026-2dff9.web.app/avatars/dorado.png",
      "local_path": "frontend/public/avatars/dorado.png"
    }
  ]
}
```
