# =====================================================================
# OpenClaw / HB Jewelry — 1-Click Google Drive Sync & Backup (Rclone)
# =====================================================================
# Excluye carpetas pesadas (node_modules, .git) para sincronización ultra-rápida
# =====================================================================

$ROOT = "C:\Users\ipane\openclaw-cloud-2026"
$APP = "C:\openclaw\hb-jewelry"

Clear-Host
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "      STARTING GOOGLE DRIVE BACKUP (RCLONE)" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# Exclusiones optimizadas
$excludeList = @(
    "--exclude", "node_modules/**",
    "--exclude", ".git/**",
    "--exclude", "dist/**",
    "--exclude", ".cache/**",
    "--exclude", ".npm/**"
)

# 1. Sincronizar App Frontend
Write-Host "`n[1/2] Sincronizando Frontend (HB Jewelry) -> drive:HBJewelry..." -ForegroundColor Yellow
rclone sync $APP drive:HBJewelry @excludeList -v
Write-Host "✓ HB Jewelry respaldado." -ForegroundColor Green

# 2. Sincronizar Repositorio Base (Contenedores + Orquestación)
Write-Host "`n[2/2] Sincronizando backend y Docker -> drive:openclaw-cloud-2026-backup..." -ForegroundColor Yellow
rclone sync $ROOT drive:openclaw-cloud-2026-backup @excludeList -v
Write-Host "✓ Repositorio base respaldado." -ForegroundColor Green

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host "      RESPALDO EXITOSO EN TU GOOGLE DRIVE (GOOGLE ONE)" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
