---
name: government-data-pipelines
version: "1.2.0"
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

**📐 Calidad profesional — requisito mínimo para herramientas de equipo (VERIFICADO 2026-06-26):**
Cuando el usuario dice "tengo que enviárselo al equipo y crearles una herramienta que puedan usar ellos", el estándar es **calidad de producción, no prototype**. Checklist mínimo:
- **100% de informes con título descriptivo** (no "Informe NN/YYYY")
- **0% HTML como texto plano** en el frontend ( `<strong>` se renderiza como bold, no como literal)
- **0% etiquetas duplicadas** en el panel de detalle
- **Nombres de campos consistentes** entre parser→index→frontend (mismo idioma, mismo nombre)
- **Estaciones limpias** (sin frases del PDF como nombre)
- **Fechas completas** (sin campos vacíos en informes con PDF fuente)
- **Enlaces funcionales** (PDF local + enlace oficial CIAF)

Si algún dato es visible para el usuario final, debe ser correcto y presentable. No vale "más o menos" — el usuario lo envía a su equipo y se juega su credibility.

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

### Paso 3b: Extracción por páginas vs regex completo (VERIFICADO 2026-06-26)

**⚠️ PATRÓN CRÍTICO: Extraer por páginas, NO por regex sobre texto completo.**

El enfoque regex sobre texto completo falla porque:
- El TOC (índice con puntos `.....39`) se confunde con contenido real
- Headers/footers de cada página se mezclan con el contenido
- Secciones de diferentes idiomas (inglés al final) contaminan la extracción

**Enfoque correcto — extracción por páginas:**

```python
def extract_pages(pdf_path: str) -> list[str]:
    """Extrae texto de cada página por separado."""
    doc = fitz.open(pdf_path)
    pages = [page.get_text() for page in doc]
    doc.close()
    return pages

def find_section_pages(pages: list[str]) -> dict[int, int]:
    """Encuentra en qué página empieza cada sección (saltando TOC)."""
    section_pages = {}
    for i, text in enumerate(pages):
        if i < 2:  # Skip cover + warning
            continue
        if re.search(r'\.{10,}', text):  # Skip TOC pages
            continue
        for m in re.finditer(r'(?:^|\n)\s*(\d+)\.\s+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{5,40})', text):
            num = int(m.group(1))
            if num not in section_pages:
                section_pages[num] = i
    return section_pages

def get_pages_text(pages, start_page, end_page):
    """Concatena páginas limpiando headers/footers individuales."""
    text = ""
    for i in range(start_page, min(end_page, len(pages))):
        page_text = pages[i]
        # Limpiar headers/footers de CADA página
        page_text = re.sub(r'Comisión de Investigación de\s*Accidentes Ferroviarios', '', page_text)
        page_text = re.sub(r'Informe Final de la CIAF\s+\d+/\d{4}', '', page_text)
        page_text = re.sub(r'^\s*\d{1,2}\s*$', '', page_text, flags=re.MULTILINE)  # page numbers
        page_text = re.sub(r'^.*\.{10,}.*$', '', page_text, flags=re.MULTILINE)  # TOC remnants
        text += page_text + "\n"
    return text.strip()
```

**Ventajas comprobadas:**
- 2024: 3/3 títulos, 3/3 conclusiones, 3/3 recomendaciones (vs 0/3 con regex completo)
- 2009: 43/43 títulos, 38/43 conclusiones, 25/43 recomendaciones
- Maneja 3 eras de formato automáticamente

**Detección de TOC:** Líneas con 10+ puntos consecutivos (`.{10,}`) → saltar página completa

**Manejo de bilingüismo:** Los informes 2014+ tienen sección en inglés al final. Cortar extracción de recomendaciones antes de "SAFETY RECOMMENDATIONS" o "English summary":
```python
for i in range(start + 1, min(start + 5, len(pages))):
    if re.search(r'SAFETY\s+RECOMMENDATIONS|English\s+summary', pages[i], re.IGNORECASE):
        end = i
        break
```

**Script completo:** `/root/workspace/CIAF-visor/scripts/parse_year_v2.py` — parser funcional con extracción por páginas, geocoding local, y manejo de 3 eras. Ver también: `references/page-based-pdf-extraction.md`, `references/station-coords-geocoding.md`, y `references/ciaf-memoria-parsing.md` (parseo de memorias anuales, diferente de informes individuales).

### Paso 3c: Extracción semántica de campos
El mayor reto NO es extraer texto del PDF (PyMuPDF lo hace bien), sino **estructurar el texto libre en campos JSON**.

**⚠️ PARADIGMA SHIFT (2026-06):** Para PDFs digitales con texto seleccionable, el enfoque LLM (`pdf-llm-extraction`) supera cualitativamente a los regex:
- **LLM:** 270/270 conclusiones (100%), 268/270 recomendaciones (99%), 381 trenes
- **Regex:** 194/270 conclusiones (72%), 149/270 recomendaciones (55%), 0 trenes

**Usar `pdf-llm-extraction` para batch processing de PDFs digitales.** Los regex de abajo quedan como referencia para entender la estructura de los informes, pero no son la herramienta principal recomendada.

