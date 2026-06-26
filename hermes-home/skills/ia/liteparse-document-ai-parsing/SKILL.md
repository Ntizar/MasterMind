---
name: liteparse-document-ai-parsing
version: "1.0.0"
description: "Liteparse — parser de documentos con IA del equipo LlamaIndex (10K⭐). Extrae datos estructurados (JSON/CSV) de PDFs, HTML, markdown, imágenes usando LLMs. Rápido (Rust)."
tags: [document-parsing, llm, extraction, pdf, rust, llamaindex, ai]
---

# Liteparse — Document AI Parsing

## Resumen

Liteparse de LlamaIndex (run-llama) es un parser de documentos **rápido** (Rust) que extrae datos estructurados de documentos no estructurados usando **LLMs**. A diferencia de markitdown (conversión a markdown), liteparse extrae **esquemas específicos** (JSON/CSV con campos definidos).

## Características

- **Rápido:** Escrito en Rust → milisegundos por página
- **Estructurado:** Extrae JSON/CSV según schema que definas
- **Multi-formato:** PDF, HTML, Markdown, imágenes
- **LLM integrado:** Usa modelos locales o API (OpenAI, Claude)
- **Open-source:** Apache 2.0

## Instalación

```bash
pip install liteparse  # Python bindings
# O CLI directa
cargo install liteparse  # Rust
```

## Uso

```python
from liteparse import DocumentParser

# Definir schema de extracción
schema = {
    "company_name": "string",
    "invoice_number": "string",
    "date": "date",
    "total_amount": "number",
    "line_items": [{"description": "string", "amount": "number"}]
}

# Parsear
parser = DocumentParser(model="gpt-4o")
result = parser.parse("factura.pdf", schema=schema)
# → {"company_name": "ACME", "invoice_number": "INV-001", ...}
```

## Integración con Mastermind

- Pipeline `pdf-to-dashboard` (extraer datos de presupuestos de obra)
- Pipeline `pdf-to-landing` (estructurar contenido de PDFs)
- OCR quirúrgico (complementar `ocr-quirurgico-pdf-md`)
- Extracción de datos de facturas, contratos, informes
- **Informes oficiales (CIAF)** — ingesta masiva de informes de la CIAF: scraping web → markitdown → LLM structuring → base de datos SQLite → mapa interactivo Leaflet

## Casos de uso: informes oficiales (CIAF)

**Contexto:** La CIAF (Comisión de Investigación de Accidentes Ferroviarios) publica informes finales en PDF con estructura fija. Más de 20 años de datos en español.

**Pipeline recomendado:**
1. **Scraping:** curl con User-Agent (la web bloquea browser tools con 403). URLs siguen patrón `recursos_mfom/paginabasica/recursos/XXXX-YY-ZZZZ-if-*.pdf`
2. **Extracción texto:** `markitdown` (más flexible que pdftotext para estructuras complejas)
3. **Estructuración LLM:** Schema JSON fijo con secciones mapeadas (ver `templates/ciaf-report-schema.json`)
4. **Almacenamiento:** SQLite con tablas normalizadas (informes, eventos, causas, recomendaciones, geolocalización)
5. **Visualización:** Leaflet + map points, Chart.js + gráficos temporales, filtrado por año/tipo/ubicación

**Estructura fija de informes CIAF (mapeo al schema):**
- "1. RESUMEN" → fecha, hora, tipo, ubicación, trenes, resumen ejecutivo
- "3. DESCRIPCIÓN DEL SUCESO" → circunstancias, víctimas, material rodante, infraestructura
- "4. ANÁLISIS DEL SUCESO" → cometidos, factores humanos, mecanismos de control
- "5. CONCLUSIONES" → causas identificadas
- "6. RECOMENDACIONES FINALES" → acciones preventivas

## Comparativa

| Herramienta | Output | Velocidad | Formato target |
|------------|--------|-----------|----------------|
| **markitdown** | Markdown | Media | Conversión genérica |
| **liteparse** | JSON/CSV | Alta (Rust) | Extracción estructurada |
| **pdfplumber** | Tablas | Baja | PDF-only |
| **Unstructured** | Markdown+JSON | Media | Multi-formato |

