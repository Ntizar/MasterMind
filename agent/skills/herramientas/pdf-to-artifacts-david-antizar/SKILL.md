---
name: pdf-to-artifacts-david-antizar
description: Pipeline de transformación de PDF a 3 artefactos — análisis técnico, post LinkedIn, infografía HTML + comparativa. Con marca Ntizar David Antizar, sistema Aurora, atribución correcta.
version: "1.0.0"
tags: [pdf, artifacts, linkedin, html, aurora, david-antizar]
---

# PDF → 3 Artifacts (Estilo David Antizar)

## Descripción

Pipeline completo que, dado un PDF de informe técnico (especialmente del sector energía/transporte/infraestructuras), genera **3 artefactos** con el branding y estilo de David Antizar:

1. **Artefacto HTML** — resumen interactivo con Aurora Design System (CDN), liquid glass, colores azul+naranja, tablas, KPIs, comparativas
2. **Post LinkedIn** — estilo David Antizar: datos duros, tono provocador-constructivo, estructura con secciones, emojis estratégicos, tesis clara
3. **Nota de auditoría** — en `notes/` con fecha, hallazgos cuantificados, crítica metodológica

## No es para

- **Extracción de datos estructurados (JSON/CSV)** de PDFs → usar `pdf-llm-extraction` (nuevo paradigma validado: font analysis + LLM, 100% confianza)
- OCR de documentos escaneados → usar `ocr-quirurgico-pdf-md`
- Conversión PDF → Markdown navegable → usar `ocr-quirurgico-pdf-md`

## Atribución

Siempre poner **David Antizar** como autor. **Mastermind** es el agente ejecutor, David es el autor visible.

**Footer HTML EXACTO:** `Hecho con (L) por David Antizar` — NUNCA "Análisis por David Antizar", NUNCA "· vía Mastermind Agent", NUNCA "vía Mastermind". Literal exacto.

En el post LinkedIn: redacción en primera persona como si David lo escribiera. En las notas: "Autor: David Antizar".

## Diseño Aurora

**Usar Aurora Design System.** No duplicar configuración aquí — cargar el skill `aurora-design-system` que es la fuente de verdad del branding visual.

Reglas que este pipeline hereda de `aurora-design-system`:
- CDN obligatorio (`ntizar.css` + `ntizar.next.css`)
- Skin `aurora` por defecto (azul + naranja + liquid glass)
- Footer con atribución: `Hecho con (L) por David Antizar`
- Sin CSS custom suelto

Para voz de LinkedIn de David Antizar, ver `references/linkedin-voice.md`.
Para presupuestos de construcción, ver `references/budget-dashboard-pattern.md`.

## Pipeline

### Paso 1: Extraer PDF
```bash
python3 -c "
import fitz
doc = fitz.open('ruta.pdf')
text = ''
for page in doc: text += page.get_text()
print(text)
"
```

### Paso 2: Analizar contenido
Identificar:
- Contexto (institución, fecha, autores)
- Datos clave (KPIs, tablas, cifras)
- Hallazgos principales (3-5)
- Metodología usada
- Recomendaciones/conclusiones
- Crítica metodológica

### Paso 3: Generar HTML (Aurora)
Usar Aurora CDN. Estructura:
- Hero con `nz-gradient-text` y glass effect
- Cards KPI con clases Aurora + colores semánticos
- Tablas con `.nz-table`
- Highlight boxes con colores semánticos
- Comparativas €/km/tiempo por tipo
- Footer: "Análisis por David Antizar | Mastermind Agent"

### Paso 4: Generar Post LinkedIn
Estructura del post:
1. **Hook inicial** — dato provocador o afirmación fuerte
2. **Secciones con emojis** (📉 ⏱️ 💰 🚗 🏡)
3. **Datos duros** intercalados con análisis
4. **Conclusión/tesis clara** al final
5. **Hashtags** (#MovilidadSostenible #Ferrocarril etc.)
6. SIN tablas markdown en LinkedIn (no renderizan)

### Paso 5: Nota de auditoría
- Archivo: `notes/YYYY-MM-DD-tema-auditoria.md`
- Contexto, Hallazgos, Crítica metodológica, Valoración general

## ⚠️ PITFALL: Extracción de texto de PDFs — Fallback chain

Cuando `pdftotext` (poppler-utils) no está disponible en el PATH, usar esta cadena de fallback:

### Paso 1: Verificar herramientas CLI disponibles
```bash
which pdftotext mutool pdfgrep  # Si ninguno responde → usar Python
```

### Paso 2: Usar `fitz` (PyMuPDF) vía Python
```bash
python3 -c "
import fitz
doc = fitz.open('ruta.pdf')
text = ''
for page in doc: text += page.get_text()
print(text[:10000])  # Limitar para no saturar
"
```

**Ventajas de fitz:**
- Extrae texto página por página (útil para PDFs grandes)
- No requiere instalación adicional (ya viene en el entorno)
- Funciona con PDFs generados por Acrobat PDFMaker (donde pdf.js falla)

### Paso 3: Guardar texto completo para parsing posterior
```bash
python3 -c "
import fitz
doc = fitz.open('ruta.pdf')
with open('/tmp/pdf_text.txt', 'w') as f:
    for page in doc: f.write(page.get_text())
"
```

### Herramientas Python disponibles (verificar con `pip list | grep -i pdf`)
- `fitz` (PyMuPDF) — **PRIMERA OPCIÓN**, más fiable
- `pdfplumber` — buena para tablas
- `PyPDF2` — fallback básico
- `pdfminer` — más lento pero preciso

### ⚠️ Limitaciones conocidas
- **PDFs generados por Acrobat PDFMaker:** pdf.js en navegador devuelve 0 palabras. Usar fitz siempre.
- **PDFs con imágenes solo (sin texto):** Necesitan OCR (tesseract, liteparse).
- **PDFs muy grandes (>300 páginas):** Extraer por secciones, no todo junto.

## Verificación final
- [ ] HTML carga correctamente con Aurora CDN
- [ ] Post LinkedIn tiene voz de David Antizar
- [ ] Nota guardada en `notes/`
- [ ] Atribución: "Análisis por David Antizar" siempre visible
- [ ] Aurora skin aurora activa (azul+naranja)
