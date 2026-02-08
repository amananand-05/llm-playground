# Production Deployment Guide

## Environment Variables Required in Production

When you deploy to production, the application will look for these environment variables (`.env` file is **NOT** used in production).

---

## ✅ Required Environment Variables

These **MUST** be set in production, or the application will fail to start:

### 1. `LLM_API_KEY`
- **Description:** Your LLM provider's API authentication key
- **Type:** String
- **Required:** ✅ Yes
- **Example:** `gsk_...` (Groq) or `sk-...` (OpenAI)
- **Security:** 🔒 **NEVER commit to git or expose publicly**

### 2. `LLM_BASE_URL`
- **Description:** Base URL of your LLM provider's API endpoint
- **Type:** String (URL)
- **Required:** ✅ Yes
- **Examples:**
  - Groq: `https://api.groq.com/openai`
  - OpenAI: `https://api.openai.com`
  - Azure: `https://your-resource.openai.azure.com`

### 3. `LLM_MODEL`
- **Description:** Model identifier to use for generation
- **Type:** String
- **Required:** ✅ Yes
- **Examples:**
  - Groq: `moonshotai/kimi-k2-instruct-0905`
  - OpenAI: `gpt-4o` or `gpt-3.5-turbo`
  - Azure: `your-deployment-name`

---

## ⚙️ Optional Environment Variables

These have default values and can be customized:

### 4. `API_TIMEOUT`
- **Description:** Request timeout in seconds
- **Type:** Integer
- **Required:** ❌ No
- **Default:** `60`
- **Recommendation:** Set based on your provider's typical response time
- **Example:** `30` (faster), `120` (slower connections)

### 5. `LLM_PROVIDER`
- **Description:** Provider name for logging/monitoring (cosmetic)
- **Type:** String
- **Required:** ❌ No
- **Default:** `"generic"`
- **Example:** `groq`, `openai`, `azure`
- **Note:** Not used in API calls, only for logging

---

## 📋 Quick Reference Table

| Variable | Required | Default | Example |
|----------|----------|---------|---------|
| `LLM_API_KEY` | ✅ Yes | None | `gsk_abc123...` |
| `LLM_BASE_URL` | ✅ Yes | None | `https://api.groq.com/openai` |
| `LLM_MODEL` | ✅ Yes | None | `moonshotai/kimi-k2-instruct-0905` |
| `API_TIMEOUT` | ❌ No | `60` | `30` |
| `LLM_PROVIDER` | ❌ No | `"generic"` | `groq` |

---

## 🚀 How Pydantic Settings Works

### Development (with `.env` file)
```python
# Pydantic reads from .env file automatically
settings = Settings()
```

### Production (without `.env` file)
```python
# Pydantic reads from system environment variables
# export LLM_API_KEY="gsk_..."
# export LLM_BASE_URL="https://api.groq.com/openai"
# export LLM_MODEL="moonshotai/kimi-k2-instruct-0905"
settings = Settings()
```

**Pydantic automatically looks in this order:**
1. System environment variables (always checked first)
2. `.env` file (if present, only in development)
3. Default values (if defined in code)

---

## 🔧 Platform-Specific Setup

### AWS EC2 / Virtual Machine

**Option 1: Export in shell profile**
```bash
# Add to ~/.bashrc or ~/.bash_profile
export LLM_API_KEY="gsk_your_key"
export LLM_BASE_URL="https://api.groq.com/openai"
export LLM_MODEL="moonshotai/kimi-k2-instruct-0905"
export API_TIMEOUT="60"
export LLM_PROVIDER="groq"
```

**Option 2: Systemd service file**
```ini
# /etc/systemd/system/llm-fastapi.service
[Unit]
Description=LLM FastAPI Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/llm-fastapi
Environment="LLM_API_KEY=gsk_your_key"
Environment="LLM_BASE_URL=https://api.groq.com/openai"
Environment="LLM_MODEL=moonshotai/kimi-k2-instruct-0905"
Environment="API_TIMEOUT=60"
Environment="LLM_PROVIDER=groq"
ExecStart=/opt/llm-fastapi/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

---

### Docker / Docker Compose

**Dockerfile**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application
COPY app ./app

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**
```yaml
version: '3.8'

services:
  llm-fastapi:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LLM_API_KEY=${LLM_API_KEY}
      - LLM_BASE_URL=${LLM_BASE_URL}
      - LLM_MODEL=${LLM_MODEL}
      - API_TIMEOUT=${API_TIMEOUT:-60}
      - LLM_PROVIDER=${LLM_PROVIDER:-groq}
    restart: unless-stopped
