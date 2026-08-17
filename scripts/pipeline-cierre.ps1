# ==============================================================================
# OPENCLAW CIERRE OPERATIVO DESATENDIDO
# ==============================================================================
$ErrorActionPreference = "Stop"

Write-Host ">>> EJECUTANDO CIERRE OPERATIVO INTEGRAL..." -ForegroundColor Magenta
& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "pipeline-dag-2026-08-17.ps1")

Write-Host "`n>>> Verificando resumen de correos diarios..." -ForegroundColor Magenta
python (Join-Path $PSScriptRoot "mail_guardian_agent.py") --unread

Write-Host "`n[OK] Entorno cerrado, blindado y sincronizado." -ForegroundColor Green
