# HTML Report Generation — Informes profesionales 60-80 páginas

## El patrón

Generar informes HTML completos (60-80 páginas impresas) a partir de datos de `appState`. El informe se crea como un string HTML enorme con CSS embebido, se renderiza en un `iframe` o `document.write()`, y se exporta a PDF vía html2canvas + jsPDF.

## Arquitectura típica

```
report.js (3000-4000 líneas)
├── generarInformeCompleto(appState) → string HTML
│   ├── CSS embebido (A4 print, headers, tablas, KPIs)
│   ├── Portada con logo y metadata
│   ├── Índice automático
│   ├── Capítulos (20-25) con page-break-before
│   └── Footer con paginación
├── helpers por capítulo (uno por función)
└── utils (safe access, formateo)
```

## El HTML del informe — patrón base

```javascript
export function generarInformeCompleto(app) {
    return `<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PMST — ${safe(app, 'centro', {}).nombre || 'Centro'}</title>
    <style>${CSS_INFORME}</style>
</head>
<body>
    ${generarPortada(app)}
    ${generarIndice(app)}
    ${generarCapitulo1_ResumenEjecutivo(app)}
    ${generarCapitulo2_MarcoLegal(app)}
    ...
</body>
</html>`;
}
```

## CSS embebido para print

```javascript
const CSS_INFORME = `
    @page { size: A4; margin: 2cm; }
    body { font-family: 'Segoe UI', sans-serif; font-size: 11pt; line-height: 1.5; }
    .chapter { page-break-before: always; margin-top: 40px; }
    .chapter:first-child { page-break-before: avoid; }
    h1 { color: #1e40af; font-size: 22pt; border-bottom: 3px solid #f97316; padding-bottom: 8px; }
    h2 { color: #1e40af; font-size: 16pt; margin-top: 24px; }
    table { width: 100%; border-collapse: collapse; margin: 16px 0; }
    th { background: #2563eb; color: white; padding: 10px 12px; }
    td { padding: 8px 12px; border-bottom: 1px solid #e5e7eb; }
    .kpi-card { display: inline-block; background: #dbeafe; padding: 8px 16px; border-radius: 6px; }
    .kpi-value { font-size: 20pt; font-weight: 800; color: #1e40af; }
    .cover { text-align: center; padding: 120px 40px; }
    .cover h1 { font-size: 32pt; border: none; }
`;
```

## Helper safe access (anti-crash)

```javascript
function safe(obj, path, fallback = 'N/D') {
    try { return path.split('.').reduce((o, k) => o?.[k], obj) ?? fallback; }
    catch { return fallback; }
}
```

## Exportación a PDF

```javascript
import { generarInformeCompleto } from './report.js';

export async function exportPDF() {
    const app = window.pmstApp.appState;
    const html = generarInformeCompleto(app);

    // Renderizar en iframe oculto
    const iframe = document.createElement('iframe');
    iframe.style.cssText = 'position:fixed;top:-9999px;width:794px;height:1123px';
    document.body.appendChild(iframe);
    iframe.contentDocument.open();
    iframe.contentDocument.write(html);
    iframe.contentDocument.close();
    await new Promise(r => setTimeout(r, 1500));

    // html2canvas → jsPDF
    const canvas = await html2canvas(iframe.contentDocument.body, { scale: 2 });
    const pdf = new jspdf.jsPDF('p', 'mm', 'a4');
    // ... paginación y descarga
    document.body.removeChild(iframe);
}
```

## 22 capítulos típicos de un PMST (Ley 8/2021)

1. Portada → 2. Índice → 3. Resumen Ejecutivo → 4. Marco Legal → 5. Metodología → 6. Análisis del Entorno (isocronas, NAP, GBFS) → 7. Caracterización Centro → 8. Caracterización Empresa → 9. Resultados Encuesta → 10. Reparto Modal → 11. Distancias/Tiempos → 12. Huella Carbono (MITECO 2024) → 13. Aparcamiento → 14. Transporte Público (NAP DGT) → 15. Infraestructura Ciclista (GBFS) → 16. DAFO → 17. Objetivos SMART → 18. Plan de Medidas → 19. Cronograma → 20. Presupuesto → 21. Seguimiento (KPIs multi-año) → 22. Conclusiones

## Estimación de páginas

- **3000 chars/página** como regla general (A4, 11pt, 1.5 line-height)
- 160KB HTML ≈ 55-60 páginas impresas
- Tablas grandes consumen más espacio; page breaks añaden saltos

## Mapas en informes — tiles IGN para proyectos españoles

Para proyectos de movilidad/gobierno en España, **usar tiles del IGN** (Instituto Geográfico Nacional) en vez de OpenStreetMap:

```javascript
// IGN WMTS — capa topográfica gris (recomendada para data viz)
const IGN_GRIS = 'https://www.ign.es/wmts/ign-base?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=IGNBase-gris&STYLE=default&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX={z}&TILECOL={x}&TILEROW={y}&FORMAT=image/jpeg';
const IGN_ATTR = '© IGN — Instituto Geográfico Nacional (CC BY 4.0)';

L.tileLayer(IGN_GRIS, { attribution: IGN_ATTR, maxZoom: 19 }).addTo(map);
```

Capas disponibles: `IGNBase-gris` (dato), `IGNBaseTodo` (colores), `IGNBaseOrto` (fotos aéreas). **Obligatorio:** `FORMAT=image/jpeg` si no devuelve 400.

## Layout de mapas — anti-rompe-estructura

Los mapas Leaflet pueden romper el layout del informe. Siempre:

```css
.map-container {
    height: 450px;
    max-height: 450px;
    overflow: hidden;
    page-break-inside: avoid;    /* PDF: no cortar a mitad */
    break-inside: avoid;
    border-radius: 12px;
    border: 2px solid #e5e7eb;
    margin: 16px 0;
    position: relative;
}
.map-container .leaflet-container {
    height: 100% !important;
    width: 100% !important;
}
```

## Isócronas realistas (no círculos)

Las isócronas de círculo no representan la realidad. Generar polígonos tipo "mano de pulpo" con:
- **Ejes viales** con factores de extensión (ej: Castellana N factor 1.4)
- **Barreras urbanas** con factores de contracción (ej: río -40%, vía tren -25%)
- **Transporte público** que extiende la isócrona (ej: metro L9 +25%)
- **48 puntos** de resolución por polígono
- **Fórmula:** radio × factor_eje × factor_barrera × variación

Ver `isochrones-realistas.js` en PLANDEMOVILIDAD.

## Pipeline PDF con mapas

WeasyPrint no ejecuta JS → mapas vacíos. Pipeline completo:

```python
# 1. Generar HTML con mapas Leaflet
html = generarInformeCompleto(app)

# 2. Generar imágenes estáticas con staticmap (Python)
from staticmap import StaticMap, Marker, CircleMarker
m = StaticMap(800, 600, url_template='https://www.ign.es/wmts/ign-base?...')
# Añadir markers, polígonos de isócronas...
image = m.render()
image.save('mapas/entorno.png')

# 3. Convertir a JPEG comprimido
from PIL import Image
img = Image.open('mapas/entorno.png').convert('RGB')
img.save('mapas/entorno.jpg', 'JPEG', quality=85)

# 4. Embeber como base64 en el HTML
import base64
with open('mapas/entorno.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
html = html.replace('<div id="map-entorno">', f'<img src="data:image/jpeg;base64,{b64}" style="width:100%;height:450px;object-fit:cover">')

# 5. Generar PDF con WeasyPrint
from weasyprint import HTML
HTML(string=html).write_pdf('informe.pdf')
```

## Comentarios IA después de mapas

Añadir análisis contextual después de cada mapa con estilo visual diferenciado:

```html
<div style="background:#f0f9ff;border-left:4px solid #2563eb;padding:14px 18px;border-radius:0 8px 8px 0;margin:16px 0;font-size:14px">
    <div style="font-size:13px;font-weight:700;color:#1e40af;margin-bottom:6px">🤖 Análisis IA — [Nombre del mapa]</div>
    <p><strong>[Hallazgo clave con datos]:</strong> [Explicación]</p>
    <p><strong>[Recomendación]:</strong> [Acción concreta]</p>
</div>
```

Colores por tipo: azul `#f0f9ff` = entorno/isócronas, verde `#f0fdf4` = transporte, amarillo `#fefce8` = general.

## HTML auto-contenido (file:// compatible)

Si el informe se va a abrir directamente (sin servidor), NO usar `<script type="module">`:

```html
<!-- ❌ NO — falla sin servidor -->
<script type="module">
    import { init } from './js/map.js';
</script>

<!-- ✅ SÍ — funciona con file:// -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
    // Todo el código inline, sin imports
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(initMaps, 800);
    });
</script>
```

## Pitfalls

- **No llamar `buildSummary()` recursivamente** — OOM en NaN builders (2GB RAM)
- **CSS embebido > CSS externo** — el informe es string HTML standalone
- **`page-break-before: always`** en cada capítulo — sin esto el PDF sale sin saltos
- **`iframe` para render** — no usar `document.write()` directamente porque destruye la app
- **`var charts = window.charts = {}`** — NO `const` para charts en inline scripts (TDZ)
- **⚠️ WeasyPrint no ejecuta JS → mapas vacíos en PDF:** Usar pipeline estático descrito arriba.
- **IGN: `FORMAT=image/jpeg` obligatorio** — si no, devuelve 400.
- **IGN: `IGNBaseSimplificado` y `IGNBaseTodo-nofondo` fallan en algunos zooms** — usar solo `IGNBase-gris`, `IGNBaseTodo` o `IGNBaseOrto`.
- **No duplicar archivos de informe** — mantener solo `informe_preview.html` (con mapas interactivos). El `informe_estatico.html` se genera bajo demanda para PDF.

## Referencia de sesión

- Proyecto: PLANDEMOVILIDAD v2.0
- Archivo: `js/report.js` (3850 líneas, 22 capítulos)
- Output: ~186KB HTML, ~71 páginas, 31 tablas, 3 mapas IGN
- PDF: WeasyPrint + staticmap + JPEG base64
