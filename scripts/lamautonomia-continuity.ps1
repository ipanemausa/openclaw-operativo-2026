# ============================================================
# LAMAUTONOMIA Continuity Script
# Actualiza el pipeline log con el estado en tiempo real
# 
# Uso:
#   .\scripts\lamautonomia-continuity.ps1 -Tarea "descripcion" -Estado "en-progreso"
#   .\scripts\lamautonomia-continuity.ps1 -Tarea "descripcion" -Estado "completado"
#   .\scripts\lamautonomia-continuity.ps1 -Tarea "descripcion" -Estado "bloqueado" -Handoff
# ============================================================

Param(
    [string]$Tarea     = "sin-descripcion",
    [string]$Estado    = "en-progreso",
    [string]$Pendiente = "",
    [string]$Completado = "",
    [switch]$Handoff
)

$timestamp   = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logFile     = Join-Path $PSScriptRoot "lamautonomia-log.txt"
$contextFile = Join-Path $PSScriptRoot "..\agents\lamautonomia\current_task.md"
$handoffFile = Join-Path $PSScriptRoot "..\agents\lamautonomia\HANDOFF.md"

Write-Output ""
Write-Output "============================================"
Write-Output "   LAMAUTONOMIA CONTINUITY UPDATE"
Write-Output "============================================"
Write-Output "Timestamp : $timestamp"
Write-Output "Tarea     : $Tarea"
Write-Output "Estado    : $Estado"
if ($Pendiente)  { Write-Output "Pendiente : $Pendiente" }
if ($Completado) { Write-Output "Completado: $Completado" }

# Registrar en el log principal
Add-Content -Path $logFile -Value "$timestamp | continuity | estado=$Estado | $Tarea"

if ($Completado) {
    Add-Content -Path $logFile -Value "$timestamp | completado | $Completado"
}
if ($Pendiente) {
    Add-Content -Path $logFile -Value "$timestamp | pendiente | $Pendiente"
}

# Si es handoff (Antigravity bloqueado), alertar
if ($Handoff) {
    Write-Output ""
    Write-Output "!!! MODO HANDOFF ACTIVADO !!!"
    Write-Output "    Antigravity esta bloqueado."
    Write-Output "    Sigue estos pasos:"
    Write-Output ""
    Write-Output "    1. Abre el archivo:"
    Write-Output "       $contextFile"
    Write-Output ""
    Write-Output "    2. Copia todo su contenido"
    Write-Output ""
    Write-Output "    3. Abre Copilot en Microsoft Edge"
    Write-Output ""
    Write-Output "    4. Pega el contenido y pide que retome la tarea"
    Write-Output ""
    Write-Output "    5. Cuando termines, registra con:"
    Write-Output "       .\scripts\lamautonomia-pipeline.ps1 -Servicio handoff -Mensaje 'Copilot retomo: descripcion'"
    Write-Output ""
    Add-Content -Path $logFile -Value "$timestamp | HANDOFF-ACTIVADO | Antigravity bloqueado en: $Tarea"
}

Write-Output ""
Write-Output "Log actualizado: $logFile"
Write-Output "============================================"
Write-Output ""
