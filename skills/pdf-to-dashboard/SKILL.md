---
name: pdf-to-dashboard
description: Extraer datos estructurados de PDFs complejos (presupuestos, informes tecnicos, documentos de construccion) y generar dashboards HTML interactivos con Aurora Design System. Pipeline completo de extraccion a visualizacion.
version: "1.0.0"
tags: [pdf, dashboard, presupuesto, construccion, datos, html, aurora, visualizacion]
---

# PDF-to-Dashboard — Extraccion de datos estructurados de PDFs complejos

## Cuándo usarlo

- El usuario adjunta un PDF con datos tabulares/estructurados (presupuestos, informes tecnicos, documentos de construccion)
- El usuario pide "convertir en herramienta HTML", "crear dashboard", "visualizar el presupuesto"
- El documento tiene capitulos, partidas, importes, desgloses financieros
- Se necesita extraer datos numeric y generar visualizacion interactiva

## No es para

- Informes institucionales/regulatorios (usar `documentos-institucionales`)
- Propuestas de diseno web (usar `pdf-to-landing`)
- PDFs academicos con formulas (usar `documentos-institucionales` con PyMuPDF)
- Resumenes simples sin estructura tabular

## Pipeline completo

### Fase 0 — Preparacion del entorno

**Paso 1: Intentar herramientas CLI primero**
```bash
# pdftotext (poppler-utils)
pdftotext -layout archivo.pdf - | head -100

# strings (fallback rapido)
strings archivo.pdf | head -50
```

**Paso 2: Si CLI falla, intentar Python con fitz (PyMuPDF)**
```bash
python3 -c "import fitz; doc = fitz.open('archivo.pdf'); print(len(doc), 'paginas')"
```

**Paso 3: Si Python no tiene fitz ni pip, usar pdfplumber del venv de Hermes**
```bash
# pdfplumber ya instalado en /opt/hermes/.venv (NO requiere pip)
/opt/hermes/.venv/bin/python3 -c "import pdfplumber; print('ok')"
```

**Paso 4: Si nada funciona, usar Node.js con pdfjs-dist**
```bash
cd /root/workspace/pdf-to-landing
npm install pdfjs-dist@3.11.174 --save
```

> **Pitfall critico:** `pdf-parse@2.4.5` tiene API incompatible. Usar `pdfjs-dist@3.11.174` que es mas estable.

### Fase 1 — Extraccion del PDF

#### Opcion A: PyMuPDF (recomendado si disponible)
```python
import fitz
doc = fitz.open('/ruta/al/pdf.pdf')
pages_text = []
for i, page in enumerate(doc):
    pages_text.append(page.get_text())
```

#### Opcion B: pdfjs-dist (fallback robusto)
```javascript
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { getDocument } = require('pdfjs-dist/legacy/build/pdf.mjs');

const pdf = await getDocument('/ruta/al/pdf.pdf').promise;
const pages = [];
for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const textContent = await page.getTextContent();
    const text = textContent.items.map(item => item.str).join('');
    pages.push({ page: i, text });
}
require('fs').writeFileSync('/tmp/pages.json', JSON.stringify(pages));
```

> **Pitfall:** Usar `execute_code` para scripts complejos, no `terminal()` con scripts inline. Scripts largos fallan con timeout.

### Fase 2 — Analisis de estructura

Leer las primeras paginas para entender el patron de texto:
- Codigo de partida + descripcion + unidad + cantidad + precio → importe
- Encabezados de capitulo con importes
- Tablas resumen con totales por capitulo

### Fase 3 — Parsing estructurado

#### Patron para presupuestos de construccion

```
CAPÍTULO 1 — MOVIMIENTO DE TIERRAS
  01.01 — Desmontaje
    m23E02AM010 | Desmonte de terreno... | m3 | 150,00 | 2,50 | 375,00

TOTAL CAPÍTULO 1: 3.375,00 €
```

**Regex clave:**
```javascript
// Codigo de partida
const codePattern = /\b([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)\b/;

// Importes con formato español (1.234,56)
const amountPattern = /(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)/;

// Linea completa: codigo | descripcion | unidad | cantidad | precio | importe
const linePattern = /([A-Z0-9]+)\s*\|\s*(.+?)\s*\|\s*(\w+)\s*\|\s*(\d[\d.,]*)\s*\|\s*(\d[\d.,]*)\s*\|\s*(\d[\d.,]*)/;
```

### Fase 4 — Generacion del HTML Dashboard

**Usar Aurora Design System** (skill `aurora-design-system`):
- CDN obligatorio: ntizar.css + ntizar.next.css + packs necesarios
- Skin: aurora, Theme: light
- Componentes glass-liquid para tarjetas de capitulo
- Graficos con Chart.js o ApexCharts
- Navegacion por capitulos con tabs
- Links clicables a paginas especificas del PDF

