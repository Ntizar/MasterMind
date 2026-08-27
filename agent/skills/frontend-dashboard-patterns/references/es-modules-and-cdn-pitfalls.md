# ES Modules, Module Chain Debugging & CDN Vendoring

> Pitfalls descubiertos en TimeIneco v0.8 (2026-06-20). Aplicables a cualquier proyecto vanilla JS sin bundler.

## 1. ES Modules + DOMContentLoaded — init nunca se ejecuta

Cuando se usa `<script type="module">`, los módulos ES se cargan de forma diferida (después de parsing). Si el código usa `document.addEventListener('DOMContentLoaded', ...)`, el listener **nunca se ejecuta** porque el evento ya se disparó.

**Síntoma:** La app parece "muerta". El HTML carga, el CSS aplica, pero nada funciona. No hay errores visibles en consola porque el listener simplemente nunca se registra.

**Fix — detectar estado del documento:**
```javascript
async function init() {
  // toda la inicialización aquí
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();  // Ya cargado → ejecutar directamente
}
```

**Causa técnica:** Los módulos ES (`type="module"`) se cargan con `defer` implícito. El parsing del HTML termina, se disparan los scripts síncronos, se dispara DOMContentLoaded, y DESPUÉS se ejecutan los módulos ES. Por eso el listener nunca captura el evento.

## 2. Module chain debugging — un módulo roto rompe TODA la cadena

Cuando `main.js` importa 10+ módulos y uno tiene un error de sintaxis (ej: `return` fuera de función), **todo el árbol de imports falla silenciosamente**. El navegador muestra un error críptico ("Illegal return statement") pero no dice en qué archivo está el problema.

**Técnica de debug (OBLIGATORIA):**
```bash
# Verificar TODOS los módulos JS uno por uno con node --check
for f in js/*.js; do echo -n "$f: "; node --check "$f" 2>&1 && echo "OK" || echo "FAIL"; done
```

Esto revela inmediatamente cuál módulo tiene el error de sintaxis. En TimeIneco, `shp.js` tenía un `return buf;` fuera de su función contenedora (línea 451), lo que rompía la carga de toda la app.

**Regla:** Si la app no funciona y no hay errores claros en consola, ejecutar `node --check` en TODOS los archivos JS importados antes de buscar bugs lógicos.

**Error de ejemplo (shp.js):**
```
js/shp.js:451
  return buf;
  ^^^^^^
SyntaxError: Illegal return statement
```

## 3. CDN bloqueado — vendorizar dependencias críticas

En entornos con restricciones de red (MicroVMs NaN.builders, corporativos), los CDN externos pueden estar bloqueados. Si una librería crítica (como `docx` para generar Word) falla al cargar, toda la app se rompe.

**Patrón de fix:**
```bash
# 1. Instalar localmente
npm install docx@9.7.1

# 2. Copiar UMD build a directorio vendor
mkdir -p js/vendor
cp node_modules/docx/dist/index.umd.cjs js/vendor/docx.umd.js

# 3. Actualizar HTML para usar ruta local
# ANTES: <script src="https://cdn.jsdelivr.net/npm/docx@8.5.1/build/index.umd.min.js"></script>
# DESPUÉS: <script src="js/vendor/docx.umd.js"></script>
```

**Verificar qué CDN falla:** En browser console:
```javascript
performance.getEntriesByType('resource')
  .filter(r => r.transferSize === 0 && r.duration > 0)
  .map(r => r.name.split('/').pop())
```

Los recursos con `transferSize === 0` y `duration > 0` son los que fallaron al cargar.

**Nota sobre versiones:** Siempre verificar que la versión del paquete existe en npm antes de referenciarla en CDN. `docx@8.5.1` no existía — la versión correcta era `9.7.1`.

## 4. Detección de estado de carga

Para verificar si los módulos cargaron correctamente:
```javascript
// En browser console
JSON.stringify({
  hasMap: !!document.querySelector('.leaflet-container'),
  docxDefined: typeof docx !== 'undefined',
  turfDefined: typeof turf !== 'undefined',
  mapChildren: document.getElementById('mapContainer')?.children.length || 0
})
```

Si `typeof docx === 'undefined'` pero el `<script>` está en el HTML, el CDN está bloqueado.