Patrones verificados con CIAF (regex, referencia histórica):

**Expediente/informe — 4 patrones de título según era (VERIFICADO 2026-06-26):**
Los informes CIAF tienen 4 formatos de título distintos. Detectar por orden de prioridad:
```python
# Patrón 1 (2007-2008): "Investigación del accidente ferroviario ocurrido en..."
m = re.search(r'Investigaci[oó]n del accidente.*?ocurrido.*?(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})', text[:2000])

# Patrón 2 (2015-2018): "CIAF Nº X/XXXX" o "IF X/XXXX"
m = re.search(r'(?:CIAF|Informe)\s+(?:N[º°]|n[º°])\s*(\d+/\d{4})', text[:2000])

# Patrón 3 (2019-2021): "expediente nº X/XXXX ocurrido el DD.MM.YYYY"
m = re.search(r'expediente\s+n[º°]\s*(\d+/\d{4}).*?(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})', text[:2000], re.IGNORECASE)

# Patrón 4 (2022+): "Investigación del accidente Nº X/XXXX — Descripción"
m = re.search(r'N[º°]\s*(\d+/\d{4})\s*[—–-]\s*(.+?)(?:\n|$)', text[:2000])
```
**⚠️ NO confundir patrones:** Patrón 1 tiene fecha en el título; Patrón 2 tiene "CIAF" explícito; Patrón 3 tiene "expediente"; Patrón 4 tiene "—" separador. El orden de detección importa.

**Extracción de título en PDFs antiguos sin título en portada (2007-2013) (VERIFICADO 2026-06-26):**
Los PDFs pre-2014 no tienen título descriptivo en la portada — solo dicen "Investigación del accidente nº XXXX". La descripción está en el cuerpo. Estrategia multi-pass:

```python
# Pass 1: Buscar sección RESUMEN
for heading in ['RESUMEN DEL ANÁLISIS', 'RESUMEN DEL ACCIDENTE', 'RESUMEN']:
    idx = text.find(heading)
    if idx >= 0:
        # Extraer primera línea significativa después del heading
        body = text[idx+len(heading):idx+len(heading)+500]
        lines = [l.strip() for l in body.split('\n') if len(l.strip()) > 20]
        if lines:
            title = lines[0][:120]
            break

# Pass 2: Buscar patrón "El día DD de MM de AAAA"
m = re.search(r'[Ee]l\s+d[íi]a\s+\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', text[:3000])
if m:
    # Capturar hasta el siguiente punto
    end = text.find('.', m.start())
    title = text[m.start():end][:120] if end > 0 else text[m.start():m.start()+120]

# Pass 3: Buscar primera frase descriptiva del cuerpo
for pattern in [
    r'(?:accidente|incidente|avería|descarrilamiento|arrollamiento|colisión)\s+.{20,100}',
]:
    m = re.search(pattern, text[1000:4000], re.IGNORECASE)
    if m:
        title = m.group(0)[:120]
        break

# Pass 4: Fallback — usar solo expediente (ya no es "sin título")
title = f"Informe {expediente}"
```

**Resultado verificado:** 126 informes antiguos (2007-2019) pasaron de "Informe NN/YYYY" a título descriptivo extraído del PDF. 270/270 informes con título (100%).

**Métricas del parser v2 (ACTUALIZADO 2026-06-27, 270 informes):**

**Con LLM (pdf-llm-extraction, v4.0 — RECOMENDADO):**
| Campo | Éxito | % |
|-------|-------|---|
| Conclusiones | 270/270 | 100% |
| Recomendaciones | 268/270 | 99% |
| Trenes | 270/270 | 100% |
| Víctimas | 270/270 | 100% (517 total) |

**Con regex (parser v2, referencia histórica):**
| Campo | Éxito | % |
|-------|-------|---|
| Fechas | 268/270 | 99.3% |
| Títulos | 270/270 | 100% |
| Estaciones | 195/270 | 72.2% |
| Conclusiones | 194/270 | 71.9% |
| Recomendaciones | 149/270 | 55.2% |

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
# 1. PRIORIZAR nombre de estación ("Cuenca-Fernando" → Cuenca)
# 2. Buscar "Provincia: X" en contexto del accidente
# 3. Buscar primera mención de provincia DESPUÉS del encabezado (>posición 1000)
# ⚠️ NO confundir "Madrid" en dirección de sede CIAF con provincia del accidente
# ⚠️ "Albacete" en texto puede ser "CRC de Albacete" (centro de regulación), NO la provincia
def extract_province(text, station):
    # Primero: check si el nombre de estación contiene una provincia
    if station:
        for prov in PROVINCIAS:
            if prov.upper() in station.upper():
                return prov
    # Luego: buscar en el cuerpo (saltar primeros 500 chars del header)
    search_text = text[500:] if len(text) > 500 else text
    for prov in PROVINCIAS:
        if re.search(rf'\b{re.escape(prov)}\b', search_text, re.IGNORECASE):
            return prov
    return ""
