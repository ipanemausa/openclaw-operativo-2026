# ====================================================================
#  🎬 PIPELINE AUDIOVISUAL RESILIENTE (SUB-PIPELINE DAG VIDEO 2026)
#  OpenClaw Cloud 2026 — Protocolo de Producción Autónoma 1080p
# ====================================================================
param (
    [string]$Topic = "Revolucion IA Empresarial",
    [switch]$ForceRebuild = $false,
    [switch]$PublishYouTube = $false
)

$ErrorActionPreference = "Stop"
$ROOT_DIR = "C:\Users\ipane\openclaw-operativo-2026"
$PUBLIC_DIR = "C:\openclaw\hb-jewelry\public"
$OUT_DIR = "$PUBLIC_DIR\videos\youtube_masterclass"

Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host " 🚀 INICIANDO SUB-PIPELINE AUDIOVISUAL AUTOMÁTICO DE RESILIENCIA" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "-> Tema de Producción: $Topic" -ForegroundColor Yellow

# Step 1: Verificar y Compilar Mini-Lote Bilingüe con Paridad 1:1
Write-Host "`n[1/4] Ejecutando Motor Bilingüe Cinema Studio 2.5 (Voz Real TikTok Input)..." -ForegroundColor Green
python "$ROOT_DIR\scripts\hb_cinema_studio_engine.py" 2>&1 | Write-Host

# Step 2: Verificación de Integridad y Resiliencia de Salida
Write-Host "`n[2/4] Verificando Integridad Físicas de Archivos MP4..." -ForegroundColor Green

$es_mp4 = "$PUBLIC_DIR\youtube_30min_masterclass_full_1080p.mp4"
$en_mp4 = "$PUBLIC_DIR\youtube_30min_masterclass_en_1080p.mp4"

if ((Test-Path $es_mp4) -and (Get-Item $es_mp4).Length -gt 1MB) {
    $size_es = [math]::Round((Get-Item $es_mp4).Length / 1MB, 2)
    Write-Host " ✅ Video Maestro Español OK: $es_mp4 ($size_es MB)" -ForegroundColor Green
} else {
    Write-Error "❌ Error de Resiliencia: Video Maestro Español no pasó control de peso."
}

if ((Test-Path $en_mp4) -and (Get-Item $en_mp4).Length -gt 1MB) {
    $size_en = [math]::Round((Get-Item $en_mp4).Length / 1MB, 2)
    Write-Host " ✅ Video Maestro Inglés OK: $en_mp4 ($size_en MB)" -ForegroundColor Green
} else {
    Write-Error "❌ Error de Resiliencia: Video Maestro Inglés no pasó control de peso."
}

# Step 3: Generación de Miniaturas HD Estilo YouTube
Write-Host "`n[3/4] Generando Miniaturas de Alto Impacto 1080p..." -ForegroundColor Green
if (Test-Path "$ROOT_DIR\scripts\generate_youtube_style_thumbnails.py") {
    python "$ROOT_DIR\scripts\generate_youtube_style_thumbnails.py" 2>&1 | Write-Host
}

# Step 3.5: Publicación Autónoma en YouTube Cloud (R^768 Governed)
if ($PublishYouTube) {
    Write-Host "`n[3.5/4] Publicando Video Maestro en YouTube Cloud via API (R^768 Vector Governed)..." -ForegroundColor Yellow
    if (Test-Path "$ROOT_DIR\scripts\youtube_auto_publisher.py") {
        python "$ROOT_DIR\scripts\youtube_auto_publisher.py" --file "$es_mp4" --title "$Topic - Masterclass HB Jewelry 2026" --privacy "unlisted" 2>&1 | Write-Host
    }
}

# Step 4: Despliegue Inmediato en Firebase Hosting
Write-Host "`n[4/4] Sincronizando Nube Firebase Hosting..." -ForegroundColor Green
Set-Location "C:\openclaw\hb-jewelry"
npm run build 2>&1 | Out-Null
npx firebase-tools deploy --only hosting 2>&1 | Write-Host

Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host " 🎉 SUB-PIPELINE DE VIDEO COMPLETADO Y OPERATIVO EN LA NUBE" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Cyan
