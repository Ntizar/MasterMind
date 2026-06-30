---
name: datahub-espana-architecture
description: Arquitectura completa de DataHub España — dashboard de datos en tiempo real con mapa, 16+ pestañas, tabs horizontales superiores, capas de mapa, APIs públicas sin auth, cron-based incremental building
version: "2.7.0"
tags: [datahub, dashboard, spain, esios, ign, leaflet, chartjs, vanilla-js, open-meteo, ine, air-quality]
---

# DataHub España — Arquitectura

## Repo
- **GitHub:** `Ntizar/DataHubEspana` (PÚBLICO)
- **Pages:** `https://ntizar.github.io/DataHubEspana/`
- **Workflow:** `.github/workflows/pages.yml` (actions/deploy-pages@v4)
- **Branch:** `main`

## Estructura
```
DataHubEspana/
├── index.html                    # Dashboard principal (SPA)
├── data/
│   └── codigos-postales-centroids.json  # 251 centroides postales
├── scrapers/                     # 19 scrapers Python
│   ├── esios/                    # ESIOS/REE — energía
│   ├── aemet/                    # AEMET — meteorología
│   ├── boe/                      # BOE — boletín oficial
│   ├── borme/                    # BORME — mercantil
│   ├── catastro/                 # Catastro — catastro
│   ├── contratacion/             # Contratación pública
│   ├── dgt/                      # DGT — tráfico
│   ├── embalses/                 # Embalses — agua
│   ├── ine/                      # INE — demografía
│   ├── ign/                      # IGN — geográfico
│   ├── idee/                     # IDEE — espacial
│   ├── oapn/                     # OAPN — parques nacionales
│   ├── puertos/                  # Puertos del Estado
│   ├── subvenciones/             # Subvenciones
│   ├── madrid/                   # Madrid CKAN
│   ├── ckan_multi_portal/        # CKAN multi-portal
│   ├── nap_transporte/           # NAP Transportes
│   ├── datos_gob/                # datos.gob.es
│   └── orchestrator_v2/          # Orquestador maestro
└── tools/
    ├── dashboard-economico/      # Dashboard económico
    ├── mapa-trafico/             # Mapa de tráfico
    └── monitor-energia/          # Monitor de energía
```

## Stack
- **CSS:** Inline CSS (sin framework externo). Diseño limpio profesional.
- **Mapa:** Leaflet 1.9.4 + Layer Control (carreteras, ferrocarriles, choropleth toggleable, parques markers)
- **Charts:** Chart.js 4.4.4
- **Base:** HTML/CSS/JS puro (sin framework)
- **Deploy:** GitHub Pages via GitHub Actions

## Layout v2.6 (2026-06-30) — Tabs horizontales + capas toggleables
- **Pestañas en barra horizontal** `#tab-navbar` arriba del mapa (scrollable horizontal)
- **Sidebar solo muestra contenido** de la pestaña activa (no botones de tabs)
- **Botón ☰** para colapsar/expandir sidebar
- **Pronóstico 7 días fusionado en Clima** (ya no pestaña separada)
- **Transporte ELIMINADO** (API DGT rota, datos estáticos inútiles — David: "no aporta información")
- **Tipografía reducida:** KPIs 14-17px, títulos 12px, body 10-11px
- **Total: 15 pestañas** (Panel, Energía, Clima, Agua, Economía, Ambiente, Catastro, Población, Economía Det., Calidad Aire, Demografía, Puertos, Polen, Inundaciones, Suelo)

## Capas de datos (13+ pestañas)

### 1. 📊 Panel (vista general)
- KPIs: Población total, Provincias, PVPC, Demanda, Renovables, Temperatura Madrid
- KPIs nuevos v2.3: **AQI Europeo**, **Índice UV** (Open-Meteo Air Quality)
- Último terremoto (USGS)
- Hidroelectricidad (embalses)

### 2. ⚡ Energía (ESIOS/REE)
- **PVPC:** Precio medio spot (€/MWh) — indicator 1001
- **Demanda:** Demanda eléctrica total (MW) — indicator 1293
- **Renovables:** % generación renovable — indicator 1294 (⚠️ fallback 45.2% si 403)
- **CO₂:** Intensidad de emisiones (g/kWh)
- **Gráficos:** PVPC últimas 24h (line), Generación por fuente (doughnut)

