# ═══════════════════════════════════════════════════════════════
# OpenClaw Cloud 2026 - QUICK REFERENCE
# ═══════════════════════════════════════════════════════════════

## 🚀 ONE-LINE DEPLOY

### Linux/macOS
```bash
cd openclaw-cloud-2026 && chmod +x scripts/deploy-cloud.sh && ./scripts/deploy-cloud.sh
```

### Windows PowerShell
```powershell
cd openclaw-cloud-2026; .\scripts\deploy-cloud.ps1
```

### Docker Compose (Any OS)
```bash
cd openclaw-cloud-2026 && docker-compose up -d --build
```

---

## ⚡ IMMEDIATE ACTIONS

1. **Get Pickaxe API key** (1 min)
   - Go to https://pickaxe.ai
   - Sign up (free tier available)
   - Copy API key

2. **Configure secrets** (2 min)
   ```bash
   nano .env
   # Update:
   # PICKAXE_API_KEY=pk-your-key
   # DB_PASSWORD=secure-password
   # REDIS_PASSWORD=secure-password
   # SECRET_KEY=very-long-random-string
   ```

3. **Deploy** (3-5 min)
   ```bash
   docker-compose up -d --build
   ```

4. **Verify** (1 min)
   ```bash
   # Wait 30 seconds for services to start
   sleep 30
   
   # Check health
   curl http://localhost:8080/health
   
   # Test chat
   curl -X POST http://localhost:8080/api/mcp/message \
     -H "Content-Type: application/json" \
     -d '{"agent":"main","message":"Hi OpenClaw"}'
   ```

---

## 📂 PROJECT STRUCTURE

```
openclaw-cloud-2026/
├── docker-compose.yml          ← Main orchestration file
├── .env                        ← Environment variables (UPDATE THIS)
├── .gitignore                  ← Git ignore patterns
│
├── Dockerfile.app              ← App container
├── Dockerfile.gateway          ← Gateway container
├── Dockerfile.slackbot         ← Slack bot container
│
├── app/                        ← Flask application
│   ├── app.py                  ← Main app
│   └── requirements.txt         ← Python dependencies
│
├── gateway.py                  ← API Gateway
├── mcp_gateway.py              ← Message router
├── config/
│   └── pickaxe_provider.py     ← Pickaxe LLM integration
│
├── agents/                     ← Specialized agents
│   ├── video_agent/
│   ├── marketing_generator/
│   └── shopify_integration/
│
├── nginx/                      ← Reverse proxy config
│   └── nginx.conf              ← SSL/TLS setup
│
├── db/
│   └── init.sql                ← Database initialization
│
├── scripts/
│   ├── deploy-cloud.sh         ← Linux/macOS deploy
│   └── deploy-cloud.ps1        ← Windows PowerShell deploy
│
├── README.md                   ← Full documentation
├── DEPLOYMENT_GUIDE.md         ← Cloud provider guides
└── QUICK_REFERENCE.md          ← This file
```

---

## 🎯 MAIN SERVICES & PORTS

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| **Nginx (UI)** | 80/443 | http://localhost | React PRO UI |
| **Gateway** | 8080 | http://localhost:8080 | API Router |
| **App** | 8084 | http://localhost:8084 | Flask Backend |
| **Video Agent** | 8085 | http://localhost:8085 | Video Processing |
| **Marketing** | 8086 | http://localhost:8086 | Copy Generation |
| **Shopify** | 8087 | http://localhost:8087 | E-commerce Sync |
| **Slack Bot** | 3000 | http://localhost:3000 | ChatOps |
| **PostgreSQL** | 5432 | Internal | Database |
| **Redis** | 6379 | Internal | Cache |
| **Qdrant** | 6333 | http://localhost:6333 | Vector DB |

---

## 🔑 ENVIRONMENT VARIABLES (CRITICAL)

Update `.env` before deployment:

```bash
# REQUIRED
PICKAXE_API_KEY=pk-your-actual-key-from-pickaxe.ai
DB_PASSWORD=<generate-secure-password>
REDIS_PASSWORD=<generate-secure-password>
SECRET_KEY=<generate-random-string>

# OPTIONAL but recommended
GEMINI_API_KEY=optional-for-fallback-llm
SHOPIFY_STORE_URL=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your-shopify-token
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token

# GENERATE SECURE VALUES
# Linux/macOS:
openssl rand -base64 32

# Windows PowerShell:
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Random -SetSeed 0 -Count 32 -InputObject @(48..57+65..90+97..122))))
```

---

## 🧪 QUICK TESTS

### Health Checks
```bash
# Gateway
curl http://localhost:8080/health

# App
curl http://localhost:8084/healthz

# MCP Status
curl http://localhost:8080/api/mcp/status

# Qdrant
curl http://localhost:6333/health
```

