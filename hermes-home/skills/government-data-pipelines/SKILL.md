---
name: government-data-pipelines
version: "1.1.0"
description: "Patrones para ingerir, estructurar y visualizar datos de fuentes gubernamentales — scraping de webs institucionales, parsers de PDFs con estructura fija, normalización a base de datos, dashboards interactivos. Incluye casos CIAF (ferroviario), CIAIAC (aviación), CIAIM (marítimo)."
tags: [government, scraping, pdf-parsing, data-ingestion, dashboard, geolocation]
---

# Government Data Pipelines — Patrones de ingestión de datos gubernamentales

## Resumen

Procedimiento sistémico para convertir documentos públicos gubernamentales (informes, estadísticas, registros) en bases de datos estructuradas + visualizaciones interactivas. Los documentos oficiales españoles suelen tener estructura fija y URLs predecibles.

## Casos de uso

### 1. Informes de la CIAF (ferroviario)
- **Fuente:** https://www.transportes.gob.es/organos-colegiados/ciaf
- **URLs PDF:** Varios patrones (ver `references/ciaf-scraping.md` — 4 patrones según año)
- **Estructura fija:** Resumen → Descripción → Análisis → Conclusiones → Recomendaciones
- **Schema:** Ver `templates/ciaf-report-schema.json` en skill `liteparse-document-ai-parsing`
- **Scraping:** Ver `references/ciaf-scraping.md` (dentro de este skill)
- **⚠️ Disponibilidad:** 2007-2025 están publicados. **277 informes** (ya descargados en `/root/workspace/CIAF/`) + 17 memorias + 7 normativas = 301 PDFs total.

**⚠️ PATRÓN DE URL POR AÑOS (CRÍTICO — verificado 2026-06-26):**
- **2007-2016:** `/MFOM/LANG_CASTELLANO/ORGANOS_COLEGIADOS/CIAF/INFORMES/YYYY/`
  - Ej: `/MFOM/LANG_CASTELLANO/ORGANOS_COLEGIADOS/CIAF/INFORMES/2009/`
  - Los PDFs están en el HTML estático (no AJAX)
  - Patrón de PDF: `href="(/recursos_mfom/pdf/UUID/ID/FILENAME.pdf)"` (comillas dobles)
  - Total: ~181 PDFs (2009-2016; 2007-2008 vacíos)
- **2017-2025:** `/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados/infofin-YYYY`
  - Ej: `/infofin-2025`
  - PDFs en `/recursos_mfom/paginabasica/recursos/XXXX-YY-ZZZZ-if-*.pdf`
  - Total: ~38 PDFs (ya descargados)
- **NO usar filtros GET** (`?field_ciaf_anyo_value=2015`) — no funcionan, solo devuelven menú.
- **TOTAL REAL: 277 informes** (ya descargados en `/root/workspace/CIAF/YYYY/` desde 2007 hasta 2025). Distribución: 2007:4, 2008:53, 2009:43, 2010:28, 2011:24, 2012:22, 2013:23, 2014:14, 2015:10, 2016:11, 2017:12, 2018:2, 2019:3, 2020:3, 2021:6, 2022:5, 2023:3, 2024:3, 2025:1.

**⚠️ TRES ERAS DE FORMATO (CRÍTICO para el parser):**
Los informes tienen 3 formatos distintos según la normativa vigente:
1. **Pre-RD 810/2007 (2007-2008):** Formato libre, secciones variables (Antecedentes/Hechos/Análisis)
2. **RD 810/2007 (2009-2013):** Secciones 1-5 (Resumen, Descripción, Análisis, Conclusiones, Recomendaciones)
3. **RD 623/2014 (2014-2025):** Secciones 0-6 (Abreviaturas, Resumen, Descripción, Análisis, Conclusiones, Recomendaciones, Anexos)
- **Normativa de referencia:** `/root/workspace/CIAF/normativa/04-RD_623_2014_ciaf.pdf` — Art. 15 define la estructura obligatoria del informe
- **Detectar era por año** antes de parsear. Los 2007-2008 son los más irregulares.

