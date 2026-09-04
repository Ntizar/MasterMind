---
name: browser-local-tools
description: >
  Herramientas HTML que funcionan 100% en el navegador sin instalación.
  Patrón para crear tools locales con drag-drop, extracción de texto
  (mammoth.js para Word, pdf.js para PDF), normalización y comparación.
  Incluye pitfalls de PDF.js Worker y normalización de documentos legales.
version: "1.0.0"
tags: [html, javascript, browser, local-tools, zero-install, pdfjs, mammoth]
triggers:
  - "herramienta local"
  - "sin instalar nada"
  - "comparar documentos"
  - "procesar PDF en navegador"
  - "procesar Word en navegador"
  - "herramienta HTML"
  - "sin Python"
  - "error con Python"
  - "exe"
  - "fácil de usar"
  - "visor de transporte"
  - "mapa con paradas"
  - "buscar paradas cercanas"
  - "GTFS a HTML"
  - "datos geoespaciales en navegador"
  - "VJ processor"
  - "visuales en vivo"
  - "detección de cuerpo"
  - "MediaPipe"
  - "webcam effects"
  - "real-time visuals"
  - "audio reactive"
---

# Browser Local Tools — Herramientas HTML que funcionan en local

## Cuándo usar esta skill

Cuando el usuario necesita una herramienta de procesamiento que funcione **sin instalación** — sin Python, sin .exe, sin servidor. Se resuelve con un archivo `.html` que se abre en el navegador y usa JavaScript para procesar archivos.

**Señales clave del usuario:**
- "no me deja Python" / "da error con Python"
- "¿no puedes hacerlo más fácil?"
- "algo que se abra con doble clic"
- "sin instalar nada"
- Necesita procesar documentos Word/PDF/Imágenes de forma aislada

## Arquitectura típica

```
archivo.html (SOLO para uso personal en tu PC)
├── CDN libs (mammoth.js, pdf.js, etc.) ← solo si NUNCA compartirás el archivo
├── CSS inline (estilo limpio, responsive)
├── UI: drag-drop zone + botón comparar + resultados
└── JS: extracción → limpieza → normalización → comparación → reporte

archivo.html (PARA COMPARTIR con otros) ← PATRÓN POR DEFECTO
├── Librerías EMBEBIDAS inline (mammoth.min.js, pdf.min.js, etc.)
├── CSS inline
├── UI
└── JS
```

## ⚠️ PITFATAL CRÍTICO: CDN vs Embedding

**Cuando el HTML se va a compartir con otros usuarios, NUNCA usar CDN.**

Razón: Si el otro PC no tiene internet, tiene firewall corporativo, o abre el archivo desde `file://` → la librería no se carga → el programa no funciona.

```javascript
// ❌ MAL — No funciona en otros PCs
<script src="https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.8.0/mammoth.browser.min.js"></script>

// ✅ BIEN — Funciona en cualquier PC, sin internet
<script>
!function(f){if("object"==typeof exports&&...){/* mammoth.js completo embebido */}}...
</script>
```

**Cómo embeber:**
1. Descargar la librería: `curl -sL "CDN_URL" -o lib.min.js`
2. Reemplazar `<script src="CDN_URL"></script>` por `<script>` + contenido + `</script>`
3. El HTML crecerá (~600KB con mammoth.js) pero funcionará 100% offline

**Regla:** Si David (o cualquier usuario) dice "funciona en mi PC pero no en el de otros" → el 99% de las veces es CDN. Primera acción: embeber la librería.

## Patrón: Comparación de documentos con diff por palabras

**NUNCA usar diff carácter a carácter** — el resultado es ilegible (bloques de caracteres pegados sin espacios). Siempre usar diff **por palabras** con algoritmo LCS.

### Algoritmo LCS para palabras
```javascript
function diffPalabras(palabrasA, palabrasB) {
    const m = palabrasA.length, n = palabrasB.length;
    const dp = Array(m+1).fill(null).map(() => Array(n+1).fill(0));
    for (let i = 1; i <= m; i++)
        for (let j = 1; j <= n; j++)
            dp[i][j] = palabrasA[i-1] === palabrasB[j-1]
                ? dp[i-1][j-1] + 1
                : Math.max(dp[i-1][j], dp[i][j-1]);
    // Retroceder para obtener cambios: { tipo: 'add'|'del', palabra, idx }
    // ...
}
```

