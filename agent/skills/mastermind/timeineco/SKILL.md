---
name: timeineco
version: "1.1.0"
description: "TimeIneco — visor de isocronas multi-modo (coche, bus, metro, tranvía, bici, andando) con motor ORS real, fallback simulación orgánica, datos demográficos reales por código postal (salarios INE, precios vivienda, CO₂), GTFS EMT Madrid, DOCX informe 12+ secciones, y SHP real para QGIS."
author: David Antizar
tags: [timeineco, isochrones, gtfs, routing, ors, nap, leaflet, transport, mobility, docx, shapefile, shp]
---

# TimeIneco — Visor de Isocronas Multi-Modo

TimeIneco calcula y visualiza **isocronas** (áreas accesibles en X tiempo) para 4 modos de transporte con 3 rangos temporales cada uno. Desplegado en NaN.builders.

**URL:** `https://timeineco-ntizar-ntizar.apps.nan.builders/`

**Repositorio:** GitHub `Ntizar/TimeIneco` (privado)

---

## 1. Arquitectura General

```
Frontend (HTML/JS vanilla, sin framework)
    ├── Leaflet (mapa base CartoDB Positron)
    ├── OpenRouteService API (isocronas reales vía proxy Node.js)
    ├── Motor de simulación orgánica (fallback sin ORS)
    ├── GTFS Engine browser-side (paradas cercanas a 500m + rutas)
    ├── Turf.js (coastline clipping)
    ├── Clipping costero (Natural Earth 110m)
    ├── docx.js (informe DOCX 10 secciones — reemplaza jsPDF)
    ├── JSZip (subida de GTFS ZIP + export SHP)
    └── shp.js (ESRI Shapefile QGIS-compatible: .shp/.shx/.dbf/.prj)

Backend (Node.js, server.mjs)
    ├── Proxy ORS (POST /isochrone)
    ├── Proxy GTFS download (POST /gtfs-download)
    ├── Health check (GET /healthz)
    └── Static files + MIME types
```

## 2. Modos de Transporte

| Modo | Perfil ORS | Simulación | Velocidad | Color |
|------|-----------|-----------|-----------|-------|
| Coche 🚗 | `driving-car` | 40 km/h, calles marcadas (σ 0.10, peso 0.35) | 40 km/h | `#2563eb` |
| Bus 🚌 | `driving-car` (ORS no tiene bus) | 12 km/h, orgánico | 12 km/h | `#a855f7` |
| Metro 🚇 | `driving-car` (aproximación) | 32 km/h, radial | 32 km/h | `#ef4444` |
| Tranvía 🚊 | `driving-car` (aproximación) | 20 km/h, radial suave | 20 km/h | `#06b6d4` |
| Bici 🚲 | `cycling-regular` | 15 km/h, estrellado (σ 0.12, peso 0.20), elevación simulada | 15 km/h | `#f97316` |
| Andando 🚶 | `foot-walking` | 5 km/h, difuso (σ 0.18, peso 0.07) | 5 km/h | `#22c55e` |

Rangos: **15, 30, 45, 60 minutos** (configurable).

### Datos Demográficos (v1.0)

`demographics.js` carga datasets JSON desde `/data/` y enriquece cada isócrona:

- **Códigos postales** (`data/codigos-postales-spain.json`): 299 CPs con centroides, densidad, municipio, provincia, comunidad
- **Salarios medios** (`data/salarios-medios.json`): 51 provincias, datos INE 2024-2025
- **Precios vivienda** (`data/precios-vivienda.json`): 127 CPs con €/m² alquiler y compra

Funciones clave:
- `buscarCP(lat, lng)` → CP más cercano con datos enriquecidos
- `buscarCPsEnPoligono(coords)` → todos los CPs dentro de una isócrona
- `estadisticas(cps)` → población, salario medio, precios de la zona
- `calcularAhorroCO2(distancia)` → CO₂ por modo con equivalencia en árboles
- `calcularPorcentajeSueldo(coste, salario)` → % del salario en transporte
- `cargarGTFS()` → carga datos GTFS (paradas + rutas) al inicio junto con datos demográficos
- `buscarParadasCercanas(lat, lng, radioKm=1.5)` → {paradas, lineas, resumen} — paradas de bus/metro dentro de un radio, con rutas que pasan por cada una
- `buscarLineasConectoras(lat1, lng1, lat2, lng2)` → líneas que conectan dos puntos (por paradas cercanas a ambos)

