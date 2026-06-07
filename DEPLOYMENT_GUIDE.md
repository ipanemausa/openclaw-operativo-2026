# ═══════════════════════════════════════════════════════════════
# OpenClaw Cloud 2026 - DEPLOYMENT INSTRUCTIONS
# ═══════════════════════════════════════════════════════════════

## 📋 PRE-DEPLOYMENT CHECKLIST

Before deploying to cloud, verify:

- [ ] Docker installed and running
- [ ] Docker Compose v2.0+
- [ ] Git installed (for version control)
- [ ] 20GB+ disk space available
- [ ] 8GB+ RAM available
- [ ] Internet connection (for pulling images)
- [ ] Pickaxe API key obtained (free tier available at https://pickaxe.ai)
- [ ] SSL certificates ready (or auto-generate)

---

## 🚀 QUICK START (5 MINUTES)

### Step 1: Get the code
```bash
# Option A: Git clone
git clone <your-repo-url> openclaw-cloud-2026
cd openclaw-cloud-2026

# Option B: Direct copy
cp -r openclaw-cloud-2026 /opt/openclaw
cd /opt/openclaw
```

### Step 2: Configure secrets
```bash
# Edit .env with your keys
nano .env

# Required changes:
# - PICKAXE_API_KEY=pk-your-actual-key
# - DB_PASSWORD=strong-random-password
# - REDIS_PASSWORD=strong-random-password
# - SECRET_KEY=very-long-random-string
```

### Step 3: Deploy
```bash
# Linux/macOS
chmod +x scripts/deploy-cloud.sh
./scripts/deploy-cloud.sh

# Windows PowerShell
.\scripts\deploy-cloud.ps1

# Manual
docker-compose up -d --build
```

### Step 4: Verify
```bash
# Check services
docker-compose ps

# Check health
curl http://localhost:8080/health

# Test chat
curl -X POST http://localhost:8080/api/mcp/message \
  -H "Content-Type: application/json" \
  -d '{"agent":"main","message":"Hello"}'
```

---

## ☁️ CLOUD PROVIDER SETUP

### AWS ECS (Elastic Container Service)

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name openclaw-cloud

# 2. Build and push images
docker-compose build
docker tag openclaw-cloud-2026_app:latest <AWS_ACCOUNT>.dkr.ecr.<REGION>.amazonaws.com/openclaw-cloud:app
docker push <AWS_ACCOUNT>.dkr.ecr.<REGION>.amazonaws.com/openclaw-cloud:app

# 3. Create ECS task definition (use docker-compose.yml as reference)
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# 4. Create ECS service
aws ecs create-service \
  --cluster openclaw-cluster \
  --service-name openclaw-service \
  --task-definition openclaw-cloud:1 \
  --desired-count 1
```

### Google Cloud Run

```bash
# 1. Enable Container Registry
gcloud services enable containerregistry.googleapis.com

# 2. Build and push
docker build -t gcr.io/PROJECT_ID/openclaw:latest .
docker push gcr.io/PROJECT_ID/openclaw:latest

# 3. Deploy to Cloud Run
gcloud run deploy openclaw \
  --image gcr.io/PROJECT_ID/openclaw:latest \
  --platform managed \
  --region us-central1 \
  --set-env-vars PICKAXE_API_KEY=pk-your-key
```

### DigitalOcean App Platform

```bash
# 1. Create app.yaml in project root
cat > .do/app.yaml << EOF
name: openclaw-cloud
services:
- name: openclaw-app
  github:
    repo: your-username/openclaw-cloud-2026
    branch: main
  build_command: docker-compose build
  run_command: docker-compose up -d
  envs:
  - key: PICKAXE_API_KEY
    value: ${PICKAXE_API_KEY}
EOF

# 2. Deploy via doctl
doctl apps create --spec .do/app.yaml
```

### Azure Container Instances

```bash
# 1. Create resource group
az group create --name openclaw-rg --location eastus

# 2. Build and push to ACR
az acr build --registry openclaw --image openclaw:latest .

# 3. Deploy container
az container create \
  --resource-group openclaw-rg \
  --name openclaw-app \
  --image openclaw.azurecr.io/openclaw:latest \
  --environment-variables PICKAXE_API_KEY=pk-your-key
```

### Heroku (Free Tier)

```bash
# 1. Create Procfile
echo "web: docker-compose up -d" > Procfile

# 2. Create heroku.yml
cat > heroku.yml << EOF
build:
  docker:
    web: Dockerfile.app
release:
  image: web
run:
  web: gunicorn -b 0.0.0.0:$PORT app:app
EOF

# 3. Deploy
heroku login
heroku apps:create openclaw-cloud
git push heroku main
```

### Self-Hosted VPS (DigitalOcean Droplet, Linode, etc.)

```bash
# 1. SSH into server
ssh root@your.vps.ip

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Clone and deploy
git clone <repo> /opt/openclaw
cd /opt/openclaw
nano .env  # Add secrets
docker-compose up -d

# 5. Setup SSL with Let's Encrypt
sudo apt-get update && sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d your-domain.com
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/openclaw.crt
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/openclaw.key
docker-compose restart nginx
```

---

## 🔐 SECURITY CHECKLIST

- [ ] Change all default passwords in .env
- [ ] Enable SSL/TLS (nginx is configured)
- [ ] Configure firewall rules
- [ ] Setup backup strategy
- [ ] Enable monitoring/alerting
- [ ] Review security headers (already in nginx.conf)
- [ ] Rotate secrets regularly
- [ ] Enable Docker container security scanning
- [ ] Use environment variables for secrets (not hardcoded)
- [ ] Enable audit logging

---

## 📊 MONITORING & MAINTENANCE

### Daily Checks
```bash
# Container health
docker-compose ps

# Service logs
docker-compose logs --tail=100

# Database size
docker-compose exec db du -sh /var/lib/postgresql/data
```

### Weekly Maintenance
```bash
# Backup database
docker-compose exec db pg_dump -U openclaw_admin openclaw_prod > backup-$(date +%Y%m%d).sql

# Clean unused Docker objects
docker system prune -a --volumes
```

### Monthly Optimization
```bash
# Review logs for errors
docker-compose logs | grep ERROR | wc -l

# Check resource usage
docker stats

# Update images
docker-compose pull
docker-compose up -d
```

---

## 📱 ACCESS YOUR DEPLOYMENT

After successful deployment:

**Local Machine:**
- UI: http://localhost
- API: http://localhost:8080/api
- Chat: http://localhost/chat

**Cloud Deployment (with domain):**
- UI: https://your-domain.com
- API: https://your-domain.com/api
- Chat: https://your-domain.com/chat

**API Examples:**
```bash
# Get MCP status
curl https://your-domain.com/api/mcp/status

# Send message to agent
curl -X POST https://your-domain.com/api/mcp/message \
  -H "Content-Type: application/json" \
  -d '{"agent":"main","message":"Hello OpenClaw"}'

# Check gateway health
curl https://your-domain.com/health
```

---

## 🆘 TROUBLESHOOTING COMMON ISSUES

### Issue: Services fail to start
```bash
# Check environment
cat .env | grep -E "PICKAXE|SECRET_KEY"

# Check logs
docker-compose logs -f

# Rebuild
docker-compose down
docker-compose up -d --build
```

### Issue: Pickaxe API key not working
```bash
# Verify key format
echo $PICKAXE_API_KEY | head -c 3  # Should be "pk-"

# Test API connection
curl -H "Authorization: Bearer $PICKAXE_API_KEY" \
  https://api.pickaxe.ai/v1/health
```

### Issue: SSL certificate errors
```bash
# Regenerate self-signed certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/openclaw.key \
  -out nginx/ssl/openclaw.crt
docker-compose restart nginx
```

### Issue: Database connection refused
```bash
# Check if database is running
docker-compose ps | grep openclaw_db

# Check database logs
docker-compose logs openclaw_db

# Verify credentials
docker-compose exec db psql -U openclaw_admin -d openclaw_prod -c "SELECT 1;"
```

### Issue: Out of memory
```bash
# Check resource usage
docker stats

# Reduce worker count
sed -i 's/GATEWAY_WORKERS=4/GATEWAY_WORKERS=2/' .env
docker-compose up -d
```

---

## 📚 ADDITIONAL RESOURCES

- **Documentation:** See `docs/` folder
- **Governance:** `docs/openclaw-governance.md`
- **API Reference:** Run `/api/docs` (Swagger)
- **GitHub Issues:** Report bugs and feature requests
- **Community:** Join OpenClaw Discord

---

## 🎯 NEXT STEPS AFTER DEPLOYMENT

1. **Create first agent session**
   ```bash
   curl -X POST https://your-domain.com/api/mcp/session \
     -H "Content-Type: application/json" \
     -d '{"agent":"main"}'
   ```

2. **Send test message**
   ```bash
   curl -X POST https://your-domain.com/api/mcp/message \
     -H "Content-Type: application/json" \
     -d '{"agent":"main","message":"What can you do?"}'
   ```

3. **Setup monitoring**
   - Configure DataDog, New Relic, or similar
   - Setup alerts for service failures

4. **Enable integrations**
   - Slack Bot: Add SLACK_BOT_TOKEN and SLACK_APP_TOKEN
   - Shopify: Add store URL and access token
   - Video: Upload sample videos to test

5. **Backup strategy**
   - Daily database snapshots
   - Config file backups
   - Volume snapshots

---

## ✅ DEPLOYMENT SUCCESS CRITERIA

- [ ] All containers running (`docker-compose ps` shows all UP)
- [ ] Health checks passing (curl /health returns 200)
- [ ] Database connected and initialized
- [ ] Pickaxe API responding
- [ ] UI loads without errors
- [ ] Chat accepts messages and responds
- [ ] SSL/TLS configured (if on cloud)
- [ ] Backups in place
- [ ] Monitoring active

---

## 📞 SUPPORT & CONTACT

- **Issues:** GitHub Issues
- **Documentation:** docs/
- **Community:** Discord/Slack channel
- **Commercial Support:** support@openclaw.ai

---

**Version:** 2026.5.27-cloud  
**Last Updated:** 2026-06-02  
**Status:** Production Ready
