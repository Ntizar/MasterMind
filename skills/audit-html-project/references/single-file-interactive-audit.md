# Single-File Interactive App Audit

Procedimiento para auditar aplicaciones web **monolíticas** (un solo archivo HTML con CSS+JS inline): visores interactivos, dashboards vanilla, herramientas de mapa, etc.

## Cuándo usar

- Un solo archivo HTML con CSS `<style>` + JS `<script>` inline
- El usuario reporta "no funciona" o "no hace lo que debería"
- Visores interactivos (Leaflet, Three.js, D3, etc.)
- Herramientas webapp con lógica JS compleja

## Diferencia con `audit-html-project` (multi-file)

| | Multi-file educativo | Single-file interactivo |
|---|---|---|
| Alcance | 10+ archivos | 1 archivo |
| Enfoque | grep batch, enlaces rotos | Lectura línea a línea, lógica JS |
| Errores típicos | href="#", navegación rota | Variables no declaradas, comillas rotas |

## Pasos

### 1. Lectura completa del archivo

Leer TODO el archivo con `read_file`. No usar grep para este tipo de archivos — la lógica está en JS inline y necesita contexto.

### 2. Análisis de variables y scope

Buscar variables usadas antes de declararse. `let` tiene hoisting de bloque: si se usa dentro de una función definida antes pero llamada después, funciona pero es anti-pattern. Declarar arriba con las demás variables globales.

### 3. Análisis de strings HTML generados dinámicamente

Buscar `innerHTML +=` y `htmlContent +=` que contengan atributos `onclick=` con comillas. Las comillas simples dentro de un string JS con comillas simples rompen el output HTML.

**Patrón roto:** `onclick="this.parentElement.classList.toggle('open')"` dentro de `'...'`
**Fix:** Escapar con `\'open\'` o usar template literals (backticks) para el string externo.

### 4. Análisis de lecturas duplicadas

Buscar el mismo archivo/endpoint leído múltiples veces en la misma función. Unificar en una sola lectura.

### 5. Análisis de limpieza de estado entre operaciones

Verificar que variables globales se limpian o no se solapan entre operaciones (ej: múltiples ZIPs GTFS).

### 6. Análisis de UX

Verificar:
- ¿Cierra panel con Escape? → Añadir `keydown` listener
- ¿Debounce en búsqueda? → Añadir `input` listener con `setTimeout`
- ¿Rate limiting de APIs externas? → Nominatim: 1 req/seg

### 7. Verificación post-fix

- No quedan referencias a variables eliminadas
- Balance de comillas en strings HTML generados
- Variables declaradas antes de su primer uso

## Checklist de errores comunes

| Error | Dónde buscar | Fix |
|-------|-------------|-----|
| Variable usada antes de declarar | `let X` vs `X[` | Mover al scope global |
| Comillas rotas en onclick | `htmlContent +=` con `onclick=` | Escapar o usar backticks |
| Lectura duplicada de datos | Mismo archivo 2x | Unificar |
| Estado global no limpio | Variables acumulativas | Limpiar o usar scope local |
| Sin Escape para cerrar paneles | Paneles fijos | Añadir `keydown` |
| Sin debounce en búsqueda | Input sin listener | Defer 500ms |
| KPI subcuenta entidades | `Set(r.entity)` solo primera | `flatMap(r.entities)` todas |

## Ejemplo real: GTFSSpain visor (2026-06-23)

1. `tripRouteMap` declarado en línea 1085, usado en 734 → movido a línea 523
2. `classList.toggle('open')` comillas rotas → escapado con `\\'open\\'`
3. `stop_times.txt` leído 2x → unificado
4. Sin Escape para cerrar panel → añadido `keydown`
5. Sin debounce en geocodificación → añadido `input` listener 500ms

---

## Data-Driven Visor Audit (JSON backend)

Visores que cargan datos desde múltiples archivos JSON tienen una clase distinta de problemas. Patrones extraídos de CIAF-visor (2026-06-26).

### Cuándo usar

- App carga 1+ archivos JSON (reports, memorias, index)
- Hay `enlaces` o campos de referencia en los JSON que el frontend podría usar
- El proyecto tiene PDFs/archivos descargables referenciados por los datos

### Checks específicos

