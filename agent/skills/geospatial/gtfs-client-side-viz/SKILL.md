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

## Pitfalls

- **ZIP parsing:** JSZip carga todo el ZIP en memoria. Feeds grandes (>50MB) pueden ser lentos.
- **CSV parsing:** Usar PapaParse para streams grandes. No usar split('\n') — hay saltos de línea dentro de strings.
- **Shapes:** No todos los feeds tienen shapes.txt. Si no, generar ruta desde stop_times secuencial.
- **Memory:** Feeds grandes pueden agotar memoria del navegador. Considerar Web Workers.
- **Time format:** GTFS usa HH:MM:SS (puede pasar de 24:00:00 para servicios nocturnos).

## Referencias

- gtfs-viz: https://github.com/gabrielAHN/gtfs-viz
- JSZip: https://stuk.github.io/jszip/
- PapaParse: https://www.papaparse.com/

---

**Hecho con ❤️ por David Antizar**
