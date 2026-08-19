# audit-repos.ps1 - Auditoria de repos git
# Uso: powershell -ExecutionPolicy Bypass -File .\scripts\audit-repos.ps1
# Ejecutar cuando aparezcan cambios fantasma en VS Code Source Control

Write-Host "============================================================"
Write-Host " AUDITORIA DE REPOS GIT - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Write-Host "============================================================"

# REPOS CANONICOS (los unicos que deben existir activos)
$canonical = @{
    "https://github.com/ipanemausa/openclaw-operativo-2026"     = "c:\Users\ipane\openclaw-operativo-2026"
    "https://github.com/ipanemausa/openclaw-hb-jewelry.git"     = "c:\openclaw\hb-jewelry"
}

Write-Host ""
Write-Host "[CANONICOS - deben estar aqui y solo aqui]"
foreach ($remote in $canonical.Keys) {
    $path  = $canonical[$remote]
    $count = (git -C $path status --short 2>&1 | Measure-Object -Line).Lines
    $last  = git -C $path log --oneline -1 2>&1
    Write-Host "  [$count cambios] $path"
    Write-Host "  Ultimo commit: $last"
}

Write-Host ""
Write-Host "[SCAN - buscando repos duplicados o zombie en c:\Users\ipane]"

$found = Get-ChildItem -Path "c:\Users\ipane" -Recurse -Depth 5 -Directory -Filter ".git" `
    -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*\node_modules\*" } |
    Where-Object { $_.FullName -notlike "*\.git\modules*" } |
    ForEach-Object { $_.Parent.FullName }

$zombies = 0
foreach ($repo in $found) {
    $isCanonical = $false
    foreach ($v in $canonical.Values) { if ($repo -eq $v) { $isCanonical = $true } }

    if (-not $isCanonical) {
        $remote = git -C $repo remote get-url origin 2>&1
        $count  = (git -C $repo status --short 2>&1 | Measure-Object -Line).Lines
        $last   = git -C $repo log --oneline -1 2>&1
        $age    = (git -C $repo log -1 --format="%ar" 2>&1)
        Write-Host ""
        Write-Host "  [FUERA DE CANONICO] $repo"
        Write-Host "  Remote:  $remote"
        Write-Host "  Cambios: $count | Ultimo: $last ($age)"
        $zombies++
    }
}

Write-Host ""
if ($zombies -eq 0) {
    Write-Host "  OK - Ningun repo duplicado encontrado. Entorno limpio."
} else {
    Write-Host "  ATENCION: $zombies repos fuera de paths canonicos"
    Write-Host "  Para cada uno aplica el protocolo de 3 preguntas:"
    Write-Host "    1. Tiene commits en los ultimos 30 dias? (NO = eliminar .git)"
    Write-Host "    2. Tiene cambios utiles que no estan en el canonico? (NO = eliminar .git)"
    Write-Host "    3. Esta en un path logico para el proyecto? (NO = eliminar .git)"
}
Write-Host "============================================================"
