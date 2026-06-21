# ═══════════════════════════════════════════════════════════════
# LAMAUTONOMIA — VIDEO VEO MODULE DEPLOY
# Ejecutar desde: C:\Users\ipane\openclaw-cloud-2026
# ═══════════════════════════════════════════════════════════════

Set-Location C:\Users\ipane\openclaw-cloud-2026

Write-Host "`n[1/6] Verificando GEMINI_API_KEY..." -ForegroundColor Cyan
$envContent = Get-Content .env -Raw
if ($envContent -match 'GEMINI_API_KEY=(.+)') {
    $key = $matches[1].Trim()
    if (-not $key) {
        Write-Host "GEMINI_API_KEY esta vacia en .env" -ForegroundColor Red
        $key = Read-Host "Pega tu GEMINI_API_KEY aqui"
        $envContent = $envContent -replace 'GEMINI_API_KEY=', "GEMINI_API_KEY=$key"
        Set-Content .env $envContent -NoNewline
        Write-Host "GEMINI_API_KEY guardada en .env" -ForegroundColor Green
    } else {
        Write-Host "GEMINI_API_KEY encontrada OK" -ForegroundColor Green
    }
} else {
    Write-Host "Variable GEMINI_API_KEY no encontrada en .env" -ForegroundColor Red
    exit 1
}

# ───────────────────────────────────────────────────────────────
Write-Host "`n[2/6] Corrigiendo requirements.txt..." -ForegroundColor Cyan
Set-Content agents\video_veo\requirements.txt @"
flask==3.0.3
google-generativeai==0.7.2
redis==5.0.4
requests==2.32.3
"@
Write-Host "requirements.txt corregido OK" -ForegroundColor Green

# ───────────────────────────────────────────────────────────────
Write-Host "`n[3/6] Reemplazando veo_client.py (fix GEMINI_API_KEY)..." -ForegroundColor Cyan
Set-Content agents\video_veo\app\veo_client.py @"
import requests
import os

API_KEY = os.getenv("GEMINI_API_KEY")
VEO_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/veo-3.0-generate-preview:generateVideo"

def generate_video(prompt, duration, resolution, style):
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY no configurada en .env")

    payload = {
        "instances": [{"prompt": f"{style}: {prompt}"}],
        "parameters": {
            "duration_seconds": duration,
            "resolution": resolution,
            "aspect_ratio": "16:9"
        }
    }

    response = requests.post(
        f"{VEO_ENDPOINT}?key={API_KEY}",
        json=payload,
        timeout=120
    )
    response.raise_for_status()
    data = response.json()

    predictions = data.get("predictions", [])
    if not predictions:
        raise ValueError("Veo no devolvio predicciones")

    return predictions[0].get("videoUri", predictions[0].get("url", ""))
"@
Write-Host "veo_client.py reemplazado OK" -ForegroundColor Green

# ───────────────────────────────────────────────────────────────
Write-Host "`n[4/6] Actualizando docker-compose.yml (agrega redis + video_veo_worker)..." -ForegroundColor Cyan
Set-Content docker-compose.yml @"
version: "3.9"

services:
  claw-orchestrator:
    build: ./claw-orchestrator
    container_name: claw-orchestrator
    restart: always
    ports:
      - "8090:8090"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  openclaw_app:
    build: ./app
    container_name: openclaw_app
    restart: always
    ports:
      - "3000:3000"
    depends_on:
      - claw-orchestrator

  redis:
    image: redis:7-alpine
    container_name: openclaw_redis
    restart: always
    ports:
      - "6379:6379"

  video_veo_worker:
    build:
      context: ./agents/video_veo
      dockerfile: Dockerfile.txt
    container_name: video_veo_worker
    restart: always
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis
"@
Write-Host "docker-compose.yml actualizado OK" -ForegroundColor Green

# ───────────────────────────────────────────────────────────────
Write-Host "`n[5/6] Actualizando claw-estado.json..." -ForegroundColor Cyan
$estado = @{
    tareas_activas = @(
        "Modulo Video: agregar endpoints /api/radio/input /api/radio/publish al orchestrator"
        "Modulo Video: verificar Veo API con GEMINI_API_KEY real"
        "Ajustar Docker socket en claw-orchestrator - HECHO"
        "redis + video_veo_worker en docker-compose - HECHO"
    )
    notas = "veo_client.py corregido a GEMINI_API_KEY. docker-compose incluye redis y video_veo_worker. Orquestador expone :8090 con Docker socket."
    siguiente_agente = "claude"
    ultima_actualizacion = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
} | ConvertTo-Json -Depth 3
Set-Content claw-estado.json $estado -Encoding UTF8
Write-Host "claw-estado.json actualizado OK" -ForegroundColor Green

# ───────────────────────────────────────────────────────────────
Write-Host "`n[6/6] Rebuild y levantando stack completo..." -ForegroundColor Cyan
docker compose down
docker compose up -d --build

Write-Host "`n═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host "LAMAUTONOMIA — VIDEO VEO MODULE DESPLEGADO" -ForegroundColor Green
Write-Host "Servicios esperados:" -ForegroundColor Green
Write-Host "  openclaw_app      → http://localhost:3000" -ForegroundColor Green
Write-Host "  claw-orchestrator → http://localhost:8090" -ForegroundColor Green
Write-Host "  redis             → puerto 6379" -ForegroundColor Green
Write-Host "  video_veo_worker  → procesando cola redis" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green

docker compose ps
