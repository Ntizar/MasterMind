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
