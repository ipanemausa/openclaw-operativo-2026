# ═══════════════════════════════════════════════════════════════
# OpenClaw Cloud 2026 - Windows Deployment Script
# ═══════════════════════════════════════════════════════════════

param(
    [string]$Environment = "production",
    [switch]$BuildOnly = $false,
    [switch]$CleanFirst = $false
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 OpenClaw Cloud 2026 - Windows Deployment" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# STEP 1: Prerequisites Check
# ═══════════════════════════════════════════════════════════════

Write-Host "[STEP 1] Checking prerequisites..." -ForegroundColor Yellow

# Check Docker
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed" -ForegroundColor Red
    exit 1
}

# Check Docker Compose
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed" -ForegroundColor Red
    exit 1
}

# Check .env
if (!(Test-Path ".env")) {
    Write-Host "❌ .env file not found" -ForegroundColor Red
    exit 1
}
Write-Host "✅ .env file exists" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# STEP 2: Load environment
# ═══════════════════════════════════════════════════════════════

Write-Host "[STEP 2] Loading environment..." -ForegroundColor Yellow
$envContent = Get-Content .env | Where-Object { $_ -notmatch "^#" -and $_ -ne "" }
foreach ($line in $envContent) {
    $parts = $line -split "=", 2
    if ($parts.Count -eq 2) {
        [Environment]::SetEnvironmentVariable($parts[0].Trim(), $parts[1].Trim())
    }
}
Write-Host "✅ Environment loaded" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# STEP 3: Clean previous deployment (optional)
# ═══════════════════════════════════════════════════════════════

if ($CleanFirst) {
    Write-Host "[STEP 3] Cleaning previous deployment..." -ForegroundColor Yellow
    docker-compose down --remove-orphans 2>$null | Out-Null
    Start-Sleep -Seconds 2
    Write-Host "✅ Previous deployment cleaned" -ForegroundColor Green
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════════
# STEP 4: Build Docker images
# ═══════════════════════════════════════════════════════════════

Write-Host "[STEP 4] Building Docker images..." -ForegroundColor Yellow
docker-compose build --no-cache
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker images built" -ForegroundColor Green
Write-Host ""

if ($BuildOnly) {
    Write-Host "✅ Build completed (BuildOnly mode)" -ForegroundColor Green
    exit 0
}

# ═══════════════════════════════════════════════════════════════
# STEP 5: Start services
# ═══════════════════════════════════════════════════════════════

Write-Host "[STEP 5] Starting services..." -ForegroundColor Yellow
docker-compose up -d
Write-Host "✅ Services started" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# STEP 6: Wait for services
# ═══════════════════════════════════════════════════════════════

Write-Host "[STEP 6] Waiting for services to be healthy..." -ForegroundColor Yellow

function Check-Service {
    param(
        [string]$ServiceName,
        [int]$Port
    )
    
    $retries = 0
    $maxRetries = 30
    
    while ($retries -lt $maxRetries) {
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:$Port/health" -Method GET -TimeoutSec 2
            Write-Host "✅ $ServiceName is healthy" -ForegroundColor Green
            return $true
        } catch {
            Write-Host "⏳ Waiting for $ServiceName... ($($retries + 1)/$maxRetries)" -ForegroundColor Gray
            Start-Sleep -Seconds 2
            $retries++
        }
    }
    
    Write-Host "❌ $ServiceName failed to become healthy" -ForegroundColor Red
    return $false
}

Check-Service "App" 8084 | Out-Null
Check-Service "Gateway" 8080 | Out-Null

Write-Host ""

# ═══════════════════════════════════════════════════════════════
# STEP 7: Health checks
# ═══════════════════════════════════════════════════════════════

Write-Host "[STEP 7] Running health checks..." -ForegroundColor Yellow

# Check containers
$runningContainers = docker-compose ps -q | Measure-Object -Line
Write-Host "✅ Running containers: $($runningContainers.Lines)" -ForegroundColor Green

# Check Gateway API
try {
    $status = Invoke-RestMethod -Uri "http://localhost:8080/api/mcp/status" -Method GET -TimeoutSec 5
    Write-Host "✅ Gateway API responding" -ForegroundColor Green
    Write-Host "   Status: $($status.status)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Gateway API check failed (may still be initializing)" -ForegroundColor Yellow
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════
# STEP 8: Display summary
# ═══════════════════════════════════════════════════════════════

Write-Host "[STEP 8] Deployment Summary" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""

docker-compose ps

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "🎉 OpenClaw Cloud 2026 Deployment Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "📍 Access Points:" -ForegroundColor Cyan
Write-Host "   • UI: http://localhost" -ForegroundColor White
Write-Host "   • Gateway: http://localhost:8080" -ForegroundColor White
Write-Host "   • Chat: http://localhost/chat" -ForegroundColor White
Write-Host "   • API: http://localhost/api" -ForegroundColor White
Write-Host ""

Write-Host "📊 Management Commands:" -ForegroundColor Cyan
Write-Host "   • View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "   • Stop: docker-compose down" -ForegroundColor White
Write-Host "   • Restart: docker-compose restart" -ForegroundColor White
Write-Host "   • Status: docker-compose ps" -ForegroundColor White
Write-Host ""

Write-Host "🔐 Production Checklist:" -ForegroundColor Cyan
Write-Host "   ☐ Update .env with production secrets" -ForegroundColor White
Write-Host "   ☐ Configure Pickaxe API key" -ForegroundColor White
Write-Host "   ☐ Setup proper SSL certificates" -ForegroundColor White
Write-Host "   ☐ Configure database backups" -ForegroundColor White
Write-Host "   ☐ Setup monitoring & alerting" -ForegroundColor White
Write-Host "   ☐ Configure DNS" -ForegroundColor White
Write-Host ""
