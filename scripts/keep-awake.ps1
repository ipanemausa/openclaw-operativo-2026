<#
.SYNOPSIS
    OpenClaw Keep-Awake — Previene que el PC se apague o hiberne durante procesos largos.
    Usa Windows SetThreadExecutionState API. No requiere permisos de administrador.
    
.USAGE
    # Iniciar (en background):
    Start-Job { powershell -ExecutionPolicy Bypass -File C:\Users\ipane\openclaw-operativo-2026\scripts\keep-awake.ps1 }
    
    # Detener:
    Get-Job | Where-Object { $_.Name -like "*keep*" } | Stop-Job

.NOTES
    Se auto-termina después de MaxHoras (default: 12h)
#>

param(
    [int]$MaxHoras = 12,
    [int]$IntervalSegundos = 60
)

# Cargar Windows API para control de energía
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class OpenClawPower {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);

    // Flags
    public const uint ES_CONTINUOUS       = 0x80000000;
    public const uint ES_SYSTEM_REQUIRED  = 0x00000001;  // Previene sleep del sistema
    public const uint ES_DISPLAY_REQUIRED = 0x00000002;  // Previene apagado de pantalla
    public const uint ES_AWAYMODE_REQUIRED = 0x00000040; // Previene Away Mode

    public static bool PreventSleep() {
        uint flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED;
        return SetThreadExecutionState(flags) != 0;
    }

    public static bool AllowSleep() {
        return SetThreadExecutionState(ES_CONTINUOUS) != 0;
    }
}
"@

$startTime  = Get-Date
$maxSeconds = $MaxHoras * 3600
$logFile    = "C:\Users\ipane\openclaw-operativo-2026\scripts\keep-awake.log"

function Write-Log($msg) {
    $ts = Get-Date -Format "HH:mm:ss"
    $line = "[$ts] $msg"
    Write-Host $line -ForegroundColor Cyan
    Add-Content $logFile $line
}

# Activar prevención de sleep
$ok = [OpenClawPower]::PreventSleep()
if ($ok) {
    Write-Log "✅ KEEP-AWAKE ACTIVO — PC bloqueado contra sleep/hibernate"
    Write-Log "   Duración máxima: $MaxHoras horas"
    Write-Log "   Intervalo heartbeat: $IntervalSegundos segundos"
} else {
    Write-Log "❌ Error activando keep-awake. Verificar permisos."
    exit 1
}

# Registrar en ANTIGRAVITY_WORK_LOG
Add-Content "C:\Users\ipane\openclaw-operativo-2026\ANTIGRAVITY_WORK_LOG.txt" "`n$(Get-Date -Format 'yyyy-MM-dd HH:mm') | KEEP-AWAKE INICIADO | MaxHoras=$MaxHoras"

# Loop de heartbeat — reafirma el estado cada IntervalSegundos
$iteration = 0
while ($true) {
    $elapsed = (Get-Date) - $startTime
    
    # Verificar tiempo máximo
    if ($elapsed.TotalSeconds -ge $maxSeconds) {
        Write-Log "⏰ Tiempo máximo alcanzado ($MaxHoras h). Liberando bloqueo."
        break
    }

    # Reafirmar prevención (Windows puede resetear después de un tiempo)
    [OpenClawPower]::PreventSleep() | Out-Null
    
    $iteration++
    $horasRestantes = [math]::Round(($maxSeconds - $elapsed.TotalSeconds) / 3600, 1)
    
    if ($iteration % 10 -eq 0) {  # Log cada 10 iteraciones
        Write-Log "💚 Heartbeat #$iteration — PC activo — Restante: ${horasRestantes}h"
        
        # Verificar si hay procesos críticos corriendo
        $dockerProcs = (docker ps --format "{{.Names}}" 2>$null | Measure-Object -Line).Lines
        $pythonProcs = (Get-Process python* -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Log "   Docker: $dockerProcs containers · Python: $pythonProcs procesos"
    }
    
    Start-Sleep -Seconds $IntervalSegundos
}

# Restaurar comportamiento normal
[OpenClawPower]::AllowSleep() | Out-Null
Write-Log "🔓 Keep-Awake terminado. Sleep permitido."
Add-Content "C:\Users\ipane\openclaw-operativo-2026\ANTIGRAVITY_WORK_LOG.txt" "$(Get-Date -Format 'yyyy-MM-dd HH:mm') | KEEP-AWAKE TERMINADO"
