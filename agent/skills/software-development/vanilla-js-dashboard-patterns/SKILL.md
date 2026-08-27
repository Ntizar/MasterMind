     1|---
     2|name: vanilla-js-dashboard-patterns
     3|description: >
     4|  Patrones para dashboards frontend vanilla JS multi-archivo: orquestación de init(),
     5|  lazy loading de pestañas, manejo de overlays/loading states, comunicación entre
     6|  scripts sin bundler, error handling defensivo.
     7|tags: [frontend, dashboard, vanilla-js, patterns, architecture]
     8|---
     9|
    10|# Vanilla JS Dashboard Patterns — Arquitectura multi-archivo sin bundler
    11|
    12|## Estructura típica
    13|
    14|```
    15|index.html          ← carga scripts en orden específico
    16|js/
    17|  state.js          ← constantes + let globales + Object.defineProperty → window
    18|  datahub.js        ← IIFE: cache + fetch wrapper (se carga primero)
    19|  api.js            ← funciones de fetch por fuente de datos
    20|  charts.js         ← funciones de renderizado de gráficos
    21|  map.js            ← Leaflet/Mapbox init + interacciones
    22|  ui.js             ← sidebar, toast, clock, mobile
    23|  main.js           ← ORQUESTADOR: init() + event wiring + start
    24|  panels/
    25|    agua.js, economia.js, clima.js, ...
    26|```
    27|
    28|## Regla de carga de scripts
    29|
    30|```html
    31|<!-- Orden: librerías CDN → state → helpers → panels → main (SIEMPRE último) -->
    32|<script src="leaflet.js"></script>
    33|<script src="chart.js"></script>
    34|<script src="js/datahub.js?v=YYYYMMDD"></script>  <!-- IIFE, no depende de nada -->
    35|<script src="js/state.js?v=YYYYMMDD"></script>     <!-- const + let + defineProperty -->
    36|<script src="js/api.js?v=YYYYMMDD"></script>        <!-- depende de state -->
    37|<script src="js/charts.js?v=YYYYMMDD"></script>     <!-- depende de state + chart.js -->
    38|<script src="js/map.js?v=YYYYMMDD"></script>        <!-- depende de state + leaflet -->
    39|<script src="js/tabs.js?v=YYYYMMDD"></script>
    40|<script src="js/ui.js?v=YYYYMMDD"></script>
    41|<script src="js/panels/*.js?v=YYYYMMDD"></script>  <!-- dependen de state + api + charts -->
    42|<script src="js/main.js?v=YYYYMMDD"></script>       <!-- ORQUESTADOR, SIEMPRE ÚLTIMO -->
    43|```
    44|
    45|## Patrón de orquestación (main.js)
    46|
    47|```js
    48|// ===== Safety nets =====
    49|setTimeout(() => {
    50|    const ol = document.getElementById('loading-overlay');
    51|    if (ol && !ol.classList.contains('hidden')) ol.classList.add('hidden');
    52|}, 10000);
    53|
    54|async function init() {
    55|    initMap();                    // 1. Mapa (puede fallar → no bloquea)
    56|    await loadProvinces();        // 2. Datos esenciales (GeoJSON)
    57|    
    58|    // 3. Fetches paralelos no críticos
    59|    Promise.allSettled([
    60|        fetchEnergyData(),
    61|        fetchWeather(),
    62|        fetchSeismic()
    63|    ]).then(() => {
    64|        document.getElementById('loading-overlay').classList.add('hidden');
    65|        showToast('Dashboard cargado', 'success', 3000);
    66|    });
    67|    
    68|    // 4. Fetches independientes (fire and forget)
    69|    renderWater();
    70|    renderEconomy();
    71|    fetchAireExt('all');
    72|    fetchGBFS();
    73|    // ...
    74|}
    75|
    76|init().catch(err => {
    77|    console.error('init() falló:', err);
    78|    document.getElementById('loading-overlay')?.classList.add('hidden');
    79|});
    80|```
    81|
    82|## Lazy rendering de pestañas
    83|
    84|```js
    85|// Solo renderizar cuando el usuario abre la pestaña
    86|document.querySelectorAll('.tab-btn').forEach(btn => {
    87|    btn.addEventListener('click', () => {
    88|        const tab = btn.getAttribute('data-tab');
    89|        if (tab === 'ambiente' && !window.__ambienteRendered) {
    90|            window.__ambienteRendered = true;
    91|            renderParks();  // Solo se ejecuta la primera vez
    92|        }
    93|    });
    94|});
    95|```
    96|
    97|## Comunicación entre scripts sin bundler
    98|
    99|### state.js (el "store")
   100|```js
   101|let map = null;
   102|let charts = {};
   103|
   104|// ✅ SIEMPRE Object.defineProperty para variables que cambian
   105|Object.defineProperty(window, 'map', {
   106|  get() { return map; },
   107|  set(v) { map = v; },
   108|  configurable: true
   109|});
   110|
   111|// Para constantes: window.X = X está OK (no cambian)
   112|window.CCAA_NAMES = CCAA_NAMES;
   113|window.setTxt = setTxt;
   114|```
   115|
   116|### api.js (consumidor)
   117|```js
   118|async function fetchWeather() {
   119|    // Lee de window.map (que está sincronizado via getter)
   120|    const center = map ? map.getCenter() : [40.0, -3.5];
   121|    // ...
   122|}
   123|```
   124|
   125|## Error handling defensivo
   126|
   127|```js
   128|// Cada fetch individual con try/catch + fallback
   129|async function fetchEnergyData() {
   130|    try {
   131|        const res = await fetch(esiosUrl, { headers });
   132|        if (res.status === 403) {
   133|            console.log('Auth required');
   134|        } else if (res.ok) {
   135|            // procesar datos
   136|        }
   137|    } catch (err) {
   138|        console.log('API not available:', err.message);
   139|    }
   140|    // Siempre llegar al final (no lanzar excepción)
   141|    // Fallback values si no hay datos
   142|    if (!pvpcOk) setTxt('kpi-pvpc', 'N/D');
   143|}
   144|
   145|// Para promises críticos: .catch() SIEMPRE
   146|somePromise().catch(err => {
   147|    showToast('Error', 'error');
   148|    // Nunca dejar promise sin catch → stuck silencioso
   149|});
   150|```
   151|
   152|## Patrón moderno: ES6 modules + `<script type="module">`
   153|
   154|Para proyectos nuevos, preferir ES6 modules sobre IIFE:
   155|
   156|```html
   157|<!-- index.html — importa módulos en el orden de dependencias -->
   158|<script type="module">
   159|    import { initApp } from './js/main.js';
   160|    import { initSurvey } from './js/survey.js';
   161|    import { initDiagnostico } from './js/diagnostico.js';
   162|    import { initDAFO } from './js/dafo.js';
   163|    import { initObjetivos } from './js/objetivos.js';
   164|    import { initInforme } from './js/informe.js';
   165|    
   166|    initApp();
   167|    setTimeout(() => {
   168|        initSurvey(); initDiagnostico(); initDAFO();
   169|        initObjetivos(); initInforme();
   170|    }, 100);
   171|</script>
   172|```
   173|
   174|Cada módulo exporta funciones nombradas. No necesita `window.X = X`. Comunicación vía `window.appState` compartido.
   175|
   176|## Auditoría DOM — Verificar IDs ANTES de probar
   177|
   178|**PITFALL CRÍTICO:** Los módulos buscan IDs en el DOM con `getElementById()`. Si un ID no existe, el módulo falla silenciosamente (return early). **NUNCA empieces a probar sin verificar que todos los IDs coinciden.**
   179|
   180|Procedimiento de auditoría (hacer antes del primer test en navegador):
   181|
   182|```python
   183|import re
   184|
   185|# 1. Extraer IDs del HTML
   186|html = open('index.html').read()
   187|html_ids = set(re.findall(r'id="([^"]+)"', html))
   188|
   189|# 2. Extraer IDs buscados por cada módulo JS
   190|patterns = [
   191|    r"getElementById\(['\"]([^'\"]+)['\"]\)",
   192|    r"querySelector\(['\"]#([^'\"]+)['\"]\)",
   193|    r"querySelectorAll\(['\"]#([^'\"]+)['\"]\)",
   194|]
   195|
   196|for jsfile in glob.glob('js/*.js'):
   197|    js = open(jsfile).read()
   198|    for pattern in patterns:
   199|        ids = re.findall(pattern, js)
   200|        for id_ in ids:
   201|            if id_ not in html_ids and len(id_) > 2:
   202|                print(f"❌ {jsfile} busca '{id_}' pero NO existe en HTML")
   203|```
   204|
   205|**Solo IDs alfanuméricos válidos:** filtrar con `re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', id_)`. Los IDs que contienen `#`, `.`, espacios, o caracteres especiales no son IDs DOM válidos.
   206|
   207|**IDs dinámicos:** Algunos IDs se generan dinámicamente (ej: `survey-form` creado por `generateSurveyHTML()` al hacer clic en un botón). Estos NO pueden estar en HTML estático, pero el listener que los captura debe ejecutarse DESPUÉS de la inyección. Verificar que el orden es: inyección → captura → listener.
   208|
   209|## Panel show/hide obligatorio
   210|
   211|Cada módulo que calcula datos DEBE mostrar su panel. Sin esto, el usuario calcula datos que no ve.
   212|
   213|```js
   214|// EN initX() — tras calcular datos:
   215|const panel = document.getElementById('panel-id');
   216|if (panel) panel.style.display = 'block';
   217|
   218|// EN loadSavedX() — tras cargar datos guardados:
   219|const panel = document.getElementById('panel-id');
   220|if (panel) panel.style.display = 'block';
   221|```
   222|
   223|**PITFALL:** Si el panel tiene `display:none` en CSS y el módulo no lo muestra, el cálculo se ejecuta pero el usuario no ve nada. **Siempre verificar show/hide en ambos caminos: cálculo nuevo Y carga guardada.**
   224|
   225|## localStorage keys — SET y GET siempre emparejados
   226|
   227|Cada key que se SETea debe tener un GET correspondiente en `loadSavedX()`:
   228|
   229|```js
   230|// SET (en initX)
   231|localStorage.setItem('pmst_diagnostico', JSON.stringify(data));
   232|
   233|// GET (en loadSavedX)
   234|const json = localStorage.getItem('pmst_diagnostico');
   235|if (!json) return;
   236|```
   237|
   238|**PITFALL:** Si una key solo se SETea pero nunca se GETea, los datos se pierden al recargar. Verificar con regex:
   239|
   240|```python
   241|ls_sets = re.findall(r"localStorage\.setItem\(['\"]([^'\"]+)['\"]", js)
   242|ls_gets = re.findall(r"localStorage\.getItem\(['\"]([^'\"]+)['\"]", js)
   243|for k in ls_sets:
   244|    if k not in ls_gets:
   245|        print(f"⚠️ '{k}' se SETea pero nunca se GETea")
   246|```
   247|
   248|## Canvas chart IDs — verificar contra HTML
   249|
   250|Los `<canvas>` de Chart.js deben existir en el HTML y ser buscados por el módulo:
   251|
   252|```python
   253|# HTML
   254|html_charts = re.findall(r'canvas id="([^"]+)"', html)
   255|
   256|# JS
   257|chart_gets = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js)
   258|
   259|# Verificar
   260|for cid in html_charts:
   261|    if cid not in chart_gets:
   262|        print(f"⚠️ Canvas '{cid}' en HTML pero no buscado por JS")
   263|```
   264|
   265|## Patrón moderno: ES6 modules + `<script type="module">`
   266|
   267|Para proyectos nuevos, preferir ES6 modules sobre IIFE:
   268|
   269|```html
   270|<!-- index.html — importa módulos en el orden de dependencias -->
   271|<script type="module">
   272|    import { initApp } from './js/main.js';
   273|    import { initSurvey } from './js/survey.js';
   274|    import { initDiagnostico } from './js/diagnostico.js';
   275|    import { initDAFO } from './js/dafo.js';
   276|    import { initObjetivos } from './js/objetivos.js';
   277|    import { initInforme } from './js/informe.js';
   278|    
   279|    initApp();
   280|    setTimeout(() => {
   281|        initSurvey(); initDiagnostico(); initDAFO();
   282|        initObjetivos(); initInforme();
   283|    }, 100);
   284|</script>
   285|```
   286|
   287|Cada módulo exporta funciones nombradas. No necesita `window.X = X`. Comunicación vía `window.appState` compartido.
   288|
   289|## Auditoría DOM — Verificar IDs ANTES de probar
   290|
   291|**PITFALL CRÍTICO:** Los módulos buscan IDs en el DOM con `getElementById()`. Si un ID no existe, el módulo falla silenciosamente (return early). **NUNCA empieces a probar sin verificar que todos los IDs coinciden.**
   292|
   293|Procedimiento de auditoría (hacer antes del primer test en navegador):
   294|
   295|```python
   296|import re
   297|
   298|# 1. Extraer IDs del HTML
   299|html = open('index.html').read()
   300|html_ids = set(re.findall(r'id="([^"]+)"', html))
   301|
   302|# 2. Extraer IDs buscados por cada módulo JS
   303|patterns = [
   304|    r"getElementById\(['\"]([^'\"]+)['\"]\)",
   305|    r"querySelector\(['\"]#([^'\"]+)['\"]\)",
   306|    r"querySelectorAll\(['\"]#([^'\"]+)['\"]\)",
   307|]
   308|
   309|for jsfile in glob.glob('js/*.js'):
   310|    js = open(jsfile).read()
   311|    for pattern in patterns:
   312|        ids = re.findall(pattern, js)
   313|        for id_ in ids:
   314|            if id_ not in html_ids and len(id_) > 2:
   315|                print(f"❌ {jsfile} busca '{id_}' pero NO existe en HTML")
   316|```
   317|
   318|**Solo IDs alfanuméricos válidos:** filtrar con `re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', id_)`. Los IDs que contienen `#`, `.`, espacios, o caracteres especiales no son IDs DOM válidos.
   319|
   320|**IDs dinámicos:** Algunos IDs se generan dinámicamente (ej: `survey-form` creado por `generateSurveyHTML()` al hacer clic en un botón). Estos NO pueden estar en HTML estático, pero el listener que los captura debe ejecutarse DESPUÉS de la inyección. Verificar que el orden es: inyección → captura → listener.
   321|
   322|## Panel show/hide obligatorio
   323|
   324|Cada módulo que calcula datos DEBE mostrar su panel. Sin esto, el usuario calcula datos que no ve.
   325|
   326|```js
   327|// EN initX() — tras calcular datos:
   328|const panel = document.getElementById('panel-id');
   329|if (panel) panel.style.display = 'block';
   330|
   331|// EN loadSavedX() — tras cargar datos guardados:
   332|const panel = document.getElementById('panel-id');
   333|if (panel) panel.style.display = 'block';
   334|```
   335|
   336|**PITFALL:** Si el panel tiene `display:none` en CSS y el módulo no lo muestra, el cálculo se ejecuta pero el usuario no ve nada. **Siempre verificar show/hide en ambos caminos: cálculo nuevo Y carga guardada.**
   337|
   338|## localStorage keys — SET y GET siempre emparejados
   339|
   340|Cada key que se SETea debe tener un GET correspondiente en `loadSavedX()`:
   341|
   342|```js
   343|// SET (en initX)
   344|localStorage.setItem('pmst_diagnostico', JSON.stringify(data));
   345|
   346|// GET (en loadSavedX)
   347|const json = localStorage.getItem('pmst_diagnostico');
   348|if (!json) return;
   349|```
   350|
   351|**PITFALL:** Si una key solo se SETea pero nunca se GETea, los datos se pierden al recargar. Verificar con regex:
   352|
   353|```python
   354|ls_sets = re.findall(r"localStorage\.setItem\(['\"]([^'\"]+)['\"]", js)
   355|ls_gets = re.findall(r"localStorage\.getItem\(['\"]([^'\"]+)['\"]", js)
   356|for k in ls_sets:
   357|    if k not in ls_gets:
   358|        print(f"⚠️ '{k}' se SETea pero nunca se GETea")
   359|```
   360|
   361|## Canvas chart IDs — verificar contra HTML
   362|
   363|Los `<canvas>` de Chart.js deben existir en el HTML y ser buscados por el módulo:
   364|
   365|```python
   366|# HTML
   367|html_charts = re.findall(r'canvas id="([^"]+)"', html)
   368|
   369|# JS
   370|chart_gets = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]", js)
   371|
   372|# Verificar
   373|for cid in html_charts:
   374|    if cid not in chart_gets:
   375|        print(f"⚠️ Canvas '{cid}' en HTML pero no buscado por JS")
   376|```
   377|
   378|## Checklist antes de push
   379|
   380|- [ ] ¿Los scripts se cargan en orden correcto?
   381|- [ ] ¿`window.X = X` está DESPUÉS de la declaración de X?
   382|- [ ] ¿Variables que cambian usan Object.defineProperty?
   383|- [ ] ¿Tiene `.catch()` en promises críticos?
   384|- [ ] ¿Tiene safety timeout para overlays?
   385|- [ ] ¿Version strings bumpeados en index.html?
   386|- [ ] ¿AUDITORÍA DOM: todos los IDs buscados existen en HTML?
   387|- [ ] ¿AUDITORÍA DOM: IDs dinámicos se inyectan antes de ser capturados?
   388|- [ ] ¿Cada módulo muestra su panel tras calcular datos?
   389|- [ ] ¿Cada módulo muestra su panel tras cargar datos guardados?
   390|- [ ] ¿Cada localStorage key tiene SET y GET emparejados?
   391|- [ ] ¿Canvas charts en HTML son buscados por los módulos?
   392|- [ ] ¿Servidor de desarrollo está activo antes de probar?
   393|
   394|## Referencias
   395|
   396|- **Auditoría DOM completa:** `references/dom-audit-checklist.md` — script de verificación automática de IDs, localStorage keys, canvas charts y estructura HTML antes de probar en navegador
   397|- [ ] ¿AUDITORÍA DOM: todos los IDs buscados existen en HTML?
   398|- [ ] ¿AUDITORÍA DOM: IDs dinámicos se inyectan antes de ser capturados?
   399|- [ ] ¿Cada módulo muestra su panel tras calcular datos?
   400|- [ ] ¿Cada módulo muestra su panel tras cargar datos guardados?
   401|- [ ] ¿Cada localStorage key tiene SET y GET emparejados?
   402|- [ ] ¿Canvas charts en HTML son buscados por los módulos?
   403|- [ ] ¿Servidor de desarrollo está activo antes de probar?
   404|
   405|## Referencias
   406|
   407|- **Auditoría DOM completa:** `references/dom-audit-checklist.md` — script de verificación automática de IDs, localStorage keys, canvas charts y estructura HTML antes de probar en navegador
   408|

