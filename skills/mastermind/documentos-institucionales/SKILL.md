---
name: documentos-institucionales
description: "Análisis de informes institucionales/regulatorios públicos (CNMC, REE, MITMS, BOE, Comisión Europea) — extracción PDF, auditoría estructurada y generación multi-formato (HTML resumen, LinkedIn/post, nota técnica)."
version: 1.0.0
author: Mastermind
tags: [documentos, auditoria, informes, cnmc, regulacion, contenido, linkedin, html]
---

# Documentos Institucionales (Informes Regulatorios)

## Cuándo usarlo

- El usuario adjunta un PDF de un organismo público (CNMC, REE, MITMS, CE, BOE, AVE, ADIF, AENA)
- El usuario pide "auditar", "analizar", "resumir" o "sacar conclusiones" de un informe institucional
- El usuario pide contenido para redes sociales basado en un documento extenso
- El usuario pide múltiples formatos de salida del mismo análisis

## No es para

- Auditorías de código/software (usar `requesting-code-review` o `technical-audit-remediation`)
- Auditorías de simuladores eléctricos (usar `auditoria-simulacion-energetica`)
- Análisis de competidores desde web (usar `competitive-intelligence`)
- Resúmenes rápidos sin estructura de auditoría (hacer directo sin este skill)

## Pipeline completo

### Fase 0 — Extracción del PDF

```bash
# Instalar PyMuPDF si no está
python3 -m pip install PyMuPDF -q

# Extraer texto completo
python3 -c "
import fitz
doc = fitz.open('/ruta/al/documento.pdf')
print(f'{len(doc)} páginas')
for i, page in enumerate(doc):
    text = page.get_text()
    print(f'--- Página {i+1} ---')
    print(text)
"
```

**Pitfall:** Si `pip install` falla, probar `python3 -m pip install PyMuPDF -q`. Si no hay `pip`, usar `which python3` primero.

### ❌ Embedded-font PDFs (CMap/ToUnicode)

⚠️ **CRÍTICO:** Muchos PDFs académicos (arxiv/LaTeX, informes técnicos de Microsoft/Google/DeepMind) usan **fuentes embebidas con CMap personalizado + ToUnicode mapping**. Esto hace que **TODOS los enfoques naive fallen**:

| Enfoque | Resultado |
|---------|-----------|
| `strings` / raw ASCII search | Solo captura metadatos, PDF syntax, referencias a objetos |
| `re.findall(rb'\\(([^)]+)\\)\\s*Tj', decompressed)` | Devuelve garbage binario porque los caracteres no son ASCII |
| `re.findall(rb'BT.*?ET', data, DOTALL)` | Los streams están en FlateDecode y los caracteres no son UTF-8 |
| `zlib.decompress()` + lookup parens | El texto usa bytes de la fuente embebida, no Unicode |
| **PyMuPDF (`fitz`)** | ✅ **Funciona.** Resuelve CMap internamente |

**Síntomas de un PDF con fuente embebida:**
- `strings documento.pdf` devuelve casi nada legible
- La estructura de secciones se ve (sec.1, subsection.2.1, cite.xxx) pero el texto real no
- `fitz.open(doc)` extrae texto perfectamente
- En metadatos del PDF: producer = "xdvipdfmx" (LaTeX) o productos similares

**Regla:** Ante cualquier PDF académico/técnico, ir DIRECTAMENTE a PyMuPDF. No perder tiempo con strings/regex/binario.

### 🔄 PDFs con fuentes embebidas SIN PyMuPDF disponible

Cuando **PyMuPDF no está disponible** (sin pip, sin internet) y el PDF usa fuentes embebidas con CMap corrupto/inválido, hay un patrón de extracción fallback:

#### Paso 1 — Detectar si el PDF usa Identity-UCS encoding

Buscar `ToUnicode` en el PDF:
```python
import re, zlib
data = open(pdf_path, 'rb').read()
to_unicode_refs = re.findall(rb'/ToUnicode\\s+(\\d+)\\s+(\\d+)\\s+R', data)
```

