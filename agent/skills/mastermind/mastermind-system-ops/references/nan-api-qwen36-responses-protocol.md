# NaN API: crons con qwen3.6 fallan por protocolo /responses (verificado 2026-09-05)

## Síntoma

Crons con `model: qwen3.6` revientan con:
```
RuntimeError: Invalid API response after 3 retries: response time 32.3s
```
y recorren la racha (Informe presidencial 08:00, Consejo de Ministros 22:00, kit72h-editor 04:30
fallaron en cadena). El `vigia-cron` alerta de fallos nuevos. En `logs/agent.log` la firma es:
```
WARNING agent.conversation_loop: Codex response.output is empty after stream backfill (status=completed, incomplete_details=None, model=qwen3.6). api_mode=codex_responses provider=openai-api
WARNING agent.conversation_loop: Invalid API response (retry 1/3): response.output is empty | Provider: model=qwen3.6
ERROR  agent.conversation_loop: Invalid API response after 3 retries.
```
Nota: los crons con `qwen3.8-flash` / `deepseek-v4-flash` en la MEDIA conexión `openai-api`
NUNCA caen. Solo caen los de `qwen3.6`.

## NO es la causa (descartado)

- **NO es límite de tokens.** NaN no corta por `max_tokens` de esa forma con `qwen3.6`.
- **NO es el cómo se escribe el modelo.** `qwen3.6` es un id válido en `/v1/models`.
  El id interno que NaN devuelve en `response.model` (`qwen3.6-35b-a3b-nvfp4`) NO es un modelo
  accesible → 401 `This API key does not have access to the requested model`.
- **NO es un pico transitorio.** Reintentar el run falla siempre (25-45s, mismo error).

## Causa raíz

El provider `openai-api` del overlay built-in de Hermes (`hermes_cli/providers.py`, línea 68)
declara `transport="codex_responses"` → `determine_api_mode("openai-api", ...)` devuelve
`codex_responses` SIEMPRE, porque `host_mandated_api_mode("https://api.nan.builders/v1")`
devuelve `None` (NaN NO es host oficial OpenAI/Meta/Anthropic) y cae al overlay.

Resultado: Hermes le habla a NaN por la **Responses API** (`/v1/responses`), un protocolo que
NaN implementa solo a medias para `qwen3.6`. En el stream, **NaN NO emite el evento de cierre
`response.output_text.done`** (ni `response.output_item.done` ni `response.content_part.done`)
para `qwen3.6` → Hermes hace "stream backfill" para reconstruir el `message` → queda vacío →
"response.output is empty" → 3 retries → FAIL.

### Evidencia: secuencia de eventos stream `/responses`

Comparar (directo contra `https://api.nan.builders/v1/responses`, streaming):

| Evento | `qwen3.8-flash` ✓ | `qwen3.6` ✗ |
|---|---|---|
| `response.output_text.delta` | sí | sí |
| `response.output_text.done` | **sí** | **NO** |
| `response.output_item.done` | sí | NO |
| `response.content_part.done` | sí | NO |
| `response.completed` | sí | sí |

Por eso `qwen3.8-flash` funciona y `qwen3.6` no en la ruta `/responses`.

### En chat_completions TODO funciona

`qwen3.6` por `/v1/chat/completions` con contexto grande responde perfecto:
`content=598 reasoning=2227 finish=stop` en ~8s. El protocolo correcto es `chat_completions`.

## Fix

Forzar el protocolo correcto vía config (el campo `model.api_mode` es reconocido por
`_resolve_plain_custom_api_mode` en `runtime_provider.py` para providers no-`custom`):

```bash
hermes config set model.api_mode chat_completions
# verificar
hermes config get model.api_mode   # -> chat_completions
```

### Verificación del fix (pasar de codex_stream_request a chat_completion_request)

Relanzar el job y mirar `logs/agent.log`:
```bash
# ANTES (falla):
run_agent: OpenAI client created (codex_stream_request, shared=False) ... model=qwen3.6
# DESPUÉS (funciona):
run_agent: OpenAI client created (chat_completion_request, shared=False) ... model=qwen3.6
```
Las llamadas van con `latency` 2-7s y `cache=` 50-97%, sin "Invalid API response".

Adjuntar NB: qwen3.6 sigue siendo modelo de razonamiento — el razonamiento va en
`reasoning_content` y el content final en `content`. No confundir `reasoning_content` vacío
con fallo; en `chat_completions` con max_tokens>=8000 ambos se llenan bien.

## Referencia de código consultada

- `hermes_cli/providers.py` línea 68: overlay `openai-api` con `transport="codex_responses"`.
- `hermes_cli/providers.py` `determine_api_mode()`: devuelve `codex_responses` para `openai-api`.
- `hermes_cli/runtime_provider.py` `_resolve_plain_custom_api_mode()`: honra `model.api_mode`.
- `hermes_cli/runtime_provider.py` línea ~1418: para provider no-custom, `api_mode` =
  `_parse_api_mode(model_cfg.get("api_mode"))` o `_detect_api_mode_for_url(base_url)` o
  `"chat_completions"`.
- `cron/scheduler.py` `_resolve_job_reasoning_config`: soporta `reasoning_effort: none`
  (→ `{enabled: false}`) por job; útil si se quiere desactivar el razonamiento en crons.
