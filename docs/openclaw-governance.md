# 📘 OPENCLAW – DOCUMENTO ÚNICO DE GOBERNANZA, OPERACIÓN Y SINCRONIZACIÓN

**Versión:** 1.0 (Única y Final)  
**Fecha:** 2026-06-02  
**Estado:** ACTIVO - Reemplaza todos los documentos previos  
**Autoridad:** Guillermo (Usuario Principal)

---

## RESUMEN EJECUTIVO

Este documento consolidado define TODAS las reglas de OpenClaw:
- Gobernanza (main read-only, PR obligatorio)
- Operación (sincronización, health checks)
- Responsabilidades (RACI matrix)
- Fases del pipeline (1-4)
- Protocolos (Anti ↔ Gordon ↔ PowerShell)
- Rollback (reversión rápida)
- .env management (secretos protegidos)

**TODO ESTÁ EN ESTE DOCUMENTO. No hay referencias externas.**

Reemplaza y deja OBSOLETOS todos los documentos anteriores.

---

## 1. PRINCIPIO FUNDAMENTAL

- **Main branch = Producción estable, lectura única**
- **Ningún agente escribe directo en main**
- **TODO entra por Pull Request**
- **Anti revisa, PowerShell autoriza, Gordon ejecuta**

---

## 2. POLÍTICA DE RAMAS

```
main                    ← Producción (PROTEGIDA)
user/guillermo          ← Cambios del usuario
agent/gordon            ← Cambios de diagnóstico
agent/anti              ← Auditoría
agent/pickaxe           ← Motor (raro)
```

**Reglas:**
- ✅ Crear rama si no existe
- ❌ Trabajar en main
- ❌ Commit directo a main
- ❌ Force push

---

## 3. FLUJO DE INTEGRACIÓN (TODO entra por PR)

```
1. Agente crea rama + commit + push
2. Abre PR en GitHub
3. Anti revisa + aprueba
4. Gordon valida coherencia
5. PowerShell merge a main
6. docker compose down + up
7. HEALTH_CHECK
8. Registrar en DAILY_LOG.md
```

---

## 4. ARCHIVOS SAGRADOS (PROTEGIDOS)

NO se pueden modificar sin PR + review:

```
docker-compose.yml    (puerto 8080, networking)
.env                  (secretos, NUNCA en GitHub)
Dockerfile.*          (builds)
gateway.py            (router)
app.py                (lógica)
mcp_gateway.py        (enrutamiento)
```

---

## 5. POWERSHELL VERDE = ORQUESTADOR

Tu pestaña verde es:
- Punto de control
- Autoridad final
- Lugar donde se sincroniza TODO
- Lugar donde se valida TODO

Ejecuta:
```
git pull
docker compose down/up
HEALTH_CHECK
```

---

## 6. PROTOCOLO ANTI ↔ GORDON ↔ POWERSHELL

**PASO 1: PowerShell (local)**
- git pull, commit, push, crear PR

**PASO 2: Anti (auditor GitHub)**
- Revisa PR
- Si OK: "Approved ✅"
- Si NO: "Changes Requested"

**PASO 3: Gordon (ejecutor)**
- Valida coherencia
- Señala problemas si los hay

**PASO 4: PowerShell (merge)**
- git merge
- docker rebuild
- HEALTH_CHECK
- Registrar en DAILY_LOG.md

---

## 7. ESTADO VÁLIDO DE DOCKER

Checklist obligatorio:

```bash
# Gateway
curl http://localhost:8080/health → {"status":"ok"}
curl http://localhost:8080/api/mcp/status → {"status":"operational"}

# App
curl http://localhost:8084/ → {"status":"online"}

# DB
psql -c "SELECT 1;" → 1

# Agente main
curl -X POST .../mcp/message → {"status":"success"}

# UI
curl http://localhost:8080/chat → HTTP 200
```

---

## 8. MATRIZ RACI (RESPONSABILIDADES)

| Tarea | Gordon | PowerShell | Anti | Pickaxe |
|-------|--------|------------|------|---------|
| Monitoreo | C | R | I | - |
| Diagnóstico | R | A | S | - |
| Propuesta | R | A | - | - |
| Aprobación | - | R | A | - |
| Aplicar cambio | S | R | - | - |
| Testeo | R | A | - | S |
| Documentar | A | R | R | - |
| Auditar | - | - | R | - |

---

## 9. ROLLBACK (REVERSIÓN)

Antes de cambios críticos:

```bash
docker compose config > snapshots/config-$(date +%s).yml
git rev-parse HEAD > snapshots/last-commit.txt
```

Si falla:

```bash
docker compose down
git checkout $(cat snapshots/last-commit.txt)
docker compose up -d
HEALTH_CHECK
```

---

## 10. MANEJO DE .ENV

- **`.env` NUNCA en GitHub** (contiene secretos)
- **`.env.example` SÍ en GitHub** (sin valores)
- Cambios documentados en `docs/ENV_CHANGELOG.txt` (sin valores reales)
- Gordon puede ver `.env` localmente SOLO
- Anti audita cambios sin ver secretos

---

## 11. SINCRONIZACIÓN DIARIA

### Mañana (09:00)
```
git pull origin main
docker compose down
docker compose up -d --build
HEALTH_CHECK
Registrar en DAILY_LOG.md
```

### Mediodía (12:30)
```
git status
Si hay cambios: crear PR, esperar Anti, merge
docker rebuild + HEALTH_CHECK
```

### Tarde (17:00)
```
git status → limpio
docker ps → todos UP
HEALTH_CHECK → verde
Registrar en DAILY_LOG.md
```

---

## 12. FASES DEL PIPELINE

### FASE 1: OPERACIÓN NORMAL (0%)
- Chat normal
- Sin cambios

### FASE 2: CAMBIO PUNTUAL (< 1%)
- Cambio en 1-2 líneas indicadas
- "Edita X en línea Y"
- Sin exploración

### FASE 3: DIAGNÓSTICO (3-5%)
- Algo está roto
- Necesita investigación
- Gordon propone solución
- Espera aprobación

### FASE 4: AUDITORÍA GLOBAL (10-15%)
- Revisión completa
- Requiere confirmación de costo ANTES
- Requiere aprobación de cambios ANTES

---

## 13. DOCUMENTOS OFICIALES (CONSOLIDADOS EN ESTE ARCHIVO)

Todo está aquí. No hay archivos externos.

Documentos viejos archivados en `docs/archive/` con etiqueta `[OBSOLETO]`.

---

## 14. FIN DEL DOCUMENTO

Este documento es la única fuente de verdad.

Reemplaza TODOS los anteriores.

En vigor a partir de: **2026-06-02**

Autoridad: **Guillermo (Usuario Principal)**
