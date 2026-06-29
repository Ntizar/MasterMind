---
name: ciaf-data-pipeline
description: "Pipeline completo CIAF: PDF → JSON individual → cruzar con Excel → visor web. Geolocalización, limpieza, taxonomía RD 929/2022."
version: "1.0.0"
tags: [ciaf, pipeline, data, geocoding, railroad, spain]
---

# CIAF Data Pipeline

Pipeline de datos para el visor de informes CIAF (Comisión de Investigación de Accidentes Ferroviarios).

## Arquitectura de datos

```
PDFs originales → JSON individuales (pdf_to_jsonv2) → Cruzar con Excel → reports/YYYY.json (visor)
                  /root/workspace/ciaf-data/           /root/workspace/CIAF-visor/data/reports/
                  data/individual/                     
```

**Fuentes de verdad (en orden de fiabilidad):**
1. **JSON individuales** (`ciaf-data/data/individual/`) — generados directamente del PDF, contienen el resumen correcto
2. **Excel** (`260218_Base_Datos_CIAF_1.xlsx`) — metadatos estructurados (fecha, tipo, víctimas, pk, línea)
3. **JSONs del visor** (`CIAF-visor/data/reports/YYYY.json`) — targets de visualización, se rellenan desde fuentes 1+2

## ⚠️ Pitfall crítico: Cross-reference por expediente incompleto

**El error más grave descubierto:** cruzar por número de expediente **sin el año** causa corrupción masiva de datos.

```
# MAL — el mismo resumen se copia a 5 registros:
exp = "50"  # ← matching parcial
# Resultado: 50/2008, 50/2009, 50/2010, 50/2011, 50/2012 → todos con el texto de 50/2009

# BIEN — matching completo:
exp = "0050/2009"  # ← número + año
```

**Síntomas:** múltiples registros mostrando el mismo "Resumen del análisis" en el visor, con fechas/lugares que no coinciden con el expediente.

**Detección:** buscar resúmenes duplicados:
```python
from collections import Counter
resumen_map = {}
for r in all_records:
    res = r['analisis']['resumen'][:80]
    resumen_map.setdefault(res, []).append(r['expediente'])
duplicates = {k: v for k, v in resumen_map.items() if len(v) > 1}
```

**Corrección:** re-cruzar usando expediente normalizado (número con ceros + `/` + año):
```python
# Normalizar: "50/2009" → "0050/2009"
parts = exp.split('/')
norm_exp = f"{parts[0].zfill(4)}/{parts[1]}"
```

## Geolocalización

### Estrategia en orden de preferencia
1. **Coords del JSON individual** — el parser extrae lat/lng cuando aparecen en el PDF. Son las más precisas (~100m)
2. **PK + línea** del Excel → interpolación con ADIF LTV FeatureServer (~500m)
3. **Nombre de estación** → lookup en `data/station-coords.json` (355 entries)
4. **Nominatim** → fallback con nombre + provincia (~2km)
5. **Coords manuales** → para registros sin datos suficientes

**Pitfall crítico:** la interpolación por PK puede dar.coords muy alejadas del punto real (diferencias > 0.1 grado). SIEMPRE verificar coords del JSON individual antes de usar LTV. Si el individual tiene coords válidas, usarlas aunque el LTV dé otras.

### Pitfall: Nominatim rate limiting
Nominatim bloquea con HTTP 429 tras ~20 peticiones. Soluciones:
- Acumular geocodificaciones y hacerlas en batch con 1.1s entre peticiones
- Usar coordenadas hardcodeadas para estaciones conocidas
- La DB de estaciones (`station-coords.json`) es la fuente principal

### Pitfall: Nombres de estación genéricos
Nombres como "La", "San", "Los", "Sant" son resultados de parsing truncado. **Nunca geolocalizar con estos nombres** — siempre extraer el nombre completo del resumen del informe.

Patrón de extracción:
```python
# Buscar en resumen: "estación de X (Provincia)"
m = re.search(r'estaci[oó]n\s+de\s+(\w[\w\s]+)\((\w[\w\s]+)\)', resumen)
station, province = m.group(1), m.group(2)
```

