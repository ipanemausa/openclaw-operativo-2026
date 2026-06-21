# ═══════════════════════════════════════════════════════════════
# PROTOCOLO LAMAUTONOMIA — REGLAS DE TRABAJO
# Proyecto: C:\Users\ipane\openclaw-cloud-2026
# Version: 1.0 — 2026-06-21
# ═══════════════════════════════════════════════════════════════

# REGLA 1 — UN SOLO PROMPT HACE TODO
# Flujo sin excepcion: abrir → borrar completo → pegar curado → guardar → cerrar → probar
# Nunca parches. Nunca editar sobre lo viejo. Siempre version completa.

# REGLA 2 — TODO SE CREA EN EL PATH DE DESTINO
# Nunca crear en Descargas y mover despues.
# Patron correcto siempre:
#   Set-Content C:\Users\ipane\openclaw-cloud-2026\scripts\nombre.ps1 $contenido
#   Unblock-File C:\Users\ipane\openclaw-cloud-2026\scripts\nombre.ps1
#   .\scripts\nombre.ps1

# REGLA 3 — NOTAS DIRECTAS AL ARCHIVO CORRECTO
# claw-estado.json es la memoria del sistema.
# Cada sesion termina con ese archivo actualizado.
# Formato: tareas completadas, tareas pendientes, siguiente agente.

# REGLA 4 — SIN OVERRIDES MANUALES
# docker-compose.override.yml siempre vacio.
# Todo cambio va en docker-compose.yml completo y curado.

# REGLA 5 — GUARDRAILS FIJOS
# Nunca tocar sin mostrar diff primero:
#   - docker-compose.yml
#   - .env
#   - orchestrator.py

# REGLA 6 — PRUEBA ANTES DE CERRAR
# Todo script termina con verificacion automatica.

# PATRON PS1 — USO UNIVERSAL
# Para crear cualquier script nuevo:
#   $contenido = @' ... '@ 
#   Set-Content C:\Users\ipane\openclaw-cloud-2026\scripts\nombre.ps1 $contenido
#   Unblock-File C:\Users\ipane\openclaw-cloud-2026\scripts\nombre.ps1
#   C:\Users\ipane\openclaw-cloud-2026\scripts\nombre.ps1

# STACK ACTUAL
# claw-orchestrator  → :8090
# openclaw_app       → :3000
# openclaw_redis     → :6379
# video_veo_worker   → cola redis

# VERIFICACION RAPIDA
# docker compose ps
# curl http://localhost:8090/health
# curl http://localhost:3000/healthz

# SIGUIENTE TAREA
# Endpoints /api/radio/input y /api/radio/publish en orchestrator.py
