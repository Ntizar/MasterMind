# ChromaDB Reindexación 2026-06-10

## Resumen
- **Skills indexados:** 189/191 SKILL.md
- **Tiempo:** ~3 min (con rate limits)
- **Rate limits 429:** Sí, 23 requests rechazados por `max_parallel_requests` (límite 3 concurrentes)
- **Solución aplicada:** Delay de 1.5s entre embeddings en `indexar-skills.py`

## Problemas encontrados
1. **`python3` del sistema no tiene `requests`** — el paquete `python3-requests` estaba corrupto (marcado como instalado pero archivos faltaban). Se usa `/opt/hermes/.venv/bin/python3` para ejecutar los scripts.
2. **Rate limit 429** — NaN API permite solo 3 requests paralelos. El script original no tenía delay entre embeddings.
3. **Nombres de directorio vs frontmatter** — algunos skills tienen nombres de directorio diferentes al nombre del frontmatter (ej: `creative-ideation/` → `ideation`). El sistema funciona correctamente porque usa el nombre del frontmatter.

## Cambios realizados
- `indexar-skills.py`: añadido `import time` y delay de 1.5s entre embeddings
- Reindexación de 9 skills que fallaron por rate limit (completados con script dedicado)

## Verificación
- Consulta prueba "dashboard energía eléctrica": top 3 con scores 0.6033, 0.6012, 0.5947 (todos > 0.5) ✅
- ChromaDB corriendo en localhost:8000 ✅
