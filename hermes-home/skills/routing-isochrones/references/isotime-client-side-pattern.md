# ISOTime — Patrón de Isocronas Client-Side-Only

**Repo:** `github.com/Ntizar/ISOTime` (público)
**Live:** `ntizar.github.io/ISOTime/`
**Creado:** 2026-06-30

## Arquitectura

100% client-side, sin servidor. HTML + ES modules + Leaflet + ORS API v2.

```
index.html
├── css/style.css          # UI limpia: header #2563eb, sidebar blanca
├── js/
│   ├── config.js          # ORS profiles, IGN WMTS URL, constants
│   ├── map.js             # Leaflet + IGN tiles + simulation + rendering
│   ├── isochrones.js      # ORS API directa + fallback simulación
│   ├── geocoding.js       # Nominatim search + debounce
│   ├── export.js          # GeoJSON + binary SHP/SHX/DBF/PRJ via JSZip
│   └── main.js            # Orquestador: events, state, UI flow
└── .github/workflows/pages.yml  # Build type: workflow
```

## Stack

| Componente | Tecnología |
|---|---|
| Mapa | Leaflet + IGN WMTS (EPSG:3857) |
| Isocronas | ORS API v2 (directo desde fetch) |
| Geocoding | Nominatim (sin key) |
| Export GeoJSON | Native Blob + download |
| Export SHP | Binary construction + JSZip |
| CSS | Vanilla, sin framework |
| JS | ES modules, sin bundler |

## Tiles IGN (alternativa a CARTO)

IGN provee tiles WMTS gratuitos para España:

```javascript
// Configuración en config.js
const IGN_WMTS = {
  url: 'https://www.ign.es/wmts/ign-base?service=wmts',
  layer: 'IGNBaseTodo',
  format: 'image/png',
  crs: 'EPSG:3857',
  attribution: '© IGN'
};

// En map.js
L.tileLayer.wms(IGN_WSTS.url, {
  layers: IGN_WMTS.layer,
  format: IGN_WMTS.format,
  crs: L.CRS.EPSG3857,
  attribution: IGN_WMTS.attribution,
  maxZoom: 19
}).addTo(map);
```

## Key Management

- User introduces ORS API key via modal首次
- Stored in `localStorage.setItem('ors_api_key', key)`
- Read on each request: `localStorage.getItem('ors_api_key')`
- If missing: fallback to simulation mode (no error, just simulated polygons)
- Key visible in DevTools (acceptable for free-tier personal use)

## SHP Binary Generation (in-browser)

Pattern for generating shapefile components without any library:

1. **SHP file**: 100-byte file header (big-endian) + record headers + polygon geometry
2. **SHX file**: spatial index (record headers only, 8 bytes each)
3. **DBF file**: dBASE III header + field descriptors + record data
4. **PRJ file**: WGS84 projection string (text file)

All four files packaged into a ZIP via JSZip for download.

Key values:
- Shape type: 5 (Polygon)
- Byte order: Little-endian for all numeric fields
- DBF encoding: CP850 (0x08)
- Records start at file offset 50 (SHP) or 33 (DBF)

## Simulation Fallback

When no API key is present, generates visually plausible isochrone polygons:

- 48 vertices with sinusoidal jitter (frequency 7.3, amplitude 12%)
- Area calculated via shoelace formula with latitude correction: `111.32² × cos(lat)`
- Speed profiles: car 50 km/h, walk 5 km/h, bike 15 km/h

## Responsive Design

- Desktop: sidebar izquierda fija + mapa
- Mobile (<768px): sidebar → bottom sheet, mapa full-width
- Search bar always visible
- Bottom action bar: "Export GeoJSON" + "Export SHP"

## Pitfalls (ISOTime-specific)

1. **IGN WMTS CORS**: Tiles servidos con CORS abierto, funciona sin proxy
2. **ORS direct-from-browser**: CORS habilitado por ORS. La key se ve en Network tab — aceptable para free-tier
3. **SHP binary**: No hay librería CDN que genere .shp. Hay que construir el binario byte a byte
4. **ES modules cache**: Añadir `?v=N` a imports para development. En Pages, el CDN cachea 2-5 min
5. **Leaflet + EPSG:3857**: IGN tiles funcionan con CRS estándar, no necesita transformación especial
