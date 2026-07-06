---
name: eravisor-pipeline
description: Pipeline automatizado para extraer, clasificar y visualizar informes de accidentes ferroviarios de la Agencia Ferroviaria de la UE (ERA), clasificados según el Anexo III del RD 929/2020.
version: "1.0.0"
---

# eravisor-pipeline — Pipeline de datos ERA Europa

## Resumen

Pipeline automatizado para extraer, clasificar y visualizar informes de accidentes ferroviarios de la Agencia Ferroviaria de la UE (ERA), clasificados según el Anexo III del RD 929/2020.

## Ubicación

- **Script:** `/root/workspace/ERAVisor/scripts/pipeline_europa.py`
- **Datos:** `/root/workspace/ERAVisor/data/`
- **PDFs:** `/root/workspace/ERAVisor/pdfs/{pais}/`
- **Visor:** `/root/workspace/ERAVisor/visor/`
- **Repo:** `github.com/Ntizar/ERAVisor` (público, GitHub Pages)

## Fases del pipeline

1. **Cargar índices** — Lee JSONs pre-cacheados (`data/*-investigations-index.json`)
2. **Descargar PDFs** — Batch de 10, con delays anti-429
3. **Extraer con LLM** — Batch de 5, qwen3.6 clasifica según Anexo III
4. **Exportar** — CSV + Excel + JSON por país
5. **Generar visor** — Combina todos los países en `visor/datos.js`

## Estado persistente

La fuente de verdad es el **disco**: `cargar_estado()` cuenta archivos `.pdf` en `pdfs/{pais}/`.

## Pitfalls

### Drupal 11 — No hacer scraping de ERA
ERA es un Drupal 11 con carga JS. **No se pueden extraer PDFs con requests + regex del HTML**. Usar índices JSON pre-cacheados.

### Rate limiting agresivo
ERA devuelve **429 después de ~50 peticiones**. Delays de **30-150s** entre descargas, batches pequeños.

### PYTHONUNBUFFERED para background
```bash
PYTHONUNBUFFERED=1 python3 scripts/pipeline_europa.py >> data/pipeline_log.txt 2>&1
```

### PyCryptodome para PDFs cifrados
`pip install pycryptodome`

## Taxonomía

- 79 códigos de suceso, 53 códigos de causa (Anexo III RD 929/2020)

## Pitfalls del Visor

### window.DATOS HARDCODEADO SOBREESCRIBE datos.js
El `index.html` tiene un bloque `window.DATOS = [...]` inline que se ejecuta DESPUÉS de `<script src="datos.js">`, sobreescribiendo los datos reales. **Siempre verificar** que no hay redefinición de `window.DATOS` en el HTML:
```bash
grep -n 'window.DATOS' visor/index.html  # Debe aparecer solo en el fallback: if (!window.DATOS)
```

### Coordenadas placeholder (48.0, 10.0)
El pipeline de extracción LLM no extrae lat/lon de los PDFs. Las coordenadas se generan por separado:
1. Mapeo directo `{(pais, provincia): (lat, lon)}` para provincias conocidas
2. Geocodificación Nominatim para las demás (1.1s delay entre peticiones)
3. Fallback al centro del país con jitter determinista (hash del ID)

### La columna `provincia` puede estar corrupta
El LLM a veces pone fragmentos del resumen del PDF en `provincia` en vez del nombre real. Verificar:
```bash
python3 -c "
import json
data = json.loads(open('visor/datos.js').read().replace('window.DATOS = ','').rstrip(';'))
bad = [d for d in data if len(d.get('provincia','')) > 30 or ' ' in d.get('provincia','')[:5]]
print(f'Provincias corruptas: {len(bad)}')
"
```

## Cron

- `eravisor-pipeline-europa` — Cada 10 min (batch)
- `ERAVisor — Indexar, descargar y extraer` — Dominical 04:00 UTC (full)