### Búsqueda de Transporte Público Cercano (v1.1)

Al clicar un punto, `main.js` ejecuta `buscarParadasCercanas()` que:
1. Recorre todas las paradas GTFS y calcula distancia Haversine
2. Filtra por radio (default 1.5km)
3. Para cada parada, busca en `route_stops` qué rutas pasan por ella
4. Compila lista de líneas únicas ordenadas por cobertura (paradas en radio)
5. Devuelve resumen: total paradas, total líneas, parada más cercana, distribución por tipo

**Pitfall:** Las paradas GTFS del cache pueden tener `route_stops` con stop_ids que no coinciden exactamente con los stop_ids de `stops[]`. Verificar que el `stop_id` en `route_stops` existe en `stops[]` antes de buscar rutas.

**Pitfall:** `demographics.js` usa `fetch()` para cargar datos → funciona en browser pero NO en Node.js directo. Para tests unitarios, cargar los JSON manualmente con `fs.readFileSync()`.

### Salarios por CP (v1.1.1)

**Problema:** Los salarios por provincia (`salarios-medios.json`) dan el MISMO salario a todos los CPs de una provincia. Chamberí y Vallecas reciben 32.500€ ambos, cuando en realidad Chamberí ~35.500€ y Vallecas ~23.000€.

**Solución:** `salarios-por-cp.json` — estimación por CP usando el **precio del alquiler como proxy de poder adquisitivo** (correlación ~0.75 con salarios reales en España):

```javascript
// Fórmula de estimación
rent_ratio = alq_m2_cp / alq_m2_provincia_promedio
salary_adj = base_provincia * (1 + (rent_ratio - 1) * 0.5)  // elasticidad 0.5
// Clamped: 70%-150% del salario provincial
```

**Datos:** 299 CPs con salario estimado. Rango: 18.685€ — 40.185€. Media: 26.967€.

**Pitfall:** La correlación alquiler→salario no es perfecta (~0.75). Zonas universitarias o industriales pueden tener alquiler bajo pero salarios medios-altos. Para producción, cruzar con EPA por distrito + convenios colectivos por sector.

### Informes Multi-Ciudad (v1.1.2)

**Patrón:** Función parametrizable `build_report(lat, lng, nombre, ciudad, archivo)` que genera un informe HTML completo para **cualquier punto de España**.

**Archivos generados:**
- `informe-plaza-mayor-madrid.html` — 40.4167, -3.7038
- `informe-nuevos-ministerios-madrid.html` — 40.4464, -3.6921
- `informe-barcelona-sants-ave.html` — 41.3792, 2.1404

**Estructura del informe HTML:**
1. Mapa Leaflet interactivo con círculos de radio por modo (5km → 40km)
2. Resumen ejecutivo (6 KPIs)
3. Transporte público cercano (top 10 paradas + top 15 líneas)
4. Población accesible por modo y tiempo
5. **Coste por minuto** (la sección estrella — €/min por modo)
6. Escenarios teletrabajo (5d/3+2d/2+3d/full remote)
7. CO₂ y coste para la empresa (EU ETS 50€/ton)
8. Mercado inmobiliario (top 10 CPs)
9. Comparativa visual (barras)
10. Recomendaciones para RRHH y empleado

**Cómo usar:**
```javascript
// En execute_code o script Python
build_report(lat, lng, "Nombre del punto", "Ciudad", "/ruta/salida.html")
```

**Pitfall:** El GTFS por defecto solo tiene datos de Madrid (EMT). Para Barcelona u otras ciudades, crear un `gtfs-cache-{ciudad}.json` y fusionarlo:
```python
gtfs = {
    'routes': gtfs_madrid['routes'] + gtfs_otra_ciudad['routes'],
    'stops': gtfs_madrid['stops'] + gtfs_otra_ciudad['stops'],
    'route_stops': {**gtfs_madrid['route_stops'], **gtfs_otra_ciudad['route_stops']},
}
```

**Pitfall:** Si no hay paradas GTFS en 1.5km del punto (ciudad sin datos), el informe debe manejar `paradas_top[0]` vacío. Añadir check: `if paradas_top:` antes de acceder.

### GTFS Barcelona (v1.1.2)

