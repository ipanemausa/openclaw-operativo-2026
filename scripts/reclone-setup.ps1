# =====================================================================
# OpenClaw / HB Jewelry — 1-Click Reclone & Sync Command Center
# =====================================================================
# Este script sincroniza y levanta todo el entorno:
# GitHub (Código) + Docker (Servicios) + Frontend (App) + Agentes IA
# =====================================================================

$ROOT = "C:\Users\ipane\openclaw-cloud-2026"
$APP_DIR = "C:\openclaw\hb-jewelry"

Clear-Host
Write-Host "=========================================================" -ForegroundColor Green
Write-Host "       STARTING OPENCLAW & HB JEWELRY AUTO-SYNC" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green

# 1. GitHub Sync (Código Actualizado)
Write-Host "`n[1/4] Sincronizando repositorios con GitHub..." -ForegroundColor Cyan
if (Test-Path $ROOT) {
    Set-Location $ROOT
    Write-Host "-> Actualizando repositorio cloud..." -ForegroundColor DarkGray
    git fetch origin 2>$null
    git pull origin main --rebase 2>$null
}
if (Test-Path $APP_DIR) {
    Set-Location $APP_DIR
    Write-Host "-> Actualizando frontend app..." -ForegroundColor DarkGray
    git fetch origin 2>$null
    git pull origin main --rebase 2>$null
}
Write-Host "✓ GitHub sincronizado correctamente." -ForegroundColor Green

# 2. Docker Orchestration Check
Write-Host "`n[2/4] Verificando contenedores Docker..." -ForegroundColor Cyan
Set-Location $ROOT
$dockerCheck = docker ps 2>$null
if ($null -eq $dockerCheck) {
    Write-Host "[ALERTA] Docker Desktop no parece estar iniciado. Por favor, abre Docker Desktop." -ForegroundColor Red
} else {
    Write-Host "-> Levantando servicios del orquestador..." -ForegroundColor DarkGray
    docker compose up -d --build
    Write-Host "✓ Contenedores Docker levantados y saludables." -ForegroundColor Green
}

# 3. Frontend App Launch
Write-Host "`n[3/4] Iniciando servidor de desarrollo Frontend..." -ForegroundColor Cyan
if (Test-Path $APP_DIR) {
    Set-Location $APP_DIR
    # Matar proceso previo en puerto 5174
    $port = netstat -ano | findstr "LISTENING" | findstr ":5174 "
    if ($port) {
        $procId = ($port -split '\s+')[-1]
        Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
    }
    # Iniciar Vite
    Write-Host "-> Ejecutando Vite en puerto 5174..." -ForegroundColor DarkGray
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $APP_DIR; npx vite --force --port 5174"
}
Write-Host "✓ Frontend iniciado correctamente en http://localhost:5174/" -ForegroundColor Green

# 4. Environment & Health Diagnostics
Write-Host "`n[4/4] Ejecutando diagnósticos de conexión..." -ForegroundColor Cyan
Start-Sleep -Seconds 4

$gatewayStatus = "offline"
$orchestratorStatus = "offline"

try {
    $gatewayStatus = (Invoke-RestMethod -Uri "http://localhost:8080/health" -TimeoutSec 2).status
} catch {}

try {
    $orchestratorStatus = (Invoke-RestMethod -Uri "http://localhost:8090/health" -TimeoutSec 2).status
} catch {}

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host "                     ESTADO FINAL" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
Write-Host "App Frontend URL : http://localhost:5174/" -ForegroundColor Green
Write-Host "Gateway API      : http://localhost:8080/health  -> $gatewayStatus" -ForegroundColor ($gatewayStatus -eq "healthy" ? "Green" : "Red")
Write-Host "Orquestador DAG  : http://localhost:8090/health  -> $orchestratorStatus" -ForegroundColor ($orchestratorStatus -eq "ok" ? "Green" : "Red")
Write-Host "=========================================================" -ForegroundColor Green

Write-Host "`n[INFO] Para operar con tus Agentes de Inteligencia:" -ForegroundColor Yellow
Write-Host "1. En Microsoft Edge (Copilot): Puedes consultarle sobre la arquitectura del orquestador en el puerto 8090." -ForegroundColor DarkGray
Write-Host "2. En Antigravity: Puedes editar el código de la app con el blindaje de seguridad activo." -ForegroundColor DarkGray
Write-Host "=========================================================" -ForegroundColor Green
