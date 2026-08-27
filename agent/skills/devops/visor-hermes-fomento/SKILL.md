---
name: visor-hermes-fomento
version: "1.0.0"
description: >
  Visor Hermes — Visor cartográfico del Ministerio de Transportes (Fomento).
  ArcGIS Web Application con capas de infraestructura de transporte: carreteras,
  ferrocarriles, puertos, aeropuertos, movilidad big data, seguridad, combustibles
  alternativos, TEN-T. Acceso a servicios ArcGIS REST.
---

# Visor Hermes — Ministerio de Transportes

## Qué es

Visor cartográfico interactivo del Ministerio de Transportes y Movilidad Sostenible.
Aplicación ArcGIS Web AppBuilder (WAB v2.29) que muestra la Red de Transporte de
Interés General (RTIG) de España con múltiples capas temáticas.

## URLs

- **Visor principal:** https://mapas.fomento.gob.es/VisorHermes/?locale=es
- **Visor TEN-T:** https://mapas.fomento.gob.es/VisorTENT
- **Portal ArcGIS:** https://mapas.fomento.gob.es/portal
- **Web Map ID:** `4a400eaef6e04680ad4a9020c778a4c7` (HERMES_PUBLICO)

## Capas del visor (ArcGIS REST services)

### Capas base
- **Unidades administrativas** — WMS IGN (`https://www.ign.es/wms-inspire/unidades-administrativas`)
- **Redes de transporte (IGR-RT)** — WMS IDEE (`https://servicios.idee.es/wms-inspire/transportes`)

### Capas temáticas (MapServer)

| # | Capa | URL base |
|---|------|----------|
| 1 | Infraestructura básica | `Hermes/1_INFRAESTRUCTURA_BÁSICA` |
| 2 | Instalaciones y servicios | `Hermes/2_INSTALACIONES_Y_SERVICIOS` |
| 3 | Uso de la red | `Hermes/3_USO_DE_LA_RED` |
| 3.1 | **Movilidad con Big Data** | `BigData/Movilidad_Big_Data_2` |
| 5 | Seguridad | `Hermes/5_SEGURIDAD` |
| 7 | Combustibles alternativos | `Hermes/7_COMBUSTIBLES_ALTERNATIVOS` |
| 8 | Actuaciones planificadas | `Hermes/8_ACTUACIONES_PLANIFICADAS` |

### Capas de infraestructura
- **Ferrocarriles** — `Hermes/0_FERROCARRILES`
- **Carreteras** — `Hermes/0_CARRETERAS`
- **Terminales intermodales** — `Hermes/0_TERMINALES_INTERMODALES`
- **Puertos** — `Hermes/0_PUERTOS`
- **Aeropuertos** — `Hermes/0_AEROPUERTOS`
- **Red transeuropea TEN-T** — `Hermes/NEW_RED_TRANSEUROPEA_DE_TRANSPORTE__TEN_T_2024`

### Capas externas (FeatureServer)
- **Cámaras DGT** — `services1.arcgis.com/.../CamarasDGT`
- **Predicción Meteorológica AEMET** (precipitación/nieve)
- **Avisos meteorológicos AEMET**
- **Estaciones de bus** (IGN BTN POI Transportes)
- **ECLIPSES** — Servicio propio Fomento

## Capa clave: Movilidad Big Data

**URL:** `https://mapas.fomento.gob.es/arcgis2/rest/services/BigData/Movilidad_Big_Data_2/MapServer`

Esta capa consume los datos del OpenData Movilidad MITMA y los publica como servicio ArcGIS.

| ID | Nombre |
|----|--------|
| 1282 | Viajeros_día |
| 1283 | Viajeros_día por distancia viaje |
| 1285 | Carreteras |
| 1289 | Viajes O_D |
| 1290 | Viajes Entradas y Salidas (martes medio) |
| 1291 | Viajes Interiores (martes medio) |
| 1292 | Viajes_OD |

## Cómo consultar capas ArcGIS REST

```bash
# Listar capas de un servicio
curl -sL "https://mapas.fomento.gob.es/arcgis2/rest/services/BigData/Movilidad_Big_Data_2/MapServer?f=json"

# Consultar una capa específica
curl -sL "https://mapas.fomento.gob.es/arcgis2/rest/services/BigData/Movilidad_Big_Data_2/MapServer/1282?f=json"

# Query con filtros
curl -sL "https://mapas.fomento.gob.es/arcgis2/rest/services/BigData/Movilidad_Big_Data_2/MapServer/1282/query?where=1=1&outFields=*&f=json&resultRecordCount=10"
```

## Widgets del visor

- Leyenda, Galería de mapas base, Medición
- **Consultas y filtros** (Query widget)
- Dibujo, Añadir datos, Descarga de servicios
- Imprimir, Tabla de atributos
- Búsqueda, Coordenadas, Barra de escala

## Relación con otros datos

- **OpenData Movilidad MITMA** → Fuente de datos de la capa BigData
  - `opendata-movilidad-mitma` skill
- **NAP DGT** → Datos de tráfico tiempo real (paneles, incidencias, radares)
  - `nap-dgt` skill
- **ESIOS/REE** → Datos energéticos
  - `esios-complete` skill

## Nota

Guardado 2026-06-30. El visor es una aplicación de escritorio, no tiene API REST propia,
pero sus servicios ArcGIS subyacentes son consultables directamente.
La capa de Movilidad BigData es el puente entre los datos MITMA y la visualización cartográfica.
