# ============================================================
# OPENCLAW 2026 - GitHub Token Setup via gh CLI (sin sudo)
# Ejecutar desde PowerShell en: openclaw-operativo-2026
# ============================================================

$MASTER_ENV = "C:\Users\ipane\.openclaw-master.env"

Write-Host "`n[1/4] Verificando gh CLI..." -ForegroundColor Cyan
try {
    $ghVersion = & gh --version 2>&1 | Select-Object -First 1
    Write-Host "  OK: $ghVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: gh CLI no encontrado. Instalar con: winget install GitHub.cli" -ForegroundColor Red
    exit 1
}

Write-Host "`n[2/4] Autenticando con GitHub (browser - una sola vez)..." -ForegroundColor Cyan
$authStatus = & gh auth status 2>&1
if ($authStatus -match "Logged in to github.com") {
    Write-Host "  Ya autenticado: $($authStatus | Select-String 'account')" -ForegroundColor Green
} else {
    Write-Host "  Iniciando login..." -ForegroundColor Yellow
    & gh auth login --hostname github.com --git-protocol https --web
}

Write-Host "`n[3/4] Obteniendo token..." -ForegroundColor Cyan
$token = & gh auth token 2>&1
if ($token -match "^gh[ps]_" -or $token -match "^github_pat_") {
    Write-Host "  Token obtenido: $($token.Substring(0,12))..." -ForegroundColor Green

    Write-Host "`n[4/4] Escribiendo en master env..." -ForegroundColor Cyan
    $content = Get-Content $MASTER_ENV -Raw -Encoding UTF8

    if ($content -match "GITHUB_TOKEN=") {
        # Reemplazar linea existente
        $content = $content -replace "GITHUB_TOKEN=.*", "GITHUB_TOKEN=$token"
    } else {
        # Agregar al final
        $content += "`n# --- GITHUB PAT (generado via gh CLI) ---`nGITHUB_TOKEN=$token`n"
    }
    Set-Content $MASTER_ENV $content -Encoding UTF8
    Write-Host "  Escrito en: $MASTER_ENV" -ForegroundColor Green

    # Tambien actualizar .env del repo (sin commitear - esta en .gitignore)
    $repoEnv = "C:\Users\ipane\openclaw-operativo-2026\.env"
    $repoContent = Get-Content $repoEnv -Raw -Encoding UTF8
    $repoContent = $repoContent -replace "GITHUB_TOKEN=.*", "GITHUB_TOKEN=$token"
    Set-Content $repoEnv $repoContent -Encoding UTF8
    Write-Host "  Tambien actualizado: .env (local, en .gitignore)" -ForegroundColor Green

    Write-Host "`n✅ LISTO. Reiniciar MCP servers en Antigravity (Ctrl+Shift+P > Restart MCP Servers)" -ForegroundColor Green
    Write-Host "   Token: $($token.Substring(0,15))..." -ForegroundColor DarkGray

} else {
    Write-Host "  ERROR obteniendo token: $token" -ForegroundColor Red
    Write-Host "  Ejecutar manualmente: gh auth token" -ForegroundColor Yellow
}