**📊 Memorias anuales:**
- URL: `/organos-colegiados/ciaf/memorias-anuales/memoriasanuales`
- 17 memorias (2008-2024), guardadas en `/root/workspace/CIAF/memorias/`
- PDFs en el HTML directamente (no AJAX) — buscar `href='(/recursos_mfom/[^']+\\.pdf)'`
- Pattern de PDFs: múltiples rutas (`/recursos_mfom/`, `/recursos_mfom/pdf/UUID/`, `/recursos_mfom/listado/recursos/`)
- **NO hay memoria de 2011** — sí existe, pero se saltó en script anterior. Verificar siempre.
- **📄 Normativa:** 7 PDFs en `/root/workspace/CIAF/normativa/` — incluye RD 623/2014 que define estructura de informes

**📐 Preferencia de arquitectura (verificado):**
- **JSON como fuente de verdad** (no MD, no SQLite): GitHub Pages sirve JSON estático
- **JSON particionado por año**: `data/reports/YYYY.json` + `data/index.json` ligero (~50KB para 500 registros)
- **relations.json** para cruzar entidades × informes × recomendaciones
- **Imágenes extraídas** de PDFs con `pdfimages` (poppler) + `pdftoppm` como fallback
- **Coherencia** entre memorias anuales e informes individuales — verificar que los datos coinciden
- **Auto-import**: pipeline `sync.py` que detecta nuevos PDFs en la web y los procesa automáticamente

### 2. Informes de la CIAIAC (aviación)
- **Fuente:** https://www.transportes.gob.es/organos-colegiados/ciaiac
- **Mismo patrón** que CIAF pero para accidentes aéreos

### 3. Informes de la CIAIM (marítimo)
- **Fuente:** https://www.transportes.gob.es/organos-colegiados/ciaim
- **Investigaciones organizadas por año:** `/organos-colegiados/ciaim/investigaciones/2024`

### Arquitectura para datasets grandes (>100 registros, GitHub Pages)

Cuando hay 200+ registros, NO usar un solo JSON gigante. Usar **JSON particionado por año**:

```
data/
├── index.json              ← Índice ligero (todos los IDs, metadatos mínimos, ~50KB)
├── reports/
│   ├── 2009.json           ← Registros del 2009
│   ├── 2010.json           ← Registros del 2010
│   └── ...
├── relations.json          ← Entidades × registros × relaciones
└── images/
    ├── 2009/
    │   └── IF-001-2009-fig01.png
    └── ...
```

**Por qué funciona:**
- `index.json` se carga una vez para mapa + filtros (50KB para 500 registros)
- `reports/YYYY.json` se carga solo al hacer clic en un registro de ese año
- GitHub Pages sirve JSON estático sin backend
- Escalable a 500+ registros sin problemas de rendimiento

**Por qué NO SQLite en navegador:**
- GitHub Pages no sirve SQLite — necesitarías sql.js (500KB) + WebAssembly
- Para <1000 registros, JSON con fetch es suficiente
- JSON es más fácil de mantener y versionar con git

### Pipeline genérico (paso a paso)

### Paso 1: Descubrimiento de fuentes
```bash
# Acceder a la web con curl (NO browser tool — 403 en transportes.gob.es)
curl -sL 'https://www.transportes.gob.es/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'

# Extraer enlaces a PDFs
curl ... | grep -oP 'href="[^"]*\.pdf"' | sort -u
```

**⚠️ 4 patrones de URL para PDFs en transportes.gob.es:**
1. `recursos_mfom/paginabasica/recursos/XXXX-YY-ZZZZ-if-*.pdf` (2017-2025)
2. `recursos_mfom/pdf/UUID-UUID/UUID/FILENAME.pdf` (2015-2016)
3. `recursos_mfom/YYMMDD-YYMMYY-if-*.pdf` (2015-2016)
4. `recursos_mfom/comodin/recursos/YYMMDDYYMMYYif*.pdf` (2016)