## IDs Dinámicos vs Estáticos

- IDs estáticos → deben existir en HTML
- IDs dinámicos → generados por JS en runtime (ej: `survey-form`), no deben estar en HTML
- Los IDs dinámicos se capturan tras insertar el HTML generado en el DOM

## Panel Show/Hide Pattern

Cada módulo que oculta/muestra paneles:
- Usa `style.display = 'block'` para mostrar
- Usa `style.display = 'none'` para ocultar
- Verifica que el ID del panel existe antes de manipular

## Canvas Charts

Los `<canvas>` de Chart.js deben existir en HTML antes de que el módulo intente crear el chart.
Verificar con regex:
```python
html_charts = re.findall(r'canvas id="([^"]+)"', html)
chart_gets = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js)
for cid in html_charts:
    if cid not in chart_gets:
        print(f"⚠️ Canvas '{cid}' en HTML pero no buscado por JS")
```

## Despliegue Estático

- GitHub Pages: branch `main`, ruta `/`
- URL: `https://<usuario>.github.io/<repo>/`
- No requiere backend
- Solo necesita API keys para servicios externos (ORS, Nominatim, etc.)

## Patrón "Herramienta Profesional" vs "Documento Superficial"

**PITFALL CRÍTICO:** Cuando el usuario dice "¿esto es realmente completo?" o "¿no crees que deberías implementar MUCHISIMAS mas cosas?", significa que la herramienta ES SUPERFICIAL. El documento bonito sin datos reales NO ES una herramienta.

