# openclaw-launch.ps1
# Script de arranque automatizado para OpenClaw Operativo 2026

Write-Host "=== OpenClaw Operativo 2026: Inicio de pipeline ===" -ForegroundColor Cyan

# 1. Ir al directorio del repo
Set-Location "C:\Users\ipane\openclaw-operativo-2026"

# 2. Actualizar repo desde GitHub
git fetch --all
git checkout scripts/Dockerfile
git pull origin scripts/Dockerfile

# 3. Reconstruir stack limpio
docker compose down --rmi all --volumes --remove-orphans
docker compose up -d --build

# 4. Verificar contenedores activos
docker ps

# 5. Health-check del gateway
Write-Host "=== Verificando gateway en http://127.0.0.1:18789/healthz ===" -ForegroundColor Yellow
curl http://127.0.0.1:18789/healthz

# 6. Abrir IDE OC en navegador
Start-Process "http://127.0.0.1/chat?session=main"

Write-Host "=== Pipeline completado. IDE OC conectado. ===" -ForegroundColor Green
