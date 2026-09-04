---
name: gtfs-client-side-viz
version: "1.0.0"
description: "Visualización de GTFS a escala en el cliente sin backend. Inspirado en gabrielAHN/gtfs-viz (⭐50). Renderiza rutas, paradas y horarios directamente en el navegador."
tags: [gtfs, visualization, client-side, browser, transit, leaflet]
---

# Visualización GTFS Client-Side

## Resumen

Renderizar archivos GTFS completos (rutas, paradas, horarios) directamente en el navegador sin necesidad de backend. Parsea ZIP, procesa CSV y renderiza en Leaflet/Canvas.

## Cuándo usar

- Visor de GTFS sin servidor
- Explorar feeds GTFS descargados localmente
- Dashboard de transporte que carga GTFS bajo demanda

## Patrón de uso

```javascript
// 1. Cargar ZIP GTFS en el navegador
import JSZip from 'jszip';

async function loadGTFS(zipUrl) {
  const response = await fetch(zipUrl);
  const zip = await JSZip.loadAsync(await response.arrayBuffer());
  
  // Parsear archivos CSV del ZIP
  const stopsCSV = await zip.file('stops.txt').async('text');
  const routesCSV = await zip.file('routes.txt').async('text');
  const stopTimesCSV = await zip.file('stop_times.txt').async('text');
  const tripsCSV = await zip.file('trips.txt').async('text');
  const shapesCSV = await zip.file('shapes.txt').async('text');
  
  return {
    stops: parseCSV(stopsCSV),
    routes: parseCSV(routesCSV),
    stopTimes: parseCSV(stopTimesCSV),
    trips: parseCSV(tripsCSV),
    shapes: parseCSV(shapesCSV)
  };
}

// 2. Renderizar en Leaflet
const map = L.map('map').setView([40.4, -3.7], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Renderizar shapes de rutas
gtfs.shapes.forEach(shape => {
  const latlngs = gtfs.shapes
    .filter(s => s.shape_id === shape.shape_id)
    .sort((a, b) => a.shape_pt_sequence - b.shape_pt_sequence)
    .map(s => [parseFloat(s.shape_pt_lat), parseFloat(s.shape_pt_lon)]);
  L.polyline(latlngs, { color: routeColor, weight: 3 }).addTo(map);
});

// Renderizar paradas
gtfs.stops.forEach(stop => {
  L.circleMarker([stop.stop_lat, stop.stop_lon], {
    radius: 4, fillColor: '#2563eb', fillOpacity: 0.8
  }).addTo(map).bindPopup(stop.stop_name);
});

// 3. Filtrar horarios por ruta y hora
function getSchedule(routeId, hour) {
  const trips = gtfs.trips.filter(t => t.route_id === routeId);
  return gtfs.stopTimes
    .filter(st => trips.some(t => t.trip_id === st.trip_id))
    .filter(st => st.arrival_time.startsWith(hour))
    .sort((a, b) => a.arrival_time.localeCompare(b.arrival_time));
}
```

## Elegir proveedor de tiles: Leaflet vs Mapbox

**REGLA: Tiles 100% gratis sin API = `tile.openstreetmap.org`.** CartoDB/CARTO tiles aunque parezcan gratis tienen rate limits y pueden bloquear. Mapbox requiere token y tiene tier gratuito limitado.

| Proveedor | URL | Gratis? | Token? | Nota |
|-----------|-----|---------|--------|------|
| **OpenStreetMap** | `tile.openstreetmap.org/{z}/{x}/{y}.png` | ✅ Siempre | No | **Recomendado para todo** |
| CARTO Dark | `basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png` | Parcial | No | Rate limits, puede bloquear |
| Mapbox | `api.mapbox.com/...` | Tier free | **Sí** | 50K loads/mes,后 pago |

**Para proyectos David:** Siempre OSM tiles. Si el usuario quiere dark mode, usar un CSS filter `brightness(0.6) invert(1) contrast(3) hue-rotate(200deg)` sobre OSM, o el plugin `leaflet-tilelayer-colorfilter`.