### Filtrado de ruido antes de comparar
Los documentos Word certificados/electrónicos tienen ruido que hay que eliminar:
- **URLs embebidas:** `https://sede.xunta.gal/...`
- **Sellos CVE:** `[As copias en papel deste documento...](url)` — formato markdown de hipervínculo
- **Texto de verificación:** "As copias en papel deste documento teñen a condición de copia e serán verificables a través deste código"
- **Headers de página:** "PASEO DE LA CASTELLANA, 67 Página 1 / 5"
- **Líneas con solo guiones/asteriscos** (separadores de tabla)

```javascript
function eliminarRuido(texto) {
    return texto
        .replace(/https?:\/\/[^\s]+/g, ' ')           // URLs sueltas
        .replace(/\[([^\]]*)\]\(https?:\/\/[^)]+\)/g, '$1') // [texto](url) → texto
        .replace(/As copias en papel deste documento[^.]*\./g, '')
        .replace(/condici[oó]n de copia[^.]*\./g, '')
        .replace(/\s+/g, ' ').trim();
}
```

### UX: Porcentaje de similitud + frases legibles
Mostrar resultado como:
- ✅ 100% = "CONTENIDO IDÉNTICO"
- 🟡 95%+ = "CASO IDÉNTICO" (probablemente solo formato/sellos)
- 🟠 80-95% = "SIMILAR" (diferencias significativas)
- 🔴 <80% = "DIFERENTES"

Diferencias como frases:
```
➕ Lo que AÑADE el Doc B: "As copias en papel deste documento..."
❌ Lo que ELIMINA el Doc B: (nada)
```

**NUNCA** mostrar bloques de caracteres pegados sin espacios — el usuario se frustra ("así no se que puede ser lo que es distinto... igual es un espacio o una chorrada").

**Excepción:** Solo usar CDN si el HTML es un prototipo temporal que NUNCA se compartirá.

## Librerías CDN confiables (solo para desarrollo personal)

| Librería | CDN | Uso |
|---|---|---|
| mammoth.js | `cdnjs.cloudflare.com/ajax/libs/mammoth/1.8.0/mammoth.browser.min.js` | Word → texto plano |
| pdf.js | `cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js` | PDF → texto |
| marked | `cdnjs.cloudflare.com/ajax/libs/marked/4.0.10/marked.min.js` | Markdown → HTML |

**⚠️ Preferir jsdelivr sobre cdnjs para pdf.js** — cdnjs tiene timeouts ocasionales.

## Pitfalls críticos

### PDF.js Worker (CRÍTICO)

```javascript
// ❌ MAL — Worker falla desde file:// protocol
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdn.../pdf.worker.min.js';

// ✅ BIEN — Sin worker, funciona desde file:// y https://
pdfjsLib.GlobalWorkerOptions.workerSrc = '';
```

