# Export Shapefile v2.2 — Campos Enriquecidos + Multi-Formato Batch

**Fecha:** 2026-06-22
**Archivo:** `js/shp.js` (TimeIneco2)

## Resumen

Se mejoró el sistema de exportación SIG de TimeIneco con:
1. **8 campos en el DBF** (antes 5): se añadieron POBLACION, RENTA_MEDIA, PRECIO_M2
2. **Shapefile multi-registro**: un único SHP con todos los modos/tiempos
3. **Nuevos formatos**: exportarGeoJSON(), exportarCSV(), exportarTodo()
4. **KML con estilos** por modo de transporte
5. **Batch ZIP**: un solo archivo con los 4 formatos

## Campos DBF enriquecidos

| Campo | Tipo | Long | Dec | Descripción |
|-------|------|------|-----|-------------|
| MODO | C | 10 | 0 | Modo de transporte (ej: "Coche") |
| MINUTOS | N | 3 | 0 | Tiempo en minutos |
| AREA_KM2 | N | 10 | 2 | Área en km² |
| TIPO_REAL | C | 10 | 0 | "ORS" o "Simulado" |
| COLOR | C | 7 | 0 | Hex color (#RRGGBB) |
| POBLACION | N | 8 | 0 | Población dentro de la isócrona |
| RENTA_MEDIA | N | 8 | 2 | Renta media per cápita |
| PRECIO_M2 | N | 6 | 2 | Precio medio m² vivienda |

Cálculo del DBF:
- Header: `32 + 8*32 + 1 = 289 bytes`
- Record: `1 + 10+3+10+10+7+8+8+6 = 63 bytes`
- Total: `289 + N * 63`

## Funciones exportadas

```javascript
// GeoJSON individual (una isócrona)
downloadGeoJSON(modo, minutos, geojson)

// GeoJSON todas las isocronas (descarga directa)
exportarGeoJSON(resultados)  // FeatureCollection con propiedades enriquecidas

// CSV tabla resumen (descarga directa)
exportarCSV(resultados)  // modo;minutos;area_km2;poblacion;renta_media;precio_m2

// Shapefile individual (ZIP)
downloadSHP(modo, minutos, geojson)

// Batch: GeoJSON + CSV + SHP multi-registro + KML en un ZIP
exportarTodo(resultados, punto)
```

## Shapefile Multi-Registro

### buildMultiSHP(records)
Construye un .shp con N polígonos (uno por isócrona).
- Header con BBox global de todos los registros
- Cada registro: ShapeType=5, BBox local, coordenadas
- Endianness: header BIG-ENDIAN, content LITTLE-ENDIAN

### buildMultiSHX(records)
Index con N entradas. Cada entrada: offset (palabras 16-bit) + content length.

### buildMultiDBF(records)
DBF con 8 campos y N registros. Usa writeString() para padding.

### buildMultiKML(resultados)
KML con <Placemark> por isócrona, <Style> por modo.
Colores: `#RRGGBB` → `ffBBGGRR` (KML usa AABBGGRR).

## Datos demográficos

Las funciones de export leen de `r.demograficos`:
- `poblacion` → POBLACION en DBF / poblacion en GeoJSON
- `rentaMedia` → RENTA_MEDIA en DBF / renta_media en GeoJSON
- `precioM2` → PRECIO_M2 en DBF / precio_m2 en GeoJSON

Estos datos vienen de `demographics.js` (cargados en main.js).

## Integración UI (index.html)

```html
<button id="btnExportarTodo">📦 Exportar TODO (SHP+GeoJSON+CSV+KML)</button>
<button id="btnGeoJSON">🌐 GeoJSON</button>
<button id="btnCSV">📊 CSV</button>
<button id="btnSHPAll">🗺️ SHP (todos los modos)</button>
```

En main.js:
```javascript
document.getElementById('btnGeoJSON').addEventListener('click', () => {
  if (state.resultados) exportarGeoJSON(state.resultados);
});
document.getElementById('btnCSV').addEventListener('click', () => {
  if (state.resultados) exportarCSV(state.resultados);
});
document.getElementById('btnExportarTodo').addEventListener('click', () => {
  if (state.resultados && state.punto) exportarTodo(state.resultados, state.punto);
});
```

## Pitfalls

- **JSZip**: `exportarTodo()` requiere `window.JSZip`. Si no está disponible (dashboard.html no lo carga), muestra alert.
- **Demographics null**: Si `demograficos` no se cargó (ej: dashboard.html sin server), las exportaciones usan 0 para poblacion/renta/precio.
- **Nombre del ZIP**: Se basa en `punto.display_name` sanitizado. Si no hay punto, usa "export".
- **Multi-SHP**: Los records comparten el mismo BBox global en el header. Cada record tiene su propio BBox local.