`data/gtfs-cache-barcelona.json` — 61 paradas, 8 rutas:
- **L1** (Roja): Hospital de Bellvitge ↔ Fondo (12 paradas)
- **L3** (Verde): Zona Universitària ↔ Trinitat Nova (15 paradas)
- **L5** (Azul): Cornellà Centre ↔ Vall d'Hebron (12 paradas)
- **L9**: Aeroport T1 ↔ ZAL Riu Vell (6 paradas)
- **R1** Rodalies: Sants → Clot (6 paradas)
- **Bus TMB**: H12, V15, D20 (10 paradas)

Parada más cercana a Sants: **Sants Estació (0m)** — L1+L3+L5+R1 convergen.

### Coste por Minuto y Teletrabajo (v1.1.1)

Nuevas funciones en `demographics.js`:

```javascript
// Coste por minuto de desplazamiento
calcularCostePorMinuto(minutosIda, salarioBruto, modo, distanciaKm)
// → { coste_mensual, coste_anual, coste_por_minuto, salario_neto_anual,
//     sueldo_neto_trasporte, pct_neto, co2_anual_kg, co2_precio_eur }

// Escenarios de teletrabajo (5d/3+2d/2+3d/full remote)
calcularEscenariosTeletrabajo(minutosIda, salarioBruto, modo, distanciaKm)
// → { base, escenarios[], ahorro_total_teletrabajo }

// CO₂ con precio EU ETS para la empresa
calcularCosteCO2Empresa(co2AnualKg, sector='general')
// → { coste_ets, coste_reputacional, certificado_voluntario, coste_total }
```

**Constantes clave:**
- `PRECO2_EUR_KG = 0.050` (50€/tonelada EU ETS 2025)
- `DIAS_LABORALES = 230`
- IRPF estimado por tramo: 15%/21%/28%/35%/42%
- Precios sector: general=50, banca=80, industria=45, tecnología=60 €/ton

**KPIs ejemplo (Plaza Mayor, 60min metro):**
- Coste por minuto: 0.02€
- Sueldo neto trasporte: 19.151€/año
- CO₂ empresa: 1.104 ton = 55€ EU ETS/año
- Ahorro 3d teletrabajo: 10€/año

**Pitfall:** El IRPF es una estimación por tramo. El cálculo real depende de circunstancias personales (hijos, discapacidad, etc.). El informe debe indicar "IRPF estimado" explícitamente.

## 3. Motor de Isocronas

### ORS Real (prioritario)

- Endpoint proxy: `POST /isochrone` → ORS API
- Perfiles: `driving-car`, `foot-walking`, `cycling-regular`
- APi key en `.env`, servidor arrancado con `node --env-file=.env server.mjs`
- Health check: `GET /healthz` → `{ ors_api: true/false }`

### Simulación Orgánica (fallback)

Cuando ORS no responde, se usa un motor de simulación local que NO genera círculos perfectos:

1. **72 puntos base** (5° spacing)
2. **5 capas de ruido multicapa** (frecuencias: 0.7, 2.3, 5.1, 11.3, 17.1)
3. **12 corredores radiales** (calles principales cada 30° + secundarias offset 15°)
4. **[Bici] Campo de elevación simulado** (5 capas de ruido orográfico, penaliza radio hasta 30%)
5. **Suavizado Gaussiano** 3-ventana ([0.25, 0.50, 0.25])
6. **Clipeo costero** (turf.intersect con Natural Earth 110m)

### Clipeo Costero

Ver skill `isochrone-routing-tools` sección 8. Datos: Natural Earth 110m land (135KB, 127 features). Carga lazy solo si el punto está en zona costera (lista de 16+ ciudades). Fallback a polígono mínimo ~50m si la isocrona cae completamente en el mar.

## 4. GTFS Engine

### Qué hace

- Detecta ciudad del usuario por coordenadas
- Muestra operadores candidatos (EMT Madrid, EMTUSA Gijón, ALSA, etc.)
- Carga GTFS del operador elegido (desde cache localStorage o subida ZIP)
- Busca paradas a ≤1.5km del origen (Haversine)
- Muestra rutas disponibles (chips de líneas)
- Exporta paradas a GeoJSON
- Incluye tabla en PDF

### Datos simulados

`data/gtfs-cache.json` contiene datos EMT Madrid (46 rutas, 250 paradas). Es suficiente para demo sin conexión a API real.

**Pitfall GTFS sintético:** El cache puede tener 0 trips, 0 stop_times, 0 shapes. Esto es suficiente para búsqueda de paradas cercanas (usa `stops[]` + `route_stops{}`) pero NO para simulación de rutas en tiempo real (necesita `trips[]` + `stop_times[]`). Si se necesita realismo de horarios, descargar GTFS ZIP real de EMT Madrid.

