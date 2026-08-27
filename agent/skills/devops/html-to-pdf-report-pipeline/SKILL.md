---
name: html-to-pdf-report-pipeline
version: "1.0.0"
description: >
  Pipeline completo para generar informes PDF profesionales desde HTML/JS vanilla:
  generación en browser, transferencia a disco, conversión con weasyprint,
  manejo de charts/maps como imágenes estáticas. Patrón para dashboards que
  necesitan exportar a PDF sin Puppeteer/Chromium.
tags: [pdf, html, weasyprint, reports, pipeline, browser, charts, maps]
---

# HTML→PDF Report Pipeline — Informes profesionales sin Puppeteer

## Resumen

Pipeline para generar informes PDF de 60+ páginas desde aplicaciones web vanilla JS.
Cubre: generación HTML en browser → rasterización de charts/maps → transferencia a disco → conversión PDF con weasyprint.

| Fase | Herramienta | Output |
|------|-------------|--------|
| Generación HTML | `generarInformeCompleto()` en browser | HTML 160KB+, 22 capítulos |
| Rasterización charts | `canvas.toDataURL()` | PNG embebido en HTML |
| Rasterización maps | `html2canvas` o `exportMapAsImage()` | PNG embebido en HTML |
| Transferencia | HTTP receiver o base64 chunks | HTML en disco |
| Conversión PDF | `weasyprint input.html output.pdf` | PDF A4 profesional |

## Arquitectura del pipeline

```
Browser (generarInformeCompleto)
    │
    ├── Canvas charts → toDataURL() → <img> embebido
    ├── Leaflet maps → html2canvas → <img> embebido
    └── HTML enriquecido (164KB+)
           │
           ├── [Opción A] HTTP receiver POST → disco
           ├── [Opción B] Base64 chunks → disco
           └── [Opción C] Node.js directo (si no usa DOM)
                  │
                  ▼
            weasyprint input.html output.pdf
                  │
                  ▼
            PDF A4 profesional (60+ págs)
```

## Decision Guide

```
¿El informe usa Canvas/Leaflet/JS?
├── NO → Generar con Node.js directo (sin browser)
│        └── weasyprint directo
│
├── SÍ → ¿Tienes Puppeteer/Chromium?
│   ├── SÍ → Puppeteer (mejor fidelidad)
│   └── NO → weasyprint (limitaciones conocidas)
│       ├── Rasterizar charts como PNG primero
│       ├── Rasterizar maps como PNG primero
│       └── weasyprint con @page CSS
│
└── ¿Necesitas transferir HTML del browser al disco?
    ├── <50KB → base64 chunks (1-2 rounds)
    ├── 50-200KB → HTTP receiver (recomendado)
    └── >200KB → Node.js directo (evitar transferencia)
```

## Fase 1: Generación HTML en browser

```js
// En browser, tras cargar datos y sincronizar appState
const { generarInformeCompleto } = await import('./js/report.js');
const html = generarInformeCompleto(appState);
window.__fullReport = html;
console.log(`HTML generado: ${Math.round(html.length/1024)}KB`);
```

**Pitfall:** `generarInformeCompleto()` puede fallar silenciosamente si `appState` tiene datos incompletos. Verificar antes:
```js
const app = window.pmstApp.appState;
console.assert(app.diagnostico, 'Falta diagnostico');
console.assert(app.medidas?.length > 0, 'Falta medidas');
```

## Fase 2: Rasterización de charts (Canvas→PNG)

```js
// Convertir todos los canvas a imágenes ANTES de exportar
document.querySelectorAll('canvas').forEach(c => {
    const img = document.createElement('img');
    img.src = c.toDataURL('image/png');
    img.style.width = c.style.width || '100%';
    img.style.height = c.style.height || 'auto';
    c.parentNode.replaceChild(img, c);
});
```

**Pitfall:** Los charts de Chart.js usan `devicePixelRatio` para nitidez. `toDataURL()` preserva la resolución original.

## Fase 3: Rasterización de maps (Leaflet→PNG)

```js
// Opción 1: html2canvas (si está disponible)
const mapEl = document.getElementById('map');
const canvas = await html2canvas(mapEl);
const img = document.createElement('img');
img.src = canvas.toDataURL();
mapEl.parentNode.replaceChild(img, mapEl);

// Opción 2: exportMapAsImage() del proyecto (usa html2canvas lazy-loaded)
await exportMapAsImage('map-container', 'mapa.png');
```

**Pitfall:** Leaflet necesita que el mapa esté renderizado y visible para capturar. Si el mapa está en un tab oculto, renderizarlo primero.

## Fase 4: Transferencia Browser→Disco

Ver `references/browser-to-pdf-patterns.md` en skill `vanilla-js-dashboard-patterns` para los 3 patrones detallados.

**Resumen rápido:**
- <50KB: base64 chunks
- 50-200KB: HTTP receiver (recomendado)
- >200KB: Node.js directo

## Fase 5: Conversión con weasyprint

```bash
weasyprint input.html output.pdf
```

### CSS esencial para A4

