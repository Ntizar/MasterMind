# PLANDEMOVILIDAD — Arquitectura y patrones

## Contexto

PLANDEMOVILIDAD es una aplicación vanilla JS de ~22K líneas en 32 módulos que genera
Planes de Movilidad Sostenible al Trabajo (PMST/PTST) conforme a la Ley 8/2021.
Genera informes de 60-80 páginas con datos reales de APIs públicas.

## Reglas de oro

### 1. Namespace `window.pmstApp`

El HTML usa `onclick="window.pmstApp.xxx()"` en toda la aplicación.

```javascript
// ✅ SIEMPRE: Exponer funciones al namespace
window.pmstApp = {
    guardarCentro() { ... },
    calcularDiagnostico() { ... },
};

// ❌ NUNCA: Dejar funciones sin exponer
function guardarCentro() { ... }  // ← HTML no puede llamarla
```

**Nunca eliminar funciones del namespace** — el HTML las llama directamente.

### 2. Estado centralizado

```javascript
// ✅ SIEMPRE: window.pmstApp.appState como fuente única de verdad
window.pmstApp.appState.empleados.push(nuevoEmp);

// ❌ NUNCA: Variables globales paralelas
let empleadosLocales = [];  // ← ROMPE sincronización
```

### 3. Categorización de archivos

**SAGRADO (no tocar sin aprobación):**
- `css/style.css` — Selectores por clase, no ID
- `index.html` — Estructura DOM, class names, IDs, CDN imports
- `js/config.js` — Constantes, endpoints API, factores MITECO
- `js/utils.js` — Funciones puras (Haversine, formateo)
- `js/graficas.js` — Chart.js (referencia IDs de canvas específicos)
- `js/export.js` — Lógica PDF/DOCX/ZIP con atribución

**MODIFICABLE con cuidado:**
- `js/app.js` — Orquestador, afecta flujo completo
- `js/mapa.js` — Leaflet, isocronas, capas
- `js/diagnostico.js` — Cálculos afectan dashboard, export, informe
- `js/survey.js` — Encuesta RGPD, IndexedDB

**LIBRE (crear/modificar):**
- `js/api-*.js` — Módulos de APIs externas
- `js/medidas.js`, `js/dafo.js`, `js/objetivos.js`
- `js/state.js`, `js/informe.js`
- `data/*.js` — Datos estáticos

### 4. CSS

```css
/* ✅ SIEMPRE: Selectores de clase */
.app-header { ... }
.kpi-card { ... }

/* ❌ NUNCA: IDs para estilos */
#app-header { ... }  /* ← PROHIBIDO */
```

### 5. Atribución

```javascript
// SIEMPRE incluir en todos los documentos generados
const ATTRIBUTION = 'Hecho con ❤️ por David Antizar';
```

## Fuentes de datos verificadas

| Fuente | Uso | URL |
|--------|-----|-----|
| MITECO 2024 | Factores CO2e | miteco.gob.es |
| NAP DGT | Paradas transporte | nap.dgt.es |
| Overpass API | Infraestructura ciclista | overpass-api.de |
| OpenRouteService | Isocronas | api.openrouteservice.org |
| GBFS | Bicis compartidas | APIs ciudad por ciudad |
| Nominatim | Geocodificación | nominatim.openstreetmap.org |

**REGLA:** N/D > dato inventado. Solo APIs verificadas.

## IndexedDB Stores

| Store | Key | Descripción |
|-------|-----|-------------|
| `empresas` | `id` | Catálogo de empresas |
| `datosEmpresa` | `empresaId` | Datos completos por empresa |
| `respuestas` | `id` | Respuestas raw de encuestas |

## Pitfalls críticos

1. **IA desconectada:** `ia-generativa.js` genera textos pero `report.js` nunca los lee
2. **Canvas/Leaflet en PDF:** weasyprint no renderiza JS. Rasterizar antes con html2canvas
3. **report.js es gigante:** 3938 líneas, 216KB. Refactorizar en módulos más pequeños
4. **Múltiples versiones de state.js:** `app.js` tiene v2, `state.js` tiene v3. Unificar
5. **API keys en código:** Mover a variables de entorno
6. **Duplicados en IndexedDB:** El demo script puede crear entradas duplicadas

## Dependencias conocidas

```
index.html → css/style.css (selectores de clase)
index.html → js/app.js (onclick → window.pmstApp)
index.html → CDN: Leaflet 1.9.4, Chart.js 4.4.0, JSZip 3.10.1

js/app.js → js/config.js (import { CONFIG })
js/app.js → js/utils.js (utilidades)
js/app.js → js/graficas.js (crear gráficas)
js/app.js → js/mapa.js (iniciar mapa)
js/app.js → js/diagnostico.js (calcular indicadores)

js/graficas.js → index.html canvas IDs (chart-modal, chart-co2e, etc.)
js/mapa.js → index.html div IDs (mapa-principal, dashboard-map)
```

## Proceso de cambio

1. Identificar categoría del archivo (SAGRADO / MODIFICABLE / LIBRE)
2. Leer el archivo completo para entender contexto
3. Verificar dependencias
4. Hacer el cambio mínimo y preciso
5. Probar el flujo completo afectado
6. Actualizar documentación si afecta arquitectura