**Dato clave:** Las paradas del cache tienen nombres reales de Madrid (Puerta del Sol, Gran Vía, Sol, Ópera, Atocha, etc.) con coordenadas reales. Esto hace que el informe sea creíble para demostración.

### Radio de búsqueda: 500m

El radio por defecto de `findStopsNear()` es **500 metros** (cambiado de 2km en v0.8). Esto es más realista para andar a la parada (5-7 min) que los 2km originales. Para cambiar: editar `radiusKm = 0.5` en la firma de `findStopsNear()` en `gtfs-engine.v7.js`.

### Pitfall: CDN cachea 404 en NaN

Cuando se renombra un archivo GTFS engine (ej: `gtfs-engine.js → gtfs-engine.v7.js`), Cloudflare cachea el 404 del .js original por 4h. Los imports ES module en `main.js` y `nap.js` deben actualizarse. **No usar `?v=N` en imports ES module** — los imports no llevan query params. Versionar el nombre del archivo.

### Subida de ZIP real

El usuario puede arrastrar/soltar su propio GTFS ZIP. Se parsea con JSZip en el navegador, sin enviar datos al servidor.

### Proxy de descarga

`POST /gtfs-download` en server.mjs permite descargar feeds GTFS externos que no soportan CORS.

## 5. Estructura de Archivos

```
TimeIneco/
├── index.html              # Entry point, CDNs (Leaflet, turf, jsPDF, JSZip, html2canvas)
├── css/style.css           # Estilos completos (+180 líneas GTFS)
├── js/
│   ├── main.js             # Orquestación: eventos, flujo cálculo, integración GTFS + demographics
│   ├── map.js              # Leaflet: mapa base, isocronas, marcadores paradas
│   ├── isochrones.js       # Motor: ORS proxy + simulación orgánica (72pts + ruido + calles)
│   ├── clip.js             # Coastline clipping con turf.intersect()
│   ├── config.js           # Configuración: 6 modos, velocidades, colores, rangos
│   ├── demographics.js     # Motor demográfico: CP, salarios, vivienda, CO₂ (v1.0)
│   ├── pdf.js              # jsPDF: informe multi-página con mapas, tablas, GTFS
│   ├── nap.js              # Catálogo NAP: operadores GTFS por ciudad, UI selección
│   ├── docx-report.js      # DOCX informe 12+ secciones (reemplaza jsPDF)
│   ├── gtfs-engine.v7.js   # Motor GTFS browser-side (JSZip, Haversine, localStorage)
│   ├── shp.js              # ESRI Shapefile QGIS-compatible (.shp/.shx/.dbf/.prj)
│   └── utils.js            # Funciones auxiliares (formatKm2, formatNum, etc.)
├── data/
│   ├── gtfs-cache.json     # EMT Madrid: 46 rutas, 250 paradas reales
│   ├── codigos-postales-spain.json  # 299 CPs España con centroides y densidad (v1.0)
│   ├── salarios-medios.json         # 51 provincias, salario medio INE (v1.0)
│   ├── salarios-por-cp.json         # 299 CPs con salario estimado por proxy alquiler (v1.1.1)
│   ├── precios-vivienda.json        # 127 CPs con €/m² alquiler y compra (v1.0)
│   └── ne_110m_land.geojson         # Coastline global (135KB)
├── server.mjs              # Node.js: proxy ORS + GTFS download + static files + rate limiting
├── .env                    # ORS_API_KEY (no commit)
├── informe-plaza-mayor-madrid.html  # Informe demo generado (v1.0)
├── AUDITORIA-v1.0.md       # Auditoría completa del proyecto
└── package.json            # Solo server.mjs deps
```

## 6. Modo de Arranque

```bash
# Local
cd /root/workspace/TimeIneco
node --env-file=.env server.mjs

# El servidor sirve en http://localhost:4000
# Health check: curl http://localhost:4000/healthz
```

Si muere el proceso: `pkill -f "server.mjs"` y volver a arrancar.

## 7. Despliegue en NaN

- Repo push a GitHub → NaN auto-deploy
- NaN usa Cloudflare CDN → si hay archivos nuevos JS, **usar versionado en nombre** (ej: `gtfs-engine.v7.js`) para evitar cache de 404
- Cache-bust: `v=7` en query param para `<script>` y `<link>` tags
- Ver skill `nan-deploy-sync` para CDN cache pitfalls

## 8. DOCX Report (12+ secciones)

