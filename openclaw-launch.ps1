# openclaw-launch.ps1
# Script de arranque automatizado para OpenClaw Operativo 2026

Write-Host "=== OpenClaw Operativo 2026: Inicio de pipeline ===" -ForegroundColor Cyan

# 1. Ir al directorio del repo
Set-Location $PSScriptRoot

# 2. Actualizar repo desde GitHub
git fetch --all
git checkout scripts/Dockerfile
git pull origin scripts/Dockerfile

# 3. Reconstruir stack limpio
docker compose down --rmi all --volumes --remove-orphans
docker compose up -d --build

# 4. Verificar contenedores activos
docker ps

# 5. Health-check del gateway y dashboard
Write-Host "=== Verificando gateway en http://127.0.0.1:8080/health ===" -ForegroundColor Yellow
Invoke-RestMethod -Uri "http://127.0.0.1:8080/health"

Write-Host "=== Verificando dashboard en http://127.0.0.1:18789/healthz ===" -ForegroundColor Yellow
Invoke-RestMethod -Uri "http://127.0.0.1:18789/healthz"

# 6. Obtener token de OpenClaw
$OpenClawConfigPath = "C:\Users\ipane\.openclaw\openclaw.json"
if (Test-Path $OpenClawConfigPath) {
    $openclawJson = Get-Content -Raw -Path $OpenClawConfigPath | ConvertFrom-Json
    $token = $openclawJson.gateway.auth.token
    Write-Host "✅ Token de Gateway detectado." -ForegroundColor Green
    $dashboardUrl = "http://127.0.0.1:18789/chat?session=main&token=$token"
} else {
    Write-Warning "⚠️ No se pudo encontrar openclaw.json en $OpenClawConfigPath. Abriendo sin token..."
    $dashboardUrl = "http://127.0.0.1:18789/chat?session=main"
}

# 7. Abrir IDE OC en navegador
Write-Host "🌐 Abriendo OpenClaw en el navegador: $dashboardUrl" -ForegroundColor Cyan
Start-Process $dashboardUrl

Write-Host "=== Pipeline completado. IDE OC conectado. ===" -ForegroundColor Green
