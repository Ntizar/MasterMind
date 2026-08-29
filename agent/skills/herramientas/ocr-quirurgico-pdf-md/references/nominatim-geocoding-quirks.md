# Nominatim Geocoding — Quirks y Patrones

## User-Agent Restriction

Nominatim requiere un User-Agent válido. **Paréntesis en el UA causan 403 Forbidden.**

```python
# ❌ RECHAZADO (403)
ua = "CIAF-Visor/1.0 (proyecto educativo; contacto: ciaf@example.com)"

# ✅ FUNCIONA
ua = "CIAF-Visor/1.0"
```

## Rate Limits

- **Límite oficial:** 1 petición por segundo
- **En la práctica:** ~429 tras 20-30 peticiones con 1.1s de delay
- **Tras 429:** El IP queda bloqueado temporalmente (~5-15 minutos)

### Retry Strategy

```python
def geocode_with_retry(query, max_retries=3):
    for attempt in range(max_retries):
        resp = urllib.request.urlopen(req)
        if resp.status == 200:
            return json.loads(resp.read())
        if resp.status == 429:
            wait = 2 ** (attempt + 2)  # 4s, 8s, 16s
            time.sleep(wait)
    return None
```

## Local Lookup Pattern (Preferred)

Para datasets con cientos de ubicaciones, **construir un JSON local** es mejor que llamadas API:

1. Extraer estaciones únicas del dataset
2. Buscar coordenadas manualmente o con script batch
3. Guardar como `station-coords.json`
4. En el parser, buscar localmente antes de Nominatim

```python
STATION_COORDS = json.load(open("data/station-coords.json"))

def _lookup_local(name, province=""):
    clean = _normalize(name)  # uppercase, sin tildes
    for key, coords in STATION_COORDS.items():
        if clean in key or key in clean:
            return coords["lat"], coords["lng"]
    return None, None
```

**Ventaja:** 0延迟, offline, 100% success rate para estaciones conocidas.

## Query Optimization

```python
# Buscar con límite y priorizar resultados ferroviarios
queries = [
    f"{station} España",
    f"estación {station} España",
    f"{station} {province} España",
]
for q in queries:
    url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=5&countrycodes=es"
    # Priorizar resultados que contengan "railway" o "station"
```