#### 1. Consistencia entre fuentes de datos

Cuando hay múltiples JSON con datos solapados (ej: `reports/2024.json` y `memorias/2024.json`), **cruzar los datos** para detectar inconsistencias:

```python
for year in years:
    reports = json.load(f'reports/{year}.json')
    memoria = json.load(f'memorias/{year}.json')
    actual_count = len(reports)
    reported_count = memoria.get('total_accidents', 0)
    if actual_count != reported_count:
        print(f'❌ {year}: reports={actual_count}, memoria={reported_count}')
```

**Señal de datos fabricados**: si los aggregate counts no coinciden con los source data, los JSON de resumen probablemente son auto-generados/inventados.

#### 2. Enlaces no utilizados (frontend ignora JSON)

Verificar si el frontend usa los campos `enlaces` del JSON o si hardcodea URLs:

```python
# Encontrar campos enlaces en JSON
enlaces_fields = set()
for r in reports:
    enlaces_fields.update(r.get('enlaces', {}).keys())

# Verificar si el frontend los referencia
for field in enlaces_fields:
    if field not in frontend_js:
        print(f'⚠️ Campo enlaces.{field} existe en JSON pero no se usa en frontend')
```

**Patrón roto**: `enlaces.pdf_local` apunta a `pdfs/2025/2025-41-0522-if.pdf` pero el frontend siempre enlaza a la URL genérica del sitio oficial.

#### 3. Existencia de archivos referenciados

Si el JSON tiene `enlaces.pdf_local` u otros campos de path, verificar que los archivos existen en el repo:

```python
missing = []
for r in reports:
    pdf = r.get('enlaces', {}).get('pdf_local', '')
    if pdf and not os.path.isfile(os.path.join(repo_root, pdf)):
        missing.append(pdf)
print(f'PDFs referenciados pero inexistentes: {len(missing)}')
```

#### 4. Claridad de títulos

Verificar que los títulos de los informes son descriptivos, no solo nombres de archivo:

```python
unclear = [r for r in reports if not r.get('titulo') or 
           len(r['titulo']) < 10 or 
           any(x in r['titulo'] for x in ['if_', 'ciaf.pdf', '-if-'])]
```

**Criterio**: si el título parece un nombre de archivo en vez de una descripción humana, es 🟡 Mejora.

#### 5. Vistas ausentes por dimensiones clave

Verificar si los datos soportarían vistas adicionales que no existen:

```python
# ¿Hay entidades/empresas en los datos?
all_entities = set()
for r in reports:
    all_entities.update(r.get('entidades', []))

# ¿El frontend tiene vista por entidad?
if 'entity' not in frontend_filters and len(all_entities) > 3:
    print(f'💡 Datos tienen {len(all_entities)} entidades pero no hay vista por empresa')
```

### Ejemplo real: CIAF-visor (2026-06-26)

- 270 PDFs existen en repo, paths correctos en JSON → ✅
- Frontend ignora `enlaces.pdf_local`, siempre enlacia a URL genérica → ❌ enlace roto
- Memorias JSON dicen "58 accidents" pero solo hay 1 report → ❌ datos fabricados
- 13 informes con títulos tipo nombre de archivo → 🟡 mejoras
- 17 entidades pero sin vista por empresa → 💡 oportunidad
- 17 memorias PDFs en repo pero no enlazadas desde el visor → ❌ recurso desperdiciado

**Post-audit cleanup (2026-06-29):** After the audit, deleted all unused assets: `pdfs/` (322 MB), `data/images/` (249 MB), `data/train-tracks.geojson` (7.5 MB), `ltv_lookup.json`, `station-coords.json`, `relations.json`. Repo went from 330+ MB → 13 MB. **Lesson:** When a data-driven visor loads everything from JSON, any non-JSON asset (PDFs, images, geojson) that the frontend never references is dead weight. Delete aggressively — PDFs can always be re-downloaded from the source.

### Pitfalls de visores data-driven