## Añadir personajes 3D al mapa (sin reemplazar)

Cuando el usuario pide "hacer los buses en 3D sobre el mapa", NO significa reemplazar el mapa con Three.js. Significa **mantener el mapa** y añadir elementos 3D encima. Reemplazar el mapa frustra al usuario — pierde búsqueda, popups, controles, y el contexto geográfico.

### Enfoque recomendado: Leaflet + SVG divIcon con rotación

Usar `L.divIcon` con SVG inline para personajes que **giran según la dirección de movimiento**:

```javascript
// Cálculo de bearing geográfico entre dos puntos [lng, lat]
function bearing(a, b) {
  const lon1 = a[0] * Math.PI / 180, lat1 = a[1] * Math.PI / 180
  const lon2 = b[0] * Math.PI / 180, lat2 = b[1] * Math.PI / 180
  const dLon = lon2 - lon1
  const y = Math.sin(dLon) * Math.cos(lat2)
  const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon)
  return ((Math.atan2(y, x) * 180 / Math.PI) + 360) % 360
}

// Pac-Man SVG rotado según bearing
function pacmanIcon(color = '#FFD700', bearingDeg = 0, size = 26) {
  return L.divIcon({
    className: 'pac-icon',
    html: `<div style="
      width:${size}px;height:${size}px;
      transform:rotate(${bearingDeg}deg);
      filter:drop-shadow(0 0 6px ${color}99);
    ">
      <svg viewBox="0 0 100 100" width="${size}" height="${size}">
        <circle cx="50" cy="50" r="46" fill="${color}"/>
        <path d="M50,50 L98,22 A46,46 0 0,1 98,78 Z" fill="#000"/>
        <circle cx="62" cy="35" r="6" fill="#000"/>
      </svg>
    </div>`,
    iconSize: [size, size],
    iconAnchor: [size/2, size/2],
  })
}

// Fantasma SVG con domo + ondas + ojos
function ghostIcon(color = '#FF0000', bearingDeg = 0, size = 26) {
  return L.divIcon({
    className: 'ghost-icon',
    html: `<div style="
      width:${size}px;height:${size}px;
      transform:rotate(${bearingDeg}deg);
      filter:drop-shadow(0 0 6px ${color}88);
    ">
      <svg viewBox="0 0 100 100" width="${size}" height="${size}">
        <path d="M10,95 Q10,70 20,70 Q30,70 30,95 Q30,70 40,70 Q50,70 50,95
                 Q50,70 60,70 Q70,70 70,95 Q70,70 80,70 Q90,70 90,95
                 L90,40 Q90,10 50,10 Q10,10 10,40 Z" fill="${color}"/>
        <circle cx="35" cy="40" r="8" fill="white"/>
        <circle cx="65" cy="40" r="8" fill="white"/>
        <circle cx="38" cy="42" r="4" fill="#2244AA"/>
        <circle cx="68" cy="42" r="4" fill="#2244AA"/>
      </svg>
    </div>`,
    iconSize: [size, size],
    iconAnchor: [size/2, size/2],
  })
}

// Calcular bearing desde las coordenadas de la ruta
const sh = route.shapes[0]
const idx = Math.floor(progress * (sh.coordinates.length - 1))
const bear = bearing(sh.coordinates[idx], sh.coordinates[Math.min(idx+1, sh.coordinates.length-1)])

// Crear icono rotado
const icon = useGhost
  ? ghostIcon('#FF0000', bear)
  : pacmanIcon('#FFD700', bear)

L.marker([lat, lng], { icon }).addTo(map)
```

### Por qué SVG divIcon > Canvas 2D icons

- **Rotación nativa:** `transform: rotate(Xdeg)` en CSS — Canvas 2D requiere rotar todo el contexto
- **Calidad:** SVG escala perfecto a cualquier zoom, Canvas pixela
- **Interactividad:** CSS hover/transition funciona directamente
- **Flexibilidad:** Se puede animar con CSS keyframes (boca abierta/cerrada)

