# Web Share API + Lazy CDN Loading — Mobile Sharing para Zero-Install HTML Apps

Patrones para compartir contenido generado en el navegador desde apps HTML sin servidor.

## 1. Web Share API con Fallback a Clipboard

**Cuándo usarlo:** Cuando el usuario necesita compartir resultados (encuestas, informes, datos) directamente desde el navegador en móvil — WhatsApp, email, SMS, etc.

**Flujo:**
```javascript
async function shareSurvey(data) {
  const text = `📋 Encuesta PMST\n\n${data.map(d => `${d.pregunta}: ${d.respuesta}`).join('\n')}`;
  
  // 1. Intentar Web Share API (móvil nativo)
  if (navigator.share) {
    try {
      await navigator.share({
        title: 'Encuesta PMST',
        text: text,
      });
      return; // Éxito — usuario eligió app
    } catch (err) {
      if (err.name === 'AbortError') return; // Usuario canceló — no hacer nada
      // Otro error → fallback
    }
  }
  
  // 2. Fallback: copiar al portapapeles
  try {
    await navigator.clipboard.writeText(text);
    alert('✅ Copiado al portapapeles — pégalo en WhatsApp/email');
  } catch {
    // 3. Fallback final: textarea temporal
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    alert('✅ Copiado al portapapeles');
  }
}
```

**Pitfalls:**
- `navigator.share()` solo funciona en contextos seguros (HTTPS o localhost). En `file://` no funciona.
- `navigator.share()` requiere gesto del usuario (click/tap) — no llamar en `DOMContentLoaded` o `setTimeout`.
- Si el usuario cancela, `AbortError` se lanza — NO mostrar error, simplemente retornar.
- `navigator.clipboard.writeText()` requiere foco del documento. Si se llama desde un callback async sin foco, falla silenciosamente.

**UI pattern:** Botón simple con icono 📤:
```html
<button onclick="shareSurvey()" style="padding: 8px 16px; border-radius: 8px; 
  background: #2563eb; color: white; border: none; cursor: pointer;">
  📤 Compartir (WhatsApp, email...)
</button>
```

**Demo real:** PLANDEMOVILIDAD — `encuesta.html` → `shareSurvey()`.

---

## 2. Lazy CDN Library Loading (On-Demand)

**Cuándo usarlo:** Cuando una librería CDN pesada (html2canvas, jsPDF, SheetJS) solo se usa en una acción específica (exportar imagen, generar PDF). No cargar 200KB+ al inicio si el usuario quizás nunca lo use.

**Patrón:**
```javascript
let html2canvasLoaded = false;

async function exportMapAsImage() {
  if (!html2canvasLoaded) {
    await loadScript('https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js');
    html2canvasLoaded = true;
  }
  
  const canvas = await html2canvas(document.getElementById('mapa-container'));
  const link = document.createElement('a');
  link.download = 'mapa-pmst.png';
  link.href = canvas.toDataURL('image/png');
  link.click();
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}
```

**Pitfalls:**
- `html2canvas` no renderiza WebGL/Canvas2D internos — solo DOM. Si el mapa usa Leaflet Canvas renderer, el resultado puede estar vacío. Verificar con `canvas.toDataURL()` que el output no es transparente.
- CDN timeout → Promise never resolves. Añadir timeout:
  ```javascript
  function loadScript(src, timeoutMs = 10000) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('CDN timeout')), timeoutMs);
      const script = document.createElement('script');
      script.src = src;
      script.onload = () => { clearTimeout(timer); resolve(); };
      script.onerror = () => { clearTimeout(timer); reject(new Error('CDN load failed')); };
      document.head.appendChild(script);
    });
  }
  ```
- Si el usuario hace click rápido múltiples veces, iniciar múltiples descargas. Añadir guard:
  ```javascript
  let exporting = false;
  async function exportMapAsImage() {
    if (exporting) return;
    exporting = true;
    try { /* ... */ } finally { exporting = false; }
  }
  ```

**Demo real:** PLANDEMOVILIDAD — `js/mapa.js` → `exportMapAsImage()` lazy-loads html2canvas.

---

## 3. CSV Format Auto-Detection

**Cuándo usarlo:** Cuando una app puede recibir CSVs de múltiples fuentes con formatos diferentes (encuesta con 21 columnas vs import básica con 5 columnas).

**Patrón:**
```javascript
function detectCSVFormat(header) {
  const cols = header.split(',').map(c => c.trim().toLowerCase());
  if (cols.includes('nombre_completo') || cols.length > 10) {
    return 'encuesta'; // Formato encuesta.html (21 columnas)
  }
  return 'basico'; // Formato básico (nombre, departamento, etc.)
}

function importarCSVTexto(csvText, formatoDetectado) {
  const lines = csvText.trim().split('\n');
  const header = lines[0];
  const format = formatoDetectado || detectCSVFormat(header);
  
  if (format === 'encuesta') {
    return parseEncuestaCSV(lines); // 21 columnas
  } else {
    return parseBasicoCSV(lines); // Formato simple
  }
}
```

**Pitfalls:**
- BOM (Byte Order Mark) al inicio del CSV — `trim()` no lo elimina. Usar `csvText.replace(/^\uFEFF/, '')` antes de procesar.
- Encuesta CSV tiene `nombre_completo` como primera columna — es el indicador más fiable para detectar formato.
- Si el CSV viene de Excel español, los separadores pueden ser `;` en vez de `,`. Detectar: `const sep = header.includes(';') ? ';' : ',';`

**Demo real:** PLANDEMOVILIDAD — `index.html` → `importarCSVTexto()` + `pegarCSV()`.
