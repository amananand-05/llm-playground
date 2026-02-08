# LLM FastAPI

**Provider-agnostic FastAPI backend for any OpenAI-compatible LLM API.**

Works with Groq, OpenAI, Azure OpenAI, and any other OpenAI-compatible provider - just update environment variables!

---

## 📋 Table of Contents

1. [Features](#features)
2. [Quick Start](#quick-start)
3. [API Endpoints](#api-endpoints)
4. [Switch LLM Providers](#switch-llm-providers)
5. [PyCharm Setup](#pycharm-setup)
6. [Architecture](#architecture)
7. [Provider-Agnostic Design](#provider-agnostic-design)
8. [Configuration Reference](#configuration-reference)
9. [Development Guide](#development-guide)
10. [Troubleshooting](#troubleshooting)

---

## Features

- 🔄 **Provider-Agnostic** - Switch LLM providers without code changes
- ⚡ **FastAPI** - Modern, fast web framework with async/await
- 🚀 **Multiple Providers** - Groq, OpenAI, Azure OpenAI, and more
- ✨ **Pydantic v2** - Data validation and settings management
- 📦 **Poetry** - Dependency management and virtual environments
- 🎨 **Ruff** - Fast code linting and formatting
- 🐍 **Python 3.12+** - Latest Python features with type hints throughout
- 📖 **Auto-generated API docs** - Interactive Swagger UI and ReDoc

---

## Quick Start

### 1. Prerequisites

- **Python 3.12+** installed
- **Poetry** installed (`brew install poetry` on macOS)
- API key from any OpenAI-compatible provider (Groq, OpenAI, etc.)

### 2. Install Dependencies

```bash
poetry install
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your LLM provider credentials:

**Using Groq (Current Default - Free & Fast):**
```env
LLM_API_KEY=your_groq_api_key_here
LLM_BASE_URL=https://api.groq.com/openai
LLM_MODEL=moonshotai/kimi-k2-instruct-0905
LLM_PROVIDER=groq
```

**Using OpenAI:**
```env
LLM_API_KEY=sk-your-openai-key
LLM_BASE_URL=https://api.openai.com
LLM_MODEL=gpt-4o
LLM_PROVIDER=openai
```

See [Switch LLM Providers](#switch-llm-providers) for more examples!

### 4. Run Server

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Test API

```bash
# Health check
curl http://localhost:8000/health

# Generate response
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing in simple terms"}'
```

### 6. Interactive API Documentation

Visit http://localhost:8000/docs for Swagger UI with live API testing.

---

## API Endpoints

### POST /generate

Generate AI response from a text prompt.

**Request:**
```json
{
  "prompt": "your text here"
}
```

**Response (200 OK):**
```json
{
  "response": "AI-generated response"
}
```

**Error Responses:**
- `422 Unprocessable Entity` - Invalid request format
- `502 Bad Gateway` - LLM API error
- `500 Internal Server Error` - Server error

### GET /health

Health check endpoint.

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

---

## Switch LLM Providers

**No code changes needed!** Just update `.env` and restart the server.

### Groq (Fast, Free Tier Available)
```env
LLM_API_KEY=gsk_your_groq_key
LLM_BASE_URL=https://api.groq.com/openai
LLM_MODEL=moonshotai/kimi-k2-instruct-0905
LLM_PROVIDER=groq
```

**Popular Groq Models:**
- `moonshotai/kimi-k2-instruct-0905` - Kimi K2
- `llama-3.3-70b-versatile` - Llama 3.3 70B
- `mixtral-8x7b-32768` - Mixtral 8x7B

Get API key: https://console.groq.com/

### OpenAI
```env
LLM_API_KEY=sk-your_openai_key
LLM_BASE_URL=https://api.openai.com
LLM_MODEL=gpt-4o
LLM_PROVIDER=openai
```

**Popular OpenAI Models:**
- `gpt-4o` - GPT-4 Optimized
- `gpt-4-turbo` - GPT-4 Turbo
- `gpt-3.5-turbo` - GPT-3.5 Turbo

Get API key: https://platform.openai.com/

### Azure OpenAI
```env
LLM_API_KEY=your_azure_key
LLM_BASE_URL=https://your-resource.openai.azure.com
LLM_MODEL=gpt-4
LLM_PROVIDER=azure
```

Get started: https://learn.microsoft.com/azure/ai-services/openai/

### Other OpenAI-Compatible Providers

✅ Together AI  
✅ Anyscale  
✅ Perplexity  
✅ Local models (via LM Studio, Ollama)  
✅ Any custom OpenAI-compatible endpoint

---

## PyCharm Setup

### Quick Setup (2 minutes)

1. **Open Project**
   - `File → Open → llm-playground → Open`

2. **Wait for Poetry**
   - PyCharm auto-detects Poetry and installs dependencies
   - Watch progress bar at bottom (30-60 seconds)

3. **Run Server**
   - Select "FastAPI Server" from dropdown (top-right)
   - Click green play button ▶️
   - Server starts on http://localhost:8000

4. **Test**
   - Visit: http://localhost:8000/docs

### Alternative Run Method

**Terminal in PyCharm:**
```bash
poetry run uvicorn app.main:app --reload
```

### PyCharm Keyboard Shortcuts

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Run | ⌃R | Shift+F10 |
| Debug | ⌃D | Shift+F9 |
| Stop | ⌘F2 | Ctrl+F2 |
| Terminal | ⌥F12 | Alt+F12 |
| Search | ⇧⇧ | Shift+Shift |

### Troubleshooting PyCharm

**"No module named 'app'"**
- Right-click project root → Mark Directory as → Sources Root

**"Module 'uvicorn' not found"**
```bash
poetry install
```
Then: File → Invalidate Caches → Invalidate and Restart

**Poetry not detected**
- Settings → Plugins → Search "Poetry" → Install → Restart

**Port 8000 in use**
```bash
lsof -i :8000
kill -9 <PID>
# Or: pkill -9 -f uvicorn
```

---

## Architecture

### Project Structure

```
llm-playground/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   └── routes.py        # API route handlers
│   ├── core/
│   │   └── config.py        # Generic settings (provider-agnostic)
│   ├── services/
│   │   └── llm_client.py    # Generic LLM client (works with any provider)
│   └── schemas/
│       └── prompt.py        # Pydantic request/response models
├── .env                     # Your secrets (git-ignored)
├── .env.example             # Configuration template
├── pyproject.toml           # Poetry dependencies
├── poetry.lock              # Locked dependency versions
└── README.md                # This file
```

### Design Principles

#### 1. Provider Agnosticism
- No hardcoded provider names in code
- All provider specifics driven by environment variables
- Works with any OpenAI-compatible API
- Switch providers without changing a single line of code

#### 2. Separation of Concerns
- **API layer** (`routes.py`) - HTTP requests/responses only
- **Service layer** (`llm_client.py`) - Business logic and external API calls
- **Config layer** (`config.py`) - Environment variable management
- **Schema layer** (`prompt.py`) - Data validation and serialization

#### 3. Async Throughout
- All functions use async/await for non-blocking I/O
- `httpx.AsyncClient` for concurrent API requests
- FastAPI's native async support for optimal performance

#### 4. Type Safety
- Full type hints on all functions and variables
- Pydantic models for request/response validation
- Runtime type checking via Pydantic

#### 5. Error Handling
- Upstream API errors return 502 Bad Gateway
- Internal errors return 500 Internal Server Error
- Validation errors handled by FastAPI (422)
- Meaningful error messages for debugging

---

## Provider-Agnostic Design

### Why Provider-Agnostic?

- 💰 **Cost Optimization** - Switch to cheaper providers easily
- 🔄 **Flexibility** - Try different models without refactoring
- 🛡️ **Reliability** - Fallback to another provider if one is down
- 🧪 **Testing** - Use different providers for dev/staging/prod
- 🚀 **Future-Proof** - Support new providers as they emerge

### How It Works

The codebase uses **generic naming** throughout:

**Generic Client:**
```python
# app/services/llm_client.py
class LLMClient:
    """Generic LLM client that works with any OpenAI-compatible API."""
    
    async def generate(self, prompt: str) -> str:
        """Generate response from configured LLM provider."""
```

**Generic Configuration:**
```python
# app/core/config.py
class Settings(BaseSettings):
    llm_api_key: str
    llm_base_url: str
    llm_model: str
    llm_provider: str | None = None  # Optional, for logging
```

**Generic Routes:**
```python
# app/api/routes.py
async with get_llm_client() as client:
    response = await client.generate(request.prompt)
```

### Migration from Old Config

If you had provider-specific configuration:

**OLD (.env):**
```env
KIMI_API_KEY=gsk_...
KIMI_BASE_URL=https://api.groq.com/openai
MODEL_NAME=moonshotai/kimi-k2-instruct-0905
```

**NEW (.env):**
```env
LLM_API_KEY=gsk_...
LLM_BASE_URL=https://api.groq.com/openai
LLM_MODEL=moonshotai/kimi-k2-instruct-0905
LLM_PROVIDER=groq
```

Simply rename the variables - the values stay the same!

---

## Configuration Reference

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `LLM_API_KEY` | ✅ Yes | API authentication key | `gsk_...` or `sk-...` |
| `LLM_BASE_URL` | ✅ Yes | Base API endpoint URL | `https://api.groq.com/openai` |
| `LLM_MODEL` | ✅ Yes | Model identifier | `moonshotai/kimi-k2-instruct-0905` |
| `LLM_PROVIDER` | ❌ No | Provider name (for logging) | `groq`, `openai`, `azure` |
| `API_TIMEOUT` | ❌ No | Request timeout in seconds | `60` (default) |

### .env.example

The project includes `.env.example` with configuration templates for:
- Groq (with available models)
- OpenAI (with available models)
- Azure OpenAI (with deployment example)
- Generic OpenAI-compatible APIs

Copy it to start:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

---

## Development Guide

### Code Quality

**Format code:**
```bash
poetry run ruff format .
```

**Check for issues:**
```bash
poetry run ruff check .
```

**Auto-fix issues:**
```bash
poetry run ruff check --fix .
```

### Adding Dependencies

**Production dependency:**
```bash
poetry add package-name
```

**Development dependency:**
```bash
poetry add --group dev package-name
```

### Auto-reload Development

With `--reload` flag, the server automatically restarts when you save files:

```bash
poetry run uvicorn app.main:app --reload
```

**Watch logs:**
```
INFO:     Detected file change in 'app/routes.py'
INFO:     Restarting...
```

### Testing the API

**Using curl:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?"}'
```

**Using httpie:**
```bash
http POST localhost:8000/generate prompt="What is FastAPI?"
```

**Using Python requests:**
```python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={"prompt": "Tell me a joke"}
)
print(response.json())
```

### Development Workflow

1. **Start server** with auto-reload
2. **Edit code** in your IDE
3. **Save file** (⌘S / Ctrl+S)
4. **Server auto-restarts**
5. **Test** changes immediately
6. **Repeat**

### Before Committing

1. Format code: `poetry run ruff format .`
2. Check for issues: `poetry run ruff check .`
3. Test manually in browser/curl
4. Commit changes

---

## Troubleshooting

### Server Won't Start

**Check Python version:**
```bash
python3 --version  # Should be 3.12+
```

**Check port availability:**
```bash
lsof -i :8000
```

**Ensure dependencies installed:**
```bash
poetry install
```

**Validate .env file exists:**
```bash
ls -la .env
```

### API Returns 401/403 Error

- Verify `LLM_API_KEY` in `.env` is correct
- Check API key is active with your provider
- Ensure no extra spaces/newlines in `.env`
- Try regenerating API key from provider console

### API Returns 502 Error

- Check `LLM_BASE_URL` is correct
- Verify internet connectivity
- Check provider API status
- Increase `API_TIMEOUT` if needed

### Import Errors

**Activate Poetry environment:**
```bash
poetry shell
```

**Or prefix commands with:**
```bash
poetry run python your_script.py
```

**Reinstall dependencies:**
```bash
poetry install
```

### Port Already in Use

**Find and kill process:**
```bash
# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Kill all uvicorn
pkill -9 -f uvicorn
```

**Or use different port:**
```bash
poetry run uvicorn app.main:app --reload --port 8001
```

---

## Production Deployment

### Production Server

Use multiple workers for production:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment Configuration

- ✅ Never commit `.env` to version control
- ✅ Use environment variables or secrets management in production
- ✅ Set appropriate `API_TIMEOUT` for your use case
- ✅ Implement rate limiting for production traffic
- ✅ Add authentication if exposing publicly

### Security Considerations

- 🔒 Keep API keys secret and rotate regularly
- 🔒 Use HTTPS in production (configure reverse proxy)
- 🔒 Implement rate limiting to prevent abuse
- 🔒 Add authentication for public APIs
- 🔒 Monitor API usage and set budget limits
- 🔒 Never log API keys or sensitive data

### Performance Optimization

- ⚡ Adjust worker count based on CPU cores
- ⚡ Configure timeout values based on average response time
- ⚡ Use connection pooling (built into httpx)
- ⚡ Consider caching for repeated prompts
- ⚡ Monitor response times and optimize slow endpoints

---

## Technologies

- **FastAPI** - Modern async web framework
- **OpenAI-Compatible APIs** - Universal LLM access
- **Poetry** - Dependency and virtual environment management
- **httpx** - Async HTTP client
- **Pydantic v2** - Data validation and settings
- **Uvicorn** - Lightning-fast ASGI server
- **Ruff** - Fast Python linter and formatter
- **Python 3.12+** - Latest Python with enhanced features

---

## Supported Providers

✅ **Groq** - Lightning-fast inference (Current default)  
✅ **OpenAI** - GPT-4, GPT-3.5 models  
✅ **Azure OpenAI** - Enterprise OpenAI  
✅ **Together AI** - Multiple open-source models  
✅ **Anyscale** - Scalable LLM inference  
✅ **Any OpenAI-compatible API** - Local models, custom endpoints, etc.

**Switch between providers without changing code!**

---

## What This Project Does NOT Include

Deliberately excluded to maintain simplicity and focus:

- ❌ Docker containerization
- ❌ Database integration
- ❌ Authentication/authorization
- ❌ CI/CD pipelines
- ❌ Microservices architecture
- ❌ Message queues
- ❌ Caching layers
- ❌ Background workers
- ❌ Complex monitoring/observability
- ❌ Multi-environment configurations

These can be added when requirements justify the complexity.

---

## Code Quality Standards

This project follows:

- ✅ PEP 8 style guide (enforced by Ruff)
- ✅ Type hints everywhere (PEP 484, 585, 604)
- ✅ Async best practices
- ✅ Clean code principles
- ✅ SOLID principles where applicable
- ✅ Explicit is better than implicit

---

## Contributing

When extending this project:

1. Maintain type hints on all functions
2. Use async/await consistently
3. Keep business logic in service layer
4. Add validation with Pydantic models
5. Handle errors gracefully
6. Update README for significant changes
7. Run Ruff before committing
8. Keep dependencies minimal

---

## License

MIT License - Use freely for personal and commercial projects.

---

## Resources

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **Poetry Documentation:** https://python-poetry.org/docs/
- **Pydantic Documentation:** https://docs.pydantic.dev/
- **httpx Documentation:** https://www.python-httpx.org/
- **Groq API:** https://console.groq.com/docs
- **OpenAI API:** https://platform.openai.com/docs
- **Azure OpenAI:** https://learn.microsoft.com/azure/ai-services/openai/

---

## Project Status

✅ **Production-ready**  
✅ **Provider-agnostic**  
✅ **Well-documented**  
✅ **Type-safe**  
✅ **Async throughout**  
✅ **Tested and working**

---

**Ready to build with any LLM provider! 🚀**
