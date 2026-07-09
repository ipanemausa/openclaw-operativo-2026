# ═══════════════════════════════════════════════════════════════
# LAMAUTONOMIA — WORKFLOW / PIPELINE / ARTEFACTO PARA MAÑANA
# HB Jewelry — OpenClaw Cloud 2026
# Generado: 2026-07-09 (noche) para sesion 2026-07-10
# ═══════════════════════════════════════════════════════════════

## 1. PEGAR ESTO COMO PRIMER MENSAJE EN EL CHAT NUEVO CON CLAUDE

Contexto LAMAUTONOMIA - HB Jewelry. Proyecto raiz: C:\Users\ipane\openclaw-cloud-2026
(NUNCA openclaw-ui ni openclaw-operativo-2026 como raiz - esos son symlink/submodulo)

Estado confirmado al cierre de la sesion anterior:
- 6 contenedores Docker corriendo: claw-orchestrator, openclaw_app, redis,
  video_veo_worker, chat_worker, gateway
- docker-compose.yml reconstruido completo con los 6 servicios reales
- Volumen claw-estado.json montado correctamente en claw-orchestrator
- Dashboard con LAMAUTONOMIA funcionando: Contenedores, Gateway, DAG-Tareas (7 completadas)
- Scroll interno del panel central corregido (min-height: 0 en app-content)
- Sidebar agrupado en 4 secciones: Principal, Operaciones, Marketing & Analytics, Sistema
- Chat-IDE funcional: chat_worker con DeepSeek detecta "crea/modifica" y escribe
  archivos directo via POST /api/hb/write-file
- Guardrail creado: scripts/lamautonomia-guardrail.ps1 (backup + verificacion + restore)
- Tags de git: v2.0-estable (checkpoint del Dashboard restaurado)

Historial multimodel encontrado (para investigar mas si hace falta):
- commit 0ae4514: chat_worker Gemini + file upload
- commit 4fb3cd3: SSE Gemini funcional
- commit 2d79580: chat_worker IDE mode + gemini-2.0-flash
- chat_worker actual tiene AMBAS keys cargadas: GEMINI_API_KEY y DEEPSEEK_API_KEY
  (verificado con docker inspect chat_worker)

Reglas de Gordon (scripts/PROTOCOLO-LAMAUTONOMIA.ps1) que seguimos:
1. Un solo prompt hace todo - version completa, nunca parches
2. Todo se crea en el path de destino final - nunca en Descargas
3. claw-estado.json es la memoria del sistema - cuidar su estructura {tareas: {...}}
4. Sin overrides manuales - docker-compose.yml completo y curado
5. Guardrails fijos - nunca tocar docker-compose.yml/.env/orchestrator.py sin mostrar diff
6. Prueba antes de cerrar - verificacion automatica

═══════════════════════════════════════════════════════════════

## 2. PRIMER COMANDO AL ABRIR (verificacion, sin tocar nada)

cd C:\Users\ipane\openclaw-cloud-2026
docker compose ps
Get-Content scripts\lamautonomia-log.txt -Tail 15

Luego abrir Vite:
cd frontend
pnpm dev

