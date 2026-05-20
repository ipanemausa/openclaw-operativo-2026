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
  - Ninguna decisión operativa de OpenClaw se considera "real" si no está reflejada en este repo y, cuando corresponda, en alguno de esos `.md`.

## 2. Rol de Antigravity (Anti)

- Anti es un **IDE / consola avanzada** conectada a mis repos Git (incluyendo `openclaw-operativo-2026`).
- Anti **NO** es la fuente de verdad:
  - La verdad vive en Git (GitHub).
- Anti se usa para:
  - Edición asistida, refactors, generación de documentación.
  - Cambios importantes de código y diseño cuando necesito ayuda de modelos grandes.
- Modelos disponibles actualmente en Anti (aprox.):
  - Varios modelos Gemini (al menos 3 variantes).
  - Claude Sonnet y Claude Opus (Anthropic).
  - Un modelo "GPT OSS 120B" u otro modelo OSS grande.
- Estrategia:
  - Usar estos modelos como "booster mental" para superar bloqueos (Ollama, Anthropic API, etc.).
  - No depender de Anti como runtime permanente para OpenClaw.

## 3. Plan 0 costo para OpenClaw

- Regla central:
  - Toda la operación de OpenClaw debe ser posible sin planes de pago obligatorios.
- Prioridades:
  - Modelos locales (Ollama u otros runtimes) y tiers gratuitos de APIs.
  - APIs de pago (Anthropic, OpenAI, etc.) son recursos excepcionales, no el motor por defecto.
- Consecuencia:
  - Claude Sonnet / Opus se consideran modelos estratégicos pero caros.
  - Cualquier uso de Anthropic vía OpenClaw se debe documentar y limitar explícitamente.

### Configuración ganadora actual (25 abril 2026)

**Stack operativo hoy**:
- **OpenClaw**: versión 2026.5.19 (actualizada desde 2026.4.24)
  - DeepSeek V4 Flash como modelo default en onboarding ($0.14 input / $0.28 output por 1M tokens)
  - Google Meet bundled, WebRTC para voz en tiempo real
  - Generación de imágenes ampliada (OpenAI, OpenRouter, Codex)
  - Mejoras de seguridad: agente no puede reescribir config crítica
  - Memoria persistente mejorada con pruning automático

- **Ollama**: versión 0.19 (abril 2026)
  - Compatibilidad con OpenAI Chat Completions API (permite usar herramientas existentes con modelos locales)
  - Soporte MLX de Apple: 1.6x más rápido en prefill, 2x en decode en Macs M5+
  - Modelos locales disponibles: Gemma 4, Qwen3-Coder-30B, GLM-4.6

- **Anti (Antigravity)**: IDE/booster con Gemini Flash, Claude Sonnet/Opus, GPT OSS 120B
  - Solo para diseño y refactors críticos, NO como runtime de producción

- **Costo real mensual estimado**: $0 (todo local con Ollama) + $2-5 si uso DeepSeek V4 Flash ocasionalmente

### Protocolo de vigilancia y migración ágil

> **Regla de oro**: "Lo que cuesta hoy, mañana no cuesta. La tendencia en IA es deflación de precios y mejora de capacidades. No aferrarse a configuraciones viejas por inercia."

**Riesgos reales** (NO es subida de precios, es quedarse atrás):
1. Dependencia de proveedor que desaparece o cambia modelo de negocio radicalmente
2. Quedarse en versiones viejas cuando hay mejoras de 2x-3x en velocidad/costo
3. Configuraciones que se pudren por incompatibilidades entre versiones nuevas
4. No documentar setup ganador y no poder replicarlo después

**Acciones de vigilancia**:

- **Mensual**:
  - Revisar releases de Ollama, OpenClaw, DeepSeek para **mejoras** (no solo pricing)
  - Identificar modelos nuevos más baratos/rápidos que los actuales
  - Probar configuraciones nuevas en entorno aislado antes de migrar producción

- **Trimestral**:
  - Actualizar esta sección con "Configuración ganadora actual"
  - Deprecar información de versiones viejas que ya no aplican
  - Ejecutar migración si hay mejora significativa (>30% en costo o velocidad)

- **Ante cambio crítico** (proveedor cierra, API deprecada, incompatibilidad mayor):
  - Documentar el evento en este archivo inmediatamente
  - Ejecutar plan B (siempre mantener 2+ alternativas documentadas)
  - No entrar en pánico: en IA siempre hay algo más barato/mejor disponible

**Planes B actuales documentados**:
- Si Ollama falla o se vuelve de pago → DeepSeek V4 Flash (cloud, muy barato)
- Si DeepSeek sube precio → otro modelo económico del momento (revisar mensualmente)
- Si OpenClaw se vuelve pesado/comercial → NanoClaw (código mínimo) o fork de versión actual
- Si Anti mete límites duros → usar solo VS Code + GitHub Copilot (training opt-out activo)

### Cambios sustanciales recientes (OC 2026.4.24 -> 2026.5.19)

Por qué actualizar a 2026.5.19:

1. **Control de Plugins**: Nuevos comandos CLI nativos (`/codex plugins list`, `enable`, `disable`) para gestionar plugins desde el chat.
2. **Estabilidad de Navegador**: Corrección en manejo de diálogos y mejor manejo de bloqueos en tiempo de ejecución.
3. **Rediseño de Ajustes**: Nueva pantalla de Ajustes con navegación simplificada para permisos, voz y skills.
4. **Robustez Operativa**: Refuerzo de la pasarela (gateway/proxy), trazas de reinicio y enrutamiento seguro de subagentes.

### Cambios previos (OC 4.15 -> 4.24)

Por qué actualizar de 4.15 a 4.24 mejora el plan 0 costo:

1. DeepSeek V4 Flash bundled: antes había que configurar manualmente, ahora es default y extremadamente barato
2. Seguridad mejorada: el agente no puede modificar su propia config -> menos riesgo de romper setup estable
3. Memoria más eficiente: pruning automático -> menos consumo de recursos locales
4. WebRTC y Meet: nuevas capacidades sin costo adicional (útil para Globy + Discord en el futuro)

Migración recomendada: de 4.15 a 4.24 vale la pena por mejoras de estabilidad y modelo default más barato.

## 4. Otros proyectos (estado de clarificación)

> Esta sección es un placeholder para aterrizar la realidad de cada proyecto. No implica que todos estén activos.

- **Diamantino Universe**
  - Estado actual: [pendiente de documentar].
  - Repos asociados: [listar cuando se identifiquen].
  - Rol esperado: marco conceptual y operativo de estudios/producción.

- **DAVS (estudio de video)**
  - Estado actual: [pendiente de revisión].
  - Repos/scripts actuales: [pendiente].
  - Nota: en el pasado se consideró "industrial", pero debe re‑examinarse como si fuera un sistema ajeno para ver qué sigue vivo.

- **TESO**
  - Estado actual: [pendiente de documentar].
  - Repos asociados: [pendiente].

## 5. Decisión de foco (abril–mayo 2026)

- Proyecto activo principal:
  - OpenClaw operativo + Globy + Discord, bajo el plan 0 costo.
- Uso de Anti:
  - Solo como IDE y booster, no como dependencia de producción.
- Proyectos en clarificación (no ejecución industrial):
  - Diamantino Universe.
  - DAVS.
  - TESO.
- Próximo paso:
  - A medida que tenga energía, ir rellenando la sección 4 con la realidad concreta de cada proyecto (repos, scripts, estado real), sin intentar industrializar todo a la vez.
