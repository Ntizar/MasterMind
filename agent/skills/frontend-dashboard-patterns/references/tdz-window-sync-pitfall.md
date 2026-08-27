# Temporal Dead Zone + Window Sync — Pitfalls en Scripts Vanilla JS

**Fecha:** 2026-07-13
**Proyecto:** DataHub España

## Bug 1: TDZ — `window.X = X` antes de `const X`

### Problema
`window.LLUVIA_CITIES = LLUVIA_CITIES` antes de `const LLUVIA_CITIES = [...]` → ReferenceError silencioso que mata todo el script.

### Por qué es engañoso
- No hay error visible en la UI (solo overlay pegado)
- `function` declarations SÍ tienen hoisting (funcionan antes de declararse)
- `const`/`let` NO tienen hoisting → temporal dead zone
- El script simplemente deja de ejecutarse en esa línea

### Detección rápida
```javascript
// ¿state.js se ejecutó?
({
  CCAA: typeof CCAA_NAMES !== 'undefined',
  setTxt: typeof setTxt !== 'undefined',
  LLUVIA: typeof LLUVIA_CITIES !== 'undefined'
})
// Si todos false → state.js no corrió. Causa probable: TDZ.
```

### Verificación del archivo
```bash
curl -s 'https://site.com/js/state.js' | python3 -c "
import sys, re
lines = sys.stdin.readlines()
window_assigns = [(i+1, l.strip()) for i, l in enumerate(lines) if 'window.' in l and '=' in l]
const_decls = [(i+1, l.strip()) for i, l in enumerate(lines) if re.match(r'\s*(const|let)\s+\w+\s*=', l)]
for ln, line in window_assigns:
    var = re.search(r'window\.(\w+)', line)
    if var:
        name = var.group(1)
        decl = [d for d in const_decls if name in d[1]]
        if decl and decl[0][0] > ln:
            print(f'⚠️  TDZ: window.{name} (L{ln}) BEFORE const {name} (L{decl[0][0]})')
"
```

### Fix
Mover TODAS las asignaciones `window.X = X` DESPUÉS de las declaraciones `const X`.

---

## Bug 2: `let` + `window.map` — Propiedades no sincronizadas

### Problema
```javascript
let map = null;
window.map = map;  // copia null

// Más tarde en initMap():
map = L.map('map', {...});  // actualiza la variable let
// Pero window.map sigue null!
```

### Causa
`window.map = map` es asignación por valor. `let` en scope de script no se sincroniza con `window`.

### Solución: Object.defineProperty
```javascript
let map = null;
Object.defineProperty(window, 'map', {
  get() { return map; },
  set(v) { map = v; },
  configurable: true
});
// Ahora: map = L.map(...) → window.map TAMBIÉN se actualiza
```

### Alternativa más simple
Reasignar explícitamente después de cada cambio:
```javascript
function initMap() {
  map = L.map('map', {...});
  window.map = map;  // Reasignar EXPLÍCITAMENTE
}
```

---

## Bug 3: Script `?v=` Cache Busting incompleto

### Problema
Index.html se recarga con `?v=nuevo`, pero los `<script src="js/state.js?v=old">` siguen cacheados.

### Fix
Actualizar `?v=` en TODOS los script tags:
```bash
sed -i 's/v=20260712/v=20260713/g' index.html
```

### Verificación
```bash
curl -s 'https://site.com/' | grep 'state.js'
# Debe mostrar el nuevo ?v=
```
