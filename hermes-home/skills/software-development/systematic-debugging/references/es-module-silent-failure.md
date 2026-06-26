# ES Module Silent Failure — Debugging Pattern

## El síntoma

La página web carga (HTML visible, assets servidos), pero **nada funciona**:
- El mapa no se renderiza (Leaflet no se inicializa)
- Los botones no responden
- No hay ningún error en la consola del navegador
- Los archivos JS se sirven correctamente (HTTP 200)

## La causa raíz

Un `import` en un módulo ES (`type="module"`) referencia un nombre que **no existe** en la exportación del módulo destino. Ejemplo:

```javascript
// pdf.js — import
import { downloadShp } from './shp.js';  // ❌ "downloadShp" NO EXISTE
```

```javascript
// shp.js — export  
export async function downloadSHP(modo, minutos, geojson) {  // ✅ "downloadSHP" (S mayúscula)
```

El navegador no muestra ningún error porque los ES modules fallan **en cascada silenciosamente**: si un módulo de la cadena falla al cargar, TODOS los importadores también fallan, **pero sin lanzar una excepción visible en `window.onerror`**.

## Caso real (TimeIneco, 2026-06-19)

El proyecto TimeIneco tenía 7 módulos ES cargados desde `main.js`. `pdf.js` importaba `{ downloadShp }` con `S` minúscula, pero la función se exportaba como `downloadSHP` con `SHP` mayúscula.

**Cadena de fallo:**
```
main.js → import { generarPDF } from './pdf.js' → import { downloadShp } from './shp.js' ❌
                                                              ↓
main.js no se ejecuta → initMap() nunca se llama → mapa no se renderiza → botones sin handlers
```

**Síntomas observados:**
- `pageSnapshot` muestra solo 12 elementos (sidebar sin mapa)
- `browser_console` reporta 0 mensajes y `js_errors: [{message: "", source: "exception"}]`
- Leaflet está disponible (`L.version = "1.9.4"`)
- El mapContainer existe y tiene dimensiones (900×577px)
- El CSS está correcto (`.ti-map-container { flex: 1 }`)
- Crear el mapa manualmente desde la consola funciona: `L.map('mapContainer')` ✅

## Diagnóstico (cómo detectarlo)

### Paso 1: Confirmar que los módulos no se ejecutan

```javascript
// En la consola del navegador: comprobar si el DOMContentLoaded handler se ejecutó
document.getElementById('resultsCard').style.display === 'none'
  ? 'Module did NOT init' 
  : 'Module init OK'
```

### Paso 2: Verificar cada import de la cadena

Buscar TODOS los imports del módulo principal y verificar que cada nombre exportado existe en cada módulo destino:

```bash
# Listar imports del módulo principal
grep "^import" js/main.js

# Para cada módulo importado, verificar que las funciones importadas existen:
grep "^export" js/map.js | grep -c "initMap"  # ¿existe initMap?
grep "^export" js/pdf.js | grep -c "generarPDF"  # ¿existe generarPDF?
```

### Paso 3: Caso especial — imports no utilizados

Si un archivo importa una función que **nunca se usa**, y el nombre del import no coincide con ningún export, el módulo igualmente falla. **Los ES modules no hacen tree-shaking en el navegador** — el módulo completo se invalida si hay un solo import roto.

### Paso 4: Verificar nombres de exportación exactos

El matching de import/export en ES modules es **case-sensitive** con respecto a la declaración exacta de export:

```javascript
export function downloadSHP(...)   // exportado como: downloadSHP
import { downloadShp } from '...'  // importado como: downloadShp ❌
```

La diferencia entre `SHP` y `Shp` es suficiente para romper la cadena entera.

## Prevención

### 1. Verificar sintaxis de módulos completa

Tras añadir cualquier nuevo import/export, verificar que todos los nombres coinciden:

```bash
node -e "
const fs = require('fs');
const main = fs.readFileSync('js/main.js', 'utf8');
const imports = [...main.matchAll(/import\\s+\\{([^}]+)\\}\\s+from\\s+['\"]([^'\"]+)['\"]/g)];
for (const [, names, path] of imports) {
  const mod = fs.readFileSync(path.replace('./', 'js/').replace('.js', '.js'), 'utf8') || '(not found)';
  for (const n of names.split(',').map(s => s.trim())) {
    if (!mod.includes(\`export \${n}\`) && !mod.includes(\`export default \${n}\`)) {
      console.log(\`❌ \${path} NO exporta '\${n}'\`);
    }
  }
}
"
```

### 2. Test de integración básico

Crear un pequeño test HTML que importe el módulo principal y verifique que se ejecuta:

```html
<script type="module">
import { initMap } from './js/main.js';
// Si esto se ejecuta, los módulos cargan.
// Si no, algún import está roto.
console.log('✅ Módulos cargados correctamente');
</script>
```

### 3. Cache-busting consciente

Cuando se añaden nuevos imports, actualizar el cache-buster (`?v=N`) del módulo principal y de TODOS los módulos que importa. Si solo se actualiza `main.js?v=6` pero los otros módulos quedan con la versión anterior cacheada, el mismatch puede persistir.

## Lectura adicional

- [MDN: JavaScript modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) — la especificación ES module no produce errores visibles para imports rotos
- Ver también `routing-isochrones` pitfall #10 sobre cache de ES modules y por qué no se refrescan