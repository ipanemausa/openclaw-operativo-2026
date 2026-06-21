param(
    [string]$Archivo  = "",
    [string]$Servicio = "all",
    [string]$Mensaje  = "auto: agente lamautonomia",
    [switch]$Escuchar = $false
)

$ROOT    = "C:\Users\ipane\openclaw-cloud-2026"
$SCRIPTS = "$ROOT\scripts"
Set-Location $ROOT

function Log-OK   { param($msg) Write-Host "  OK $msg" -ForegroundColor Green }
function Log-FAIL { param($msg) Write-Host "  FAIL $msg" -ForegroundColor Red }
function Log-INFO { param($msg) Write-Host "  -> $msg" -ForegroundColor Cyan }

function Modo-Escucha {
    Write-Host "AGENTE EN MODO ESCUCHA" -ForegroundColor Cyan
    Write-Host "Ctrl+C para detener" -ForegroundColor Yellow
    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = $ROOT
    $watcher.Filter = "*.py"
    $watcher.IncludeSubdirectories = $true
    $watcher.EnableRaisingEvents = $true
    $ultimoCambio = @{}
    Register-ObjectEvent $watcher "Changed" -Action {
        $archivo = $Event.SourceEventArgs.FullPath
        $ahora = Get-Date
        if ($ultimoCambio.ContainsKey($archivo)) {
            if (($ahora - $ultimoCambio[$archivo]).TotalSeconds -lt 5) { return }
        }
        $ultimoCambio[$archivo] = $ahora
        $svc = "all"
        if ($archivo -match "claw-orchestrator") { $svc = "claw-orchestrator" }
        if ($archivo -match "app.py") { $svc = "openclaw_app" }
        Write-Host "Cambio detectado: $archivo" -ForegroundColor Yellow
        & "$SCRIPTS\lamautonomia-pipeline.ps1" -Servicio $svc -Mensaje "auto-change"
    } | Out-Null
    while ($true) { Start-Sleep -Seconds 1 }
}

function Ejecutar-Flujo {
    param([string]$RutaArchivo, [string]$Servicio, [string]$Mensaje)
    Write-Host "AGENTE FLUJO: $RutaArchivo" -ForegroundColor Cyan
    & "$SCRIPTS\lamautonomia-pipeline.ps1" -Servicio $Servicio -Mensaje $Mensaje
    if ($LASTEXITCODE -eq 0) {
        $estado = Get-Content "$ROOT\claw-estado.json" -Raw | ConvertFrom-Json
        $estado.notas = "Agente ejecuto flujo en $RutaArchivo"
        $estado.ultima_actualizacion = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        $estado | ConvertTo-Json -Depth 3 | Set-Content "$ROOT\claw-estado.json" -Encoding UTF8
        Log-OK "Estado actualizado"
    }
}

if ($Escuchar) {
    Modo-Escucha
} elseif ($Archivo) {
    Ejecutar-Flujo -RutaArchivo $Archivo -Servicio $Servicio -Mensaje $Mensaje
} else {
    Write-Host "USO:" -ForegroundColor Cyan
    Write-Host "  Escucha: .\scripts\lamautonomia-agente.ps1 -Escuchar"
    Write-Host "  Directo: .\scripts\lamautonomia-agente.ps1 -Archivo ruta.py -Servicio claw-orchestrator"
}