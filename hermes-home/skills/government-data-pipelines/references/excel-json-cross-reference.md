# Cruce Excel ↔ JSONs — Patrón completo

Cruzar una fuente estructurada (Excel) con una colección de JSONs generados por LLM/OCR. Aplicable a CIAF, informes gubernamentales, datasets híbridos.

---

## 1. Matching por expediente/número

El problema principal: los JSONs tienen nombres caóticos (`IF100108300908CIAF.json`, `2022-48-0612-if.json`, `46-220601-if-sn_ciafv2.json`) mientras el Excel usa formato uniforme (`0001/2008`).

### Estrategia de extracción (orden de prioridad)

```python
def extract_exp_from_json(data, filename):
    """Extraer expediente de múltiples fuentes."""
    titulo = data.get('titulo', data.get('title', ''))
    jid = data.get('id', '')
    year = data.get('año', '')
    
    # 1. Título: "Nº 34/2012", "IF 34/2012", "expediente nº 34/2012"
    for pat in [r'N[º°]?\s*(\d{1,4})/(\d{4})', r'IF\s+(\d{1,4})/(\d{4})',
                r'expediente\s+n[º°]?\s*(\d{1,4})/(\d{4})', r'IFC\s+(\d{1,4})/(\d{4})']:
        m = re.search(pat, titulo, re.IGNORECASE)
        if m: return f"{int(m.group(1))}/{m.group(2)}"
    
    # 2. ID: "IF-48-2022", "CIAF IF 11-2023", "IFC 12-2019"
    for pat in [r'IFC\s+(\d{1,4})-(\d{4})', r'IF\s+(\d{1,4})-(\d{4})', r'(\d{1,4})-(\d{4})']:
        m = re.search(pat, jid, re.IGNORECASE)
        if m: return f"{int(m.group(1))}/{m.group(2)}"
    
    # 3. Nombre de archivo (fallback frágil)
    numbers = re.findall(r'(\d{1,4})', filename.replace('.json', '').replace('CIAF', ''))
    for n in numbers:
        if int(n) < 500 and year:
            return f"{int(n)}/{year}"
    
    return None
```

### Normalización de expediente
```python
def normalize_exp(exp_str):
    """'0001/2008' → '1/2008'"""
    m = re.match(r'^0*(\d+)/(\d{4})$', str(exp_str).strip())
    return f"{m.group(1)}/{m.group(2)}" if m else exp_str
```

### Pitfalls
- **IDs como "IFC 12-2019"**: el prefijo IFC/IF/CIAF varía. Buscar con múltiples patrones.
- **Nombres como "IF180412261212CIAF"**: no tienen separadores claros. Extraer del título, no del nombre.
- **Expedientes >500**: raros pero existen (111/2024). No filtrar por umbral bajo.

---

## 2. Normalización de severidad (RD 929/2022)

```python
def compute_severity(muertos, heridos_graves):
    """Taxonomía ferroviaria española."""
    if muertos > 0: return "muy grave"
    elif heridos_graves > 0: return "grave"
    else: return "menor"
```

**Regla:** Siempre calcular desde datos numéricos (víctimas), nunca desde texto descriptivo.

---

## 3. Normalización de tipología

Mapeo de categorías granulares del Excel → categorías estándar:

```python
# Ejemplo: 58 categorías Excel → ~25 normalizadas
TIPO_MAP = {
    "descarrilamiento": "accidente",
    "colisión frontal de trenes": "accidente",
    "arrollamiento de persona": "accidente",
    "conato de colisión": "incidente",
    "rebase de señal": "incidente",
    "fallo de señalización": "incidente",
    # ... mappings completos en cruce_datos.py
}
```

Cada categoría granular también se guarda como `tipo_suceso_normalizado` para filtros detallados.

---

## 4. Geocodificación por PK + línea (ADIF LTV)

### Fuente de datos
**FeatureServer ArcGIS LTV:** `https://services7.arcgis.com/XTupIrLX53AjaJqO/arcgis/rest/services/LTV_2/FeatureServer/0/query`

- ~1.162 puntos con PK + coordenadas
- 119 líneas con cobertura
- Datos dinámicos (ADIF actualiza)

### Query correcta
```
where=1=1
outFields=CODLINEA,DESCLINEA,PKINI,PKFIN
outSR=4326
returnGeometry=true  ← OBLIGATORIO
f=geojson
resultRecordCount=2000
```

### ⚠️ Pitfall crítico: coordinates
Las propiedades `X` e `Y` son NULL con `outSR=4326`. Usar SIEMPRE `geometry.coordinates`.

### Interpolación PK
```python
def geocode_pk(ltv_by_line, line_code, pk_value):
    """Encontrar coordenadas para un PK dado."""
    points = ltv_by_line[line_code]['points']  # sorted by pk_ini
    for pt in points:
        if pt['pk_ini'] <= pk_value <= pt['pk_fin']:
            return pt['lat'], pt['lng']
    # Fallback: punto más cercano si <50km
    return nearest_point(points, pk_value, max_dist_km=50)
```