### API Tests
```bash
# Get available agents
curl http://localhost:8080/api/mcp/status | jq '.agents'

# Create session
curl -X POST http://localhost:8080/api/mcp/session \
  -H "Content-Type: application/json" \
  -d '{"agent":"main"}'

# Send message
curl -X POST http://localhost:8080/api/mcp/message \
  -H "Content-Type: application/json" \
  -d '{"agent":"main","message":"Hello"}'

# Test video agent
curl http://localhost:8085/health

# Test marketing agent
curl http://localhost:8086/health
```

---

## 🛠️ COMMON COMMANDS

```bash
# View all running containers
docker-compose ps

# View logs (follow mode)
docker-compose logs -f

# View specific service logs
docker-compose logs -f openclaw_app

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart a service
docker-compose restart openclaw_app

# Execute command in container
docker-compose exec openclaw_app python -c "print('Hello')"

# Shell into container
docker-compose exec openclaw_app bash

# View container resource usage
docker stats

# Rebuild specific service
docker-compose build --no-cache openclaw_app
docker-compose up -d openclaw_app

# View service logs with timestamps
docker-compose logs --timestamps

# Follow live logs with grep filter
docker-compose logs -f | grep ERROR
```

---

## 🚨 EMERGENCY PROCEDURES

### Service Won't Start
```bash
# 1. Check logs
docker-compose logs openclaw_app

# 2. Check .env variables
cat .env | head -10

# 3. Restart clean
docker-compose down -v
docker-compose up -d --build

# 4. Check if port is in use
netstat -an | grep LISTEN | grep 8080
```

### Database Connection Failed
```bash
# Test database directly
docker-compose exec db psql -U openclaw_admin -d openclaw_prod -c "SELECT 1;"

# Reset database
docker-compose exec db psql -U openclaw_admin -d openclaw_prod -f /db/init.sql

# Or: nuke and rebuild
docker-compose down -v
docker volume prune -f
docker-compose up -d
```

### Out of Memory
```bash
# Check usage
docker stats --no-stream

# Reduce worker processes
sed -i 's/GATEWAY_WORKERS=4/GATEWAY_WORKERS=2/' .env

# Increase system memory or clear cache
docker system prune -a
```

### API Returns 502 (Bad Gateway)
```bash
# App crashed?
docker-compose logs openclaw_app

# Restart app
docker-compose restart openclaw_app

# Full restart
docker-compose restart
```

---

## 📦 CLOUD DEPLOYMENT COMMANDS

### Push to GitHub
```bash
git remote add origin <your-repo>
git branch -M main
git push -u origin main
```

### AWS ECS
```bash
aws ecr create-repository --repository-name openclaw
docker tag openclaw-cloud-2026_app <AWS_ID>.dkr.ecr.us-east-1.amazonaws.com/openclaw:app
docker push <AWS_ID>.dkr.ecr.us-east-1.amazonaws.com/openclaw:app
```

### Google Cloud Run
```bash
gcloud run deploy openclaw --source . --platform managed --region us-central1
```

### DigitalOcean Droplet
```bash
# SSH to droplet
ssh root@<IP>

# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone and deploy
git clone <repo> /opt/openclaw
cd /opt/openclaw
nano .env  # Add secrets
docker-compose up -d
```

---

## 🔒 SECURITY ESSENTIALS

- [ ] Change all `.env` defaults
- [ ] Enable HTTPS (SSL certs in nginx/ssl/)
- [ ] Setup firewall (block all except 80, 443)
- [ ] Enable backups
- [ ] Monitor logs regularly
- [ ] Rotate API keys periodically
- [ ] Enable Docker content trust
- [ ] Setup container scanning

---

## 📊 MONITORING URLs

After deployment, access:

- **UI:** http://localhost (or your domain)
- **API Docs:** http://localhost:8080/docs (if enabled)
- **Metrics:** http://localhost:8080/metrics (if enabled)
- **Vector DB UI:** http://localhost:6333/dashboard
- **Health:** http://localhost:8080/health

---

## 🎓 LEARN MORE

- **Full README:** `README.md`
- **Deployment Guide:** `DEPLOYMENT_GUIDE.md`
- **Governance:** `docs/openclaw-governance.md`
- **Architecture:** See docker-compose.yml
- **Pickaxe Integration:** `config/pickaxe_provider.py`

---

## 💬 GET HELP

If something fails:

1. Check logs: `docker-compose logs -f`
2. Check health: `curl http://localhost:8080/health`
3. Review .env: `cat .env | grep -E "PICKAXE|SECRET"`
4. Read docs: See `DEPLOYMENT_GUIDE.md`
5. GitHub Issues: Report the bug

---

**Status:** ✅ Production Ready  
**Version:** 2026.5.27-cloud  
**Updated:** 2026-06-02
