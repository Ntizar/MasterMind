---
name: transit-map-simulation
version: "1.0.0"
description: "Mapas de tránsito animados tipo Swiss Trains — patrón inspirado en vasile/transit-map (⭐372). Servidor + cliente para simulaciones de mapas de transporte en tiempo real."
tags: [transit, map, simulation, realtime, websocket, animation]
---

# Simulación de Mapas de Tránsito

## Resumen

Patrón para crear mapas de tránsito animados en tiempo real (tipo swisstrains.ch). Servidor envía posiciones de vehículos via WebSocket, cliente renderiza con SVG/Canvas.

## Cuándo usar

- Mapa de trenes/buses/metros animados en tiempo real
- Visualización de red de transporte con vehículos moviéndose
- Dashboard de movilidad con tracking en vivo

## Arquitectura

```
Servidor (Node.js)
  ├── Cargar GTFS estático (rutas, paradas)
  ├── Fetch GTFS-realtime cada 5s
  ├── Calcular posiciones interpoladas
  └── WebSocket → broadcast posiciones
  ↓
Cliente (SVG/Canvas)
  ├── Renderizar líneas de ruta (SVG paths)
  ├── Renderizar paradas (circles)
  ├── Animar vehículos (interpolación suave)
  └── UI: zoom, pan, selección de línea
```

## Patrón de uso

```javascript
// Servidor: WebSocket con posiciones de vehículos
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

setInterval(async () => {
  const positions = await fetchGTFSRealtime();
  wss.clients.forEach(client => {
    client.send(JSON.stringify({
      type: 'positions',
      vehicles: positions.map(v => ({
        id: v.id,
        route: v.route_id,
        lat: v.latitude,
        lng: v.longitude,
        bearing: v.bearing
      }))
    }));
  });
}, 5000);

// Cliente: SVG con interpolación suave
const svg = d3.select('#map');
const projection = d3.geoMercator();

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  data.vehicles.forEach(v => {
    const [x, y] = projection([v.lng, v.lat]);
    let dot = svg.select(`#v-${v.id}`);
    if (dot.empty()) {
      dot = svg.append('circle')
        .attr('id', `v-${v.id}`)
        .attr('r', 4)
        .attr('fill', routeColors[v.route]);
    }
    // Interpolación suave
    dot.transition().duration(5000).ease(d3.easeLinear)
      .attr('cx', x).attr('cy', y);
  });
};
```

## Pitfalls

- **Interpolación:** Usar `transition().duration(5000).ease(linear)` para smooth movement entre updates.
- **WebSocket reconnection:** Implementar reconexión automática con backoff.
- **Projection:** Mercator distorsiona a alta latitud. Considerar EqualEarth para mapas globales.
- **Performance:** >500 vehículos = usar Canvas en vez de SVG. >5000 = WebGL.
- **Bearing:** Rotar icono de vehículo según dirección de movimiento.

## Referencias

- transit-map: https://github.com/vasile/transit-map (demo: https://swisstrains.ch)
- GTFS-realtime: https://gtfs.org/realtime/

---

**Hecho con ❤️ por David Antizar**
