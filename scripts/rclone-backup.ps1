# =====================================================================
# OpenClaw / HB Jewelry — 1-Click Google Drive Sync & Backup (Rclone)
# OpenClaw 2026.7.1 (Optimizado para Sincronización Incremental Ultrarrápida)
# =====================================================================

$ROOT_OPERATIVO = "C:\Users\ipane\openclaw-operativo-2026"
$APP            = "C:\openclaw\hb-jewelry"
$ROOT_CLOUD     = "C:\Users\ipane\openclaw-cloud-2026"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "      STARTING GOOGLE DRIVE BACKUP (RCLONE 2026)" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# Exclusiones optimizadas y banderas de aceleración incremental
$rcloneArgs = @(
    "sync",
    "--update",
    "--fast-list",
    "--transfers", "8",
    "--checkers", "16",
    "--exclude", "node_modules/**",
    "--exclude", ".git/**",
    "--exclude", "dist/**",
    "--exclude", ".cache/**",
    "--exclude", ".npm/**",
    "--exclude", "__pycache__/**",
    "--exclude", "*.pyc",
    "--exclude", ".ipynb_checkpoints/**",
    "--exclude", "agents/video_agent/SadTalker/checkpoints/**",
    "--exclude", "public/temp_*/**",
    "--exclude", "public/temp_yt_frames/**",
    "--exclude", "public/videos/**",
    "--exclude", "frontend/public/videos/**",
    "--exclude", "**/temp_*/**",
    "--exclude", "*.tmp"
)

# 1. Sincronizar App Frontend (hb-jewelry)
Write-Host "`n[1/3] Sincronizando Frontend (HB Jewelry) -> drive:HBJewelry..." -ForegroundColor Yellow
try {
    & rclone @rcloneArgs $APP "drive:HBJewelry"
    Write-Host "[OK] HB Jewelry respaldado exitosamente." -ForegroundColor Green
} catch {
    Write-Host "[WARN] Advertencia en sync HBJewelry: $_" -ForegroundColor Yellow
}

# 2. Sincronizar Repositorio Operativo Principal (openclaw-operativo-2026)
Write-Host "`n[2/3] Sincronizando openclaw-operativo-2026 -> drive:openclaw-operativo-2026-backup..." -ForegroundColor Yellow
try {
    & rclone @rcloneArgs $ROOT_OPERATIVO "drive:openclaw-operativo-2026-backup"
    Write-Host "[OK] Repositorio operativo respaldado exitosamente." -ForegroundColor Green
} catch {
    Write-Host "[WARN] Advertencia en sync Operativo: $_" -ForegroundColor Yellow
}

# 3. Sincronizar Repositorio Cloud Base (openclaw-cloud-2026)
if (Test-Path $ROOT_CLOUD) {
    Write-Host "`n[3/3] Sincronizando openclaw-cloud-2026 -> drive:openclaw-cloud-2026-backup..." -ForegroundColor Yellow
    try {
        & rclone @rcloneArgs $ROOT_CLOUD "drive:openclaw-cloud-2026-backup"
        Write-Host "[OK] Repositorio cloud respaldado exitosamente." -ForegroundColor Green
    } catch {
        Write-Host "[WARN] Advertencia en sync Cloud: $_" -ForegroundColor Yellow
    }
}

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host "      RESPALDO COMPLETADO EN GOOGLE DRIVE" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