### Cobertura típica
- 49/61 líneas CIAF tienen cobertura LTV → ~71% geocodificación
- Líneas sin cobertura: regionales cortas (Cercanías, FEVE, ramales)

### Formato PK
Normalizar a `NNN+NNN`:
- `"P.K. 429,825"` → `"429+825"`
- `"415+648"` → `"415+648"` (ya correcto)
- `"P.K. 62+902"` → `"62+902"`

---

## 5. Enriquecimiento selectivo (NO sobrescribir)

```python
# Regla: solo mejorar campos débiles, nunca sobrescribir completos
if excel_causa and not json_data.get('causa_directa'):
    json_data['causa_directa'] = excel_causa

# Array de recomendaciones del Excel (múltiples filas por expediente)
json_data['recomendaciones_excel'] = [
    {'texto': row['recomendacion_texto'], 'destinatario': row['recomendacion_destinatario']}
    for row in excel_rows[exp] if row.get('recomendacion_texto')
]

# Metadatos de cruce (para trazabilidad)
json_data['_cross_ref'] = {
    'excel_exp': exp,
    'corrected_at': datetime.now().isoformat(),
    'changes': changes_list
}
```

---

## 6. Resultados típicos (CIAF, 270 informes)

| Métrica | Antes | Después |
|---------|-------|---------|
| Severidad correcta | 65% | 99% |
| Tipología detallada | 0% | 99% |
| PK normalizado | 23% | 99% |
| Geolocalizados | 3% | 100% |
| Causa directa | 0% | 99% |
| Provincia correcta | ~60% | 100% |

---

## 8. Provincia desde resumen (CRÍTICO — VERIFICADO 2026-06-29)

**El Excel tiene provincias equivocadas para ~25% de los registros.** La fuente fiable es el resumen del informe PDF, que menciona la provincia entre paréntesis justo después del nombre de la estación.

### Patrón de extracción
```python
PROVINCES = {
    'a coruña', 'álava', 'albacete', 'alicante', 'almería', 'asturias', 'ávila',
    'badajoz', 'barcelona', 'bizkaia', 'burgos', 'cáceres', 'cádiz', 'cantabria',
    'castellón', 'ciudad real', 'córdoba', 'cuenca', 'gipuzkoa', 'guipúzcoa', 'girona',
    'granada', 'guadalajara', 'huelva', 'huesca', 'islas baleares', 'jaén',
    'león', 'lleida', 'lugo', 'madrid', 'málaga', 'murcia', 'navarra',
    'orense', 'ourense', 'palencia', 'pontevedra', 'la rioja', 'salamanca',
    'soria', 'tarragona', 'teruel', 'toledo', 'valencia', 'valladolid',
    'vizcaya', 'zamora', 'zaragoza',
}

def extract_province_from_resumen(text):
    """Extraer provincia del resumen del informe — más fiable que el Excel."""
    if not text:
        return None
    # Patrón: "estación de X (Provincia)" o "apeadero de X (Provincia)"
    m = re.search(
        r'(?:estaci[oó]n|apeadero)\s+de\s+[^\s,(]+(?:\s+(?:de|del|la|el|los|las|a|en|y|al)\s+[^\s,(]+)*?'
        r'\s*\(([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[a-záéíóúñ]+)*)\)',
        text, re.IGNORECASE
    )
    if m:
        prov = m.group(1).strip()
        if prov.lower() in PROVINCES:
            return prov
    return None
```

### Ejemplo de error corregido
- Excel dice: 0002/2009 → "Asturias"
- Resumen dice: "...estación de Vila-real (Castellón)..."
- **Corrección:** Castellón (no Asturias)

### Regla
Cuando el Excel y el resumen discrepen en provincia, **SIEMPRE confiar en el resumen**. El Excel puede tener la provincia de la sede CIAF (Madrid) o de otro registro cercano.

### Extensión: extraer estación completa del resumen
Cuando el nombre de estación está vacío o truncado ("La", "San", "Sant"), extraer del resumen:
```python
def extract_station_from_resumen(text):
    patterns = [
        r'estaci[oó]n\s+de\s+([^\s,(]+(?:\s+(?:de|del|la|el|los|las|a|en|y|al)\s+[^\s,(]+)*?)(?:\s*\(|\s*,|\s+donde)',
        r'apeadero\s+de\s+([^\s,(]+(?:\s+(?:de|del|la|el|los|las|a|en|y|al)\s+[^\s,(]+)*?)(?:\s*\(|\s*,|\s+donde)',
        r'paso a nivel\s+(?:de\s+)?(?:la\s+)?estaci[oó]n\s+de\s+([^\s,(]+(?:\s+(?:de|del|la|el|los|las|a|en|y|al)\s+[^\s,(]+)*?)(?:\s*\(|\s*,)',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            station = m.group(1).strip()
            if len(station) >= 3:
                return station
    return None
```

---

## 7. Script completo

Ver `scripts/cruce_datos.py` en `CIAF-visor/scripts/` para implementación completa con:
- Carga Excel (openpyxl, read_only=True)
- Matching por expediente normalizado
- Corrección severidad/tipología/PK
- Enriquecimiento de campos
- Generación de informe markdown