## Referencia

- Repo: `run-llama/liteparse`
- **Template:** `templates/ciaf-report-schema.json` — Schema JSON completo para informes CIAF (estructura fija mapeada a secciones del PDF)
- **Template:** `templates/ciaf-normalized-schema.yaml` — Schema YAML+Markdown para normalización de informes CIAF (frontmatter estructurado + cuerpo editable)
- **Referencia:** `references/ciaf-scraping.md` — Procedimiento de scraping de transportes.gob.es (URLs de PDFs, patrón de URLs, pitfalls de browser tools, estructura por años)
- **Referencia:** `references/ciaf-pipeline.md` — Pipeline completo de ingesta: PDF → markitdown → Nominatim → OpenRailwayMap → YAML+MD, con regex útiles y estructura del repo
- **Referencia:** `references/ciaf-dashboard-v2.md` — Patrón de dashboard v2.0: HTML+CSS inline, JS con datos incrustados, tabs (Resumen/Conclusiones/Recomendaciones/Datos), mapa Leaflet, filtros, responsive, GitHub Pages

## Formato híbrido YAML+Markdown (v2.0 — normalización de informes)

**Problema:** Los PDFs de informes oficiales tienen estructuras variables entre años. JSON puro pierde texto libre (conclusiones, recomendaciones). Markdown puro no permite búsqueda/filtrado programático.

**Solución:** YAML frontmatter + cuerpo Markdown.

- **Frontmatter YAML** → campos estructurados para búsqueda, filtros, mapa, estadísticas
- **Cuerpo Markdown** → texto completo del informe, editable por humanos
- **Campos opcionales** → si un informe no tiene un campo (ej: coordenadas), se omite
- **Enlace al PDF** siempre presente → trazabilidad 100%
- **Un archivo por informe** → `repo/informes/{year}/{id}.md`

**Ejemplo de estructura:**
```yaml
---
id: "IF-41-2025"
tipo_informe: "incidente_operacional"
fecha_suceso: "2025-05-22T21:53:00"
ubicacion:
  estacion: "Cortes de Navarra"
  provincia: "Navarra"
  coordenadas: [41.9931, -1.8769]
tipo_suceso:
  categoria: "operacional"
  subtipo: "rebase_señal"
trenes:
  - tipo: "Media Distancia"
    numero: "18079"
    operador: "Renfe Viajeros"
---

# Informe Final IF-41/2025

## 1. Resumen
[Texto completo del resumen]

## 2. La investigación y su contexto
[Texto completo]
```

**Schema completo:** Ver `templates/ciaf-normalized-schema.yaml`

## Georreferenciación máxima — Integración con Nominatim + OpenRailwayMap

**Flujo completo de geocodificación para informes con ubicación ferroviaria:**

1. **Extraer nombre de estación** del texto del informe (regex: `estación\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,]+?)`)
2. **Geocodificar con Nominatim:**
   ```bash
   curl -s 'https://nominatim.openstreetmap.org/search?format=json&q={estación}+{provincia}+Spain&limit=1&addressdetails=1' \
     -H 'User-Agent: CIAF-Data-Parser/1.0'
   ```
   → Devuelve lat, lng, display_name, address
3. **Extraer PK (punto kilométrico)** si existe: regex `PK\s+([\d,]+\+[\d,]+)`
4. **Consulta OpenRailwayMap API** para datos de la línea:
   ```bash
   curl -s 'https://api.openrailwaymap.org/lines?format=geojson&protected=1'
   ```
   → Devuelve electrificación, ancho de vía, velocidad máxima
5. **Guardar en frontmatter:**
   ```yaml
   geolocalizacion:
     fuente_coordenadas: "nominatim"
     precision: "estacion"  # estacion | tramo | pk | aproximada
     lat: 41.9931
     lng: -1.8769
   datos_linea:
     electrificacion: "3000Vcc"
     ancho_via: "ibérico"
     velocidad_max: 250
   ```

