---
name: deepseek-harness-orchestrator
description: Sub-agente y habilidad de orquestación inspirada en la arquitectura unificada de DeepSeek Harness V4/V5. Maneja la jerarquización de plugins, catalogación de código de colores, ruteo de logs y despliegue determinista sin duplicidades.
---

# 🤖 DeepSeek Harness Orchestrator (V4/V5 Standard)

## 📌 Principios de Arquitectura
1. **Unificación Total (Single Source of Truth)**:
   - Todo plugin, regla, script o microservicio pertenece a una categoría única con metadatos estructurados.
   - Las claves de API derivan exclusivamente del archivo maestro `C:\Users\ipane\.openclaw-master.env`.

2. **Categorización Visual & Código de Colores**:
   - 🟢 **Gateway / MCP**: APIs, WSGI, Servidores Backend.
   - 🔵 **Frontend / UI**: Componentes React, Estilos CSS, Vistas de usuario.
   - 🟡 **Plugins & Skills**: Habilidades `.agents/skills/`, sub-agentes.
   - 🟣 **DAG & Automation**: Scripts de compilación, pipelines de renderizado.
   - 🔴 **Logs & Audits**: Trazabilidad, métricas RAG, logs de error.

3. **Gobernanza Inmutable**:
   - Cero duplicación de código.
   - Verificación previa de firma de funciones y endpoints antes de desplegar.
   - Blindaje de componentes UI bajo la versión de referencia `v2.0-stable`.

## 🛠️ Flujo de Invocación
Cuando el sistema ejecuta una tarea bajo esta habilidad:
1. Inspecciona el `MANIFIESTO_ARQUITECTURA_OPENCLAW_2026.md` para ubicar el módulo correspondiente.
2. Ejecuta la validación de claves en `.env`.
3. Invoca la pasarela MCP a través de `/api/mcp/message` o el ejecutable Python correspondiente.
4. Escribe la telemetría de ejecución en `logs/` y registra el resultado final en `ANTIGRAVITY_WORK_LOG.txt`.
