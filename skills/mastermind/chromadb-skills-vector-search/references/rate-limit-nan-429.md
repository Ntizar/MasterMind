# Rate Limit 429 en NaN API — Recuperación

## El problema

NaN API tiene dos rate limits:
- **60 requests/minuto** por API key
- **3 requests paralelos** máximo

Cuando indexas 190+ skills, cada uno requiere una llamada a `qwen3-embedding`. A partir del skill ~60, empiezan los 429.

## Síntomas

```
ERROR embedding: 429 {"error":{"message":"Rate limit exceeded for api_key: ... 
  Limit type: requests. Current limit: 60, Remaining: 0. 
  Limit resets at: 2026-06-10 07:31:39 UTC"}}
```

## Solución

### 1. Indexación inicial (script con delay anti-rate-limit)

El script `indexar-skills.py` incluye delay de 1.5s entre embeddings (desde 2026-06-10).
Aun así, puede alcanzar el límite. Los skills que fallan se saltan.

### 2. Re-indexar skills fallados

Verificar qué falta:
```bash
bash /hermes-home/skills/mastermind/chromadb-skills-vector-search/scripts/verify-index.sh
```

Re-indexar manualmente con `/opt/hermes/.venv/bin/python3` y delay de 1.5s entre calls.

### 3. Esperar a que se resetee

El rate limit se resetea **1 minuto después del primer 429**. Esperar 60s y re-ejecutar.

### 4. Prevención

- El delay de 1.5s en `indexar-skills.py` reduce significativamente los 429
- No ejecutar indexación masiva más de una vez al día
- El cron semanal (domingo 04:00 UTC) está fuera de horas pico
- Si solo cambian 1-2 skills, indexar solo esos individualmente

## Nota

El rate limit es por API key, no por IP. Compartes el límite con cualquier otro proceso que use la misma key (ej: el modelo qwen3.6 para respuestas de Mastermind). Si Mastermind está muy activo, puede consumir parte del rate limit y dejar menos para embeddings.