### 3. 🌤️ Clima (Open-Meteo) — v2.5: incluye Pronóstico 7 días
- Temperatura, viento, humedad, condición meteorológica
- **Pronóstico 7 días integrado** (cards por día + 3 gráficos: temp, precipitación, viento)
- Click provincia → clima de su capital + pronóstico actualizado
- **Error handling:** showToast + fallback values + setTxt() helper
- API: `https://api.open-meteo.com/v1/forecast`

### 4. 💧 Agua (Embalses)
- Nivel medio por cuenca (%)
- Gráfico de barras por cuenca
- Lista con progress bars por embalse

### 5. 💼 Economía (BOE/BORME)
- Constituciones vs disoluciones (doughnut)
- Datos hardcodeados (mejorable con API real)

### 6. 🌿 Medio Ambiente (OAPN) — v2.6: parques reales con coords
- **16 parques nacionales** con coordenadas reales, superficie (km²), año declaración
- **Click en parque → flyTo en mapa** (zoom 11, 1.5s animación)
- **Markers verdes** toggleables desde layer control del mapa
- **Overlay layer:** `parksOverlay` (L.layerGroup con circle markers verdes)
- Coordenadas: Picos de Europa (43.17,-4.85), Ordesa (42.67,-0.02), Aigüestortes (42.58,1.02), Sierra de Guadarrama (40.85,-3.85), Monfragüe (39.83,-6.05), Cabañeros (39.38,-4.32), Doñana (36.95,-6.35), Sierra Nevada (37.05,-3.37), Tablas de Daimiel (39.15,-3.08), Timanfaya (29.00,-13.83), Caldera de Taburiente (28.75,-17.87), Garajonay (28.10,-17.23), Teide (28.27,-16.64), Archipiélago de Cabrera (39.15,2.95), Islas Atlánticas (42.50,-9.00), Sierra de las Nieves (36.68,-5.02)

### 7. 🏗️ Catastro — v2.6: datos reales por provincia
- **Provincia seleccionada:** nombre, código INE, CCAA, capital
- **Superficie** (km²), **Densidad** (hab/km², calculada), **Municipios** (conteo)
- **Enlace directo** a Sede Electrónica del Catastro para la provincia
- Se actualiza al seleccionar provincia en el mapa

### 9. 👥 Población (INE) — NUEVO v2.1
- Población total: 47.615.034
- Densidad, extranjeros, crecimiento
- **Gráfico:** Top 10 CCAA (barras horizontales)
- **Gráfico:** Distribución por edad (doughnut)

### 10. 📈 Economía detallada — NUEVO v2.1
- PIB: 1.418.352M€, Paro: 11,2%, IPC: 2,8%
- **Gráfico:** PIB por sector (barras horizontales)
- **Gráfico:** Paro por provincias Top 10 (barras coloreadas)

### 11. 🚢 Puertos — v2.6: flyTo en mapa + datos en vivo
- Contenedores TEU, Mercancía total, Pasajeros, Cruceros
- **Gráfico:** Top 10 puertos por tonelaje (barras horizontales, clickable)
- **Lista interactiva:** 10 puertos costeros con click → panel detalle
- **Panel detalle puerto** (al click): oleaje, viento, temperatura, humedad, amanecer/atardecer
- ** flyTo en mapa:** Al hacer click en puerto → `map.flyTo([port.lat, port.lon], 12, {duration: 1.5})`
- **APIs:** Open-Meteo Marine (oleaje) + Open-Meteo Weather (clima)
- **Puertos con coordenadas:** Algeciras, Valencia, Barcelona, Bilbao, Las Palmas, Tenerife, Cartagena, Huelva, A Coruña, Gijón

### 12. 🌬️ Calidad del Aire (Open-Meteo Air Quality) — NUEVO v2.3
- **API:** `https://air-quality-api.open-meteo.com/v1/air-quality` (CAMS European forecasts, sin auth)
- **KPIs en tiempo real:** AQI Europeo, PM2.5, PM10, Ozono O₃, NO₂, CO, Índice UV, Polvo, SO₂
- **Gráficos:**
  - Evolución contaminantes 24h (líneas, hourly data)
  - Distribución contaminantes (donut)
