# ==============================================================================
# ARTEFACTO MAESTRO AUTÓNOMO: WATCHER & DEMONIO DE CIERRE (OPENCLAW-CORE)
# Espacio Vectorial: R^768 Unitario | Sincronización Automática por Eventos
# Política: $0 Costo Operativo / Cero Fricción / Cero Intervención Manual
# ==============================================================================

param(
    [string]$WatcherPath = "C:\Users\ipane\openclaw-operativo-2026",
    [int]$DebounceSeconds = 30
)

$Filter = "*.*"
$global:IncludeExtensions = @(".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".env", ".md", ".css", ".html")
$global:WorkspaceRoot = $WatcherPath

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " INICIANDO WATCHER AUTÓNOMO OPENCLAW-CORE (R^768)" -ForegroundColor Green
Write-Host " Monitoreando cambios en: $WatcherPath" -ForegroundColor Cyan
Write-Host " Ventana de debounce: ${DebounceSeconds}s" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

if (-not (Test-Path $WatcherPath)) {
    Write-Host "[ERROR] La ruta especificada no existe: $WatcherPath" -ForegroundColor Red
    exit 1
}

$Watcher = New-Object System.IO.FileSystemWatcher
$Watcher.Path = $WatcherPath
$Watcher.Filter = $Filter
$Watcher.IncludeSubdirectories = $true
$Watcher.EnableRaisingEvents = $true

# Control de debounce para evitar ejecuciones múltiples ante ráfagas de guardado
$global:LastExecution = [DateTime]::MinValue

$Action = {
    $Path = $Event.SourceEventArgs.FullPath
    $Extension = [System.IO.Path]::GetExtension($Path)
    
    # Filtrar solo extensiones de interés y evitar bucles en carpetas de logs o git internas
    if ($global:IncludeExtensions -contains $Extension -and $Path -notmatch "(\.git|node_modules|logs|archive|dist|\.cache|temp_)") {
        $Now = Get-Date
        # Esperar al menos el tiempo de debounce entre ejecuciones automáticas
        if (($Now - $global:LastExecution).TotalSeconds -gt 30) {
            $global:LastExecution = $Now
            Write-Host "`n[AUTO-SYNC] Cambio detectado en: $Path" -ForegroundColor Yellow
            Write-Host "[AUTO-SYNC] Ejecutando pipeline de gobernanza y respaldo..." -ForegroundColor Cyan
            
            Push-Location $global:WorkspaceRoot
            try {
                # 1. Ejecutar Gobernanza Vectorial R^768
                $govScript = Join-Path $global:WorkspaceRoot "scripts\r768_orchestrator_governor.py"
                if (Test-Path $govScript) {
                    python $govScript
                }
                
                # 2. Sincronización automática con Git
                git add .
                $gitStatus = git status --porcelain
                if ($gitStatus) {
                    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                    git commit -m "auto: sincronización inteligente por watcher R768 [$timestamp]"
                    git push origin main
                    Write-Host "[AUTO-SYNC] Cambios propagados a GitHub con éxito." -ForegroundColor Green
                } else {
                    Write-Host "[AUTO-SYNC] No hay cambios pendientes para commit." -ForegroundColor Gray
                }
                
                # 3. Respaldo asíncrono con Rclone a Google Drive 5TB
                rclone sync "./" "drive:openclaw-operativo-2026-backup/workspace-sync/" `
                    --ignore-size --inplace --update --fast-list `
                    --transfers 4 --checkers 8 `
                    --exclude "node_modules/**" `
                    --exclude ".git/**" `
                    --exclude "dist/**" `
                    --exclude ".cache/**"
                
                Write-Host "[AUTO-SYNC] Ciclo autónomo completado. Entorno blindado." -ForegroundColor Green
            } catch {
                Write-Host "[AUTO-SYNC ERROR] $_" -ForegroundColor Red
            } finally {
                Pop-Location
            }
        }
    }
}

# Limpiar suscripciones previas si existiesen
Get-EventSubscriber | Where-Object { $_.SourceIdentifier -in @("OpenClawFileChanged", "OpenClawFileCreated") } | Unregister-Event -Force

# Registrar los eventos de modificación y creación
Register-ObjectEvent -InputObject $Watcher -EventName "Changed" -SourceIdentifier "OpenClawFileChanged" -Action $Action | Out-Null
Register-ObjectEvent -InputObject $Watcher -EventName "Created" -SourceIdentifier "OpenClawFileCreated" -Action $Action | Out-Null

Write-Host "Watcher activo en segundo plano. Puedes trabajar libremente; el sistema se encarga del resto." -ForegroundColor Yellow

# Loop de mantenimiento
try {
    while ($true) {
        Start-Sleep -Seconds 60
    }
} finally {
    $Watcher.EnableRaisingEvents = $false
    $Watcher.Dispose()
    Get-EventSubscriber | Where-Object { $_.SourceIdentifier -in @("OpenClawFileChanged", "OpenClawFileCreated") } | Unregister-Event -Force
    Write-Host "`n[WATCHER] Demonio detenido limpiamente." -ForegroundColor Gray
}
