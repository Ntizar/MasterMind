# Time v3.0 — Plan de Movida | Arquitectura

**Fecha:** 02/07/2026
**Autor:** David Antizar
**Concepto:** Informe de oferta de transporte para planes de movida de personal

## Contexto

Time v1 era una herramienta de isocronas: clic en un punto → área alcanzable por modo.
Time v3.0 transforma el concepto: el punto es el DESTINO (nueva oficina), y se analizan
las rutas de múltiples EMPLEADOS hacia ese destino, cruzando toda la oferta de transporte
disponible (GTFS, GBFS, parkings, demografía INE).

## Módulos nuevos

### empleados.js
- `addEmpleado(nombre, direccion)` — añade a la lista
- `removeEmpleado(id)` — elimina
- `geocodificarEmpleado(id)` — geocodifica vía Nominatim (secuencial, no paralelo)
- `geocodificarTodos()` — geocodifica pendientes secuencialmente
- `getEmpleadosValidos()` — solo los geocodificados correctamente
- UI: filas con nombre + dirección + estado (✅/❌/⏳/⚪) + botón eliminar
- Event listeners: Enter en campo dirección → geocodificar; change → marcar pendiente

### parkings.js
- `buscarParkings(lat, lng, radiusKm=1.5)` — Overpass API query
- Query OSM: `node["amenity"="parking"](around:${radiusM},${lat},${lng})`
- Fallback endpoints: overpass-api.de → kumi.systems → /overpass (proxy local)
- `resumirParkings(parkings)` — total, conPlazas, totalPlazas, gratis, pago, masCercano
- Tags OSM útiles: name, capacity, fee (yes/no), access, parking (surface/multi-storey/underground)
- Timeout: 12s por endpoint

### routes.js
- `calcularRutas(origen, destino, modos, gtfsCercano)` — calcula rutas para todos los modos
- Modos ORS (car/bike/foot): `POST /ors-directions` con profile correspondiente
- Modos TP (bus/metro/train): estimación basada en distancia + velocidad + tiempo acceso parada
- `recomendarModo(rutas)` — score compuesto: tiempo×0.4 + costeMes×0.035 + co2Anual×0.0025
- `textoRecomendacion(rutas, modoRec)` — genera texto explicativo con razones
- Costes: €/km AEAT 2024, abonos TP por distancia (45/65/85€)
- CO₂: IPCC AR6 factors por modo
- Fallback: si ORS falla, estimar con Haversine × factor ruta (1.3 urbano, 1.2 interurbano)

### report.js
- `generarInforme(data)` — genera DOCX con 14 secciones
- **Pattern clave:** variables `let` a nivel de módulo para constantes docx
  ```javascript
  let HL, AT, BS, ST, WT, PB;
  let _TextRun, _Paragraph, _Table, _TableRow, _TableCell;
  ```
  Asignadas en `generarInforme()`, usadas por todas las funciones `_seccion()`.
  Evita pasar 10+ parámetros a cada función.
- Secciones: portada, disclaimer, resumen, destino, TP, bicis, parkings, demografía,
  isocronas, análisis por empleado (una sección por empleado), comparativa, costes,
  metodología, disclaimer final
- Helpers: `_cell(text, bold, bg, color)`, `_infoRow(label, value)`
- Header: "Time — Plan de Movida | Proyecto Kaizen interno temporal"
- Footer: "Hecho con ❤️ por David Antizar | Página X de Y"

### app.js
- Orquestador principal. Reemplaza a main.js de v1.
- Estado: `destino`, `oferta`, `rutasEmpleados`, `modos`, `tiempos`
- Flujo handleCalcular():
  1. Validar destino (geocodificar si hace falta)
  2. Geocodificar empleados pendientes
  3. Oferta en destino: GTFS + GBFS + parkings + demografía + isocronas
  4. Rutas por empleado (secuencial, con progress bar)
  5. Render: KPIs, tabla, paneles, rutas
- Reutiliza: map.js, isochrones.js, demographics.js, nap.js, citybikes.js, gtfs-engine.v7.js, layers.js
- `colocarMarcador(lat, lng, 'destino')` — marcador rojo para destino

## Endpoints servidor nuevos (server.mjs)

### POST /ors-directions
- Proxy a `api.openrouteservice.org/v2/directions/{profile}`
- Body: `{ profile: 'driving-car', body: { coordinates: [[lng,lat],[lng,lat]], ... } }`
- Auth: `Authorization: <ORS_API_KEY>` (sin Bearer)
- Timeout: 15s
- Diferente del proxy de isocronas (`/v2/isochrones/{profile}`)

### GET /overpass
- Proxy a Overpass API (OSM)
- Query: `?data=<overpass_ql_query>`
- Fallback: overpass-api.de → overpass.kumi.systems
- Sin API key (datos abiertos OSM, licencia ODbL)
- Timeout: 12s por endpoint, fallback automático en 429/error
- Rate limited por server.mjs (30 req/min por IP)

## CSS nuevo (css/time.css)
- `.time-disclaimer` — banner amarillo (#fef3c7) con borde izquierdo naranja
- `.time-empleado-row` — fila de empleado con inputs nombre + dirección
- `.time-oferta-grid` — grid 2 columnas para KPIs de oferta en destino
- `.time-ruta-empleado` — card con rutas por empleado + recomendación
- `.time-table-rutas` — tabla comparativa tiempos por empleado y modo
- `.time-marker-destino` / `.time-marker-empleado` — estilos de marcadores

## Disclaimer
Aparece en 3 sitios:
1. UI sidebar (banner amarillo siempre visible)
2. Portada del DOCX (banner con borde)
3. Sección final del DOCX (con borde completo)

Texto: "Este informe se genera como parte de un proyecto Kaizen interno de carácter
temporal para apoyar el proyecto de movida. No tiene continuidad. Los datos se procesan
en local y no se almacenan ni comparten."
