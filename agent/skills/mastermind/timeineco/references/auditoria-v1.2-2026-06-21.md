# Auditoría TimeIneco v1.2 — 21 de junio 2026

## Contexto

David Antizar pidió una auditoría experta de software de `https://timeineco-ntizar-ntizar.apps.nan.builders/` con plan en 3 fases para MVP el lunes.

## Bugs encontrados y corregidos

### 🔴 Críticos (MVP dañados)

1. **`cargarDatos()` no cargaba GTFS** → `buscarParadasCercanas()` devolvía `{paradas:[], lineas:[], resumen:null}` → DOCX se generaba sin datos de transporte público.
   - **Fix:** Añadir `fetch('/data/gtfs-cache.json')` en el `Promise.all` de `cargarDatos()`.

2. **`suavizarPoligono()` era fantasma** → Comentario decía "cada 3 puntos" pero el código era `for (let i = 0; i < n; i++)` → 72 puntos pasaban sin reducción.
   - **Fix:** Cambiar a `for (let i = 0; i < n; i += 3)` → 72 → ~24 vértices.

3. **jsPDF + html2canvas + autotable muertos** → 280 KB de scripts CDN que no se usan. El informe DOCX es la única salida.
   - **Fix:** Eliminar los 3 `<script>` del HTML + simplificar `capturarMapa()` en map.js.

4. **3 imports dinámicos duplicados de `gtfs-engine.v7.js`** → `await import()` dentro de funciones, se cargaba dos veces.
   - **Fix:** Import estático único al principio de `main.js` con `findStopsNear` y `limpiarGTFS`.

5. **Nested loop O(n²) en `buscarCP()`** → `Object.entries(_precios)` (127) × `_cpData.find()` (299) = 38K iteraciones por clic.
   - **Fix:** `_preciosMap = new Map(...)` y `_cpMap = new Map(...)` → lookup O(1).

### 🟡 Graves

6. **`renderizarPanelNAP` llamado 2 veces** → Una en `mostrarResultados()`, otra en `handleCalcular()`.
   - **Fix:** Una sola llamada en `handleCalcular()`.

7. **`capturarMapa()` en map.js** usaba `html2canvas` que fue eliminado.
   - **Fix:** Función devuelve `null`.

### 🟢 Leves

8. **CSS versionado desincronizado** → `style.css?v=8` vs `main.js?v=12`.
   - **Fix:** Unificar a `v=12`.

9. **Modos extra (bus, metro, tranvía)** → Sobran para MVP del lunes.
   - **Fix:** Quitar del HTML, dejar solo 🚗 🚲 🚶.

## Plan 3 fases

| Fase | Qué | Cuándo |
|------|-----|--------|
| 1 | Apagar incendios: GTFS loading, suavizado real, scripts muertos, import único | Hoy (3h) |
| 2 | MVP real: 3 modos, cache Maps, debounce 200ms | Sábado (4h) |
| 3 | Entregable: test, error boundary, población con asterisco | Domingo (3h) |

## Resultado final

- **Commits:** 3 (fixes + MVP 3 modos)
- **Branch:** `main` → pushhead a GitHub
- **NaN:** despliegue automático en 2-3 min
- **DOCX:** funciona con datos GTFS reales
- **Tiempo de respuesta:** <3s (sin 280KB de bloat)
- **Modos:** 3 (🚗 🚲 🚶)
- **GTFS:** EMT Madrid 250 paradas, 46 rutas
- **Datos demográficos:** 299 CPs, salarios, precios vivienda