## Limpieza de nombres de estación

**Problema:** el parsing original deja nombres con:
- Provincia entre paréntesis: "Tolosa (Guipúzcoa)" → "Tolosa"
- Mayúsculas: "TRASONA" → "Trasona"
- Puntos finales: "Atocha." → "Atocha"
- Nombres truncados por limpieza agresiva: "Vila-real" → "Vila"

**Regla:** la limpieza NUNCA debe eliminar partes del nombre que no sean provincia entre paréntesis.

## Taxonomía de severidad (RD 929/2022)

| Categoría | Definición |
|-----------|-----------|
| **Muy grave** | Al menos 1 fallecido O lesiones muy graves |
| **Grave** | Lesiones graves sin fallecidos, evacuación significativa, daños materiales importantes |
| **Menor** | Sin víctimas ni daños significativos |

**Mapping desde Excel:** columna `muertos` (>0 → muy grave), `heridos_graves` (>0 → grave), resto → menor.

## Tipología de sucesos (RD 929/2022)

Categorías normalizadas:
- Accidente (colisión, descarrilamiento, atropello)
- Incidente (conato, rebasamiento de señal, fallo infraestructura)
- Sin categorizar

El Excel tiene ~58 categorías que se agrupan en ~18 normalizadas.

## Restauración de datos originales tras cross-reference

**Pitfall crítico:** el cross-reference script sobreescribe campos con contenido generado por IA o datos de otros años. SIEMPRE restaurar desde JSON individuales después del cruce.

### Campos a restaurar (en orden de prioridad)

1. **Título** — usar `titulo` del JSON individual (formato original del PDF: "INFORME FINAL SOBRE EL ACCIDENTE FERROVIARIO Nº 0033/2009..."). NUNCA usar el formato generado por IA ("IF 0033/2009 — El día...")

2. **Conclusiones** — usar `conclusiones` del JSON individual (texto real extraído del PDF). El campo del visor frecuentemente tiene texto diferente inventado.

3. **Recomendaciones** — usar `recomendaciones` del JSON individual.

4. **Estación y provincia** — usar del JSON individual cuando el campo del visor tiene valores incorrectos (fragmentos como "clase C" o datos de otros años).

5. **PK y tramo** — restaurar desde JSON individual si el visor no los tiene.

6. **Tipo de suceso** — usar `tipo_suceso_normalizado` del JSON individual.

### Patrón de restauración

```python
# Normalizar expediente para matching
parts = exp.split('/')
norm_exp = f"{parts[0].zfill(4)}/{parts[1]}"

# Restaurar desde individual
if norm_exp in ind_index:
    ind = ind_index[norm_exp]
    r['titulo'] = ind.get('titulo', r['titulo'])
    r['conclusiones'] = ind.get('conclusiones', r['conclusiones'])
    r['ubicacion']['estacion'] = ind.get('estacion') or r['ubicacion']['estacion']
    r['ubicacion']['provincia'] = ind.get('provincia') or r['ubicacion']['provincia']
```

## Extracción de estación desde Excel "lugar"

El campo `lugar` del Excel contiene descripciones largas como:
- "Paso a nivel clase C en la población de Monforte de Lemos, carretera..."
- "P.K. 104,857, entre Salamanca y Babilafuente"

**Pitfall:** extracciones regex pueden devolver fragmentos como "clase C" o "clase A" en vez del nombre real de la estación.

**Solución:** usar el JSON individual como fuente primaria para estación. Solo usar Excel como fallback cuando el individual no tiene estación.

```python
# Orden de preferencia para estación:
# 1. JSON individual (si tiene nombre > 3 chars y no es fragmento)
# 2. Excel lugar (con extracción limpia)
# 3. Coordenadas geolocalizadas

fragments = {'clase A', 'clase B', 'clase C', 'clase P', 'plena vía'}
if ind_est and len(ind_est) > 3 and ind_est not in fragments:
    station = ind_est
```

## Corrección de provincias

**Pitfall:** los JSON individuales pueden tener provincias incorrectas heredadas del parser. El Excel también puede tener errores (ej: Ponferrada → Barcelona).

