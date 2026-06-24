---
name: dashboard-estructurado-mapa
version: "1.0.0"
description: "Patrón para construir dashboards interactivos de datos estructurados con mapa Leaflet — pipeline PDF→YAML+MD→dashboard estático"
tags: [dashboard, leaflet, mapa, pdf, datos-estructurados, github-pages, static]
---

# Dashboard Estructurado con Mapa Interactivo

## Resumen

Patrón completo para construir dashboards interactivos a partir de documentos PDFs con datos geoespaciales. Pipeline: PDF → markitdown → YAML+MD → dashboard estático → GitHub Pages.

## Cuándo usar

- Informes oficiales con ubicación geográfica (accidentes, incidentes, eventos)
- Colecciones de documentos con datos estructurables (informes, actas, memorias)
- Necesidad de visualización temporal + geográfica de eventos históricos
- Cuando los datos están en PDFs y se quiere hacerlos navegables e interactivos

## Pipeline completo

### Paso 1: Scraping de PDFs

```bash
# Descargar PDFs con curl (browser tools bloquean con 403)
curl -s -L -o pdf.pdf \
  'https://ejemplo.com/documento.pdf' \
  -H 'User-Agent: Mozilla/5.0 (compatible; DataBot/1.0)'
```

**Pitfall:** Las webs gubernamentales (transportes.gob.es, etc.) bloquean browser tools. Usar siempre `curl` con User-Agent.

### Paso 2: Extracción de texto

```bash
/opt/hermes/.venv/bin/markitdown archivo.pdf > texto.txt
```

**Pitfall:** PDFs grandes (>4MB) pueden tardar 30s+. No usar timeout < 30s.

### Paso 3: Parseo y estructuración

El script de parseo debe:

1. **Extraer ID único** del PDF — patrón `IF-XX-YYYY` o `IF XX/YYYY`. NO usar solo el año.
2. **Extraer campo `coordenadas`** del frontmatter YAML (formato `[lat, lng]`) — NO buscar `lat` y `lng` por separado en bloques distintos.
3. **Geocodificar con Nominatim** — siempre con URL encoding (`urllib.parse.quote`).
4. **Guardar en `informes/{año}/{id}.md`** — nunca sobrescribir.

**Regex para ID:**
```python
# Patrón principal: IF-XX-YYYY o IF XX/YYYY
id_match = re.search(r'IF[-/](\d+)[-/](\d{4})', text)
if not id_match:
    id_match = re.search(r'IF\s+(\d+)\s*/\s*(\d{4})', text)
```

**Regex para coordenadas del frontmatter:**
```python
# Leer coordenadas del bloque ubicacion (formato [lat, lng])
ubicacion_match = re.search(r'^ubicacion:\s*\n((?:\s+.+\n)*)', fm, re.MULTILINE)
coords_match = re.search(r'\s+coordenadas:\s*\[([^\]]+)\]', ubicacion_match.group(1))
parts = [p.strip() for p in coords_match.group(1).split(',')]
lat = float(parts[0])
lng = float(parts[1])
```

### Paso 4: Construir índice JSON

Generar `data/reports.json` con estructura:
```json
{
  "version": "1.0",
  "stats": { "total": N, "con_coords": M, ... },
  "reports": [
    {
      "id": "IF-41-2025",
      "año": 2025,
      "estacion": "Cortes de Navarra",
      "provincia": "Navarra",
      "lat": 41.9153579,
      "lng": -1.4208711,
      "gravedad": "menor",
      "victimas": 0,
      "horas_interrupcion": 1499,
      "tags": ["señal", "comunicación"]
    }
  ]
}
```

### Paso 5: Dashboard estático

**Estructura de archivos:**
```
dashboard/
├── index.html      ← HTML principal con CSS inline
├── js/app.js       ← Lógica con datos incrustados
└── data/reports.json ← (opcional, si se sirve correctamente)
```

**Pitfall crítico — GitHub Pages no sirve `.json`:**
- GitHub Pages devuelve 404 para archivos `.json`
- **Solución:** Incrustar los datos directamente en `app.js` como variable `const REPORTS_DATA = [...]`
- O usar `raw.githubusercontent.com` para servir JSON

**CSS:** Usar CSS inline en `<style>` del HTML para evitar dependencias externas.

### Paso 6: Deploy en GitHub Pages

```bash
# Configurar GitHub Pages
curl -X POST -H 'Authorization: token TOKEN' \
  -H 'Accept: application/vnd.github+json' \
  'https://api.github.com/repos/USER/REPO/pages' \
  -d '{"source": {"branch": "main", "path": "/"}}'

# URL resultante: https://USER.github.io/REPO/
```

## Estructura del repo

```
proyecto/
├── informes/           # Informes procesados YAML+MD
│   └── {año}/IF-{num}-{año}.md
├── pdfs/              # PDFs originales
├── database/          # Catálogos auxiliares
├── scripts/           # Scripts de procesamiento
│   ├── download.sh
│   └── parse.py
├── index.html         # Dashboard (raíz para GitHub Pages)
├── js/app.js          # Lógica con datos incrustados
└── data/              # Datos estructurados
```

## Pitfalls comunes

1. **IDs duplicados:** El parser sobrescribe informes si el ID no es único. Verificar antes de escribir.
2. **Coordenadas en bloque equivocado:** `ubicacion.coordenadas` es un array `[lat, lng]`, NO `geolocalizacion.lat` separado.
3. **Nominatim sin URL encoding:** Caracteres especiales (á, é, ñ) dan curl error 3.
4. **GitHub Pages 404 en .json:** Incrustar datos en JS, no hacer fetch.
5. **markitdown timeout:** PDFs grandes >4MB tardan 30s+. Timeout mínimo 30s.
6. **Browser tools bloqueadas:** Webs gubernamentales devuelven 403. Usar curl siempre.

## Alternativas de hosting

- **GitHub Pages:** Gratis, pero no sirve `.json`
- **NAN.builders:** Sirve cualquier archivo, pero requiere deploy manual
- **Netlify/Vercel:** Gratis, sirven JSON correctamente
- **Servidor propio:** Con `python3 -m http.server` o nginx

## Extensión con IA

Una vez los datos están estructurados:
- **Análisis temporal:** Gráficos Chart.js de eventos por año/tipo
- **Predicción de riesgos:** Clasificación de gravedad con ML
- **Generación de informes:** LLM que use datos estructurados para redactar nuevos informes
- **Mapa de calor:** Densidad de eventos por región

## Archivos de referencia

- `references/regex-extraccion.md` — Regex probadas para extraer ID, coordenadas, estación, PK, expediente de documentos oficiales
- `scripts/geo-fix.py` — Script para geocodificar estaciones con Nominatim (batch, all, single modes)