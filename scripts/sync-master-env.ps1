# =====================================================================
# SYNC-MASTER-ENV.PS1
# Sincroniza C:\Users\ipane\.openclaw-master.env a todos los proyectos
# Uso: .\scripts\sync-master-env.ps1
# =====================================================================

$masterEnv = 'C:\Users\ipane\.openclaw-master.env'

if (-not (Test-Path $masterEnv)) {
    Write-Host '[ERROR] Master env no encontrado.' -ForegroundColor Red
    exit 1
}

Write-Host '======================================================' -ForegroundColor Cyan
Write-Host '  OPENCLAW SYNC MASTER ENV                           ' -ForegroundColor Cyan
Write-Host "  Fuente: $masterEnv" -ForegroundColor Cyan
Write-Host '======================================================' -ForegroundColor Cyan

$targets = @(
    'C:\Users\ipane\openclaw-operativo-2026\.env',
    'C:\openclaw\hb-jewelry\.env.local'
)

foreach ($target in $targets) {
    $dir = Split-Path $target -Parent
    if (Test-Path $dir) {
        Copy-Item -Path $masterEnv -Destination $target -Force
        Write-Host "[OK] -> $target" -ForegroundColor Green
    } else {
        Write-Host "[SKIP] No existe: $dir" -ForegroundColor Yellow
    }
}

Write-Host ''
Write-Host '[LISTO] Proyectos sincronizados con master env.' -ForegroundColor Cyan
Write-Host 'Reinicia Docker: docker compose up -d --force-recreate' -ForegroundColor Yellow
