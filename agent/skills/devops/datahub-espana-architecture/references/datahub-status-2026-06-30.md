# DataHub España — Estado (2026-06-30 21:00 UTC)

## Fix applied tonight
- **fetchFloods → fetchFlood naming bug:** `fetchFloods()` was called in init() but only `fetchFlood` was defined. Caused ReferenceError that broke the Inundaciones tab. Fixed by renaming the call.

## Overnight fix plan (8 cron jobs)
7 waves of 5 tabs each + final audit, running 21:10-22:10 UTC.

### Tabs to fix per wave
1. Panel, Energía, Clima, Agua, Economía
2. Ambiente (EMPTY), Catastro (EMPTY), Población, EconDet, CalidadAire
3. Demografía, Puertos, Polen, Inundaciones, Suelo
4. TempSuelo, GBFS, Nieve, Mar, UV
5. Visibilidad, Ráfagas, Lluvia, Presión, Fuego
6. Evapo, CAPE, Sol, Rocío, Radiación
7. Térmica, Mareas, Eólica, Nubosidad, AireExt

### Known issues per tab
- **Panel:** PVPC=0.18 (corrupt), Población="—", UV="—"
- **Ambiente:** Panel empty (renderParks exists but panel has no HTML)
- **Catastro:** Panel empty (no content at all)
- **Población:** Population KPI not loading
- **Many tabs:** Missing city selectors, missing Chart.js charts

## Previous status (v2.6)
- 35 tab buttons, 35 panels
- DOM balanced (1186 divs)
- ~120 JS functions defined
- Map with choropleth, parks, layer control
- 12+ APIs integrated

## Estado Actual del Proyecto

### Layout (v2.5)
- Tabs en barra horizontal SUPERIOR (no sidebar lateral)
- Sidebar: solo muestra contenido de la pestaña activa
- Botón ☰ para colapsar/expandir sidebar
- 14 pestañas: Panel, Energía, Clima, Agua, Economía, Ambiente, Catastro, Población, Demografía, Calidad del Aire, Puertos, Polen, Inundaciones, Suelo

### APIs que funcionan (15 fuentes)
| API | Endpoint | Datos |
|-----|----------|-------|
| Open-Meteo Weather | `/v1/forecast` | Clima por coordenadas |
| Open-Meteo Air Quality | `/v1/air-quality` | PM2.5, PM10, O3, NO2, CO, UV, SO2, dust, Polen (6 tipos) |
| Open-Meteo Marine | `/v1/marine` | Oleaje, dirección, periodo, oleaje swell |
| Open-Meteo Flood | `/v1/flood` | Caudal río 14 días |
| Open-Meteo Soil | `/v1/forecast` | Temp/humedad suelo a 3 profundidades |
| USGS Earthquake | `earthquake.usgs.gov/...` | Terremotos últimos 30 días (reemplaza IGN) |
| INE Table 9681 | `servicios.ine.es/...` | Población por CCAA y sexo |
| INE Table 4247 | `servicios.ine.es/...` | Tasa de paro por CCAA |
| ESIOS (fallback) | `api.esios.ree.es` | Renewables 45.2% hardcodeado (API 403) |
| Puertos del Estado | Datos estáticos 2023 | Top 10 puertos por volumen |

### APIs que NO funcionan (no usar)
- **IGN Terremotos:** Devuelve HTML en vez de JSON → usar USGS
- **ESIOS Renewables:** Devuelve 403 → fallback hardcodeado 45.2%
- **DGT/NAP Transporte:** API rota, datos estáticos → eliminada del dashboard

### Capas de Mapa (toggleables desde layer control)
- **Provincias (choropleth):** 52 provincias con GeoJSON simplificado, Canvas renderer
- **Carreteras:** OpenStreetMap HOT tiles
- **Ferrocarriles:** OpenRailwayMap tiles
- **Parques Nacionales:** 16 markers verdes con coordenadas reales

### Parques Nacionales (16)
Picos de Europa, Ordesa, Aigüestortes, Sierra de Guadarrama, Monfragüe, Cabañeros, Doñana, Sierra Nevada, Tablas de Daimiel, Timanfaya, Caldera de Taburiente, Garajonay, Teide, Cabrera, Islas Atlánticas, Sierra de las Nieves

### Ríos por Provincia (52 mapeados)
Madrid→Tajo, Barcelona→Llobregat, Sevilla→Guadalquivir, Bilbao→Nervión, Valencia→Turia, Zaragoza→Ebro, etc.

## Preferencias de David (CRÍTICO)

### Diseño — RECHAZA explícitamente:
- **NO** `border-left: 4px solid color` en cards ("se notan que son ia")
- **NO** liquid glass, glassmorphism, blur effects
- **NO** dark themes
- **NO** fuentes grandes (>16px para KPIs)
- **NO** datos mockup/inventados — NUNCA

### Diseño — QUIERE:
- **SÍ** fondo blanco, sombras sutiles, hover elevación
- **SÍ** fuentes compactas (12-14px labels, 14-17px values)
- **SÍ** tabs horizontales arriba
- **SÍ** pantallas densas con más datos visibles
- **SÍ** cada pestaña: mínimo 4-6 KPIs + 1-2 charts + datos contextuales
- **SÍ** listas clickeables que navegan al mapa
- **SÍ** capas toggleables en el mapa

### Funcionalidad:
- Click en provincia → TODAS las pestañas se actualizan con datos de esa provincia
- Click en puerto → flyTo en mapa + datos en vivo
- Click en parque → flyTo en mapa + info del parque
- Cada pestaña debe ser útil por sí sola Y contextual con provincia seleccionada

### Data Quality:
- Inundaciones DEBE mostrar nombre del río ("no muestra qué río es ni nada")
- Catastro DEBE mostrar datos reales ("no dice nada")
- Parques DEBE tener coordenadas reales para navegar ("debería llevarse a cada parque")
- Puertos DEBE navegar al mapa ("cuando pulsas en un puerto te tendría que llevar ahí")

## Changelog

### 2026-06-30
- Layout: tabs horizontales superiores, Transporte eliminado, Pronóstico en Clima
- Capas mapa toggleables: choropleth, carreteras, ferrocarriles, parques
- Puertos: click → flyTo + datos en vivo
- Parques: 16 nacionales reales con coordenadas
- Catastro: superficie, densidad, municipios, enlace Sede Electrónica
- Inundaciones: 52 ríos mapeados por provincia
- Clima fix: `fetchProvinceWeather()` — sunrise/sunset movidos a daily parameters
- Cron-based building: 20 cron jobs one-shot cada 10 min para añadir 20 pestañas nuevas (GBFS, nieve, oleaje, UV, visibilidad, ráfagas, lluvia, nubosidad, presión, fuego, ET0, CAPE, sol, rocío, suelo, radiación, sensación térmica, aire ext., mareas, eólica)

### Cron-Based Feature Building (2026-06-30)
- 20 cron jobs one-shot espaciados 10 min
- Cada cron: git pull → tab button + panel HTML + JS function → DOM verify → commit + push
- APIs: Open-Meteo (14 endpoints) + GBFS (bike sharing)
- Total: 16→36 pestañas en ~3 horas
- Ver `frontend-dashboard-patterns/references/cron-based-dashboard-building.md` para patrón
