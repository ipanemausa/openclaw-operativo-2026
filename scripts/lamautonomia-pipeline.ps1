param(
    [string]$Servicio = "all",
    [string]$Mensaje  = "auto: pipeline lamautonomia"
)
$ROOT = "C:\Users\ipane\openclaw-cloud-2026"
Set-Location $ROOT

# ── VALIDACION GEMINI KEY ──────────────────────────────────────
if (-not $env:GEMINI_API_KEY -or $env:GEMINI_API_KEY -match "TU_API|tu-key|placeholder") {
    Write-Host "  FAIL GEMINI_API_KEY no esta exportada en Windows" -ForegroundColor Red
    Write-Host "  Ejecuta: `$env:GEMINI_API_KEY='tu-key-real'" -ForegroundColor Yellow
    exit 1
}
Write-Host "  OK GEMINI_API_KEY validada" -ForegroundColor Green
# ──────────────────────────────────────────────────────────────

$errores = 0
function Log-OK   { param($msg) Write-Host "  OK $msg" -ForegroundColor Green }
function Log-FAIL { param($msg) Write-Host "  FAIL $msg" -ForegroundColor Red; $script:errores++ }
function Log-INFO { param($msg) Write-Host "  -> $msg" -ForegroundColor Cyan }

Write-Host "[1/5] BUILD" -ForegroundColor Yellow
if ($Servicio -eq "all") {
    docker compose up -d --build 2>&1 | Out-Null
} else {
    docker compose up -d --build --force-recreate $Servicio 2>&1 | Out-Null
}
if ($LASTEXITCODE -ne 0) { Log-FAIL "Build fallido"; exit 1 }
Log-OK "Build exitoso"

Write-Host "[2/5] CONTENEDORES" -ForegroundColor Yellow
Start-Sleep -Seconds 5
$running = docker compose ps --format "{{.Name}}|{{.State}}" 2>&1
$running -split "`n" | ForEach-Object {
    if ($_ -match "\|running") { Log-OK ($_ -split "\|")[0] }
    elseif ($_ -match "\|") { Log-FAIL ($_ -split "\|")[0] }
}
if ($errores -gt 0) { Write-Host "PIPELINE DETENIDO" -ForegroundColor Red; exit 1 }

Write-Host "[3/5] HEALTH CHECKS" -ForegroundColor Yellow
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

Write-Host "[4/5] ENDPOINTS" -ForegroundColor Yellow
try {
    $r = Invoke-RestMethod -Uri "http://localhost:8090/api/radio/input" -Method POST -ContentType "application/json" -Body '{"prompt":"pipeline-test","duration":8,"resolution":"1280x720","style":"cinematic"}' -TimeoutSec 10
    Log-OK "radio/input -> $($r.status)"
} catch {
    Log-FAIL "radio/input fallo"
}
if ($errores -gt 0) { Write-Host "PIPELINE DETENIDO" -ForegroundColor Red; exit 1 }

Write-Host "[5/5] COMMIT Y SYNC" -ForegroundColor Yellow
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

Write-Host "PIPELINE COMPLETO -- $errores errores" -ForegroundColor Green
docker compose ps