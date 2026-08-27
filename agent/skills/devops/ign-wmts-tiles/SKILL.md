---
name: ign-wmts-tiles
description: >-
  Mapas base del IGN (Instituto Geográfico Nacional) vía WMTS para Leaflet/MapLibre.
  Capas gratuitas CC BY 4.0: topográfica, gris, ortofoto. Incluye Catastro (WMS, sin tiles).
version: "1.0.0"
tags: [maps, leaflet, ign, spain, wmts, tiles, catastro, open-data]
related_skills: [leaflet-canvas-choropleth, satellite-gis-patterns]
---

# IGN WMTS Tiles — Mapas base de España

## Descripción

El **Instituto Geográfico Nacional (IGN)** ofrece un servicio WMTS gratuito con mapas base de toda España. Licencia **CC BY 4.0** — solo requiere atribución. Ideal como alternativa a OpenStreetMap/CARTO para proyectos de transporte, cartografía o datos geoespaciales en España.

## Servicio WMTS del IGN

**URL base:** `https://www.ign.es/wmts/ign-base`

### Capas disponibles

| Capa | Descripción | Uso recomendado |
|------|-------------|-----------------|
| `IGNBase-gris` | Mapa topográfico en escala de grises | **Recomendado para datos** — fondos que no compiten con capas de datos |
| `IGNBaseTodo` | Mapa topográfico completo (colores) | Navegación general, apps de consumo |
| `IGNBaseOrto` | Ortofotografía (foto aérea) | Verificación visual, análisis territorial |
| `IGNBaseSimplificado` | Versión simplificada | ⚠️ Puede devolver 400 en algunos zooms |
| `IGNBaseTodo-nofondo` | Sin fondo | ⚠️ Puede devolver 400 en algunos zooms |

### Parámetros del servicio

- **TileMatrixSet:** `GoogleMapsCompatible` (EPSG:3857) — compatible con Leaflet/MapLibre
- **Formato:** `image/jpeg` (requerido, si no se pone devuelve 400)
- **Zoom máximo:** 19
- **Coordenadas:** TMS invertido (y normal de Leaflet)

## Código Leaflet

### Capa individual (mínimo)

```javascript
L.tileLayer('https://www.ign.es/wmts/ign-base?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=IGNBase-gris&STYLE=default&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX={z}&TILECOL={x}&TILEROW={y}&FORMAT=image/jpeg', {
    attribution: '© IGN — Instituto Geográfico Nacional (CC BY 4.0)',
    maxZoom: 19
}).addTo(map);
```

### Selector de capas (multi-capas)

```javascript
const ignGris = L.tileLayer('https://www.ign.es/wmts/ign-base?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=IGNBase-gris&STYLE=default&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX={z}&TILECOL={x}&TILEROW={y}&FORMAT=image/jpeg', {
    attribution: '© IGN — Instituto Geográfico Nacional (CC BY 4.0)',
    maxZoom: 19
});
const ignTopo = L.tileLayer('https://www.ign.es/wmts/ign-base?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=IGNBaseTodo&STYLE=default&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX={z}&TILECOL={x}&TILEROW={y}&FORMAT=image/jpeg', {
    attribution: '© IGN — Instituto Geográfico Nacional (CC BY 4.0)',
    maxZoom: 19
});
const cartoLight = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap © CARTO',
    maxZoom: 19,
    subdomains: 'abcd'
});

ignGris.addTo(map);
L.control.layers({
    'IGN Gris (recomendado)': ignGris,
    'IGN Topográfica': ignTopo,
    'CARTO Light': cartoLight
}, null, { position: 'topright' }).addTo(map);
```

### MapLibre GL JS

```javascript
map.addSource('ign', {
    type: 'raster',
    tiles: ['https://www.ign.es/wmts/ign-base?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=IGNBase-gris&STYLE=default&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX={z}&TILECOL={x}&TILEROW={y}&FORMAT=image/jpeg'],
    tileSize: 256,
    attribution: '© IGN — Instituto Geográfico Nacional (CC BY 4.0)'
});
map.addLayer({ id: 'ign-layer', type: 'raster', source: 'ign' });
```

## Licencia y condiciones

### IGN WMTS ✅

- **Licencia:** CC BY 4.0 (Creative Commons Attribution 4.0)
- **Condiciones:** "No se aplican condiciones"
- **Atribución obligatoria:** `© IGN — Instituto Geográfico Nacional`
- **Fuente:** Sistema Cartográfico Nacional de España (scne.es)
- **Uso permitido:** Libre, comercial y no comercial, con atribución

### Catastro WMS ⚠️

- **URL:** `https://ovc.catastro.meh.es/Cartografia/WMS/ServidorWMS.aspx`
- **Licencia:** Acceso gratuito
- **RESTRICCIÓN IMPORTANTE:** "Se prohibe la descarga masiva de porciones de cartografía y **peticiones teseladas**"
- **Uso:** Solo consultas puntuales de parcelas. **NO sirve como mapa base con tiles**
- **Categoría:** No es cartografía oficial, no usar para certificados

### OpenStreetMap (para comparar)

- **Licencia:** ODbL (Open Database License)
- **Uso:** Libre, con atribución yShareAlike
- **CARTO tiles:** Servicio gratuito de CARTO, mismas condiciones ODbL

## Pitfalls

1. **FORMAT=image/jpeg es OBLIGATORIO** — si no se pone, el servicio devuelve error 400. No usar `image/png`.
2. **No todas las capas funcionan** — `IGNBaseSimplificado` y `IGNBaseTodo-nofondo` devuelven 400 en algunos tile coordinates. Usar solo `IGNBase-gris`, `IGNBaseTodo` o `IGNBaseOrto`.
3. **El Catastro NO sirve para tiles** — aunque es WMS gratuito, prohíbe explícitamente "peticiones teseladas". No intentar usarlo como basemap.
4. **Rate limiting** — el IGN puede limitar peticiones si se abusa. En producción, considerar caché de tiles.
5. **Attribution** — la licencia CC BY 4.0 requiere atribución. Siempre incluir `attribution: '© IGN — Instituto Geográfico Nacional (CC BY 4.0)'` en el tile layer.

## Verificación del servicio

Para comprobar que el servicio funciona:

```bash
# Test tile
curl -s -o /tmp/test.jpg "https://www.ign.es/wmts/ign-base?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=IGNBase-gris&STYLE=default&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX=6&TILECOL=32&TILEROW=23&FORMAT=image/jpeg"

# Debe devolver imagen JPEG (~10KB)
file /tmp/test.jpg  # JPEG image data
```

## Referencias

- IGN WMTS: https://www.ign.es/wmts/ign-base
- Capacidades WMTS: https://www.ign.es/wmts/ign-base?SERVICE=WMTS&REQUEST=GetCapabilities
- Sistema Cartográfico Nacional: https://www.scne.es
- Catastro WMS: https://ovc.catastro.meh.es/Cartografia/WMS/ServidorWMS.aspx
- Licencia CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