**Reemplaza a jsPDF.** Genera informe `.docx` editable por el equipo.

### CDN

```html
<script src="https://cdn.jsdelivr.net/npm/docx@8.5.1/build/index.umd.min.js"></script>
```

Vía `window.docx` (global UMD).

### Estructura del documento

| Sección | Contenido |
|---------|-----------|
| **1. Portada** | Título, barra azul decorativa, dirección, fecha, modos |
| **2. Resumen Ejecutivo** | KPIs, tabla principal [Modo, 15min, 30min, 60min, Velocidad, Tipo] |
| **3. Comparativa** | Tabla de costes (0.20€/km coche, 1.50€ bus, 0.05€ bici, 0€ andando), emisiones (120g, 80g, 0g), población (5.200 hab/km²) |
| **3C. Transporte Público Cercano** | Paradas EMT en 1.5km (tabla top 10), líneas que pasan cerca (tabla top 15), distribución por tipo (Bus/Metro/Tranvía) |
| **3D. Coste por Minuto** | €/min por modo, min/día, min/año, % sueldo neto, sueldo neto − transporte |
| **3E. Escenarios Teletrabajo** | 5d presencial / 2dTT / 3dTT / full remote — coste anual, ahorro vs 5d |
| **3F. CO₂ Empresa** | ton CO₂/año × precio EU ETS (50€/ton) + coste reputacional |
| **4. Coche 🚗** | Coste detallado (combustible, parking, peajes), emisiones, recomendación |
| **5. Transporte Público 🚌** | Tabla paradas GTFS a 500m, rutas, abono 54.60€, emisiones |
| **6. Bici 🚲** | Penalización desnivel, coste 0.05€/km, emisiones 0 |
| **7. Andando 🚶** | Área peatonal, coste 0€, emisiones 0 |
| **8. Rutas Recomendadas** | Ranking por modo (🥇🥈🥉), combinaciones multi-modo |
| **9. Recomendaciones Empresa** | Ayudas TP, parking bici, carpooling, flexibilidad |
| **10. Notas Técnicas** | Metodología, ORS vs simulación, clip costero, versión |

### API

```javascript
import { generarDOCX } from './docx-report.js';

const result = await generarDOCX(
  resultados,        // [{modo, minutos, geojson, areaKM2, real}]
  punto,             // {lat, lng, display_name}
  modosActivos,      // ['car', 'bike', ...]
  tiempos,           // [15, 30, 60]
  gtfsData,          // {totalStops, totalRoutes, operador, stops, rutas}
  transporteCercano  // {paradas, lineas, resumen} — de DEMO.buscarParadasCercanas()
);
// → descarga timeineco-informe-movilidad.docx
```

### Estructura del export

```javascript
export async function generarDOCX(resultados, punto, modosActivos, tiempos, gtfsData, transporteCercano) {
  // Exponer datos de transporte para las secciones internas
  window.__timeineco_transporte = transporteCercano;
  
  const doc = new docx.Document({
    sections: [/* ... */],
    styles: { /* Calibri, sizes */ }
  });
  
  const blob = await docx.Packer.toBlob(doc);
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'timeineco-informe-movilidad.docx';
  a.click();
  URL.revokeObjectURL(url);
}
```

### Formato DOCX

- Márgenes: 2.54cm (1 inch) por defecto
- Fuente: Calibri 11pt cuerpo, 16pt títulos, 26pt portada
- Tablas con borde delgado, header azul #2563eb, filas alternadas #f1f5f9
- Colores por modo en cabeceras (`2563eb` coche, `f97316` bici, `22c55e` andando, `a855f7` bus)

### Pitfalls