### Canvas 2D (solo para Mapbox)

Si el proyecto usa Mapbox (requiere token), usar Canvas 2D + `map.addImage()`:

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

map.addImage('pacman', createPacmanIcon(48, '#FFD700'))
```

Ver `references/mapbox-css-3d-overlay.md` para el patrón completo Mapbox.

### Efectos 3D con CSS

Para profundidad visual sin Three.js:

```css
.pac-icon, .ghost-icon {
  transition: transform 0.15s, filter 0.15s;
}
.pac-icon:hover, .ghost-icon:hover {
  transform: scale(1.3) rotateY(15deg);
  filter: brightness(1.3) drop-shadow(0 0 12px var(--glow));
}
```

## Aislar ruta seleccionada

Cuando el usuario selecciona una línea, **ocultar las demás** para que el mapa no se sature:

```javascript
// Al seleccionar una ruta:
if (sel) {
  // Ocultar todas las líneas de ruta
  routeLayer.eachLayer(layer => map.removeLayer(layer))

  // Mostrar solo la ruta seleccionada (brillante)
  sel.shapes.forEach(sh => {
    const latlngs = sh.coordinates.map(c => [c[1], c[0]])
    L.polyline(latlngs, { color: '#FFD700', weight: 10, opacity: 0.25 }).addTo(hlLayer)
    L.polyline(latlngs, { color: '#FFD700', weight: 3, opacity: 0.9 }).addTo(hlLayer)
  })

  // Enfocar mapa en la ruta
  const bounds = L.latLngBounds(sel.shapes.flatMap(sh =>
    sh.coordinates.map(c => [c[1], c[0]])
  ))
  map.fitBounds(bounds, { padding: [60, 60], duration: 600 })
}

// Al deseleccionar:
if (!sel) {
  routeLayer.eachLayer(layer => layer.addTo(map))
  hlLayer.clearLayers()
}
```

## Hora real con timezone

Para mostrar la hora de una ciudad específica (no la del navegador):

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

// Actualizar cada segundo (sin aceleración)
useEffect(() => {
  const interval = setInterval(() => setSimTime(ciudadNow()), 1000)
  return () => clearInterval(interval)
}, [])
```

## Pitfalls

- **NO reemplazar el mapa:** Si el usuario tiene un mapa funcional y pide "3D", es overlay, no reemplazo. Perder búsqueda, popups, controles y contexto geográfico frustra al usuario SIEMPRE.
- **NO usar CartoDB tiles como "gratis":** Aunque no piden token, tienen rate limits. Si el usuario dice "algo libre", usar `tile.openstreetmap.org` que es garantizado gratis.
- **Rotación de personajes:** SVG divIcon con `transform: rotate(bearing deg)` es la forma más limpia. Canvas 2D no soporta rotación CSS nativa.
- **Aislamiento de ruta:** Si el usuario selecciona una línea, ocultar las demás. Mostrar 200+ rutas a la vez satura el mapa y lo hace lento.
- **ZIP parsing:** JSZip carga todo el ZIP en memoria. Feeds grandes (>50MB) pueden ser lentos.
- **CSV parsing:** Usar PapaParse para streams grandes. No usar split('\n') — hay saltos de línea dentro de strings.
- **Shapes:** No todos los feeds tienen shapes.txt. Si no, generar ruta desde stop_times secuencial.
- **Memory:** Feeds grandes pueden agotar memoria del navegador. Considerar Web Workers.
- **Time format:** GTFS usa HH:MM:SS (puede pasar de 24:00:00 para servicios nocturnos).

## Referencias

- gtfs-viz: https://github.com/gabrielAHN/gtfs-viz
- JSZip: https://stuk.github.io/jszip/
- PapaParse: https://www.papaparse.com/
- Patrón Mapbox + Canvas 3D icons: `references/mapbox-css-3d-overlay.md`
- Patrón Leaflet + SVG divIcon con rotación: `references/leaflet-svg-divicon-pattern.md`

---

**Hecho con ❤️ por David Antizar**
