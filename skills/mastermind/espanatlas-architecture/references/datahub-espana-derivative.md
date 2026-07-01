# DataHub España — Proyecto derivado de EspañaAtlas

## Relación con EspañaAtlas
DataHub España (Ntizar/DataHubEspana) es un dashboard que aplica los patrones de EspañaAtlas pero con un enfoque diferente:
- **EspañaAtlas**: 8.132 municipios, 20+ datasets, dark theme, choropleth municipal
- **DataHub España**: 52 provincias, 8 capas de datos en tiempo real, light theme, API-driven

## Patrones reutilizados de EspañaAtlas
1. **Canvas renderer** (`preferCanvas: true, renderer: L.canvas()`) — obligatorio para choropleth
2. **Pane system** — z-index controlado para labels, choropleth, overlays
3. **GeoJSON real** — nunca circle markers para datos geográficos
4. **Lazy loading** — datasets temáticos se cargan bajo demanda
5. **Hash index IDX** — acceso O(1) por código de provincia/municipio
6. **`setStyle()` en vez de recrear** — re-colorea sin tocar geometría

## Diferencias clave
| Aspecto | EspañaAtlas | DataHub España |
|---------|-------------|----------------|
| Granularidad | Municipal (8.132) | Provincial (52) |
| Datos | Estáticos (JSON pre-cargados) | APIs en tiempo real |
| Theme | Dark (CartoDB dark_nolabels) | Light (CartoDB light_nolabels) |
| GeoJSON source | Propio (TopoJSON 5.9MB) | codeforamerica/click_that_hood (487KB) |
| Interactividad | Rankings, correlaciones, clusters | Click→zoom, búsqueda, panel detalle |

## GeoJSON de referencia
- **Provincias España**: `codeforamerica/click_that_hood` → 52 features
- **Municipios**: `AlexGPlay/SpainLayers` → por provincia (28, 29, 41, 46)
- **Simplificación**: Douglas-Peucker tolerancia 0.001 (~100m) → 96% reducción

## APIs en tiempo real
- ESIOS/REE: PVPC, demanda, renovables (requiere token para algunos endpoints)
- Open-Meteo: clima actual por coordenadas (gratuito, sin token)
- IGN: sísmica últimos 30 días (CORS puede fallar desde Pages)
- Embalses: datos estáticos por cuenca