**Estrategia (en orden de fiabilidad):**
1. **Resumen del informe** — si menciona "en Asturias", la provincia debe ser Asturias
2. **Excel** — más fiable que el parser para ubicaciones
3. **JSON individual** — fallback cuando no hay Excel

**Verificación obligatoria:** después de cruzar, comparar provincia del Excel vs provincia del JSON individual. Si difieren, investigar cuál es correcta mirando el resumen.

```python
# Verificar consistencia provincia
for exp, ind in ind_index.items():
    if exp in excel_data:
        ex_prov = excel_data[exp]['provincia']
        ind_prov = ind.get('provincia', '')
        if ex_prov and ind_prov and ex_prov.lower() != ind_prov.lower():
            print(f"MISMATCH: {exp} | Excel: {ex_prov} | Individual: {ind_prov}")
```

## Documentación del proyecto (README)

Para que el proyecto sea mantenible sin su autor, el README debe incluir:

### Estructura mínima requerida
1. **¿Qué es?** — una frase clara + lista de capacidades
2. **Fuentes de datos** — tabla con fuente, cantidad, período, enlace
3. **Estructura del proyecto** — árbol de carpetas con comentarios
4. **Flujo de datos** — diagrama ASCII del pipeline completo
5. **Fuentes de verdad** — tabla de qué campo viene de dónde
6. **Scripts** — tabla de cada script con función, entrada, salida
7. **Cómo añadir datos** — paso a paso para nuevos informes
8. **Errores conocidos** — lo que se descubrió y cómo se resolvió
9. **Normativa** — marco legal aplicable
10. **Licencia** — datos públicos + código MIT

### Ejemplo de sección "Fuentes de verdad"

```markdown
| Campo | Fuente | Notas |
|-------|--------|-------|
| Título | JSON individual | Título original del PDF |
| Conclusiones | JSON individual | Texto literal del informe |
| Severidad | Excel + RD 929/2022 | "fatal" → "muy grave" |
| Provincia | Excel + resumen | Verificar consistencia |
| Coordenadas | JSON individual | Más precisas que LTV |
```

### Pitfall: README genérico
Un README con solo "instalación" y "uso" no sirve para mantener el proyecto. Debe explicar el **porqué** de las decisiones de diseño y los **errores descubiertos** para que el siguiente desarrollador no los repita.

## Detección de coordenadas duplicadas erróneas

**Técnica para encontrar geolocalizaciones incorrectas:** agrupar registros por coordenadas redondeadas y buscar grupos donde estaciones de provincias diferentes comparten las mismas coords.

```python
from collections import defaultdict
coord_groups = defaultdict(list)
for r in all_records:
    lat = r.get('ubicacion', {}).get('lat')
    lng = r.get('ubicacion', {}).get('lng')
    if lat and lng:
        key = f"{lat:.4f},{lng:.4f}"
        coord_groups[key].append(r)

# Investigar grupos con >1 registro de provincias diferentes
for coord, records in coord_groups.items():
    if len(records) > 1:
        provinces = set(r['ubicacion']['provincia'] for r in records)
        if len(provinces) > 1:
            print(f"DUPLICATE: {coord} — {len(records)} records from {provinces}")
```

**Ejemplo real:** 3 registros (Zaragoza, Soria, Lleida) compartían coords (41.63, 0.51) porque la interpolación PK asignó la misma ubicación a líneas diferentes.

## Geolocalización por Nominatim cuando PK falla

Cuando la interpolación PK da coordenadas claramente erróneas (verificación por provincia), usar Nominatim directamente:

```python
import requests, time

def geocode_station(station, province):
    """Geocodificar estación usando Nominatim"""
    query = f"{station}, {province}, España"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    headers = {'User-Agent': 'CIAF-Visor/1.0'}
    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    return None, None

# Rate limit: 1.1s entre peticiones
lat, lng = geocode_station("Plasencia de Jalón", "Zaragoza")
time.sleep(1.1)
```

**Regla:** si la provincia del registro no coincide con la ubicación de las coords, la geolocalización es incorrecta y debe rehacerse con Nominatim.

