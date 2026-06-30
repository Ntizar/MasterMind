# Time v5.0 — Patrones de Arquitectura Nuevos

## Nuevos módulos creados en la evolución TimeIneco → Time

### layers.js — Sistema de Capas Toggleables
- Cada capa es un `L.layerGroup()` independiente
- Toggle ON/OFF individual por capa
- Renderizado dinámico del panel de capas en sidebar
- Capas: isócronas (5 modos), GTFS (paradas + líneas), GBFS, radio 500m, CP
- API: `initLayers(mapa)`, `toggleCapa(id)`, `renderPanelCapas()`, `getLayerGroup(id)`

### csv-export.js — CSV Completo
- Estructura: `seccion,categoria,indicador,valor,unidad,fuente,anio_fuente,fecha_generacion`
- Secciones: resumen, isocrona, transporte, bici, costes, co2
- BOM UTF-8 (`\uFEFF`) para Excel
- `descargarArchivo(nombre, contenido, tipoMime)` — helper genérico
- `generarCSV(resultados, punto, modos, tiempos, gtfsData, biciData, transporteCercano)` — generador principal

### interpretaciones.js — Interpretaciones Automáticas
- Genera texto narrativo profesional a partir de datos calculados
- 7 secciones: accesibilidad, transporte público, bicicletas, costes, CO₂, demografía, recomendaciones
- `generarInterpretaciones(...)` → objeto con todas las secciones
- Comparativas automáticas entre modos
- Recomendaciones concretas basadas en umbrales

### config.js — Config Centralizada
- Kaizen colors: `#1A4488` (azul), `#CB1823` (rojo)
- IGN config: URLs WMTS, capas, atribución, maxZoom
- Modos de transporte con perfiles ORS, velocidades, colores
- `CONFIG.IGN.tileUrl(capa)` → genera URL WMTS completa

## Patrón de integración de nuevos features

1. Crear módulo JS independiente (`js/nombre.js`)
2. Importar en `index.html` antes de `main.js`
3. Exportar API pública via `window.ModuleName` o import estático
4. Integrar en `main.js` en el flujo de inicialización
5. Añadir botón/panel en `index.html` sidebar
6. Añadir interpretación en `interpretaciones.js`
7. Añadir datos al CSV export
8. Añadir sección al DOCX si aplica

## Colores de modos de transporte (v5.0)

| Modo | Color | Hex |
|------|-------|-----|
| 🚗 Coche | Azul Kaizen | `#1A4488` |
| 🚌 Bus | Púrpura | `#a855f7` |
| 🚇 Metro | Rojo Kaizen | `#CB1823` |
| 🚲 Bici | Naranja | `#f97316` |
| 🚶 Andando | Verde | `#22c55e` |
