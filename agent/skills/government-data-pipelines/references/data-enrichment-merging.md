# Enriquecimiento y Fusión de Datasets — Patrón de dos fuentes JSON

## Escenario clásico

Tienes **dos fuentes de datos** para el mismo conjunto de registros, pero con esquemas diferentes y niveles de detalle distintos. Ejemplo real:

- **Fuente A** (`ciaf-data/data/individual/*.json`): 270 informes con datos ricos extraídos por LLM (víctimas detalladas: fallecidos/graves/leves/heridos, hora, PK, tramo, trenes array, resumen verificado)
- **Fuente B** (`CIAF-visor/data/reports/2007-2025.json`): 269 informes con esquema más simple del visor (campo `resumen`, `conclusiones`, `recomendaciones`)

**Objetivo:** Enriquecer Fuente B con los campos detallados de Fuente A sin sobrescribir lo que ya está bien.

## Paso 1: Identificar la clave de emparejamiento

La clave más fiable es el **número de expediente** (ej: `0062/2007`, `46/2022`). Extraerlo de ambos conjuntos:

```python
import re, json

def extract_expedition(json_data, filename):
    """Extraer número de expediente del título o campo directo."""
    # 1. Campo directo
    exp = json_data.get('expediente', '')
    if exp and re.match(r'\d+/\d{4}', exp):
        return exp
    
    # 2. Del título: "Nº 62/2007" o "IF 62/2007" o "expediente nº 62/2007"
    titulo = json_data.get('titulo', json_data.get('title', ''))
    m = re.search(r'N[º°]?\s*(\d{3,4}/\d{4})', titulo)
    if m:
        return m.group(1)
    m = re.search(r'IF\s+(\d+/\d{4})', titulo)
    if m:
        return m.group(1)
    m = re.search(r'expediente\s+n[º°]?\s*(\d+/\d{4})', titulo, re.IGNORECASE)
    if m:
        return m.group(1)
    
    # 3. Del nombre de archivo
    numbers = re.findall(r'(\d{3,4})', filename)
    # Cruzar con año para formar expediente
    year = json_data.get('año', json_data.get('year', 0))
    for n in numbers:
        if int(n) < 500 and year:  # expedientes suelen ser <500
            return f"{n}/{year}"
    
    return None

# Construir índices por expediente
def build_expindex(jsons_dir):
    """Indexar JSONs por número de expediente."""
    index = {}
    for f in os.listdir(jsons_dir):
        if not f.endswith('.json'):
            continue
        with open(os.path.join(jsons_dir, f)) as fh:
            data = json.load(fh)
        exp = extract_expedition(data, f)
        if exp:
            index[exp] = {'file': f, 'data': data}
    return index
```

## Paso 2: Emparejar registros

```python
def match_records(source_a_index, source_b_records):
    """
    source_a_index: dict por expediente → {file, data} (fuente rica)
    source_b_records: list de registros del visor (fuente base)
    
    Retorna: dict con matches y stats
    """
    matched = []
    unmatched_b = []
    
    for record in source_b_records:
        exp_b = record.get('expediente', '')
        if exp_b in source_a_index:
            matched.append({
                'visor_record': record,
                'rich_data': source_a_index[exp_b]['data'],
                'expediente': exp_b
            })
        else:
            unmatched_b.append(record)
    
    return {
        'matched': matched,
        'unmatched': unmatched_b,
        'stats': {
            'total_vis': len(source_b_records),
            'total_rich': len(source_a_index),
            'matched': len(matched),
            'unmatched': len(unmatched_b)
        }
    }
```

## Paso 3: Fusión selectiva (NUNCA sobrescribir completo)

