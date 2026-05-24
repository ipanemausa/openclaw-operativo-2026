# setup-workspace.ps1 - Configura workspace híbrido (1, 2 o 3 ventanas)

param([int]$Ventanas = 3)

Write-Host "🚀 OpenClaw Workspace Setup - $Ventanas ventana(s)" -ForegroundColor Cyan

# Ventana 1: PowerShell CLI (SIEMPRE)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; Write-Host '📱 Ventana 1: CLI' -ForegroundColor Cyan; docker compose ps"

if ($Ventanas -ge 2) {
    Start-Sleep -Seconds 1
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; Write-Host '🐳 Ventana 2: DevContainer' -ForegroundColor Green"
}

if ($Ventanas -ge 3) {
    Start-Sleep -Seconds 1
    Start-Process explorer -ArgumentList "$PSScriptRoot"
}

Write-Host "✅ Workspace listo" -ForegroundColor Green
