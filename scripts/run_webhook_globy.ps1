# run_webhook_globy.ps1
# Lanza el servidor Flask para recibir tareas de Globy

$WebhookPath = "C:\Users\ipane\openclaw-operativo-2026\webhook_globy.py"

Write-Host "🚀 Levantando Webhook de Globy en el puerto 8080..." -ForegroundColor Cyan
Write-Host "📂 Script: $WebhookPath" -ForegroundColor Gray

# Intentar cargar variables de entorno si existe .env
if (Test-Path "C:\Users\ipane\openclaw-operativo-2026\.env") {
    Write-Host "✅ Cargando configuración local (.env)..." -ForegroundColor Green
}

# Ejecutar el webhook
python $WebhookPath