## Verificación post-fix

```python
# Checklist obligatorio después de cualquier fix:
# 1. Sin resúmenes duplicados (excepto legítimos)
# 2. Sin nombres de estación <= 3 caracteres
# 3. Sin coordenadas por defecto (A Coruña: 43.336, -8.3953)
# 4. Provincia consistente con el resumen
# 5. Total registros = total en Excel (≈278-280)
# 6. Títulos en formato original del PDF (no formato IA)
# 7. Conclusiones extraídas del PDF (no generadas por IA)
# 8. Estaciones > 3 caracteres, sin fragmentos ("clase C", etc.)
# 9. Sin grupos de coords duplicadas con provincias diferentes
# 10. Coords del JSON individual preferidas sobre LTV
```

### Verificación en GitHub después de push

**Pitfall:** el usuario puede ver datos antiguos por caché del navegador. SIEMPRE verificar que GitHub sirve los datos correctos antes de informar "fix completado".

```bash
# 1. Verificar raw content en GitHub
curl -s "https://raw.githubusercontent.com/Ntizar/CIAF-visor/master/data/reports/2012.json" | python3 -c "
import sys,json; data=json.load(sys.stdin)
for r in data:
    if r.get('expediente') == '0050/2012':
        print(f'lat={r[\"ubicacion\"][\"lat\"]}, lng={r[\"ubicacion\"][\"lng\"]}')
"

# 2. Verificar que el frontend carga los datos
# Abrir DevTools → Console → ejecutar:
# allReports.find(x => x.expediente === '0050/2012')
```

**Pitfall: caché del navegador** — si el usuario reporta "sigue mal" después de push correcto:
1. Pedir `Ctrl+Shift+R` (hard refresh)
2. O abrir en ventana incógnita
3. Verificar con `curl` que GitHub sirve los datos nuevos
4. Si persiste, puede haber un problema real → investigar

### Verificación de que los datos están en GitHub

```bash
# Verificar que el push llegó
cd /root/workspace/CIAF-visor && git log --oneline -3

# Verificar raw content
curl -s "https://raw.githubusercontent.com/Ntizar/CIAF-visor/master/data/reports/YYYY.json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d), 'records')"

# Verificar que no hay diff local vs remote
git diff origin/master --stat
```

## Estructura del proyecto (post-limpieza 2026-06-29)

```
CIAF-visor/
├── data/
│   ├── index.json              # Índice: años disponibles, stats globales
│   ├── reports/YYYY.json       # 269 informes (2007-2025) — FUENTE DE VERDAD
│   └── memorias/YYYY.json      # 18 resúmenes anuales (2007-2024)
├── frontend/
│   └── index.html              # SPA completa (CSS+JS inline)
└── scripts/
    ├── parse_all.py            # Pipeline: PDF → JSON
    ├── parse_reports_v2.py     # Parser v2
    ├── parse_year_v2.py        # Parser por año
    ├── generate_index.py       # Genera index.json
    ├── sync.py                 # Sincronización
    ├── test_parser.py          # Tests
    └── archive/                # Scripts de fix completados
```

**Nota:** `pdfs/`, `data/images/`, `data/train-tracks.geojson`, `ltv_lookup.json`, `data/station-coords.json`, `data/relations.json` fueron eliminados en la limpieza de 2026-06-29. El frontend solo usa los JSONs de data/.

## Limpieza post-auditoría

### Qué eliminar (archivos que el frontend NUNCA usa)
Tras auditar el frontend con `grep` de fetch/references, se confirmó que solo carga:
1. `data/index.json` → lista de años
2. `data/reports/YYYY.json` → informes
3. `data/memorias/YYYY.json` → memorias anuales
4. APIs externas: IGN WMTS, ADIF WMS, ArcGIS LTV

