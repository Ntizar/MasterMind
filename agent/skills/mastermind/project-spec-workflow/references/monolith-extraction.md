# Extracción Programática de Monolitos

Técnica para refactorizar un monolito HTML+JS (todo inline en un `index.html` de miles de líneas) a una arquitectura modular de archivos separados.

## Cuándo usar

- `index.html` (o equivalente) tiene >2K líneas con JS inline
- Hay 50+ funciones mezcladas en un solo archivo
- El agente necesita descomponer sin perder código
- Un refactor manual (LLM) sería demasiado propenso a errores

## Por qué Python y no LLM

Para 147 funciones, un LLM:
- Pierde funciones (las "olvida" al final del contexto)
- Cambia nombres de variables inadvertidamente
- Introduce errores de sintaxis sutiles
- No es reproducible (cada ejecución da resultado distinto)

Un script Python con regex:
- Es determinista: mismas funciones, mismo resultado
- No pierde código: cada función se extrae por nombre exacto
- Es reproducible: se puede re-ejecutar tras ajustar el MODULE_MAP
- Es auditable: se puede revisar el script antes de ejecutar

## Patrón MODULE_MAP

El corazón del script es un diccionario que mapea nombres de función a archivos destino:

```python
MODULE_MAP = {
    # state.js — estado global + constantes
    'STATE': 'state.js',  # special: extrae bloque de constantes
    'currentState': 'state.js',

    # api.js — fetch de APIs
    'fetchWeather': 'api.js',
    'fetchMarine': 'api.js',
    'fetchAirQuality': 'api.js',

    # charts.js — renderizado de gráficos
    'renderChart': 'charts.js',
    'updateChart': 'charts.js',

    # map.js — mapa Leaflet
    'initMap': 'map.js',
    'addMarkers': 'map.js',

    # tabs.js — gestión de pestañas
    'switchTab': 'tabs.js',
    'renderTab': 'tabs.js',

    # ui.js — utilities
    'showToast': 'ui.js',
    'formatNumber': 'ui.js',

    # main.js — init + event wiring
    'DOMContentLoaded': 'main.js',
    'init': 'main.js',
}
```

Funciones no mapeadas → `unmapped.js` para revisión manual.

## Estructura del script

```
1. Leer index.html completo
2. Extraer bloque <script> inline (todo el JS)
3. Parsear funciones top-level por regex:
   function NAME(...) { ... }
   const NAME = (...) => { ... }
   async function NAME(...) { ... }
4. Para cada función, buscar en MODULE_MAP → archivo destino
5. Extraer cuerpo completo (balanceando llaves { })
6. Escribir cada módulo con sus funciones
7. Generar index.html nuevo con <script src="js/..."> en orden de carga
8. Crear placeholders vacíos para módulos sin funciones top-level
```

## Orden de carga (crítico)

```html
<script src="js/state.js"></script>   <!-- estado global primero -->
<script src="js/api.js"></script>     <!-- funciones de fetch -->
<script src="js/charts.js"></script>  <!-- renderizado -->
<script src="js/map.js"></script>     <!-- mapa -->
<script src="js/tabs.js"></script>    <!-- pestañas -->
<script src="js/ui.js"></script>      <!-- UI utils -->
<!-- panels/* cargados dinámicamente o al final -->
<script src="js/main.js"></script>    <!-- orquestador último -->
```

**Regla:** state.js siempre primero (define globales), main.js siempre último (los consume).

## Pitfall: funciones anidadas

Las funciones definidas DENTRO de otras funciones no son top-level:

```javascript
// TOP-LEVEL — el script extrae esto ✅
function fetchWeather() {
    // ...
    renderWeatherChart(data);
}

// ANIDADA — el script NO extrae esto ❌
function fetchWeather() {
    function renderWeatherChart(data) {  // ← closure, no top-level
        // ...
    }
    renderWeatherChart(data);
}
```

**Solución:** El script crea un placeholder vacío para el módulo. Después, el agente extrae manualmente las funciones anidadas de su función contenedora y las mueve al archivo del módulo.

**Detección:** Después de ejecutar el script, buscar módulos con 0 líneas de funciones (solo comentarios/placeholder). Esos son los que necesitan extracción manual.

## Verificación post-extracción

```bash
# 1. Syntax check (necesario pero NO suficiente)
for f in js/*.js js/panels/*.js; do node --check "$f" || echo "FAIL: $f"; done

# 2. Verificar que no quedan funciones en index.html
grep -c 'function ' index.html  # debe ser ~0

# 3. Verificar que los <script> tags apuntan a archivos que existen
grep '<script src=' index.html

# 4. Abrir en navegador y verificar runtime (lo que node --check no cubre)
```

## Caso real: DataHubEspana

- **Antes:** index.html de 11.539 líneas (588KB), 151 funciones inline
- **Después:** index.html de 2.339 líneas (140KB) + 32 archivos JS modulares
- **Reducción:** 76% del tamaño del HTML
- **Funciones extraídas:** 147 de 151 (4 perdidas por anidamiento → 3 placeholders)
- **Script usado:** `refactor-extractor.py` (486 líneas Python)
- **Tiempo:** ~2 horas incluyendo spec, decisiones, extracción y verificación