```

**Entidades — normalizar variants (VERIFICADO 2026-06-26):**
```python
ENTITY_MAP = {
    'renfe operaciones': 'Renfe',
    'renfe viajeros': 'Renfe Viajeros',
    'renfe mercancías': 'Renfe Mercancías',
    'adif': 'ADIF',
    'adif av': 'ADIF AV',  # ⚠️ ADIF AV es distinto de ADIF
    'continental rail': 'Continental Rail',
    'acciona rail': 'Acciona Rail',
}
# Buscar: "empresa ferroviaria X", "operador X", "gestor de infraestructura X"

# Normalización final:case-insensitive dedup
# "RENFE" y "Renfe" → fusionar a la forma canónica
# Orden de precedencia: Renfe Viajeros > Renfe Mercancías > RENFE
def normalize_entities(entities):
    dedup = {}
    for e in entities:
        key = e.upper()
        if key not in dedup:
            dedup[key] = e
    return sorted(dedup.values())
```

**Recomendaciones — patrón split-by-number (VERIFICADO 2026-06-26):**
El patrón más robusto NO es regex complejo, sino **dividir el texto por los números de recomendación**:
```python
# 1. Encontrar la ÚLTIMA sección "RECOMENDACIONES FINALES" (no el TOC)
all_matches = list(re.finditer(r'RECOMENDACIONES\s+FINALES', text, re.IGNORECASE))
for m in all_matches:
    start = m.end()
    next_section = re.search(r'\n\s*\d+\s*\.\s+[A-ZÁÉÍÓÚÑ]{3,}', text[start:start+5000])
    end = start + next_section.start() if next_section else min(start + 5000, len(text))
    candidate = text[start:end].strip()
    if 'Destinatario' in candidate or re.search(r'\d{2,}/\d{2,4}[-–]\d', candidate):
        rec_section = candidate
        break

# 2. Limpiar headers de tabla, TOC, y APPENDIX: ENGLISH
rec_section = re.sub(r'Destinatario\s+...', '', rec_section)
rec_section = re.sub(r'APPENDIX.*$', '', rec_section, flags=re.DOTALL | re.IGNORECASE)
rec_section = re.sub(r'^[.\\.·]+\s*\d+\s*$', '', rec_section, flags=re.MULTILINE)

# 3. Encontrar TODOS los números y dividir entre ellos
num_pattern = re.compile(r'((?:IF[-\s]?)?\d+/\d{2,4}[–-]\d+)')
all_nums = list(num_pattern.finditer(rec_section))
for i, m in enumerate(all_nums):
    num = m.group(1)
    text_start = m.end()
    text_end = all_nums[i+1].start() if i+1 < len(all_nums) else len(rec_section)
    texto = re.sub(r'\s+', ' ', rec_section[text_start:text_end].strip())
    # Extraer implementador del contexto anterior
    ctx = rec_section[max(0, m.start()-300):m.start()]
    ent_match = re.findall(r'(AESF|ADIF|RENFE|CAF|FEVE|FGC|Euskotren)', ctx, re.IGNORECASE)
    implementador = ent_match[-1] if ent_match else ""
```
**⚠️ NO usar regex monolítico** — las tablas CIAF tienen formato inconsistente (saltos de línea, columnas separadas). El patrón split-by-number captura 7/7 recomendaciones vs 1/7 con regex complejo.

**Formatos de número de recomendación:** `11/2023-1`, `065/2007-1`, `IF-300109-1`, `0011/2009-1`, `11/09-1` — el regex debe aceptar `2-4` dígitos en el año: `\d+/\d{2,4}-\d+`

**Resumen del análisis — extraer del cuerpo, NO del TOC (VERIFICADO 2026-06-26):**
```python
# 1. Buscar "RESUMEN DEL ANÁLISIS Y CONCLUSIONES" o "RESUMEN DEL ANÁLISIS"
for heading in ['RESUMEN DEL ANÁLISIS Y CONCLUSIONES', 'RESUMEN DEL ANÁLISIS',
                'RESUMEN DEL ACCIDENTE', '1. RESUMEN', '0.1. RESUMEN']:
    idx = text.find(heading)
    if idx >= 0:
        start = idx + len(heading)
        # Buscar siguiente sección (número + título)
        next_sec = re.search(r'\n\s*\d+\s*\.\s+[A-ZÁÉÍÓÚÑ]', text[start:start+3000])
        end = start + next_sec.start() if next_sec else min(start + 2000, len(text))
        candidate = text[start:end].strip()
        # FILTROS: eliminar TOC (líneas con puntos), headers de página, appendix inglés
        lines = [l.strip() for l in candidate.split('\n')
                 if '.....' not in l
                 and not re.match(r'^\d+\s*$', l)
                 and not re.match(r'^Comisión de Investigación', l, re.I)
                 and not re.match(r'^[a-z\s]*(?:the |a |an |this )', l.strip(), re.I)]  # inglés
        if lines:
            return ' '.join(lines)[:2000]
