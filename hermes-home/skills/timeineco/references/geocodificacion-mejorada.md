# Geocodificación Mejorada — Nominatim + Overpass

**Añadido:** 2026-06-22, TimeIneco2 (`Ntizar/TimeIneco2`)

## Arquitectura

```
utils.js
├── geocode(query)           → Nominatim search + cache local + rate limit
├── geocodeAddress(query)    → Alias público preferido de geocode()
├── autocomplete(partial)    → Sugerencias parciales (mín 3 chars)
├── reverseGeocode(lat,lng)  → Nominatim reverse + barrio/CP/calle
├── extractAddressInfo(res)  → Parsea dirección estructurada
├── clearGeocodeCache()      → Limpia localStorage para debugging
├── respectRateLimit()       → Debounce 1.1s entre requests
├── fetchWithRetry()         → Backoff exponencial (2 reintentos)
├── _cacheGet/_cacheSet()    → localStorage TTL 24h, máx 500 entradas
├── overpassReverseGeocode() → Fallback Overpass si Nominatim falla
└── overpassGeocodeFallback()→ Fallback Overpass para búsqueda directa
```

## Nominatim API

### Search (geocodificación directa)
```
GET https://nominatim.openstreetmap.org/search
  ?q={query}&format=json&limit=5&accept-language=es
  &addressdetails=1&namedetails=1&countrycodes=es
```

### Reverse geocoding
```
GET https://nominatim.openstreetmap.org/reverse
  ?lat={lat}&lon={lon}&format=json&accept-language=es
  &addressdetails=1&zoom=18
```

### Rate Limits
- **Máximo 1 request/segundo** (obligatorio)
- **User-Agent requerido** (403 sin él)
- **Formato:** `Producto/versión (contacto)`
- **En TimeIneco:** `TimeIneco/1.0 (timeineco@antizar.es)`

### Errores
- `404` → Dirección no encontrada (no reintentar)
- `429` → Rate limit (reintentar con backoff exponencial)
- `5xx` → Error servidor (reintentar con backoff exponencial)

## Overpass API (Fallback)

### Reverse geocoding
```
POST https://overpass-api.de/api/interpreter
  data=[timeout:5];(node["addr:street"]["addr:housenumber"](bbox);
    way["addr:street"]["addr:housenumber"](bbox);
    node["name"](bbox);relation["name"](bbox));out body qt 5;>;out skel qt;
```

### Direct geocoding
```
POST https://overpass-api.de/api/interpreter
  data=[timeout:10];(node["name"~query,case="ignore"];
    way["name"~query,case="ignore"];
    node["addr:street"~query,case="ignore"]);out center 10;
```

## Cache Local

- **Clave:** `ti_geocode_{type}_{base64hash}`
- **TTL:** 24 horas
- **Máximo:** 500 entradas (elimina las 10% más antiguas al exceder)
- **Formato:** `{ts: timestamp, data: result}`
- **Silencioso:** localStorage lleno → catch y continuar

## Dirección Estructurada (Reverse)

Campos priorizados por `addressdetails`:
1. `road` + `house_number` → calle y número
2. `neighbourhood` → barrio/vecindario
3. `suburb` → subbarrio/zona
4. `quarter` → barrio administrativo
5. `borough` → distrito municipal
6. `city`/`town`/`village` → localidad
7. `postcode` → código postal
8. `state` → provincia/estado

## Pitfalls

- **Nominatim rechaza sin User-Agent** → siempre enviar `TimeIneco/1.0 (timeineco@antizar.es)`
- **Rate limit 1 req/s** → usar debounce interno de 1.1s, no solo el frontend
- **`addressdetails=1`** es obligatorio para obtener barrio, CP y calle en reverse
- **`zoom=18`** en reverse para máxima resolución (barrio y calle)
- **Overpass API puede ser lento** → timeout 5-10s, fallback silencioso
- **localStorage puede estar lleno** → catch y continuar, no bloquear la app
- **`countrycodes=es`** en search para priorizar resultados españoles