**⚠️ 2 patrones de URL por año:**
- 2015-2016: `/informes-finales-de-sucesos-investigados/AÑO`
- 2017-2025: `/informes-finales-de-sucesos-investigados/infofin-AÑO`
- **NO usar filtros GET** (`?field_ciaf_anyo_value=2015`) — no funcionan.

### Paso 2: Scraping masivo
- **Frecuencia:** Cron semanal (domingo 06:00 UTC)
- **Detección de nuevos:** Comparar hashes de URLs con base de datos local
- **Velocidad:** 1 PDF/sec es suficiente para cientos de informes

### Paso 3: Extracción de texto
- **Herramienta principal:** `PyMuPDF` (`fitz`) — más fiable que poppler/markitdown, puro Python, sin dependencias del sistema
  ```python
  import fitz
  doc = fitz.open(str(pdf_path))
  text = "\n".join(page.get_text() for page in doc)
  doc.close()
  ```
- **Fallback:** `markitdown` con extras: `pip install "markitdown[pdf]"` (requiere `pymupdf` como backend de PDF)
- **⚠️ `pdftotext` (poppler) frágil en entornos containerizados:** puede fallar por `libpoppler.so.XXX` faltante. Si aparece `No such file or directory: 'pdftotext'`, instalar `libpoppler-dev` O cambiar a PyMuPDF.
- **Extracción de imágenes:** `PyMuPDF` también extrae imágenes incrustadas (`page.get_images()` + `doc.extract_image(xref)`). Si no hay imágenes incrustadas, renderizar páginas como PNG con `page.get_pixmap(dpi=150)`.
- **OCR:** Si el PDF es imagen (no texto), usar `ocrmypdf`

### Paso 3b: Extracción semántica de campos (CRÍTICO)
El mayor reto NO es extraer texto del PDF (PyMuPDF lo hace bien), sino **estructurar el texto libre en campos JSON**. Patrones verificados con CIAF:

**Expediente/informe:**
```python
patterns = [
    r'IF\s+(\d+/\d{4})',              # RD 623: "IF 64/2024"
    r'n[º°]\s*(\d+/\d{4})',           # RD 810: "nº 065/2007"
    r'N[º°]\s*(\d+/\d{4})',           # Mayúsculas
    r'investigación\s+.*?n[º°]\s*(\d+/\d{4})',  # Contexto
]
```

**Estación/ubicación — múltiples patrones por era:**
```python
patterns = [
    r'estación\s+de\s+([A-ZÁÉÍÓÚÑ][^\.]+?)(?:\s*[,\.]|\s+el\s)',  # "estación de Madrid Chamartín"
    r'EN\s+LA\s+ESTACI[ÓO]N\s+DE\s+([A-ZÁÉÍÓÚÑ\s]+)',           # Mayúsculas
    r'en\s+el\s+apeadero\s+de\s+([A-ZÁÉÍÓÚÑ][^\.]+?)(?:\s*,)',   # "apeadero de X"
    r'(?:Lugar|Ubicación)[:\s]+([^\n]+)',                           # Campo directo
]
```

**Provincia — extraer del cuerpo, NO del encabezado:**
```python
# 1. Buscar "Provincia: X" en contexto del accidente
# 2. Inferir del nombre de estación ("Cuenca-Fernando" → Cuenca)
# 3. Buscar primera mención de provincia DESPUÉS del encabezado (>posición 1000)
# ⚠️ NO confundir "Madrid" en dirección de sede CIAF con provincia del accidente
```

