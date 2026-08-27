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

## Preferencia del usuario (David)

Cuando David dice "no me deja Python" o "algo más fácil", la respuesta **nunca** es "instala X" o "usa Y". La respuesta es: **crear un HTML que funcione en el navegador**. Cero dependencias, cero instalación, doble clic y listo.

**Portabilidad:** Si el HTML se va a compartir con otros (compañeros de trabajo, clientes), SIEMPRE embeber las librerías inline. David ha tenido problemas con HTMLs que usaban CDN al compartirlos — otros PCs no cargaban las dependencias.

Para el futuro: si la herramienta necesitaba Python, considerar si se puede resolver con:
1. HTML + JavaScript en navegador (preferido, con libs embebidas si es compartido)
2. Script .bat/.sh que instale dependencias automáticamente
3. .exe con PyInstaller (último recurso, requiere compilación en Windows)
