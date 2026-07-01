# CIAF Data — Pipeline completo de ingesta y visualización

## Resumen

Pipeline completo para convertir PDFs de informes oficiales (CIAF) en datos estructurados con georreferenciación máxima y dashboard interactivo.

## Estructura del repositorio

```
ciaf-data/
├── informes/           # Informes en YAML+Markdown
│   └── {año}/IF-{num}-{año}.md
├── pdfs/              # PDFs originales descargados
│   └── {año}/
├── schema/            # Esquemas de normalización YAML
├── database/          # Catálogos auxiliares
│   ├── trenes.json    # 19 tipos de trenes
│   └── entidades.json # 13 entidades ferroviarias
├── scripts/           # Scripts de procesamiento
│   ├── download-pdfs.sh
│   └── parse-reports.py
├── dashboard/         # Dashboard web interactivo
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
└── docs/
    └── SCHEMA.md
```

## Pipeline de ingesta

```
PDF → markitdown (texto) → regex (extraer estacion, provincia, PK) → Nominatim (geocodificar) → OpenRailwayMap API (datos línea) → YAML+MD → commit
```

### Paso 1: Descargar PDFs

```bash
bash scripts/download-pdfs.sh
```

Usa curl con User-Agent. URLs patrón:
```
https://www.transportes.gob.es/recursos_mfom/paginabasica/recursos/{filename}.pdf
```

### Paso 2: Parsear con Nominatim

```bash
python3 scripts/parse-reports.py <ruta_pdf> [año]
python3 scripts/parse-reports.py --all  # procesa todos
```

El script:
1. Extrae texto con `markitdown`
2. Busca estación con regex
3. Geocodifica con Nominatim (OSM)
4. Extrae PK, líneas, operadores
5. Genera archivo `.md` con frontmatter YAML

### Paso 3: Dashboard

Abrir `dashboard/index.html` en navegador. Incluye:
- Mapa Leaflet + OpenRailwayMap tiles
- Filtros por año, tipo, categoría
- Panel de detalles con toda la info

## OpenRailwayMap — Capas de tiles

| Capa | URL | Uso |
|------|-----|-----|
| standard | `https://tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png` | Vías con colores por electrificación |
| fast | `https://tiles.openrailwaymap.org/fast/{z}/{x}/{y}.png` | Versión simplificada, más rápida |

**Opacidad recomendada:** 0.4-0.6 sobre mapa base CARTO Light para buen contraste.

**API GeoJSON:**
```
GET https://api.openrailwaymap.org/lines?format=geojson&protected=1
```
→ Devuelve electrificación, ancho de vía, velocidad máxima.

## Nominatim — Geocodificación

```bash
curl -s 'https://nominatim.openstreetmap.org/search?format=json&q={query}&limit=1&addressdetails=1' \
  -H 'User-Agent: CIAF-Data-Parser/1.0'
```

**Pitfalls:**
- User-Agent obligatorio (bloquea sin él)
- Rate limit: 1 req/seg
- Para batch: usar delays de 1.1s entre requests

## Regex útiles para extracción

| Dato | Regex | Ejemplo |
|------|-------|---------|
| PK | `PK\s+([\d,]+\+[\d,]+)` | `PK 90+594` |
| Estación | `estación\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,]+?)` | `Cortes de Navarra` |
| Línea | `(?:línea\s+|L\/)(\d+)` | `084` |
| Comunidad | `(?:comunidad|Comunidad)\s+(?:de\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+?)` | `Navarra` |
| Tipo tren | `(?:tren|Tren)\s+(?:de\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+?)` | `Media Distancia` |
