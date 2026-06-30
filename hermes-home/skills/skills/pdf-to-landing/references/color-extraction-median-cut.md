# Extracción de colores de PDF — Median Cut Algorithm

## Patrón completo (client-side, multi-página v5)

### 1. Renderizar MÚLTIPLES páginas del PDF a canvas con pdf.js
```javascript
pdfjsLib.GlobalWorkerOptions.workerSrc = ''; // Sin worker para compatibilidad file://

async function extractColorsFromPDF(file) {
  const arrayBuffer = await file.arrayBuffer();
  const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
  const totalPages = Math.min(pdf.numPages, 5); // Máximo 5 páginas

  const allPixels = [];

  for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
    const page = await pdf.getPage(pageNum);
    const scale = 1;
    const viewport = page.getViewport({ scale });

    // Canvas offscreen para cada página
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = viewport.width;
    tempCanvas.height = viewport.height;
    const tempCtx = tempCanvas.getContext('2d');

    await page.render({ canvasContext: tempCtx, viewport }).promise;

    // Extraer píxeles de esta página
    const imageData = tempCtx.getImageData(0, 0, tempCanvas.width, tempCanvas.height);
    const data = imageData.data;
    for (let i = 0; i < data.length; i += 8) { // cada 2 píxeles
      const r = data[i], g = data[i+1], b = data[i+2], a = data[i+3];
      if (a < 128) continue;
      allPixels.push([r, g, b]);
    }

    // Renderizar primera página al canvas visible (preview)
    if (pageNum === 1) {
      const canvas = document.getElementById('pdfCanvas');
      const ctx = canvas.getContext('2d');
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      await page.render({ canvasContext: ctx, viewport }).promise;
    }
  }

  return allPixels;
}
```

**Por qué multi-página:** Un PDF puede tener colores de marca solo en páginas interiores (ej: página 1 es blanca con logo gris, página 3 tiene el hero con verde). Renderizar solo página 1 pierde esos colores.

**Por qué escala 1 (no 1.5):** Con 5 páginas, escala 1.5 genera demasiados píxeles. Escala 1 es suficiente para detección de colores.

### 2. Extraer píxeles (samplear cada 2px para precisión)
```javascript
function extractPixels(ctx, canvas) {
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const pixels = [];
  const data = imageData.data;
  for (let i = 0; i < data.length; i += 8) { // cada 2 píxeles (no 4)
    const r = data[i], g = data[i+1], b = data[i+2], a = data[i+3];
    if (a < 128) continue; // skip transparentes
    pixels.push([r, g, b]);
  }
  return pixels;
}
```

### 3. Median Cut Algorithm
```javascript
function medianCut(pixels, numColors) {
  function getRange(bucket) {
    let minR=255,maxR=0,minG=255,maxG=0,minB=255,maxB=0;
    for (const p of bucket) {
      if(p[0]<minR) minR=p[0]; if(p[0]>maxR) maxR=p[0];
      if(p[1]<minG) minG=p[1]; if(p[1]>maxG) maxG=p[1];
      if(p[2]<minB) minB=p[2]; if(p[2]>maxB) maxB=p[2];
    }
    return { r:maxR-minR, g:maxG-minG, b:maxB-minB };
  }
  function avgColor(bucket) {
    let r=0,g=0,b=0;
    for (const p of bucket) { r+=p[0]; g+=p[1]; b+=p[2]; }
    const n = bucket.length;
    return [Math.round(r/n), Math.round(g/n), Math.round(b/n)];
  }

  let buckets = [pixels.slice()];
  while (buckets.length < numColors) {
    let maxIdx=0, maxLen=0;
    for (let i=0; i<buckets.length; i++) {
      if (buckets[i].length > maxLen) { maxLen=buckets[i].length; maxIdx=i; }
    }
    if (buckets[maxIdx].length < 2) break;
    const range = getRange(buckets[maxIdx]);
    let channel = 0;
    if (range.g >= range.r && range.g >= range.b) channel = 1;
    else if (range.b >= range.r && range.b >= range.g) channel = 2;
    buckets[maxIdx].sort((a,b) => a[channel] - b[channel]);
    const mid = Math.floor(buckets[maxIdx].length / 2);
    buckets.splice(maxIdx, 1, buckets[maxIdx].slice(0,mid), buckets[maxIdx].slice(mid));
  }
  return buckets.map(avgColor);
}
```

