---
name: refactor-nodejs-monolith
version: "1.0.0"
description: Refactorizar proyecto Node.js monolítico a arquitectura modular por dominios
tags: [software-development, refactor, nodejs, architecture]

---

# Refactorización de proyecto Node.js monolítico a arquitectura modular

## Cuándo aplicar
Cuando un proyecto Node.js/Express tiene un `server.js` >1000 líneas con lógica mezclada (config, clientes HTTP, dominio, rutas, persistencia).

## Pasos

### 1. Crear estructura de directorios
```
src/
  config/          → validación de entorno
  shared/          → utilidades compartidas
    time/          → utilidades de fecha/hora
    io/            → repositorios de datos
  infra/           → clientes externos + cache
    clients/       → HTTP clients
    cache/         → cache strategies
  domains/         → dominios de negocio
    <domain>/      → service.js, schemas.js, mapper.js
  jobs/            → trabajos programados
```

### 2. Extraer configuración
- Crear `src/config/env.js` con validación estricta de variables obligatorias
- Crear `.env.example` documentado
- Fail-fast al arranque si faltan vars obligatorias

### 3. Extraer utilidades compartidas
- Centralizar lógica de tiempo/fecha en `src/shared/time/`
- Centralizar parseo de datos en `src/shared/`
- Reemplazar `fs.sync` por `fs/promises`

### 4. Extraer clientes HTTP
- `src/infra/clients/<name>.client.js` con reintentos, backoff exponencial, jitter
- Sin lógica de negocio en clientes

### 5. Extraer dominios
- `src/domains/<domain>/` con service + schemas + mapper
- Cada dominio con interfaz clara y testeable

### 6. Reescribir server.js
- Solo bootstrap Express + routing
- Importar servicios de dominios
- Eliminar autoconsumo HTTP interno (llamar servicios directamente)
- Añadir helmet + CORS whitelist + metrics endpoint

### 7. Actualizar Dockerfile
- Multi-stage build
- Usuario no-root
- HEALTHCHECK
- Copiar solo artefactos necesarios

### 8. Tests
- Jest con `testEnvironment: node` (NO vitest para proyectos CommonJS)
- `@jest/globals` para `describe/it/expect` con require()
- `--forceExit --detectOpenHandles` para tests de integración con supertest
- `delete require.cache[require.resolve(...)]` para recargar módulos con env variables diferentes
- Tests de integración: `supertest` + `require('../server')` — el server se queda abierto, `--forceExit` lo maneja
- Tests de env: guardar/restaurar `process.env` original, limpiar cache, recargar módulo

### 9. Verificar
- Misma respuesta funcional en todos los endpoints
- Tests de integración con mocks
- `git diff server.js` muestra reducción significativa

## Pitfalls

### Backend
- **Módulos ESM vs CommonJS**: Si el proyecto usa `require()`, NO usar `export` en archivos nuevos. Todo debe ser `module.exports`.
- **Rutas relativas**: `require('../../shared/time/madrid')` depende de la ubicación del archivo que importa, no del CWD. Verificar cada import.
- **Variables de entorno**: El archivo `.env` NO se hace commit. `.env.example` SÍ.
- **Autoconsumo HTTP**: Si un endpoint llama a otro endpoint del mismo servidor, reemplazar por llamada directa al servicio.
- **Vitest vs Jest**: Vitest no funciona con `require()` — usa `import`. Para proyectos CommonJS existentes, usar Jest con `@jest/globals`.
- **Locale en tests**: `toLocaleString('es-ES')` puede no incluir separador de miles en entornos con locale por defecto. Tests deben aceptar ambas formas.
- **Server abierto en tests**: Importar `server.js` en supertest deja TCP abierto. Usar `--forceExit --detectOpenHandles` en Jest.

