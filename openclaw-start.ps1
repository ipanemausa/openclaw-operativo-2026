# ============================
# OpenClaw - Ritual de Apertura
# ============================
Write-Host "=== Ritual de Apertura OpenClaw ==="
Write-Host "1. Verifica Docker Desktop (debe estar activo)."
Write-Host "2. Ejecutando docker-compose up..."
docker-compose up -d

Write-Host "3. Validando contenedores..."
docker ps --filter "name=openclaw_app"
docker ps --filter "name=openclaw_db"

Write-Host "4. Abriendo panel de Control en navegador..."
Start-Process "http://127.0.0.1:18789/chat?session=main"

Write-Host "=== Listo. Ya puedes interactuar con OC ==="
