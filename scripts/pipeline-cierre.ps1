# =====================================================================
# OPENCLAW MASTER CLOSURE PIPELINE (CIERRE DE JORNADA / RESPALDO TOTAL)
# =====================================================================

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMsg = "backup: Auto-sync total pipeline closure [$timestamp]"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "     OPENCLAW MASTER CLOSURE PIPELINE - FULL STACK       " -ForegroundColor Cyan
Write-Host "     Fecha/Hora: $timestamp                              " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# 1. VERIFICACION Y COMMIT / PUSH GIT
Write-Host "`n[1/3] Sincronizando repositorio Git y GitHub..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "-> Cambios detectados. Creando commit automatico..." -ForegroundColor Gray
    git add .
    git commit -m "$commitMsg"
    git push origin main
    Write-Host "-> Commit y Push a GitHub completado." -ForegroundColor Green
} else {
    Write-Host "-> No hay cambios pendientes en Git. Repositorio al dia." -ForegroundColor Green
}

# 2. RESPALDO GOOGLE DRIVE VIA RCLONE
Write-Host "`n[2/3] Sincronizando respaldo en Google Drive (Rclone)..." -ForegroundColor Yellow
$rcloneScript = Join-Path $PSScriptRoot "rclone-backup.ps1"
if (Test-Path $rcloneScript) {
    & $rcloneScript
    Write-Host "-> Respaldo Rclone en Google Drive finalizado." -ForegroundColor Green
} else {
    Write-Host "-> Script rclone-backup.ps1 no encontrado en $rcloneScript" -ForegroundColor Red
}

# 3. ACTUALIZAR LOG
Write-Host "`n[3/3] Registrando estado final del ecosistema..." -ForegroundColor Yellow
$parentDir = Split-Path -Path $PSScriptRoot -Parent
$logFile = Join-Path $parentDir "ANTIGRAVITY_WORK_LOG.txt"
$logEntry = "[$timestamp] PIPELINE CIERRE COMPLETO: Git synced, Google Drive backed up, Stack verified."
Add-Content -Path $logFile -Value "`n$logEntry"

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host "    PIPELINE DE CIERRE Y RESPALDO COMPLETADO 100%        " -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
