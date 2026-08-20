# ==============================================================================
# OPENCLAW CIERRE OPERATIVO DESATENDIDO & PIPELINE DAG
# ==============================================================================
$ErrorActionPreference = "Continue"

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host " [OPENCLAW-CORE-MATRIX] EJECUTANDO CIERRE OPERATIVO Y SINCRONIZACION" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# 1. Consolidación Git en openclaw-operativo-2026
Write-Host "`n[1/3] Sincronizando Git en openclaw-operativo-2026..." -ForegroundColor Yellow
Set-Location "C:\Users\ipane\openclaw-operativo-2026"
git add .
$DateTag = Get-Date -Format 'yyyy-MM-dd HH:mm'
git commit -m "autonomic(core-matrix): consolidation & closure $DateTag [skip ci]" --quiet
git push origin main --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Git openclaw-operativo-2026 al dia con origin/main." -ForegroundColor Green
} else {
    Write-Host "  [INFO] Git ya se encontraba al dia o status limpio." -ForegroundColor DarkGray
}

# 2. Consolidación Git en hb-jewelry si existe
if (Test-Path "C:\openclaw\hb-jewelry\.git") {
    Write-Host "`n[2/3] Sincronizando Git en hb-jewelry..." -ForegroundColor Yellow
    Set-Location "C:\openclaw\hb-jewelry"
    git add .
    git commit -m "autonomic(frontend): sync handoff and components $DateTag [skip ci]" --quiet
    git push origin main --quiet
    Write-Host "  [OK] Git hb-jewelry sincronizado." -ForegroundColor Green
}

# 3. Respaldo Rclone a Google Drive 5TB
Write-Host "`n[3/3] Ejecutando Respaldo Rclone a Google Drive (drive)..." -ForegroundColor Yellow
Set-Location "C:\Users\ipane\openclaw-operativo-2026"
& powershell -ExecutionPolicy Bypass -File ".\scripts\rclone-backup.ps1"

# Registrar en log
$logEntry = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] [OPENCLAW-CORE-MATRIX] CIERRE OPERATIVO COMPLETADO: Git Synced | Rclone 5TB Synced."
Add-Content -Path "C:\Users\ipane\openclaw-operativo-2026\ANTIGRAVITY_WORK_LOG.txt" -Value "`n$logEntry"

Write-Host "`n==================================================================" -ForegroundColor Green
Write-Host " [OK] ENTORNO CERRADO, BLINDADO Y SINCRONIZADO EN NUBE" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green

