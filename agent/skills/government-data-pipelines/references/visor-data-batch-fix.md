# Visor Data Batch Fix — Corrección masiva de datos de visor

Cuando un visor ya tiene datos cargados pero con errores sistemáticos (severidad incorrecta, nombres sucios, sin geolocalización), aplicar corrección batch sobre los archivos de datos del visor (`YYYY.json`), no sobre los JSONs individuales del pipeline.

---

## 1. Severidad: mapeo de vocabulario legacy → RD 929/2022

El visor original usa "fatal"/"leve"/"grave" pero la taxonomía oficial (RD 929/2022) es "muy grave"/"grave"/"menor".

```python
GRAVEDAD_MAP = {
    "fatal": "muy grave",    # fallecidos > 0
    "leve": "menor",         # sin víctimas graves
    "grave": "grave",        # heridos graves
    # Siempre recalcular desde datos numéricos cuando sea posible
}

# Precisión: si hay Excel con víctimas, calcular desde ahí
def compute_severity_from_excel(row):
    muertos = row.get('muertos', 0) or 0
    hg = row.get('heridos_graves', 0) or 0
    if muertos > 0: return "muy grave"
    elif hg > 0: return "grave"
    else: return "menor"
```

**Regla:** SIEMPRE recalcular desde datos numéricos (víctimas) cuando haya fuente. El map es fallback.

---

## 2. Tipología: enriquecer con detalle del pipeline

El visor original tiene solo "accidente"/"incidente"/"avería". El pipeline genera categorías detalladas.

```python
# Si el visor tiene tipo_suceso del pipeline, añadir tipo_suceso_normalizado
if tipo_suceso:
    tipo_lower = tipo_suceso.lower().strip()
    if tipo_lower in TIPO_MAP:
        cat, detalle = TIPO_MAP[tipo_lower]
        r['tipo'] = cat
        r['tipo_suceso'] = tipo_suceso
        r['tipo_suceso_normalizado'] = detalle
```

---

## 3. Estaciones: limpieza masiva

Ver `references/station-name-cleanup.md` para patrones de limpieza de estaciones contaminadas. Aquí el patrón batch:

```python
# Procesar cada archivo YYYY.json
for yf in sorted(os.listdir(REPORT_DIR)):
    if not yf.endswith('.json'): continue
    with open(os.path.join(REPORT_DIR, yf)) as f:
        records = json.load(f)
    
    for r in records:
        loc = r.get('ubicacion', {})
        est = loc.get('estacion', '')
        if est:
            loc['estacion'] = clean_station_name(est)  # Ver station-name-cleanup.md
    
    with open(os.path.join(REPORT_DIR, yf), 'w') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
```

---

## 4. Geolocalización batch

Cuando el visor tiene ~84% geolocalizado y el resto falta:

```python
# 1. DB local de estaciones (station-coords.json) — fuente primaria
# 2. Nominatim como fallback (rate limit: 1 req/seg)
# 3. Fix manual para los 4-5 últimos

for r in records:
    loc = r.get('ubicacion', {})
    if loc.get('lat') and loc.get('lng'):
        continue  # ya tiene coords
    
    station = loc.get('estacion', '')
    lat, lng = lookup_station_db(station, station_db)
    if not lat:
        lat, lng = geocode_nominatim(station, loc.get('provincia', ''))
        time.sleep(1.1)
    
    if lat and lng:
        loc['lat'] = lat
        loc['lng'] = lng
```

---

## 5. Enriquecimiento desde JSONs individuales

El visor puede enriquecerse con datos de los JSONs individuales del pipeline (generados por LLM):

```python
# Indexar individual JSONs por expediente
individual_index = {}
for f in os.listdir(INDIVIDUAL_DIR):
    with open(os.path.join(INDIVIDUAL_DIR, f)) as fh:
        d = json.load(fh)
    exp = d.get('_cross_ref', {}).get('excel_exp')
    if exp:
        individual_index[exp] = d

# Enriquecer visor
for r in records:
    exp = r.get('expediente', '')
    ind = individual_index.get(exp, {})
    if ind:
        # Añadir campos detallados que el visor no tiene
        if ind.get('tipo_suceso'):
            r['tipo_suceso'] = ind['tipo_suceso']
        if ind.get('tipo_suceso_normalizado'):
            r['tipo_suceso_normalizado'] = ind['tipo_suceso_normalizado']
        if ind.get('causa_directa'):
            r['causa_directa'] = ind['causa_directa']
```

---

## Pitfalls

- **NO confundir archivos:** El visor lee de `data/reports/YYYY.json`, NO de `ciaf-data/data/individual/*.json`. Son dos conjuntos de datos distintos.
- **Sync bidireccional:** Si se corrigen los individual JSONs, hay que propagar los cambios al visor también. No asumir que están sincronizados.
- **index.json del visor:** También contiene gravedad. Actualizar ahí también, no solo en los YYYY.json.
- **Backup antes de batch fix:** Siempre hacer `cp -r data/reports data/reports_backup_YYYYMMDD` antes de ejecutar.
- **🔴 Excel tiene provincias equivocadas (VERIFICADO 2026-06-29):** El Excel de origen tiene provincias incorrectas para ~25% de los registros. La fuente fiable es el resumen del informe PDF. SIEMPRE cruzar provincia desde el resumen cuando esté disponible. Patrón: `extract_province_from_resumen()` → sobrescribir provincia del Excel. Ver `references/excel-json-cross-reference.md` sección 8.
- **🔴 Nominatim bloquea IP tras ~50 requests (VERIFICADO 2026-06-29):** Tras ~50 requests en pouco tempo, Nominatim devuelve 429 y bloquea la IP durante horas. **Solución:** (1) station-coords.json como fuente primaria (355+ entradas), (2) Nominatim SOLO como fallback con `time.sleep(1.1)`, (3) coordenadas hardcodeadas para los últimos 5-10 que fallan todo. NUNCA hacer batch geocoding con Nominatim como fuente principal.
- **🔴 geocode() devuelve None si la estación no está en la DB (VERIFICADO 2026-06-29):** Si `geocode()` falla, el fix NO se aplica silenciosamente. SIEMPRE verificar que `geocode()` devolvió coords antes de marcar como "fixed". Patrón: `if lat and lng: loc['lat'] = lat; changed = True` — sin el check, el script dice "Fixed: 0" sin explicación.
