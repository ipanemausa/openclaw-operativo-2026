# Módulo Video — Veo 3.1 + Google Vids API
## OpenClaw Cloud 2026 — HB Jewelry

### OBJETIVO
Integrar generación de video con Veo 3.1 (Google Vids API) dentro del ecosistema OpenClaw:
- Endpoint en Orquestador
- Worker dedicado
- Cliente API
- Flujo Redis → Worker → Storage
- Dockerfile + Compose

---

## 1. ESTRUCTURA DEL MÓDULO

/agents/video_veo/
    ├── app/
    │     ├── veo_worker.py
    │     ├── veo_client.py
    ├── Dockerfile
    ├── requirements.txt

/claw-orchestrator/app/routes/video_veo.py

/docs/video_veo.md (esta nota)

---

## 2. ENDPOINT PRINCIPAL (ORQUESTADOR)

POST /api/video/veo/create

Payload:
{
  "prompt": "...",
  "duration": 10,
  "resolution": "1080p",
  "style": "cinematic"
}

Respuesta:
{
  "job_id": "...",
  "status": "queued",
  "poll": "/api/video/veo/status/<job_id>"
}

---

## 3. WORKER (video_veo_worker)

Consume jobs desde Redis:
queue:video_veo

Estados:
- queued
- processing
- completed
- error

Salida:
- video_url

---

## 4. CLIENTE VEO 3.1 (Google Vids API)

Endpoint:
https://generativelanguage.googleapis.com/v1beta/models/veo-3.1:generateVideo

Requiere:
GOOGLE_API_KEY

---

## 5. DOCKERFILE DEL WORKER

FROM python:3.11-slim  
WORKDIR /app  
COPY requirements.txt .  
RUN pip install -r requirements.txt  
COPY app/ app/  
CMD ["python", "app/veo_worker.py"]

---

## 6. BLOQUE PARA DOCKER-COMPOSE

video_veo_worker:
  build: ./agents/video_veo
  container_name: video_veo_worker
  restart: always
  environment:
    - GOOGLE_API_KEY=${GOOGLE_API_KEY}
  depends_on:
    - redis

---

## 7. ENDPOINT DE STATUS

GET /api/video/veo/status/<job_id>

Devuelve:
{
  "status": "...",
  "video_url": "...",
  "prompt": "...",
  "duration": "...",
  "resolution": "...",
  "style": "..."
}

---

## 8. FLUJO COMPLETO

1. Orquestador recibe prompt  
2. Crea job_id  
3. Guarda estado en Redis  
4. Envía job a queue:video_veo  
5. Worker procesa  
6. Llama a Veo 3.1  
7. Guarda video_url  
8. Cliente consulta /status  
9. Devuelve resultado final

---

## 9. ESTADO ACTUAL DEL PROYECTO

- Orquestador operativo en :8090  
- Handoff HO-20260620-233645 recibido  
- Módulo Veo 3.1 en construcción  
- GitHub sincronizado  
- Flujo Claude → Copilot estable  
