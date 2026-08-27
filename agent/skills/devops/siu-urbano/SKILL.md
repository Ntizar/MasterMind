---
name: siu-urbano
description: SIU (Sistema de Información Urbana) — datos gráficos de suelo urbanístico de España. Clases de suelo, recintos, sectores, CORINE Land Cover, SIOSE. SHP descargable + WMS/WFS en vivo. Nacional, 5.898 municipios.
version: "1.0.0"
tags: [urbanismo, suelo, SHP, WMS, WFS, CORINE, SIOSE, MITMA, datos-gob-es, IDEE]
---

# SIU — Sistema de Información Urbana

## Qué es

El **Sistema de Información Urbana (SIU)** es un sistema público de información urbanística del **Ministerio de Vivienda y Agenda Urbana** (MITMA). Cubre **5.898 municipios** (98,61% población española) y el 100% de áreas urbanas.

**Cobertura: TODO ESPAÑA** — Cantabria, Madrid, Asturias, todas las CCAA. Datos unificados y comparables.

Fuente: https://datos.gob.es/es/catalogo/e05233601-siu-datos-graficos

## Descarga directa (SHP)

| Archivo | Tamaño | Fecha | URL |
|---------|--------|-------|-----|
| Clases de suelo | 286 MB | 2025-12-02 | `https://cdn.mivau.gob.es/portal-web-mivau/urbanismo-suelo/CLASES_SUELO_20251202.zip` |
| Recintos | 44 MB | 2025-12-02 | `https://cdn.mivau.gob.es/portal-web-mivau/urbanismo-suelo/RECINTOS_20251202.zip` |
| Sectores | 42 MB | 2025-12-02 | `https://cdn.mivau.gob.es/portal-web-mivau/urbanismo-suelo/SECTORES_20251202.zip` |
| Datos alfanuméricos (Excel) | 6 MB | 2026-06-19 | `https://cdn.mivau.gob.es/portal-web-mivau/urbanismo-suelo/Datos%20alfanumericos%20SIU%20-%20Excel%20-%2020260619.zip` |

**Total: ~378 MB** de Shapefiles.

## Servicios web (live, sin descarga)

### WMS (visualización)

**Base URL:**
```
https://mapas.fomento.gob.es/arcgis/services/SIU/Servicios_OGC/MapServer/WMSServer
```

**Capas disponibles:**

| Capa WMS | Descripción |
|----------|-------------|
| `OGC_Clases_Suelo` | Clases de suelo urbanístico |
| `OGC_Recintos` | Recintos de planeamiento |
| `OGC_Sectores` | Sectores de desarrollo |
| `OGC_Areas_Urbanas` | Áreas urbanas |
| `OGC_CORINE_2018` | Corine Land Cover 2018 |
| `OGC_CORINE_2012` | Corine Land Cover 2012 |
| `OGC_CORINE_2006` | Corine Land Cover 2006 |
| `OGC_CORINE_2000` | Corine Land Cover 2000 |
| `OGC_CORINE_1990` | Corine Land Cover 1990 |
| `OGC_CORINE_Variacion_2012_2018` | Variación CORINE 2012-2018 |
| `OGC_CORINE_Variacion_2006_2012` | Variación CORINE 2006-2012 |
| `OGC_CORINE_Variacion_2000_2006` | Variación CORINE 2000-2006 |
| `OGC_CORINE_Variacion_1990_2000` | Variación CORINE 1990-2000 |
| `OGC_SIOSE_2014` | SIOSE 2014 |
| `OGC_SIOSE_2011` | SIOSE 2011 |
| `OGC_SIOSE_2009` | SIOSE 2009 |
| `OGC_SIOSE_2005` | SIOSE 2005 |

**CRS:** EPSG:25830 (ETRS89 / UTM zona 30N)

**Ejemplo GetMap (Cantabria):**
```url
https://mapas.fomento.gob.es/arcgis/services/SIU/Servicios_OGC/MapServer/WMSServer?service=wms&version=1.3.0&request=GetMap&layers=OGC_Clases_Suelo&styles=&bbox=550000,4750000,600000,4800000&crs=EPSG:25830&width=512&height=512&format=image/png&transparent=true
```

**BBOX de referencia por comunidad (EPSG:25830):**
- Cantabria: `530000,4740000,620000,4810000`
- Madrid: `440000,4440000,520000,4550000`
- Asturias: `470000,4730000,580000,4820000`
- País Vasco: `490000,4720000,600000,4830000`
- Galicia: `500000,4650000,640000,4830000`
- Cataluña: `460000,4540000,620000,4720000`

### WFS (descarga vectorial)

**Base URL:**
```
https://mapas.fomento.gob.es/arcgis/services/SIU/Servicios_OGC/MapServer/WFSServer
```

