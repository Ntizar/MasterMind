# Cache de ES Modules en navegador — Desarrollo

## El problema

Los módulos ES (`<script type="module">`) se cachean por URL en el navegador. Cambiar el contenido del archivo en el servidor NO fuerza recarga si la URL no cambia. Esto incluye:

- Imports estáticos: `import { foo } from './bar.js'`
- Imports dinámicos: `import('./bar.js')`

El cache es **independiente del HTTP cache**. Incluso con `Cache-Control: no-cache, no-store`, el navegador mantiene el módulo en memoria.

## Síntomas recurrentes

1. Una URL con `?v=2` (cache-buster) en el HTML carga main.js nuevo
2. Pero los submódulos importados (`./ors.js`, `./config.js`, `./utils.js`) siguen siendo los viejos
3. Porque los imports resueltos por el módulo padre NO heredan el query string
4. Solo import('./config.js') desde el HTML base usaría la URL base; `import { x } from './config.js'` desde `main.js?v=2` resuelve como `./config.js` sin `?v=2`

## Solución: cache-buster en cascade

Regla: **TODOS los imports entre módulos deben llevar el mismo `?v=N`**.

```javascript
// En main.js:
import { initMap } from './map.js?v=2';
import { computeAllIsochrones } from './ors.js?v=2';
import CONFIG from './config.js?v=2';

// En ors.js:
import { addIsochroneLayer } from './map.js?v=2';
import CONFIG from './config.js?v=2';
```

El HTML carga el entry point con cache-buster:
```html
<script type="module" src="js/main.js?v=2"></script>
```

Esto fuerza al navegador a descargar `main.js` fresco, y los imports internos con `?v=2` son URLs diferentes → también se descargan frescos.

## Alternativa: servidor sin cache + navegación cross-domain

Configurar el servidor para JS con:
```
Cache-Control: no-cache, no-store, must-revalidate
```

Pero esto NO ES SUFICIENTE para ES module cache. Para forzar recarga completa:
1. Navegar a un dominio completamente diferente (ej: `https://example.com`)
2. Volver a la URL de desarrollo
3. `about:blank` NO limpia el módulo cache

## Alternativa: renombrar archivos

La más radical pero infalible: cambiar el nombre de los archivos (ej: `config.js` → `config.v2.js`) y actualizar todos los imports. No recomendado para desarrollo iterativo.

## Notas

- Este problema es específico de navegadores Chromium. Firefox puede comportarse diferente.
- En producción con bundlers (webpack, vite, esbuild) el problema no existe porque los módulos se empaquetan en un solo bundle.
- Para apps sin bundler (CDN-based vanilla JS como TimeIneco), es un problema recurrente.