```

**Run with:**
```bash
# Set variables in your shell
export LLM_API_KEY="gsk_your_key"
export LLM_BASE_URL="https://api.groq.com/openai"
export LLM_MODEL="moonshotai/kimi-k2-instruct-0905"

# Start container
docker-compose up -d
```

---

### Kubernetes

**deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-fastapi
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-fastapi
  template:
    metadata:
      labels:
        app: llm-fastapi
    spec:
      containers:
      - name: llm-fastapi
        image: your-registry/llm-fastapi:latest
        ports:
        - containerPort: 8000
        env:
        - name: LLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: llm-secrets
              key: api-key
        - name: LLM_BASE_URL
          value: "https://api.groq.com/openai"
        - name: LLM_MODEL
          value: "moonshotai/kimi-k2-instruct-0905"
        - name: API_TIMEOUT
          value: "60"
        - name: LLM_PROVIDER
          value: "groq"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**secrets.yaml** (Never commit this!)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: llm-secrets
type: Opaque
stringData:
  api-key: "gsk_your_actual_api_key"
```

**Create secret from command line:**
```bash
kubectl create secret generic llm-secrets \
  --from-literal=api-key='gsk_your_actual_key'
```

---

### AWS Elastic Beanstalk

**Option 1: EB Console**
1. Go to Configuration → Software
2. Add Environment Properties:
   - `LLM_API_KEY` = `gsk_your_key`
   - `LLM_BASE_URL` = `https://api.groq.com/openai`
   - `LLM_MODEL` = `moonshotai/kimi-k2-instruct-0905`
   - `API_TIMEOUT` = `60`
   - `LLM_PROVIDER` = `groq`

**Option 2: EB CLI**
```bash
eb setenv \
  LLM_API_KEY=gsk_your_key \
  LLM_BASE_URL=https://api.groq.com/openai \
  LLM_MODEL=moonshotai/kimi-k2-instruct-0905 \
  API_TIMEOUT=60 \
  LLM_PROVIDER=groq
```

---

### Heroku

```bash
heroku config:set \
  LLM_API_KEY=gsk_your_key \
  LLM_BASE_URL=https://api.groq.com/openai \
  LLM_MODEL=moonshotai/kimi-k2-instruct-0905 \
  API_TIMEOUT=60 \
  LLM_PROVIDER=groq
```

**Or via Heroku Dashboard:**
Settings → Config Vars → Add each variable

---

### Vercel

**vercel.json**
```json
{
  "env": {
    "LLM_API_KEY": "@llm-api-key",
    "LLM_BASE_URL": "https://api.groq.com/openai",
    "LLM_MODEL": "moonshotai/kimi-k2-instruct-0905",
    "API_TIMEOUT": "60",
    "LLM_PROVIDER": "groq"
  }
}
```

**Add secret:**
```bash
vercel secrets add llm-api-key gsk_your_actual_key
```

---

### Railway

**Via Dashboard:**
1. Go to your project → Variables
2. Add each variable:
   - `LLM_API_KEY`
   - `LLM_BASE_URL`
   - `LLM_MODEL`
   - `API_TIMEOUT`
   - `LLM_PROVIDER`

**Via CLI:**
```bash
railway variables set \
  LLM_API_KEY=gsk_your_key \
  LLM_BASE_URL=https://api.groq.com/openai \
  LLM_MODEL=moonshotai/kimi-k2-instruct-0905
```

---

### Google Cloud Run

```bash
gcloud run deploy llm-fastapi \
  --image gcr.io/your-project/llm-fastapi \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars \
    LLM_API_KEY=gsk_your_key,\
    LLM_BASE_URL=https://api.groq.com/openai,\
    LLM_MODEL=moonshotai/kimi-k2-instruct-0905,\
    API_TIMEOUT=60,\
    LLM_PROVIDER=groq
```

**Or use Secret Manager:**
```bash
# Create secret
echo -n "gsk_your_key" | gcloud secrets create llm-api-key --data-file=-

# Deploy with secret
gcloud run deploy llm-fastapi \
  --image gcr.io/your-project/llm-fastapi \
  --update-secrets LLM_API_KEY=llm-api-key:latest \
  --set-env-vars \
    LLM_BASE_URL=https://api.groq.com/openai,\
    LLM_MODEL=moonshotai/kimi-k2-instruct-0905
```

---

### Azure App Service

**Via Azure Portal:**
1. Go to Configuration → Application settings
2. Add New application setting for each variable

