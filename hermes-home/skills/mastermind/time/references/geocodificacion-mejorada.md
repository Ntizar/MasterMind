# Geocodificación — Nominatim + Overpass Fallback

## Nominatim
- Search: `GET /search?q={query}&format=json&limit=5&accept-language=es&addressdetails=1&countrycodes=es`
- Reverse: `GET /reverse?lat={lat}&lon={lon}&format=json&addressdetails=1&zoom=18`
- Rate limit: 1 req/s, User-Agent obligatorio
- Time User-Agent: `Time/2.0 (time@antizar.es)`

## Cache Local
- Clave: `ti_geocode_{type}_{hash}`, TTL 24h, máx 500 entradas
- localStorage lleno → catch silencioso

## Overpass Fallback
- Reverse: POST con bbox query por addr:street + addr:housenumber
- Direct: POST con regex name~query
- Timeout 5-10s

## Pitfalls
- 429 → backoff exponencial
- addressdetails=1 OBLIGATORIO para reverse
- zoom=18 para máxima resolución
- countrycodes=es para priorizar España
