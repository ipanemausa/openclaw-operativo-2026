# ============================================================
# ECC Check — Estado Cognitivo Centralizado
# Uso:
#   .\scripts\ecc-check.ps1              → Muestra estado actual
#   .\scripts\ecc-check.ps1 -Validate    → Fuerza validacion
#   .\scripts\ecc-check.ps1 -Audit       → Muestra ultimas acciones
#   .\scripts\ecc-check.ps1 -Drift       → Detecta drift
# ============================================================

Param(
    [switch]$Validate = $false,
    [switch]$Audit    = $false,
    [switch]$Drift    = $false,
    [string]$Host     = "localhost",
    [int]$Port        = 8090
)

$BASE = "http://${Host}:${Port}"

function Show-Header {
    Write-Host ""
    Write-Host "════════════════════════════════════════" -ForegroundColor DarkYellow
    Write-Host "  ECC — Estado Cognitivo Centralizado" -ForegroundColor Yellow
    Write-Host "════════════════════════════════════════" -ForegroundColor DarkYellow
    Write-Host ""
}

function Get-ECCState {
    try {
        $response = Invoke-RestMethod -Uri "$BASE/api/ecc/state" -Method GET -TimeoutSec 5
        $ecc = $response.ecc
        Write-Host "  Version        : $($ecc.version)" -ForegroundColor Cyan
        Write-Host "  Timestamp      : $($ecc.timestamp)" -ForegroundColor White
        Write-Host "  System Stable  : $($ecc.system_stable)" -ForegroundColor $(if ($ecc.system_stable -eq "true") { "Green" } else { "Red" })
        Write-Host "  Last Actor     : $($ecc.last_actor)" -ForegroundColor White
        Write-Host "  Last Action    : $($ecc.last_action)" -ForegroundColor White
        Write-Host "  Validated      : $($ecc.last_action_validated)" -ForegroundColor White
        Write-Host "  Active Task    : $(if ($ecc.active_task) { $ecc.active_task } else { '(none)' })" -ForegroundColor $(if ($ecc.active_task) { "Yellow" } else { "Green" })
        Write-Host "  Locked By      : $(if ($ecc.active_task_locked_by) { $ecc.active_task_locked_by } else { '(none)' })" -ForegroundColor White
        Write-Host "  Pending Commit : $($ecc.pending_commit)" -ForegroundColor $(if ($ecc.pending_commit -eq "true") { "Yellow" } else { "Green" })
        Write-Host "  Pending Sync   : $($ecc.pending_sync)" -ForegroundColor $(if ($ecc.pending_sync -eq "true") { "Yellow" } else { "Green" })
        Write-Host "  Docker Healthy : $($ecc.docker_healthy)" -ForegroundColor $(if ($ecc.docker_healthy -eq "true") { "Green" } else { "Red" })
        Write-Host "  Drift Detected : $($ecc.drift_detected)" -ForegroundColor $(if ($ecc.drift_detected -eq "true") { "Red" } else { "Green" })
    } catch {
        Write-Host "  ERROR: No se pudo conectar a $BASE/api/ecc/state" -ForegroundColor Red
        Write-Host "  Asegurate que claw-orchestrator esta corriendo y tiene ECC habilitado" -ForegroundColor Yellow
    }
}

function Invoke-Validate {
    try {
        Write-Host "  Ejecutando validacion..." -ForegroundColor Yellow
        $response = Invoke-RestMethod -Uri "$BASE/api/ecc/validate" -Method POST -ContentType "application/json" -Body "{}" -TimeoutSec 10
        if ($response.stable) {
            Write-Host "  RESULTADO: Sistema ESTABLE" -ForegroundColor Green
        } else {
            Write-Host "  RESULTADO: DRIFT DETECTADO" -ForegroundColor Red
            foreach ($issue in $response.issues) {
                Write-Host "    - $issue" -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "  ERROR: No se pudo ejecutar validacion" -ForegroundColor Red
    }
}

function Get-Audit {
    try {
        $response = Invoke-RestMethod -Uri "$BASE/api/ecc/audit?count=10" -Method GET -TimeoutSec 5
        Write-Host "  Ultimas $($response.count) acciones:" -ForegroundColor Cyan
        Write-Host ""
        foreach ($entry in $response.audit) {
            $color = if ($entry.result -eq "success" -or $entry.result -eq "allowed" -or $entry.result -eq "stable") { "Green" } elseif ($entry.result -eq "failed" -or $entry.result -eq "drift_detected") { "Red" } else { "White" }
            Write-Host "    [$($entry.timestamp)] $($entry.actor) → $($entry.action) | $($entry.task) | $($entry.result)" -ForegroundColor $color
        }
    } catch {
        Write-Host "  ERROR: No se pudo obtener audit log" -ForegroundColor Red
    }
}

function Get-Drift {
    try {
        $response = Invoke-RestMethod -Uri "$BASE/api/ecc/drift" -Method GET -TimeoutSec 10
        if ($response.drift_detected) {
            Write-Host "  DRIFT DETECTADO:" -ForegroundColor Red
            foreach ($issue in $response.issues) {
                Write-Host "    - $issue" -ForegroundColor Yellow
            }
        } else {
            Write-Host "  Sin drift — sistema coherente" -ForegroundColor Green
        }
        Write-Host "  Checked at: $($response.checked_at)" -ForegroundColor White
    } catch {
        Write-Host "  ERROR: No se pudo verificar drift" -ForegroundColor Red
    }
}

# ── Main ──
Show-Header

if ($Validate) {
    Invoke-Validate
    Write-Host ""
} elseif ($Audit) {
    Get-Audit
} elseif ($Drift) {
    Get-Drift
} else {
    Get-ECCState
}

Write-Host ""
Write-Host "════════════════════════════════════════" -ForegroundColor DarkYellow
Write-Host ""
