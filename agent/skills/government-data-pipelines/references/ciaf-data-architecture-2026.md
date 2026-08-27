# CIAF — Arquitectura de Datos (2026-06-26)

## Inventario verificado

| Tipo | Cantidad | Ubicación |
|------|----------|-----------|
| Informes (PDFs fuente) | 277 | `/root/workspace/CIAF/YYYY/*.pdf` |
| Informes (JSONs en visor) | 270 | `data/reports/YYYY.json` en CIAF-visor |
| Memorias | 17 | `data/memorias/YYYY.json` (2008-2024) |
| Normativa | 7 | `/root/workspace/CIAF/normativa/` |
| **Total PDFs** | **301** | |

**⚠️ Diferencia 277 vs 270:** El repo CIAF tiene 277 PDFs descargados, pero el visor GitHub Pages tiene 270 JSONs. La diferencia son PDFs duplicados o con nombres que no encajan en el patrón de parseo. Verificar al re-parsear.

### Distribución por año (informes)
2007:4, 2008:53, 2009:43, 2010:28, 2011:24, 2012:22, 2013:23, 2014:14, 2015:10, 2016:11, 2017:12, 2018:2, 2019:3, 2020:3, 2021:6, 2022:5, 2023:3, 2024:3, 2025:1

## Tres eras de formato

### Era 1: Pre-RD 810/2007 (2007-2008)
- **Normativa:** Sin formato estandarizado
- **Secciones:** Variables (Antecedentes, Hechos, Análisis)
- **Características:** Formato libre, más narrativo
- **Parser:** Difícil — requiere detección por contenido

### Era 2: RD 810/2007 (2009-2013)
- **Normativa:** Real Decreto 810/2007
- **Secciones:** 1-5 (Resumen, Descripción del accidente, Análisis, Conclusiones, Recomendaciones)
- **Características:** Estructura más definida pero menos rigidizada

### Era 3: RD 623/2014 (2014-2025)
- **Normativa:** Real Decreto 623/2014 (Art. 15)
- **Secciones:** 0-6 (Abreviaturas, Resumen del accidente, Descripción, Análisis, Conclusiones, Recomendaciones, Anexos)
- **Características:** Estructura más detallada, incluye abreviaturas y anexos

## Arquitectura propuesta (David Antizar)

### Fuente de verdad: JSON particionado
```
ciaf-web/
├── data/
│   ├── index.json              ← ~50KB, todos los IDs + metadatos mínimos
│   ├── reports/
│   │   ├── 2007.json
│   │   ├── ...
│   │   └── 2025.json
│   ├── relations.json          ← entidades × informes × recomendaciones
│   ├── memorias.json           ← resúmenes anuales
│   └── normativa.json          ← referencias normativas
├── images/
│   ├── 2007/
│   │   └── IF-01-2007-fig01.png
│   └── ...
├── scripts/
│   ├── parser-v4.py            ← parser multi-formato
│   ├── sync.py                 ← auto-import desde web
│   └── coherence-check.py      ← verificar consistencia memorias↔informes
└── index.html                  ← dashboard principal
```

### Memorias anuales (verificado 2026-06-26)
- 17 memorias (2008-2024), PDFs en `pdfs/memorias/`
- JSONs en `data/memorias/YYYY.json` — datos reales extraídos con PyMuPDF
- **NO existe memoria 2007** (aunque hay 4 informes de ese año)
- **NO existe memoria 2025** (año incompleto) — eliminar JSON fabricado
- Alcance: memorias = TODOS los incidentes; informes = solo los investigados

### Verificaciones de frontend (verificado 2026-06-26)
- Enlace PDF informe: `enlaces.pdf_local` → `pdfs/YYYY/YYYY-NNN-MMDD-if.pdf`
- Enlace PDF memoria: `pdfs/memorias/CIAF_Memoria_YYYY.pdf`
- KPI entidades: iterar TODO el array `entities`, no solo `entities[0]`
- Selector memorias: solo años con PDF real (2008-2024)

### Parser v2 (verificado 2026-06-26)
- **Script:** `scripts/parse_reports_v2.py` en repo CIAF-visor
- **Métricas:** 99% fechas, 100% títulos, 96.7% conclusiones, 95.2% recomendaciones
- **Enfoque:** Extracción por páginas (no regex sobre texto completo)
- **4 patrones de título:** Pre-2009 (fecha en título), 2015-era ("CIAF Nº"), 2019-era ("expediente nº"), 2022+ ("Nº X/XXXX — Descripción")
- **Campos en español:** `conclusiones`, `recomendaciones` (NO `conclusions`/`recommendations`)
- **Validación:** después de parsear, verificar que cada JSON tiene campos `conclusiones` y `recomendaciones` (no null para >95% de informes)

### Relaciones entre entidades
- **Empresas:** Renfe, Adif, operadores, fabricantes
- **Causas:** Señalización, error humano, vía, material rodante
- **Recomendaciones:** A quién, qué se recomienda, estado de implementación
- **Ubicaciones:** Estaciones, líneas, pk (punto kilométrico)

### Características del visor
- **Mapa:** Leaflet con todas las líneas férreas + markers de informes
- **Dashboard:** Filtros multi-selección (año, empresa, causa, gravedad)
- **Resumen ejecutivo:** KPIs, gráficos Chart.js de evolución temporal
- **Memorias:** Sección dedicada para comparar año a año
- **Coherencia:** Warning cuando memorias e informes no coinciden
- **Auto-import:** `sync.py` descarga nuevos PDFs y los procesa

## Fuentes de datos verificadas

| Fuente | Patrón URL | Estado |
|--------|------------|--------|
| Informes 2017-2025 | `infofin-YYYY` | ✅ Verificado |
| Informes 2009-2016 | `/MFOM/.../YYYY/` | ✅ Verificado |
| Memorias | `memoriasanuales` | ✅ Verificado |
| Normativa | `comodin/recursos/` | ✅ Verificado |
