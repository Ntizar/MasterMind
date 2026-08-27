---
name: ai-report-generation
version: "1.0.0"
description: "Generación de informes y documentos profesionales mediante LLM. Arquitectura prompt→LLM→HTML capítulo, plantillas por sección, integración con datos de appState, y patrón demo interactivo. Aplicable a PMST, informes técnicos, auditorías, y cualquier documento estructurado."
tags: [ai, llm, report, document-generation, prompt-engineering, html, templates]
related_skills: [software-development, frontend-dashboard-patterns, educational-html-pipeline]
---

# AI Report Generation — Generación de Informes con IA

## Resumen

Patrón para generar documentos profesionales de 50-80+ páginas mediante LLM, donde cada capítulo se construye individualmente con un prompt estructurado que inyecta datos reales de la aplicación.

## Arquitectura

```
appState (datos reales)
    ↓
Normalización (JSON por capítulo)
    ↓
Prompt Template (system + datos + instrucciones + formato)
    ↓
LLM (qwen/gpt/claude via API)
    ↓
HTML Chapter (sección del informe)
    ↓
CSS Print (A4, page-break, headers)
    ↓
Documento Final (PDF/HTML descargable)
```

## Flujo por Capítulo

### 1. Definir datos de entrada por capítulo

Cada capítulo necesita datos específicos de `appState`:

| Capítulo | Datos necesarios |
|----------|-----------------|
| Resumen Ejecutivo | centro, diagnostico, comparativas, medidas |
| Análisis Entorno | centro (coords), transportePublico, isocronas |
| Resultados Encuesta | encuesta (departments, modes, distances) |
| Huella Carbono | diagnostico.huellaCO2e, MITECO factors |
| Transporte Público | transportePublico (from NAP DGT API) |
| DAFO | dafo (fortalezas, debilidades, oportunidades, amenazas) |
| Medidas | medidas (from DAFO derivation) |
| Conclusiones | ALL (synthesis) |

### 2. Construir prompt por capítulo

```javascript
function buildPrompt(chapterId, appState) {
    const data = extractChapterData(chapterId, appState);
    return `
Eres un consultor de movilidad sostenible redactando el capítulo "${chapterId}"
de un PMST conforme a la Ley 8/2021 de Movilidad Sostenible.

DATOS DEL CENTRO:
${JSON.stringify(data.centro, null, 2)}

DATOS DEL DIAGNÓSTICO:
${JSON.stringify(data.diagnostico, null, 2)}

INSTRUCCIONES:
1. Redacta entre 400-800 palabras
2. Incluye tablas con datos reales (no genéricos)
3. Menciona cifras específicas del centro
4. Tono: profesional pero accesible para dirección general
5. Formato: HTML con h3, tablas, listas, KPIs inline

FORMATO DE SALIDA: Solo HTML, sin markdown fences.
`;
}
```

### 3. Generar y capturar respuesta

```javascript
async function generateChapter(chapterId, appState) {
    const prompt = buildPrompt(chapterId, appState);
    const response = await fetch(LLM_ENDPOINT, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${API_KEY}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
            model: 'qwen3-6',
            messages: [{ role: 'user', content: prompt }],
            max_tokens: 4096
        })
    });
    const data = await response.json();
    return data.choices[0].message.content;
}
```

### 4. Ensamblar informe final

```javascript
async function generateFullReport(appState) {
    const chapters = [];
    for (const ch of CHAPTER_ORDER) {
        const html = await generateChapter(ch.id, appState);
        chapters.push(`<section class="chapter" id="${ch.id}">${html}</section>`);
    }
    return wrapInHTMLDocument(chapters.join('\n'), getCSS());
}
```

## Prompt Engineering para Informes

### Estructura de prompt efectiva

