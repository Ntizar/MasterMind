# ADIF — Fuentes de datos ferroviarios españoles

## Fuentes disponibles

ADIF (Administrador de Infraestructuras Ferroviarias) expone datos geoespaciales vía OGC standards.

### 1. WMS Tramificación (RECOMENDADO para mapa base)

- **URL:** `https://ideadif.adif.es/gservices/Tramificacion/wms`
- **Capas:** `TramificacionComun`, `TramosServicio`, `TramosFueraServicio`, `Dependencias`, `PKTeoricos`
- **Estilo:** Líneas con detalle real de vía (mucho más fino que INSPIRE)
- **CRS:** WMS 1.3.0, maneja CRS automáticamente

### 2. WMS INSPIRE (NO recomendado — poco detallado)

- **URL:** `https://ideadif.adif.es/services/wms`
- **Capa:** `TN.RailTransportNetwork.RailwayLink`
- **Problema:** Líneas gruesas, sin detalle de vía
- **Requiere:** `crs: L.CRS.EPSG3857` en Leaflet

### 3. FeatureServer LTV (Limitaciones de Velocidad)

- **URL:** `https://services7.arcgis.com/XTupIrLX53AjaJqO/arcgis/rest/services/LTV_2/FeatureServer/0`
- **Registros:** ~1,162 puntos de restricción
- **Campos:** `RESTRICCIONVELOCIDAD`, `DESCLINEA`, `DESCPSINI`, `DESCPSFIN`

**PITFALL CRÍTICO:** Con `outSR=4326`, los atributos X/Y vienen NULL. Usar siempre `f.geometry.x`/`f.geometry.y`. Añadir `returnGeometry=true` al query.

### 4. WFS Tramificación

- **URL:** `https://ideadif.adif.es/gservices/Tramificacion/wfs`
- **Formato:** GeoJSON, GML
- **Útil para:** geometrías de tramos para renderizado custom

### 5. Renfe Tiempo Real — Cercanías (API JSON)

- **Web:** https://tiempo-real.renfe.com/
- **Solo cubre Cercanías** — NO AVE, Alvia, Avlo, Media Distancia ni Larga Distancia
- **15 núcleos:** Asturias, Bilbao, Cádiz, Cantabria, Cartagena, Ferrol, León, Madrid, Málaga, Murcia/Alicante, Rodalies de Catalunya, San Sebastián, Sevilla, Valencia, Zaragoza

#### Endpoints

| Endpoint | Contenido | Volumen |
|----------|-----------|---------|
| `renfe-visor/lineas.geojson` | Líneas con color y nucleo | 73 líneas |
| `data/estaciones.geojson` | Estaciones con coords, accesibilidad, conexiones | 879 estaciones |
| `renfe-visor/flota.json` | Posición en tiempo real de trenes activos | ~143 trenes |
| `renfe-visor/flota_anterior.json` | Posiciones anteriores (para animación) | Variable |

#### Flota.json (tiempo real) — campos

- `codTren` / `codLinea` — código tren y línea
- `retrasoMin` — retraso en minutos
- `latitud` / `longitud` — posición GPS actual
- `codEstOrig` / `codEstDest` — origen y destino
- `codEstAct` / `codEstSig` — estación actual y siguiente
- `horaLlegadaSigEst` — llegada a siguiente estación
- `nucleo` — código numérico del núcleo (ver tabla en `references/adif-spatial-data-apis.md`)
- `accesible` / `via` / `nextVia`

#### Limitaciones

- ❌ NO AVE / Alta Velocidad / Media Distancia / Larga Distancia
- ❌ Solo estado real — NO horarios programados
- ❌ NO precios ni disponibilidad

### 6. Red de Ferrocarriles IGN (FeatureServer) — datos vectoriales completos

- **URL:** `https://services1.arcgis.com/nCKYwcSONQTkPA4K/arcgis/rest/services/RedFerrocarrilesIGN/FeatureServer`
- **Propietario:** IGN — **Licencia CC-BY 4.0**
- **3 capas:** estaciones (3.035), líneas (50.165 tramos), áreas ferroviarias (8.167)
- **Atributos ricos:** ancho de vía, electrificación, titular, uso, Red TenT, estado físico
- **⚠️ Ver sección 4 de `references/adif-spatial-data-apis.md` para campos detallados, queries y código Leaflet**
- **Superior a ADIF WMS** para queries de atributos; ADIF WMS sigue siendo mejor para visualización de mapa base
