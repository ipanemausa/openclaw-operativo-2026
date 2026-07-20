# 🚀 OpenClaw Cloud 2026 - Complete Deployment Package

**Production-ready OpenClaw deployment with Docker Compose, Pickaxe LLM integration, and PRO UI.**

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Infrastructure](#infrastructure)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Access Points](#access-points)
- [Production Setup](#production-setup)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Linux/macOS
```bash
# Clone/copy the project
cd openclaw-cloud-2026

# Update environment variables
nano .env  # Set PICKAXE_API_KEY and other secrets

# Deploy
chmod +x scripts/deploy-cloud.sh
./scripts/deploy-cloud.sh
```

### Windows (PowerShell)
```powershell
# Navigate to project
cd openclaw-cloud-2026

# Update environment
notepad .env  # Set PICKAXE_API_KEY and secrets

# Deploy
.\scripts\deploy-cloud.ps1
```

### Docker Compose (Any OS)
```bash
# Build and start
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🏗️ Architecture (Updated: Edge Computing + RAG)

```mermaid
graph TD
    %% NGINX Router
    NGINX["NGINX (Reverse Proxy)<br/>Ports 80/443"]
    
    %% Frontend Edge
    subgraph Frontend Edge
        UI["UI PRO (React/Vite)<br/>Port 80"]
        AvatarEdge["Edge Computing<br/>(Mathematical Lip-sync / AudioContext)"]
        UI --- AvatarEdge
    end
    
    %% Backend Services
    subgraph Docker Internal Network
        Gateway["Gateway (Python)<br/>Port 8080"]
        VoiceWorker["Voice Worker<br/>(Gemini Live Translator)"]
        RagWorker["Financial RAG Worker<br/>(Port 8093)"]
        ChatWorker["Chat Worker<br/>(DeepSeek)"]
        App["App Core<br/>Port 5000"]
    end
    
    %% Data Layer
    subgraph Data & State
        Qdrant[("Qdrant<br/>(Vector DB - 6333)")]
        Redis[("Redis<br/>(Cache - 6379)")]
        Postgres[("PostgreSQL<br/>(Relational - 5432)")]
    end
    
    %% Routing
    NGINX -->|/| UI
    NGINX -->|/ws/voice| VoiceWorker
    NGINX -->|/api/rag| RagWorker
    NGINX -->|/api/chat| ChatWorker
    NGINX -->|/api/*| Gateway
    
    %% Internal Logic
    Gateway --> App
    RagWorker -->|Embeddings| Qdrant
    ChatWorker --> Redis
    App --> Postgres
    App --> Redis
    
    %% Edge Stream
    VoiceWorker -.->|Binary Audio Stream (0-Latency)| AvatarEdge
    
    classDef proxy fill:#f9f,stroke:#333,stroke-width:2px;
    classDef frontend fill:#bbf,stroke:#333,stroke-width:2px;
    classDef edge fill:#dfd,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;
    classDef db fill:#fdb,stroke:#333,stroke-width:2px;
    
    class NGINX proxy;
    class UI frontend;
    class AvatarEdge edge;
    class Qdrant,Redis,Postgres db;
```


---

## 🔧 Infrastructure Components

### Database (PostgreSQL 15)
- **Container:** `openclaw_db`
- **Port:** 5432 (internal)
- **Volume:** `db_data`
- **Init Script:** `db/init.sql`
- **Features:** UUID extensions, JSONB support, full-text search

### Cache (Redis 7)
- **Container:** `openclaw_redis`
- **Port:** 6379 (internal)
- **Volume:** `redis_data`
- **Auth:** Password protected
- **Use:** Session cache, message queue, rate limiting

### Vector Store (Qdrant)
- **Container:** `openclaw_qdrant`
- **Port:** 6333 (internal)
- **Volume:** `qdrant_data`
- **Use:** Embeddings, RAG, semantic search

### Main App (Flask + Gunicorn)
- **Container:** `openclaw_app`
- **Port:** 8084 (external), 5000 (internal)
- **LLM Provider:** Pickaxe (configurable)
- **Features:** REST API, WebSocket support

### Gateway (Router + Auth)
- **Container:** `openclaw_gateway`
- **Port:** 8080 (external)
- **Features:** Request routing, rate limiting, token validation

### Specialized Agents
- **video_agent** → Port 8085 (video processing)
- **marketing_generator** → Port 8086 (copy generation + RAG)
- **shopify_integration** → Port 8087 (e-commerce sync)
- **slack_bot** → Port 3000 (Slack ChatOps)

### Reverse Proxy (Nginx)
- **Port:** 80 (HTTP), 443 (HTTPS)
- **Static Files:** React UI PRO
- **Features:** SSL/TLS, rate limiting, compression, security headers

---

## ⚙️ Configuration

### Environment Variables (.env)

**Required:**
```bash
PICKAXE_API_KEY=pk-your-actual-key        # Main LLM provider
DB_PASSWORD=your-secure-db-password        # Database
REDIS_PASSWORD=your-redis-password         # Redis
SECRET_KEY=your-very-secret-key           # Flask secret
```

**Optional but Recommended:**
```bash
GEMINI_API_KEY=optional-gemini-key        # Secondary LLM
SHOPIFY_STORE_URL=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your-token
SLACK_BOT_TOKEN=xoxb-token
SLACK_APP_TOKEN=xapp-token
```

See `.env` file for complete list.

### Pickaxe LLM Configuration

The app uses **Pickaxe as the primary LLM provider**:

```python
# app.py (auto-configured)
PICKAXE_API_KEY = os.getenv('PICKAXE_API_KEY')
PICKAXE_MODEL = os.getenv('PICKAXE_MODEL', 'pickaxe-7b-instruct')
```

**Features:**
- Default fallback to Pickaxe if Gemini is unavailable
- Token-based authentication
- Configurable model and parameters
- Timeout protection (60s default)

### Gateway Configuration

```python
# gateway.py (auto-configured)
- Rate limiting: 10 req/s API, 5 req/s chat
- Token validation on protected endpoints
- Request/response logging
- Health check endpoint: /health
```

---

## 🚀 Deployment

### Option 1: Automatic Deployment Script

**Linux/macOS:**
```bash
chmod +x scripts/deploy-cloud.sh
./scripts/deploy-cloud.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\deploy-cloud.ps1
```

Script does:
1. ✅ Prerequisites check
2. ✅ Environment loading
3. ✅ Previous deployment cleanup
4. ✅ SSL certificate generation
5. ✅ Docker image build
6. ✅ Service startup
7. ✅ Health checks
8. ✅ Summary display

### Option 2: Manual Docker Compose

```bash
# Build
docker-compose build --no-cache

# Start
docker-compose up -d

# Watch logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option 3: Cloud Providers

#### AWS ECS
```bash
# Install AWS CLI and configure credentials
aws configure

# Use docker-compose.yml with ECS CLI
ecs-cli compose --file docker-compose.yml service up
```

#### Google Cloud Run
```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/openclaw
gcloud run deploy openclaw --image gcr.io/PROJECT_ID/openclaw
```

#### DigitalOcean App Platform
```bash
# Use .do/app.yaml configuration
doctl apps create --spec .do/app.yaml
```

#### Azure Container Instances
```bash
# Deploy using docker-compose
docker-compose --file docker-compose.yml config | \
  az container create --resource-group openclaw --file -
```

---

## 🌐 Access Points

After deployment:

| Service | URL | Port | Purpose |
|---------|-----|------|---------|
| UI PRO | `http://localhost` | 80 | React frontend |
| Gateway | `http://localhost:8080` | 8080 | API gateway |
| Chat | `http://localhost/chat` | 80 | Chat interface |
| API | `http://localhost/api` | 80 | REST API |
| App Direct | `http://localhost:8084` | 8084 | Direct app access |
| Database | `localhost:5432` | 5432 | PostgreSQL |
| Redis | `localhost:6379` | 6379 | Cache |
| Qdrant | `http://localhost:6333` | 6333 | Vector DB |

**Example API Call:**
```bash
curl -X POST http://localhost:8080/api/mcp/message \
  -H "Content-Type: application/json" \
  -d '{"agent":"main","message":"Hello OpenClaw"}'
```

---

## 🔒 Production Setup

### 1. Update Secrets (.env)

```bash
# Database
DB_PASSWORD=$(openssl rand -base64 32)

# Redis
REDIS_PASSWORD=$(openssl rand -base64 32)

# Flask
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# Save these securely (AWS Secrets Manager, Vault, etc.)
```

### 2. SSL/TLS Certificates

**Option A: Let's Encrypt (Recommended)**
```bash
certbot certonly --standalone -d your-domain.com
cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/openclaw.crt
cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/openclaw.key
```

**Option B: Self-signed (Testing)**
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/openclaw.key \
  -out nginx/ssl/openclaw.crt
```

### 3. Database Backups

```bash
# Daily backup script
docker-compose exec db pg_dump -U openclaw_admin openclaw_prod > backup-$(date +%Y%m%d).sql

# Or use volume snapshots (AWS, GCP, Azure)
```

### 4. Monitoring & Logging

```bash
# View logs
docker-compose logs -f

# Export logs to file
docker-compose logs > openclaw-logs-$(date +%Y%m%d).log

# Use external logging (DataDog, New Relic, etc.)
```

### 5. Resource Limits

Update `docker-compose.yml` with resource constraints:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

---

## 🔧 Troubleshooting

### Service won't start

```bash
# Check logs
docker-compose logs -f openclaw_app

# Common issues:
# - Port already in use
# - Missing .env variables
# - Insufficient disk space
# - Database connection timeout
```

### Gateway returning 502 (Bad Gateway)

```bash
# Check if app is healthy
docker-compose logs openclaw_app

# Restart app service
docker-compose restart openclaw_app

# Check database connection
docker-compose exec db psql -U openclaw_admin -d openclaw_prod -c "SELECT 1;"
```

### Out of memory

```bash
# Check Docker stats
docker stats

# Reduce worker count in compose
GATEWAY_WORKERS=2 docker-compose up -d

# Increase system memory or add swap
```

### Database migration issues

```bash
# Reset database (WARNING: loses data)
docker-compose down -v
docker-compose up -d

# Or restore from backup
docker-compose exec db psql -U openclaw_admin openclaw_prod < backup.sql
```

---

## 📊 Health Checks

```bash
# Gateway
curl http://localhost:8080/health

# App
curl http://localhost:8084/healthz

# MCP Status
curl http://localhost:8080/api/mcp/status

# Chat test
curl -X POST http://localhost:8080/api/mcp/message \
  -H "Content-Type: application/json" \
  -d '{"agent":"main","message":"test"}'
```

---

## 📚 Documentation

- `docs/openclaw-governance.md` - System governance
- `docs/PHASE_DEFINITIONS.md` - Pipeline phases
- `docs/ROLLBACK_PROCEDURE.md` - How to rollback
- `docs/ENV_MANAGEMENT.md` - Environment variables

---

## 🤝 Support

For issues, check:
1. Logs: `docker-compose logs -f`
2. Health endpoints: `/health`, `/healthz`
3. MCP Status: `/api/mcp/status`
4. Database: `docker-compose exec db psql -U openclaw_admin -d openclaw_prod`

---

## 📄 License

OpenClaw 2026 - Production deployment package

**Version:** 2026.7.1
**Updated:** 2026-07-19
**Status:** Ready for cloud deployment
