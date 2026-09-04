# Mapbox + CSS 3D Overlay — Patrón PacMan Madrid

Patrón para añadir elementos 3D a un mapa Mapbox funcional sin reemplazarlo.

## Arquitectura

```
Mapbox GL JS (mapa base dark CARTO)
  ├── Rutas: GeoJSON LineString + line layer (glow + solid)
  ├── Paradas: circle layer (pellets dorados)
  ├── Vehículos: symbol layer (Canvas 2D icons: Pac-Man + ghosts)
  └── Popups: mapboxgl.Popup en click
```

## Canvas 2D Icon Generation

Crear iconos como `ImageData` y registrarlos con `map.addImage()`:

```javascript
function createPacmanIcon(size = 48, color = '#FFD700') {
  const c = document.createElement('canvas')
  c.width = size; c.height = size
  const ctx = c.getContext('2d')
  const cx = size / 2, cy = size / 2, r = size / 2 - 2
  ctx.fillStyle = color
  ctx.beginPath()
  ctx.moveTo(cx, cy)
  ctx.arc(cx, cy, r, 0.25 * Math.PI, 1.75 * Math.PI)
  ctx.closePath()
  ctx.fill()
  ctx.fillStyle = '#000'
  ctx.beginPath()
  ctx.arc(cx + 2, cy - r * 0.38, size * 0.06, 0, Math.PI * 2)
  ctx.fill()
  return ctx.getImageData(0, 0, size, size)
}

function createGhostIcon(size = 48, color = '#FF0000') {
  const c = document.createElement('canvas')
  c.width = size; c.height = size
  const ctx = c.getContext('2d')
  const cx = size / 2
  ctx.fillStyle = color
  ctx.beginPath()
  ctx.moveTo(4, size * 0.95)
  const waveCount = 4, waveWidth = (size - 8) / waveCount
  for (let i = 0; i < waveCount; i++) {
    const x = 4 + i * waveWidth
    ctx.quadraticCurveTo(x + waveWidth * 0.25, size * 0.78, x + waveWidth * 0.5, size * 0.95)
    ctx.quadraticCurveTo(x + waveWidth * 0.75, size * 0.78, x + waveWidth, size * 0.95)
  }
  ctx.lineTo(size - 4, size * 0.55)
  ctx.quadraticCurveTo(size - 4, 4, cx, 4)
  ctx.quadraticCurveTo(4, 4, 4, size * 0.55)
  ctx.closePath()
  ctx.fill()
  const eyeR = size * 0.11, pupilR = size * 0.06
  ctx.fillStyle = '#fff'
  ctx.beginPath(); ctx.arc(cx - size * 0.13, size * 0.42, eyeR, 0, Math.PI * 2); ctx.fill()
  ctx.beginPath(); ctx.arc(cx + size * 0.13, size * 0.42, eyeR, 0, Math.PI * 2); ctx.fill()
  ctx.fillStyle = '#2244AA'
  ctx.beginPath(); ctx.arc(cx - size * 0.1, size * 0.42, pupilR, 0, Math.PI * 2); ctx.fill()
  ctx.beginPath(); ctx.arc(cx + size * 0.16, size * 0.42, pupilR, 0, Math.PI * 2); ctx.fill()
  return ctx.getImageData(0, 0, size, size)
}

map.addImage('pacman', createPacmanIcon(48, '#FFD700'))
map.addImage('ghost', createGhostIcon(48, '#FF0000'))
```

## Symbol Layer con alternancia

```javascript
map.addLayer({
  id: 'bus-icon', type: 'symbol', source: 'buses',
  layout: {
    'icon-image': ['get', 'icon'],
    'icon-size': ['interpolate', ['linear'], ['zoom'], 10, 0.35, 14, 0.55, 17, 0.8],
    'icon-allow-overlap': true,
    'icon-ignore-placement': true,
  },
})
```

## Simulación temporal con Turf.js

```javascript
function activeBuses(route, simTime) {
  const out = []
  for (const band of route.frequencies || []) {
    if (band.headway <= 0) continue
    const dur = band.tripDur || route.tripDuration || 1800
    for (let dep = band.startSec; dep < band.endSec; dep += band.headway) {
      const elapsed = simTime - dep
      if (elapsed < 0 || elapsed > dur) continue
      out.push({ progress: elapsed / dur })
    }
  }
  return out
}
```

## Pitfalls

- **Carto dark tiles:** `@2x` en la URL es clave para nitidez
- **Pellet eating:** Usar `performance.now()` para respawn independiente del zoom
- **Alternancia de iconos:** Patrones deterministas (`ri % 5`) dan variedad sin aleatoriedad que cambia cada frame
- **fitBounds en selección:** Al clickear línea, enfocar con `map.fitBounds()` a los bounds de esa ruta