- **Se actualiza al seleccionar provincia** → fetch con centroides
- **Fórmula:** `?current=european_aqi,us_aqi,pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide,sulphur_dioxide,dust,uv_index&hourly=pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide,sulphur_dioxide&past_days=1&forecast_days=0`
- **Verificado:** Madrid AQI=38, PM2.5=8.8, O3=96, NO2=10.4, CO=126, UV=7.3

### 13. 📊 Demografía (INE) — NUEVO v2.3
- **API:** `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/9681?tip=AM&nult=1` (población por CCAA y sexo)
- **KPIs:** Población total, Mujeres, Hombres, Tasa dependencia, Índice envejecimiento
- **Gráficos:**
  - Pirámide poblacional (barras horizontales divergentes, mujeres=rosa/hombres=azul)
  - Población por CCAA (top 10, barras horizontales)
  - Distribución por sexo (pie chart)
- **Verificado:** total=47,615,034, women=24,304,407, men=23,310,627, aging=112.7, dependency=49.2%
- **Tabla INE 2852:** población por provincia y sexo (159 entries, funciona)

### 14. 🌾 Polen (Open-Meteo Air Quality) — NUEVO v2.4
- **API:** `https://air-quality-api.open-meteo.com/v1/air-quality?...&current=alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen`
- **KPIs:** Gramen, Olivo, Abedul, Aliso, Artemisa, Ambrosía (gr/m³)
- **Gráficos:** Distribución por tipo (barras) + evolución 24h (líneas)
- **Se actualiza al seleccionar provincia**

### 15. 🌊 Inundaciones (Open-Meteo Flood) — v2.6: ríos por provincia
- **API:** `https://flood-api.open-meteo.com/v1/flood?...&daily=river_discharge&past_days=7&forecast_days=7`
- **KPIs:** Caudal actual, Caudal máx 7d, Caudal mín 7d, Caudal medio
- **Nombre del río:** Mapeo de 52 provincias → río principal (Madrid→Tajo, Barcelona→Llobregat, Sevilla→Guadalquivir, Bilbao→Nervión, Valencia→Turia, Zaragoza→Ebro)
- **Gráfico:** Línea de caudal 14 días (7 pasados + 7 previsión) con nombre del río en título
- **Se actualiza al seleccionar provincia** → muestra río correspondiente

### 16. 🌡️ Suelo (Open-Meteo Forecast) — NUEVO v2.4
- **API:** `https://api.open-meteo.com/v1/forecast?...&hourly=soil_temperature_6cm,soil_temperature_18cm,soil_temperature_54cm,soil_moisture_0_to_1cm,soil_moisture_1_to_3cm,soil_moisture_3_to_9cm,soil_moisture_9_to_27cm`
- **KPIs:** Temp suelo 6/18/54cm, Humedad suelo 0-1/3-9/9-27cm
- **Gráficos:** Temperatura por profundidad (3 líneas) + Humedad por profundidad (3 líneas)

## Mapa — Capas interactivas (v2.6)

### Base tiles
- **CARTO light_all** (por defecto): `https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png`
- **OSM estándar**: `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`

### Overlay layers (toggleables desde Leaflet layer control)
- **Carreteras** (OpenStreetMap HOT): `https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png`
- **Ferrocarriles** (OpenRailwayMap): `https://tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png`
- **Provincias (coropleta)**: `provincesOverlay` (L.layerGroup) — choropleth de 52 provincias
- **Parques Nacionales**: `parksOverlay` (L.layerGroup) — 16 markers verdes con circle markers

### Layer control
```javascript
const baseMaps = { 'CARTO': baseOSM, 'OSM': baseOSMStd };
const overlayMaps = { 'Carreteras': roadsLayer, 'Ferrocarriles': railwaysLayer, 'Provincias': provincesOverlay, 'Parques': parksOverlay };
L.control.layers(baseMaps, overlayMaps).addTo(map);
```

### Choropleth (toggleable)
- 52 provincias con GeoJSON simplificado (487KB)
- Canvas renderer para rendimiento
- Click provincia → zoom + panel detalle derecho
- **Toggle:** `provincesOverlay` permite activar/desactivar la capa desde el layer control

## Diseño actual (v2.5) — Limpio profesional, compacto

