# Integración GTFS en TimeIneco v0.7

## Contexto

TimeIneco es una aplicación web de isocronas de movilidad laboral. En v0.7 se añadió integración GTFS completa: detección de ciudad, catálogo de operadores, carga selectiva de paradas cercanas y visualización en mapa + PDF.

## Estructura de archivos

```
TimeIneco/
├── js/
│   ├── gtfs-engine.js    ← Motor GTFS (carga, parsing, búsqueda, estado)
│   ├── nap.js            ← Catálogo operadores + panel UI + eventos
│   ├── main.js           ← Orquestación (flujo isocronas + GTFS)
│   ├── map.js            ← Marcadores de paradas Leaflet
│   └── pdf.js            ← Sección GTFS en informe PDF
├── css/
│   └── style.css         ← ~180 líneas de estilos GTFS
├── data/
│   └── gtfs-cache.json   ← Cache simulado EMT Madrid (46 rutas, 100+ paradas)
└── server.mjs            ← Endpoint POST /gtfs-download (proxy CORS)
```

## Motor GTFS (gtfs-engine.js)

### Estado global
```javascript
const _state = {
  loaded: false,
  operador: null,
  ciudad: null,
  data: null,        // { routes, stops, trips, stopTimes, shapes, stopRoutes }
  lastQuery: null
};
```

### Funciones exportadas
| Función | Descripción |
|---|---|
| `cargarDesdeCache(data, op, ciudad)` | Carga cache simulado JSON |
| `cargarDesdeZip(file, op, ciudad)` | Parsea GTFS ZIP real (JSZip) |
| `cargarDesdeLocal(ciudad, op)` | Recupera de localStorage |
| `findStopsNear(lat, lng, radiusKm)` | Búsqueda Haversine |
| `getRouteSummary(stopsNear)` | Resumen agrupado para UI/PDF |
| `getEstado()` | Estado actual del motor |
| `limpiarGTFS()` | Limpia datos cargados |

### Índice stop→routes
Sin stop_times, se infiere por coincidencia semántica:
```javascript
function construirIndiceStopRoutes(data) {
  const stopRoutes = {};
  // 1. Si hay stop_times + trips: enlace real
  // 2. Si no: coincidencia de palabras route_long_name ↔ stop_name
  // 3. Fallback: paradas céntricas reciben rutas base
}
```

### Cache en localStorage
- Prefijo: `timeineco_gtfs_`
- Clave: `{ciudad}_{operador}` ej: `timeineco_gtfs_madrid_emt-madrid`
- Se guarda automáticamente tras cargarDesdeZip()
- Se recupera con cargarDesdeLocal()

## Catálogo de Operadores (nap.js)

### Ciudades cubiertas
Madrid, Barcelona, Sevilla, Valencia, Bilbao, Zaragoza, Málaga, Gijón, Oviedo + ~40 detectables por substring.

### Campos por operador
```javascript
{ id, nombre, modo, lineas, web, gtfsUrl, disponible, cacheable }
```

### Flujo de carga
1. `cargarDesdeCache()` si operador es `cacheable: true`
2. `cargarDesdeLocal()` si hay datos en localStorage
3. Si no: mostrar botón "Subir GTFS"

## Interfaz de Usuario

### Panel NAP (sidebar, dentro de resultados)
```
┌─────────────────────────────────┐
│ 🚌 Transporte público — Madrid   │
│ Operadores y líneas disponibles  │
│ ┌─────────────────────────────┐  │
│ │ 🚌 EMT Madrid           📥 Car│  │
│ │    217 líneas · web         │  │
│ ├─────────────────────────────┤  │
│ │ 🚇 Metro de Madrid   📂 Sube│  │
│ │    13 líneas · web          │  │
│ └─────────────────────────────┘  │
│ 📂 Subir archivo GTFS (.zip)     │
│ ┌─────────────────────────────┐  │
│ │ 🚏 Paradas cercanas    (51) │  │
│ │ 23 rutas · 51 paradas · Aut│  │
│ │ [1 Sol] [2 Gran Vía] [3...]│  │
│ │ [+15 más]                   │  │
│ │ 📋 Ver detalle              │  │
│ └─────────────────────────────┘  │
│ 🗑️ Descartar GTFS               │
│ 📥 Exportar paradas (GeoJSON)    │
└─────────────────────────────────┘
```

### Marcadores en mapa
- Puntos morados (#a855f7) de 10px
- Tooltip: nombre + distancia
- Popup: nombre, distancia, lista de rutas (máx 5)

## PDF: Sección GTFS

- Cabecera: "Rutas de transporte público disponibles"
- Operador, paradas cercanas, líneas disponibles, modo predominante
- Tabla con autoTable (cabecera #a855f7)
- Columnas: Parada | Distancia | Líneas (máx 12 filas)
- Líneas destacadas con paradas que cubren (máx 10)

## Eventos Personalizados

```javascript
// Disparado tras cargar GTFS exitosamente
document.dispatchEvent(new CustomEvent('gtfs:loaded', {
  detail: { estado: getEstado(), punto }
}));

// Escuchado en main.js para añadir marcadores al mapa
document.addEventListener('gtfs:loaded', (e) => {
  const stops = findStopsNear(e.detail.punto.lat, e.detail.punto.lng);
  colocarMarcadoresParadas(stops, e.detail.estado.operador);
});
```

## Datos simulados (gtfs-cache.json)

```json
{
  "_meta": {
    "fuente": "Simulado",
    "descripcion": "EMT Madrid con 46 lineas reales y ~100 paradas representativas"
  },
  "routes": [
    { "route_id": "1", "route_short_name": "1", "route_long_name": "Plaza de Cristo Rey", "route_type": 3 },
  ],
  "stops": [
    { "stop_id": "S001", "stop_name": "Sol", "stop_lat": 40.4170, "stop_lon": -3.7030 },
  ]
}
```

## Testing (consola navegador)

```javascript
// Cargar GTFS y buscar paradas
const resp = await fetch('/data/gtfs-cache.json');
const data = await resp.json();
const engine = await import('./js/gtfs-engine.js');
engine.cargarDesdeCache(data, 'emt-madrid', 'madrid');
const stops = engine.findStopsNear(40.415, -3.707, 1.5);
console.log(`${stops.length} paradas encontradas`);
const summary = engine.getRouteSummary(stops);
console.log(`${summary.totalRoutes} rutas unicas`);
```