### 4. Deduplicar colores similares (distancia euclídea)
```javascript
// Distancia entre dos colores en espacio RGB (0-441)
function colorDistance(c1, c2) {
  return Math.sqrt(
    Math.pow(c1[0] - c2[0], 2) +
    Math.pow(c1[1] - c2[1], 2) +
    Math.pow(c1[2] - c2[2], 2)
  );
}

// Eliminar colores duplicados (threshold ~30 = perceptualmente cercanos)
function deduplicateColors(colors, threshold = 30) {
  const unique = [];
  for (const c of colors) {
    const isDuplicate = unique.some(u =>
      colorDistance([c.r, c.g, c.b], [u.r, u.g, u.b]) < threshold
    );
    if (!isDuplicate) unique.push(c);
  }
  return unique;
}
```

**Por qué deduplicar:** Sin esto, el mismo color aparece 3-4 veces con hex casi idénticos (#2E7D32, #2F7E33, #307F34). La UI muestra chips confusos y la IA recibe colores redundantes. Threshold 30 elimina duplicados perceptuales sin perder variedad real.

### 5. Devolver TODOS los colores (SIN FILTRAR, post-deduplicación)
```javascript
// 1. Median Cut con 20 buckets
const rawColors = medianCut(allPixels, 20);

// 2. Ordenar por saturación (más saturados primero)
rawColors.sort((a, b) => {
  const satA = (Math.max(...a) - Math.min(...a)) / Math.max(...a);
  const satB = (Math.max(...b) - Math.min(...b)) / Math.max(...b);
  return satB - satA;
});

// 3. Convertir a objetos
let colors = rawColors.map(c => ({
  r: c[0], g: c[1], b: c[2],
  hex: rgbToHex(c[0], c[1], c[2])
}));

// 4. Deduplicar colores similares (distancia euclídea < 30)
colors = deduplicateColors(colors, 30);

return colors; // 8-15 colores únicos
```

**Por qué no filtrar:**
- Un verde claro como `#81C784` tiene saturación ~0.35 — se filtraba con el umbral de 0.08
- Un blancocrema como `#F5F5DC` tiene brightness ~238 — se filtraba con el umbral de 240
- Los colores "aburridos" (grises, beige) son el fondo y texto del diseño — son IMPORTANTES
- El Median Cut con 15 buckets ya separa bien los colores dominantes sin necesidad de filtro
- El usuario puede eliminar colores manualmente en la UI (chips editables con ✕)

### 5. Enviar colores al backend
```javascript
const formData = new FormData();
formData.append('pdf', file);
formData.append('detectedColors', JSON.stringify(colors.map(c => hex(c))));
await fetch('/api/analyze', { method: 'POST', body: formData });
```

## Backend: recibir colores y usarlos en el prompt
```javascript
const detectedColors = req.body.detectedColors
  ? JSON.parse(req.body.detectedColors) : [];

// Incluir en el prompt de análisis:
const colorInfo = detectedColors.length > 0
  ? '\n\nCOLOLES REALES extraidos visualmente del PDF:\n' +
    detectedColors.map((c,i) => `  ${i+1}. ${c}`).join('\n')
  : '';
```

## Backend:强制 colores en generación
```javascript
// En generateLandingHTML:
const colorEnforcement = paleta.primario
  ? '\n\nCOLOLES OBLIGATORIOS (extraidos del PDF real):\n' +
    `- primario: ${paleta.primario}\n` +
    `- secundario: ${paleta.secundario}\n` +
    `- acento: ${paleta.acento}\n` +
    '\nUsa estos colores EXACTAMENTE. NUNCA uses colores por defecto.'
  : '';
```

## UI: Chips de colores editables
```javascript
function renderColorChips() {
  colorsRow.innerHTML = '';
  detectedColors.forEach((c, idx) => {
    const chip = document.createElement('div');
    chip.className = 'color-chip';
    chip.innerHTML = `
      <input type="color" class="color-dot" value="${c.hex}" data-idx="${idx}">
      <input type="text" class="color-input" value="${c.hex}" data-idx="${idx}" maxlength="7">
      <button class="color-remove" data-idx="${idx}">✕</button>
    `;
    colorsRow.appendChild(chip);
  });
  // Botón añadir
  const addBtn = document.createElement('button');
  addBtn.className = 'color-add';
  addBtn.textContent = '+ Añadir';
  addBtn.addEventListener('click', () => {
    detectedColors.push({ r: 128, g: 128, b: 128, hex: '#808080' });
    renderColorChips();
  });
  colorsRow.appendChild(addBtn);
  // Bind events: color input, text input, remove button
}
```

## Pitfalls
- **pdf.js workerSrc vacío:** Obligatorio para que funcione desde `file://`. Si se configura un CDN worker, falla con CORS.
- **Sample rate:** Cada 2 píxeles da buena precisión sin ser lento. Cada píxel es innecesario para detección de colores.
- **🔴 FILTRAR colores elimina verdes y pastels:** El filtro de saturación (<0.08) eliminaba verdes claros y pastels legítimos. El filtro de brightness eliminaba beige y crema. **NO FILTRAR** — dejar al usuario decidir con chips editables.
- **20 buckets > 15 > 6:** Con 6 buckets, un PDF con 70% blanco pierde los colores minoritarios. Con 20, aparecen todos (y la deduplicación elimina los repetidos).
- **Orden por saturación:** Los colores más saturados son visualmente más relevantes que los grises, pero NO eliminar los grises — son fondo/texto.
- **UI editable:** Cada chip de color debe ser editable (input type="color" + input text + botón eliminar). El usuario es la última autoridad sobre los colores.

## Diseño detectado editable (v5+)

Después del análisis de IA, TODOS los campos deben ser editables antes de generar:

### Campos editables
| Campo | Tipo de input | Ejemplo |
|-------|--------------|---------|
| Empresa | text input | "Fairground" |
| Sector | text input | "Marketing Digital" |
| Tono | select dropdown | formal/informal/creativo/corporativo/minimalista/audaz |
| Inspiración | text input | "Notion" |
| Tipografía Heading | select dropdown | serif/sans-serif/display/monospace |
| Estilo | textarea | Descripción del estilo visual |

### Colores de paleta editables
Cada color (primario, secundario, acento, fondo, texto) tiene:
- `input type="color"` — selector nativo del navegador
- `input type="text"` — para escribir hex manualmente
- Label con el nombre del color

### Por qué editable
- La IA a menudo no capta el color exacto del PDF (ej: detecta `#ffcfb5` en vez de naranja quemado `#E85D04`)
- El usuario conoce su identidad visual mejor que la IA
- Permite correcciones rápidas sin re-analizar
- Los cambios se reflejan en `currentDesign` antes de generar el HTML

### Implementación JavaScript
```javascript
function showDesignInfo(design) {
  // Renderizar campos editables
  const fields = [
    { key: 'empresa', label: 'Empresa', type: 'text' },
    { key: 'tono', label: 'Tono', type: 'select', options: ['formal','informal','creativo'] },
    { key: 'estilo', label: 'Estilo', type: 'textarea' },
  ];

  fields.forEach(f => {
    const div = document.createElement('div');
    div.className = 'design-item';
    if (f.type === 'select') {
      div.innerHTML = `<select class="design-select" data-field="${f.key}">
        ${f.options.map(o => `<option ${o === design[f.key] ? 'selected' : ''}>${o}</option>`).join('')}
      </select>`;
    } else if (f.type === 'textarea') {
      div.innerHTML = `<textarea class="design-textarea" data-field="${f.key}">${design[f.key] || ''}</textarea>`;
    } else {
      div.innerHTML = `<input type="text" class="design-input" data-field="${f.key}" value="${design[f.key] || ''}">`;
    }
    designGrid.appendChild(div);
  });

  // Bind change events para sincronizar con currentDesign
  designGrid.querySelectorAll('input, select, textarea').forEach(input => {
    input.addEventListener('change', (e) => {
      const field = e.target.dataset.field;
      currentDesign[field] = e.target.value;
    });
  });
}
```
