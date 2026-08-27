---
name: gtfs-box
description: gtfs-box — visor de GTFS/GTFS Realtime para ver operación en tiempo real del transporte público.
---

# GTFS Box — Visor GTFS en Tiempo Real

## Qué hace

[gtfs-box](https://github.com/nagix/gtfs-box) es un visor de GTFS y GTFS Realtime que permite ver la operación en tiempo real del transporte público. Ideal para dashboards de monitorización de flotas y centros de control de transporte.

## Instalación

```bash
# Clonar y construir
git clone https://github.com/nagix/gtfs-box.git
cd gtfs-box
npm install
npm run build
```

## Uso básico

```bash
# Iniciar visor con feed GTFS + GTFS-RT
gtfs-box --gtfs feed.zip --rt-url "https://example.com/rt" --port 3000

# Con opciones de mapa
gtfs-box --gtfs feed.zip --rt-url "https://example.com/rt" \
  --map-style osm \
  --center 40.4168,-3.7038 \
  --zoom 12
```

```javascript
// Integración como librería
import { GTFSBox } from 'gtfs-box';

const viewer = new GTFSBox({
  container: '#map-container',
  gtfs: 'feed.zip',
  realtime: {
    url: 'https://example.com/rt',
    format: 'gtfs-rt'
  }
});

viewer.on('vehicle-update', (vehicle) => {
  console.log(`Vehicle ${vehicle.id} at ${vehicle.lat},${vehicle.lng}`);
});
```

## Pitfalls

- Necesita un servidor GTFS Realtime compatible (GTFS-RT protocol)
- El rendimiento puede degradarse con feeds muy grandes (>1000 vehículos)
- No incluye análisis de frecuencias ni stringlines (usar `gtfs-to-chart` para eso)
- Depende de Leaflet/Mapbox para el mapa base

## Referencias

- Repo: https://github.com/nagix/gtfs-box
- Relacionado: `node-gtfs`, `onebusaway-gtfs-realtime-visualizer`, `transit-data-pipelines`