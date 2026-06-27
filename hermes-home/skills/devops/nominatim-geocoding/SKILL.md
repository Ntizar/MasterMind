---
name: nominatim-geocoding
version: "1.0.0"
description: "Geocodificación de direcciones/estaciones usando Nominatim (OpenStreetMap) con manejo correcto de rate limits, User-Agent, y filtrado de resultados. Patrón para batch de geocoding sin bloqueo."
tags: [geocoding, nominatim, openstreetmap, batch, rate-limit, stations]
---

# Nominatim Geocoding — Guía Práctica

## Cuándo usarlo

- Necesitas convertir nombres de lugares (estaciones, calles, ciudades) a coordenadas lat/lng
- Tienes un batch grande (100+ ubicaciones) y no puedes hacer todas las requests de golpe
- Estás trabajando en un proyecto que necesita geocoding sin APIs de pago

## No es para

- Geocoding en tiempo real de una sola dirección (usa fetch directo)
- APIs que ya tienen geocoding integrado (Google Maps, Mapbox)

## Pitfalls críticos

### 🔴 User-Agent: NUNCA con paréntesis
Nominatim rechaza User-Agents que contengan paréntesis `()` con **403 Forbidden**.

❌ `USER_AGENT = "MiApp/1.0 (contacto@email.com)"` → 403 Forbidden
✅ `USER_AGENT = "MiApp/1.0"` → funciona

### 🔴 Rate limiting: máximo 1 request/segundo
Nominatim aplica rate limiting estricto. Si envías más de 1 request/segundo, recibirás **429 Too Many Requests** y tu IP será bloqueada temporalmente (5-60 minutos).

**Solución para batch grande:**
1. **Delay de 1.1-2.1 segundos** entre cada request (NO menos)
2. **Exponential backoff** en 429: esperar 30s, 60s, 120s...
3. **Cache en memoria** para no repetir queries idénticas
4. **Dos pasos:** Primero parsear todo sin geocoding, luego geocodificar las ubicaciones únicas

### 🔴 `limit=1` devuelve barrios, no estaciones
Cuando buscas "Madrid Chamartín", `limit=1` devuelve el **barrio** (boundary administrativo), no la estación de tren. Necesitas `limit=5` y filtrar por tipo de resultado.

```python
# ❌ Solo devuelve el barrio
params = {'q': 'Madrid Chamartín España', 'format': 'json', 'limit': '1'}

# ✅ Devuelve estaciones y barrios, filtramos
params = {'q': 'Madrid Chamartín España', 'format': 'json', 'limit': '5'}
# Luego filtrar por: d.get('type') == 'train_station' o d.get('class') == 'railway'
```

### 🔴 Queries específicas para estaciones de tren
Las queries genéricas ("Chamartin Madrid") pueden no encontrar la estación específica. Patrón que funciona:

```python
queries = [
    f"{station_name} España",           # Primero intento general
    f"{station_name} {province} España", # Con provincia
    station_name,                         # Sin acentos/adicionales
]
```

## Patrón de batch con retry

```python
import urllib.request, urllib.parse, json, time, re

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "MiApp/1.0"
_cache = {}

def geocode(station_name: str, province: str = "") -> tuple[float|None, float|None]:
    """Geocodifica una estación con retry y cache."""
    key = f"{station_name.lower().strip()}|{province.lower().strip()}"
    if key in _cache:
        return _cache[key]
    
    clean = re.sub(r'\s+', ' ', station_name.strip())
    queries = [f"{clean} España"]
    if province:
        queries.append(f"{clean} {province} España")
    
    for query in queries:
        for attempt in range(3):
            params = urllib.parse.urlencode({
                'q': query, 'format': 'json', 'limit': '5', 'countrycodes': 'es'
            })
            url = f"{NOMINATIM_URL}?{params}"
            req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
            
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode())
                if data:
                    # Priorizar estaciones de tren
                    for d in data:
                        if d.get('type') in ('train_station', 'tram_stop'):
                            _cache[key] = (float(d['lat']), float(d['lon']))
                            return _cache[key]
                    # Fallback: primer resultado
                    _cache[key] = (float(data[0]['lat']), float(data[0]['lon']))
                    return _cache[key]
                break  # Sin resultados, probar siguiente query
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    wait = 30 * (attempt + 1)
                    print(f"429 → esperando {wait}s...")
                    time.sleep(wait)
                    continue
                break
            except Exception:
                break
        time.sleep(1.1)  # Delay entre queries
    
    _cache[key] = (None, None)
    return (None, None)
```