```
**⚠️ PITFALL:** Muchos informes tienen "RESUMEN DEL ANÁLISIS" como entrada de TOC (con puntos `.....39`). El filtro `'.....' not in l` elimina estas entradas.

**Enlace directo a PDF (VERIFICADO 2026-06-26):**
Los PDFs de CIAF están en: `https://www.transportes.gob.es/recursos_mfom/paginabasica/recursos/{filename}.pdf`
```python
# Generar enlace directo al PDF original
pagina_ciaf = f"https://www.transportes.gob.es/recursos_mfom/paginabasica/recursos/{pdf_path.name}"
```
**⚠️ NO usar la URL del listing page** (`/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados`) — el usuario quiere enlaces directos al PDF.

**Trenes — extraer IDs y tipo (VERIFICADO 2026-06-26):**
```python
# Patrones para IDs de tren: "tren de viajeros 8604", "tren 28467", "serie S 120.050"
train_patterns = [
    r'tren\s+(?:de\s+)?(?:viajeros|mercanc[ií]as|mantenimiento)\s+(\d{3,6})',
    r'tren\s+n[º°]?\s*(\d{3,6})',
    r'serie\s+(S?\s*\d{3,5}(?:\.\d{1,3})?)',  # "serie S 120.050"
    r'(?:locomotora|coche|motive)\s+(?:n[º°]?\s*)?(\d{3,6})',
]
```
**⚠️ NO confundir con texto suelto** — el regex anterior capturaba "de", "diésel", "sin" como IDs.

