# PROTOCOLO DE BLINDAJE PERMANENTE — OpenClaw Cloud 2026

## Estado estable verificado
- **Tag de referencia:** `v2.0-stable`
- **Commit:** `49c8425` — Layout + Header + Sidebar agrupado + estilos unificados
- **Build:** Vite — 198 modulos compilados sin errores

---

## Archivos CRITICOS — PROHIBIDO modificar sin autorizacion explicita del usuario

Los siguientes archivos estan BLINDADOS. Cualquier agente debe tratarlos como de solo lectura
a menos que el usuario diga explicitamente "autorizo cambio en [archivo]":

- frontend/src/components/Layout/Layout.jsx        [BLINDADO]
- frontend/src/components/Header/Header.jsx        [BLINDADO]
- frontend/src/components/Sidebar/Sidebar.jsx      [BLINDADO]
- frontend/src/styles/layout.css                   [BLINDADO]
- frontend/src/styles/sidebar.css                  [BLINDADO]

---

## Reglas de conducta para TODOS los agentes

1. NUNCA sobrescribir archivos criticos con codigo experimental o generico.
2. SIEMPRE verificar que "npm run build" pase antes de cualquier commit a archivos criticos.
3. Si un archivo critico se rompe -> restaurar inmediatamente con:
      git checkout v2.0-stable -- <archivo>
