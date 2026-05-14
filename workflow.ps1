# workflow.ps1
Write-Host "🔧 Verificando Docker Desktop..." -ForegroundColor Cyan
docker info | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker no está corriendo. Abre Docker Desktop y vuelve a ejecutar este script." -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Levantando contenedores de OpenClaw..." -ForegroundColor Cyan
cd C:\Users\ipane\openclaw-operativo-2026
docker-compose build
docker-compose up -d

Write-Host "📊 Estado de los contenedores:" -ForegroundColor Cyan
docker ps

Write-Host "🌐 Gateway disponible en: http://127.0.0.1:18789/" -ForegroundColor Green