**Entidades — normalizar variants:**
```python
ENTITY_MAP = {
    'renfe operaciones': 'Renfe',
    'renfe viajeros': 'Renfe',
    'adif': 'ADIF',
    'continental rail': 'Continental Rail',
    'acciona rail': 'Acciona Rail',
}
# Buscar: "empresa ferroviaria X", "operador X", "gestor de infraestructura X"
```

**Recomendaciones — patrón tabular:**
```python
# RD 623/2014: tabla con columnas "Destinatario | Nº | Recomendación"
# RD 810/2007: lista numerada "1. Se recomienda a..."
# Pre-RD: texto narrativo, harder to extract
rec_pattern = r'(?:destinatario|remitente)[:\s]*([^\n]+).*?(?:recomendaci[oó]n)[:\s]*([^\n]+)'
```

**Víctimas — verificar negación primero:**
```python
# "sin víctimas mortales" → 0
# "no se produjeron víctimas" → 0
# "una persona fallecida" → 1
# "N fallecidos" → N
if re.search(r'sin\s+v[íi]ctimas|no\s+se\s+produjeron', text_lower):
    return 0
```

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
- **Vías de tren (si ferroviario):** Descargar de OpenStreetMap vía Overpass API → GeoJSON local. **No** llamar Overpass en tiempo real desde el frontend (lento, rate-limited).

#### Simplificación de GeoJSON grande (PATRÓN VERIFICADO)
Cuando el GeoJSON de referencia (vías de tren, carreteras, etc.) supera 10MB:
1. Reducir precisión de coordenadas a 4 decimales (~11m) — suficiente para visualización
2. Eliminar features con <3 coordenadas (tramos irrelevantes)
3. Para features largas (>10 coords), keep every 3rd coordinate
4. Eliminar propiedades innecesarias (mantener solo: color, weight, name, usage)
5. Usar `json.dump(data, f, separators=(',', ':'))` para JSON compacto
- Resultado típico: 24MB → 7MB (70% reducción)
- **NO servir GeoJSON >10MB en frontend** — causa lag en móviles y cargas lentas

#### Mapeo de campos parser → frontend
El parser genera campos en español (`tipo`, `fecha_suceso`, `ubicacion.estacion`), pero el frontend puede usar campos en inglés (`type`, `date`, `city`). **Patrón:** añadir capa de mapeo en `loadData()`:
```javascript
const mapped = yearData.map(r => ({
    id: r.id,
    year: r.year,
    type: r.tipo || 'desconocido',
    severity: r.gravedad || 'leve',
    date: r.fecha_suceso || '',
    city: r.ubicacion?.estacion || r.ubicacion?.provincia || '',
    entity: (r.entidades && r.entidades[0]) || '',
    lat: r.ubicacion?.lat,
    lng: r.ubicacion?.lng,
    // ... resto de campos
}));
```
Esto desacopla el parser del frontend — cada uno puede evolucionar independientemente.

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

### ⚠️ Geocodificación de estaciones de tren con Nominatim (PATRÓN VERIFICADO)
Nominatim NO encuentra estaciones de tren con queries simples. Patrón que funciona:

```python
import urllib.request, urllib.parse, json, re, time

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "CIAF-Visor/1.0 (email@domain.com)"  # Requerido por ToS

def geocode_station(station_name: str, province: str = "") -> tuple[float|None, float|None]:
    """Patrón verificado: limit=5 + filtro por tipo railway/train_station."""
    clean_name = re.sub(r'\s+', ' ', station_name.strip())
    
    # Estrategia 1: "Estación Nombre España"
    queries = [f'{clean_name} España']
    
    # Estrategia 2: Sin calificadores ("Clasificación", "Terminal", etc.)
    simplified = re.sub(r'\b(Clasificación|Clasificacion|Terminal|Central|Norte|Sur)\b', '', clean_name).strip()
    if simplified and simplified != clean_name:
        queries.append(f'{simplified} España')
    
    # Estrategia 3: Solo nombre + provincia
    if province:
        queries.append(f'{clean_name} {province} España')
    
    for query in queries:
        try:
            params = urllib.parse.urlencode({
                'q': query, 'format': 'json',
                'limit': 5,  # ⚠️ NO limit=1 — el primer resultado suele ser el barrio/distrito
                'countrycodes': 'es',
            })
            url = f"{NOMINATIM_URL}?{params}"
            req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            
            if data:
                # ⚠️ FILTRO CLAVE: priorizar railway/station, NO el primer resultado
                best = None
                for d in data:
                    t = d.get('type', '')
                    c = d.get('class', '')
                    if t in ('station', 'train_station') and c in ('railway', 'building'):
                        best = d; break
                    if c == 'railway':
                        best = d; break
                    if 'train' in t.lower() or 'rail' in c.lower():
                        best = d; break
                if not best:
                    best = data[0]  # Fallback al primero
                
                lat = float(best['lat'])
                lng = float(best['lon'])
                return lat, lng
        except Exception:
            time.sleep(0.5)
    
    return None, None
```