**Archivos seguros de eliminar** (verificados con grep que no aparecen en index.html):
- `pdfs/` — PDFs originales (322 MB). Útiles como archive, pero el frontend no los carga
- `data/images/` — Imágenes extraídas de PDFs (249 MB). Nunca referenciadas
- `data/train-tracks.geojson` — GeoJSON local (7.5 MB). Frontend usa WMS de ADIF
- `ltv_lookup.json` — Lookup PK→coords (170 KB). Frontend carga LTV desde ArcGIS en vivo
- `data/station-coords.json` — Coords de estaciones (32 KB). Nunca referenciado
- `data/relations.json` — Relations pre-computadas (51 KB). Frontend calcula in-memory
- `data/reports/YYYY/` — Subdirectorios con índices obsoletos
- `frontend/css/kaizen.css` — CSS no referenciado (todo inline en HTML)
- `frontend/js/` — Directorio vacío

### ⚠️ Pitfall: verificar CI/CD tras eliminar archivos

**Cuando elimines archivos del repo, SIEMPRE revisar `.github/workflows/`** por si algún workflow los referencia.

```bash
# Buscar referencias a archivos eliminados en workflows
grep -rn 'train-tracks\|station-coords\|relations\|ltv_lookup\|kaizen.css' .github/workflows/
```

**Ejemplo real:** tras limpiar CIAF-visor (eliminar 330 MB), el workflow `pages.yml` intentaba `cp data/train-tracks.geojson data/relations.json frontend/css/` → deploy falló con exit code 1. Fix: reescribir el workflow para copiar solo lo que existe.

### Regenerar index.json tras limpieza

Si se eliminan archivos dependientes, regenerar `index.json`:

```python
import json, os
from collections import defaultdict

reports_dir = "data/reports"
years, total, victims, heridos = [], 0, 0, 0
types, severities, entities = defaultdict(int), defaultdict(int), defaultdict(int)
stats_by_year = {}

for fname in sorted(os.listdir(reports_dir)):
    if not fname.endswith('.json'): continue
    year = int(fname.replace('.json', ''))
    years.append(year)
    data = json.load(open(os.path.join(reports_dir, fname)))
    yv, yh, yc = 0, 0, len(data)
    for r in data:
        v = r.get('consecuencias', {}).get('victimas_mortales', 0) or 0
        h = r.get('consecuencias', {}).get('heridos', 0) or 0
        total += 1; victims += v; heridos += h; yv += v; yh += h
        types[r.get('tipo', 'desc')] += 1
        severities[r.get('gravedad', 'desc')] += 1
        for e in r.get('entidades', []): entities[e] += 1
    stats_by_year[year] = {"total": yc, "victimas": yv, "heridos": yh}
```

## Rendering de recomendaciones en el frontend

### Pitfall: esquemas de dict inconsistentes

Las recomendaciones en los JSONs tienen **4 esquemas de dict** diferentes según el año/parser:

| Frecuencia | Keys | Texto en |
|-----------|------|----------|
| 181x | `numero`, `destinatario`, `texto` | `texto` |
| 52x | `numero`, `implementador`, `texto` | `texto` |
| 26x | `numero`, `destinatario`, `contenido` | `contenido` ← NO `texto` |
| 5x | `número`, `destinatario`, `texto` | `texto` ← tilde en `número` |

**El frontend DEBE buscar todas las variantes:**
```javascript
const num = rec.numero || rec.número || '';
const dest = rec.destinatario || rec.destinatarios || rec.implementador || '';
const body = rec.texto || rec.text || rec.contenido || '';
```

Si solo busca `rec.texto`, los 26 informes con `contenido` muestran JSON crudo.

## Scripts del pipeline

| Script | Función |
|--------|---------|
| `scripts/parse_all.py` | Pipeline completo: PDF → JSON individuales |
| `scripts/parse_reports_v2.py` | Parser v2 de informes CIAF |
| `scripts/parse_year_v2.py` | Parser por año con batch processing |
| `scripts/generate_index.py` | Genera index.json desde reports/ |
| `scripts/sync.py` | Sincronización de datos |
| `scripts/test_parser.py` | Tests del parser |

Scripts archivados en `scripts/archive/` (ya no se ejecutan):
- `cruce_datos.py`, `fix_visor_complete.py`, `fix_visor_data.py`, `geocode_all.py`, `geocode_visor.py`, `build-station-map.py`