## Estrategia de dos pasos (RECOMENDADA)

Para 100+ ubicaciones:

```bash
# Paso 1: Parsear documentos (sin geocoding) — rápido
python3 parse_all.py --no-geocode

# Paso 2: Geocodificar ubicaciones únicas — lento pero seguro
python3 geocode_all.py  # Con delays de 2s + exponential backoff
```

El Paso 2 deduplica ubicaciones automáticamente (muchos documentos comparten la misma estación), reduciendo las llamadas a Nominatim.

## Geocoding con mapa hardcodeado (alternativa sin API) — VERIFICADO 2026-06-26

Si Nominatim está bloqueado o no disponible, **usar `station-coords.json` como fuente primaria**:

1. Extraer todas las ubicaciones únicas del paso 1
2. Crear un JSON manual con las coordenadas conocidas (`data/station-coords.json`)
3. Lookup local primero, Nominatim como fallback

```python
STATION_COORDS = json.loads(open('data/station-coords.json').read())

def geocode_with_local(station_name, province=""):
    # 1. Lookup local (instantáneo, sin API)
    lat, lng = lookup_local(station_name, province)
    if lat: return lat, lng
    # 2. Nominatim fallback (solo si no encontrado localmente)
    return geocode_nominatim(station_name, province)
```

**Patrón de matching flexible:**
```python
def lookup_local(station, province=""):
    norm = normalize(station)  # uppercase, sin tildes
    # Exact match
    if station in STATION_COORDS:
        return STATION_COORDS[station]['lat'], STATION_COORDS[station]['lng']
    # Normalized match
    for name, coords in STATION_COORDS.items():
        if normalize(name) == norm:
            return coords['lat'], coords['lng']
    # Partial match (first 2 significant words)
    words = [w for w in norm.split() if len(w) > 2][:2]
    key = ' '.join(words)
    for name, coords in STATION_COORDS.items():
        if key in normalize(name):
            return coords['lat'], coords['lng']
    return None, None
```

**Ventaja:** 328 estaciones con coords = 71% de los 277 informes geolocalizados sin tocar Nominatim.

Para estaciones de tren españolas, consultar:
- https://www.renfe.com/es/es/informacion-util/horarios/estaciones
- Coordenadas de estaciones principales en Wikipedia
- Overpass API: `[out:json];node["railway"="station"]["network"~"RENFE|ADIF"](area:España);`

## Verificación

```bash
# Test rápido de Nominatim
python3 -c "
import urllib.request, json
url = 'https://nominatim.openstreetmap.org/search?q=Madrid+Chamartin&format=json&limit=1&countrycodes=es'
req = urllib.request.Request(url, headers={'User-Agent': 'Test/1.0'})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())
    print(f'OK: {data[0][\"lat\"]}, {data[0][\"lon\"]}')
except Exception as e:
    print(f'Error: {e}')
"
```

## Referencias

- Nominatim Usage Policy: https://operations.osmfoundation.org/policies/nominatim/
- `ocr-quirurgico-pdf-md` — Pipeline de extracción que puede usar este geocoding
- `github-workflow` — Deploy de proyectos con geocoding en Pages

## Atribución

**Autor:** David Antizar (Ntizar)
**Agente:** Mastermind (ejecutor, no autor)
**Repo:** `github.com/Ntizar/Mastermind`
