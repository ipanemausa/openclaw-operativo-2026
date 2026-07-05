Param(
    [Parameter(Mandatory=$true)][string]$Componente,
    [switch]$Verificar,
    [switch]$Restaurar
)
$ROOT = 'C:\Users\ipane\openclaw-cloud-2026'
$COMPONENTS = "$ROOT\frontend\src\components"
$BACKUPS = "$ROOT\scripts\backups"
$compPath = "$COMPONENTS\$Componente\$Componente.jsx"
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupPath = "$BACKUPS\$Componente-$timestamp.jsx"
if (-not (Test-Path $BACKUPS)) { New-Item -ItemType Directory -Path $BACKUPS -Force | Out-Null }
function Verificar-Sintaxis($ruta) {
    if (-not (Test-Path $ruta)) { return @{ ok = $false; razon = 'Archivo no existe' } }
    $contenido = Get-Content $ruta -Raw
    if ($contenido.Length -lt 30) { return @{ ok = $false; razon = "Archivo corto ($($contenido.Length) chars)" } }
    $exports = ([regex]::Matches($contenido, 'export\s+default')).Count
    if ($exports -eq 0) { return @{ ok = $false; razon = 'Sin export default' } }
    if ($exports -gt 1) { return @{ ok = $false; razon = "$exports export default duplicados" } }
    if ($contenido -match '\.\./\.\./\.\./styles') { return @{ ok = $false; razon = 'Ruta CSS con 3 niveles - incorrecta' } }
    $abre = ([regex]::Matches($contenido, '\{')).Count
    $cierra = ([regex]::Matches($contenido, '\}')).Count
    if ($abre -ne $cierra) { return @{ ok = $false; razon = "Llaves desbalanceadas: $abre vs $cierra" } }
    return @{ ok = $true; razon = 'OK' }
}
if ($Restaurar) {
    $ultimo = Get-ChildItem $BACKUPS -Filter "$Componente-*.jsx" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($ultimo) { Copy-Item $ultimo.FullName $compPath -Force; Write-Host "[OK] Restaurado desde $($ultimo.Name)" -ForegroundColor Green }
    else { Write-Host '[ERROR] No hay backups' -ForegroundColor Red }
    exit
}
if ($Verificar) {
    $r = Verificar-Sintaxis $compPath
    if ($r.ok) { Write-Host "[OK] $Componente correcto" -ForegroundColor Green }
    else { Write-Host "[ERROR] $Componente: $($r.razon)" -ForegroundColor Red; Write-Host "Ejecuta: .\scripts\lamautonomia-guardrail.ps1 -Componente $Componente -Restaurar" -ForegroundColor Yellow }
    exit
}
if (Test-Path $compPath) { Copy-Item $compPath $backupPath -Force; Write-Host "[BACKUP] $backupPath" -ForegroundColor Green }
else { Write-Host '[INFO] Componente nuevo, sin backup previo' -ForegroundColor Yellow }
Write-Host "[LISTO] Puedes editar $Componente" -ForegroundColor Cyan
