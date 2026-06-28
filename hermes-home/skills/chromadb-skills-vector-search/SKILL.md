---
name: chromadb-skills-vector-search
description: "Búsqueda semántica de skills con ChromaDB + qwen3-embedding — indexación, consulta, re-indexación y troubleshooting del servicio."
version: "1.0.0"
tags: [chromadb, vector-search, skills, embedding, qwen3]
author: Ntizar + Hermes Agent
---

# ChromaDB Skills Vector Search

Búsqueda semántica de skills usando ChromaDB con embeddings de `qwen3-embedding` (4096 dims) vía NaN API.

## Arquitectura

- **Servidor:** ChromaDB en `localhost:8000`
- **Colección:** `mastermind-skills`
- **Modelo:** `qwen3-embedding` (NaN API, 4096 dims)
- **Venv:** `/hermes-home/chromadb-venv/`
- **Datos persistentes:** `/hermes-home/chromadb-data/`
- **Scripts:**
  - `consultar-skills.py` — Consulta semántica
  - `indexar-skills.py` — Indexación / re-indexación
  - `start-chromadb.sh` — Arranque del servicio

## Flujo de uso (OBLIGATORIO antes de cargar skills)

1. **Consultar ChromaDB** antes de `skill_view()`:
   ```bash
   cd /hermes-home/scripts && NAN_API="$NAN_API" /hermes-home/chromadb-venv/bin/python consultar-skills.py "PALABRAS_CLAVE" --json
   ```
2. **Filtrar resultados** con score > 0.25 (⚠️ threshold bajo: qwen3-embedding rara vez da >0.5 incluso para skills muy relevantes)
3. **Cargar SOLO esos skills** con `skill_view()`
4. **Fallback:** Si ChromaDB no responde o no hay resultados > 0.25, cargar por dominio desde `available_skills`

## Auto-start

Si ChromaDB no responde, ejecutar:
```bash
bash /hermes-home/scripts/start-chromadb.sh
```

Verificar que responde:
```bash
curl -s http://localhost:8000/api/v1/version
# → "1.5.9"
```

## Re-indexación

### Manual
```bash
cd /hermes-home/scripts && NAN_API="$NAN_API" /hermes-home/chromadb-venv/bin/python indexar-skills.py --reset
```

### Cron semanal
`chromadb-reindex-semanal` — domingo 04:00 UTC. Verificar `last_status: "ok"` en `hermes cron list`.

## Pitfalls

- **ChromaDB NO sobrevive a reinicios de VM.** Tras reinicio de NaN, ejecutar `start-chromadb.sh`. Los datos persisten en `/hermes-home/chromadb-data/`.
- **Re-indexación lenta:** ~20 min para 241 skills (qwen3-embedding, 4096 dims). No usar timeout < 300s. Preferir `background=true` con `notify_on_complete`.
- **Skills duplicados:** El script encuentra 241 SKILL.md pero puede indexar menos si hay nombres duplicados (ej. `static-digest-pipeline` aparece en dos categorías). Verificar el conteo final vs el de encontrados.
- **NAN_API debe estar set:** La variable de entorno `NAN_API` es necesaria para el embedding. Si falta, los embeddings fallan silenciosamente.
- **Threshold de 0.25:** qwen3-embedding da scores bajos. 0.25 es el umbral mínimo; no filtrar agresivamente.
- **Colección se destruye con --reset:** El flag `--reset` elimina la colección existente y la recrea. No hay rollback.

## Performance

- **Tiempo por embedding:** ~2-5 segundos (promedio ~3s)
- **Tiempo total 241 skills:** ~20 minutos
- **Batches de inserción:** 10 skills por lote HTTP POST
- **Lotes totales para 241:** 24 lotes

## Referencias

- `references/reindex-procedures.md` — Procedimientos detallados de re-indexación con logs y métricas
