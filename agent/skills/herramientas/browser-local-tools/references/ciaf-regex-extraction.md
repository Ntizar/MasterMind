# CIAF Regex Extraction — Extracción de PDFs sin LLM

Patrón de extracción estructurada de PDFs gubernamentales usando **PyMuPDF + regex** (sin LLM, sin API calls, 100% local). Complementario al patrón wizard con LLM (`pdf-to-json-wizard-pattern.md`).

**Proyecto:** CIAF-Tool (`/root/workspace/CIAF-Tool/`)
**Fuente:** Informes CIAF (Comisión de Investigación de Accidentes Ferroviarios, Ministerio de Transportes)

## Cuándo usar regex vs LLM

| Criterio | Regex (este patrón) | LLM (wizard pattern) |
|---|---|---|
| Formato del PDF | Estructura repetible entre informes | Estructura variable |
| Volumen | 100+ PDFs, batch processing | Cualquier volumen |
| Coste | Cero (sin API calls) | Coste por PDF |
| Velocidad | <1s por PDF | 2-5s por PDF |
| Precisión | Alta si regex bien calibrada | Alta pero variable |
| Mantenimiento | Regex frágil a cambios de formato | Prompts más resilientes |

**Regla:** Si los PDFs tienen estructura repetible (mismo organismo, mismo template) → regex. Si son heterogéneos → LLM.

## Arquitectura

```
extract.py (núcleo de extracción)
├── extract_metadata()      → expediente, fecha, título, informe_num
├── extract_station_province() → estación, provincia (del título)
├── extract_summary()       → resumen del suceso
├── extract_conclusions()   → conclusiones/causas
├── extract_recommendations() → lista de recomendaciones (hasta 10)
├── extract_entities()      → entidades implicadas
├── extract_tags()          → tags discriminantes
└── extract_severity()      → tipo, gravedad, víctimas, daños

extract_csv.py (wrapper CSV)
├── Importa TODAS las funciones de extract.py (sin duplicar)
├── Aplana recomendaciones: rec_1_numero, rec_1_destinatario, rec_1_texto...
├── Deduplica por expediente
├── Genera datos.csv (Excel) + datos.js (auto-load visor)
└── 59 columnas total
```

## Pitfalls críticos

### 1. Catastrophic backtracking con `[\s\S]*?`

**Síntoma:** El script se cuelga indefinidamente en PDFs grandes (50+ páginas).

**Causa:** `[\s\S]*?` en regex sobre texto completo causa backtracking exponencial.

```python
# ❌ MAL — Se cuelga en PDFs grandes
pattern = r'RESUMEN\s*[\s\S]*?CONCLUSIONES'
match = re.search(pattern, full_text)

# ✅ BIEN — Limitar scope y usar texto acotado
resumen_start = full_text.find('RESUMEN')
if resumen_start > -1:
    chunk = full_text[resumen_start:resumen_start + 5000]  # Limitar a 5K chars
    # Buscar dentro del chunk, no en todo el texto
```

### 2. TOC entries vs contenido real

**Síntoma:** El resumen captura entradas del índice ("RESUMEN.......... página 15") en vez del contenido real.

**Causa:** La palabra "RESUMEN" aparece en el índice antes que en el cuerpo.

```python
# ❌ MAL — Captura el primer "RESUMEN" (que es el índice)
idx = full_text.find('RESUMEN')

# ✅ BIEN — Iterar ocurrencias y filtrar
for match in re.finditer(r'RESUMEN', full_text):
    after = full_text[match.end():match.end() + 200]
    # Filtrar: índice tiene "...." o números de página
    if '....' in after or re.match(r'\s*\d+\s*$', after.strip()):
        continue
    # Filtrar: "RESUMEN DEL ANÁLISIS" no es el resumen del suceso
    if 'DEL ANÁLISIS' in after.upper():
        continue
    # El resumen real empieza con fecha del suceso
    if re.match(r'\s*El\s+\d+', after):
        resumen_start = match.end()
        break
```

### 3. Recomendaciones: cabeceras de tabla vs contenido

