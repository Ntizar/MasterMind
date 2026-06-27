# Batch Processing Notes — CIAF PDFs

## Datos del batch
- **Fecha:** 2026-06-27
- **PDFs procesados:** 38 (2017-2025)
- **Resultado:** 38/38 exitosos (100%)
- **Tiempo total:** ~11 minutos
- **Modelo:** Qwen 3.6 vía NaN API

## Errores encontrados y fixes

### 1. `span["text"]` returning None (10 PDFs)
- **Causa:** PyMuPDF retorna `None` en `span["text"]` para algunos PDFs
- **Error:** `TypeError: can only concatenate str (not "NoneType") to str`
- **Fix:** `span.get("text") or ""` en lugar de `span["text"]`
- **Recuperación:** 8/10 exitosos al reintentar con fix

### 2. LLM returning empty content (2 PDFs)
- **Causa:** PDFs con contenido tricky (tablas complejas, formato unusual)
- **Fix:** Verificar `content = ... or ""` y retry con texto truncado a 20K
- **PDFs afectados:** `211125-200605-if-sn_ciaf.pdf`, `2024-122-1213-if.pdf`

### 3. PyMuPDF API changes
- `numPages` → `len(doc)` (propiedad eliminada en v1.24+)
- `destroy()` → `close()` (método eliminado)
- Afecta: scripts que usan la API antigua

### 4. Python output buffering
- Background processes con `terminal(background=True)` no muestran output
- Fix: `PYTHONUNBUFFERED=1` o `sys.stdout.flush()` after print

## Estadísticas por año
- 2025: 1 PDF
- 2024: 3 PDFs
- 2023: 3 PDFs
- 2022: 5 PDFs
- 2021: 6 PDFs
- 2020: 3 PDFs
- 2019: 3 PDFs
- 2018: 2 PDFs
- 2017: 12 PDFs

## Estadísticas por tipo
- Incidente: 18
- Accidente: 19
- Colisión con obstáculo y descarrilamiento: 1

## Comparativa v2.0 (regex) vs v3.0 (LLM)

| Campo | v2.0 regex | v3.0 LLM |
|-------|-----------|----------|
| Conclusiones | 16/38 (42%) | 38/38 (100%) |
| Recomendaciones | 18/38 (47%) | 36/38 (95%) |
| Trenes | 0/38 (0%) | 38/38 (100%) |
| Víctimas | 0 total | 200 total |
| Texto limpio | Parcial | Literal |

## Scripts utilizados
- `test-pipeline.py` — Test individual con 3 PDFs
- `batch-ciaf.py` — Batch processor principal
- `reprocess-failed.py` — Reproceso de fallos con NoneType fix

## Output
- 38 JSONs individuales en `data/individual/`
- `data/reports.json` consolidado (157KB)
- `dashboard/data/reports.json` copia para dashboard