- **docx.js no es ESM nativo** — usa UMD global `window.docx`. Los imports de módulos ES no pueden usar `import`; deben cargar el CDN global.
- **docx.Packer.toBlob()** — requiere `async/await`. No olvidar el `await` en el handler.
- **Tablas con `docx.Table`** — el constructor `new docx.Table({rows})` recibe un array de `TableRow`. Cada `TableRow` lleva `{children: [TableCell]}`. Es anidado, no plano.
- **Encabezados de tabla** — el `shading: {fill: "2563eb"}` se pasa en `TableCell` properties. `{shading: {fill: "2563eb", val: "clear"}}`.
- **Saltos de página** — `new docx.Paragraph({children: [new docx.PageBreak()]})` para secciones nuevas.
- **Rangos de tiempo** — si el usuario selecciona solo 3 rangos (15, 30, 60), la tabla DOCX muestra esos 3. Si selecciona 4 (15, 30, 60, 90), se adapta. No hardcodear columnas.
- **DOCX signature v1.1** — `generarDOCX()` ahora recibe 6 parámetros: `(resultados, punto, modosActivos, tiempos, gtfsData, transporteCercano)`. El 6º parámetro es `{paradas, lineas, resumen}` de `buscarParadasCercanas()`. Si no se pasa, la sección 3C se omite.
- **DOCX v1.1.1** — Se añaden secciones 3D (coste por minuto), 3E (teletrabajo), 3F (CO₂ empresa). Estas secciones usan `window.__timeineco_transporte` y los datos de `demographics.js` para calcular costes reales por modo. El informe incluye mapas Leaflet capturados como imagen para el DOCX.
- **window.__timeineco_transporte** — el DOCX generator expone `transporteCercano` en `window.__timeineco_transporte` para que las secciones internas lo accedan. Si el informe no muestra la sección de transporte público, verificar que este global está definido.
- **state.transporteCercano** — se inicializa como `null` en el state object de main.js. Se llena después de `buscarParadasCercanas()` en `handleCalcular()`. Si el informe DOCX no muestra datos de transporte, verificar que `state.transporteCercano` no es null.

## 9. SHP Export (Shapefile QGIS-compatible)

**Capa SIG descargable por cada modo × tiempo.** No requiere servidor — se genera en el navegador con `shp.js`.

### Formato

Archivo .zip con:
- `timeineco_{modo}_{minutos}min.shp` — Main file (ESRI Polygon Type 5)
- `timeineco_{modo}_{minutos}min.shx` — Index (offset + content length)
- `timeineco_{modo}_{minutos}min.dbf` — dBASE III con 5 campos: MODO(C10), MINUTOS(N3), AREA_KM2(N10.2), TIPO_REAL(C10), COLOR(C7)
- `timeineco_{modo}_{minutos}min.prj` — WGS84 (GEOGCS["WGS 84",...])

### Endianness

| Componente | Endianness |
|-----------|------------|
| File Header (.shp, .shx) | BIG-ENDIAN (Motorola) |
| Record Header (.shp, .shx) | BIG-ENDIAN |
| Record Content (.shp) | LITTLE-ENDIAN (Intel) |
| DBF | LITTLE-ENDIAN |
| PRJ | Texto (WKT) |

### API

```javascript
import { downloadSHP } from './shp.js';

// Por modo
await downloadSHP('car', 15, geojson);
// → timeineco_car_15min_shp.zip

// Todos a la vez
for (modo of modos) {
  for (t of tiempos) {
    const r = resultados.find(rr => rr.modo === modo && rr.minutos === t);
    if (r?.geojson) await downloadSHP(modo, t, r.geojson);
  }
}
```

### Verificación en QGIS

```bash
# Abrir el ZIP en QGIS
# Layer → Add Layer → Add Vector Layer
# Source type: .zip (ZIP contenedor)
# File encoding: UTF-8
```

Si no abre:
1. **El SHP debe tener `dv.setInt32(0, 9994, false)`** (file code BIG-ENDIAN). Si está en true (LITTLE-ENDIAN), el file code se corrompe.
2. **File Length debe estar en `dv.setInt32(24, fileLenWords16, false)`** (palabras de 16 bits, no bytes).
3. **BBox en el SHP header** debe estar en LITTLE-ENDIAN (`true`), no BIG-ENDIAN (`false`).

### Pitfalls

- **buildSHP en shp.js v0.7 tenía endianness mixto** — el BBox en el header estaba en BIG-ENDIAN cuando debe ser LITTLE-ENDIAN. Se corrigió en v0.8.
- **buildSHX en v0.7 solo tenía 108 bytes** — el índice SHX correcto tiene 108 bytes (100 header + 8 record), pero v0.7 tenía 116 bytes con un record extra. Se corrigió.
- **El DBF debe tener headerLen calculado correctamente** — `32 + 5×32 + 1 = 193` para 5 campos. Si cambias los campos, recalcula.
- **Los puntos `coords` son [lng, lat]** — en el SHP se usan como X (longitud) e Y (latitud), no al revés. No confundir con coordenadas de mapa (lat, lng).
- **La exportación SHP no bloquea el UI** — `downloadSHP` descarga el ZIP en un `<a>` click. El usuario puede seguir usando la app mientras descarga.