1. **Role assignment**: "Eres un consultor de [dominio]..."
2. **Context**: Tipo de documento, normativa aplicable
3. **Data injection**: JSON con datos reales (NO placeholders)
4. **Constraints**: Extensión, tono, formato de salida
5. **Negative instructions**: "NO uses jerga técnica sin explicar", "NO inventes datos"
6. **Output format**: HTML tags específicos esperados

### Prompt por tipo de capítulo

| Tipo | Enfoque | Extensión |
|------|---------|-----------|
| Resumen Ejecutivo | Síntesis + KPIs + prioridades | 400-600 palabras |
| Análisis Técnico | Datos + tablas + interpretación | 600-1000 palabras |
| Marco Legal | Referencia normativa + obligaciones | 300-500 palabras |
| Estratégico (DAFO) | Matriz + estrategias derivadas | 400-600 palabras |
| Plan de Acción | Medidas priorizadas + cronograma | 500-800 palabras |
| Conclusiones | Síntesis + compromisos + hoja de ruta | 300-500 palabras |

## CSS Print para Informes

```css
@page { size: A4; margin: 2cm; }
.chapter { page-break-before: always; }
.chapter:first-child { page-break-before: avoid; }
h2 { color: #1e40af; border-bottom: 2px solid #2563eb; padding-bottom: 8px; }
table { width: 100%; border-collapse: collapse; margin: 16px 0; }
th { background: #2563eb; color: white; padding: 10px; }
td { padding: 8px 10px; border-bottom: 1px solid #e5e7eb; }
.kpi-inline { background: #dbeafe; padding: 2px 8px; border-radius: 4px; font-weight: 700; }
```

### Generación PDF con WeasyPrint + staticmap

WeasyPrint **no ejecuta JavaScript**, así que los mapas Leaflet se renderizan como cuadros vacíos en el PDF. Solución: generar imágenes estáticas con la librería Python `staticmap` y reemplazar los divs de mapa por `<img>`.

**Pipeline completo:**
```
1. report.js genera HTML con mapas Leaflet interactivos
2. Abre HTML en navegador para que Leaflet renderice (opcional, solo para preview)
3. gen_static_maps.py genera PNG/JPG estáticos con staticmap
4. gen_pdf_static.py reemplaza divs de mapa por <img> con base64
5. WeasyPrint genera el PDF con imágenes estáticas
```

**Paso 3 — Generar mapas estáticos:**
```python
# gen_static_maps.py
import staticmap

def generar_mapa_estatico(center, paradas, gbfs, isocronas, output_path):
    m = staticmap.StaticMap(800, 600, url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')
    
    # Añadir paradas TP (círculos rojos)
    for p in paradas:
        marker = staticmap.CircleMarker((p['lon'], p['lat']), '#dc2626', 8)
        m.add_marker(marker)
    
    # Añadir estaciones BiciMAD (verde/amarillo/rojo por disponibilidad)
    for s in gbfs:
        color = '#16a34a' if s['bikes'] > 5 else '#eab308' if s['bikes'] > 0 else '#dc2626'
        m.add_marker(staticmap.CircleMarker((s['lon'], s['lat']), color, 10))
    
    # Añadir isócronas (polígonos semitransparentes)
    for iso in isocronas:
        m.add_polygon(iso['coords'], fill=iso['color'], outline=iso['color'], width=2)
    
    # Añadir etiqueta del centro
    m.add_text((center[0], center[1]), '🏢 Centro', 24, '#1e40af', 'bold')
    
    image = m.render()
    image.save(output_path)
```

**Paso 4 — Reemplazar mapas en HTML y generar PDF:**
```python
# gen_pdf_static.py
import base64, re
from weasyprint import HTML

def reemplazar_mapas(html_content, mapas_dir):
    for map_id, img_file in [('map-entorno', 'entorno.jpg'), ('map-tp', 'tp.jpg'), ('map-isocronas', 'isocronas.jpg')]:
        with open(f'{mapas_dir}/{img_file}', 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        # Reemplazar div de mapa por imagen
        html_content = re.sub(
            f'<div id="{map_id}".*?</div>',
            f'<img src="data:image/jpeg;base64,{b64}" style="width:100%;border-radius:12px">',
            html_content, flags=re.DOTALL
        )
    return html_content

html = HTML(string=html_modified)
html.write_pdf('PMST_Ineco_Paseo_Habana.pdf')
```