**Daños materiales — booleano limpio:**
```python
# Si el texto dice "Sí" o "Se produjeron daños" → True
# Si dice "No" o está vacío → False
# NO extraer texto basura del TOC
damages = bool(re.search(r'\b[Ss]í\b|\b[Ss]e\s+produjeron\s+daños', text))
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
- **Vías de tren (si ferroviario):** Usar WMS de Tramificación ADIF (`https://ideadif.adif.es/gservices/Tramificacion/wms`, capa `Tramificacion:TramificacionComun`) — mucho más detallado que el INSPIRE WMS. Para LTV (limitaciones de velocidad), usar FeatureServer ArcGIS (`services7.arcgis.com/.../LTV_2/FeatureServer/0`) — ⚠️ `outSR=4326` hace NULL las属性 X/Y, usar `f.geometry.coordinates`. Ver `references/adif-spatial-data-apis.md` para URLs, esquemas, pitfalls y código completo. **Fallback:** OpenStreetMap vía Overpass API → GeoJSON local. **No** llamar Overpass en tiempo real desde el frontend (lento, rate-limited).

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
USER_AGENT = "CIAF-Visor/1.0"  # SIN paréntesis — Nominatim rechaza UAs con ()

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
- **🔴 Extracción por páginas > regex sobre texto completo (VERIFICADO 2026-06-26):** El regex sobre texto completo falla porque el TOC se confunde con contenido, headers/footers se mezclan, y secciones en inglés contaminan. **Solución:** extraer por páginas, detectar secciones por página, limpiar cada página individualmente. Resultado: 100% títulos vs ~60% con regex completo.
- **🔴 Detección de TOC:** Líneas con 10+ puntos consecutivos (`.{10,}`) son entradas de índice, NO contenido real. Saltar páginas que contengan estas líneas al detectar secciones.
- **🔴 SIEMPRE verificar el alcance real antes de proponer arquitectura:** No asumir el número de registros basándose solo en lo que hay descargado localmente. Contar los PDFs/disponibles en la web ANTES de diseñar la arquitectura. Ejemplo: asumir 38 PDFs cuando hay 219 en la web → arquitectura equivocada.
- **🔴 Browser tools en webs gubernamentales:** La mayoría bloquean browser tools (403). Siempre usar curl con User-Agent: `"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"`
- **🔴 PDFs que no son texto, son imágenes:** Si markitdown devuelve texto vacío, el PDF es una escaneada. Usar `ocrmypdf input.pdf output.pdf` antes de procesar.
- **🔴 Nombres de lugares ambiguos:** "Cortes" puede ser de Navarra, de La Muela, etc. Usar contexto del PDF (provincia, región) para desambiguar.
- **⚠️ User-Agent con paréntesis causa 403 en Nominatim (VERIFICADO 2026-06-26):** `"CIAF-Visor/1.0 (proyecto educativo)"` → 403 Forbidden. `"CIAF-Visor/1.0"` → 200 OK. Nominatim rechaza UAs con paréntesis.
- **⚠️ Rate limiting Nominatim bloquea IP:** Tras ~50 requests en poco tiempo, la IP queda bloqueada (429). **Solución: `station-coords.json` hardcodeado** como fuente primaria de geocoding. Nominatim como fallback solo cuando la estación no está en el JSON local.
- **⚠️ Cache de geocoding persiste None values:** Si el parser cachea resultados de Nominatim en memoria y se ejecuta sin limpiar el cache, los None values de la sesión anterior persisten. **Siempre limpiar `__pycache__` y el dict de cache al re-ejecutar el parser.**
- **🔴 Servidor HTTP y rutas relativas:** Si el frontend usa `fetch('../data/index.json')`, el servidor HTTP DEBE arrancar desde la raíz del proyecto (no desde `frontend/`). Si arranca desde `frontend/`, `../data/` queda fuera del root y devuelve 404/HTML.
- **🔴 GeoJSON de Overpass API muy grande:** 50K features de vías de tren = 24MB raw. Siempre simplificar antes de servir al frontend (reducir coords, eliminar features cortas). Técnica: precision 4 decimales (~11m), eliminar features <3 coords, subsamplear features >10 coords.
- **⚠️ Mapeo de campos parser → frontend:** El parser genera campos en español (`tipo`, `fecha_suceso`, `ubicacion.estacion`), pero el frontend puede usar campos en inglés (`type`, `date`, `city`). Añadir capa de mapeo en `loadData()` para desacoplar parser de frontend.
- **⚠️ Nombres de estación en mayúsculas + provincias (VERIFICADO 2026-06-29):** El visor puede tener estaciones en MAYÚSCULAS COMPLETAS ("MADRID-CHAMARTÍN") o con provincias entre paréntesis ("Pradell de la Teca (Tarragona)"). Limpieza: `.title()` + strip de paréntesis provinciales + truncar en puntos/comas + limpiar patrones PK. Ver `references/station-name-cleanup.md`.
- **⚠️ Geocodificación por PK via LTV (VERIFICADO 2026-06-29):** El FeatureServer LTV de ADIF tiene ~1162 puntos con PKINI/PKFIN + coordenadas. Para un PK dado, encontrar el punto cuyo rango lo contiene. 49/61 líneas CIAF tienen cobertura LTV → 71% geocodificación. Las líneas sin cobertura son regionales cortas (Cercanías, FEVE, ramales). **Pitfall:** `outSR=4326` hace NULL las propiedades X/Y — usar SIEMPRE `geometry.coordinates`. Ver `references/adif-spatial-data-apis.md` y `references/excel-json-cross-reference.md`.
- **⚠️ Estrategia de geocodificación multi-fuente (VERIFICADO 2026-06-29):** Cuando la geolocalización es crítica pero la precisión varía: (1) Excel con lat/lng reales → usar directo, (2) PK + línea → interpolar LTV (precisión ~100m), (3) nombre estación → DB local (station-coords.json, 328 entradas) + Nominatim fallback, (4) fix manual para los últimos 4-5. Orden de prioridad siempre: fuente primaria > interpolación > geocoding > manual. Resultado CIAF: de 3% a 100% geolocalizados.
- **🔴 Campo `titulo` no mapeado en frontend (VERIFICADO 2026-06-26):** El parser escribe `titulo` en JSON pero el frontend no lo incluye en el data mapping (`loadData()`). Resultado: panel de detalle muestra `"Informe 64/2024"` en vez del título descriptivo. **Regla:** cuando se añade un campo nuevo al parser, SIEMPRE verificar que el frontend lo mapea en `loadData()`. Patrón: añadir `titulo: r.titulo || ''` en el objeto mapped.
- **🔴 SUBAGENTE QUE INVENTA DATOS PARA AÑOS SIN FUENTE (VERIFICADO 2026-06-26):** Cuando se delega parseo de PDFs a subagentes, estos pueden crear JSONs con datos fabricados para años donde no existe el PDF fuente. Ejemplo: 17 memorias reales (2008-2024) + subagent genera 2025.json fabricado (sin PDF) y 2007.json con números inventados. **Detección:** después de delegar, verificar que cada JSON generado tiene un PDF correspondiente en `pdfs/`. `os.path.exists()` para cada año. **Corrección:** eliminar JSONs sin fuente. **Regla:** SIEMPRE validar que el subagente tiene acceso al PDF antes de confiar en su output. Los subagentes no distinguen "no pude parsear" de "inventé datos".
- **⚠️ Contar solo la primera entidad en array (VERIFICADO 2026-06-26):** Cuando un informe tiene `entities: ["ADIF", "Renfe"]`, usar solo `r.entity` (= `r.entities[0]`) para KPIs subcuenta entidades. KPI mostraba 2 entidades cuando había 17 reales. **Corrección:** iterar sobre TODO el array `r.entities`, no solo el primero. Patrón: `new Set(reports.flatMap(r => r.entities || [r.entity]))`.
- **🔴 LLM fragmenta párrafos en líneas sueltas (VERIFICADO 2026-06-28):** Cuando el pipeline LLM extrae texto de conclusiones/recomendaciones, puede partir cada párrafo en líneas individuales de ~60 chars. El 49.8% de los informes CIAF tenía exactamente 20 items (corte artificial del pipeline), cada uno era un bullet suelto en vez de un párrafo coherente. **Detección:** items < 100 chars que no terminan en punto, o exactamente 20 items (corte del pipeline). **Solución:** script de re-combinación que une líneas por puntuación (línea termina sin punto → siguiente es continuación), detecta párrafos por mayúsculas tras punto, y limpia headers embebidos (5.1. RESUMEN, RECOMENDACIONES). Ver `references/llm-text-recombination.md` para el algoritmo completo. **Multi-pass:** pasada 1 (re-combinación), pasada 2 (limpieza de headers), pasada 3 (limpieza final de artefactos). Resultado CIAF: de 1022 items sueltos a ~600 párrafos coherentes (230 chars/item promedio).
- **⚠️ Fusión de datasets con esquemas diferentes (VERIFICADO 2026-06-27):** Cuando existen dos fuentes de datos para el mismo conjunto (ej: CIAF-visor con esquema rico + ciaf-data con esquema simple), fusionar selectivamente: (1) usar el esquema más rico como base, (2) mejorar solo los campos débiles del dataset base con los valores del otro, (3) NUNCA sobrescribir campos que ya están completos. Resultado CIAF: 62/270 informes mejorados, +111 conclusiones, +59 recomendaciones. **Clave de emparejamiento fiable:** número de expediente (ej: `0062/2007`), extraído con regex `Nº?\\\\s*(\\\\d{3,4}/\\\\d{4})` del título. Ver `references/data-enrichment-merging.md` para el patrón completo con código.
- **⚠️ Dos conjuntos de datos para el mismo proyecto (VERIFICADO 2026-06-29):** El visor CIAF lee de `data/reports/YYYY.json`, mientras el pipeline genera `individual/*.json`. Son estructuras diferentes (schema del visor vs schema del pipeline). Si se corrigen los individual, HAY QUE propagar los cambios al visor. No asumir sincronización automática. **Script de sync:** cruzar por expediente, aplicar correcciones al visor, backup antes de batch. Ver `references/visor-data-batch-fix.md`.
- **⚠️ Severidad "fatal"/"leve" del visor vs RD 929/2022 (VERIFICADO 2026-06-29):** El visor original usa vocabulario legacy ("fatal"=199, "leve"=68, "grave"=2) pero la taxonomía oficial del RD 929/2022 es "muy grave"/"grave"/"menor". Siempre recalcular desde datos numéricos (víctimas) cuando haya fuente Excel. Mapeo: fatal→muy grave, leve→menor, grave→grave. El index.json del visor TAMBIÉN contiene gravedad — actualizar ahí también.
- **⚠️ LIMPIEZA AGRESIVA DESTRUYÓ NOMBRES REALES (VERIFICADO 2026-06-29):** La limpieza de estaciones que elimina paréntesis y trunca en "de" destruyó nombres reales: "Vila-real (Castellón)" → "Vila", "Sama de Langreo (Asturias)" → "La". **Reglas:** (1) eliminar SOLO provincia entre paréntesis al FINAL, (2) preservar "de", "del", "la", "el", (3) si el resultado es < 4 chars, devolver el original y extraer del resumen. Ver `references/station-name-cleanup.md` sección "LIMPIEZA DEMASIADO AGRESIVA".
- **⚠️ Excel tiene provincias equivocadas (VERIFICADO 2026-06-29):** El Excel tiene la provincia incorrecta para ~25% de los registros. La fuente fiable es el resumen del informe PDF. SIEMPRE cruzar provincia desde el resumen cuando esté disponible. Ver `references/excel-json-cross-reference.md` sección 8.
- **⚠️ Cruce Excel ↔ JSONs con matching caótico (VERIFICADO 2026-06-29):**
- **⚠️ LLM que inventa datos:** El prompt DEBE incluir: "NO inventes datos. Si un campo no existe en el PDF, pon null."
- **⚠️ Consistencia de idioma en campos JSON (VERIFICADO 2026-06-26):** El parser escribe `conclusions` (inglés) pero el index generator y frontend esperan `conclusiones` (español).Resultado: 270 JSONs con campo `conclusions` → index.json no los encontraba → frontend mostraba 0 conclusiones. **Corrección:** mass find-replace `conclusions`→`conclusiones`, `recommendations`→`recomendaciones` en los 270 archivos. **Regla:** definir el schema de campos ANTES del parser y verificar que parser→index→frontend usan los mismos nombres. Preferir español si el frontend es en español.
- **🔴 `patch()` con strings no únicos causa reemplazos múltiples (VERIFICADO 2026-06-29):** Al usar `patch()` en `execute_code` con `mode="replace"` (default), si el `old_string` aparece múltiples veces en el archivo, se reemplazan TODAS las ocurrencias. Esto destruyó un HTML de 1435 líneas al reemplazar `(r.severity||'').replace(/ /g,'-')` (que aparecía 6 veces) con un bloque JavaScript completo. **Solución:** (1) SIEMPRE verificar unicidad con `grep -c "old_string" archivo` antes de patchear, (2) usar strings contextualizados que solo aparezcan una vez (incluir función contenedora, comentarios, o contexto adicional), (3) si se necesita replace_all, ser explícito con `replace_all=true`, (4) como alternativa segura para reemplazos grandes, usar `write_file` con el contenido completo reconstruido.
- **⚠️ Estructura variable:** Algunos PDFs pueden tener secciones ligeramente diferentes. Tener un fallback que procese sin schema estricto.
- **⚠️ Paginación en webs gubernamentales:** Los listados de documentos suelen tener paginación. Recorrer todas las páginas antes de descargar PDFs.
- **⚠️ Encoding en PDFs antiguos:** PDFs antes de 2015 pueden tener caracteres especiales mal codificados. Usar `chardet` o forzar UTF-8.
- **⚠️ PATRÓN URL POR AÑOS:** Las webs gubernamentales cambian su estructura de URL entre años. Para CIAF: 2015-2016 usan `/AÑO`, 2017-2025 usan `/infofin-AÑO`. **Siempre probar ambas variantes antes de descartar años.**
- **⚠️ 4 PATRONES DE PDF DIFERENTES:** Los PDFs del mismo repositorio pueden usar rutas distintas según el año de publicación (paginabasica/recursos/, pdf/UUID/, recursos_mfom/, comodin/recursos/). Usar múltiples patrones regex simultáneamente.
- **🔴 NO hardcodear etiquetas geográficas aproximadas (VERIFICADO 2026-06-29):** Etiquetas de líneas ferroviarias con posiciones `[lat, lng]` inventadas se ven **terrible** — no se alinean con la geometría real del mapa WMS/WFS. **No crear capas de texto hardcodeado sobre mapas reales.** Si se necesitan nombres de líneas, usar atributos de las APIs oficiales (LTV `DESCLINEA`, WFS `nombre`) como popup/tooltip en interacción de clic. Ver `references/adif-spatial-data-apis.md`.

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

