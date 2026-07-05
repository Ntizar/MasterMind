---
name: gtfs-static-editor
version: "1.0.0"
description: "Editor GUI para crear, editar y exportar datos GTFS estáticos. Inspirado en WRI-Cities/static-GTFS-manager (⭐159). Interfaz visual para gestionar agencias, rutas, paradas y horarios."
tags: [gtfs, editor, gui, transit, static, data-management]
---

# Editor GUI de GTFS Estático

## Resumen

Herramienta web para crear, editar y exportar feeds GTFS estáticos sin programar. Interfaz visual para gestionar agencias, rutas, paradas, viajes y horarios. Exporta ZIP GTFS válido.

## Cuándo usar

- Crear feed GTFS desde cero para una agencia pequeña
- Editar feed GTFS existente (añadir rutas, cambiar horarios)
- Validar y exportar GTFS para Google Maps, Transit, etc.
- Migrar horarios de Excel/CSV a GTFS

## Estructura de un feed GTFS

```
feed.zip
├── agency.txt          # Agencias de transporte
├── routes.txt          # Rutas (líneas)
├── trips.txt           # Viajes (recorridos específicos)
├── stops.txt           # Paradas (coordenadas GPS)
├── stop_times.txt      # Horarios por parada y viaje
├── calendar.txt        # Días de servicio (L-V, L-S, etc.)
├── calendar_dates.txt  # Excepciones (festivos, obras)
├── shapes.txt          # Geometría de rutas (polilíneas)
├── frequencies.txt      # Frecuencia en vez de horarios exactos
├── transfers.txt       # Transbordos entre paradas
├── fare_attributes.txt # Tarifas
└── fare_rules.txt      # Reglas de tarifas
```

## Patrón de uso

```javascript
// Cargar feed GTFS existente
async function loadGTFS(file) {
  const zip = await JSZip.loadAsync(file);
  const tables = {};
  for (const filename of ['agency', 'routes', 'stops', 'trips', 'stop_times', 'calendar', 'shapes']) {
    const content = zip.file(`${filename}.txt`);
    if (content) {
      tables[filename] = PapaParse.parse(await content.async('text'), { header: true }).data;
    }
  }
  return tables;
}

// Editar parada
function editStop(gtfs, stopId, newData) {
  const stop = gtfs.stops.find(s => s.stop_id === stopId);
  Object.assign(stop, newData);
  // Actualizar mapa
  updateMapMarker(stopId, newData.stop_lat, newData.stop_lon);
}

// Exportar GTFS válido
async function exportGTFS(gtfs) {
  const zip = new JSZip();
  for (const [name, data] of Object.entries(gtfs)) {
    const csv = PapaParse.unparse(data);
    zip.file(`${name}.txt`, csv);
  }
  return zip.generateAsync({ type: 'blob' });
}
```

## Validación

```javascript
// Validar antes de exportar
function validateGTFS(gtfs) {
  const errors = [];
  // Cada ruta debe tener al menos un viaje
  gtfs.routes.forEach(route => {
    if (!gtfs.trips.some(t => t.route_id === route.route_id)) {
      errors.push(`Ruta ${route.route_id} sin viajes`);
    }
  });
  // Cada viaje debe tener stop_times
  gtfs.trips.forEach(trip => {
    if (!gtfs.stop_times.some(st => st.trip_id === trip.trip_id)) {
      errors.push(`Viaje ${trip.trip_id} sin stop_times`);
    }
  });
  // Paradas con coordenadas válidas
  gtfs.stops.forEach(stop => {
    const lat = parseFloat(stop.stop_lat);
    const lon = parseFloat(stop.stop_lon);
    if (isNaN(lat) || lat < -90 || lat > 90) errors.push(`Parada ${stop.stop_id} lat inválida`);
    if (isNaN(lon) || lon < -180 || lon > 180) errors.push(`Parada ${stop.stop_id} lon inválida`);
  });
  return errors;
}
```

## Pitfalls

- **stop_times orden:** Los stop_times de un viaje deben estar ordenados por stop_sequence.
- **calendar vs calendar_dates:** Si se usa calendar_dates sin calendar, todos los viajes deben tener service_id en calendar_dates.
- **shapes:** Si se usan shapes, shape_pt_sequence debe ser secuencial sin gaps.
- **Encoding:** UTF-8 sin BOM. Algunos validadores rechazan BOM.
- **IDs únicos:** route_id, trip_id, stop_id deben ser únicos en todo el feed.

## Referencias

- static-GTFS-manager: https://github.com/WRI-Cities/static-GTFS-manager
- GTFS spec: https://gtfs.org/schedule/
- GTFS Validator: https://github.com/MobilityData/gtfs-validator

---

**Hecho con ❤️ por David Antizar**