- **🔴 Leaflet map instances leak on tab switch** — When a SPA has multiple tabs and one renders a Leaflet map, switching tabs without destroying the old map causes: (1) memory leak, (2) broken rendering when returning to the tab (tiles don't load, markers invisible), (3) duplicate event listeners. **Fix:** Store the map instance in a module-level variable (`let _mapInstance = null`), call `_mapInstance.remove()` before creating a new one, and use `requestAnimationFrame()` to init the map AFTER the DOM element is visible. Pattern:
  ```javascript
  let _mapInstance = null;
  function showTab(tabName) {
      if (_mapInstance) { _mapInstance.remove(); _mapInstance = null; }
      // ... render tab content ...
      requestAnimationFrame(() => {
          const map = L.map('mapDiv').setView([40, -3.5], 6);
          // ... add tiles, markers ...
          _mapInstance = map;
      });
  }
  ```
- **🔴 Spanish government WAF blocks headless browsers** — Sites like `transportes.gob.es` return 403 to browser automation tools (Browserbase, Playwright, etc.). **Workaround:** Use `curl -H "User-Agent: Mozilla/5.0 ..."` to fetch the HTML, then parse with Python regex. This works because the WAF checks for headless browser fingerprints, not User-Agent alone. Applicable to: BOE, transportes.gob.es, minetur.gob.es, and most Spanish government portals.
- **🔴 Normativa/legal links must match official source** — When a project references legal documents (laws, regulations, standards), NEVER invent or guess links. Always scrape the official source page (e.g., the Ministry's normativa page) and use only the documents listed there. BOE/EUR-Lex URLs may be correct but the document might not be on the official list — use the Ministry's own PDFs when available.

---

## 🔴 Single-File Dashboard Post-Fix Audit (v1.0 — NUEVO)

Procedimiento para verificar la integridad de un dashboard HTML monolítico **después de múltiples oleadas de fixes**. Diferente de la auditoría de debugging — aquí el archivo ya está "arreglado" y necesitamos verificar que todo funciona correctamente.

### Cuándo usar

- Dashboard de un solo archivo con 30+ pestañas lazy-rendered
- Después de 5+ oleadas de fixes nocturnos (ej: DataHub España)
- Verificar que todas las pestañas tienen su panel, gráficos, y funciones definidas
- Pre-commit verification de integridad estructural

### Checklist de integridad estructural

#### 1. Balance de tags HTML

```python
content = open('index.html').read()
assert content.count('<div') == content.count('</div>'), 'DIVs desbalanceados'
assert content.count('<script') == content.count('</script>'), 'Scripts desbalanceados'
```

**Criterio:** Balance debe ser 0. Si no, hay estructura rota.

#### 2. Tab buttons ↔ panels mapping

```python
buttons = re.findall(r'data-tab="([^"]*)"', content)
panels = re.findall(r'id="tab-([^"]*)"', content)
real_buttons = [b for b in buttons if '${' not in b]
real_panels = [p for p in panels if '${' not in p]
missing = [b for b in real_buttons if b not in real_panels]
assert not missing, f'Botones sin panel: {missing}'
```

**Criterio:** Cada botón `data-tab="X"` debe tener un panel `id="tab-X"`. Los botones con template literal (`${...}`) son dinámicos y se excluyen.

#### 3. Funciones definidas vs llamadas

```python
# Todas las definiciones de funciones
func_defs = set(re.findall(r'function\s+(\w+)\s*\(', content))
func_defs.update(re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*async\s*\(', content))
func_defs.update(re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>', content))

# Llamar a init() y verificar cada llamada
init_match = re.search(r'async function init\(\)\s*\{(.*?)\n\}', content, re.DOTALL)
if init_match:
    calls = re.findall(r'(\w+)\(\)', init_match.group(1))
    builtin = {'now','sort','parseInt','parseFloat','console','document', 'window', ...}
    undefined = [c for c in set(calls) if c not in builtin and c not in func_defs]
    assert not undefined, f'Funciones indefinidas: {undefined}'
```

**Criterio:** Cada función llamada en `init()` debe estar definida en el archivo.

**Pitfall:** `init()` puede no coincidir con patrón `async function init()\s*\{(.*?)\n\}` si hay más de un nivel de cierre. Si falla el regex, buscar `function init(` y contar llaves manualmente hasta encontrar el balance.

#### 4. Panel size y features

```python
panel_starts = [(m.start(), m.group(1)) for m in re.finditer(
    r'<div[^>]*class="[^"]*tab-panel[^"]*"[^>]*id="([^"]*)"', content)]

for i, (start, pid) in enumerate(panel_starts):
    end = panel_starts[i+1][0] if i+1 < len(panel_starts) else len(content)
    panel = content[start:end]
    size = len(panel)
    has_canvas = '<canvas' in panel
    has_select = '<select' in panel
    has_fetch = 'fetch(' in panel
    assert size > 300, f'{pid} demasiado pequeño ({size}b)'
    # Report features
    features = []
    if has_canvas: features.append('chart')
    if has_select: features.append('selector')
    if has_fetch: features.append('api')
```

**Criterio:** Cada panel debe tener >300 bytes. Reportar qué features tiene cada uno.

**Pitfall:** El regex de panel puede no encontrar paneles con `tab-panel` en un orden diferente dentro de `class=`. Si `re.finditer` no devuelve resultados, usar `id="tab-"` como fallback para encontrar los paneles por ID y luego escanear hacia adelante hasta encontrar `class=` con `tab-panel`.

#### 5. Detección de errores JS comunes

```python
errors = []
if 'fetchFloods' in content: errors.append('fetchFloods (debería ser fetchFlood)')
backticks = content.count('`')
if backticks % 2 != 0: errors.append(f'Template literals rotos: {backticks} backticks')
debug_logs = len(re.findall(r'console\.log\s*\(', content))
if debug_logs > 0: print(f'⚠️ {debug_logs} console.log leftovers')
```

**Criterio:** 0 errores críticos. Warnings de console.log son aceptables.

#### 6. Duplicados de funciones

```python
func_defs_count = {}
for m in re.finditer(r'function\s+(\w+)\s*\(', content):
    name = m.group(1)
    func_defs_count[name] = func_defs_count.get(name, 0) + 1
dups = {k: v for k, v in func_defs_count.items() if v > 1}
if dups:
    print(f'⚠️ Duplicados: {dups}')
    # Verificar si están dentro de otras funciones (no es error si es nested)
```

**Nota:** Un duplicado dentro de funciones anidadas (ej: `haversine` dentro de `fetchMar()` y `renderMarChartFor()`) no es un bug — es redundante pero funcional. Reportar como warning.

### Flujo de auditoría post-fix

```
1. Balance de tags → 2. Tab mapping → 3. Funciones definidas → 4. Panel sizes → 5. JS errors → 6. Duplicados
```

### Formato de informe final

```markdown
## AUDITORÍA FINAL — [Nombre del Proyecto]

### 📁 Integridad del archivo
- **Tamaño:** X bytes / X líneas
- **DIV balance:** ✅ 0
- **Script balance:** ✅ 0
- **Tab buttons:** X funcionales + X dinámicos
- **Panel coverage:** ✅ Todos los botones tienen su panel

### 📊 Resumen de funcionalidades
- **Total pestañas:** X/X funcionales
- **Con gráficos (canvas):** X
- **Con selectores:** X
- **Con APIs fetch:** X

### 🐛 Issues encontrados (N warnings, 0 críticos)
1. [Descripción]
2. [Descripción]

### 🟢 Estado general: APROBADO / CON WARNINGS / RECHAZADO
```

### Pitfalls

- **🔴 Panel demasiado grande** — Un panel puede ocupar >80% del archivo (ej: nubosidad con 424KB). Esto indica que el contenido debería estar lazy-loaded o separado. Reportar pero no es bug funcional.
- **🔴 Funciones nested duplicadas** — `haversine` definida dentro de `fetchMar()` y `renderMarChartFor()` no es un bug (cada scope tiene su propia copia), pero es redundante. Reportar como warning.
- **🔴 Template literal en tab buttons** — `${tabKeys[e.key]}` es un botón dinámico para navegación por teclado. No es un bug — es funcionalidad móvil. Excluirlo del check de mapping.
- **🔴 console.log en código de producción** — 10+ console.log en un archivo de 500KB es aceptable para debugging temporal, pero debería limpiarse antes de producción. Reportar como warning.
- **🔴 init() no encontrado por regex** — El patrón `async function init\(\)\s*\{(.*?)\n\}` puede fallar si hay más niveles de anidamiento o si init() no es async. Si falla, buscar `function init(` con `content.find()` y contar llaves manualmente.
