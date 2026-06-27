param(
    [Parameter(Mandatory=$true)][string]$Archivo,
    [string]$Mensaje = "update: $Archivo"
)

$ROOT = "C:\Users\ipane\openclaw-cloud-2026"
$FRONTEND = "$ROOT\frontend"

Write-Host "`n[HB] Actualizando: $Archivo" -ForegroundColor Cyan

# 1. Verificar que el archivo existe
if (-not (Test-Path $Archivo)) {
    Write-Host "[ERROR] Archivo no encontrado: $Archivo" -ForegroundColor Red
    exit 1
}

# 2. Verificar sintaxis basica (no vacio)
$contenido = Get-Content $Archivo -Raw
if ($contenido.Length -lt 10) {
    Write-Host "[ERROR] Archivo vacio o muy corto" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Archivo verificado ($($contenido.Length) chars)" -ForegroundColor Green

# 3. Git add + commit
Set-Location $ROOT
git add $Archivo 2>&1 | Out-Null
$status = git status --short
if ($status) {
    git commit -m $Mensaje 2>&1 | Out-Null
    Write-Host "[OK] Commit: $Mensaje" -ForegroundColor Green
} else {
    Write-Host "[INFO] Sin cambios para commitear" -ForegroundColor Yellow
}

# 4. Resultado
Write-Host "[HB] Listo. Vite recarga automaticamente." -ForegroundColor Cyan
Write-Host "[HB] Browser: http://localhost:5176" -ForegroundColor DarkCyan