### CSP con helmet
- **Google Fonts**: Necesita `styleSrc` + `styleSrcElem` con `https://fonts.googleapis.com` Y `fontSrc` con `https://fonts.gstatic.com`. Solo `styleSrc` no basta.
- **Sourcemaps CDN**: Necesita `connectSrc` explícito para `https://cdn.jsdelivr.net` o los sourcemaps se bloquean.
- **scriptSrcAttr**: Cuidado con comillas — `'unsafe-inline'` debe tener comilla simple de cierre. `'unsafe-inline"` (falta ') causa error silencioso de CSP.
- **scriptSrcElem explícito**: No confiar en el fallback a `scriptSrc`. Definir `scriptSrcElem` explícitamente.
- **Verificar CSP generado**: Tras cambiar helmet, hacer `curl -s -D- http://localhost:4000/ | grep Content-Security-Policy` para ver la directiva resultante. Cada recurso externo necesita su directiva específica (styleSrc para CSS, fontSrc para fuentes, connectSrc para fetch/XHR, scriptSrcAttr para atributos inline).

### Frontend modular (extraer de index.html monolítico)
- **Variable scoping en módulos**: Al extraer JS de un `<script>` único a módulos separados, verificar NUNCA que variables globales como `tableSort` sean en realidad propiedades de un objeto (`AppState.tableSort`). Buscar TODAS las referencias con `grep -rn 'variableName' public/js/`.
- **Duplicación accidental**: Al extraer secciones, verificar que no se haya duplicado la misma constante en dos archivos (`const tableColumns` en render.js Y render-final.js causa SyntaxError).
- **Orden de carga en HTML**: Los `<script>` tags deben cargarse en orden de dependencia: config → state → utils → api → ui → data → render → render-charts → render-final. Si un módulo usa algo de otro, debe venir DESPUÉS.
- **`DOMContentLoaded` en módulo final**: Solo el último módulo (init) debe tener `document.addEventListener('DOMContentLoaded', ...)`. Los otros módulos solo definen funciones/constantes.
- **Verificación post-extracción**: Tras reescribir el HTML limpio, verificar en consola del browser: (1) no hay `ReferenceError`, (2) cada `<script src="...">` devuelve 200, (3) `window.AppState` existe antes de cargar datos.
- **⚠️ CRÍTICO: al reescribir utils.js, verificar TODAS las funciones que usan los renderers**. Las funciones `formatNum`, `numericValues`, `average`, `fmtHora`, `hourlySeries`, `priceColor` son llamadas por `render.js`. Si se eliminan al reescribir utils.js, TODOS los renderers fallan con `ReferenceError` → dashboard en blanco. Antes de hacer commit de un rewrite de utils.js: `grep -rn 'function formatNum\|function numericValues\|function average\|function fmtHora\|function hourlySeries\|function priceColor' public/js/utils.js` — si alguno no aparece, está roto.
- **⚠️ Funciones de timezone deben existir en frontend Y backend**. `getMadridHour()` se definía en backend (`src/shared/time/madrid.js`) pero los renderers frontend la llamaban directamente. Al modularizar frontend, verificar que TODAS las funciones de timezone estén definidas en `utils.js` frontend, no solo en backend.
- **⚠️ Funciones helper NO deben ser llamadas antes de definirse**. `activeTechKeys()` era llamada por `renderGeneracionMix()` pero no existía en `utils.js`. Siempre verificar que cada función llamada por renderers esté definida en algún módulo cargado antes del renderer.

## Resultado esperado
- server.js reducido 40-60%
- Código separable por dominios
- Sin secretos en código
- Headers de seguridad (helmet)
- CORS por lista blanca
- I/O asíncrona
- Cache con métricas
- Docker hardening
- Tests: Jest con `testEnvironment: node` (NO vitest para proyectos CommonJS)

## Frontend modular
- Extraer CSS/JS/HTML de monolitos >1500 líneas en módulos separados
- Orden de carga crítico: config → state → utils → api → ui → data → render → init
- Verificar scoping: `AppState.tableSort` NO `tableSort`
- Verificar duplicados de `const` entre módulos
- **Cache-busting OBLIGATORIO**: añadir `?v=TIMESTAMP` a todos los `<script src>` en HTML. Sin esto, el navegador sirve JS antiguo y da ReferenceError.
- **Cache-busting dinámico preferible**: en lugar de `?v=202605260830` estático, usar un script inline que inyecte `Date.now()` al cargar la página:
  ```html
  <script>
  (function(){var ts=Date.now();document.querySelectorAll('script[src^="js/"]').forEach(function(s){var src=s.src;if(src.indexOf('?')===-1)src+='?v='+ts;else src=src.replace(/v=\d+/,'v='+ts);s.src=src;});})();
  </script>
  <script src="js/config.js"></script>
  ```
  Esto garantiza que cada recarga de página descargue los JS más recientes, incluso con cache del navegador.
- **No-cache en servidor**: aplicar `Cache-Control: no-cache, no-store, must-revalidate` a `.js` en middleware Express. El navegador NUNCA debe cacheart JS de dashboard.
- **No bloquear render por datos null**: el check `hasRealData = v.some(d => d.precio !== null)` es demasido agresivo. Si los datos vienen null, renderizar igual — los componentes muestran "—" para valores null. Bloquear el render completo por datos null es un error: el usuario ve pantalla en blanco en lugar de un dashboard con campos vacíos.
- **⚠️ CRÍTICO: CDN dependencies se pierden al extraer JS inline a archivo separado** — Cuando el HTML tiene `<script>` inline que usa librerías externas (Chart.js, Three.js, Plotly, etc.), el patrón es: `<head>` carga CDN → `<script>` inline usa la librería. Al extraer el inline a `<script src="dashboard.js">`, se olvidan los CDN del `<head>`. El JS externo carga pero falla silenciosamente (`new Chart()` → `ReferenceError` → `.catch()` muestra "Error cargando datos"). **VERIFICACIÓN OBLIGATORIA post-extracción:**
  1. `grep -oP 'new\s+(Chart|THREE|Plotly)\b' dashboard.js` — detectar constructores usados
  2. `grep 'cdn.jsdelivr\|unpkg\|cdnjs' dashboard.html` — verificar que los CDN correspondientes siguen en `<head>`
  3. Si falta algún CDN, añadirlo ANTES de hacer push
  - **Patrón de verificación universal:** `grep -oP '\bnew\s+([A-Z]\w+)\b' archivo.js` → lista de constructores → verificar que cada uno tiene su CDN/script tag en el HTML
- **Ver referencia**: `references/frontend-module-extraction.md`

## Fecha y prediccion (bug 502)
- **NUNCA hacer fetch de prediccion para dia futuro** — ESIOS no tiene datos → 502
- Solo pedir `/api/esios/prediccion` si fecha=hoy o ayer (el dia siguiente tiene datos)
- Funciones clave: `shouldFetchPrediccion(fecha)`, `isFutureDate(fechaStr)`, `clampDate(fechaStr)`
- Input date HTML: `max` dinamico = hoy (set en `loadState()`), `min` = hoy-365 dias
- Flechas teclado: clampar a [min,max] con toast informativo
- **Validación frontend + backend**: el frontend bloquea selección de fechas futuras, el backend no necesita validación extra si el frontend ya filtra
- Ver referencia: `references/fecha-prediccion-502-fix.md`

## Referencias
- `references/frontend-module-extraction.md` — patrón detallado para extraer frontend modular, orden de dependencias, reglas de escoping, bug conocido 2026-05-26
- `references/frontend-debug-reference-errors.md` — diagnóstico de ReferenceError en cascada al reescribir utils.js (formatNum, numericValues, average, fmtHora, hourlySeries, priceColor, activeTechKeys, getMadridHour)
- `references/csp-helmet-fix.md` — configuración completa de CSP con helmet: Google Fonts, CDN, sourcemaps, pitfalls de comillas
- `references/nan-spaces-deploy.md` — patrón de deploy a NaN Spaces, limitaciones (sin CLI), proceso manual, pitfall de verificación
- `references/fecha-prediccion-502-fix.md` — fix para 502 en /api/esios/prediccion: validación de fechas, conditional fetch, clampDate, input date max/min