## Post-extracción: Limpieza y geocodificación batch (NUEVO 2026-06-29)

Después de extraer datos del PDF/Excel, la fase crítica es **limpiar y geolocalizar**. Patrón verificado con CIAF (269 registros):

### Cadena de geocodificación por prioridad
1. **DB local** (`station-coords.json`, 355+ entradas) → fuente primaria, NO Nominatim
2. **PK + línea → interpolación LTV** (FeatureServer ADIF, ~100m precisión)
3. **Nominatim como último fallback** con `time.sleep(1.1)` entre requests
4. **Fix manual** para los últimos 4-5 registros que fallan todo

**⚠️ Nominatim bloquea IP tras ~50 requests.** SIEMPRE usar DB local como primaria. Nominatim solo para registros nuevos que la DB no tiene.

### Extracción de estación desde resumen cuando el nombre está vacío o truncado
Cuando `ubicacion.estacion` está vacío, es genérico ("La", "El", "Pk", "San", "Sant") o fue destruido por limpieza agresiva, extraer del resumen:

**⚠️ LIMPIEZA AGRESIVA DESTRUYÓ NOMBRES REALES (VERIFICADO 2026-06-29):**
"Vila-real (Castellón)" → limpieza eliminó "(Castellón)" + truncó en "de" → "Vila" (3 chars, destruido).
**Regla:** si el nombre limpiado es < 4 chars o está en GENERIC_NAMES (`la`, `el`, `los`, `san`, `sant`, `de`, `del`, `que`, `pk`), NO limpiar — extraer del resumen.
```python
patterns = [
    r'estaci[oó]n\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+(?:de|del|la|el)\s+[A-ZÁÉÍÓÚÑ]?[a-záéíóúñ]+)*)',
    r'apeadero\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
    r'paso a nivel\s+(?:de\s+|entre\s+[^i]+y\s+)([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
    r'en\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+(?:de|del|la|el)\s+[A-ZÁÉÍÓÚÑ]?[a-záéíóúñ]+)*)\s*,',
]
```

