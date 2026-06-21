# ═══════════════════════════════════════════════════════════════
# LAMAUTONOMIA — AGENTE RESIDENTE v1.0
# Uso: .\scripts\lamautonomia-agente.ps1 -Escuchar
# ═══════════════════════════════════════════════════════════════

param(
    [string]$Archivo   = "",
    [string]$Servicio  = "all",
    [string]$Mensaje   = "auto: agente lamautonomia",
    [switch]$Escuchar  = $false
)

$ROOT    = "C:\Users\ipane\openclaw-cloud-2026"
$SCRIPTS = "$ROOT\scripts"
Set-Location $ROOT

function Log-OK   { param($msg) Write-Host "  OK $msg" -ForegroundColor Green }
function Log-FAIL { param($msg) Write-Host "  FAIL $msg" -ForegroundColor Red }
function Log-INFO { param($msg) Write-Host "  -> $msg" -ForegroundColor Cyan }

function Escribir-EnVSCode {
    param([string]$RutaArchivo, [string]$NuevoContenido)
    Log-INFO "Abriendo VS Code: $RutaArchivo"
    Start-Process "code" -ArgumentList $RutaArchivo
    Start-Sleep -Seconds 3
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::SetText($NuevoContenido)
    $vs = Get-Process "Code" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($vs) {
        Add-Type @"
        using System; using System.Runtime.InteropServices;
        public class Win32 { [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h); }
"@
        [Win32]::SetForegroundWindow($vs.MainWindowHandle) | Out-Null
        Start-Sleep -Milliseconds 800
    }
    [System.Windows.Forms.SendKeys]::SendWait("^a")
    Start-Sleep -Milliseconds 300
    [System.Windows.Forms.SendKeys]::SendWait("^v")
    Start-Sleep -Milliseconds 500
    [System.Windows.Forms.SendKeys]::SendWait("^s")
    Start-Sleep -Milliseconds 500
    [System.Windows.Forms.SendKeys]::SendWait("^w")
    Start-Sleep -Seconds 1
    Log-OK "VS Code: guardado y cerrado"
}

function Ejecutar-Flujo {
    param([string]$RutaArchivo, [string]$Servicio, [string]$Mensaje)
    Write-Host "`n===============================================" -ForegroundColor Cyan
    Write-Host "AGENTE LAMAUTONOMIA — FLUJO INICIADO" -ForegroundColor Cyan
    Write-Host "Archivo : $RutaArchivo" -ForegroundColor Cyan
    Write-Host "===============================================`n" -ForegroundColor Cyan
    & "$SCRIPTS\lamautonomia-pipeline.ps1" -Servicio $Servicio -Mensaje $Mensaje
    if ($LASTEXITCODE -eq 0) {
        $estado = Get-Content "$ROOT\claw-estado.json" -Raw | ConvertFrom-Json
        $estado.notas = "Agente ejecuto flujo en $RutaArchivo — $Mensaje"
        $estado.ultima_actualizacion = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        $estado | ConvertTo-Json -Depth 3 | Set-Content "$ROOT\claw-estado.json" -Encoding UTF8
        Log-OK "claw-estado.json actualizado"
    }
    Write-Host "`n===============================================" -ForegroundColor Green
    Write-Host "FLUJO COMPLETO" -ForegroundColor Green
    Write-Host "===============================================" -ForegroundColor Green
}

function Modo-Escucha {
    Write-Host "`nAGENTE EN MODO ESCUCHA — monitoreando $ROOT" -ForegroundColor Cyan
    Write-Host "Ctrl+C para detener`n" -ForegroundColor Yellow
    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = $ROOT
    $watcher.Filter = "*.py"
    $watcher.IncludeSubdirectories = $true
    $watcher.EnableRaisingEvents = $true
    $ultimoCambio = @{}
    Register-ObjectEvent $watcher "Changed" -Action {
        $archivo = $Event.SourceEventArgs.FullPath
        $ahora = Get-Date
        if ($ultimoCambio.ContainsKey($archivo) -and ($ahora - $ultimoCambio[$archivo]).TotalSeconds -lt 5) { return }
        $ultimoCambio[$archivo] = $ahora
        $svc = "all"
        if ($archivo -match "claw-orchestrator") { $svc = "claw-orchestrator" }
        if ($archivo -match "\\app\\app.py")     { $svc = "openclaw_app" }
        Write-Host "Cambio detectado: $archivo" -ForegroundColor Yellow
        & "$SCRIPTS\lamautonomia-pipeline.ps1" -Servicio $svc -Mensaje "auto: $([IO.Path]::GetFileName($archivo))"
    } | Out-Null
    while ($true) { Start-Sleep -Seconds 1 }
}

if ($Escuchar) {
    Modo-Escucha
} elseif ($Archivo) {
    Ejecutar-Flujo -RutaArchivo $Archivo -Servicio $Servicio -Mensaje $Mensaje
} else {
    Write-Host @"
LAMAUTONOMIA AGENTE — USO:
  Modo escucha:  .\scripts\lamautonomia-agente.ps1 -Escuchar
  Flujo directo: .\scripts\lamautonomia-agente.ps1 -Archivo "ruta\archivo.py" -Servicio "claw-orchestrator"
  Solo pipeline: .\scripts\lamautonomia-pipeline.ps1 -Servicio "claw-orchestrator"
"@ -ForegroundColor Cyan
}