4. Codigo experimental va en ramas temporales (feature/*, exp/*), NUNCA directo a main.
5. Si aparecen archivos basura (.txt con codigo, archivos sin extension) -> eliminar y agregar a .gitignore.
6. Si hay duda entre modificar y proteger -> SIEMPRE PROTEGER.
7. COMUNICACIÓN DIRECTA Y PRAGMÁTICA: Cero elogios innecesarios, adjetivos inflados o rellenos verbales. Foco 100% en ingeniería, producto de alto valor B2B y mejora continua diaria.

---

## Protocolo de recuperacion de emergencia

Si el sidebar, header o layout aparecen rotos o vacios, ejecutar en PowerShell:

  git checkout v2.0-stable -- frontend/src/components/Layout/Layout.jsx
  git checkout v2.0-stable -- frontend/src/components/Header/Header.jsx
  git checkout v2.0-stable -- frontend/src/components/Sidebar/Sidebar.jsx
  git checkout v2.0-stable -- frontend/src/styles/layout.css
  git checkout v2.0-stable -- frontend/src/styles/sidebar.css
  cd frontend && npm run build

---

## Arquitectura del frontend (NO cambiar sin protocolo)

App.jsx
  Layout (activeSection, onSelect)
    Header        -> .app-header, .header-brand, .status-dot
    Sidebar       -> 4 grupos: Principal / Operaciones / Marketing & Analytics / Sistema
    <main>        -> contenido por seccion (Dashboard, Chat, Ventas, etc.)

CSS responsable:
  - Layout:  frontend/src/styles/layout.css
  - Sidebar: frontend/src/styles/sidebar.css

---

## Verificacion diaria de integridad

  cd C:\Users\ipane\openclaw-cloud-2026\frontend
  npm run build
  # Debe decir: "built in Xms" sin errores

---

REGLA DE ORO: v2.0-stable es el estado maestro. En caso de duda -> PROTEGER.

---

## Protocolo Automático de Cierre y Respaldo (PIPELINE DAG)

Siempre que el usuario solicite un cierre, respaldo, o diga frases como "hacer backup", "commit y push", "sync drive", "cierre de jornada" o similar:

1. Ejecutar inmediatamente el script maestro de cierre:
   `powershell -ExecutionPolicy Bypass -File .\scripts\pipeline-cierre.ps1`
2. Este script ejecuta automáticamente:
   - Git `add .`, `commit`, `push` a GitHub (`origin/main`).
   - Sincronización en la nube vía `rclone` hacia Google Drive (`drive:HBJewelry` y `drive:openclaw-cloud-2026-backup`).
   - Registro de estado en `ANTIGRAVITY_WORK_LOG.txt`.
3. Confirmar la ejecución al usuario con un resumen conciso de lo respaldado.

---

## Protocolo Permanente de Producción Audiovisual Resiliente & Gobernanza Lingüística RAE / Oxford

Para producción autónoma diaria de video sin intervención ni ajustes manuales de configuración:

1. **Gobernanza Lingüística & Ortográfica Inmutable:**
   - **Español (Estándar RAE):** Acentuación gráfica estricta, acápites claros, puntuación prosódica y preservación de nombres institucionales (`MinTIC`, `Ruta N`, `Universidad EAFIT`).
   - **Inglés (Oxford / Chicago Manual):** Nombres de modelos y personas en inglés nativo exacto (`Jensen Huang`, `Dario Amodei`, `GPT-4o`, `Claude 3.5 Sonnet`, `DeepSeek-R1`, `Qwen 2.5`, `GLM-4`, `Hunyuan`, `Kimi`, `Yi-Lightning`, `SenseNova`, `Hailuo AI`).
   - **Estructura Visual:** Formato **Breakdown Jerárquico con Sangría** de 24px para sub-modelos. PROHIBIDO párrafos apelmazados con listas separadas por comas.
2. **Normas de Calidad & Paridad Inmutables:**
   - **Avatar:** Silueta de Guillermo HD en PNG transparente con logotipo oficial `HB.OS (SOVEREIGN AI)` estampado directamente en los píxeles de la tela (cero cajas ni capas flotantes desfasadas).
   - **Fondo:** Cinemática cósmica continua con 180 partículas de paralaje suave y barra superior flotante minimalista.
   - **Audio:** Voz estéreo 48kHz (-16 LUFS EBU R128), cadencia pausada (-10% rate) con respiración natural (250ms a 500ms entre acápites).
   - **Streaming:** FastStart MP4 (`-movflags +faststart`) activado para 0 buffer en navegadores.
   - **Paridad Bilingüe:** 100% paridad 1 a 1 de duración exacta entre Español e Inglés.

---

## Regla de Orden de Deploy — OBLIGATORIO PARA TODO PIPELINE

TODO pipeline, script o tarea que implique deploy DEBE respetar este orden sin excepcion:

  1. BUILD local (npm run build / vite build)
  2. FIREBASE HOSTING deploy (npx firebase deploy --only hosting)
  3. GIT commit + push a GitHub (origin/main)
  4. RCLONE backup a Google Drive 5TB

Firebase SIEMPRE antes que rclone. Si Firebase falla, NO se ejecuta rclone.
Si el agente invierte este orden -> corregir inmediatamente.

---

## Protocolo de API Keys — Fuente Unica de Verdad

- Archivo maestro: C:\Users\ipane\.openclaw-master.env  (FUERA de todo repo git)
- Para actualizar una key: editar SOLO el archivo maestro.
- Para propagar a todos los proyectos: ejecutar el script de sync:
    powershell -ExecutionPolicy Bypass -File .\scripts\sync-master-env.ps1
- Despues del sync: docker compose up -d --force-recreate (para que los contenedores tomen los cambios)
- NUNCA hardcodear API keys en codigo ni en archivos commiteados.
- NUNCA duplicar keys en distintos .env de proyectos — siempre vienen del master via sync.

---

## Regla de Verdad Absoluta Post-Deploy (Anti-Humo)

Todo despliegue (deploy) que involucre GitHub Actions CI **NO se considera exitoso** solo porque los tests locales pasen o el build local termine sin errores. 

**REGLA OBLIGATORIA:** 
Un (1) DAG después de ejecutar el pipeline de deploy, el agente DEBE:
1. Requerir la verificación del estado remoto (consultar API de GitHub Actions o pedir confirmación al usuario de que no llegaron emails de fallo).
2. Asumir que el resultado local es "humo" hasta que el servidor de integración continua remoto (GitHub) devuelva luz verde definitiva.

---

---

## Protocolo de Activación Rápida: [OPENCLAW-CORE-MATRIX]

Cuando el usuario inicie una sesión con el comando:
`"Carga la matriz técnica completa bajo el estándar [OPENCLAW-CORE-MATRIX] y pasemos a trabajar en: [tarea]"`

El agente debe:
1. Validar e instanciar las 5 fases de [OPENCLAW_CORE_MATRIX_2026.md](file:///c:/Users/ipane/openclaw-operativo-2026/OPENCLAW_CORE_MATRIX_2026.md):
   - **Fase 1 (Sovereign AI):** Modelos Open-Weight, $0 licencias, independencia de APIs cerradas.
   - **Fase 2 (Gobernanza Vectorial):** Espacio $\mathbb{R}^{768}$, embeddings `BAAI/bge-m3`, filtro $S \ge 0.82$, esquemas JSON deterministas.
   - **Fase 3 (Orquestación DAG):** Grafos CPM, colas asíncronas, persistencia Git + Rclone 5TB.
   - **Fase 4 (Sandboxes & Harnesses):** Docker 7/7 microservicios, aislamiento y ejecución de tools controlada.
   - **Fase 5 (Multimodalidad & Video):** 1080p FastStart, Edge-TTS 48kHz (-16 LUFS EBU R128), YouTube/Firebase CDN.
2. Ejecutar inmediatamente la tarea solicitada bajo este marco sin requerir preámbulos teóricos adicionales.

---

## Blindaje Permanente de Identidad Vocal & Branding Oficial HB.OS

1. **PROHIBICIÓN ESTRICTA DE FALLBACK SILENCIOSO:**
   - Queda TERMINANTEMENTE PROHIBIDO sustituir en silencio la voz real o el clon de voz de Guillermo por voces sintéticas genéricas (Microsoft, Edge-TTS genérico, etc.) sin avisar explícitamente.
   - Si se requiere que el clon de Guillermo lea un guion nuevo y el motor de clonación neural (ElevenLabs / Cloud GPU XTTS-v2 / CosyVoice) no está enlazado, el agente DEBE detenerse y requerir la clave o acción necesaria. NUNCA reportar éxito falso.

2. **BRANDING OFICIAL INMUTABLE:**
   - En toda producción de video, masterclass, header, teleprompter y narración, el nombre oficial del sistema es:
     `HB. OS Operation system`  (o  `HB.OS (OPERATING SYSTEM) · SOVEREIGN AI`)
   - Queda PROHIBIDO usar "OpenClaw 2026" como marca en pantalla o locución de masterclasses.

3. **CALIDAD VISUAL HD CRISTALINA:**
   - Las capturas B-Roll y avatares transparentes deben escalarse con filtro `Lanczos` de alta definición (`1040x585` en 1080p) con marco bioluminiscente, garantizando cero pixelación ni compresión degradante.


