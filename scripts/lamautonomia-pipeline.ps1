Param(
    [string]$Servicio = "all",
    [string]$Mensaje = "accion-sin-descripcion"
)

Write-Output "=== LAMAUTONOMIA PIPELINE ==="
Write-Output "Servicio: $Servicio"
Write-Output "Mensaje: $Mensaje"

$logPath = Join-Path $PSScriptRoot "lamautonomia-log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logPath -Value "$timestamp | $Servicio | $Mensaje"

Write-Output "Registro completado en $logPath"
Write-Output "=============================="