**Instalación:**
```bash
pip install --break-system-packages weasyprint staticmap Pillow PyPDF2
```

**Resolución de mapas:** 800×600px genera JPG de 124-158KB. Para mejor calidad, usar 1200×900 (~300KB).

**Ventaja sobre html2canvas:** `staticmap` genera mapas directamente desde tiles de OpenStreetMap sin necesidad de navegador. Es más rápido, reproducible, y funciona en servidores sin GUI.

## Patrón Demo Interactivo

Para presentar el sistema al usuario, crear un HTML demo que muestre:
1. **Diagrama de arquitectura**: Encuestas → APIs → Normalización → LLM → HTML
2. **Tabla de fuentes de datos**: Qué datos alimenta cada capítulo
3. **Ejemplos por capítulo**: Sidebar con navegación, prompt box (dark, syntax highlighted), AI response box (green border, formatted HTML)

Ver `references/prompt-templates.md` para ejemplos de prompts por capítulo.
Ver `references/plandemovilidad-case.md` para el caso de estudio completo.

## Integración con APIs Externas

El informe se enriquece con datos de APIs reales **ANTES de la generación**:

```javascript
// Patrón: enrichAppWithAPIs() se llama antes de generarInformeCompleto()
export async function enrichAppWithAPIs(app) {
    const lat = parseFloat(app.centro?.latitud);
    const lng = parseFloat(app.centro?.longitud);
    if (!lat || !lng) return app;
    
    // GBFS → app.gbfs = { sistema, estaciones[], total }
    // Nominatim → app.centroInfo = { ciudad, barrio, cp }, app.pois[]
    // ORS → app.isocronas[] = { modo, minutos, areaKm2, real }
    
    return app;
}

// Wrapper en index.html
window.pmstApp.exportPDF = async () => {
    await enrichAppWithAPIs(window.pmstApp.appState);
    return exportPDF();
};
```

**Dato crítico:** El enriquecimiento debe ocurrir ANTES de que el generador de informe lea `appState`. Si se genera sin enriquecer, los capítulos muestran "datos pendientes" en vez de datos reales.

Fuentes de datos y capítulos que las usan:

| API | Capítulo(s) | Qué aporta |
|-----|-------------|-----------|
| GBFS | 14 (Infraestructura Ciclista) | Estaciones cercanas, disponibilidad bicis |
| Nominatim | 5 (Entorno), 13 (TP) | Dirección del centro, barrio, POIs |
| ORS | 5 (Entorno), 13 (TP) | Isochronas de accesibilidad multi-modo |
| MITECO | 8 (Huella CO₂) | Factores de emisión por modo |

## Isochronas Realistas (sin API externa)

Cuando no hay API key de ORS, generar isócronas simuladas pero **realistas** — no círculos perfectos.

### Algoritmo de polígonos irregulares

