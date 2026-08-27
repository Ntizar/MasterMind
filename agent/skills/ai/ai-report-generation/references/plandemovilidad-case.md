# PLANDEMOVILIDAD — Case Study

## Project Overview
- **Repo**: Ntizar/PLANDEMOVILIDAD (GitHub Pages: ntizar.github.io/PLANDEMOVILIDAD/)
- **Purpose**: PMST/PTST generator for Spanish companies (Ley 8/2021)
- **Tech**: Vanilla JS ES6 modules, Leaflet 1.9.4, Chart.js 4.4, JSZip, jsPDF
- **Architecture**: Client-side SPA, no backend, data in appState

## What Was Built

### 1. CSS Rewrite (Fase 1)
- 992 lines, no orphan selectors
- Created NORMAS.md (224 lines) defining "sacred" (immutable) vs "modifiable" files
- SPEC.md v3.0 (756 lines) with 5-phase rewrite plan

### 2. Module Reconnection (Fase 2)
- **main.js**: Rewritten as dynamic import wrapper with cache-busting `?v=N`
- **dafo.js**: Fixed `indicadoresParked?.consejo?.includes()` (optional chaining)
- **diagnostico.js**: Added employee-derived modal split fallback when no survey
- **objetivos.js**: Replaced `state.encuesta`/`state.empresa` references with parameter defaults
- **Inline script**: Rewritten with showTab(), 25 pmstApp functions, render helpers

### 3. KPI Multi-Year Matrix (New Feature)
- 10 KPIs × N years, editable inputs, trend arrows
- goodDirection inversion for CO₂ and motorizado
- Auto-fill from diagnostic, add year, CSV export
- Chart.js evolution line chart

### 4. Full Report Generator (Fase 4)
- **report.js**: 3,850 lines, 22 chapters
- ~55-60 printed pages (164KB HTML)
- 31 tables, 123 paragraphs, 55 lists
- CSS: A4 print, page-break-before, blue/orange headers

### 5. AI Demo (Prototype)
- **ai-demo.html**: Interactive demo showing prompt + AI response per chapter
- 8 chapters with example prompts and generated content
- Architecture diagram, data source table, sidebar navigation

## Architecture Decisions

### ES Module Cache-Busting
Browsers aggressively cache ES modules loaded via `import()`. Even with Python http.server (no cache headers), the browser caches module URLs. Solution: append `?v=N` to ALL import paths, increment on each change.

### Employee-Derived Fallback
When no survey exists, derive modal split from employee census:
- `distanciaOficina <= 5` → coche
- `distanciaOficina > 5` → transporte público
- `teletrabajo > 0` → teletrabajo
- Rest → moto/bicicleta (split 60/40)

### Report Generation Architecture
- Each chapter = independent function generating HTML
- Functions receive `appState` and extract relevant data
- Template literals with variables from appState
- All chapters wrapped in `<section class="chapter">` with CSS page breaks
- CSS print stylesheet for A4 format

## Data Flow
```
User Input (forms) → appState (in-memory)
    ↓
Diagnostic Calculation (diagnostico.js)
    ↓
DAFO Derivation (dafo.js)
    ↓
Measures Generation (medidas via DAFO)
    ↓
Objectives SMART (objetivos.js)
    ↓
Report Assembly (report.js) → HTML Document
    ↓
Export (export.js) → PDF / DOCX / ZIP
```

## APIs Implemented (Fase 3B)
- **GBFS** (`js/api-gbfs.js`, 8.2KB): 8 sistemas España (BiciMAD, Bicing, Valenbisi, Sevici...). Auto-detección por proximidad, parser v2.3+v3.0, cache en memoria. Sin API key.
- **ORS** (`js/api-ors.js`, 6.1KB): Isochronas reales (driving-car, cycling-regular, foot-walking). Key en localStorage del usuario. Fallback simulado: polígono 48 puntos con jitter. Stagger 400ms.
- **Nominatim** (`js/api-nominatim.js`, 5.7KB): Geocodificación directa+inversa, POIs vía Overpass API, rate limit 1.1s, detección de ciudad.
- **Report enrichment** (`js/report-enrich.js`): `enrichAppWithAPIs()` carga datos reales ANTES de generar informe. GBFS→40 estaciones BiciMAD, Nominatim→20 POIs + info centro, ORS→9 isócronas multi-modo.
- **MITECO 2024**: CO₂ emission factors by transport mode (embebido en diagnostico.js)

## Key Pitfalls Found
1. ES module caching requires `?v=N` on all imports
2. `const` in inline module scope shadows previous declarations
3. Template literal variables must be declared in function scope
4. Optional chaining needed when data may be undefined
5. `renderKpiMatrix` must be exposed via `window.pmstApp` for console testing
6. **Static ES module imports execute BEFORE inline script body** — modules assigned to `window.pmstApp` get overwritten by inline script's `window.pmstApp = {...}`. Fix: assign API modules AFTER appState is defined, or use dynamic imports.
7. **Lazy map init**: Leaflet + GBFS + paradas = ~500KB. Use `await import()` in showTab() to load on first click, not on page load.
8. **Browser-to-disk saving**: No server endpoint? Start a temp Python HTTP receiver, POST from browser, receiver writes to disk.
9. **Static map PDF pipeline**: WeasyPrint can't render Leaflet JS maps. Solution: `staticmap` Python lib generates static PNG/JPG from OSM tiles, embed as base64 `<img>`, then WeasyPrint PDF. See `references/staticmap-pdf-pipeline.md`.
10. **Realistic isochrones**: Simple jitter circles look fake. Use road axes (8 directions with extension factors) + urban barriers (rivers -40%, railways -25%) + 3-frequency sine variation. 48-point polygon. See `references/realistic-isochrone-simulation.md`.
11. **AI commentary after visualizations**: After each map in the report, add a styled block (`#f0f9ff` background, blue left border) with contextual analysis: findings, barriers detected, recommendations. Makes the report feel "AI-powered" rather than just data dump.
12. **Report size expectations**: Spanish PMST/PTST should be 60-80 pages. 10 pages is a draft, not a professional report. More data, more tables, more analysis, more AI commentary = bigger report.