### Detección de coords por defecto
```python
# Buscar registros con coordenadas idénticas (>5 = defecto)
from collections import Counter
coord_counts = Counter((r['lat'], r['lng']) for r in records if r.get('lat'))
default_coords = [c for c, n in coord_counts.items() if n > 5]
# Estos registros necesitan re-geolocalización
```

### Provincia: resumen > Excel (CRÍTICO)
**El Excel tiene provincias equivocadas para ~25% de los registros.** La fuente fiable es el resumen del informe PDF, que menciona la provincia entre paréntesis después del nombre de la estación. Ver `references/excel-json-cross-reference.md` sección 8 para el patrón completo de extracción.

**Regla:** cuando el Excel y el resumen discrepen en provincia, SIEMPRE confiar en el resumen. El Excel puede tener la provincia de la sede CIAF (Madrid) o de otro registro cercano.

### Limpieza de nombres — reglas
- `title()` para mayúsculas → Title Case
- Eliminar `(Provincia)` del final
- Eliminar suffixes: `desde`, `por`, `y éste`, `PK NNN`
- **NUNCA** eliminar si el resultado queda <4 chars → usar fallback del resumen
- Verificar que la provincia del nombre coincide con la provincia registrada

## Referencias
- `references/ciaf-scraping.md` → Procedimiento completo de scraping: URLs, curl/Python, estructura nombres PDF, pitfalls
- `references/ciaf-data-architecture-2026.md` → Arquitectura completa CIAF: inventario 277 informes, 3 eras de formato, JSON particionado, relaciones entidades, diseño del visor
- `references/data-enrichment-merging.md` → Patrón de enriquecimiento/fusión de datasets: emparejamiento por expediente, fusión selectiva, geocodificación batch con DB local
- `references/llm-text-recombination.md` → Algoritmo de re-combinación de texto fragmentado por LLM: detección, multi-pass limpieza, métricas de resultado
- `references/adif-spatial-data-apis.md` → APIs espaciales de ADIF: WMS red ferroviaria, LTV (limitaciones velocidad) FeatureServer, Tramificación WFS. URLs, esquemas, código Leaflet, pitfalls

