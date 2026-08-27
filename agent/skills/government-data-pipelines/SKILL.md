---
name: government-data-pipelines
version: "1.0.0"
description: "Patrones para ingerir, estructurar y visualizar datos de fuentes gubernamentales — scraping de webs institucionales, parsers de PDFs con estructura fija, normalización a base de datos, dashboards interactivos. Incluye casos CIAF (ferroviario), CIAIAC (aviación), CIAIM (marítimo)."
tags: [government, scraping, pdf-parsing, data-ingestion, dashboard, geolocation]
---

# Government Data Pipelines — Patrones de ingestión de datos gubernamentales

## Resumen

Procedimiento sistémico para convertir documentos públicos gubernamentales (informes, estadísticas, registros) en bases de datos estructuradas + visualizaciones interactivas. Los documentos oficiales españoles suelen tener estructura fija y URLs predecibles.

## Casos de uso

### 1. Informes de la CIAF (ferroviario)
- **Fuente:** https://www.transportes.gob.es/organos-colegiados/ciaf
- **URLs PDF:** `recursos_mfom/paginabasica/recursos/XXXX-YY-ZZZZ-if-*.pdf`
- **Estructura fija:** Resumen → Descripción → Análisis → Conclusiones → Recomendaciones
- **Schema:** Ver `templates/ciaf-report-schema.json` en skill `liteparse-document-ai-parsing`
- **Scraping:** Ver `references/ciaf-scraping.md` en skill `liteparse-document-ai-parsing`

### 2. Informes de la CIAIAC (aviación)
- **Fuente:** https://www.transportes.gob.es/organos-colegiados/ciaiac
- **Mismo patrón** que CIAF pero para accidentes aéreos

### 3. Informes de la CIAIM (marítimo)
- **Fuente:** https://www.transportes.gob.es/organos-colegiados/ciaim
- **Investigaciones organizadas por año:** `/organos-colegiados/ciaim/investigaciones/2024`

## Pipeline genérico (paso a paso)

### Paso 1: Descubrimiento de fuentes
```bash
# Acceder a la web con curl (NO browser tool — 403 en transportes.gob.es)
curl -sL 'https://www.transportes.gob.es/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'

# Extraer enlaces a PDFs
curl ... | grep -oP 'href="[^"]*\.pdf"' | sort -u
```

### Paso 2: Scraping masivo
- **Frecuencia:** Cron semanal (domingo 06:00 UTC)
- **Detección de nuevos:** Comparar hashes de URLs con base de datos local
- **Velocidad:** 1 PDF/sec es suficiente para cientos de informes

### Paso 3: Extracción de texto
- **Herramienta:** `markitdown` (mejor que pdftotext para PDFs complejos)
- **Fallback:** `pdftotext` si markitdown no está disponible
- **OCR:** Si el PDF es imagen (no texto), usar `ocrmypdf`

### Paso 4: Estructuración con LLM
- **Schema fijo:** Definir antes de procesar. Cada sección del PDF mapea a un campo JSON.
- **Prompt:** "Estructura el siguiente informe en este schema JSON. No inventes datos."
- **Modelo:** qwen3.6 vía NaN API (barato y bueno con estructura)
- **Validación:** JSON schema validation en Python (pydantic)

### Paso 5: Almacenamiento
- **Opción rápida:** SQLite (un archivo, fácil de backup)
- **Opción producción:** PostgreSQL + PostGIS (geolocalización)
- **Tablas mínimas:**
  - `informes` (id, fecha, tipo, resumo, url_pdf)
  - `eventos` (informe_id, tipo, descripción, consecuencias)
  - `causas` (informe_id, tipo, texto)
  - `recomendaciones` (informe_id, destinatario, contenido, estado)

### Paso 6: Visualización
- **Mapa:** Leaflet.js + puntos geolocalizados
- **Gráficos:** Chart.js para tendencias temporales
- **Filtros:** Año, tipo, ubicación, causa, operador
- **Drill-down:** Clic en punto → ver informe completo