```javascript
function generarIsocronaRealista(centro, radioMax, modo, tiempo) {
    const PUNTOS = 48;
    const coords = [];
    
    // Ejes viales de la ciudad (ángulo → factor de extensión)
    const ejes = [
        { angulo: 0,   factor: 1.4, nombre: 'Castellana N' },
        { angulo: 45,  factor: 1.1, nombre: 'Bravo Murillo' },
        { angulo: 90,  factor: 0.7, nombre: 'Río Manzanares' },  // barrera
        { angulo: 180, factor: 1.3, nombre: 'Paseo Habana S' },
        { angulo: 270, factor: 0.8, nombre: 'Zona menos desarrollada' },
    ];
    
    // Barreras urbanas
    const barreras = [
        { anguloInicio: 75, anguloFin: 105, factor: 0.6 },   // río
        { anguloInicio: 260, anguloFin: 285, factor: 0.75 }, // vía tren
    ];
    
    for (let i = 0; i < PUNTOS; i++) {
        const angulo = (i / PUNTOS) * 2 * Math.PI;
        const anguloDeg = (i / PUNTOS) * 360;
        
        // Factor de ejes viales
        let factorEje = 1;
        for (const eje of ejes) {
            const diff = Math.abs(anguloDeg - eje.angulo);
            if (diff < 30) factorEje *= 1 + (eje.factor - 1) * (1 - diff / 30);
        }
        
        // Factor de barreras
        let factorBarrera = 1;
        for (const b of barreras) {
            if (anguloDeg >= b.anguloInicio && anguloDeg <= b.anguloFin) {
                factorBarrera *= b.factor;
            }
        }
        
        // Variación natural (senoide con 3 frecuencias)
        const variacion = 1 + 0.15 * Math.sin(angulo * 0.1) + 0.1 * Math.cos(angulo * 0.23);
        
        const radio = radioMax * factorEje * factorBarrera * variacion;
        
        // Convertir a coordenadas
        const lat = centro.lat + (radio / 111320) * Math.cos(angulo);
        const lon = centro.lon + (radio / (111320 * Math.cos(centro.lat * Math.PI / 180))) * Math.sin(angulo);
        coords.push([lat, lon]);
    }
    
    return coords;
}
```

**Velocidad por modo:** coche 25 km/h, bici 14 km/h, pie 4.5 km/h.

**Resultado:** Polígonos tipo "mano de pulpo" que se extienden por ejes viales principales y se contraen en barreras urbanas. 48 puntos de resolución por polígono.

## Comentarios IA después de visualizaciones

En informes largos (60-80 páginas), después de cada mapa, gráfico o tabla importante, incluir un bloque de análisis de la IA que:

1. **Interpreta los datos** — "El análisis revela que en 15 min se cubren 150-200 km² en coche..."
2. **Identifica barreras** — "La barrera del río reduce accesibilidad al SE un 40%..."
3. **Da recomendaciones** — "Se recomienda fomentar Metro L9 y líneas 14/27..."

```html
<div class="ai-analysis" style="background:#f0f9ff;border-left:4px solid #2563eb;padding:16px;border-radius:0 8px 8px 0;margin:16px 0">
    <h4>🤖 Análisis contextual de la IA</h4>
    <p><strong>Principales hallazgos:</strong> El análisis revela que en 15 minutos se cubren 150-200 km² en coche...</p>
    <p><strong>Barreras detectadas:</strong> Río Manzanares (-40%), vía tren Chamartín (-25%)...</p>
    <p><strong>Recomendación:</strong> Priorizar conexiones transversales que superen las barreras naturales...</p>
</div>
```

**Patrón de color por tipo de mapa:**
- Isochromas → fondo azul `#f0f9ff`
- Transporte Público → fondo verde `#f0fdf4`
- Entorno → fondo amarillo `#fefce8`

## Pitfalls

1. **Variables no definidas en template literals** — Al generar HTML con backticks, variables como `lat`, `manana`, `turno` pueden no estar declaradas en el scope de la función. Fix: declarar todas las variables al inicio.
2. **LLM genera Markdown en vez de HTML** — El prompt debe especificar explícitamente "formato HTML, NO markdown". Incluir tags de ejemplo.
3. **Respuestas inconsistentes entre capítulos** — Inyectar los mismos datos base en todos los prompts para mantener coherencia.
4. **Tokens excedidos en capítulos grandes** — Dividir capítulos largos en sub-secciones, generar cada una por separado.
5. **Cache de respuestas** — Almacenar respuestas generadas para no re-generar innecesariamente. Invalidar cuando cambien los datos de entrada.
6. **ES modules en HTML estático** — `<script type="module">` e `import()` no funcionan con file:// URLs. Para informes auto-contenidos que se abren directamente, usar `<script>` inline sin `type="module"`. Los mapas Leaflet y cualquier JS interactivo debe estar todo inline.
7. **WeasyPrint no ejecuta JS** — El PDF generado con WeasyPrint no incluye mapas interactivos, gráficos Chart.js, ni elementos dinámicos. Solo renderiza HTML/CSS estático. Para mapas en PDF: capturar como imagen con html2canvas primero.

