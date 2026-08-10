# =====================================================================
# OPENCLAW SADTALKER CHECKPOINT DOWNLOADER
# Descarga los pesos neuronales 3DMM para animación de cabeza, cara y labios
# =====================================================================

$CHECKPOINTS_DIR = Join-Path $PSScriptRoot "SadTalker\checkpoints"
$GFPGAN_DIR = Join-Path $PSScriptRoot "SadTalker\gfpgan\weights"

if (-not (Test-Path $CHECKPOINTS_DIR)) {
    New-Item -ItemType Directory -Path $CHECKPOINTS_DIR -Force
}
if (-not (Test-Path $GFPGAN_DIR)) {
    New-Item -ItemType Directory -Path $GFPGAN_DIR -Force
}

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "  DESCARGANDO PESOS NEURONALES SADTALKER (ANIMACION 3D)  " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

$baseUrl = "https://huggingface.co/vinthony/SadTalker/resolve/main/checkpoints"
$files = @(
    "SadTalker_V0.0.2_256.safetensors",
    "mapping_0.0.1.pth",
    "mapping_0.0.2.pth",
    "auido2pose_0.0.1.pth",
    "auido2exp_0.0.1.pth",
    "facevid2vid_0.0.1_256.pth",
    "epoch_20.pth"
)

foreach ($f in $files) {
    $targetPath = Join-Path $CHECKPOINTS_DIR $f
    if (-not (Test-Path $targetPath)) {
        Write-Host "[+] Descargando $f..." -ForegroundColor Yellow
        $url = "$baseUrl/$f?download=true"
        Invoke-WebRequest -Uri $url -OutFile $targetPath -UseBasicParsing
        Write-Host "✓ $f completado." -ForegroundColor Green
    } else {
        Write-Host "[OK] $f ya existe." -ForegroundColor Green
    }
}

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host "  DESCARGA DE MODELOS SADTALKER COMPLETA EXITOSAMENTE  " -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
