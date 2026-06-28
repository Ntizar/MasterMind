# Debug: ReferenceError en frontend modular (2026-05-26)

## Síntoma
Dashboard en blanco. Consola muestra:
```
ReferenceError: formatNum is not defined
    at renderMetrics (render.js:13:21)
    at renderAll (data.js:166:5)
```

## Causa
Al reescribir `utils.js`, se eliminaron funciones que `render.js` necesita:
- `formatNum` — formateo de números
- `numericValues` — filtrar valores numéricos de array
- `average` — calcular media
- `fmtHora` — formatear hora (HH:00)
- `hourlySeries` — convertir points array a array de 24 valores
- `priceColor` — color por rango de precio
- `activeTechKeys` — filtrar tech keys con datos reales
- `getMadridHour` — hora actual en timezone Madrid

## Diagnóstico
```bash
# Verificar que TODAS las funciones llamadas por renderers existen
grep -rn 'function formatNum\|function numericValues\|function average\|function fmtHora\|function hourlySeries\|function priceColor\|function activeTechKeys\|function getMadridHour' public/js/

# Verificar que techMap y techKeys existen en config.js
grep -n 'const techMap\|const techKeys' public/js/config.js
```

## Solución
1. **Restaurar versión funcional de utils.js**: `git checkout <commit-bueno> -- public/js/utils.js`
2. **Añadir funciones nuevas** que faltaban (ej: `activeTechKeys`)
3. **Verificar con grep** que todas las funciones llamadas existen
4. **No hacer commit** hasta verificar que no hay ReferenceErrors

## Funciones críticas que NUNCA deben faltar en utils.js
| Función | Usada por |
|---|---|
| `formatNum` | render.js (renderMetrics, renderTechCards, renderHourlyTable) |
| `numericValues` | render-charts.js (renderMonteCarlo, renderPrecioCurve) |
| `average` | render-charts.js (renderMonteCarlo) |
| `fmtHora` | render-charts.js (renderMonteCarlo) |
| `hourlySeries` | render-charts.js (renderPrecioCurve) |
| `priceColor` | render-charts.js (renderPrecioCurve) |
| `activeTechKeys` | render.js (renderTechCards) |
| `getMadridHour` | render.js (renderMetrics, renderTechCards) |
| `getMadridDateStr` | data.js, utils.js (date helpers) |
| `showToast` | data.js, ui.js (feedback usuario) |
| `showLoading` | data.js (loading overlay) |

## Lección aprendida
Al reescribir `utils.js`, SIEMPRE hacer diff contra la versión funcional anterior. Las funciones helper son el pegamento entre módulos — eliminar una causa ReferenceError en cascada que deja el dashboard completamente en blanco.