**Pitfalls Nominatim verificados:**
- `limit=1` devuelve el barrio/administración, NO la estación → usar `limit=5` y filtrar
- `featurecodes` parameter NO funciona como se espera → ignorar
- Queries complejas ("estacion de tren Madrid Chamartin Madrid") devuelven 0 resultados → queries simples mejor
- "Madrid-Chamartín-Clara Campoamor" tiene `class=building, type=train_station` → buscar ambos
- **Rate limiting:** Nominatim ToS requiere 1 req/seg. Usar `time.sleep(1.1)` entre requests
- **In-memory cache:** Usar dict en memoria para no repetir queries. ⚠️ NO cachear None values entre runs del parser — limpiar cache al re-ejecutar

### Almacenamiento geográfico
- **SQLite:** `spatialite` extension para consultas geográficas
- **PostgreSQL:** PostGIS para consultas avanzadas (radio, distancia, buffers)

## Pitfalls

- **🔴 La extracción semántica es lo difícil, no la de texto:** PyMuPDF/markitdown extraen texto limpio de PDFs, pero convertir texto libre a campos estructurados (fechas, estaciones, entidades, recomendaciones) requiere regex robustos o LLM. Los campos `fecha_suceso`, `ubicacion.estacion`, `entidades` y `recomendaciones` suelen venir vacíos si el parser solo hace split por secciones. **Solución:** validar que cada informe tenga ≥3 campos no vacíos; si no, usar LLM para extracción asistida.
- **🔴 SIEMPRE verificar el alcance real antes de proponer arquitectura:** No asumir el número de registros basándose solo en lo que hay descargado localmente. Contar los PDFs/disponibles en la web ANTES de diseñar la arquitectura. Ejemplo: asumir 38 PDFs cuando hay 219 en la web → arquitectura equivocada.
- **🔴 Browser tools en webs gubernamentales:** La mayoría bloquean browser tools (403). Siempre usar curl con User-Agent: `"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"`
- **🔴 PDFs que no son texto, son imágenes:** Si markitdown devuelve texto vacío, el PDF es una escaneada. Usar `ocrmypdf input.pdf output.pdf` antes de procesar.
- **🔴 Nombres de lugares ambiguos:** "Cortes" puede ser de Navarra, de La Muela, etc. Usar contexto del PDF (provincia, región) para desambiguar.
- **🔴 Cache de geocoding persiste None values:** Si el parser cachea resultados de Nominatim en memoria y se ejecuta sin limpiar el cache, los None values de la sesión anterior persisten. **Siempre limpiar `__pycache__` y el dict de cache al re-ejecutar el parser.**
- **🔴 Servidor HTTP y rutas relativas:** Si el frontend usa `fetch('../data/index.json')`, el servidor HTTP DEBE arrancar desde la raíz del proyecto (no desde `frontend/`). Si arranca desde `frontend/`, `../data/` queda fuera del root y devuelve 404/HTML.
- **🔴 GeoJSON de Overpass API muy grande:** 50K features de vías de tren = 24MB raw. Siempre simplificar antes de servir al frontend (reducir coords, eliminar features cortas). Técnica: precision 4 decimales (~11m), eliminar features <3 coords, subsamplear features >10 coords.
- **⚠️ Mapeo de campos parser → frontend:** El parser genera campos en español (`tipo`, `fecha_suceso`, `ubicacion.estacion`), pero el frontend puede usar campos en inglés (`type`, `date`, `city`). Añadir capa de mapeo en `loadData()` para desacoplar parser de frontend.
- **⚠️ LLM que inventa datos:** El prompt DEBE incluir: "NO inventes datos. Si un campo no existe en el PDF, pon null."
- **⚠️ Estructura variable:** Algunos PDFs pueden tener secciones ligeramente diferentes. Tener un fallback que procese sin schema estricto.
- **⚠️ Paginación en webs gubernamentales:** Los listados de documentos suelen tener paginación. Recorrer todas las páginas antes de descargar PDFs.
- **⚠️ Encoding en PDFs antiguos:** PDFs antes de 2015 pueden tener caracteres especiales mal codificados. Usar `chardet` o forzar UTF-8.
- **⚠️ PATRÓN URL POR AÑOS:** Las webs gubernamentales cambian su estructura de URL entre años. Para CIAF: 2015-2016 usan `/AÑO`, 2017-2025 usan `/infofin-AÑO`. **Siempre probar ambas variantes antes de descartar años.**
- **⚠️ 4 PATRONES DE PDF DIFERENTES:** Los PDFs del mismo repositorio pueden usar rutas distintas según el año de publicación (paginabasica/recursos/, pdf/UUID/, recursos_mfom/, comodin/recursos/). Usar múltiples patrones regex simultáneamente.
- **⚠️ Servidor HTTP y rutas relativas:** Si el frontend usa `fetch('../data/index.json')`, el servidor HTTP DEBE arrancar desde la raíz del proyecto (no desde `frontend/`). Si arranca desde `frontend/`, `../data/` queda fuera del root y devuelve 404/HTML.
- **⚠️ GeoJSON de Overpass API muy grande:** 50K features de vías de tren = 24MB raw. Siempre simplificar antes de servir al frontend (reducir coords, eliminar features cortas).

