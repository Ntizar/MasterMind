# Preferencias de David — Diseño de Dashboards

## Anti-patrones (NUNCA hacer)

### 1. ❌ Liquid glass genérico
- backdrop-filter masivo en cada card → se ve "como de IA"
- Gradientes translúcidos en cada elemento → ruido visual
- **Correcto:** fondo blanco limpio (#f8fafc), cards sólidas con sombra sutil (0 2px 8px rgba(0,0,0,0.06)), color solo en borders y badges

### 2. ❌ Circle markers para choropleth geográfico
- David: "los cp en vez de puntos deberían ser áreas"
- Para datos geográficos SIEMPRE polígonos reales (GeoJSON/TopoJSON)
- Referencia de oro: EspañaAtlas (espanatlas.es) — 8.132 municipios con choropleth real + Canvas renderer
- Canvas renderer obligatorio para >500 polígonos

### 3. ❌ Dark theme para datos públicos
- David odia fondos oscuros y colores neón
- **Correcto:** fondo blanco/gris claro (#f8fafc), texto oscuro (#1e293b), acentos en borders

### 4. ❌ Cards "de IA"
- Cards con gradientes de color en cada una → genérico
- Iconos grandes sin contexto → confuso
- Números sin explicar qué miden → inútil
- `border-left: 4px solid #color` → "se nota mucho que es IA" (David, 2026-06-30)
- **Correcto:** KPI tiles limpios con fondo blanco, gradientes sutiles de fondo, hover elevación, sin border-left

### 5. ❌ Datos inventados o aproximados
- David verifica manualmente cada dato del mapa
- Nunca inventar coordenadas, valores, ni nombres
- Si la API falla: mostrar "N/D" o "—", nunca fake data

## Patrones correctos

### Choropleth
- Polígonos reales (GeoJSON/TopoJSON), nunca approximations
- Canvas renderer para >500 features (Leaflet: `preferCanvas: true, renderer: L.canvas()`)
- TopoJSON para compresión (~70% menos que GeoJSON)
- Lazy loading de datasets temáticos
- Pane system para z-index controlado

### Layout
- Mapa como estrella: 70%+ del viewport
- Sidebar colapsable con datos/controles
- Click provincia → zoom + panel detalle con datos locales (clima, población, etc.)
- Footer: "Hecho con ❤️ por David Antizar"

### Datos
- APIs públicas reales: ESIOS/REE, Open-Meteo, IGN, DGT, BOE/BORME, embalses
- Fallback graceful: si API falla → "N/D", nunca inventar
- Timestamps de actualización visibles

### Chart.js
- Limpio, sin过多 decoración
- Etiquetas claras
- Colores consistentes con la paleta del dashboard
- Responsive

## Referencia visual: EspañaAtlas
- Fondo dark navío (para contrastar con David's preference de fondo claro)
- Choropleth interactivo con Canvas
- Sidebar colapsable con rankings, correlaciones, índices
- Búsqueda con autocompletado
- URL state para compartir vistas
