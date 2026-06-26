# Frontend Module Extraction — Pattern Reference

## Cuándo aplicar
Cuando `public/index.html` (o equivalente) supera ~1500 líneas y contiene CSS + HTML + JS embebido en un solo archivo.

## Patrón de extracción

### 1. Identificar secciones
- `<style>...</style>` → `public/css/styles.css`
- `<script>...</script>` → `public/js/` módulos separados
- HTML entre style y script → HTML limpio

### 2. Orden de dependencias
```
config.js    → constantes, datos estáticos (sin dependencias)
state.js     → AppState, persistencia (usa config)
utils.js     → helpers puros (usa config)
api.js       → cliente fetch (usa utils)
ui.js        → interacción UI (usa api, state)
data.js      → cargarDatos + renderAll (usa api, state, utils, render)
render.js    → funciones de renderizado (usa utils, charts)
render-charts.js → gráficos específicos (usa utils, charts)
render-final.js → CO2, tabla, INIT/DOMContentLoaded (usa todo)
```

### 3. Reglas de escopo
- **NUNCA** usar variables globales que en realidad son propiedades de objetos (`AppState.tableSort`, no `tableSort`)
- **NUNCA** duplicar constantes entre módulos
- Solo el último módulo tiene `DOMContentLoaded`
- Cada módulo usa `const`/`function` a nivel de módulo, no `let` global

### 4. Verificación post-extracción
```bash
# Verificar que no hay variables sin definir
grep -rn 'tableSort' public/js/ | grep -v 'AppState.tableSort'

# Verificar que no hay duplicados
grep -rn 'const tableColumns' public/js/

# Verificar orden de carga en HTML
grep '<script' public/index.html
```

### 5. Reducción esperada
- HTML: ~2200 → ~220 líneas
- CSS: ~380 líneas en archivo separado
- JS: ~1660 → 6-9 módulos de 100-300 líneas cada uno

### 6. Cache-busting (CRÍTICO)
**Siempre** añadir `?v=TIMESTAMP` a los `<script src>` del HTML:
```html
<script src="js/config.js?v=202605260830"></script>
```
Sin esto, el navegador sirve JS cacheado de versiones anteriores → ReferenceError.

**También** aplicar `Cache-Control: no-cache, no-store, must-revalidate` a `.js` en middleware Express:
```js
if (req.path.endsWith('.js')) {
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
}
```

### 7. Bugs conocidos
- **tableSort no definido** (2026-05-26): variable era `AppState.tableSort` pero se usaba como `tableSort` global. Grepear TODAS las referencias antes de extraer.
- **Duplicado tableColumns**: la misma constante en dos archivos causa `SyntaxError: Identifier 'tableColumns' has already been declared`. Verificar con `grep -rn 'const tableColumns' public/js/`.
- **Cache de navegador**: el navegador puede servir JS antiguo incluso tras commit+push. El cache-busting + no-cache headers son OBLIGATORIOS.
