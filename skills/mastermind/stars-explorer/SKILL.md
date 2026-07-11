---
name: stars-explorer
description: Pipeline de exploración nocturna de GitHub stars de David — fetch, análisis, creación de skills desde patrones detectados.
category: mastermind
---

# Stars Explorer — Pipeline de Exploración de GitHub Stars

## Qué hace

Ejecuta el pipeline que explora los repos que David ha starred en GitHub, extrae patrones arquitectónicos, y genera skills automáticas para los repos con valor.

## Flujo

1. Ejecutar: `bash /hermes-home/scripts/run-stars-explorer.sh --batch 15`
2. Leer el output JSON (o stdout con `--json`)
3. Para cada repo, decidir si merece skill:
   - Patrón arquitectónico interesante → crear skill
   - Librería/herramienta útil para proyectos de David → crear skill
   - Repo de referencia (three.js, d3, etc.) → crear skill de patrón
   - Skip (juego, config personal, fork sin cambios, too niche) → marcar skip
   - Ya existe skill similar → marcar reference
4. Si se crearon skills → re-indexar ChromaDB
5. Guardar resumen en `notes/` si hubo hallazgos significativos

## Ejecución

```bash
# Batch normal (default 15 repos)
bash /hermes-home/scripts/run-stars-explorer.sh --batch 15

# JSON limpio para consumo programático
source /hermes-home/.env && export GITHUB_TOKEN NAN_API
python3 /hermes-home/scripts/explorar-stars.py --batch 15 --json

# Status del registry
python3 /hermes-home/scripts/explorar-stars.py --status

# Reprocesar un repo específico
python3 /hermes-home/scripts/explorar-stars.py --reprocess user/repo

# Incluir propios repos
python3 /hermes-home/scripts/run-stars-explorer.sh --include-own
```

## Criterio de creación de skills — AGRESIVO

- Umbral MUY BAJO: si el repo tiene algo remotamente útil, CREAR el skill
- NO ser conservador. David quiere que el sistema crezca rápido.
- Cada skill debe tener: frontmatter YAML, descripción clara, código de ejemplo, pitfalls, referencias
- Categoría: según dominio (geospatial, creative, data-science, devops, ia, etc.)

## Pitfalls

### `description: null` crasha el script

La API de GitHub envía `description: null` (no `"description": ""`) para repos sin descripción. Esto causa `TypeError: 'NoneType' object is not subscriptable` al hacer `r['description'][:100]`.

**Fix aplicado:** En `explorar-stars.py`:
- Línea 139: `repo_data.get("description") or ""` (en vez de `.get("description", "")`)
- Línea 390: `(r.get('description') or '(none)')[:100]` (en vez de `r['description'][:100] or '(none)'`)

### Rate limiting de GitHub API

El script maneja rate limiting automáticamente (403 → return None), pero si se agota el token, el batch se corta. Verificar con `--status` después.

### Script puede tardar 60-120s

El fetch de la API de GitHub es lento (1s de delay entre repos). Ser paciente, no matar el proceso.

### Registry path

El registry se guarda en `/hermes-home/data/stars-registry.json`. Se puede sobrescribir con la variable `STARS_REGISTRY`.

## Estado actual

- Total repos procesados: ~234
- Total runs: ~19
- Total skills generadas: ~44
- Repos pendientes: ~0

## Referencias

- Script principal: `/hermes-home/scripts/explorar-stars.py`
- Wrapper: `/hermes-home/scripts/run-stars-explorer.sh`
- Registry: `/hermes-home/data/stars-registry.json`
