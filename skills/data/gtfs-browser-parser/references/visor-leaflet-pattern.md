# Patrón de Visor con Mapa Leaflet Interactivo

**Creado:** 2026-06-23  
**Actualizado:** 2026-06-25 — Añadidas opciones de basemap IGN

## Resumen

Patrón para construir un visor de transporte público con mapa Leaflet interactivo, geocodificación Nominatim, carga de ZIPs GTFS con JSZip, y visualización de paradas con colores por modo de transporte.

## Stack

| Componente | Tecnología | CDN |
|---|---|---|
| Mapa | Leaflet 1.9.4 | unpkg.com |
| Basemap | Ver opciones de basemap abajo | — |
| ZIP parser | JSZip 3.10.1 | embebido inline |
| Geocodificación | Nominatim | nominatim.openstreetmap.org |

## Opciones de basemap para España

### ✅ IGN — Instituto Geográfico Nacional (RECOMENDADO)

Servicio WMTS gratuito, **CC BY 4.0**, sin restricciones de uso. Tiles en EPSG:3857 (GoogleMapsCompatible), compatible directo con Leaflet.

**URL servicio:** `https://www.ign.es/wmts/ign-base`

| Capa | Descripción | Estado |
|------|-------------|:------:|
| `IGNBaseTodo` | Topográfica completa (carreteras, relieve, poblaciones) | ✅ |
| `IGNBase-gris` | Versión gris — ideal para que rutas GTFS destaquen | ✅ |
| `IGNBaseOrto` | Ortofotografía (foto aérea) | ✅ |
| `IGNBaseSimplificado` | Simplificada | ❌ 400 |
| `IGNBaseTodo-nofondo` | Sin fondo | ❌ 400 |

**Licencia:** CC BY 4.0 — "No se aplican condiciones". Atribución: `© IGN - Instituto Geográfico Nacional`

**Código Leaflet (IGN topográfica):**
```javascript
L.tileLayer('https://www.ign.es/wmts/ign-base?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=IGNBaseTodo&STYLE=default&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX={z}&TILECOL={x}&TILEROW={y}&FORMAT=image/jpeg', {
    attribution: '© IGN - Instituto Geográfico Nacional',
    maxZoom: 19
}).addTo(map);
```

**Código Leaflet (IGN gris — recomendado para visores GTFS):**
```javascript
L.tileLayer('https://www.ign.es/wmts/ign-base?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=IGNBase-gris&STYLE=default&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX={z}&TILECOL={x}&TILEROW={y}&FORMAT=image/jpeg', {
    attribution: '© IGN - Instituto Geográfico Nacional',
    maxZoom: 19
}).addTo(map);
```

**Por qué `IGNBase-gris` para GTFS:** Los colores de rutas (azul bus, rojo metro, verde FEVE) destacan sobre fondo gris. Los nombres de calles y poblaciones están en español.

### ✅ CARTO light (alternativa)

```javascript
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap © CARTO',
    maxZoom: 19, subdomains: 'abcd'
}).addTo(map);
```

### ❌ Catastro — NO sirve como basemap

El Catastro tiene WMS gratuito (`ovc.catastro.meh.es`) pero **prohíbe peticiones teseladas**:
> "Se prohibe la descarga masiva de porciones de cartografía y peticiones teseladas"

Solo sirve para consultas puntuales de parcelas, NO como mapa base con tiles.

## Arquitectura

```
┌──────────────────────────────────────────────────┐
│  Header (color del design system)                │
├──────────┬───────────────────────────────────────┤
│ Sidebar  │  Mapa Leaflet                         │
│ 380px    │  Canvas renderer                      │
│          │                                       │
│ Geocodif.│  [click → marcador + círculo radio]   │
│          │                                       │
│ Carga    │  Marcadores paradas: color por modo   │
│ GTFS ZIP │                                       │
│          │  Popup con info de rutas              │
│          │                                       │
│ Radio    │                                       │
│ slider   │                                       │
│          │                                       │
│ Stats    │                                       │
│ (KPIs)   │                                       │
│          │                                       │
│ Lista    │                                       │
│ paradas  │                                       │
└──────────┴───────────────────────────────────────┘
```

## Colores por modo de transporte

| Type | Modo | Color | Hex |
|---|---|---|---|
| 3 | Autobús | Azul | #2563eb |
| 0 | Tranvía | Púrpura | #7c3aed |
| 1 | Metro | Rojo | #dc2626 |
| 2 | Subterráneo | Rojo | #dc2626 |
| 4 | Ferrocarril | Verde | #16a34a |
| 5 | Funicular | Naranja | #ea580c |
| 6 | Barco | Cyan | #0891b2 |
| 7 | Teleférico | Violeta | #a855f7 |
| 11 | Tren ligero | Teal | #0d9488 |
| 12 | Exprés | Azul | #2563eb |

## Implementación clave

### Geocodificación Nominatim
```javascript
const resp = await fetch(
    `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5&countrycodes=es`,
    { headers: { 'User-Agent': 'GTFSSpain/1.0' } }
);
```

### Click en mapa → buscar paradas
```javascript
map.on('click', function(e) {
    currentLat = e.latlng.lat;
    currentLon = e.latlng.lng;
    updateUserMarker(currentLat, currentLon);
    buscarParadas();
});
```

### Círculo de radio visual
```javascript
searchCircle = L.circle([lat, lon], {
    radius: radius, color: '#2563eb', fillColor: '#2563eb',
    fillOpacity: 0.08, weight: 2, dashArray: '5,5'
}).addTo(map);
```

## Implementación real

Archivo: `/root/workspace/GTFSSpain/visor/index.html`  
Design system: Kaizen CSS v4.0 (`/root/workspace/kaizen-design-system/kaizen.css`)