### Fase 5 — Optimizacion y entrega

- Solo extraer texto de paginas donde aparecen partidas reales
- Guardar como `pageTextMap` en el JS del HTML
- Tamaño objetivo: <200KB HTML autocontenido

## Presupuestos CYPE Arquímedes — Patrones especificos

Los PDFs generados por CYPE Ingenieros (Arquimedes) tienen estructura fija:

- **Pagina 1:** "Presupuesto y medición" (resumen minimo, sin datos utiles)
- **Paginas 2-N-1:** Detalle de cada presupuesto parcial (partidas con mediciones)
- **Pagina N (ultima):** Resumen final con totales por capitulo + texto en letras

### Extraccion de resumen final (pagina N)
```python
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[-1]  # Ultima pagina
    text = page.extract_text()
    # Pattern: "1. MOVIMIENTO DE TIERRAS .............................… 873,19"
    pattern = r'(\d+)\.\s+(.+?)\.{2,}…?\s+([\d.,]+)'
```

### Extraccion de detalle por capitulo
```python
# Buscar cabeceras: "Presupuesto parcial nº 1 MOVIMIENTO DE TIERRAS"
chapter_match = re.search(r'Presupuesto parcial nº\s+(\d+)\s+(.+)', text)
# O: "CAPÍTULO 01 MOVIMIENTO DE TIERRAS"
chapter_match = re.search(r'CAPÍTULO\s+(\d{2})\s+(.+)', text)
```

### Formato de partidas CYPE
```
1.1  m23E02AM010  m2  Desbroce y limpieza...
Uds.  Largo  Ancho  Alto  Subtotal
197,80          197,80
Total m2 ............:  197,80  0,48  94,94
```

### CYPE vs Presto — diferencias clave
- **CYPE Arquímedes:** usa cabeceras "Presupuesto parcial nº X NOMBRE"
- **Presto:** usa cabeceras "CAPÍTULO X NOMBRE" con ceros a la izquierda (01, 02...)
- **CYPE:** el resumen final está en la ÚLTIMA página del PDF
- **CYPE:** las mediciones usan punto como separador de miles y coma decimal (1.234,56)
- **CYPE:** las partidas pueden tener subpartidas con referencias de planos (VC.T-2.1 [P16-P15])

### ⚠️ Normalizacion de claves entre presupuestos
CYPE usa `Cap-1`, `Cap-2`... pero ofertas Presto pueden usar `Cap-01`, `Cap-02`.
**Siempre normalizar:** `offer_key = f"Cap-{cap_num.zfill(2)}"` para matching.

### ⚠️ PDFs de constructoras — estructura variable
Los PDFs de ofertas de constructoras (Trevicon, etc.) pueden tener:
- Portada con datos de la empresa
- Resumen en paginas 2-3
- Detalle a partir de pagina 4
- Menos paginas que el PEM base (a veces omiten capítulos)
**Estrategia:** extraer primero paginas 1-3 para entender la estructura, luego procesar el resto.

## Pitfalls criticos

### 🔴 pdfjs-dist: API mismatch con v2.x

`pdf-parse@2.4.5` tiene API incompatible. Usar `pdfjs-dist@3.11.174`.

### 🔴 No usar `terminal()` para scripts Node.js largos

Scripts >50 lineas o con async/await fallan con timeout. Usar `write_file` + `node script.js` o `execute_code`.

### 🔴 PDFs con fuentes embebidas

Si `pdftotext` y `strings` no devuelven nada legible, el PDF usa CMap/ToUnicode. Ir directo a PyMuPDF o pdfjs-dist.

### 🔴 Parsing de presupuestos de construccion

Los presupuestos tienen:
- Codigos alfanumericos largos (ej: `m23E02AM010`)
- Subpartidas anidadas (capitulo → subcapitulo → partida)
- Precios unitarios, cantidades, importes en columnas
- Totales parciales por capitulo

**Estrategia:** Extraer primero paginas de resumen (2-3), luego capitulo por capitulo.

### 🔴 Numericos con formato español

`1.234,56` → reemplazar: `parseFloat(str.replace(/\./g, '').replace(',', '.'))`

## Referencias

- `references/pdf-extraction-nodejs-pdfjsdist.md` — Tutorial completo con pdfjs-dist@3.11.174
- `references/budget-parsing-patterns.md` — Patrones de parsing para presupuestos de construccion españoles
- `references/aurora-dashboard-template.md` — Plantilla base HTML con Aurora para dashboards
- `budget-comparison` — Skill dedicado para comparar presupuestos de obra (PEMs) entre referencia y ofertas de constructoras