**Motivo:** Cuando el usuario abre el HTML con doble clic (file:// protocol), el navegador bloquea la carga del Web Worker por CORS/Same-Origin Policy. El PDF se carga pero `getTextContent()` devuelve 0 items → 0 palabras → el usuario ve "0 palabras" en el PDF.

### PDF.js no extrae texto de PDFs generados por Acrobat PDFMaker (CRÍTICO)

**Síntoma:** pdf.js devuelve 0 palabras aunque el PDF tiene texto visible. Confirmando con `markitdown` Python → 2588 palabras. El PDF fue creado por "Acrobat PDFMaker 26 para Word".

**Causa:** Acrobat PDFMaker genera fuentes con codificación no estándar que pdf.js no puede decodificar. No es un bug del Worker — es una limitación del parser.

**Solución:** No intentar extraer texto de PDFs directamente en el navegador si el usuario tiene muchos PDFs de origen corporativo. En su lugar:
1. Convertir PDFs a Word con LibreOffice (`soffice --convert-to docx`)
2. Comparar Word vs Word con mammoth.js

```bash
# .bat para convertir PDFs a Word en lote
for %%f in (*.pdf) do "C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to docx "%%f"
```

**Solución:** Siempre configurar `workerSrc = ''` para herramientas que se usan desde archivos locales. Si se necesita rendimiento (PDFs grandes, 100+ páginas), usar fallback:

```javascript
try {
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdn.../pdf.worker.min.js';
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    // ...
} catch(e) {
    pdfjsLib.GlobalWorkerOptions.workerSrc = '';
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    // ...
}
```

### Extracción de texto de PDFs legales

Los PDFs generados desde Word o herramientas de diseño gráfico producen artefactos:
- **Tracking raro:** "A C UER DO" en vez de "ACUERDO" (espaciado entre letras)
- **Años partidos:** "20 26" o "2 026" en vez de "2026"
- **Cabeceras de página:** "PASEO DE LA CASTELLANA, 67 Página 1 / 5"
- **Tablas vacías:** Muchas filas/columnas vacías que generan ruido

### Normalización para documentos legales

```javascript
function normalizar(texto) {
    return texto
        // 1. Eliminar numeración de párrafos al inicio de línea
        .replace(/(?:^|\n)\s*\d{1,2}\.\s/g, '\n')
        .replace(/(?:^|\n)\s*\*\d{1,2}\.\s/g, '\n')  // Markdown
        // 2. Minúsculas + quitar tildes
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        // 3. Solo letras y números
        .replace(/[^a-z0-9]/g, '');
}
```

**Importante:** El regex de numeración DEBE ser `(?:^|\n)\s*\d{1,2}\.\s` (al inicio de línea), NO `\b\d+\.\s` (global) — porque `\b\d+\.\s` come "026" del año "2026." cuando hay un punto después.

### Metadata a eliminar de documentos legales

```javascript
function limpiarMetadata(texto) {
    // 1. Sección de firmas (tabla diferente entre Word y PDF)
    const idx = texto.toLowerCase().indexOf('firman en la fecha');
    if (idx > 0) texto = texto.substring(0, idx);
    
    // 2. Headers/footers de página
    texto = texto.split('\n')
        .filter(l => !/PASEO|CASTELLANA|MADRID|28071|Página\s+\d/i.test(l))
        .filter(l => !/^[\s\-|*#=_]+$/.test(l))
        .join('\n');
    
    return texto;
}
```

## Patrón: HTML autocontenido — embeber TODO en un solo archivo

**Señales clave:** "quiero que funcione con doble clic", "no necesito servidor", "visor local", "descargar y abrir".

Cuando el usuario necesita un HTML que funcione con `file://` sin servidor local:

### Estructura del HTML autocontenido

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>...</title>
    <!-- 1. CSS embebido -->
    <style>
        /* CSS completo inline */
    </style>
    <!-- 2. Librerías CDN (solo Leaflet, Leaflet-Cluster — nunca JSZip/mammoth) -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
</head>
<body>
    <!-- HTML structure -->
    <script>
        // 3. Datos embebidos
        window.SYSTEMS_DATA = [...];
    </script>
    <!-- 4. JS embebido (reemplazar TODOS los <script src="js/...">) -->
    <script>
        // config.js contenido
        // gbfs-parser.js contenido
        // map.js contenido
        // search.js contenido
        // main.js contenido
    </script>
</body>
</html>
```

### ⚠️ PITFALL CRÍTICO: Eliminar referencias a archivos JS externos

Cuando se embeben los JS en `<script>` tags, hay que **eliminar explícitamente** las etiquetas `<script src="js/...">` del HTML. Si quedan, el navegador intenta cargar los archivos desde `file:///ruta/absoluta` del desarrollador → falla en la máquina del usuario.

**Verificación post-embebido:**
```bash
# Debe devolver 0 resultados
grep -c 'src="js/' index.html
# Si devuelve > 0, hay referencias pendientes → eliminarlas
```

**Cómo embeber JS:**
1. Leer todos los archivos JS en orden de dependencia
2. Concatenar con separadores `// === filename.js ===`
3. Reemplazar todos los `<script src="js/...">` por un solo `<script>` con el contenido concatenado
4. Verificar que no queden referencias `src="js/` ni `src="css/`

### Librerías CDN aceptables en HTML autocontenido

**Solo librerías que:**
- No cambian de API entre versiones (Leaflet, Leaflet-Cluster)
- Son estables y confiables (unpkg, cdnjs)
- No requieren worker (o se configuran workerSrc='')

**NUNCA embeber:**
- mammoth.js, pdf.js → si se comparten, embeberlos completos (600KB+)
- Cualquier librería con dependencias cruzadas

### Datos embebidos

Para catálogos de datos (sistemas, estaciones, etc.):
```javascript
window.SYSTEMS_DATA = [
    { id: 'bicing', nombre: 'Bicing', ciudad: 'Barcelona', ... },
    // ...
];
```
El JS principal lee de `window.SYSTEMS_DATA` en vez de `fetch()`.

### Tamaño típico

| Componente | Tamaño |
|---|---|
| CSS inline | 5-15 KB |
| Datos (JSON) | 10-50 KB |
| JS embebido | 30-80 KB |
| **Total** | **50-150 KB** |

## Patrón: Visores de datos espaciales y GTFS

**Señales clave:** "visor de transporte", "mapa con paradas", "buscar paradas cercanas", "GTFS a HTML", "datos geoespaciales en navegador".

Cuando el usuario necesita visualizar datos geoespaciales (GTFS, paradas de transporte, rutas) sin servidor:

1. **Crear HTML autocontenido** con JSZip embebido inline para parsear ZIPs GTFS en el navegador
2. **Carga por drag & drop** de archivos ZIP desde el sistema de archivos local
3. **Cálculo Haversine** para distancias entre coordenadas
4. **Filtrado por radio** de paradas cercanas a un punto
5. **Agrupación por ruta/empresa** en tarjetas expandibles
6. **Coordenadas rápidas** predefinidas (Madrid, Barcelona, etc.)
7. **Botón GPS** para usar ubicación actual del dispositivo

**Librerías clave para visores GTFS:**
- **JSZip** (`jszip.min.js`, ~97KB) — parsea ZIPs GTFS en el navegador
- **Leaflet** (para mapas visuales) — `leaflet.min.js` + CSS
- **Haversine** — cálculo de distancia en metros entre coordenadas

**Estructura típica de un visor GTFS:**
```
visor/
└── index.html          ← Autocontenido, JSZip inline, funciona con doble clic
```

**Patrón de parseo GTFS en JS:**
1. Leer `stops.txt` → array de paradas con lat/lon
2. Leer `routes.txt` → array de rutas con tipo y nombre
3. Leer `trips.txt` → mapeo trip_id → route_id
4. Leer `stop_times.txt` → mapeo stop_id → lista de trips
5. Cruzar: para cada parada, buscar trips que la usan → obtener rutas
6. Filtrar paradas por distancia Haversine al punto buscado

**Pitfall:** JSZip es síncrono en el parseo pero `loadAsync` y `async('string')` son asíncronos. Usar `await` para cada archivo. Los ZIPs grandes (100+ MB) pueden bloquear el hilo principal — mostrar barra de progreso y feedback visual.

**Pitfall:** El visor NO necesita servidor. Los ZIPs se leen desde el sistema de archivos del usuario vía drag & drop o input file. Nunca usar `fetch()` para cargar ZIPs locales — el protocolo `file://` bloquea CORS.

**Ver enlace a:** `templates/gtfs-visor.html`

## Patrón: Visuales en tiempo real con detección de cuerpo

**Señales clave:** "VJ processor", "visuales para concierto", "efectos con webcam", "detección de cuerpo", "MediaPipe", "audio reactive".

Cuando el usuario quiere generar visuales en vivo que reaccionen al cuerpo y/o audio:

1. **MediaPipe Pose** para detección de 33 landmarks del cuerpo (NO YOLO — YOLO solo da bounding box, MediaPipe da puntos precisos)
2. **Web Audio API** para FFT y beat detection (NO p5.sound — raw API es más flexible)
3. **Canvas 2D** para renderizado con trail effects (offscreen canvas + fade)
4. **1 fichero HTML autocontenido** — webcam + detección + efectos + UI

**Efectos típicos:** neon tracer (contour glow), grid distortion (body warping), particle burst (from hands), constellation (landmark connections), shockwave (beat-triggered), portal vortex (background).

**Ver referencia completa:** `references/browser-realtime-visuals.md`

## Patrón: Wizard multi-paso con progreso y LLM

**Señales clave:** "herramienta que haga X con muchos archivos", "procesar en lote", "extraer datos de PDFs", "necesito validación".

Cuando la herramienta requiere múltiples pasos (config → carga → procesamiento → validación → export), usar un **wizard steps** con indicador visual.

### Estructura del wizard

```html
<!-- Step bar horizontal -->
<div class="step-bar">
  <div class="step-item active"><span class="num">1</span> Configuración</div>
  <span class="step-arrow">▸</span>
  <div class="step-item done"><span class="num">✓</span> Cargar</div>
  <span class="step-arrow">▸</span>
  <div class="step-item"><span class="num">3</span> Procesar</div>
</div>

<!-- Contenido por pasos -->
<main>
  <section id="step-1" class="step-section active">...</section>
  <section id="step-2" class="step-section">...</section>
  <section id="step-3" class="step-section">...</section>
</main>
```

### JS: Navegación entre pasos

```javascript
function goToStep(n) {
  S.step = n;
  document.querySelectorAll('.step-section').forEach(s => s.classList.remove('active'));
  $('step-' + n).classList.add('active');
  renderStepBar(); // Actualiza indicador: active/done/pending
}
```

### Progress tracking para batch processing

Cuando se procesan muchos archivos (100-1000), mostrar SIEMPRE:
1. **% completado** — barra de progreso animada
2. **Fase actual** — "Extrayendo texto...", "Enviando a LLM...", "Validando..."
3. **ETA** — tiempo restante estimado (calcular con promedio de los procesados)
4. **Estadísticas en vivo** — exitosos / advertencias / errores
5. **Log** — últimas operaciones en caja monospace
6. **Pausa/Reanudar** — botón para pausar el procesamiento
7. **Cancelar** — botón para detener

```javascript
// Actualizar UI cada N archivos, no en cada uno (evitar reflows)
const pct = Math.round(current / total * 100);
$('procBar').style.width = pct + '%';
$('procPct').textContent = pct + '%';
$('procETA').textContent = formatTime(remaining);
```

### LLM calls desde el navegador

Cuando la herramienta necesita llamar a una API de LLM desde el HTML:

```javascript
async function callLLM(text, schema, apiKey, model) {
  const response = await fetch('https://api.nan.builders/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: model || 'qwen3.6',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.1  // Bajo para extracción determinista
    })
  });
  const result = await response.json();
  let content = result.choices[0].message.content;
  // Limpiar markdown fences si los hay
  content = content.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '').trim();
  return JSON.parse(content);
}
```

**Throttling:** Para 1000+ llamadas, usar delay entre requests (1.5-2s). Mostrar progreso.

**API Key:** Guardar en localStorage, nunca enviar a terceros. Avisar al usuario.

**Parsing robusto:** El LLM a veces devuelve JSON envuelto en ```json. Siempre limpiar antes de parsear. Fallback: buscar `{...}` con regex si el parse directo falla.

### CSS: Kaizen vs Aurora para herramientas

**Kaizen** (flat corporativo) es mejor para:
- Herramientas de procesamiento/datos
- Tools que se usan frecuentemente
- Entorno corporativo/profesional
- Cuando el usuario dice "estilo limpio", "corporativo", "sin florituras"

**Aurora** (liquid glass, mesh) es mejor para:
- Dashboards personales
- Landings creativas
- Apps visuales
- Cuando el usuario pide "moderno", "glass", "aurora"

**Regla:** Si no se especifica, preguntar. Para tools de procesamiento de datos, Kaizen por defecto.

## Preferencia del usuario (David)

Cuando David dice "no me deja Python" o "algo más fácil", la respuesta **nunca** es "instala X" o "usa Y". La respuesta es: **crear un HTML que funcione en el navegador**. Cero dependencias, cero instalación, doble clic y listo.

**Portabilidad:** Si el HTML se va a compartir con otros (compañeros de trabajo, clientes), SIEMPRE embeber las librerías inline. David ha tenido problemas con HTMLs que usaban CDN al compartirlos — otros PCs no cargaban las dependencias.

Para el futuro: si la herramienta necesitaba Python, considerar si se puede resolver con:
1. HTML + JavaScript en navegador (preferido, con libs embebidas si es compartido)
2. Script .bat/.sh que instale dependencias automáticamente
3. .exe con PyInstaller (último recurso, requiere compilación en Windows)

## Comparativa de alternativas

- **[anthropics/html-effectiveness](https://github.com/anthropics/html-effective)** — HTML como formato de salida flexible: artefactos .html autocontenidos sin build; refuerza la filosofía de este skill de herramientas que funcionan 100% en el navegador.