```css
@page {
    size: A4;
    margin: 25mm 20mm 30mm 20mm;
    @bottom-center {
        content: "PLAN DE MOVILIDAD — Hecho con ❤️ por David Antizar";
        font-size: 8pt;
        color: #666;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    @bottom-right {
        content: counter(page);
        font-size: 8pt;
        color: #666;
    }
}

@media print {
    body { margin: 0; padding: 0; }
    .no-print { display: none !important; }
    .page-break { page-break-before: always; }
    h1, h2, h3, h4 { page-break-after: avoid; }
    table, figure { page-break-inside: avoid; }
    p { orphans: 3; widows: 3; }
}
```

### Embebido de fonts (paraweasyprint)

```css
@font-face {
    font-family: 'MiFont';
    src: url('fonts/mifont.woff2') format('woff2');
}
```

Si las fonts no están embebidas, weasyprint usa fallback del sistema.

## Limitaciones de weasyprint

| Feature | Soporte | Workaround |
|---------|---------|------------|
| HTML/CSS layout | ✅ | — |
| Tablas | ✅ | — |
| CSS @page | ✅ | — |
| Imágenes base64 | ✅ | — |
| Canvas2D charts | ❌ | Exportar como PNG primero |
| Leaflet maps | ❌ | Rasterizar con html2canvas |
| JavaScript | ❌ | Ejecutar JS antes, embebido resultado |
| Web fonts | ⚠️ | Embebidas en CSS @font-face |
| CSS Grid | ⚠️ | Usar Flexbox o tablas como fallback |
| CSS custom props | ⠼ | Resolver antes de exportar |

## Pitfalls críticos

1. **weasyprint NO ejecuta JavaScript** — todo contenido dinámico debe estar resuelto en el HTML estático ANTES de la conversión
2. **Canvas vacío en PDF** — los `<canvas>` se renderizan como cuadros blancos. SIEMPRE rasterizar antes.
3. **Maps vacíos en PDF** — Leaflet no carga tiles en weasyprint. SIEMPRE usar imagen estática.
4. **Tamaño del PDF** — Un HTML de 164KB con imágenes base64 puede generar un PDF de 1-5MB. Normal para docs de 60+ págs.
5. **@page margins** — weasyprint respeta @page pero los márgenes se aplican a CADA página. Incluir márgenes en el CSS del body también.
6. **Tabla grande sin page-break-inside: avoid** — Las tablas largas se rompen en medio de una fila. Usar `page-break-inside: avoid` o `avoid-column`.

## Verificación del output

```bash
# Tamaño mínimo esperado para doc profesional
ls -la output.pdf
# Debe ser >500KB para 60+ págs con imágenes

# Conteo de páginas (si tienes PyMuPDF)
python3 -c "import fitz; print(fitz.open('output.pdf').page_count)"

# Verificar que no está vacío
python3 -c "
import fitz
doc = fitz.open('output.pdf')
for i in range(min(3, doc.page_count)):
    text = doc[i].get_text()[:200]
    print(f'Pág {i+1}: {text[:100]}...')
"
```

## Alternativa: Puppeteer (si está disponible)

Si Chromium/Puppeteer está instalado, es MEJOR que weasyprint:
- Renderiza JavaScript completo
- Charts y maps se renderizan nativamente
- Mejor soporte CSS moderno
- PDF con vectorial real (no rasterizado)

```bash
# Instalar Puppeteer
npm install puppeteer

# Script de conversión
node -e "
const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('file:///path/to/report.html', {waitUntil: 'networkidle0'});
    await page.pdf({path: 'output.pdf', format: 'A4', printBackground: true});
    await browser.close();
})();
"
```

## Seguridad: remover API proxy de repos públicos

**PITFALL CRÍTICO:** Si tu repo es público (GitHub Pages, etc.), **nunca incluyas un proxy de API** en el código fuente. Exponer `server.mjs` o similar en un repo público revela infraestructura interna.

**Checklist de limpieza:**
1. Buscar cualquier archivo de servidor (`server.mjs`, `server.js`, `proxy.mjs`)
2. Buscar referencias a URLs internas (`nan.builders`, `localhost`, IPs privadas)
3. Si el repo es público → eliminar el proxy, mover a CI/CD o infraestructura separada
4. API keys → solo en `localStorage` del usuario, nunca en código

**Lección de PLANDEMOVILIDAD:** Un proxy Node.js (`server.mjs`) que exponía `api.nan.builders/v1` fue eliminado del repo público. La solución: eliminar proxy, usar fallback estático en `informe.js`, y dejar que la IA se conecte directamente desde el navegador del usuario (sin proxy).

## Referencias

- `references/browser-to-pdf-patterns.md` — Transferencia browser→disco detallada
- `references/plandemovilidad-pdf-pipeline.md` — Métricas reales, casos de estudio (report.js vs ia-generativa), seguridad API proxy
- Skill `vanilla-js-dashboard-patterns` — Patrones de arquitectura dashboard vanilla JS
- Skill `pdf-processing` — Extracción y procesamiento de PDFs (dirección opuesta)
