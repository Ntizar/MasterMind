# Multi-Backend LLM Pattern — Cliente unificado

## El problema

Cada proveedor de LLM tiene su propia API. OpenAI, Ollama, llama.cpp, vLLM, NaN Builders — todos diferentes. Si hardcodeas un proveedor, quedas atrapado.

## La solución: formato OpenAI-compatible

Todos los proveedores modernos implementan `/v1/chat/completions` con el mismo formato de request/response. El truco es usar UN cliente que funcione con todos:

```python
import requests

class LLMClient:
    def __init__(self, api_url, api_key="", model="default"):
        self.api_url = api_url
        self.api_key = api_key
        self.model = model

    def extract_json(self, text, schema_desc):
        messages = [{"role": "user", "content": prompt}]
        resp = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "messages": messages, "temperature": 0.1},
            timeout=180,
        )
        return resp.json()["choices"][0]["message"]["content"]
```

## Endpoints por proveedor

| Proveedor | API URL | API Key | Health Check |
|-----------|---------|---------|-------------|
| Ollama | `http://localhost:11434/v1/chat/completions` | "" (vacío) | `GET /api/tags` |
| llama.cpp | `http://localhost:8080/v1/chat/completions` | "" (vacío) | `GET /v1/models` |
| vLLM | `http://localhost:8000/v1/chat/completions` | "" (vacío) | `GET /v1/models` |
| OpenAI | `https://api.openai.com/v1/chat/completions` | `sk-xxx` | `GET /v1/models` |
| NaN Builders | `https://api.nan.builders/v1/chat/completions` | `$NAN_API` | `GET /v1/models` |
| Custom | Cualquier URL | Cualquier key | `GET /v1/models` |

## Pitfalls por proveedor

### Ollama
- El health check NO es `/v1/models` sino `/api/tags`
- El modelo debe estar descargado antes de usarlo: `ollama pull qwen2.5:7b`
- No soporta `max_tokens` — lo ignora silenciosamente
- El timeout por defecto es largo (120s para modelos grandes)
- `temperature: 0` causa respuestas repetitivas — usar 0.1

### llama.cpp
- El modelo se carga al iniciar el server, no on-demand
- Si el modelo es más grande que la RAM, el server no arranca
- `max_tokens` se llama `n_predict` en algunos builds
- No soporta `system` message en todos los builds — usar solo `user`

### OpenAI
- `max_tokens` está deprecado — usar `max_completion_tokens`
- Los precios varían mucho por modelo
- Rate limits: 3 RPM en free tier, 500+ en paid

### NaN Builders
- Similar a OpenAI pero con modelos open-source
- Rate limits menos estrictos
- Algunos modelos no están siempre disponibles

## Retry y error handling

```python
for attempt in range(3):
    try:
        resp = requests.post(..., timeout=180)
        if resp.status_code == 429:
            time.sleep(int(resp.headers.get("Retry-After", 5)))
            continue
        if resp.status_code != 200:
            raise Exception(f"API {resp.status_code}")
        return resp.json()
    except requests.exceptions.ConnectionError:
        raise Exception("¿Está el servidor ejecutándose?")
    except requests.exceptions.Timeout:
        time.sleep(2 ** attempt)  # Backoff exponencial
```
