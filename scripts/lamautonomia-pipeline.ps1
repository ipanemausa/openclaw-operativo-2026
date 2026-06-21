# ═══════════════════════════════════════════════════════════════
# LAMAUTONOMIA — PIPELINE CI/CD LOCAL v1.0
# Uso: .\scripts\lamautonomia-pipeline.ps1 -Servicio "claw-orchestrator"
# ═══════════════════════════════════════════════════════════════

param(
    [string]$Servicio = "all",
    [string]$Mensaje  = "auto: pipeline lamautonomia"
)

$ROOT = "C:\Users\ipane\openclaw-cloud-2026"
Set-Location $ROOT

$errores = 0
function Log-OK   { param($msg) Write-Host "  OK $msg" -ForegroundColor Green }
function Log-FAIL { param($msg) Write-Host "  FAIL $msg" -ForegroundColor Red; $script:errores++ }
function Log-INFO { param($msg) Write-Host "  -> $msg" -ForegroundColor Cyan }

# PASO 1 — BUILD
Write-Host "`n[1/5] BUILD" -ForegroundColor Yellow
if ($Servicio -eq "all") {
    docker compose up -d --build 2>&1 | Out-Null
} else {
    docker compose up -d --build --force-recreate $Servicio 2>&1 | Out-Null
}
if ($LASTEXITCODE -ne 0) { Log-FAIL "Build fallido"; exit 1 }
Log-OK "Build exitoso"

# PASO 2 — CONTENEDORES
Write-Host "`n[2/5] CONTENEDORES" -ForegroundColor Yellow
Start-Sleep -Seconds 5
$running = docker compose ps --format "{{.Name}}|{{.State}}" 2>&1
$running -split "`n" | ForEach-Object {
    if ($_ -match "\|running") { Log-OK ($_ -split "\|")[0] }
    elseif ($_ -match "\|") { Log-FAIL ($_ -split "\|")[0]; $errores++ }
}
if ($errores -gt 0) { Write-Host "PIPELINE DETENIDO" -ForegroundColor Red; exit 1 }

# PASO 3 — HEALTH CHECKS
Write-Host "`n[3/5] HEALTH CHECKS" -ForegroundColor Yellow
$checks = @{
    "claw-orchestrator" = "http://localhost:8090/health"
    "openclaw_app"      = "http://localhost:3000/healthz"
}
foreach ($svc in $checks.Keys) {
    if ($Servicio -ne "all" -and $Servicio -ne $svc) { continue }
    try {
        $r = Invoke-RestMethod -Uri $checks[$svc] -TimeoutSec 5
        Log-OK "$svc -> $($r.status)"
    } catch {
        Log-FAIL "$svc sin respuesta"
        docker logs $svc --tail 10
    }
}
if ($errores -gt 0) { Write-Host "PIPELINE DETENIDO" -ForegroundColor Red; exit 1 }

# PASO 4 — ENDPOINT CRITICO
Write-Host "`n[4/5] ENDPOINTS" -ForegroundColor Yellow
try {
    $r = Invoke-RestMethod -Uri "http://localhost:8090/api/radio/input" -Method POST -ContentType "application/json" -Body '{"prompt":"pipeline-test","duration":5,"resolution":"1280x720","style":"cinematic"}' -TimeoutSec 10
    Log-OK "radio/input -> $($r.status)"
} catch {
    Log-FAIL "radio/input fallo"
}
if ($errores -gt 0) { Write-Host "PIPELINE DETENIDO" -ForegroundColor Red; exit 1 }

# PASO 5 — COMMIT Y PUSH
Write-Host "`n[5/5] COMMIT Y SYNC" -ForegroundColor Yellow
git add -A
$changes = git diff --cached --name-only
if (-not $changes) {
    Log-INFO "Sin cambios para commitear"
} else {
    git commit -m $Mensaje
    git stash
    git pull origin main --rebase
    git stash pop
    git push origin main
    Log-OK "Push a GitHub OK"
}

Write-Host "`n===============================================" -ForegroundColor Green
Write-Host "PIPELINE COMPLETO — $errores errores" -ForegroundColor Green
docker compose ps
Write-Host "===============================================" -ForegroundColor Green