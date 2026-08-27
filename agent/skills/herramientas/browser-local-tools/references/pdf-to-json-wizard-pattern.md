# PdfToJson — Patrón Wizard multi-paso con LLM

Arquitectura de referencia para herramientas HTML que extraen datos estructurados de archivos usando LLM.

**Repo:** github.com/Ntizar/PdfToJson (privado)
**Creado:** 2026-06-27

## Arquitectura en 7 pasos

```
1. Configuración → API Key, modelo, proyecto
2. Cargar PDFs → Drag & drop, PDF.js, lista de archivos
3. Analizar → Auto-learn schema desde fuentes
4. Schema → Editor visual, import/export
5. Procesar → LLM batch con progreso, ETA, pausa
6. Validar → Confianza por campo, detalle, edición
7. Exportar → JSON consolidado, individual, CSV
```

## Componentes clave

### PDF.js con font metadata

```javascript
pdfjsLib.GlobalWorkerOptions.workerSrc = ''; // file:// compatible
const content = await page.getTextContent();
// items[i].transform[3] = font size
// items[i].fontName = detect bold
```

### Auto-learn: detección de headings

1. Encontrar body size (fuente más frecuente por longitud de texto)
2. Headings = fuente > bodySize + 1 AND (bold OR bodySize + 3)
3. También: regex `^\d+[\.\)]\s+[A-Z]` para secciones numeradas
4. Cluster across 3-5 sample PDFs
5. Secciones en 2+ PDFs → candidatas a schema

### LLM extraction

- Endpoint: `POST /v1/chat/completions`
- temperature: 0.1
- Prompt: schema JSON + texto truncado a 30K chars
- Response: parse JSON, limpiar fences, fallback regex

### Validation (3 niveles)

1. **Type check:** date format, number parse, array type
2. **Required check:** required fields must not be null
3. **Confidence score:** validFields / totalFields

### Schema storage

```javascript
// localStorage
localStorage.setItem('pdftojson_schemas', JSON.stringify(allSchemas));
// Import/export as JSON files
```

## CSS: Kaizen para tools de procesamiento

- Flat corporativo, sin glass, sin sombras
- Colores: azul #1A4488, rojo #CB1823
- Clases: kz-header, kz-btn-primary, kz-progress, kz-dropzone
- Responsive: grid 1 col mobile, 2 col tablet

## Progress tracking

Mostrar siempre en batch processing:
- % completado (barra animada)
- Fase actual (texto)
- ETA (promedio × restantes)
- Estadísticas (ok/warn/error)
- Log (últimas ops)
- Pausa/Reanudar + Cancelar

## Pitfalls

- PDF.js workerSrc='' obligatorio para file://
- Acrobat PDFMaker genera PDFs que pdf.js no lee → fallback a LibreOffice
- LLM a veces devuelve ```json fences → regex cleanup
- Throttling: 1.5-2s entre llamadas para 1000+ PDFs
- localStorage persiste schemas entre sesiones pero no entre dispositivos