**Via Azure CLI:**
```bash
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name myAppName \
  --settings \
    LLM_API_KEY=gsk_your_key \
    LLM_BASE_URL=https://api.groq.com/openai \
    LLM_MODEL=moonshotai/kimi-k2-instruct-0905 \
    API_TIMEOUT=60 \
    LLM_PROVIDER=groq
```

---

## 🔒 Security Best Practices

### 1. Never Hardcode Secrets
❌ **Bad:**
```python
LLM_API_KEY = "gsk_abc123..."  # Never do this!
```

✅ **Good:**
```python
from app.core.config import settings
api_key = settings.llm_api_key  # From environment variable
```

### 2. Use Secret Management Services

**AWS:**
- AWS Secrets Manager
- AWS Systems Manager Parameter Store

**Azure:**
- Azure Key Vault

**Google Cloud:**
- Google Secret Manager

**Kubernetes:**
- Kubernetes Secrets
- External Secrets Operator

**HashiCorp:**
- Vault

### 3. Rotate API Keys Regularly

Set up a rotation schedule:
- Development: Every 90 days
- Production: Every 30-60 days
- Immediately if compromised

### 4. Use Different Keys for Different Environments

```bash
# Development
LLM_API_KEY=gsk_dev_key_here

# Staging
LLM_API_KEY=gsk_staging_key_here

# Production
LLM_API_KEY=gsk_prod_key_here
```

### 5. Restrict API Key Permissions

If your provider supports it:
- Limit to specific IP addresses
- Set usage quotas
- Enable rate limiting
- Monitor usage for anomalies

---

## ✅ Verification Checklist

Before deploying to production:

- [ ] All required environment variables are set
- [ ] API key is valid and has sufficient quota
- [ ] Base URL is correct for your provider
- [ ] Model name is valid and accessible
- [ ] Timeout is appropriate for your use case
- [ ] Secrets are NOT in git repository
- [ ] Secrets are NOT in Docker images
- [ ] Secrets are NOT in logs or error messages
- [ ] Health endpoint works: `curl http://your-domain/health`
- [ ] Generate endpoint works: `curl -X POST http://your-domain/generate -d '{"prompt":"test"}'`

---

## 🧪 Testing Environment Variables

### Before Deployment

Test that all required variables are set:

```python
# test_config.py
from app.core.config import settings

def test_required_vars():
    """Verify all required environment variables are set."""
    assert settings.llm_api_key, "LLM_API_KEY not set"
    assert settings.llm_base_url, "LLM_BASE_URL not set"
    assert settings.llm_model, "LLM_MODEL not set"
    print("✅ All required environment variables are set")
    print(f"Provider: {settings.llm_provider}")
    print(f"Model: {settings.llm_model}")
    print(f"Timeout: {settings.api_timeout}s")

if __name__ == "__main__":
    test_required_vars()
```

Run before deploying:
```bash
python test_config.py
```

---

## 🚨 What Happens if Variables Are Missing?

### Application Behavior

If required variables are missing, Pydantic will raise an error on startup:

```python
pydantic_core._pydantic_core.ValidationError: 3 validation errors for Settings
llm_api_key
  Field required [type=missing, input_value={}, input_type=dict]
llm_base_url
  Field required [type=missing, input_value={}, input_type=dict]
llm_model
  Field required [type=missing, input_value={}, input_type=dict]
```

**The application will NOT start** - this is a safety feature!

### Error Messages by Platform

**Docker:**
```bash
$ docker run llm-fastapi
ValidationError: Field required: llm_api_key
Container exits with code 1
```

**Kubernetes:**
```bash
$ kubectl get pods
NAME                STATUS             RESTARTS
llm-fastapi-xyz     CrashLoopBackOff   5
```

**Systemd:**
```bash
$ systemctl status llm-fastapi
● llm-fastapi.service - failed
   Active: failed
```

---

## 📚 Summary

### Required in Production:
1. `LLM_API_KEY` - Your provider's API key
2. `LLM_BASE_URL` - Provider's API endpoint
3. `LLM_MODEL` - Model identifier

### Optional (have defaults):
4. `API_TIMEOUT` - Default: 60 seconds
5. `LLM_PROVIDER` - Default: "generic"

### Key Points:
- ✅ `.env` file is for **development only**
- ✅ Production uses **system environment variables**
- ✅ Pydantic automatically reads from both
- ✅ Application **fails fast** if required vars are missing
- ✅ Use secrets management for API keys
- ✅ Never commit secrets to git

---

**Your application is designed to be 12-factor app compliant and cloud-ready!** ☁️
