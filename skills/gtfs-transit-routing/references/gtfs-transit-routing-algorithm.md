# GTFS Transit Routing — Algoritmo BFS con Transbordos

## Complejidad

- **N** = número de paradas
- **E** = número de aristas (parada→parada en mismo trip)
- **B** = max_transfers (default 2)
- **Complejidad:** O(N × B) en el peor caso

## Optimizaciones

1. **visited map:** `stop_id → min_transfers` — no explorar un nodo con más transbordos que ya se visitó
2. **Limitar paradas de origen/destino:** solo las 20 más cercanas, no todas las del radio
3. **Pre-computar grafo:** construir `adjacency[]` una vez, reutilizar para múltiples consultas
4. **Filtrar por horario antes de BFS:** si el horario objetivo es mañana, solo considerar trips de mañana

## Patrón de Transbordo Realista

Dos paradas con IDs distintos pero físicamente cercanas (<100m) se consideran conectables a pie:

```javascript
function buildWalkingConnections(stops, radiusM = 100) {
  const connections = [];
  for (let i = 0; i < stops.length; i++) {
    for (let j = i + 1; j < stops.length; j++) {
      const dist = haversine(stops[i].stop_lat, stops[i].stop_lon,
                             stops[j].stop_lat, stops[j].stop_lon) * 1000;
      if (dist <= radiusM) {
        connections.push([stops[i].stop_id, stops[j].stop_id]);
      }
    }
  }
  return connections;
}
```

Añadir estas conexiones al grafo transit con `travel_time_sec = dist * 1.2` (andando a 5 km/h ≈ 1.2s/m).

## Referencias Externas

- **GTFS Spec:** https://gtfs.org/documentation/schedule/reference/
- **OpenTripPlanner Algorithm:** BFS con ventanas temporales (time-dependent Dijkstra)
- **Valhalla GTFS:** routing con GTFS usando A* con heurística de distancia