```python
def enrich_record(visor_record, rich_data):
    """
    Enriquecer un registro del visor con datos ricos.
    REGLA: solo mejorar campos débiles, nunca sobrescribir campos completos.
    """
    enriched = visor_record.copy()
    
    # Víctimas detalladas — solo si el visor NO las tiene
    if not enriched.get('victimas_fallecidos') and rich_data.get('victimas_fallecidos'):
        enriched['victimas_fallecidos'] = rich_data['victimas_fallecidos']
        enriched['victimas_graves'] = rich_data.get('victimas_graves', 0)
        enriched['victimas_leves'] = rich_data.get('victimas_leves', 0)
        enriched['victimas_heridos'] = rich_data.get('victimas_heridos', 0)
    
    # Hora — solo si vacía
    if not enriched.get('hora') and rich_data.get('hora'):
        enriched['hora'] = rich_data['hora']
    
    # PK y tramo — solo si vacíos
    if not enriched.get('pk') and rich_data.get('pk'):
        enriched['pk'] = rich_data['pk']
    if not enriched.get('tramo') and rich_data.get('tramo'):
        enriched['tramo'] = rich_data['tramo']
    
    # Trenes array — solo si el visor no tiene datos de trenes
    if not enriched.get('trenes') and rich_data.get('trenes'):
        enriched['trenes'] = rich_data['trenes']
    
    # Resumen verificado — usar si el del visor es genérico
    visor_len = len(enriched.get('resumen', ''))
    rich_len = len(rich_data.get('resumen_verificado', rich_data.get('resumen', '')))
    if rich_len > visor_len * 1.5:  # el rico es 50% más largo → mejor
        enriched['resumen_verificado'] = rich_data.get('resumen_verificado', rich_data.get('resumen', ''))
    
    # NO tocar: conclusiones, recomendaciones, coordenadas si ya existen
    # NO sobrescribir campos del visor que ya están bien
    
    return enriched
```

## Paso 4: Geocodificación en batch con DB local

```python
def batch_geocode(records, station_coords_path):
    """
    Geolocalizar registros usando DB local de estaciones.
    station_coords.json: dict de {nombre_normalizado: {lat, lng, ...}}
    """
    with open(station_coords_path) as f:
        station_db = json.load(f)
    
    def normalize_name(name):
        """Normalizar nombre para matching."""
        return re.sub(r'[^a-záéíóúñ]', '', name.lower().strip())
    
    geolocated = 0
    for record in records:
        if record.get('lat') and record.get('lng'):
            continue  # ya tiene coordenadas
        
        station = record.get('ubicacion', {}).get('estacion', '') or record.get('city', '')
        if not station:
            continue
        
        norm = normalize_name(station)
        if norm in station_db:
            coords = station_db[norm]
            record['lat'] = coords['lat']
            record['lng'] = coords['lng']
            geolocated += 1
        else:
            # Fallback: Nominatim con delay
            coords = geocode_station_nominatim(station, record.get('provincia', ''))
            if coords:
                record['lat'] = coords[0]
                record['lng'] = coords[1]
                geolocated += 1
            time.sleep(1.1)  # rate limit Nominatim
    
    return geolocated
```

## Paso 5: Guardar y verificar

```python
def save_enriched(enriched_records, output_path):
    """Guardar registros enriquecidos por año."""
    by_year = {}
    for r in enriched_records:
        year = r.get('year', r.get('año', 0))
        by_year.setdefault(year, []).append(r)
    
    for year, records in by_year.items():
        with open(os.path.join(output_path, f'{year}.json'), 'w') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    
    # Stats
    total = len(enriched_records)
    with_victims = sum(1 for r in enriched_records if r.get('victimas_fallecidos', 0) > 0)
    with_coords = sum(1 for r in enriched_records if r.get('lat') and r.get('lng'))
    
    print(f"Guardados: {total} registros")
    print(f"Con víctimas detalladas: {with_victims}")
    print(f"Geolocalizados: {with_coords}")
```

## Resultados típicos (CIAF)

| Métrica | Antes | Después | Delta |
|---------|-------|---------|-------|
| Registros con víctimas detalladas | 31 (11%) | 269 (100%) | +238 |
| Registros con hora exacta | 45 (17%) | 230 (85%) | +185 |
| Registros con PK | 12 (4%) | 95 (35%) | +83 |
| Registros geolocalizados | 194 (72%) | 225 (84%) | +31 |

## Pitfalls

- **Matching por título es frágil:** Los títulos pueden tener formato diferente entre fuentes ("Nº 62/2007" vs "Informe 62/2007"). Usar expediente normalizado (solo dígitos + `/` + año).
- **Nunca sobrescribir campos completos:** Si el visor ya tiene `conclusiones` con 500 palabras, no reemplazarlas con un resumen de 100 palabras de la fuente rica.
- **6 JSONs de 2009 tienen `pdf_path` incorrecto:** Todos apuntan al mismo PDF (`0056CIAF.pdf`). Solución: emparejar por número de informe en el título, no por `pdf_path`.
- **1 registro puede estar en una fuente pero no en la otra:** Siempre verificar que el conteo final sea consistente. En CIAF: 270 en ciaf-data, 269 en visor (1 missing: `IF-230114-270115-CIAF` de Fuentebureba 2014).
- **Estaciones ambiguas para geocoding:** "Cortes" puede ser de Navarra o de La Muela. Usar contexto (provincia, PK, tramo) para desambiguar. 9 registros quedan sin geolocalizar cuando el nombre es ambiguo y no hay más contexto.
