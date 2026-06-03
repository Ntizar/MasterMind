---
fecha: 2026-03-20
tarea: montecarlo-v35-context-pdf-screener
tipo: software
complejidad: alta
clusters: [arquitectura-software, finanzas-tech]
proyecto: montecarlo
patron: async-loading-flags-pattern
---

# MonteCarloInversion v3.5 — Context tab, PDF Reddit, S&P 500 ampliado, paginación ranking

## Decisión clave
Reemplazar las condiciones `!== undefined` para control de estado de carga asíncrona por flags booleanos explícitos (`_optionsLoaded`, `_redditLoaded`, `_insidersLoaded`) que se ponen a `true` tanto en el camino de éxito como en el de error del `Promise.allSettled`.

## Patrón reutilizable
**Nombre:** async-loading-flags-pattern
**Descripción:** Cuando varias fetches asíncronas alimentan una función de render que puede ejecutarse antes o después de que terminen, usar flags booleanos de "carga terminada" es más robusto que comprobar si la variable de datos es `null` vs `undefined`. El flag se pone a `true` en el bloque `finally` equivalente (o al final de ambas ramas del `catch`). El render lee el flag, no el valor nulo, para decidir entre "cargando" y "no disponible".

## Qué funcionó
- Resetear **todas** las variables de estado (`currentFundamentals`, `currentNews`, `currentOptions`, `currentReddit`, `currentInsiders`) y todos los flags en la misma función `loadContextData`, al inicio, antes de cualquier fetch.
- Añadir párrafos de interpretación en lenguaje natural **dentro del propio render** (no en los módulos de datos), con lógica condicional sobre los valores numéricos (p.ej. score >= 70 → "alcista", <= 35 → "débil", resto → "neutral").
- Usar `replaceAll: true` en el Edit tool para actualizar las 3 llamadas idénticas a `exportSimulationPDF` en `app.js` en una sola operación.
- Añadir la paginación directamente en la función `applyAndRender` del screener existente (en lugar de añadir una segunda tabla); así los filtros y la paginación comparten el mismo array `_lastSorted`.

## Qué evitar
- `currentOptions !== undefined` como guardia de "está cargando": `null !== undefined` es `true`, por lo que la rama "cargando" nunca se muestra si la variable se inicializa a `null`.
- Re-lanzar fetches dentro de `renderContextTab()` (el patrón antiguo para fundamentales y noticias): crea doble fetch si el usuario cambia de tab y vuelve, y es inconsistente con el resto de módulos.
- No resetear `currentFundamentals` / `currentNews` al cambiar de símbolo: pueden quedar datos del activo anterior visibles mientras carga el nuevo.
- Abrir el bloque HTML de un elemento `<div>` sin cerrarlo antes de un `return` condicional (genera HTML malformado). En `renderContextTab` cada sección abre y cierra su propio `<div>` sin concatenar la etiqueta de cierre en un paso separado.

## Skills usados
- software-dev

## Criterios que validaron el éxito
- Commit `abe6132` pusheado a `main` sin errores.
- CI/CD desplegó en `gh-pages` correctamente.
- Las 3 llamadas a `exportSimulationPDF` actualizadas con `currentReddit` verificadas con `grep`.
- La tabla de ranking tiene `<div class="ranking-pagination">` y los estilos `.page-btn` en `styles.css`.

## Contexto de la tarea
- Flujo ejecutado: implementer directo (contexto de sesión previa ya disponible)
- Reintentos necesarios: 1 (corrección de HTML suelto en sección técnicos del PDF tras eliminar el `<div class="tech-pdf-header">` sin reponerlo)
- Tiempo estimado: largo

## Conexiones
**Clusters:** #arquitectura-software · #finanzas-tech
**Proyecto:** [[montecarlo]]
**Aprendizajes relacionados:** [[2026-03-20-montecarlo-github-pages-subdirectory]] · [[2026-03-20-montecarlo-deploy-sin-verificar]]

## Estado del proyecto al cierre (v3.5)

### Arquitectura general
- **`app.js`** (≈1780 líneas) — controlador principal. Variables de estado globales: `currentSymbol`, `currentData`, `currentResults`, `currentMetrics`, `currentBacktest`, `currentFundamentals`, `currentNews`, `macroData`, `currentTechnicals`, `currentOptions`, `currentReddit`, `currentInsiders`, `analyzedStocks` (objeto `{}`), `_optionsLoaded`, `_redditLoaded`, `_insidersLoaded`.
- **`exporter.js`** (≈870 líneas, v3.5) — PDF con 12 secciones: señal, riesgo, backtest, modelos, macro, fundamentales, noticias, técnicos, opciones, insiders, reddit, disclaimer. Firma: `exportSimulationPDF(symbol, results, metrics, backtest, fundamentals, news, macroData, technicals, optionsData, insiders, redditData)`.
- **`config.js`** — S&P 500 fallback: ~100 tickers organizados por sector (Tech, Financieras, Salud, Consumo, Energía/Industrial, Comunicaciones, Utilities/REITs, Materiales).
- **`portfolio.js`** — Paginación de 25 activos/página en la tabla del ranking. Variable `_lastSorted` compartida entre screener y paginación.
- **`styles.css`** — Añadidos `.ranking-pagination`, `.page-btn`, `.page-btn.active`, `.page-btn[disabled]`, `.page-info`, `.page-ellipsis`, `.context-interp`.

### Funciones clave y líneas aproximadas
- `loadContextData(symbol)` — app.js ~431 — fetches asíncronos + flags
- `renderContextTab()` — app.js ~1104 — 9 secciones con interpretación
- `renderEarningsCalendar(cal, fundamentals)` — app.js ~1225
- `exportSimulationPDF(...)` — exporter.js ~212
- `renderMarketReport(report)` — portfolio.js ~576
- `applyAndRender()` (con paginación) — portfolio.js ~746

### Patrones CORS proxy
```js
const CORS_PROXIES = [
  url => `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`,
  url => `https://corsproxy.io/?url=${encodeURIComponent(url)}`,
  url => `https://api.codetabs.com/v1/proxy?quest=${encodeURIComponent(url)}`,
  url => `https://thingproxy.freeboard.io/fetch/${url}`,
];
```

### Pendientes / ideas para próximas sesiones
- La pestaña Contexto aún re-renderiza el HTML completo al terminar los fetches (no actualiza secciones individuales). Con muchas secciones esto puede causar un flash. Mejoría futura: actualizar solo los `div` pendientes via `getElementById`.
- El radar S&P 500 carga de Wikipedia vía proxy CORS — si falla, usa el fallback de `config.js`. Con el fallback ahora en ~100 tickers el escaneo es más representativo, pero la tabla de ranking sin filtros mostraría 100 filas (la paginación lo mitiga).
- `renderContextTab()` no tiene un spinner global mientras carga — solo spinners por sección. Podría mejorar la UX añadir un "resumen de estado" en la cabecera de la tab.
- El índice de correlación usa `analyzedStocks` (objeto `{}`); `computeCorrelationMatrix` en `correlation.js` debe aceptar objeto, no `Map` — verificado funcionalmente pero no hay test unitario.
- PDF: las secciones de Noticias y Backtest no tienen párrafos interpretativos todavía.
