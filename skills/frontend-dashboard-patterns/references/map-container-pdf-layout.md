# Map Containers — Layout Fix para PDF

## Problema

Los mapas Leaflet rompen la estructura del documento cuando se generan PDFs o informes largos. Los contenedores de mapa expanden más allá de su tamaño fijo porque Leaflet fuerza `height: 100%` en sus hijos.

## Solución

CSS obligatorio para mapas en documentos:

```css
.map-container {
    height: 450px;
    max-height: 450px;
    overflow: hidden;           /* ← CRÍTICO: recortar tiles que se desbordan */
    border-radius: 12px;
    border: 2px solid #e5e7eb;
    margin: 16px 0;
    position: relative;
    page-break-inside: avoid;   /* ← CRÍTICO: no partir mapa entre páginas */
    page-break-after: always;   /* ← después del mapa, nueva página */
}

/* Override Leaflet defaults */
.map-container .leaflet-container,
.map-container .leaflet-pane,
.map-container .leaflet-map-pane {
    height: 100% !important;
    width: 100% !important;
}
```

## Verificación

Después de añadir mapas, hacer scroll por el documento y comprobar que:
1. Los mapas no se desbordan del contenedor
2. No hay saltos de página a mitad de mapa
3. El texto después del mapa aparece en la posición correcta

## Ejemplo real

PLANDEMOVILIDAD v2.0 (2026-07-14): 3 mapas Leaflet en informe de 71 páginas. Sin `overflow: hidden`, los mapas se desbordaban y rompían el layout del documento.

## Nota sobre PDF generation

WeasyPrint NO ejecuta JavaScript — los mapas Leaflet no se renderizan en el PDF. Soluciones:
1. **Mapas estáticos**: Usar `staticmap` Python para generar PNG de mapas con tiles
2. **Screenshots del browser**: Capturar cada mapa como imagen y reemplazar divs
3. **IGN WMTS tiles**: Para proyectos españoles, usar tiles del IGN (ver skill `ign-wmts-tiles`)
