# Export Multi-Formato v2.2 — SHP + GeoJSON + CSV + KML

## Formatos

### Campos DBF enriquecidos (8)
MODO, MINUTOS, AREA_KM2, TIPO_REAL, COLOR, POBLACION, RENTA_MEDIA, PRECIO_M2

### GeoJSON FeatureCollection
Propiedades: modo, minutos, area_km2, tipo_real, color, poblacion, renta_media, precio_m2

### CSV resumen
modo;minutos;area_km2;poblacion;renta_media;precio_m2

### KML con estilos
Colores KML: `#RRGGBB` → `ffBBGGRR` (KML usa AABBGGRR)

## API
```javascript
exportarGeoJSON(resultados)  // FeatureCollection
exportarCSV(resultados)       // CSV tabla
exportarTodo(resultados, punto) // ZIP batch
```

## Integración UI
```javascript
document.getElementById('btnGeoJSON').addEventListener('click', () => exportarGeoJSON(state.resultados));
document.getElementById('btnExportarTodo').addEventListener('click', () => exportarTodo(state.resultados, state.punto));
```

## Pitfalls
- `exportarTodo()` requiere `window.JSZip`
- Si `demograficos` no se cargó, usar 0 para poblacion/renta/precio
- Multi-SHP: records comparten BBox global, cada uno tiene BBox local