## Schema design patterns

### Patrón A: Documentos con estructura fija
Cuando el PDF siempre tiene las mismas secciones (título, número, fecha, cuerpo):
```json
{
  "meta": { "id": "STRING", "fecha": "DATE", "tipo": "ENUM" },
  "contenido": { /* mapeo directo secciones → campos */ },
  "análisis": { "causas": [], "recomendaciones": [] }
}
```

### Patrón B: Documentos con estructura variable
Cuando el formato cambia ligeramente entre documentos:
```json
{
  "raw_text": "MARCADO: texto original completo",
  "extracted_fields": { "campos_confiables": [...] },
  "confidence": 0.0-1.0,
  "llm_notes": "Notas sobre ambigüedades"
}
```

### Patrón C: Documentos con tablas
Cuando el PDF contiene tablas (estadísticas, presupuestos):
- Extraer tabla con `markitdown` → `pandas`
- Validar columnas con schema
- Normalizar tipos de datos

## Geolocalización

### Extracción de coordenadas
1. **Nombre de lugar → coordenadas:** Nominatim (OpenStreetMap)
2. **Referencia directa en PDF:** regex para "lat: X.X, lon: Y.Y"
3. **Dirección postal:** Nominatim o Google Maps API

### Almacenamiento geográfico
- **SQLite:** `spatialite` extension para consultas geográficas
- **PostgreSQL:** PostGIS para consultas avanzadas (radio, distancia, buffers)

## Pitfalls

- **🔴 Browser tools en webs gubernamentales:** La mayoría bloquean browser tools (403). Siempre usar curl con User-Agent: `"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"`
- **🔴 PDFs que no son texto, son imágenes:** Si markitdown devuelve texto vacío, el PDF es una escaneada. Usar `ocrmypdf input.pdf output.pdf` antes de procesar.
- **🔴 Nombres de lugares ambiguos:** "Cortes" puede ser de Navarra, de La Muela, etc. Usar contexto del PDF (provincia, región) para desambiguar.
- **⚠️ LLM que inventa datos:** El prompt DEBE incluir: "NO inventes datos. Si un campo no existe en el PDF, pon null."
- **⚠️ Estructura variable:** Algunos PDFs pueden tener secciones ligeramente diferentes. Tener un fallback que procese sin schema estricto.
- **⚠️ Paginación en webs gubernamentales:** Los listados de documentos suelen tener paginación. Recorrer todas las páginas antes de descargar PDFs.
- **⚠️ Encoding en PDFs antiguos:** PDFs antes de 2015 pueden tener caracteres especiales mal codificados. Usar `chardet` o forzar UTF-8.

## Herramientas recomendadas

| Herramienta | Uso | Alternativa |
|------------|-----|-------------|
| `markitdown` | Extracción texto de PDFs | pdftotext, pdfplumber |
| `pydantic` | Validación schema JSON | jsonschema |
| `sqlite3` + spatialite | Base de datos local | PostgreSQL + PostGIS |
| `Leaflet.js` | Mapas interactivos | Mapbox GL |
| `Chart.js` | Gráficos estadísticos | D3.js, Plotly |
| `Nominatim` | Geocodificación | Google Maps API, OpenRouteService |

## Extensión multi-modal

Este patrón funciona para cualquier tipo de transporte:
- **CIAF** (ferroviario) → ya definido
- **CIAIAC** (aviación) → misma estructura, schema adaptado
- **CIAIM** (marítimo) → misma estructura, schema adaptado
- **DGT** (tráfico) → informes de accidentes viales, diferentes estructura

## Templates disponibles
- `templates/ciaf-report-schema.json` → Schema para informes CIAF (ver skill `liteparse-document-ai-parsing`)

## Referencias
- `references/ciaf-scraping.md` → Procedimiento de scraping de transportes.gob.es (ver skill `liteparse-document-ai-parsing`)
