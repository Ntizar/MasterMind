---
name: chromadb-skills-vector-search
description: "Búsqueda semántica de skills con ChromaDB + qwen3-embedding. Indexación, consulta, re-indexación y mantenimiento de la colección mastermind-skills."
version: "1.1.0"
tags: [chromadb, vector-search, skills, embedding, qwen3]
---

# ChromaDB — Búsqueda Semántica de Skills

## Resumen

Colección ChromaDB `mastermind-skills` en `localhost:8000` con embeddings `qwen3-embedding` (4096 dims). Indexa todos los skills de `/hermes-home/skills/`.

## Configuración

- **URL:** `http://localhost:8000`
- **Colección:** `mastermind-skills`
- **Modelo:** `qwen3-embedding` (NaN API)
- **Venv:** `/hermes-home/chromadb-venv/`
- **Scripts:** `/hermes-home/scripts/indexar-skills.py`, `/hermes-home/scripts/consultar-skills.py`
- **Cron:** `chromadb-reindex-semanal` (domingo 04:00 UTC)

## Flujo de carga de skills

1. Al recibir una petición del usuario, ejecutar ANTES de `skill_view()`:
   ```bash
   cd /hermes-home/scripts && NAN_API="$NAN_API" /hermes-home/chromadb-venv/bin/python consultar-skills.py "PALABRAS_CLAVE" --json
   ```
2. Filtrar con score > 0.25 (⚠️ threshold bajo: qwen3-embedding rara vez da >0.5 incluso para skills muy relevantes)
3. Cargar SOLO los skills relevantes con `skill_view()`
4. **Fallback:** Si ChromaDB no responde, ejecutar `bash /hermes-home/scripts/start-chromadb.sh` y reintentar

## Re-indexación

```bash
bash /hermes-home/scripts/run-start-chromadb.sh && bash /hermes-home/scripts/run-indexar-skills.sh
```

El cron job `chromadb-reindex-semanal` ejecuta lo mismo cada domingo 04:00 UTC.

## Pitfalls

- **Usar SIEMPRE el venv Python para scripts de ChromaDB:** `/hermes-home/chromadb-venv/bin/python`, NUNCA `python3` del sistema. Los wrappers (`run-indexar-skills.sh`, `run-start-chromadb.sh`) deben usar la ruta absoluta del venv.
  - Ejemplo de bug: `run-indexar-skills.sh` con `python3` → `ModuleNotFoundError: No module named 'chromadb'`
  - Fix: cambiar `python3 indexar-skills.py` → `/hermes-home/chromadb-venv/bin/python indexar-skills.py`
- **ChromaDB ya puede estar corriendo:** `run-start-chromadb.sh` lo detecta y no se bloquea. OK.
- **qwen3-embedding threshold:** scores > 0.5 son raros. No filtrar agresivamente.
- **Re-indexación completa vs incremental:** `indexar-skills.py` detecta automáticamente nuevos skills (por ID) e indexa solo los nuevos. No necesita borrar la colección.

## Archivos de referencia

- `references/count-skills.sh` — Script rápido para contar skills en el directorio vs ChromaDB
