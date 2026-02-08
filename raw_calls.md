# Groq API - Raw curl Examples

This document shows how to call Groq API directly using curl commands. These examples demonstrate the OpenAI-compatible API format that our application uses.

---

## 1. List Available Models

Get a list of all available models on Groq.

### Request

```bash
curl --location 'https://api.groq.com/openai/v1/models' \
  --header 'Authorization: Bearer YOUR_GROQ_API_KEY' \
  --header 'Content-Type: application/json'
```

### Response (Sample)

```json
{
  "object": "list",
  "data": [
    {
      "id": "moonshotai/kimi-k2-instruct-0905",
      "object": "model",
      "created": 1234567890,
      "owned_by": "groq"
    },
    {
      "id": "llama-3.3-70b-versatile",
      "object": "model",
      "created": 1234567890,
      "owned_by": "groq"
    },
    {
      "id": "mixtral-8x7b-32768",
      "object": "model",
      "created": 1234567890,
      "owned_by": "groq"
    }
  ]
}
```

### Notes

- **Endpoint:** `https://api.groq.com/openai/v1/models`
- **Method:** GET
- **Authentication:** Bearer token in Authorization header
- **Response:** List of available models with their IDs

### Use Case

Use this endpoint to:
- Discover available models
- Verify your API key is working
- Get exact model IDs for use in chat completions

---

## 2. Chat Completions

Generate AI responses using the chat completions endpoint.

### Request

```bash
curl --location 'https://api.groq.com/openai/v1/chat/completions' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer YOUR_GROQ_API_KEY' \
  --data '{
    "model": "moonshotai/kimi-k2-instruct-0905",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Explain recursion in one paragraph."
      }
    ],
    "temperature": 0.7,
    "max_tokens": 512
  }'
```

### Response (Sample)

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "moonshotai/kimi-k2-instruct-0905",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Recursion is a programming technique where a function calls itself to solve a problem by breaking it down into smaller, similar subproblems. Each recursive call works on a progressively simpler version of the original problem until reaching a base case—a condition that stops the recursion and provides a direct answer. The function then combines the results from these calls as it returns up the chain, ultimately solving the original problem. While powerful for tasks like traversing trees or computing factorials, recursion requires careful design to avoid infinite loops and stack overflow errors."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 32,
    "completion_tokens": 108,
    "total_tokens": 140
  }
}
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | ✅ Yes | Model identifier (e.g., `moonshotai/kimi-k2-instruct-0905`) |
| `messages` | array | ✅ Yes | Array of message objects with `role` and `content` |
| `temperature` | number | ❌ No | Sampling temperature (0.0 to 2.0). Higher = more creative. Default: 0.7 |
| `max_tokens` | integer | ❌ No | Maximum tokens to generate. Default: varies by model |
| `top_p` | number | ❌ No | Nucleus sampling (0.0 to 1.0). Alternative to temperature |
| `n` | integer | ❌ No | Number of completions to generate. Default: 1 |
| `stream` | boolean | ❌ No | Whether to stream responses. Default: false |
| `stop` | string/array | ❌ No | Stop sequences to halt generation |

### Message Roles

- **`system`** - Sets the assistant's behavior and context
- **`user`** - User's input/question
- **`assistant`** - AI's previous responses (for multi-turn conversations)

### Notes

- **Endpoint:** `https://api.groq.com/openai/v1/chat/completions`
- **Method:** POST
- **Authentication:** Bearer token in Authorization header
- **Format:** OpenAI-compatible API format
- **Response:** Generated text with usage statistics

### Use Case

This is the main endpoint for:
- Generating AI responses
- Building chatbots
- Q&A systems
- Text generation tasks

---

## How Our Application Uses These APIs

### In `app/services/llm_client.py`

```python
async def generate(self, prompt: str) -> str:
    """Generate response from LLM."""
    
    response = await self.client.post(
        f"{self.base_url}/v1/chat/completions",  # Chat completions endpoint
        headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}  # Simple user prompt
            ],
        },
        timeout=self.timeout,
    )
    
    data = response.json()
    return data["choices"][0]["message"]["content"]
```

Our application:
1. Takes a user prompt
2. Wraps it in OpenAI message format
3. Sends to Groq's chat completions endpoint
4. Extracts the response text
5. Returns to user

---

## Getting Your API Key

### Groq (Free Tier Available)