## Tamaño esperado del informe

**PMST/PTST en España:** 60-80 páginas A4 es lo profesional. Un informe de 10 páginas es un borrador, no un PMST conforme a Ley 8/2021.

| Métrica | Mínimo | Profesional | Ejemplo PLANDEMOVILIDAD |
|---------|--------|-------------|------------------------|
| Páginas PDF | 20 | 60-80 | 71 |
| Capítulos | 10 | 20-22 | 22 |
| Tablas de datos | 10 | 25-35 | 31 |
| Gráficas | 5 | 15-25 | 18 |
| Mapas interactivos | 1 | 3-5 | 3 |
| Tamaño HTML | 50KB | 150-200KB | 164KB |
| Tamaño PDF | 100KB | 500KB-1MB | 117KB (WeasyPrint, sin mapas) |
| Comentarios IA | 0 | 3-6 | 3 |

**Regla:** Si el usuario dice "es muy corto" o "debería ser más largo", el informe necesita más datos reales, más tablas comparativas, más análisis por capítulo, y comentarios de IA después de cada visualización.

## Export HTML-first (patrón PLANDEMOVILIDAD)

El flujo de exportación real es **HTML primero**, PDF como paso secundario:

```
generarInformeCompleto(appState) → string HTML (164KB, 22 capítulos)
    ↓
Download como .html autocontenido (CSS embebido, file:// compatible)
    ↓ (opcional)
WeasyPrint → PDF estático (117KB, sin mapas interactivos)
    ↓ (futuro)
Puppeteer/Chromium → PDF con mapas rasterizados (≈1MB)
```

**Por qué HTML-first:**
- El HTML es autocontenido (CSS + JS inline, sin dependencias externas)
- Se abre directamente con doble-clic (file:// compatible)
- Los mapas Leaflet son interactivos (zoom, pan, capas)
- El PDF pierde interactividad (WeasyPrint no ejecuta JS)

**Tamaños observados (PLANDEMOVILIDAD demo Renfe):**
- HTML: 164KB (22 capítulos, 31 tablas, 3 mapas)
- PDF WeasyPrint: 117KB (10 capítulos, sin mapas)
- PDF Ineco (referencia): 1.2MB (con mapas rasterizados)

**Gap vs PDF profesional:** Para alcanzar la calidad del PDF Ineco (1.2MB con mapas rasterizados), se necesita Puppeteer/Chromium para capturar screenshots de Leaflet antes de la conversión. WeasyPrint es suficiente para borradores y revisión interna.

## Cuándo usar este patrón

- Informes legales/obligatorios que requieren 50+ páginas (PMST, auditorías, EIA)
- Documentos que combinan datos reales + análisis experto
- Generación batch de informes para múltiples centros/empresas
- Prototipado rápido de informes antes de invertir en redacción manual

## Referencias

- **PMST 22 capítulos:** `references/plandemovilidad-chapters.md` — Estructura completa del informe PMST conforme a Ley 8/2021, datos de entrada por capítulo, CSS print A4, generación con LLM
- **Templates de prompt:** `references/prompt-templates.md` — Ejemplos de prompts por tipo de capítulo
- **Caso de estudio:** `references/plandemovilidad-case.md` — Implementación completa en PLANDEMOVILIDAD
