Param(
    [string]$Servicio = "all",
    [string]$Mensaje = "accion-sin-descripcion"
)

Write-Output "=== LAMAUTONOMIA PIPELINE ==="
Write-Output "Servicio: $Servicio"
Write-Output "Mensaje: $Mensaje"

# Log local (fallback — siempre funciona)
$logPath = Join-Path $PSScriptRoot "lamautonomia-log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logPath -Value "$timestamp | $Servicio | $Mensaje"
Write-Output "Log local: OK"

# Registro en ECC (si orchestrator esta corriendo)
try {
    $body = @{
        actor  = "lamautonomia-pipeline"
        action = $Mensaje
        task   = $Servicio
        gate   = "none"
    } | ConvertTo-Json
    $null = Invoke-RestMethod -Uri "http://localhost:8090/api/ecc/action" -Method POST -ContentType "application/json" -Body $body -TimeoutSec 3
    Write-Output "ECC: OK"
} catch {
    Write-Output "ECC: offline (log local guardado)"
}

Write-Output "=============================="

