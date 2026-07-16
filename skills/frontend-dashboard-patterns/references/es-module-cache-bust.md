# ES Module Cache Bust — Modificaciones no se reflejan en el browser

## El problema

Cuando modificas un archivo `.js` que se importa vía `import { X } from './mod.js'`, el browser **NO recoge los cambios** aunque:
- Reinicies el servidor HTTP
- Uses `?v=N` en la URL del HTML
- Hagas `fetch()` directo y compruebes que el archivo en disco está actualizado

## Por qué ocurre

Los módulos ES (`import`) se cachean por **URL exacta** en el browser. Si el `<script type="module">` importa `./objetivos.js` sin parámetros, el browser usa la versión cached indefinidamente hasta que se cierra la pestaña.

## La prueba

```javascript
// fetch() SÍ muestra el archivo actualizado (cache distinto)
const resp = await fetch('./js/objetivos.js?t=' + Date.now());
const text = await resp.text(); // ✅ Contenido actualizado

// Pero import() sigue usando el módulo cached
const mod = await import('./js/main.js'); // ❌ Importa módulos con URL sin cache-buster
```

## La solución

Añadir `?v=N` a **TODOS** los imports, tanto en el HTML inline como en los módulos entre sí.

### Patrón 1 — Imports estáticos (inline script)

```javascript
// index.html inline script
import { calcularDiagnostico } from './js/main.js?v=2';
```

### Patrón 2 — Dynamic imports con cache-busting (main.js wrapper)

Cuando `main.js` es un wrapper que re-exporta dinámicamente, los `import()` TAMBIÉN necesitan `?v=N`. **Este es el patrón que falla más a menudo porque `import()` no fuerza re-evaluación sin el parámetro.**

```javascript
// ❌ El browser cachea './diagnostico.js' por URL exacta
export async function calcularDiagnostico(state) {
    const { calcularDiagnostico: _calc } = await import('./diagnostico.js');
    return _calc(state);
}

// ✅ Con cache-busting en cada dynamic import
const CACHE_V = Date.now();
export async function calcularDiagnostico(state) {
    const { calcularDiagnostico: _calc } = await import(`./diagnostico.js?v=${CACHE_V}`);
    return _calc(state);
}
```

**Pitfall:** El `CACHE_V` debe ser constante dentro de la sesión (no `Date.now()` en cada call), para que todos los módulos cargados en la misma sesión compartan el mismo bust. Pero cambia entre recargas de página (distinto `Date.now()` al cargar main.js).

### Patrón 3 — Wrapper re-export con cache-busting completo

Para `main.js` que sirve como punto de entrada re-exportando de múltiples módulos:

```javascript
// main.js — 51 líneas, wrapper limpio
const V = Date.now();

export async function calcularDiagnostico(state) {
    const mod = await import(`./diagnostico.js?v=${V}`);
    return mod.calcularDiagnostico(state);
}

export async function calcularDAFO(state) {
    const mod = await import(`./dafo.js?v=${V}`);
    return mod.calcularDAFO(state);
}

export async function generarMedidas(state) {
    const mod = await import(`./objetivos.js?v=${V}`);
    return mod.generarMedidas(state);
}

export async function generarObjetivos(state) {
    const mod = await import(`./objetivos.js?v=${V}`);
    return mod.generarObjetivos(state);
}
```

## Cómo detectarlo

1. El archivo en disco tiene el fix, pero `console.log` del browser muestra el error original
2. `fetch()` con `?t=` devuelve el contenido correcto, pero `import()` falla
3. El error stack muestra línea correcta pero el contenido de esa línea es la versión antigua

## Diagnóstico rápido

```javascript
// En browser_console, verificar qué ve el browser:
(async () => {
    const resp = await fetch('./js/objetivos.js?t=' + Date.now());
    const text = await resp.text();
    const hasOldCode = text.includes('state.encuesta'); // buscar el bug que corregiste
    return { hasOldCode, length: text.length };
})();
```

## Pitfall adicional — Duplicate exports

**NUNCA usar re-exports estáticos + funciones con el mismo nombre** en el mismo módulo:

```javascript
// ❌ SyntaxError: Duplicate export
export { calcularDiagnostico } from './diagnostico.js';
export function calcularDiagnostico(state) { ... }

// ✅ Usar alias
import { calcularDiagnostico as _calcDiag } from './diagnostico.js';
export function calcularDiagnostico(state) { return _calcDiag(state); }
```

## Sesión de referencia

- Proyecto: PLANDEMOVILIDAD (rewrite multi-fase)
- Archivos afectados: `main.js`, `objetivos.js`, `index.html`
- Tiempo de debugging: ~30 min (el bug parecía estar en el archivo correcto, pero era cache)