**Capas WFS:** Mismas que WMS pero con prefijo `Servicios_OGC:`:
- `Servicios_OGC:OGC_Clases_Suelo`
- `Servicios_OGC:OGC_Recintos`
- `Servicios_OGC:OGC_Sectores`
- `Servicios_OGC:OGC_Areas_Urbanas`
- `Servicios_OGC:OGC_CORINE_*`
- `Servicios_OGC:OGC_SIOSE_*`

**Ejemplo GetFeature (Cantabria, primeros 100 features):**
```url
https://mapas.fomento.gob.es/arcgis/services/SIU/Servicios_OGC/MapServer/WFSServer?service=wfs&version=2.0.0&request=GetFeature&typeNames=Servicios_OGC:OGC_Clases_Suelo&count=100&outputFormat=application/json&srsName=EPSG:25830&BBOX=530000,4740000,620000,4810000,EPSG:25830
```

### Visor cartográfico (web)

```
https://mapas.fomento.gob.es/VisorSIU/
```

Acceso libre y gratuito. Responsive (funciona en móvil). Manual: https://www.mivau.gob.es/recursos_mfom/comodin/recursos/2020-04-20_tutorialvisor.pdf

## Datos alfanuméricos

El Excel descargable contiene información tabular de:
- Clases de suelo por municipio
- Superficies por categoría
- Grados de desarrollo
- Áreas de desarrollo urbanístico

## Uso con Leaflet

```javascript
// Capa WMS de clases de suelo
L.tileLayer.wms('https://mapas.fomento.gob.es/arcgis/services/SIU/Servicios_OGC/MapServer/WMSServer', {
    layers: 'OGC_Clases_Suelo',
    format: 'image/png',
    transparent: true,
    crs: L.CRS.EPSG25830,
    version: '1.3.0'
}).addTo(map);

// Capa WMS de CORINE 2018
L.tileLayer.wms('https://mapas.fomento.gob.es/arcgis/services/SIU/Servicios_OGC/MapServer/WMSServer', {
    layers: 'OGC_CORINE_2018',
    format: 'image/png',
    transparent: true,
    crs: L.CRS.EPSG25830
}).addTo(map);

// Capa WMS de sectores
L.tileLayer.wms('https://mapas.fomento.gob.es/arcgis/services/SIU/Servicios_OGC/MapServer/WMSServer', {
    layers: 'OGC_Sectores',
    format: 'image/png',
    transparent: true,
    crs: L.CRS.EPSG25830
}).addTo(map);
```

## Uso con fetch (WFS → GeoJSON)

```javascript
async function fetchSIULayer(layer, bbox) {
    const url = `https://mapas.fomento.gob.es/arcgis/services/SIU/Servicios_OGC/MapServer/WFSServer?service=wfs&version=2.0.0&request=GetFeature&typeNames=Servicios_OGC:${layer}&count=500&outputFormat=application/json&srsName=EPSG:25830&BBOX=${bbox},EPSG:25830`;
    const res = await fetch(url);
    return await res.json();
}

// Cantabria: bbox=530000,4740000,620000,4810000
const data = await fetchSIULayer('OGC_Clases_Suelo', '530000,4740000,620000,4810000');
```

## Convenios autonómicos

El SIU tiene convenios con: **Aragón, Asturias, Cantabria, Castilla y León, Castilla-La Mancha, Extremadura, Galicia, Madrid, Murcia y País Vasco**. Estas CCAA tienen datos más detallados.

## Pitfalls

1. **CRS:** Todos los datos están en **EPSG:25830** (ETRS89/UTM30N), NO en WGS84. Al usar Leaflet con `L.CRS.EPSG25830`, instalar `proj4leaflet` o usar `L.Proj`.
2. **WFS límite:** Por defecto devuelve max 1000 features. Usar `count=500` y paginación con `startIndex=0,500,1000...`.
3. **ZIPs grandes:** CLASES_SUELO.zip es 286 MB. Descargar solo si necesitas análisis offline. Para visualización, usar WMS.
4. **WMS vs SHP:** WMS es instantáneo pero solo imagen. SHP permite queries pero pesado. WFS es el intermedio (vectorial, filtrable).
5. **SIOSE vs CLC:** SIOSE es más detallado pero solo hasta 2014. CORINE(CLC) tiene datos hasta 2018 pero menos resolución.
6. **Datos alfanuméricos:** El Excel es pequeño (6 MB) y contiene las tablas de atributos sin geometría.

## Fuentes relacionadas

- **Visor SIU:** https://mapas.fomento.gob.es/VisorSIU/
- **Portal MITMA:** https://www.mivau.gob.es/urbanismo-y-suelo/suelo/sistema-de-informacion-urbana
- **IDEE (Infraestructura de Datos Espaciales):** https://www.idee.es/
- **Sectores Residenciales 2025:** https://publicaciones.transportes.gob.es/downloadcustom/sample/3970
