# dev-run.ps1 - Ejecuta DevContainer Hybrid con Docker Compose

Write-Host "🚀 OpenClaw Hybrid DevContainer + Docker Compose" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Verificar Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker no instalado" -ForegroundColor Red
    exit 1
}

# Obtener ruta del script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Opción del usuario
Write-Host "`nOpciones:" -ForegroundColor Yellow
Write-Host "1. Levantar Docker Compose (OpenClaw + Gemini)" -ForegroundColor Green
Write-Host "2. Abrir DevContainer CLI (con herramientas de video)" -ForegroundColor Green
Write-Host "3. Ambos (recomendado)" -ForegroundColor Green

$choice = Read-Host "Selecciona (1-3)"

# Opción 1: Docker Compose
if ($choice -eq "1" -or $choice -eq "3") {
    Write-Host "`n📦 Levantando Docker Compose..." -ForegroundColor Cyan
    docker compose down 2>$null
    docker compose up -d --build
    
    Write-Host "✅ OpenClaw dashboard disponible en: http://127.0.0.1:18789/dashboard" -ForegroundColor Green
    Start-Sleep -Seconds 3
}

# Opción 2 o 3: DevContainer
if ($choice -eq "2" -or $choice -eq "3") {
    Write-Host "`n🔧 Abriendo DevContainer CLI..." -ForegroundColor Cyan
    Write-Host "Dentro del container:" -ForegroundColor Yellow
    Write-Host "  - Python 3 + pip" -ForegroundColor White
    Write-Host "  - OpenCV para video" -ForegroundColor White
    Write-Host "  - FFmpeg para procesamiento" -ForegroundColor White
    Write-Host "  - Gemini AI client" -ForegroundColor White
    Write-Host "  - Git limpio (sin errores NTFS)" -ForegroundColor White
    Write-Host "`nEscribe 'exit' para salir del container`n" -ForegroundColor Yellow
    
    docker run -it `
        --rm `
        --volume "$($scriptPath):/workspace" `
        --volume "/var/run/docker.sock:/var/run/docker.sock" `
        --network host `
        openclaw-devenv:latest `
        /bin/bash
}

Write-Host "`n✅ Sessión finalizada" -ForegroundColor Green
