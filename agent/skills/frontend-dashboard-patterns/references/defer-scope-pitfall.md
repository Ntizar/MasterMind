# Pitfall: `defer` crea scope léxico separado por script

**Fecha:** 2026-07-12
**Proyecto:** DataHub España refactor modular

## El problema

Al refactorizar un dashboard monolítico a módulos (32 archivos JS), se añadieron `defer` a todos los `<script>` tags para que carguen después del parseo del DOM. Esto causó:

1. **Cada `<script defer>` tiene su propio scope léxico** — las variables `const`/`let` declaradas en un script NO son visibles en otro script, incluso con `defer`.
2. `init()` en `main.js` intentaba acceder a variables de `state.js` (map, charts, LLUVIA_CITIES, etc.) y fallaba con `ReferenceError`.
3. El error era silencioso: `init()` es async sin `.catch()`, así que el overlay de "Cargando..." quedaba pegado.
4. Los errores del navegador aparecían como 20-30 excepciones sin mensaje (fetch a APIs fallidas que no capturaban errores).

## Señales de detección

- Página carga pero se queda en "Cargando..."
- Overlay de loading nunca se oculta
- `window.charts` es undefined
- `typeof init === 'function'` pero `init()` falla con `ReferenceError: X is not defined`
- 20+ errores en consola sin mensaje (fetch HTTP fallidos, no JS)
- Funciones `function` sí funcionan (hoisting), pero `const`/`let` no
- **Archivos JS indentados con 4 espacios** → puede confundir a pensar que hay un IIFE oculto, pero NO lo hay. La indentación no afecta scope en JS. Ver `pitfalls-html-dashboards.md` → "Scripts Indentados con 4 Espacios"

## Falso IIFE por indentación

**Señal:** Todos los archivos JS del refactor tienen indentación de 4 espacios.

**Verificación:**
```bash
curl -s 'https://site.com/js/state.js' | python3 -c "
import sys
txt = sys.stdin.read()
lines = txt.split('\n')
code_lines = [l for l in lines if l.strip() and not l.strip().startswith('//')]
all_indented = all(l.startswith('    ') for l in code_lines)
print('TODAS indented:', all_indented)
print('Tiene IIFE real:', '(function' in txt)
"
```

Si `TODAS indented: True` pero `Tiene IIFE real: False` → los archivos están indentados pero NO hay IIFE. La indentación es solo estética del extractor. El problema real suele ser **caché del navegador** (ver `pitfalls-html-dashboards.md` → "Caché del Navegador vs CDN").

## Soluciones

### Opción A (recomendada): Scripts al final del `<body>` SIN `defer`
```html
<script src="js/state.js"></script>
<script src="js/api.js"></script>
<script src="js/main.js"></script>
```
Ventaja: todos comparten scope global, DOM está listo (los scripts se ejecutan en orden de aparición).

### Opción B: `defer` + exponer a `window`
```javascript
const map = null;
window.map = map;
window.charts = charts;
```
Ventaja: orden explícito de carga. Desventaja: más boilerplate, fácil olvidar exponer algo.

### Opción C: IIFE wrapper con exports
```javascript
(function() {
    const map = null;
    window.map = map;
    window.State = { map, charts, LLUVIA_CITIES };
})();
```

## Regla de oro para refactor modular

> Cuando un dashboard monolítico se divide en módulos JS:
> - **Si usas `defer`:** todas las variables deben exponerse a `window` o a un objeto global
> - **Si NO usas `defer`:** scripts deben estar al final del `<body>` en orden de dependencia
> - **NUNCA mezclar:** `const`/`let` a nivel de script sin `defer` → scope del script, NO global
> - **Siempre verificar:** tras refactor, `typeof variable === 'undefined'` en consola = bug

## Checklist post-refactor

1. [ ] `typeof init === 'function'`
2. [ ] `typeof map !== 'undefined'`
3. [ ] `typeof charts !== 'undefined'`
4. [ ] `typeof LLUVIA_CITIES !== 'undefined'`
5. [ ] `document.querySelectorAll('.tab-btn').length > 0`
6. [ ] `init()` se ejecuta sin ReferenceError
7. [ ] Overlay se oculta
8. [ ] Tabs responden al click