Si hay referencias a ToUnicode, extraer el stream y buscar `begincmap` / `beginbfchar`.

#### Paso 2 — Determinar si los CIDs son Unicode directos (Identity-UCS)

Si el CMap solo mapea el espacio, los CIDs restantes son probablemente **códigos Unicode directos**. Extraer todos los CIDs de los streams de contenido.

#### Paso 3 — Detectar shifts de fuente (substitution cipher)

Si los CIDs decodificados como Unicode directo no forman texto legible, buscar un **shift sistemático**.

#### Paso 4 — Decodificar con el mapeo descubierto

```python
def decode_cid(cid, shift=0):
    if cid == 3: return ' '
    if 0x20 <= cid <= 0x7E: return chr(cid - shift)
    if 0xA0 <= cid <= 0xFFFF: return chr(cid - shift)
    return '?'

chars = [decode_cid(cid, shift) for cid in cids]
result = ''.join(chars)
```

#### Pitfalls
- **CMap corrupto:** Los TTF embebidos pueden tener cmap tables con datos basura.
- **CID 3 = espacio:** El ToUnicode CMap casi siempre mapea CID 3 → espacio.
- **Shift por rango:** El shift puede variar por rango (mayúsculas vs minúsculas vs dígitos).

### 1b. BOE HTML (txt.php) — Leyes y disposiciones formales

Cuando el BOE ofrece texto plano vía `txt.php` (no PDF):

```bash
# URL: https://www.boe.es/diario_boe/txt.php?id=BOE-A-2017-12902
curl -s "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2017-12902" > boe-texto.html
```

**Parsing de estructura de ley:**
- Detectar párrafos con "Artículo N." → separar artículos
- Detectar "Libro", "Título", "Capítulo", "Sección" → jerarquía
- Generar `ley-data.js` (estructura navegable) + `ley-texto.json` (texto completo)
- Cada artículo: número, título, texto completo, metadatos de ubicación

**Pitfalls:**
- El HTML del BOE tiene `<meta>` tags antes del `<body>` — extraer solo `<body>`
- Los caracteres especiales (ñ, tildes) están como entidades HTML (`&eacute;`, `&ntilde;`) — decodificar
- Los artículos pueden tener texto corto (solo título) o extenso (varios párrafos)
- El parser debe ser robusto: no todos los artículos siguen el mismo formato

**Ver:** `references/mega-plan-pattern.md` para el patrón de orquestación multi-sesión donde se usó este parsing.

### 2. Browser PDF.js (fallback robusto)

Cuando `pdftotext` no funciona o el PDF tiene encoding CIDFonts:

1. Crear un servidor HTTP local con el PDF y un HTML que use PDF.js
2. Navegar al HTML en el browser
3. Usar `browser_console` para extraer `document.querySelector('textarea').value`

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

1. Navegar al PDF directamente en el browser
2. Esperar a que cargue
3. Usar `browser_vision()` página por página para leer el contenido

### 4. Parsing binario del PDF (último recurso absoluto)

Cuando NADA de lo anterior funciona:
- Extraer streams con `zlib.decompress()`
- Buscar operadores `TJ`/`Tj` con CIDFonts
- Decodificar CIDs manualmente

**Pitfall:** Si el PDF renderiza números como paths vectoriales, NO se puede extraer numéricamente — se necesita OCR visual.

### 5. Fallback general de investigación web

Cuando los buscadores convencionales bloquean con CAPTCHA desde la IP del servidor:

1. **Wikipedia/Wikidata APIs** — más fiable desde servidor
2. **Navegación directa** — browser tool + browser_console para DOM extraction
3. **Curl con headers** — Mozilla user-agent + Accept-Language
4. **RSS-first** — feeds RSS son más confiables que HTML scraping
5. **Conocimiento propio** — cuando la investigación falla, usar conocimiento del dominio

### Fase 1 — Macroauditoría estructurada

Estructura de análisis:

1. **Contexto del documento** — organismo emisor, fecha, alcance, metodología empleada
2. **Hallazgos principales** — datos clave, conclusiones, recomendaciones
3. **Datos extraíbles** — tablas, KPIs, comparativas, cifras relevantes
4. **Crítica metodológica** — puntos fuertes y débiles del análisis original
5. **Valoración global** — rigor, aplicabilidad, utilidad para el usuario

