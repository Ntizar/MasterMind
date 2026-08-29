# CIAF Dashboard v2.0 — Patrón de Dashboard Interactivo

## Resumen

Patrón para construir un dashboard interactivo responsive desde datos estructurados (YAML+Markdown) sin backend. Los datos se incrustan inline en el JS para que funcione standalone en GitHub Pages.

## Arquitectura

```
index.html          ← Estructura HTML + CSS inline (14KB)
js/app.js           ← Lógica + datos incrustados (90KB para 38 informes)
data/reports.json   ← Índice estructurado (78KB)
informes/           ← Archivos Markdown individuales
pdfs/              ← PDFs originales
```

### Patrón de datos inline

GitHub Pages **no sirve archivos .json** vía URL. Solución: incrustar los datos directamente en el JS:

```javascript
// En build script:
const reports_json = JSON.stringify(data.reports, null, 2);
// Insertar en template JS
js = js.replace('const CIAF_DATA = []', `const CIAF_DATA = ${reports_json}`);
```

## Estructura HTML (v2)

### Layout de 3 columnas
1. **Sidebar izquierda** (360px) — Lista de informes con filtros
2. **Centro** — Mapa Leaflet (flex:1, ocupa espacio restante)
3. **Sidebar derecha** (480px) — Panel de detalle con tabs

### HTML estructura
```html
<header class="ciaf-header"> <!-- KPIs: total informes, años, accidentes --> </header>
<div class="filters-bar"> <!-- Filtros: año, tipo, búsqueda libre --> </div>
<div class="main-layout">
  <aside class="sidebar"> <!-- Lista de informes --> </aside>
  <main class="map-container"> <div id="map"></div> </main>
  <aside class="details-panel"> <!-- Panel detalle con tabs --> </aside>
</div>
<footer class="ciaf-footer"> </footer>
```

## CSS Responsive

### Variables CSS
```css
:root {
  --primary: #1e3a5f;
  --primary-light: #2563eb;
  --accent: #f97316;
  --danger: #dc2626;
  --warning: #f59e0b;
  --success: #10b981;
}
```

### Breakpoints
- **>1200px**: 3 columnas (sidebar 360px, mapa flex, detalle 480px)
- **900-1200px**: 3 columnas pero más estrechas
- **600-900px**: Stack vertical (lista arriba, mapa 400px, detalle expandible)
- **<600px**: Todo stack, filtros en columna

### Clases clave
```css
.main-layout { display: flex; height: calc(100vh - 150px); }
.sidebar { width: 360px; border-right: 1px solid #e5e7eb; }
.map-container { flex: 1; }
.details-panel { width: 480px; border-left: 1px solid #e5e7eb; }
@media (max-width: 900px) { .main-layout { flex-direction: column; } }
```

## JS: Tabs para detalle

4 tabs en el panel de detalle:
1. **📋 Resumen** — Fecha, hora, estación, tipo, gravedad, resumen texto, tags
2. **🎯 Conclusiones** — Lista numerada de conclusiones
3. **💡 Recomendaciones** — Lista numerada de recomendaciones
4. **📊 Datos** — Víctimas, horas, daños, coordenadas, trenes, entidades

```javascript
function buildDetailHTML(r) {
    return `
        <div class="tabs">
            <button class="tab-btn active" onclick="activateTab('tab-resumen')">📋 Resumen</button>
            <button class="tab-btn" onclick="activateTab('tab-conclusiones')">🎯 Conclusiones</button>
            <button class="tab-btn" onclick="activateTab('tab-recomendaciones')">💡 Recomendaciones</button>
            <button class="tab-btn" onclick="activateTab('tab-datos')">📊 Datos</button>
        </div>
        <div class="tab-content active" id="tab-resumen"> ... </div>
        <div class="tab-content" id="tab-conclusiones"> ... </div>
        ...
    `;
}
```

## Mapa con marcadores

```javascript
// Color por gravedad
let color = '#2563eb'; // azul = menor
if (report.victimas > 0) color = '#dc2626'; // rojo = grave
else if (report.gravedad === 'moderado') color = '#f59e0b'; // amarillo

const marker = L.circleMarker([r.lat, r.lng], {
    radius: report.victimas > 0 ? 10 : 6,
    fillColor: color, color: '#fff', weight: 2, fillOpacity: 0.8
});
```

## Filtros

Tres filtros combinables:
1. **Año** — Select con todos los años disponibles
2. **Tipo** — accidente / incidente
3. **Búsqueda libre** — Busca en ID, estación, tags

```javascript
filteredReports = CIAF_DATA.reports.filter(r => {
    const matchYear = year === 'all' || String(r.año) === year;
    const matchType = type === 'all' || r.tipo === type;
    const matchSearch = !search || r.id.includes(search) || r.estacion.includes(search) || r.tags.some(t => t.includes(search));
    return matchYear && matchType && matchSearch;
});
```

## Datos incrustados en HTML

### Opción A: JS inline (recomendado)
```javascript
const CIAF_DATA = { /* JSON completo */ };
```

### Opción B: HTML data attribute
```html
<script id="data-source" type="application/json">
{ /* JSON */ }
</script>
<script>
const CIAF_DATA = JSON.parse(document.getElementById('data-source').textContent);
</script>
```

## Estilo visual

- **Colores**: Azul `#1e3a5f` primario, naranja `#f97316` acento
- **Tipografía**: Segoe UI, system-ui, sans-serif
- **Sombras**: `box-shadow: 0 1px 3px rgba(0,0,0,0.1)`
- **Border radius**: 6-8px para cards
- **Sin frameworks**: CSS puro, vanilla JS, Leaflet + Chart.js vía CDN

## Pitfalls

- **GitHub Pages no sirve .json** → Incrustar datos inline en JS
- **Tamaño archivo JS grande** (90KB+ para 38 informes) → Funciona pero verificar carga en móvil
- **Leaflet no inicializa si #map no existe** → Verificar que el div está en el DOM
- **Eventos de tabs** → Usar `onclick="activateTab('tab-id')"` inline para simplificar
- **Caracteres especiales en JS** → `ensure_ascii=False` en Python + JSON dump