**Señales de que la herramienta ES SUPERFICIAL:**
- Solo genera un documento/report final
- Sin mapas interactivos
- Sin gráficas con datos reales
- Sin comparativas
- Sin resultados de encuestas visibles
- Sin gestión de datos (empleados, vehículos, departamentos)
- Sin oferta de transporte público
- Sin seguimiento temporal

**Arquitectura profesional mínima para una herramienta de datos:**

```
proyecto/
├── js/
│   ├── app.js           — Estado global, IndexedDB, CRUD completo
│   ├── mapa.js          — Mapa interactivo (Leaflet/OpenLayers)
│   ├── graficas.js      — 9+ tipos de gráficas (Chart.js)
│   ├── export.js        — PDF/DOCX/ZIP profesional
│   ├── config.js        — APIs y constantes
│   └── main.js          — Orquestador
├── index.html           — 10+ secciones/tabs
├── css/
│   └── style.css        — Responsive completo
├── SPEC.md              — Arquitectura documentada
└── deploy.sh            — Script de deploy
```

**Módulos mínimos de una herramienta profesional de datos:**
1. **Mapa interactivo** — isocronas, capas, POI, marcadores
2. **Gráficas avanzadas** — doughnut, bar, line, horizontal, polar, scatter, pie
3. **Gestión de datos** — CRUD completo con IndexedDB
4. **Transporte/oferta** — paradas cercanas, frecuencias, cobertura
5. **Flota/vehículos** — CRUD vehículos, combustible, km, CO2e
6. **Comparativas** — vs media nacional, vs sector, vs objetivos
7. **Seguimiento temporal** — KPIs a lo largo del tiempo, evolución
8. **Export profesional** — HTML, Markdown, ZIP con todos los formatos
9. **Dashboard resumen** — 8+ KPIs, 4+ gráficas principales, mapa mini
10. **Estructura completa** — sidebar, 10+ tabs, formularios

**Ejemplo real aplicado:** PLANDEMOVILIDAD v1 → v2
- v1: Documento bonito sin datos reales (superficial)
- v2: 10 módulos profesionales, IndexedDB, 9 tipos de gráficas, Leaflet, CRUD completo, comparativas nacionales, seguimiento KPIs, flota corporativa, export ZIP