### Fase 2 — Generación multi-formato

#### Formato A: Resumen HTML

Artefacto HTML completo y autónomo con:
- **Tarjetas KPI** con los números más impactantes (rojo/verde/naranja según dirección)
- **Tablas de datos** del informe original, limpias y legibles
- **Comparativas** (€/km, tiempo/ruta, costes externos, cuotas modales)
- **Highlight boxes** para hallazgos clave
- **Conclusiones y recomendaciones** del informe original
- **Sección metodológica** breve al final
- Estilo Esios: azul #2563eb + naranja #f97316 + fondo gris claro
- Responsive, sin dependencias externas

```html
<!-- Template de sección típica -->
<div class="section">
  <h2>📋 Título</h2>
  <table>...</table>
  <div class="highlight-box">💡 Hallazgo clave</div>
</div>
```

Ver `references/resumen-html-style-guide.md` para el sistema de diseño completo.

#### Formato B: Post LinkedIn (estilo David Antizar)

**⚠️ NO USAR** — La skill `linkedin-david-antizar-style` es **provisional y sin ejemplos reales**. El usuario la ha rechazado explícitamente como no representativa de su estilo.

**Procedimiento correcto:**
1. Informar al usuario que se necesitan 3-5 posts reales suyos para capturar su voz
2. Si el usuario los proporciona, usar `references/extraer-estilo-linkedin.md` en la skill `linkedin-david-antizar-style` para extraer patrones
3. Actualizar la skill con los patrones reales
4. Sólo entonces generar el post

**No generar posts LinkedIn sin ejemplos reales del usuario.**

### Referencia eliminada
El archivo `references/linkedin-david-antizar-style.md` en este directorio es una versión antigua y genérica. No usar. La skill dedicada `linkedin-david-antizar-style` es la fuente de verdad (aunque aún provisional).

#### Formato C: Nota técnica de auditoría

Guardar en `notes/YYYY-MM-DD-titulo.md` con:
- Contexto, hallazgos, crítica metodológica, valoración
- Tabla de datos clave extraídos
- Lista de entregables generados

### Fase 3 — Validación y entrega

- Verificar que los archivos existen con `ls -la`
- Confirmar rutas absolutas
- Si se usa `MEDIA:/path` para el HTML, comprobar que el archivo está accesible

## Estructura típica de entregables

```
workspace/
├── cnmc-transporte-resumen.html    ← Artefacto HTML
├── cnmc-linkedin-post.md            ← Post LinkedIn
└── notes/YYYY-MM-DD-titulo.md       ← Nota técnica
```

## Pitfalls

### ❌ No sobre-planificar tareas multi-fix
Para bugs/correcciones que requieran 3+ arreglos: auditar → plan concreto → presentar → esperar aprobación → implementar. No silenciar entre pasos.

### ❌ No parar sin avisar
El usuario frustra "porque has parado?". Mostrar progreso en tiempo real. Al terminar tarea, pasar a la siguiente inmediatamente sin preguntar.

### ❌ Tablas en Telegram
No usar tablas markdown en Telegram. Usar listas con `key: value`.

### ❌ Resumen chulo siempre
Nunca responder con frase seca. Al terminar, resumen visualmente atractivo con formato bonito.

### ❌ Tareas simples (<3 tool calls)
Hacer directo sin sobre-planificar ni delegar a subagentes.

## Referencias

- `references/resumen-html-style-guide.md` — Sistema de diseño CSS para artefactos HTML (colores, tarjetas, tablas, highlight boxes)
- `references/pdf-extraction-identity-ucs.md` — Técnica fallback para extracción de PDFs con fuentes embebidas y CMap corrupto (Identity-UCS + shift detection) cuando PyMuPDF no está disponible
- **Post LinkedIn:** NO usar `references/linkedin-david-antizar-style.md` (incorrecta). Cargar `skill_view(name='linkedin-david-antizar-style')` en su lugar.