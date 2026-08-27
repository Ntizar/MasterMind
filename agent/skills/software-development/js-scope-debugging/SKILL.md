---
name: js-scope-debugging
description: >
  Diagnosticar y arreglar bugs de scope en JavaScript vanilla: temporal dead zone,
  let vs var vs window, Object.defineProperty para sincronizar variables entre scripts.
  Patrones de safety net para overlays/loading states.
tags: [javascript, debugging, scope, vanilla-js, frontend]
---

# JS Scope Debugging — Guía de diagnóstico y fixes

## Problema clásico: script mata silenciosamente todo lo que viene después

### Causa #1: Temporal Dead Zone (TDZ)

```js
// ❌ FATAL — ReferenceError silencioso que mata el script entero
window.LLUVIA_CITIES = LLUVIA_CITIES;  // ← LLUVIA_CITIES aún no declarado
// ... más código ...
const LLUVIA_CITIES = [...];  // ← declaración llega demasiado tarde
```

**Diagnóstico:**
```js
// En consola del navegador:
typeof window.LLUVIA_CITIES  // → "undefined" = script no ejecutó
typeof setTxt                 // → "undefined" = state.js roto
```

**Fix:** Mover `window.X = X` DESPUÉS de la declaración `const/let`.

### Causa #2: `let` + `window.map = map` no sincroniza

```js
// state.js
let map = null;
window.map = map;  // ← copia el valor null a window.map

// map.js
function initMap() {
    map = L.map('map', ...);  // ← setea la variable let de state.js
    // PERO window.map sigue null porque fue copiado antes
}
```

**Diagnóstico:**
```js
window.map          // → null (desactualizado)
typeof window.map   // → "object" (typeof null === "object" en JS!)
window.map === null // → true
```

**Fix — Object.defineProperty:**
```js
Object.defineProperty(window, 'map', {
  get() { return map; },
  set(v) { map = v; },
  configurable: true
});
// Ahora window.map SIEMPRE refleja el valor actual de la variable let
```

### Causa #3: Scripts cacheados por CDN/navegador

**Síntoma:** El código desplegado en GitHub es correcto, pero el navegador sirve versión vieja.

**Fix:** Bumpear version strings en index.html:
```html
<!-- Antes (cacheado) -->
<script src="js/state.js?v=20260712143834"></script>
<!-- Después (fuerza recarga) -->
<script src="js/state.js?v=202607131345"></script>
```

## Safety net patterns

### Overlay que nunca se oculta
```js
// Siempre añadir timeout de seguridad + catch
setTimeout(() => {
    const ol = document.getElementById('loading-overlay');
    if (ol && !ol.classList.contains('hidden')) {
        ol.classList.add('hidden');
    }
}, 10000);

init().catch(err => {
    console.error('init() falló:', err);
    document.getElementById('loading-overlay')?.classList.add('hidden');
});
```

### Variables que necesitan sincronización cross-script
Para cada `let` en un script que se accede desde otro script via `window.X`:

```js
// ✅ SIEMPRE usar Object.defineProperty para variables que cambian
Object.defineProperty(window, 'nombreVar', {
  get() { return nombreVar; },
  set(v) { nombreVar = v; },
  configurable: true
});

// ❌ NUNCA hacer window.X = X una vez (copia estática)
window.X = X;  // X cambia después, window.X no se actualiza
```

## Checklist de diagnóstico rápido

1. `typeof window.X` → `undefined` = el script no ejecutó (TDZ o syntax error)
2. `typeof window.X` → `"object"` pero `window.X === null` = let-scoped null no sincronizado
3. Código en GitHub OK pero navegador falla = cache busting necesario
4. Overlay stuck = init() nunca resuelve → buscar promise sin catch
5. Funciones `undefined` en consola = script anterior falló silenciosamente

## Errores comunes de JavaScript que parecen bugs de scope

| Error | Causa real |
|-------|-----------|
| `X is not defined` en eval() | `const` en eval tiene scope propio |
| `Cannot read property of null` | Elemento DOM no existe aún |
| Script no ejecuta nada | Syntax error o TDZ mata todo |
| `map` es null después de initMap() | let-scoped, no en window |
| Overlay forever loading | Promise sin .catch() |
