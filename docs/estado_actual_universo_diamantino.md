# Estado actual – Universo Diamantino / OpenClaw – abril 2026

Este documento describe la foto actual (no la ideal) de mi ecosistema de proyectos: Diamantino Universe, DAVS, OpenClaw, TESO y el rol de Antigravity.

## 1. Repo núcleo operativo: OpenClaw

- Repo: `ipanemausa/openclaw-operativo-2026`.
- Propósito:
  - Ser la **memoria nuclear 2026** de decisiones, versiones y protocolos para mi ecosistema OpenClaw + Discord + Globy (sin depender de Antigravity).
- Documentos clave:
  - `docs/ocosto_loop_basico.md` → loop diario 0 costo y protocolo de apertura/cierre de sesión.
  - `docs/copilot_politica.md` → políticas de privacidad y uso de GitHub Copilot.
  - `docs/globy_chat_plan.md` → plan operativo/funcional de Globy sobre Discord.
- Regla de oro:
  - Ninguna decisión operativa de OpenClaw se considera “real” si no está reflejada en este repo y, cuando corresponda, en alguno de esos `.md`.

## 2. Rol de Antigravity (Anti)

- Anti es un **IDE / consola avanzada** conectada a mis repos Git (incluyendo `openclaw-operativo-2026`). [web:164][web:166][web:159]
- Anti **NO** es la fuente de verdad:
  - La verdad vive en Git (GitHub).
- Anti se usa para:
  - Edición asistida, refactors, generación de documentación.
  - Cambios importantes de código y diseño cuando necesito ayuda de modelos grandes.
- Modelos disponibles actualmente en Anti (aprox.):
  - Varios modelos Gemini (al menos 3 variantes). [web:164][web:166]
  - Claude Sonnet y Claude Opus (Anthropic). [web:164][web:166]
  - Un modelo “GPT OSS 120B” u otro modelo OSS grande. [web:164][web:166]
- Estrategia:
  - Usar estos modelos como “booster mental” para superar bloqueos (Ollama, Anthropic API, etc.). [web:163][web:160][web:77]
  - No depender de Anti como runtime permanente para OpenClaw.

## 3. Plan 0 costo para OpenClaw

- Regla central:
  - Toda la operación de OpenClaw debe ser posible sin planes de pago obligatorios. [web:163][web:160][web:77]
- Prioridades:
  - Modelos locales (Ollama u otros runtimes) y tiers gratuitos de APIs. [web:73][web:77][web:163]
  - APIs de pago (Anthropic, OpenAI, etc.) son recursos excepcionales, no el motor por defecto. [web:115][web:142][web:163]
- Consecuencia:
  - Claude Sonnet / Opus se consideran modelos estratégicos pero caros. [web:115][web:142]
  - Cualquier uso de Anthropic vía OpenClaw se debe documentar y limitar explícitamente.

## 4. Otros proyectos (estado de clarificación)

> Esta sección es un placeholder para aterrizar la realidad de cada proyecto. No implica que todos estén activos.

- **Diamantino Universe**
  - Estado actual: [pendiente de documentar].
  - Repos asociados: [listar cuando se identifiquen].
  - Rol esperado: marco conceptual y operativo de estudios/producción.

- **DAVS (estudio de video)**
  - Estado actual: [pendiente de revisión].
  - Repos/scripts actuales: [pendiente].
  - Nota: en el pasado se consideró “industrial”, pero debe re‑examinarse como si fuera un sistema ajeno para ver qué sigue vivo.

- **TESO**
  - Estado actual: [pendiente de documentar].
  - Repos asociados: [pendiente].

## 5. Decisión de foco (abril–mayo 2026)

- Proyecto activo principal:
  - OpenClaw operativo + Globy + Discord, bajo el plan 0 costo.
- Uso de Anti:
  - Solo como IDE y booster, no como dependencia de producción. [web:164][web:166][web:159]
- Proyectos en clarificación (no ejecución industrial):
  - Diamantino Universe.
  - DAVS.
  - TESO.
- Próximo paso:
  - A medida que tenga energía, ir rellenando la sección 4 con la realidad concreta de cada proyecto (repos, scripts, estado real), sin intentar industrializar todo a la vez.
