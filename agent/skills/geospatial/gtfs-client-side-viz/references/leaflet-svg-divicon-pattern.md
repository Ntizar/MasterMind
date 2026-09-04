# Leaflet SVG divIcon — Patrón de personajes 3D rotados

Patrón completo para añadir personajes animados (Pac-Man, fantasmas) a un mapa Leaflet usando `L.divIcon` con SVG inline.

## Tile provider: siempre OSM

```javascript
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>',
  maxZoom: 19,
}).addTo(map)
```

Nunca CartoDB (`basemaps.cartocdn.com`) — tiene rate limits. Nunca Mapbox — requiere token.

## Bearing geográfico

```javascript
function bearing(a, b) {
  const lon1 = a[0] * Math.PI / 180, lat1 = a[1] * Math.PI / 180
  const lon2 = b[0] * Math.PI / 180, lat2 = b[1] * Math.PI / 180
  const dLon = lon2 - lon1
  const y = Math.sin(dLon) * Math.cos(lat2)
  const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon)
  return ((Math.atan2(y, x) * 180 / Math.PI) + 360) % 360
}
```

## SVG Pac-Man + Ghost con rotación

Ver SKILL.md sección "Enfoque recomendado" para código completo.

## Aislamiento de ruta

Cuando se selecciona una ruta, ocultar todas las demás:

```javascript
// Ocultar capa general
routeLayer.eachLayer(layer => map.removeLayer(layer))

// Mostrar solo la seleccionada
sel.shapes.forEach(sh => {
  const latlngs = sh.coordinates.map(c => [c[1], c[0]])
  L.polyline(latlngs, { color: '#FFD700', weight: 10, opacity: 0.25 }).addTo(hlLayer)
  L.polyline(latlngs, { color: '#FFD700', weight: 3, opacity: 0.9 }).addTo(hlLayer)
})
map.fitBounds(bounds, { padding: [60, 60], duration: 600 })
```

## Hora real con timezone

```javascript
function ciudadNow(timeZone = 'Europe/Madrid') {
  const now = new Date()
  const parts = new Intl.DateTimeFormat('en-GB', {
    hour: 'numeric', minute: 'numeric', second: 'numeric',
    hour12: false, timeZone,
  }).formatToParts(now)
  const h = parseInt(parts.find(p => p.type === 'hour').value)
  const m = parseInt(parts.find(p => p.type === 'minute').value)
  const s = parseInt(parts.find(p => p.type === 'second').value)
  return h * 3600 + m * 60 + s
}
```

## Contador de estaciones recorridas

```javascript
function activeBusesWithStops(route, simTime) {
  const out = []
  for (const band of route.frequencies || []) {
    if (band.headway <= 0) continue
    const dur = band.tripDur || route.tripDuration || 1800
    for (let dep = band.startSec; dep < band.endSec; dep += band.headway) {
      const elapsed = simTime - dep
      if (elapsed < 0 || elapsed > dur) continue
      const progress = Math.max(0.001, Math.min(0.999, elapsed / dur))
      const sh = route.shapes[0]
      let stopsPassed = 0
      if (sh?.stops?.length) {
        const totalD = sh.stops[sh.stops.length - 1]?.dist || 1
        for (const s of sh.stops) {
          if (progress >= s.dist / totalD) stopsPassed++
        }
      }
      out.push({ progress, stopsPassed })
    }
  }
  return out
}
```
