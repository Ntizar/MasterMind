---
name: pdf-text-extraction
description: Métodos para extraer texto de PDFs cuando las herramientas estándar fallan — PDF.js via browser, parsing binario CIDFonts, y análisis visual
category: data
---

# Extracción de texto de PDFs

## Cuándo usar

Cuando necesitas extraer texto de un PDF y las herramientas estándar fallan o no están disponibles.

## Métodos (en orden de prioridad)

### 1. `pdftotext` (poppler-utils)

```bash
pdftotext archivo.pdf salida.txt
```

**Pitfall:** Si falla con `libpoppler.so.XX: cannot open shared object`, ejecutar `ldconfig` primero. Si sigue fallando, la librería no está instalada — pasar al método 2.

### 2. Browser PDF.js (fallback robusto)

Cuando `pdftotext` no funciona o el PDF tiene encoding CIDFonts:

1. Crear un servidor HTTP local con el PDF y un HTML que use PDF.js
2. Navegar al HTML en el browser
3. Usar `browser_console` para extraer `document.querySelector('textarea').value`

**Script de referencia:** `/hermes-home/skills/pdf-text-extraction/scripts/pdf-extractor.html`

```javascript
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
const response = await fetch('http://localhost:8765/archivo.pdf');
const pdf = await pdfjsLib.getDocument({data: await response.arrayBuffer()}).promise;
for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const textContent = await page.getTextContent();
    // textContent.items[].str contiene cada fragmento de texto
}
```

### 3. Browser visual analysis (último recurso)

Cuando el PDF renderiza TODO como paths vectoriales (números, tablas, etc. sin capa de texto):

1. Navegar al PDF directamente en el browser (`file:///` o servidor local)
2. Esperar a que cargue
3. Usar `browser_vision()` página por página para leer el contenido
4. Navegar entre páginas con el input de número de página

**Pitfall crítico:** Las páginas en blanco pueden ser portadas, páginas de notas o páginas donde el contenido está en un formato no-texto. Probar múltiples páginas.

### 4. Parsing binario del PDF (último recurso absoluto)

Cuando NADA de lo anterior funciona:

- Extraer streams con `zlib.decompress()`
- Buscar operadores `TJ`/`Tj` con CIDFonts
- Decodificar CIDs manualmente (ej: CID 3 = espacio, CID 68-90 = letras - 3)
- **Limitación:** Si el PDF renderiza números como paths vectoriales (m, l, c, h, f), NO se puede extraer numéricamente — se necesita OCR visual

## Pitfalls

- **PDFs con CIDFonts:** Los CIDs no mapean directamente a ASCII. Necesitas un ToUnicode CMap o decodificación manual.
- **PDFs con contenido vectorial:** Algunos PDFs (especialmente los generados por software contable) renderizan TODO como paths, no como texto. En estos casos, los métodos 3 y 4 no funcionarán para números.
- **`pdftotext` con libpoppler:** Si falla por librería, `ldconfig` puede no bastar si la librería no está instalada en el sistema.
- **Browser tool roto en `*.apps.nan.builders`:** Usar curl-based analysis en su lugar.

## Referencias

- Ver `references/pdf-cid-encoding.md` para mapeo de CIDs comunes
- Ver `references/pdf-vector-rendering.md` para casos de PDFs renderizados como paths
