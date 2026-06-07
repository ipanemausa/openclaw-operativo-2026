#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# OpenClaw Cloud 2026 - Deployment Script
# ═══════════════════════════════════════════════════════════════

set -e

echo "🚀 OpenClaw Cloud 2026 - Deployment Script"
echo "==========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════
# STEP 1: Prerequisites Check
# ═══════════════════════════════════════════════════════════════

echo -e "${YELLOW}[STEP 1] Checking prerequisites...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker is installed$(docker --version)${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker Compose is installed$(docker-compose --version)${NC}"

# Check .env file
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env file not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ .env file exists${NC}"

echo ""

# ═══════════════════════════════════════════════════════════════
# STEP 2: Load environment variables
# ═══════════════════════════════════════════════════════════════

echo -e "${YELLOW}[STEP 2] Loading environment...${NC}"
source .env
echo -e "${GREEN}✅ Environment loaded${NC}"

echo ""

# ═══════════════════════════════════════════════════════════════
# STEP 3: Clean previous deployment
# ═══════════════════════════════════════════════════════════════

echo -e "${YELLOW}[STEP 3] Cleaning previous deployment...${NC}"
docker-compose down --remove-orphans || true
sleep 2
echo -e "${GREEN}✅ Previous deployment cleaned${NC}"

echo ""

# ═══════════════════════════════════════════════════════════════
# STEP 4: Create SSL certificates (if not exist)
# ═══════════════════════════════════════════════════════════════

echo -e "${YELLOW}[STEP 4] Checking SSL certificates...${NC}"

if [ ! -f nginx/ssl/openclaw.crt ] || [ ! -f nginx/ssl/openclaw.key ]; then
    echo "Generating self-signed certificates..."
    mkdir -p nginx/ssl
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx/ssl/openclaw.key \
        -out nginx/ssl/openclaw.crt \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=openclaw.local"
    echo -e "${GREEN}✅ Self-signed certificates generated${NC}"
else
    echo -e "${GREEN}✅ SSL certificates exist${NC}"
fi

echo ""

# ═══════════════════════════════════════════════════════════════
# STEP 5: Build Docker images
# ═══════════════════════════════════════════════════════════════

echo -e "${YELLOW}[STEP 5] Building Docker images...${NC}"
docker-compose build --no-cache
echo -e "${GREEN}✅ Docker images built${NC}"

echo ""

# ═══════════════════════════════════════════════════════════════
# STEP 6: Start services
# ═══════════════════════════════════════════════════════════════

echo -e "${YELLOW}[STEP 6] Starting services...${NC}"
docker-compose up -d
echo -e "${GREEN}✅ Services started${NC}"

echo ""

# ═══════════════════════════════════════════════════════════════
# STEP 7: Wait for services to be healthy
# ═══════════════════════════════════════════════════════════════

echo -e "${YELLOW}[STEP 7] Waiting for services to be healthy...${NC}"

# Function to check service health
check_service() {
    local service=$1
    local port=$2
    local retries=0
    local max_retries=30
    
    while [ $retries -lt $max_retries ]; do
        if curl -f http://localhost:$port/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $service is healthy${NC}"
            return 0
        fi
        echo "Waiting for $service... ($((retries + 1))/$max_retries)"
        sleep 2
        retries=$((retries + 1))
    done
    
    echo -e "${RED}❌ $service failed to become healthy${NC}"
    return 1
}

check_service "App" 8084
check_service "Gateway" 8080

echo ""

# ═══════════════════════════════════════════════════════════════
# STEP 8: Run health checks
# ═══════════════════════════════════════════════════════════════

echo -e "${YELLOW}[STEP 8] Running comprehensive health checks...${NC}"

# Database
echo "Checking Database..."
if docker-compose exec -T db psql -U $DB_USER -d $DB_NAME -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Database is operational${NC}"
else
    echo -e "${RED}❌ Database check failed${NC}"
fi

# Redis
echo "Checking Redis..."
if docker-compose exec -T redis redis-cli ping | grep -q PONG; then
    echo -e "${GREEN}✅ Redis is operational${NC}"
else
    echo -e "${RED}❌ Redis check failed${NC}"
fi

# Qdrant
echo "Checking Qdrant..."
if curl -f http://localhost:6333/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Qdrant is operational${NC}"
else
    echo -e "${RED}❌ Qdrant check failed${NC}"
fi

# Gateway API
echo "Checking Gateway API..."
if curl -f http://localhost:8080/api/mcp/status > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Gateway API is operational${NC}"
else
    echo -e "${RED}❌ Gateway API check failed${NC}"
fi

echo ""

# ═══════════════════════════════════════════════════════════════
# STEP 9: Display deployment summary
# ═══════════════════════════════════════════════════════════════

echo -e "${YELLOW}[STEP 9] Deployment Summary${NC}"
echo "==========================================="
echo ""

docker-compose ps

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo -e "${GREEN}🎉 OpenClaw Cloud 2026 Deployment Complete!${NC}"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📍 Access Points:"
echo "   • UI: http://localhost"
echo "   • Gateway: http://localhost:8080"
echo "   • Chat: http://localhost/chat"
echo "   • API: http://localhost/api"
echo ""
echo "📊 Management:"
echo "   • View logs: docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Restart services: docker-compose restart"
echo ""
echo "🔐 Important:"
echo "   • Update .env with production secrets"
echo "   • Configure Pickaxe API key"
echo "   • Setup proper SSL certificates"
echo "   • Configure database backups"
echo ""
