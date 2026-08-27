# Web Worker Pitfalls en GitHub Pages

## 1. Path Resolution — El bug clásico

**Problema:** Un Web Worker en `js/worker.js` que usa `fetch('data/file.bin')` resuelve la ruta relativa desde su propia ubicación (`js/`), NO desde la raíz de la página.

```
Worker ubicado en:  js/worker.js
fetch('data/file.bin') resuelve a:  js/data/file.bin  ← 404!
En vez de:                          data/file.bin      ← correcto
```

**Fix:** Calcular la base URL desde `self.location.href`:

```javascript
// En el worker:
const baseUrl = self.location.href.replace(/js\/[^/]*$/, '');
const url = `${baseUrl}data/graphs/${city}.bin`;
```

**Alternativa más robusta** (recomendada para proyectos con estructura variable):

```javascript
// En el worker:
const workerDir = self.location.href.substring(0, self.location.href.lastIndexOf('/') + 1);
const pageRoot = workerDir.replace(/js\//, '');
const url = `${pageRoot}data/file.bin`;
```

**Regla general:** Si el worker está en un subdirectorio (`js/`, `workers/`, `lib/`), NUNCA uses rutas relativas simples para archivos fuera de ese directorio. Siempre resuelve desde la raíz.

## 2. Debugging — self.postMessage como logging

Los Web Workers no tienen acceso a `console.log()` del padre. Para diagnosticar:

**En el worker** — enviar mensajes de debug:
```javascript
self.postMessage({ cmd: 'debug', message: `Fetching: ${url}` });
```

**En el parent** — interceptar mensajes debug:
```javascript
const handler = (e) => {
  const { cmd } = e.data;
  if (cmd === 'debug') {
    console.log('[Worker]', e.data.message);
    return;  // No procesar como resultado/error
  }
  // ... manejar loaded, error, result
};
```

**Pattern completo:**
```javascript
// Worker:
self.onmessage = async function(e) {
  const { cmd } = e.data;
  if (cmd === 'load') {
    self.postMessage({ cmd: 'debug', location: self.location.href, city: e.data.city });
    const url = resolveUrl(e.data.city);
    self.postMessage({ cmd: 'debug', url });
    // ... fetch y procesar
  }
};

// Parent:
function createWorkerHandler(resolve, reject, timeout) {
  return function handler(e) {
    if (e.data.cmd === 'debug') {
      console.debug('[Dijkstra Worker]', e.data.message || e.data);
      return;
    }
    if (e.data.cmd === 'loaded') { /* ... */ }
    if (e.data.cmd === 'error') { /* ... */ }
  };
}
```

## 3. Cache en GitHub Pages

**Problema:** GitHub Pages sirve archivos estáticos con cache headers. Después de hacer push, el browser puede seguir usando la versión vieja del worker script.

**Soluciones:**

1. **Cache bust manual** — añadir query string al worker URL:
   ```javascript
   worker = new Worker(new URL('./worker.js?v=2', import.meta.url));
   ```
   Incrementar `?v=N` cada vez que cambies el worker.

2. **Service Worker** — unregister y register nuevo (más complejo).

3. **Hard refresh** — instruct the user: `Ctrl+Shift+R` / `Cmd+Shift+R`.

**Recomendación para dashboards:** Si el worker cambia frecuentemente, usa `?v=<commit-sha-short>` o un timestamp.

## 4. Binary Files (.bin) en GitHub Pages

GitHub Pages sirve archivos `.bin` con `Content-Type: application/octet-stream` y CORS `Access-Control-Allow-Origin: *`. No hay problema para `fetch()` desde workers, pero:

- **Tamaño máximo recomendado:** <1MB para grafos viales
- **Verificar con curl:** `curl -sI https://site.github.io/project/data/file.bin`
- **Si falla:** puede ser que el archivo no esté en la rama `gh-pages` o que el build no lo copió

## 5. Worker Lifecycle en SPAs

```javascript
// Crear worker una sola vez (lazy)
let worker = null;
function getWorker() {
  if (!worker) {
    worker = new Worker(new URL('./worker.js', import.meta.url));
  }
  return worker;
}

// Cleanup en page unload (opcional pero recomendado)
window.addEventListener('beforeunload', () => {
  if (worker) {
    worker.terminate();
    worker = null;
  }
});
```

## 6. Standalone Testing — 10x faster than Pages deploy

**Problema:** Diagnosticar un Web Worker haciendo push a GitHub Pages + hard refresh + cache bust es LENTO (2-5 min por ciclo). Para debugging iterativo, hay una forma 10x más rápida.

**Testing directo en consola del navegador:**

```javascript
// 1. Navegar a la página (cualquier página del proyecto)
// 2. Abrir DevTools Console
// 3. Testear el worker directamente:

const w = new Worker('./js/dijkstra-worker.js?v=999');  // ?v=999 bypass ES module cache
w.onmessage = (e) => console.log('worker:', JSON.stringify(e.data));
w.onerror = (e) => console.error('worker error:', e.message);

// Test load
w.postMessage({cmd:'load', city:'madrid'});

// Test findNearest
w.postMessage({cmd:'findNearest', lat:40.4168, lng:-3.7038});

// Test dijkstra completo
w.postMessage({cmd:'dijkstra', lat:40.4168, lng:-3.7038, mode:'walking', cutoffSec:1800});
```

**Ventajas:**
- Sin push a Git, sin wait a Pages build, sin cache bust
- Iteración en segundos, no minutos
- Mismo contexto de-Origin que la app real (CORS, paths, etc.)

**Cuándo usar:** Cuando el worker falla en Pages pero no sabes por qué. Testea standalone para aislar si el problema es el worker o la integración con la app.

**Pitfall:** El `?v=999` es necesario porque los browsers cachean workers por URL. Sin el query string, puedes estar testeando la versión vieja.

## 7. Fallback Pattern

Cuando un Worker puede fallar (API no disponible, archivo no encontrado), siempre tener un fallback:

```javascript
async function calcularConWorker(data) {
  try {
    return await workerCalculate(data);  // Intenta worker
  } catch (workerError) {
    console.warn('Worker failed:', workerError.message);
    return calculateMainThread(data);  // Fallback sin worker
  }
}
```
