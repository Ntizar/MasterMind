# Model Context Limits — Tabla de referencia

## Context windows y chars efectivos

"Chars efectivos" = cuántos caracteres de español caben en el contexto, descontando ~20% para prompt + respuesta.

| Modelo | Provider | Contexto (tokens) | Chars efectivos | PDFs típicos | RAM |
|--------|----------|-------------------|-----------------|--------------|-----|
| llama3.1:8b | Ollama local | 8K | ~24K chars | 5-10 páginas | 6GB |
| qwen2.5:7b | Ollama local | 32K | ~96K chars | 15-30 páginas | 6GB |
| qwen2.5:14b | Ollama local | 32K | ~96K chars | 15-30 páginas | 12GB |
| qwen2.5:32b | Ollama local | 32K | ~96K chars | 15-30 páginas | 20GB |
| mistral:7b | Ollama local | 32K | ~96K chars | 15-30 páginas | 6GB |
| gemma2:9b | Ollama local | 8K | ~24K chars | 5-10 páginas | 8GB |
| gpt-4o-mini | OpenAI | 128K | ~384K chars | 100+ páginas | 0 (API) |
| gpt-4o | OpenAI | 128K | ~384K chars | 100+ páginas | 0 (API) |
| claude-3.5-sonnet | Anthropic | 200K | ~600K chars | 150+ páginas | 0 (API) |
| qwen3.6 | NaN Builders | 128K | ~384K chars | 100+ páginas | 0 (API) |

## Fórmula de estimación

```
En español: 1 token ≈ 3.5 caracteres (estimación conservadora)
En inglés: 1 token ≈ 4 caracteres

Chars caben = (context_window × 0.80) × 3.5
```

Ejemplo: qwen2.5:7b con 32K context → 32000 × 0.80 × 3.5 = **89,600 chars**

## Cuándo necesitas chunking

```
Si chars_pdf > chars_efectivos → necesita chunking
Si chars_pdf < chars_efectivos → proceso directo (mejor calidad)
```

## Velocidad típica por modelo

| Modelo | Hardware | Velocidad por PDF (20K chars) |
|--------|----------|------------------------------|
| 7B Q4 | GPU RTX 3060 | 10-20s |
| 7B Q4 | CPU (8 cores) | 60-120s |
| 7B Q4 | CPU (4 cores) | 120-300s |
| 32B Q4 | GPU RTX 4090 | 30-60s |
| API (OpenAI/NaN) | N/A | 5-15s |

## Recomendaciones por caso de uso

| Caso | Modelo recomendado | Alternativa |
|------|-------------------|-------------|
| Extracción simple (5-10 campos) | qwen2.5:7b | llama3.1:8b |
| Extracción compleja (15+ campos) | qwen2.5:32b | gpt-4o-mini |
| Batch >100 PDFs | API (NaN/OpenAI) | qwen2.5:7b + GPU |
| Sin GPU | API o 7B Q4 CPU | qwen2.5:7b Q3_K_M |
| Offline/sin internet | Ollama local | llama.cpp |