1. Visit: https://console.groq.com/
2. Sign up for an account
3. Navigate to **API Keys** section
4. Click **Create API Key**
5. Copy your key (starts with `gsk_...`)
6. Add to `.env` file:
   ```env
   LLM_API_KEY=gsk_your_key_here
   LLM_BASE_URL=https://api.groq.com/openai
   LLM_MODEL=moonshotai/kimi-k2-instruct-0905
   LLM_PROVIDER=groq
   ```

---

## Available Groq Models

| Model ID | Description | Context Length |
|----------|-------------|----------------|
| `moonshotai/kimi-k2-instruct-0905` | Kimi K2 - Multilingual, high quality | 128K tokens |
| `llama-3.3-70b-versatile` | Llama 3.3 70B - Very capable, versatile | 128K tokens |
| `llama-3.1-70b-versatile` | Llama 3.1 70B - Previous version | 128K tokens |
| `mixtral-8x7b-32768` | Mixtral 8x7B - Fast, efficient | 32K tokens |
| `gemma-2-9b-it` | Gemma 2 9B - Instruction tuned | 8K tokens |

---

## Testing Groq API Directly

### Quick Test (List Models)

```bash
# Replace YOUR_API_KEY with your actual key
export GROQ_API_KEY="gsk_your_key_here"

curl --location 'https://api.groq.com/openai/v1/models' \
  --header "Authorization: Bearer $GROQ_API_KEY" \
  --header 'Content-Type: application/json'
```

### Quick Test (Chat Completion)

```bash
export GROQ_API_KEY="gsk_your_key_here"

curl --location 'https://api.groq.com/openai/v1/chat/completions' \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $GROQ_API_KEY" \
  --data '{
    "model": "moonshotai/kimi-k2-instruct-0905",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## OpenAI Compatibility

Groq's API is **100% compatible** with OpenAI's API format. This means:

✅ Same endpoint structure (`/v1/chat/completions`)  
✅ Same request format (messages, model, parameters)  
✅ Same response format (choices, usage, etc.)  
✅ Can use OpenAI libraries with just a base URL change

### Example: Switch from OpenAI to Groq

**OpenAI:**
```bash
curl https://api.openai.com/v1/chat/completions \
  --header "Authorization: Bearer sk-..." \
  --data '{"model": "gpt-4o", "messages": [...]}'
```

**Groq (Same Format!):**
```bash
curl https://api.groq.com/openai/v1/chat/completions \
  --header "Authorization: Bearer gsk_..." \
  --data '{"model": "moonshotai/kimi-k2-instruct-0905", "messages": [...]}'
```

Only 2 changes needed:
1. Base URL: `api.openai.com` → `api.groq.com/openai`
2. Model: `gpt-4o` → `moonshotai/kimi-k2-instruct-0905`

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Solution |
|------|---------|----------|
| `200` | Success | Request processed successfully |
| `400` | Bad Request | Check request format, parameters |
| `401` | Unauthorized | Verify API key is correct |
| `429` | Rate Limited | Slow down requests, check rate limits |
| `500` | Server Error | Groq service issue, retry later |

### Example Error Response

```json
{
  "error": {
    "message": "Invalid API key provided",
    "type": "invalid_request_error",
    "code": "invalid_api_key"
  }
}
```

---

## Rate Limits (Groq Free Tier)

Groq's free tier typically includes:
- **Requests per minute:** Varies by model
- **Tokens per minute:** Varies by model
- **Daily limits:** Check your console dashboard

For production use, consider upgrading to a paid plan.

---

## Additional Resources

- **Groq API Documentation:** https://console.groq.com/docs
- **Groq Console:** https://console.groq.com/
- **OpenAI API Reference:** https://platform.openai.com/docs/api-reference
- **Our Application README:** See `README.md` for setup instructions

---

## Security Notes

⚠️ **Never commit API keys to git!**

✅ Always use environment variables  
✅ Store keys in `.env` file (git-ignored)  
✅ Rotate keys regularly  
✅ Don't share keys in screenshots or logs  
✅ Use different keys for dev/prod

---

## Summary

These raw curl examples show:
1. How to list available models
2. How to generate chat completions
3. The OpenAI-compatible format Groq uses
4. How our application wraps these API calls

Our FastAPI application abstracts these raw API calls into a simple REST endpoint, making it easy to:
- Switch between providers (Groq, OpenAI, Azure)
- Handle authentication automatically
- Provide a consistent interface
- Add error handling and validation

---

**Use these examples to test Groq API directly or understand how the application works under the hood!** 🚀