Abrir browser en el puerto que muestre (default http://localhost:5173) y confirmar
que LAMAUTONOMIA carga con Contenedores/Gateway/DAG-Tareas.

═══════════════════════════════════════════════════════════════

## 3. PIPELINE DE TRABAJO (repetir para cada bloque de cambios)

PASO 1 - Backup antes de tocar componentes:
  .\scripts\lamautonomia-guardrail.ps1 -Componente NombreDelComponente

PASO 2 - Dar la orden en el chat de la app (Chat Agentes -> General):
  Formato obligatorio por linea: "crea/modifica un componente llamado X con..."
  Nunca mezclar con preguntas o contexto largo en el mismo mensaje - el chat_worker
  busca lineas que empiecen con crea/crear/genera/generar/modifica/actualiza

PASO 3 - Verificar despues de la ejecucion:
  .\scripts\lamautonomia-guardrail.ps1 -Componente NombreDelComponente -Verificar

PASO 4 - Si fallo, restaurar:
  .\scripts\lamautonomia-guardrail.ps1 -Componente NombreDelComponente -Restaurar

PASO 5 - Confirmar visualmente en el browser (Ctrl+Shift+R)

PASO 6 - Commit + push + log, todo en un bloque:
  cd C:\Users\ipane\openclaw-cloud-2026
  git add .
  git commit -m "descripcion clara del cambio"
  git push origin main
  .\scripts\lamautonomia-continuity.ps1 -Tarea "descripcion" -Estado "completado"

═══════════════════════════════════════════════════════════════

## 4. TAREAS PENDIENTES PARA MAÑANA (en orden sugerido)

BLOQUE A - Datos reales en componentes (pegar en chat de la app, General):
  1. modifica el componente Ventas para que cargue datos reales desde GET /api/hb/ventas
     usando useEffect con loading y tabla hb-table, manteniendo import ../../styles/hb.css
  2. modifica el componente Productos para que cargue datos reales desde GET /api/hb/productos
     usando useEffect con formulario hb-form, manteniendo import ../../styles/hb.css
  3. modifica el componente Ordenes para que cargue datos reales desde GET /api/hb/ordenes
     usando useEffect con badge hb-badge en colores, manteniendo import ../../styles/hb.css
  4. modifica el componente Clientes para que cargue datos reales desde GET /api/hb/clientes
     usando useEffect con tabla hb-table, manteniendo import ../../styles/hb.css

BLOQUE B - Formularios (si el bloque A sale bien):
  5. crea un componente llamado ClienteForm con formulario nombre telefono email canal
     preferido usando hb-form hb-input, con import ../../styles/hb.css
  6. crea un componente llamado ProductoForm con formulario nombre precio stock categoria
     descripcion usando hb-form hb-input, con import ../../styles/hb.css

BLOQUE C - Investigacion pendiente (solo lectura, sin ejecutar cambios):
  7. Revisar si vale la pena reactivar el chat_worker Gemini historico (commit 2d79580)
     como fallback cuando DeepSeek falle - NO implementar sin discutir primero
  8. Revisar por que llegan emails de deploy fallido - verificar configuracion externa
     de Railway/Cloud Run (no encontramos archivos railway.toml ni workflow en el repo,
     la causa esta fuera del codigo, en el dashboard de la plataforma)

═══════════════════════════════════════════════════════════════

## 5. GUARDRAILS - NO TOCAR SIN MOSTRAR DIFF PRIMERO

- docker-compose.yml (ya reconstruido correctamente - NO reescribir desde cero otra vez)
- claw-estado.json (estructura debe mantener siempre {"tareas": {...}} no "tareas_activas")
- .env
- claw-orchestrator/app/orchestrator.py

Si algun script antiguo (como lamautonomia-video-veo.ps1) intenta sobreescribir estos
archivos con Set-Content, REVISAR el contenido resultante antes de ejecutar el bloque.

═══════════════════════════════════════════════════════════════

## 6. LECCIONES DE HOY (para no repetir errores)

- Los scripts antiguos en la raiz (lamautonomia-video-veo.ps1, etc.) pueden sobreescribir
  claw-estado.json y docker-compose.yml con versiones incompletas sin avisar.
  Revisar su contenido con Get-Content ANTES de ejecutarlos si vuelven a usarse.
- git status en la raiz puede mostrar "modified: openclaw-operativo-2026" - eso es
  el submodulo interno, no un proyecto separado. Es normal, no confundirse.
- Cuando el Dashboard muestra "Sin tareas" en el DAG, el problema casi siempre es
  el volumen de claw-estado.json no montado o el archivo con estructura incorrecta.
- Los backups completos van en scripts\backups\ con timestamp - hacer siempre backup
  + commit + push en el MISMO bloque de comandos, nunca por separado.

═══════════════════════════════════════════════════════════════
FIN DEL DOCUMENTO - Generado para continuidad de sesion 2026-07-10
═══════════════════════════════════════════════════════════════