## Herramientas recomendadas

| Herramienta | Uso | Alternativa |
|------------|-----|-------------|
| `PyMuPDF` (fitz) | Extracción texto + imágenes de PDFs | markitdown, pdfplumber |
| `markitdown` | Conversión PDF/DOCX → Markdown para LLM | PyMuPDF |
| `pydantic` | Validación schema JSON | jsonschema |
| `sqlite3` + spatialite | Base de datos local | PostgreSQL + PostGIS |
| `Leaflet.js` | Mapas interactivos | Mapbox GL |
| `Chart.js` | Gráficos estadísticos | D3.js, Plotly |
| `Nominatim` | Geocodificación | Google Maps API, OpenRouteService |
| `Overpass API` | Datos geoespaciales OSM (vías, edificios) | Descarga directa .osm |

## Extensión multi-modal

Este patrón funciona para cualquier tipo de transporte:
- **CIAF** (ferroviario) → ya definido
- **CIAIAC** (aviación) → misma estructura, schema adaptado
- **CIAIM** (marítimo) → misma estructura, schema adaptado
- **DGT** (tráfico) → informes de accidentes viales, diferentes estructura

## Templates disponibles
- `templates/ciaf-report-schema.json` → Schema para informes CIAF

## Referencias
- `references/ciaf-scraping.md` → Procedimiento completo de scraping: URLs, curl/Python, estructura nombres PDF, pitfalls
- `references/ciaf-data-architecture-2026.md` → Arquitectura completa CIAF: inventario 277 informes, 3 eras de formato, JSON particionado, relaciones entidades, diseño del visor
