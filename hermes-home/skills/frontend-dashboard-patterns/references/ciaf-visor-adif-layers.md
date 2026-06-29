# CIAF-visor — Integración capas ADIF

## Capas activas (junio 2026)

| Capa | Fuente | Tipo | Datos |
|------|--------|------|-------|
| Informes CIAF | JSON local | MarkerCluster | 270 informes, ~8 con lat/lng real |
| Red ferroviaria ADIF | `ideadif.adif.es/gservices/Tramificacion/wms` | WMS `TramificacionComun` | Línea continua azul |
| Limitaciones velocidad (LTV) | `services7.arcgis.com/.../LTV_2/FeatureServer/0` | FeatureServer GeoJSON | ~1162 restricciones, datos dinámicos |

## Capas eliminadas

- **Tramificación ADIF** (WFS `TramosServicio`): eliminada por redundancia con WMS.
- **Nombres de líneas** (hardcoded 34 posiciones): eliminada por imprecisión visual ("se ve fatal").

## LTV — Detalles técnicos

- **Coords**: usar `f.geometry.x/y` — los attributes `X,Y` vienen NULL al pedir `outSR=4326`
- **Categorías velocidad**: ≤30 (triángulo rojo), 31-60 (rombo naranja), 61-120 (cuadrado amarillo), >120 (círculo verde)
- **Campos útiles**: CODLINEA, DESCLINEA, RESTRICCIONVELOCIDAD, MOTIVO, PKINI, PKFIN, TIPOTREN, VIAS, OBSERVACIONES
- **Actualización**: dinámica, ADIF edita el FeatureServer en tiempo casi real

## Geolocalización de informes

- Solo 2% (8/270) con lat/lng real
- 71% con PK (punto kilométrico)
- 92% con nombre de estación
- Geocodificación por estación con Nominatim propuesta como mejora pendiente

## Links

- Repo: `Ntizar/CIAF-visor`
- Pages: https://ntizar.github.io/CIAF-visor/