## Data Pipeline Absorbidos

### CIAF Data Pipeline (absorbido de `ciaf-data-pipeline`)
- **Cross-reference pitfall:** cruzar por expediente SIN año causa corrupción masiva. Normalizar: "50/2009" → "0050/2009"
- **Estrategia de geolocalización:** (1) JSON individual coords → (2) PK+LTV → (3) station-coords.json → (4) Nominatim → (5) manual
- **Rendering de recomendaciones:** 4 esquemas de dict diferentes según año/parser. Frontend DEBE buscar: `rec.texto || rec.contenido || rec.text`
- **Limpieza post-auditoría:** frontend solo carga index.json + reports/YYYY.json. Eliminar: pdfs/, data/images/, train-tracks.geojson, ltv_lookup.json, station-coords.json
- **Pitfall CI/CD:** eliminar archivos del repo → verificar .github/workflows por referencias rotas
- **Verificación post-fix checklist:** 9 puntos obligatorios (sin resúmenes duplicados, estaciones >3 chars, coords consistentes, etc.)

### Data Pipeline Audit (absorbido de `data-pipeline-audit`)
Procedimiento sistemático de 6 fases:
1. Inventario de fuentes (contar registros por fuente)
2. Comparación por cobertura (gaps por año/categoría)
3. Comparación campo a campo (discrepancias)
4. Taxonomía y normalización (comparar granularidad)
5. Campos de calidad (% nulls, formatos, textos)
6. Informe de resultados (cubierta, faltantes, taxonomía, geolocalización, acciones)

**Pitfalls clave:** matching por nombres caóticos, severidad mal clasificada, limpieza que destruye datos, coordenadas por defecto contaminando dataset.

### NAP Data Pipeline (absorbido de `nap-data-pipeline`)
- **161 datasets, 0.65 GB** de GTFS español desde NAP API
- API: `https://nap.transportes.gob.es/api/v2/` con header `ApiKey`
- Endpoints: `/conjunto-dato` → `/conjunto-dato/{id}` → `/fichero/{id}/descarga` → descarga ZIP
- **⚠️ Enlaces S3 caducan en 15 min** — descargar rápido
- **Solo GTFS-ZIP descargables** — filtrar por `nombreTipoFichero`
- Script: `descargar-nap.py` con modos full/delta/dry-run
- Cron: domingo 06:00 UTC, delta mode

### Spanish Open Data Collection (absorbido de `spanish-open-data-collection`)
- **Fuentes bloqueadas desde servidor:** datos.gob.es (403+CAPTCHA), Idealista, Fotocasa, Portal de Vivienda
- **INE REST API SÍ funciona:** `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{id}?tip=AM&nult=1` — sin key, sin CAPTCHA
- **Patrón de estimación:** precios base por provincia + multiplicadores intra-provincia
- **ArcGIS FeatureServer pitfall:** `outSR=4326` → attributes X/Y NULL, usar `f.geometry.x/y`
- Referencias internas: `references/blocked-sources-checklist.md`, `references/ine-rest-api-working.md`, `references/spanish-housing-province-prices-2024.md`

## Embedded JSON Extraction — Parsear JSON desde Archivos de Código (absorbido de `embedded-json-extraction`)

### Por qué falla bracket counting simple
1. `]` dentro de strings (ej: `"trenes": []`) cierra prematuramente el depth counter
2. Código trailing después de `];` se incluye en la extracción
3. Secuencias double-escape (`\\n`, `\\s`) confunden la inspección de strings
4. Smart quotes y chars UTF-8 son JSON válido pero activan falsos alarms

### Patrones de extracción
- **Pattern 1:** Bracket counter FUERA de strings (ignora corchetes dentro de comillas)
- **Pattern 2:** Parsear objetos individuales cuando el array parsea mal
- **Pattern 3:** Regex boundary detection (buscar patrón trailing como `];\n//`)
- **Pattern 4:** `demjson3` para parsing leniente (maneja Python None, trailing commas)
- **Pattern 5:** Wrap y validar (envolver entre `[` y `]`, probar `json.loads` → `demjson3`)

### Pitfalls
- `]` dentro de string cierra prematuramente depth counter ingenuo
- Error "Extra data" de `json.loads()` = JSON válido pero contenido trailing
- Newlines double-escaped en strings son JSON válido
- Smart quotes en strings JSON están bien (UTF-8 válido)

### Scripts
- `scripts/extract-embedded-json.py` — Script completo para extracción
- `references/ciaf-json-extraction.md` — Transcript completo con edge cases
