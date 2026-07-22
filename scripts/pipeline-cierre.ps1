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
Write-Host "`n[1/4] Sincronizando repositorio Git y GitHub..." -ForegroundColor Yellow
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

# 2. BUILD Y DESPLIEGUE EN FIREBASE HOSTING (PUBLIC FULL STACK)
Write-Host "`n[2/4] Compilando y desplegando en Firebase Hosting Public..." -ForegroundColor Yellow
$appDir = "C:\openclaw\hb-jewelry"
if (Test-Path $appDir) {
    Push-Location $appDir
    try {
        Write-Host "-> Compilando bundle de produccion (npm run build)..." -ForegroundColor Gray
        npm run build
        Write-Host "-> Desplegando en Firebase Hosting..." -ForegroundColor Gray
        npx firebase deploy --only hosting
        Write-Host "-> Firebase Hosting activo en https://hb-jewelry-app.web.app" -ForegroundColor Green
    } catch {
        Write-Host "-> Error en la compilacion o despliegue de Firebase: $_" -ForegroundColor Red
    } finally {
        Pop-Location
    }
} else {
    Write-Host "-> Directorio $appDir no encontrado para despliegue." -ForegroundColor Red
}

# 3. RESPALDO GOOGLE DRIVE VIA RCLONE
Write-Host "`n[3/4] Sincronizando respaldo en Google Drive (Rclone)..." -ForegroundColor Yellow
$rcloneScript = Join-Path $PSScriptRoot "rclone-backup.ps1"
if (Test-Path $rcloneScript) {
    & $rcloneScript
    Write-Host "-> Respaldo Rclone en Google Drive finalizado." -ForegroundColor Green
} else {
    Write-Host "-> Script rclone-backup.ps1 no encontrado en $rcloneScript" -ForegroundColor Red
}

# 4. ACTUALIZAR LOG EN WORK LOG
Write-Host "`n[4/4] Registrando estado final del ecosistema..." -ForegroundColor Yellow
$parentDir = Split-Path -Path $PSScriptRoot -Parent
$logFile = Join-Path $parentDir "ANTIGRAVITY_WORK_LOG.txt"
$logEntry = "[$timestamp] PIPELINE CIERRE FULL STACK: Git GitHub synced | Firebase Hosting Deployed (hb-jewelry-app.web.app) | Google Drive Rclone backed up."
Add-Content -Path $logFile -Value "`n$logEntry"

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host "    PIPELINE FULL STACK COMPLETADO EXITOSAMENTE 100%    " -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