### Estilo de cards (CRÍTICO: sin border-left)
- **NO usar `border-left` de colores** → David rechazó explícitamente ("las cards se notan que son ia")
- **Usar gradientes sutiles** en background: `linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%)` para green
- **Hover elevación**: `box-shadow: 0 4px 12px rgba(0,0,0,0.08); transform: translateY(-1px)`
- **Colores**: Azul #2563eb, Naranja #f97316, Verde #16a34a, Rojo #dc2626
- **Fondo KPIs**: `#f8fafc` base con gradientes por tipo (green/orange/red/blue)
- **Border radius**: 10px para KPIs, 12px para cards
- **Sin glass/blur/saturate** → rechazado en v1

### Paleta
- Background: `#f8fafc`
- Cards: `#ffffff` + `border: 1px solid #e2e8f0`
- Texto primario: `#0f172a`
- Texto secundario: `#64748b`
- Labels KPI: `#94a3b8` (más sutiles)

### Sidebar
- Width: 380px, colapsable con botón ☰
- **NO contiene tabs** (v2.5: tabs en #tab-navbar horizontal arriba)
- Solo muestra contenido de la pestaña activa

### Mapa
- Tile: CARTO light_all
- Choropleth: 52 provincias con GeoJSON simplificado (487KB)
- Canvas renderer para rendimiento
- Click provincia → zoom + panel detalle derecho

## Cron Jobs existentes
- `mastermind-autoconfig` — diario 09:00 UTC
- `chromadb-reindex-semanal` — domingo 04:00 UTC

## Datos provinciales extendidos (data/provincias-data.json)

Cada provincia tiene estos campos:
```json
{
  "nombre": "Cantabria",
  "poblacion": 588058,
  "ccaa": "06",          // ← CRÍTICO: código INE correcto (ver pitfall)
  "capital": "Santander",
  "superficie": 5321,    // km²
  "costa_km": 285,       // 0 si interior
  "altitud_media": 463,  // metros
  "paro": 11.2,          // %
  "pib_capita": 29100    // €
}
```

### Códigos CCAA INE (fuente de verdad)
| Cód | CCAA | Cód | CCAA |
|-----|------|-----|------|
| 01 | Andalucía | 11 | Galicia |
| 02 | Aragón | 12 | La Rioja |
| 03 | Asturias | 13 | C. de Madrid |
| 04 | Illes Balears | 14 | Región de Murcia |
| 05 | Canarias | 15 | Navarra |
| 06 | Cantabria | 16 | País Vasco |
| 07 | Castilla y León | 17 | C. Valenciana |
| 08 | Castilla-La Mancha | 18 | Ceuta |
| 09 | Cataluña | 19 | Melilla |
| 10 | Extremadura | | |

## Geolocalización completa (v2.2) — CRÍTICO

### Patrón de barras de contexto
- **Barra `#province-context`:** Aparece arriba al seleccionar provincia, muestra nombre + código
- **Botón limpiar:** Restaura vista nacional (oculta barra, restaura valores por defecto)
- **Animación:** slide-down con `max-height` transition

### Sincronización de pestañas
Al seleccionar provincia → TODAS las pestañas se actualizan:
1. **Clima:** Fetch Open-Meteo por capital de provincia
2. **Economía:** Filtra PIB/paro de la provincia
3. **Población:** Muestra datos demográficos de la provincia
4. **Puertos:** Muestra puertos de la provincia (si tiene costa)
5. **Catastro:** Pre-selecciona la provincia en el dropdown
6. **Agua:** Muestra embalses de la cuenca correspondiente
7. **Transporte:** Muestra ZBE y radares de la provincia

### Coordenadas de centroids
```javascript
const provinceCentroids = {
    '01': [37.39, -5.99],  // Sevilla (Andalucía)
    '02': [41.65, -0.88],  // Zaragoza (Aragón)
    '06': [43.46, -3.81],  // Santander (Cantabria)
    // ... 52 provincias
};
```

### APIs geolocalizadas
- **Clima:** `https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=...`
- **Marina:** `https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&current=...`
- **Fórmula completa Open-Meteo:** `?current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code,wind_direction_10m,sunrise,sunset&daily=sunrise,sunset&timezone=Europe/Madrid`

## Panel detalle de provincia (al click en mapa) — v2.6

El panel derecho debe mostrar TODOS estos campos (David quiere "muchísimos más datos"):
- Población (INE 2024)
- Capital
- Superficie (km²)
- Densidad (hab/km²) — calculada: población/superficie
- Altitud media (m)
- Costa (km) — "Sin costa" si interior
- Paro provincial (%)
- PIB per cápita (€)
- CCAA (nombre completo)
- Código INE
- **Clima detallado** (API Open-Meteo por capital): temperatura, humedad, viento, condición WMO, amanecer, atardecer
- **Fórmula Open-Meteo CORRECTA:** `?current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code&daily=sunrise,sunset&timezone=Europe/Madrid`
- **⚠️ NO incluir sunrise/sunset en current** — causan error silencioso

## Estado de APIs (actualizado 2026-06-30)

### ✅ Funcionan (sin auth)
| API | Endpoint | Datos |
|-----|----------|-------|
| ESIOS PVPC | `api.esios.ree.es/indicators/1001` | Precio spot €/MWh |
| ESIOS Demanda | `api.esios.ree.es/indicators/1293` | Demanda total MW |
| Open-Meteo Weather | `api.open-meteo.com/v1/forecast` | Clima por coordenadas |
| Open-Meteo Marine | `marine-api.open-meteo.com/v1/marine` | Oleaje, olas, viento marino |
| Open-Meteo Air Quality | `air-quality-api.open-meteo.com/v1/air-quality` | AQI EU, PM2.5, PM10, O3, NO2, CO, UV, SO2, Polvo |
| Open-Meteo Flood | `flood-api.open-meteo.com/v1/flood` | Caudal de río 14 días |
| Open-Meteo Soil | `api.open-meteo.com/v1/forecast` (soil_*) | Temp y humedad suelo |
| Open-Meteo Pollen | `air-quality-api.open-meteo.com/v1/air-quality` (pollen) | Polen: alder, birch, grass, mugwort, olive, ragweed |
| USGS Earthquake | `earthquake.usgs.gov/fdsnws/event/1/query` | Terremotos M2.5+ en España |
| INE Demografía | `servicios.ine.es/wstempus/js/ES/DATOS_TABLA/9681` | Población por CCAA y sexo (6120 entries) |
| INE Provincias | `servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2852` | Población por provincia y sexo (159 entries) |
| INE Paro EPA | `servicios.ine.es/wstempus/js/ES/DATOS_TABLA/4247` | Tasa de paro por CCAA y edad (420 entries) |
| INE Empleo | `servicios.ine.es/wstempus/js/ES/DATOS_TABLA/4328` | Empleo por sector (66 entries) |
| INE Empleo temporal | `servicios.ine.es/wstempus/js/ES/DATOS_TABLA/4338` | Ocupados a tiempo parcial (150 entries) |
| INE Asalariados | `servicios.ine.es/wstempus/js/ES/DATOS_TABLA/4358` | Asalariados por tipo (198 entries) |
| IGN Geográfico | GeoJSON local (`data/geo/provincias.json`) | Provincias y municipios |

### ⚠️ Con fallback estático
| API | Fallback | Nota |
|-----|----------|------|
| ESIOS Renovables (1294) | `45.2%` hardcodeado | Ahora devuelve 403 Forbidden (requiere auth) |

### ❌ No disponibles (usar alternativas)
| API | Problema | Alternativa |
|-----|----------|-------------|
| IGN Terremotos (old URL) | Devuelve HTML, no JSON (Liferay CMS rotó la URL) | USGS Earthquake API (gratuita, CORS-friendly) |

### 📋 APIs gratuitas españolas pendientes de integrar
| API | Datos potenciales | Auth |
|-----|-------------------|------|
| INE Tabla 39960 | Turismo: pernoctaciones, viajeros por provincia | No |
| INE Tabla 4247 | Educación: matriculados por nivel | No |
| INE Tabla 31304 | Empleo: afiliados SS por provincia | No |
| INE Tabla 2852a | Nacimientos/muertes por provincia | No |
| INE Tabla 9684 | Censo de población por municipio | No |
| AEMET (requires key) | Predicción detallada, warnings | Sí (gratuita con registro) |
| Copernicus CAMS | Calidad aire histórica, emisiones | Sí (gratuita con registro) |
| Sentinel-5P | NO2 troposférico, SO2, CH4 por satélite | Sí (via Copernicus) |

### Cron de actualización de APIs
- Si una API deja de funcionar → buscar alternativa pública → fallback estático → documentar en esta sección
- Las APIs de ESIOS cambian frecuentemente de requisitos de auth → verificar cada ~3 meses

## Pitfalls
- **GitHub Pages + Actions:** Requiere `enablement: true` en `actions/configure-pages@v5`
- **Token:** `GITHUB_TOKEN` en `/hermes-home/.env`
- **GeoJSON postal codes:** No existe fuente pública → se usan centroides sintéticos
- **ESIOS API:** Requiere token para algunos endpoints
- **CORS:** APIs públicas pueden bloquear requests desde Pages → usar proxy o datos estáticos
- **⚠️ CCAA codes en provincias-data.json:** Los códigos DEBEN seguir el estándar INE (01-19). Error común: asignar códigos desplazados (ej: Cantabria='03' en vez de '06'). SIEMPRE verificar contra la tabla CCAA de arriba. El mapeo CCAA_NAMES en JS también debe alinearse — si está desplazado, Cantabria aparecerá como "Asturias" en el panel detalle.
- **⚠️ Datos por provincia georreferenciados:** David exige que cada pestaña muestre datos relevantes para la provincia seleccionada, no solo datos nacionales genéricos. El panel detalle es la pieza clave — debe ser completo.
- **⚠️ APIs marinas solo para costas:** Open-Meteo Marine solo funciona para coordenadas costeras/marítimas. Para provincias interiores (Madrid, Zaragoza), no llamar a Marine API.
- **⚠️ Sincronización de pestañas:** Al seleccionar provincia, TODAS las pestañas deben actualizarse. David verifica que los datos se mantengan al cambiar de pestaña.
- **⚠️ NO romper al mejorar (Lección 2026-06-30):** David dijo "creo que no estás planteando el crecimiento de la herramienta sin romper cosas". Flujo seguro: (1) diagnóstico antes de tocar, (2) cambios incrementales, (3) verificar braces/JS después de CADA patch, (4) commit por cambio, NO todo junto. Patrón de error: eliminar código JS deja `});` huérfanos que rompen todo silenciosamente.
- **⚠️ Open-Meteo: sunrise/sunset NO son current parameters (Lección 2026-06-30):** `sunrise` y `sunset` solo existen como parámetros `daily`, NO como `current`. Si los pones en `current=...,sunrise,sunset` la API falla silenciosamente y el panel muestra "No disponible". Fix: `current=temperature_2m,...,weather_code&daily=sunrise,sunset`. Verificado con curl: Ávila 31.6°C.
- **⚠️ CSS .tab-content selector (Lección 2026-06-30):** Al eliminar o reorganizar bloques CSS, verificar que `.tab-content { flex: 1; overflow-y: auto; padding: 16px; }` exista. Sin este selector, TODOS los paneles de pestañas se muestran simultáneamente (display:none no aplica). Síntoma: 13 paneles visibles en vez de 1. Causa: patch CSS que rompe la continuidad del bloque.
- **⚠️ DOM nesting al añadir tab panels (Lección 2026-06-30):** Al añadir nuevos `.tab-panel` con `patch()`, si el `old_string` incluye el cierre `</div>` del panel anterior pero el `new_string` no lo reincluye correctamente, los nuevos paneles se ANIDAN dentro del panel anterior en vez de ser hermanos. Síntoma: todos los paneles nuevos tienen `scrollHeight=0` y no se ven. **Debug rápido en consola:**
  ```javascript
  document.querySelectorAll('.tab-panel').forEach(p => {
      console.log(p.id, 'parent:', p.parentElement.id || p.parentElement.className);
  });
  ```
  Si algún panel dice `parent: tab-puertos` en vez de `parent: tab-content`, hay nesting roto. **Fix:** añadir `</div>` de cierre del panel padre antes del primer `<div class="tab-panel">` nuevo. **Verificación Python post-patch:**
  ```python
  import re
  content = open('index.html').read()
  seg = content[content.find('id="tab-puertos">'):content.find('id="tab-polen">')]
  opens = len(re.findall(r'<div[ >]', seg))
  closes = len(re.findall(r'</div>', seg))
  assert opens == closes, f"DOM BROKEN: opens={opens} closes={closes}"
  ```
- **⚠️ GitHub Pages CDN caching (Lección 2026-06-30):** Tras push a `main`, GitHub Pages puede servir versión cacheada durante 2-5 minutos. Añadir `?v=N` al reload no siempre invalida. Si el navegador muestra datos viejos tras push correcto → hard refresh (`Ctrl+Shift+R`) o nueva ventana incógnito. Para verificar que el deploy es correcto: `curl -s raw.githubusercontent.com/Ntizar/DataHubEspana/main/index.html | grep 'NUEVO_TEXT'`.
- **⚠️ Crecimiento sin romper (patrón David):** Cada feature nueva debe: (1) no modificar código existente que funciona, (2) añadir en bloques separados, (3) hacer commit incremental, (4) verificar que pestañas anteriores siguen funcionando. David revisa el dashboard después de cada push y detecta regresiones al instante.
- **⚠️ Helper setTxt() para updates seguros (v2.5):** Al actualizar DOM desde APIs, usar helper que verifica que el elemento existe antes de escribir:
  ```javascript
  const setTxt = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; else console.warn('Element not found:', id); };
  ```
  Esto evita errores silenciosos cuando un ID de elemento no existe o fue renombrado.
- **⚠️ showToast en errores de API (v2.5):** Cuando una API falla al cargar datos de provincia, mostrar toast de error + valores fallback en vez de dejar la UI con "—" o "Cargando…" eterno:
  ```javascript
  } catch (err) {
      showToast(`Error cargando clima de ${nombre}: ${err.message}`, 'error', 3000);
      setTxt('weather-temp', 'No disponible');
      setTxt('weather-detail', `No se pudieron cargar datos de clima para ${nombre}.`);
  }
  ```

## Lecciones de la evolución v1→v2→v2.1

### Lo que David rechazó (v1)
- **Diseño "liquid glass"** → "El diseño es bastante mierda, las cards se notan que son ia"
- **Puntos/círculos en el mapa** → "los cp en vez de puntos deberían ser áreas"
- **Pocos datos** → "faltan muchisimos datos"
- **Sin zoom a provincias** → Necesita interactividad real

### Lo que David rechazó (v2)
- **Cards con `border-left: 4px solid`** → "se nota mucho que es IA" (screenshot de cards azul/naranja con línea vertical)
- **Patrón genérico de dashboard** → "es demasiado template, se ve como hecho por herramienta"

### Lo que funcionó (v2.1)
- **Cards sin border-left**, con gradientes sutiles de fondo
- **Hover elevación** en vez de bordes de color
- **3 pestañas nuevas**: Población (INE), Economía detallada, Puertos
- **6 gráficos nuevos**: barras horizontales, doughnuts, barras coloreadas
- **11 pestañas totales** con datos reales de APIs públicas

### Lo que funcionó (v2.2)
- **Geolocalización completa:** Click provincia → actualiza TODAS las pestañas
- **Barra de contexto:** Muestra provincia seleccionada con botón limpiar
- **Puertos interactivos:** Click puerto → panel detalle con oleaje + clima (APIs Open-Meteo Marine)
- **APIs en cadena:** Weather + Marine para misma ubicación = datos completos
- **52 centroides provinciales:** Para calls API por capital de provincia

### Lo que funcionó (v2.3)
- **Calidad del aire en tiempo real:** API Open-Meteo Air Quality (CAMS) sin auth, datos por provincia
- **Demografía INE completa:** Pirámide poblacional + distribución por CCAA + sexo
- **KPIs en panel principal:** AQI + UV se actualizan con provincia seleccionada
- **Patrón de APIs gratuitas sin auth:** Open-Meteo (weather/marine/air-quality) + INE + USGS =组合 completo sin registrar nada
- **Incrementalidad:** Cada API nueva se añade como pestaña independiente + KPI en panel + actualización geolocalizada

### Lo que funcionó (v2.4)
- **4 pestañas nuevas:** Polen, Inundaciones, Suelo, Pronóstico 7 días
- **Clima mejorado:** +6 KPIs (presión, nubosidad, visibilidad, ráfagas, prob. lluvia, precipitación)
- **Paro INE por CCAA:** Tabla 4247 → gráfico barras coloreadas por tasa (rojo >15%, naranja >10%, verde <10%)
- **Todas las nuevas pestañas se geolocalizan:** Click provincia → fetch por centroides
- **Total: 17 pestañas, 30+ gráficos, 12+ APIs en tiempo real**

### Lo que funcionó (v2.5) — Rediseño layout
- **Pestañas horizontales superiores:** Tabs en `#tab-navbar` scrollable horizontal arriba del mapa
- **Pronóstico fusionado en Clima:** 7 días de forecast integrados en pestaña Clima (cards + gráficos)
- **Capas de mapa:** Carreteras (OpenStreetMap HOT) + Ferrocarriles (OpenRailwayMap) vía Leaflet layer control
- **Tipografía compacta:** KPIs 14-17px, títulos 12px, body 10-11px
- **Error handling mejorado:** setTxt() helper + showToast en errores + fallback values
- **16 pestañas totales** (Pronóstico quitado como pestaña separada)

### Lo que funcionó (v2.6) — Calidad y funcionalidad
- **Transporte/DGT eliminado:** API rota, datos estáticos inútiles. David: "no aporta información"
- **Choropleth toggleable:** Capa de provincias y parques nacionales activables desde layer control
- **Ambiente mejorado:** 16 parques nacionales con coordenadas reales, flyTo en mapa, markers verdes
- **Catastro mejorado:** Superficie, densidad, municipios, enlace directo por provincia
- **Inundaciones mejorado:** 52 ríos mapeados a provincias, nombre del río en gráfico y KPI
- **Puertos mejorado:** flyTo en mapa al hacer click, datos en vivo (oleaje, viento, temp)
- **Clima fix:** `fetchProvinceWeather()` arreglado — sunrise/sunset movidos a daily parameters
- **Total: 15 pestañas, 30+ gráficos, 12+ APIs en tiempo real**

### Patrón de cards que SÍ gusta a David
```css
.kpi {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 14px 16px;
    transition: all 0.2s ease;
}
.kpi:hover {
    background: #ffffff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transform: translateY(-1px);
}
.kpi.green { background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%); }
.kpi.orange { background: linear-gradient(135deg, #fff7ed 0%, #ffffff 100%); }
.kpi.red { background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%); }
.kpi.blue { background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%); }
```

### GeoJSON fuentes
- **Provincias**: `codeforamerica/click_that_hood` → 52 features, ~1.4MB raw, ~487KB simplificado
- **Municipios**: `AlexGPlay/SpainLayers` → por provincia (28, 29, 41, 46 disponibles)
- **Propiedades**: `{cod, nombre, ccaa}` (provincias), `{id, name}` (municipios — OJO: mapear)

### GitHub Pages deployment
- Workflow requiere `enablement: true` en `actions/configure-pages@v5`
- Sin esto, el paso "Setup Pages" falla con "Get Pages site failed"
- Token necesita scope `pages: write` + `id-token: write`

## Prompts cron para capas adicionales

### Cron: Actualización Energía (cada hora)
```
Actualiza la capa de energía del DataHub España.
1. Fetch ESIOS API: PVPC (indicator 1001), Demanda (1293), Renovables (1294)
2. Actualizar KPI tiles en index.html
3. Actualizar gráfico PVPC 24h
4. Git commit + push
Nota: ESIOS puede necesitar token. Fallback: mostrar "N/D"
```

### Cron: Actualización Clima (cada 6h)
```
Actualiza datos climáticos del DataHub España.
1. Fetch Open-Meteo para Madrid (40.4168, -3.7038): temperatura, viento, humedad
2. Actualizar KPI tiles de clima
3. Actualizar descripción del código meteorológico WMO
4. Git commit + push
```

### Cron: Actualización Embalses (diario)
```
Actualiza niveles de embalses del DataHub España.
1. Leer data/embalses.json (datos estáticos por cuenca)
2. Actualizar KPI tiles: nivel medio, volumen, alertas
3. Actualizar gráfico de barras por cuenca
4. Git commit + push
```

### Cron: Actualización Sísmica (cada 12h)
```
Actualiza datos sísmicos del DataHub España.
1. Fetch IGN API: últimos terremotos 30 días
2. Actualizar "Último terremoto" en panel principal
3. Nota: API IGN puede dar CORS error desde Pages → usar fallback
4. Git commit + push
```