**Pitfalls CRÍTICOS:**
- **Nominatim requiere URL encoding** (urllib.parse.quote) — caracteres á, é, ñ, ¡, ¿ dan curl error 3 si no se codifican. **SIEMPRE** usar `quote(query)` antes de construir la URL.
- Nominatim requiere User-Agent no vacío (bloquea sin él).
- Nominatim tiene rate limit: máx 1 request/segundo. Para batch, usar delays.
- **Fallback strategy en geocodificación:** 1) Nominatim con encoding, 2) Lookup en estaciones.json, 3) Nominatim sin Spain, 4) Manual fallback con coordenadas hardcoded.
- **markitdown puede tardar 30s+** en PDFs grandes (>4MB). Usar timeout 120s en subprocess.run.
- **Nombres de archivo de PDFs:** el parser sobrescribe informes si el ID se extrae mal. Verificar IDs únicos antes de escribir.
- **GitHub Pages no sirve archivos .json** vía su URL. Solución: incrustar datos inline en HTML/JS o usar raw.githubusercontent.com.
- **ID extraction bug:** La regex `IF\s*[-/]?\d+` captura el año (2025) en vez del número del informe (41). Usar `IF[-/]\d+[-/]\d{4}` o buscar patrón `IF XX/YYYY`.
- **Parser v2:** Los PDFs CIAF tienen 7 secciones numeradas (0-6) en posiciones predecibles tras markitdown. Líneas ~72, ~86, ~165, ~225, ~350, ~726, ~777. Regex: `^\d+\.\s+[A-ZÁÉÍÓÚÑ]` con len < 80.
- **Parser v2:** Extracción de conclusiones/recomendaciones con regex `^[\d]+[\.\)]\s+` o `^[a-z][\.\)]\s+`.
- **Parser v2:** Fecha con meses en español: `(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})`. Hora: `a\s+las?\s+(\d{1,2}:\d{2}(?::\d{2})?)`.
- **Parser v2:** Trenes con contexto: `(?:el\s+)?(?:tren\s+(?:de\s+(?:media\s+distan[cç]ia|cercanías|regional|mercancías|alta\s+velocidad))?\s*)(\d{4,5})(?:\s+(?:de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+?))?)`.
- **Parser v2:** Estación: `estación\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,.-]+?)`. Provincia: `(?:provincia|Provincia)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+?)`.
- **Parser v2:** Infraestructura: vía, señal, aguja, ASFA, ERTMS, talón, catenaria, CRC, CTC.
- **Parser v2:** Tags: talón, señal, comunicación, maquinista, RC, ASFA, ERTMS, desvío, mantenimiento, paso a nivel, colisión, descarrilamiento, interceptación, incendio, alta_velocidad, media_distancia, cercanías, rebase_señal, encarrilamiento, retroceso.
- **Parser v2:** Frontmatter YAML completo con campos: id, tipo_informe, fecha_suceso, hora_suceso, expediente, ubicacion (estacion, provincia, comunidad, tramo, pk, coordenadas), tipo_suceso, trenes, entidades, infraestructura, resumen, consecuencias (fallecidos, graves, leves, heridos, danos_materiales, descripcion_danos, horas_interrupcion, vía_interrumpida), geolocalizacion, conclusiones, recomendaciones, medidas_adoptadas, tags, pdf_original, md_generado, estado, fuente.

**Estrategia de geocodificación en batch:**
```python
from urllib.parse import quote
query = f"{station} {province or ''} Spain"
encoded = quote(query)  # ← SIEMPRE
url = f'https://nominatim.openstreetmap.org/search?format=json&q={encoded}&limit=1'
```

**Casos de uso:**
- Informes oficiales (CIAF) — ingesta masiva de informes de la CIAF: scraping web → markitdown → LLM structuring → base de datos SQLite → mapa interactivo Leaflet
- Informes de accidentes aéreos (CIAIAC) — misma estructura
- Informes marítimos (CIAIM) — misma estructura
- Cualquier documento oficial con estructura fija pero texto libre variable