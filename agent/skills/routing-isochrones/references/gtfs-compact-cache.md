# GTFS Compact Cache — Auto-load sin ZIP/JSZip

Patrón para tener datos GTFS pre-procesados como JSON compacto, servidos desde el servidor y auto-cargados al detectar la ciudad.

## Formato JSON compacto

```json
{
  "stops": [
    {"stop_id": "101", "stop_name": "Plaza Mayor", "stop_lat": 40.415, "stop_lon": -3.707}
  ],
  "routes": [
    {"route_id": "L1", "route_short_name": "1", "route_long_name": "Plaza Mayor - Atocha", "route_type": 3}
  ],
  "route_trip_counts": {"L1": 45, "L2": 30},
  "stop_trip_map": {
    "101": {"trip_count": 120, "sample_arrivals": ["07:00", "07:15", "07:30"]}
  }
}
```

- `route_trip_counts`: route_id → número total de viajes (frecuencia)
- `stop_trip_map`: stop_id → viajes que pasan + muestras de horarios
- Tamaño típico: 150-350KB por ciudad (vs 50-200MB ZIP original)

## Generación (offline)

Script Python que lee los archivos GTFS raw (stops.txt, routes.txt, trips.txt, stop_times.txt) y genera el JSON compacto:

```python
# Procesar GTFS raw → JSON compacto
for city in ['bilbao', 'malaga', 'sevilla', 'valencia', 'zaragoza']:
    stops = parse_csv(f'data/gtfs/{city}/stops.txt')
    routes = parse_csv(f'data/gtfs/{city}/routes.txt')
    trips = parse_csv(f'data/gtfs/{city}/trips.txt')
    stop_times = parse_csv(f'data/gtfs/{city}/stop_times.txt')
    
    # Contar viajes por ruta
    route_trip_counts = Counter(t['route_id'] for t in trips)
    
    # Mapear paradas → viajes
    stop_trip_map = {}
    for st in stop_times:
        sid = st['stop_id']
        if sid not in stop_trip_map:
            stop_trip_map[sid] = {'trip_count': 0, 'sample_arrivals': []}
        stop_trip_map[sid]['trip_count'] += 1
        if len(stop_trip_map[sid]['sample_arrivals']) < 5:
            stop_trip_map[sid]['sample_arrivals'].append(st['arrival_time'][:5])
    
    cache = {'stops': stops, 'routes': routes, 
             'route_trip_counts': dict(route_trip_counts), 
             'stop_trip_map': stop_trip_map}
    save_json(f'data/gtfs-cache/{city}.json', cache)
```

## Endpoint servidor

```javascript
// GET /gtfs-cache/:city
if (pathname.startsWith('/gtfs-cache/')) {
    const city = pathname.split('/')[2];
    if (city === 'list') {
        // Listar ciudades disponibles
        const cities = fs.readdirSync(GTFS_CACHE_DIR)
            .filter(f => f.endsWith('.json'))
            .map(f => f.replace('.json', ''));
        return sendJSON(res, 200, cities);
    }
    const filePath = path.join(GTFS_CACHE_DIR, `${city}.json`);
    if (!fs.existsSync(filePath)) {
        return sendJSON(res, 404, { error: `Cache no disponible para ${city}` });
    }
    serveFile(res, filePath, 'application/json');
    return;
}
```

## Auto-carga en frontend

```javascript
// Al detectar ciudad, auto-cargar GTFS
async function autoLoadGTFS(ciudadId) {
    try {
        const resp = await fetch(`/gtfs-cache/${ciudadId}`);
        if (!resp.ok) return null;
        const data = await resp.json();
        
        // Dispatch event para que main.js renderice
        window.dispatchEvent(new CustomEvent('gtfs:loaded', { 
            detail: { ciudad: ciudadId, data } 
        }));
        return data;
    } catch (e) {
        console.warn(`GTFS cache falló para ${ciudadId}:`, e);
        return null;
    }
}
```

## Renderizado en mapa

```javascript
// Marcadores de paradas con tamaño proporcional a frecuencia
function mostrarTodasParadasGTFS(stops, stopTripMap, ciudad) {
    const group = L.layerGroup();
    for (const stop of stops) {
        const trips = stopTripMap[stop.stop_id]?.trip_count || 0;
        const radius = Math.max(4, Math.min(12, 3 + Math.log10(trips + 1) * 2));
        L.circleMarker([stop.stop_lat, stop.stop_lon], {
            radius, fillColor: '#8b5cf6', fillOpacity: 0.7, 
            color: '#6d28d9', weight: 1
        }).bindTooltip(stop.stop_name)
          .bindPopup(`🚏 ${stop.stop_name}<br>🚌 ${trips} viajes/día`)
          .addTo(group);
    }
    group.addTo(map);
}
```

## Ciudades con cache (Time project)

| Ciudad | Paradas | Rutas | Tamaño |
|--------|---------|-------|--------|
| Bilbao | 533 | 56 | 153KB |
| Málaga | 1,126 | 48 | 315KB |
| Sevilla | 1,038 | 59 | 212KB |
| Valencia | 1,155 | 49 | 336KB |
| Zaragoza | 996 | 55 | 287KB |

## Pitfalls

1. **stop_routes es heurístico:** El cache compacto no incluye mapeo directo stop→route (sería demasiado grande). Se asignan rutas proporcionalmente por trip_count. Aproximado pero suficiente para UI.
2. **Sin shape data:** No se pueden dibujar polilíneas de rutas en el mapa sin `shapes.txt`. Solo marcadores de paradas.
3. **NAP API puede estar caída:** Para descargar GTFS de ciudades sin cache local, la NAP API (transportes.gob.es) puede no responder. Tener fallback a upload manual.
4. **MarkerCluster plugin:** Para 500+ paradas, usar `L.MarkerClusterGroup` para rendimiento. Si no está cargado, los markers se renderizan sin clustering (funcional pero lento).
