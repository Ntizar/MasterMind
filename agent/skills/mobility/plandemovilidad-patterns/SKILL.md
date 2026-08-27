---
name: plandemovilidad-patterns
description: Patrones de proyecto PLANDEMOVILIDAD v3.0 — generador de Planes de Movilidad Sostenible (PMST/PTST). Arquitectura, módulos, helpers, convenciones, archivos sagrados, clases CSS.
---

# PLANDEMOVILIDAD — Patrones de Proyecto

## Identidad
- **Proyecto:** PLANDEMOVILIDAD v3.0 — Generador de Planes de Movilidad Sostenible al Trabajo (PMST/PTST)
- **Usuario/Dueño:** David Antizar (Ntizar)
- **Stack:** Vanilla JS + IndexedDB + Leaflet + Chart.js + WeasyPrint (servidor para PDF)
- **Propósito:** Generar informes profesionales de 60-80 páginas que cumplen la Ley 8/2021 de movilidad sostenible

## Estructura del Proyecto
```
PLANDEMOVILIDAD/
├── index.html              ← Entry point, importa todos los módulos como type="module"
├── style.css               ← SAGRADO — diseño general
├── deploy.sh               ← Despliegue
├── js/
│   ├── config.js           ← SAGRADO — config global, constantes
│   ├── utils.js            ← SAGRADO — utilidades
│   ├── graficas.js         ← SAGRADO — gráficas Chart.js
│   ├── export.js           ← SAGRADO — export a PDF/DOCX/ZIP
│   ├── informe.js          ← Orquestador del informe
│   ├── ia-generativa.js    ← IA generativa (qwen3.6 vía api.nan.builders)
│   ├── report.js           ← SHIM — re-exporta desde js/report/index.js
│   ├── report-maps.js      ← Mapas Leaflet para el informe HTML
│   └── report/             ← Módulos del generador de informe
│       ├── helpers.js      ← CONSTANTES + helpers (fmt, pct, safe, getCO2e...)
│       ├── css.js          ← CSS embebido para el informe HTML
│       ├── index.js        ← Orquestador: generarInformeCompleto(app)
│       ├── 00-portada.js   ← 22 capítulos (00-21)
│       └── ...
```

## Archivos SAGRADOS (NO MODIFICAR sin permiso)
- `style.css`, `index.html`, `config.js`, `utils.js`, `graficas.js`, `export.js`

## Arquitectura del Generador de Informe

### Flujo de datos
1. `export.js` → `generarInformeCompleto(app)` (importado de `./report.js`)
2. `report.js` re-exporta desde `./report/index.js`
3. `index.js` importa 22 capítulos + helpers, ensambla HTML completo
4. Cada capítulo importa helpers desde `./helpers.js`
5. HTML completo → blob → WeasyPrint → PDF ~70 páginas

### Convenciones de código
- Cada capítulo < 200 líneas. Si supera, extraer sub-funciones internas.
- Los capítulos NO se llaman entre sí. Solo importan helpers.
- helpers.js NO importa nada. Nivel más bajo de dependencia.
- css.js NO importa nada.
- index.js es el único que importa capítulos directamente.
- `export function generarInformeCompleto(app)` = interfaz pública.

### Helpers principales
```js
fmt(num, decimales=1)      // Formato número español (1.234,5)
pct(num)                   // Porcentaje (45,2%)
fechaLarga()               // "14 de julio de 2026"
fechaCorta()               // "2026-07-14"
safe(obj, path, default)   // Acceso seguro por ruta de puntos
safeNum(obj, path, default)
safeArr(obj, path)
getEmpleados(app)          // Extrae empleados de app.empleados
getModalSplit(app)         // Calcula reparto modal
getCO2e(app)               // Calcula huella de carbono
getResumen(app)            // Nivel de sostenibilidad + % motorizado + % sostenible
getCSS()                   // String CSS completo A4
```

### Factores de emisión CO2e (kg/km)
Coche particular: 0.192 | Compartido: 0.115 | Bus urbano: 0.089 | Bus interurbano: 0.045
Metro: 0.035 | Cercanías: 0.033 | Tranvía: 0.029 | Bici: 0.000 | Bici eléctrica: 0.006
A pie: 0.000 | VMP: 0.015 | Teletrabajo: 0.010

### Regla crítica
**N/D > dato inventado** — Si API no devuelve datos, mostrar "Sin datos" o "N/D". NUNCA inventar.

## Clases CSS del informe
- `.chapter` / `.chapter-title` / `.section-title` / `.subsection-title`
- `.highlight-box` (.warning, .success, .danger)
- `.kpi-grid` / `.kpi-card` (.accent, .green)
- `.dafo-grid` / `.dafo-box` (.fortalezas, .debilidades, .oportunidades, .amenazas)
- `.cronograma-row` / `.cronograma-bar` / `.cronograma-header`
- `.badge` (.alta, .media, .baja)
- `.firma-grid` / `.firma-box`
- `.portada` / `.indice` / `.indice-item`
- `.informe-footer`
- Utilidades: `.page-break`, `.no-break`, `.text-center`, `.text-sm`, `.font-bold`, `.text-blue`, `.text-orange`

## Navegación
- Sin backend. Todo frontend estático + APIs externas.
- IA: `api.nan.builders/v1` con key de localStorage.
- PDF: HTML → WeasyPrint (servidor).
- Mapas: Leaflet + OSM + GBFS + POIs + isocronas.
- Canvas/Leaflet NO renderizan en PDF.