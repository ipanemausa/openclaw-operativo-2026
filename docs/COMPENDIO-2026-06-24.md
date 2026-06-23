# COMPENDIO LAMAUTONOMIA — 2026-06-24
> Generado al cierre 2026-06-23. Leer COMPLETO antes de ejecutar cualquier comando.

## PRIMER COMANDO MAÑANA
$env:GEMINI_API_KEY="AQ.Ab8RN6KumFXo6xbYheqn2b9xBcp44vyqMOcOGyCLwg5B8fCf8A"
cat C:\Users\ipane\openclaw-cloud-2026\claw-estado.json
docker compose ps

## REPO ACTIVO
Path:   C:\Users\ipane\openclaw-cloud-2026
GitHub: https://github.com/ipanemausa/openclaw-operativo-2026

## STACK 4/4
claw-orchestrator → 8090
openclaw_app      → 3000 (dashboard vivo)
openclaw_redis    → 6379
video_veo_worker  → sin puerto

## PROBLEMA PRINCIPAL A RESOLVER MAÑANA
Tenemos 3 repos — deben quedar como 1:
- openclaw-cloud-2026   → ACTIVO fuente de verdad
- openclaw-operativo-2026 → archivar en GitHub
- openclaw-ui           → revisar y archivar

## PLAN 2026-06-24 EN ORDEN JERARQUICO
1.  Exportar GEMINI_API_KEY
2.  cat claw-estado.json
3.  docker compose ps
4.  ls C:\Users\ipane\openclaw-ui → ver contenido
5.  Extraer util de openclaw-ui → copiar a openclaw-cloud-2026
6.  Archivar openclaw-operativo-2026 en GitHub
7.  Archivar openclaw-ui en GitHub
8.  Crear gateway/Dockerfile
9.  Agregar gateway al docker-compose.yml con claw-net
10. Pipeline → verificar gateway en localhost:8080/health
11. Conectar dashboard con HB Jewelry gateway
12. Revisar cat C:\Users\ipane\.antigravity\
13. Revisar cat C:\Users\ipane\.cagent\
14. Disenar adaptadores Antigravity y Copilot
15. Deploy gateway a Google Cloud Run
16. Probar Veo 3.1 — 1 solo request
17. Generar artefacto del dia

## REGLAS ACTIVAS
1. Archivos Python largos → VS Code. NUNCA Set-Content
2. Cada archivo modificado → pipeline inmediatamente
3. GEMINI_API_KEY → exportar ANTES de cualquier compose
4. Pipeline corre despues de cada cambio
5. No asumir que algo existe — verificar con cat/ls primero
6. Un solo repo — openclaw-cloud-2026 es la fuente de verdad
7. Cada dia genera COMPENDIO del dia siguiente antes de cerrar

## ERRORES SELLADOS HOY
- GEMINI_API_KEY placeholder → validacion en pipeline
- Set-Content corta .py largos → VS Code obligatorio
- Red entre contenedores rota → claw-net resuelto
- Docker no disponible en contenedor → SDK instalado
- claw-estado.json no visible → montado como volumen

## VARIABLES CRITICAS
GEMINI_API_KEY   = AQ.Ab8RN6KumFXo6xbYheqn2b9xBcp44vyqMOcOGyCLwg5B8fCf8A
PICKAXE_API_KEY  = deployment-2e01dfdd-9acd-472d-b478-89404b9d23ac
REDIS_HOST       = redis
REDIS_PORT       = 6379
