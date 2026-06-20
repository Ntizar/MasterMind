# Nan API — Reranker

## Estado (2026-06-11)

**El endpoint `/rerank` de Nan API devuelve 404.** La documentación existe en `https://nan.builders/docs/examples#rerank` pero el endpoint no está activo.

## Lo que se sabe

- **Modelo mencionado:** `qwen3-reranker-8B` (anunciado en post de Nan)
- **Endpoint:** `POST https://api.nan.builders/v1/rerank`
- **Payload:** `{"model": "rerank", "query": "...", "documents": ["...", "..."]}`
- **Respuesta esperada:** `results[]` ordenados por `relevance_score` desc, con `index` original
- **Compatible con:** OpenAI client (`client.post(path="/rerank", ...)`) y curl directo
- **Propósito:** reranking semántico — reordena documentos ya recuperados por un embedding search

## Modelos disponibles (2026-06-11)

```
qwen3.6, deepseek-v4-flash, whisper, gemma4, mimo-v2.5, kokoro, qwen3-embedding
```

**Ninguno de ellos es un reranker.** El reranker no aparece en `/v1/models`.

## Diferencia con embeddings

- **Embeddings:** convierten texto a vector 4096-dim para búsqueda por similitud (fase 1 de RAG)
- **Reranker:** recibe query + lista de documentos, devuelve ranking con scores de relevancia (fase 2 de RAG)
- **No son reemplazables:** se usan en conjunto — embeddings para recuperar candidatos, reranker para ordenarlos

## Plan

- Cuando Nan active el endpoint, añadir reranking como segundo paso en `consultar-skills.py`:
  1. ChromaDB query → top-10 resultados
  2. Extraer descripciones completas
  3. Enviar a `/rerank` con la query original
  4. Reordenar resultados por `relevance_score`
- Esto mejora la precisión del top-N
