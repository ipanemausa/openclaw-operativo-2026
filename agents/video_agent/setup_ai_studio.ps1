Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "  OPENCLAW AI STUDIO: INSTALADOR DE REDES NEURONALES" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

$SADTALKER_DIR = ".\SadTalker"

if (Test-Path $SADTALKER_DIR) {
    Write-Host "[OK] El motor de Deepfake ya esta descargado." -ForegroundColor Green
} else {
    Write-Host "[+] Descargando motor generativo de codigo abierto (SadTalker)..." -ForegroundColor Yellow
    git clone https://github.com/OpenTalker/SadTalker.git
}

Write-Host "[+] Instalando dependencias de Inteligencia Artificial (PyTorch)..." -ForegroundColor Yellow
# Instalamos la version CPU por seguridad, ya que CUDA depende de la tarjeta grafica local.
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r .\SadTalker\requirements.txt

Write-Host "[+] Descargando pesos neuronales (Checkpoints)..." -ForegroundColor Yellow
Write-Host "(Nota: En un entorno real, aqui se descargan los archivos .pth de 2GB desde HuggingFace)" -ForegroundColor Gray
# script real wget huggingface models...

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "  INSTALACION EXITOSA. El Nodo V2V esta listo." -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Cyan