**Síntoma:** Las recomendaciones capturan "Destinatario | Implementador | Recomendación" (cabecera de tabla) en vez del contenido real.

**Causa:** Regex greedy captura la cabecera antes que las filas de datos.

```python
# ✅ BIEN — Parsing línea a línea, anclado por patrón de número de rec.
# Las recomendaciones CIAF tienen formato: 111/2024-1, 111/2024-2, etc.
rec_pattern = re.compile(r'(\d{3}/\d{4}-\d+)')

for match in rec_pattern.finditer(text):
    rec_num = match.group(1)
    # El destinatario está en las líneas ANTES del número
    # El texto está en las líneas DESPUÉS del número
    # Buscar hacia atrás para destinatario/implementador
    before = text[max(0, match.start()-200):match.start()]
    after = text[match.end():match.end()+500]
    # Parsear before/after línea a línea
```

### 4. Año del expediente vs año del suceso

**Síntoma:** El año del informe es 2017 pero el suceso ocurrió en 2024.

**Causa:** El expediente `0055/2017` se abrió en 2017 pero el suceso se investigó años después.

```python
# ✅ BIEN — Priorizar año del suceso sobre año del expediente
year_from_exp = int(expediente.split('/')[-1])  # 2017
year_from_date = extract_year_from_summary(summary)  # 2024
if abs(year_from_exp - year_from_date) > 2:
    year = year_from_date  # Usar año del suceso
```

### 5. Tags demasiado genéricos

**Síntoma:** Tags como `'vía'`, `'clima'` aparecen en todos los informes → sin valor discriminante.

```python
# ❌ MAL — Tags que aparecen en todo
common_tags = ['vía', 'clima', 'tren', 'ferrocarril']

# ✅ BIEN — Solo términos con valor discriminante real
common_tags = [
    'factor humano', 'señalización', 'infraestructura', 'velocidad',
    'cruzamiento', 'colisión', 'descarrilamiento',
    'ERTMS', 'ASFA', 'semáfora', 'obras',
    'animal', 'vía intrusa', 'desprendimiento', 'cable',
    'electrificación', 'telecomunicaciones', 'mantenimiento',
]
```

## CSV Flattening de recomendaciones

Las recomendaciones son una lista anidada, pero CSV es plano. Aplanar hasta 10 recomendaciones:

```python
columnas = [
    'expediente', 'fecha_suceso', 'titulo', 'tipo', 'gravedad',
    'estacion', 'provincia', 'resumen', 'conclusiones',
    'victimas_mortales', 'heridos', 'danos_materiales',
    'entidades', 'tags', 'num_recomendaciones',
    'year',
]
# Añadir rec_1_numero, rec_1_destinatario, rec_1_implementador, rec_1_texto
for i in range(1, 11):
    columnas.extend([f'rec_{i}_numero', f'rec_{i}_destinatario',
                     f'rec_{i}_implementador', f'rec_{i}_texto'])
# Total: 59 columnas
```

## Sin duplicación de código

`extract_csv.py` importa TODAS las funciones de `extract.py`:

```python
# extract_csv.py
import sys
sys.path.insert(0, os.path.dirname(__file__))
from extract import (
    extract_metadata, extract_summary, extract_conclusions,
    extract_recommendations, extract_entities, extract_tags,
    extract_station_province, extract_severity
)
# Solo añade: flattening CSV + deduplicación + output dual (CSV + JS)
```

**Resultado:** 584 líneas → 190 líneas (-67% duplicación eliminada).

## Output dual: CSV + JS

```python
# CSV para Excel/Sheets (con BOM utf-8-sig)
with open('datos.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=columnas, extrasaction='ignore')
    writer.writeheader()
    for row in rows: writer.writerow(row)

# JS para auto-load del visor en file://
import json
with open('datos.js', 'w', encoding='utf-8') as f:
    f.write('window.CIAF_DATA = ')
    json.dump(rows, f, ensure_ascii=False, indent=2)
    f.write(';\n')
```

## Dependencias

```bash
pip install PyMuPDF  # import fitz
# Sin más dependencias. Sin API calls. Sin internet.
```
