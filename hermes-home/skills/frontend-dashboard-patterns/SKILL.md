---
name: frontend-dashboard-patterns
description: "Patrones completos para dashboards frontend vanilla JS: cliente API robusto, orquestación de carga, error boundaries, tabs con navegación, persistencia, fechas, colores, sparklines, Web Workers y debugging. Todo lo que necesitas para construir dashboards resilientes sin bundler."
version: "1.5.0"
author: Hermes Agent
tags: [frontend, dashboard, patterns, vanilla-js, resilience, geodatos, leaflet, choropleth]
---

# Frontend Dashboard Patterns — Colección Completa

Patrones reutilizables para dashboards frontend vanilla JS sin bundler. Inspirados en ESIOS Dashboard y Ntizar Aurora.

## Tabla de Contenidos

1. [Cliente API Robusto](#1-cliente-api-robusto) — reintentos, circuit breaker, timeouts
2. [Orquestación de Carga](#2-orquestación-de-carga) — Promise.allSettled, anti-doble-carga, cache fallback
3. [Error Boundaries](#3-error-boundaries) — overlay global, errores por sección, retry
4. [Tabs con Navegación](#4-tabs-con-navegación) — hash navigation, lazy-loading, deep-linking
5. [Persistencia de Estado](#5-persistencia-de-estado) — localStorage con validación, expiración, corrupción
6. [Manejo de Fechas](#6-manejo-de-fechas) — UTC→local, zonas horarias, DST
7. [Sistema de Colores](#7-sistema-de-colores) — tokens CSS, modo oscuro, variables semánticas
8. [Sparklines con Plotly](#8-sparklines-con-plotly) — mini gráficos inline optimizados
9. [Web Workers + Comlink](#9-web-workers--comlink) — cálculos pesados sin bloquear UI
10. [Debugging Patterns](#10-debugging-patterns) — scope, lifecycle, DOM integrity, paréntesis desbalanceados, checklist página en blanco
11. [Aurora Design System](#11-aurora-design-system) — CSS puro, 11 packs opt-in, namespaced .nz, 5 skins
12. [Geodatos Choropleth](#12-geodatos-choropleth) — Leaflet + Canvas, TopoJSON, lazy loading geodatos
13. [GTFS Browser Parser](#13-gtfs-browser-parser) — parsing GTFS en navegador sin servidor
14. [Three.js 3D Scenes](#14-threejs-3d-scenes) — escenas 3D interactivas con texturas procedurales, partículas con identidad, zoom a partícula individual, raycasting, labels flotantes, WebSocket sync, deep linking
15. [Three.js Escenarios JSON](references/threejs-scenario-loading.md) — patrón para cargar escenarios desde JSON con validación de schema, normalización y conversión de parámetros a wave params del shader
16. [ESLint v10 Flat Config](#16-eslint-v10-flat-config) — flat config, globals, ignores
17. [Vite HTML Script Processing](#17-vite-html-script-processing) — IIFEs, post-build, rutas relativas
18. [Full-Stack SPA Audit Pattern](#18-full-stack-spa-audit-pattern) — auditar SPA con backend + frontend (Express + vanilla JS)
19. [Toast Notifications](#19-toast-notifications) — sistema de feedback UX con queue, animaciones y auto-dismiss
20. [Conservative Vanilla JS Modernization](#20-conservative-vanilla-js-modernization) — refactorizar ES5→ES6 en 6 fases sin frameworks, sin romper nada
21. [Data Integrity & Graceful Degradation](#21-data-integrity--graceful-degradation) — nunca inventar datos, fallback chains, empty states honestos, limitaciones de contenedores
22. [Hero Redesign Pattern](references/hero-redesign-pattern.md) — primera pantalla con datos reales + acciones rápidas, no hero vacío
23. [NaN Deploy Cache Pattern](references/nan-deploy-cache-pattern.md) — verificación de deploy, cache de Cloudflare, debugging "no cargan datos"
24. [switchTab Pattern — onclick + event listener](references/switchtab-pattern.md) — función switchTab para onclick inline + event listener, hero placement, quick panel en tab correcta
25. [Tab System con Sidebar](references/tab-system-sidebar-pattern.md) — Sistema completo de tabs con sidebar de navegación, hero, lazy-loading, persistencia de estado y toast notifications

25. [Vanilla JS SPA Module Extension](#25-vanilla-js-spa-module-extension) — añadir nuevos módulos a un dashboard SPA existente

26. [Single-File SPA con Aurora](#26-single-file-spa-con-aurora) — patrón completo de dashboard en un solo HTML: sidebar + tabs + hero + lazy-loading + localStorage + toasts. Base para proyectos como ContrataPúblico.
27. [Single-File SPA con datos grandes](#27-single-file-spa-con-datos-grandes) — patrón para embeber datasets grandes (JSON de cientos de KB) en SPAs de un solo archivo sin romper el deploy.
28. [Debugging `typeof LEY_DATA === 'undefined'`](references/single-file-spa-large-data.md) — checklist de 4 causas: `</script>` collision, strings con newlines, Content-Type, CSP.
29. [Migración Completa a Aurora](references/aurora-migration-pattern.md) — patrón de 5 fases para migrar un HTML existente con CSS custom propio al Aurora Design System (auditoría → packs → componentes → CSS mínimo → JS dinámico). Incluye mapeo de componentes, pitfalls de mesh/orbs/gradientes, y métricas objetivo.

30. [Three.js Particle Systems](#30-threejs-particle-systems) — sistemas de partículas con Three.js: pool reciclado, shaders custom, espuma, spray, humo, fuego. Partículas con vida limitada, tamaño variable, blending additive.

---

## 1. Cliente API Robusto

Clase `ApiClient` con reintentos exponenciales (backoff + jitter), circuit breaker por endpoint, timeouts por operación, y clasificación de errores HTTP.

**Reglas clave:**
- No reintentar 4xx (excepto 429)
- Circuit breaker: N fallos → abrir circuito T segundos → half-open → cerrar/reabrir
- Timeout por request con AbortController
- Integrar con `Promise.allSettled` para carga paralela tolerante a fallos

**Ver:** `references/api-client-pattern.md` para código completo.

---

## 2. Orquestación de Carga

Clase `DataOrchestrator` para cargar múltiples endpoints en paralelo con:
- Anti-doble-carga (mínimo 3s entre cargas)
- Estados de loading por sección
- Fallback a datos cacheados
- `Promise.allSettled` para tolerancia parcial

**Ver:** `references/orquestacion-carga-pattern.md` para código completo.

---

## 3. Error Boundaries

Patrón de resiliencia:
- Overlay global cuando todo falla (network, 5xx)
- Errores por sección para fallos parciales
- `safeRender()` wrapper para que un error de render no rompa el resto
- Timeout en servidor con `withTimeout()` wrapper
- Clasificación de errores: 404, 502, 503, network, timeout → mensajes distintos

**Ver:** `references/error-boundaries-pattern.md` para código completo.

---

## 4. Tabs con Navegación

Clase `TabController` para:
- Navegación por hash (`#demanda`) con deep-linking
- Lazy-loading de contenido
- Persistencia de última tab en localStorage
- Navegación por teclado (ArrowLeft/ArrowRight)
- Accesibilidad: `role="tab"`, `aria-selected`

**Ver:** `references/tabs-navigation-pattern.md` para código completo.

---

## 5. Persistencia de Estado

Clase `PersistStore` para localStorage con:
- Validación de integridad al leer
- Expiración automática (TTL configurable)
- Control de tamaño (truncar arrays si exceden límite)
- Manejo de `QuotaExceededError`
- Recuperación ante datos corruptos
- Opcional: `HybridStore` con sessionStorage + localStorage

**Ver:** `references/persistence-pattern.md` para código completo.

---

## 6. Manejo de Fechas

Patrones para fechas consistentes:
- **NUNCA usar `new Date('YYYY-MM-DD')`** → se interpreta como UTC
- Usar `new Date(year, month, day)` para fechas locales
- `toLocaleString('es-ES')` para formateo con zona horaria del navegador
- Detección de DST con `Intl.DateTimeFormat().resolvedOptions().timeZone`
- Normalización de inputs de fecha
- **Hora por defecto en `<input type="time">`**: siempre rellenar con la hora actual de la zona horaria del usuario, no dejar vacío:
  ```javascript
  el.value = new Date().toLocaleTimeString('es-ES', { hour:'2-digit', minute:'2-digit', timeZone:'Europe/Madrid', hour12:false });
  ```

**Ver:** `references/dates-timezone-pattern.md` para código completo.

### 6.2 Retroactive Date Entry — Registro en días pasados

Patrón para formularios de registro que permitan al usuario elegir **cualquier fecha**, no solo hoy. Necesario en apps de seguimiento (dieta, fitness, hábitos) donde el usuario puede olvidar registrar un día y necesita retroceder la fecha.

**Implementación resumida (ver reference para código completo):**

1. **HTML** — añadir `<input type="date">` a cada tarjeta de registro, pre-rellenado con `today()` (helper `new Date().toLocaleDateString('sv-SE')`)
2. **Orden UX** — input date va **primero** en el layout (antes del valor), para que el usuario cambie primero el día
3. **JS** — la función de registro lee `inputFecha.value || ''` y lo pasa en el body del fetch
4. **Edición estimada** — añadir también input date en la caja de edición (comida y ejercicio estimados)
5. **Backend** — patrón `fecha || hoy()`: aceptar `fecha` opcional, usarla si viene, fallback a hoy si no
6. **UPSERT** — para tablas con lógica upsert por día (ej: pasos), usar la fecha recibida en el lookup, no `hoy()`

```javascript
// Backend — patrón clave
const { fecha, ... } = req.body;
sql_run('INSERT INTO ... fecha VALUES ?', [req.userId, fecha || hoy(), ...]);

// UPSERT — lookup con la fecha recibida
const f = fecha || hoy();
const existing = sql_get('SELECT id FROM pasos WHERE usuario_id = ? AND fecha = ?', [req.userId, f]);
```

**Pitfalls específicos:**
- El helper `today()` debe estar definido ANTES de construir los HTML templates. Ponerlo al inicio del script.
- `sv-SE` locale es el que entienden los inputs `date` nativos. `toISOString().slice(0,10)` también funciona pero puede tener offset UTC.
- La clave de todo el patrón es el backend con `fecha || hoy()` — sin eso, clientes viejos que no envían `fecha` se rompen.
- Para pasos (UPSERT por día): si no se usa `f` en el `SELECT`, los pasos de ayer se actualizarían sobre los de hoy.

**Ver:** `references/retroactive-date-entry.md` para código completo con todos los formularios, estimaciones editables y server-side.

---

## 7. Sistema de Colores

Patrón de diseño centralizado:
- Variables CSS semánticas (`--color-success`, `--color-danger`)
- Variables de gráfico fijas (`--color-chart-1`...) para consistencia
- Modo oscuro con `[data-theme="dark"]`
- Toggle con localStorage + `prefers-color-scheme` fallback
- Un solo archivo de configuración → cambios globales en un lugar

**Ver:** `references/color-system-pattern.md` para código completo.

---

## 8. Sparklines con Plotly

Mini gráficos inline optimizados:
- Reducir datos a 50 puntos máx. antes de renderizar
- Sin hover, sin ejes, sin leyenda → rendimiento máximo
- `Plotly.purge()` al destruir para liberar memoria
- Color condicional (verde si sube, rojo si baja)
- Punto final destacado con marker más grande

**Ver:** `references/sparklines-pattern.md` para código completo.

---

## 9. Web Workers + Comlink

Cálculos pesados sin bloquear UI:
- Spatial hashing para ray-casting eficiente
- Precomputación + cache
- `Comlink.transfer()` para arrays grandes (ArrayBuffer)
- `visitToken` vs `Set` para evitar allocation por frame
- Batch calculations para terrazas grandes

**Ver:** `references/web-workers-pattern.md` para código completo.

---

### 🔥 REGEX-based removal de bloques de código es INFIABLE

**2026-06-13 (MasterFit dieta):** Intenté eliminar código de dark mode con `re.sub` y un patrón regex que buscaba desde un comentario hasta `})();`. El regex eliminó el botón HTML pero **dejó fragmentos del IIFE abierto** (bloque `try { localStorage.getItem(DARK_MODE_KEY) ... } catch(e) {}`), lo que rompió la ejecución JS. `loadData()` quedó definida pero nunca llamada porque el bloque IIFE abierto cortaba el script.

**Síntomas:**
- HTML carga, CSS aplica, pero `typeof loadData === 'undefined'`
- No hay errores en consola (el parser JS no falla, solo las funciones después del bloque roto no se definen)
- Los datos existen en `database.json` pero no se muestran
- Hero vacío, botones de navegación sin efecto

**Causa:** Los bloques IIFE con `try { ... } catch(e) {}` anidados son difíciles de delimitar con regex. `re.sub(r'from_comment_to_closing', '', content)` deja fragmentos huérfanos que el parser JS ignora pero que cortan la ejecución.

**Fix seguro — 3 pasos:**
1. **Identificar el bloque completo** — buscar el comentario que inicia (`// === DARK MODE TOGGLE ===`) y el cierre (`})();`)
2. **Eliminar con `content[:start] + content[end:]`** — NO usar `re.sub`
3. **Verificar que no queda ningún fragmento** — grep por `DARK_MODE_KEY`, `darkModeToggle`, `toggleDarkMode`, `nz-btn--secondary`, `mf-dark`, `data-nz-theme`

**Regla:** Cuando elimines bloques de código, SIEMPRE verifica que no quedan fragmentos huérfanos. Los fragmentos de JS sueltos son bugs silenciosos: el parser no falla, pero las funciones después del fragmento no se definen.

**Pitfall adicional:** Después de eliminar bloques grandes con `content[:start] + content[end:]`, verificar que el archivo no se truncó. Un archivo HTML de 120KB que queda en 28KB está **truncado** — se perdió todo el JS y la mayor parte del HTML. Siempre verificar `</html>` y `</body>` están presentes.

**Verificación post-fix:**
```python
with open('dashboard.html', 'r') as f:
    content = f.read()
for term in ['darkModeToggle', 'DARK_MODE_KEY', 'toggleDarkMode', 'nz-btn--secondary', 'mf-dark', 'data-nz-theme']:
    if term in content:
        print(f"⚠️ {term} aún presente")
# Verificar integridad del archivo
assert '</html>' in content, "Archivo truncado — falta </html>"
assert '</body>' in content, "Archivo truncado — falta </body>"
assert 'function loadData()' in content, "loadData() eliminada"
assert 'function renderDashboard' in content, "renderDashboard eliminada"
```

---

### 🔥 Hero vacío en primera pantalla — UX crítica

**2026-06-13 (MasterFit dieta):** El hero solo mostraba branding ("MasterFit", "Objetivo: 88 kg", avatar) sin ningún dato ni acción. El usuario dice "no se ve información relevante" — la primera pantalla DEBE mostrar:

1. **Datos reales** — peso actual, kg perdidos, ritmo semanal (o "sin datos" si no hay)
2. **Acciones rápidas** — botones para "Registrar" y "Hablar con IA" (las 2 acciones principales)

**Patrón de hero correcto:**
```html
<section class="nz-hero nz-hero--centered">
  <div class="nz-hero__inner">
    <div class="nz-hero__eyebrow">Dashboard de seguimiento</div>
    <h1 class="nz-hero__title nz-gradient-text">🏋️ MasterFit</h1>
    <p class="nz-hero__sub">Objetivo: <strong>88 kg</strong></p>
    
    <!-- Quick Status con datos reales -->
    <div id="heroQuickStatus">
      <div class="nz-surface nz-surface--glass-soft">
        <div>⚖️ Peso</div>
        <div id="heroPeso">--</div>
      </div>
      <div class="nz-surface nz-surface--glass-soft">
        <div>📉 Perdido</div>
        <div id="heroPerdido">--</div>
      </div>
      <div class="nz-surface nz-surface--glass-soft">
        <div>🔥 Ritmo</div>
        <div id="heroRitmo">--</div>
      </div>
    </div>
    
    <!-- Acciones rápidas -->
    <div class="nz-hero__cta">
      <a class="nz-btn nz-btn--glass-liquid-brand" onclick="switchTab('registrar')">➕ Registrar</a>
      <a class="nz-btn nz-btn--glass-liquid-accent" onclick="switchTab('ia')">🤖 Hablar con IA</a>
    </div>
  </div>
</section>
```

**JS para poblar:** En `renderDashboard()`, después de calcular `pesoActual`, `perdido`, `ritmoResult`:
```javascript
const hPeso = document.getElementById('heroPeso');
const hPerdido = document.getElementById('heroPerdido');
const hRitmo = document.getElementById('heroRitmo');
if (hPeso) hPeso.textContent = pesoActual + ' kg';
if (hPerdido) hPerdido.textContent = '+' + perdido.toFixed(1) + ' kg';
if (hRitmo) hRitmo.textContent = ritmoResult.icon + ' ' + ritmoResult.ritmo.toFixed(1) + '/sem';
```

**Mobile:** En `@media (max-width:768px)`, los quick status deben apilarse verticalmente con `flex-direction: column` y los botones mantener `padding: 10px 16px`.

---

## 10. Debugging Patterns

Patrones de bugs recurrentes en vanilla JS multi-script y HTML inline:
1. **Scope de variables** → `var charts = window.charts = {}`
2. **Tab renderizada antes del fetch lazy** → marcar solo tras fetch exitoso
3. **Esquema de datos incorrecto** → fetch independiente con esquema correcto
4. **Canvas no existe en DOM** → verificar IDs coincidentes
5. **Nombre de función inconsistente** → grep en archivos JS
6. **Botón sin event listener** → verificar que `addEventListener` está vinculado en `DOMContentLoaded` o al final del script
7. **`function` usado como variable** → `function x = null` es SyntaxError que DESTRUYE todo el `<script>` — ni una sola función se define. Síntoma: HTML carga, CSS aplica, pero `typeof loadData === 'undefined'`. Fix: `var x = null`

### 🔥 Página en blanco por paréntesis desbalanceado en `<script>`

**Síntoma:** HTML carga, CSS se aplica, pero la página está completamente en blanco. Sin errores visibles en consola. `typeof window.charts === 'undefined'`.

**Causa:** Un paréntesis de más o de menos en el bloque `<script>` bloquea el parser JS completo. **Ninguna** función se define, `DOMContentLoaded` no se ejecuta.

**Detección rápida con `execute_code`:**
```python
import re
with open('dashboard.html', 'r') as f:
    html = f.read()
match = re.search(r'<script[^>]*>(.*?)</script>\s*</body>', html, re.DOTALL)
script = match.group(1)
opens = script.count('(')
closes = script.count(')')
print(f"Parens diff: {opens - closes}")  # Si != 0 → desbalanceado
```

**Para encontrar la línea exacta:**
```python
balance = 0
for i, line in enumerate(script.split('\n')):
    balance += line.count('(') - line.count(')')
    if balance < 0:
        print(f"Línea {i+1}: balance negativo → {line.strip()}")
        break
```

**Fix común:** En tooltips de Chart.js, concatenar strings con paréntesis dentro:
```javascript
// ❌ MALO — paréntesis de 'kg (' se cierra con el de toFixed
return ctx.label + ': ' + ctx.parsed.toFixed(1) + ' kg (' + ctx.parsed / d.pesoActual * 100).toFixed(1) + '%)';

// ✅ BUENO — calcular en variable separada
var pct = (ctx.parsed / d.pesoActual * 100).toFixed(1);
return ctx.label + ': ' + ctx.parsed.toFixed(1) + ' kg (' + pct + '%)';
```

**Checklist rápido de debugging de página en blanco:**
1. Contar paréntesis `(` y `)` en el script — diff debe ser 0
2. Contar braces `{` y `}` — diff debe ser 0
3. Buscar `var X` duplicado — `.count('var X')` debe ser ≤ 1
4. Comprobar `window.charts` — `browser_console(expression='typeof window.charts')`
5. Verificar canvas en DOM — `browser_console(expression='document.querySelectorAll("canvas").length')`
6. Si todo está bien → verificar que los IDs de elementos existen

**Ver:** `references/debugging-patterns.md` para código completo y ejemplos adicionales.

### 🔥 Fallo CRÍTICO: `apiFetch` NO es un fetch genérico

`apiFetch()` en `public/js/api.js` **requiere obligatoriamente un parámetro `fecha`** (segundo argumento). Construye la URL como `${API_BASE}/${endpoint}?fecha=...`.

**Si necesitas llamar un endpoint que NO usa fecha** (ej: `/api/esios/forecast?days=30`), **NUNCA uses `apiFetch()`** → usa `fetch()` directo:

```javascript
// ❌ MALO — apiFetch añade ?fecha= obligatoriamente → 400 error
const data = await apiFetch('/api/esios/forecast?days=30');

// ✅ BUENO — fetch directo
const resp = await fetch('/api/esios/forecast?days=30');
const data = await resp.json();
```

### 🔥 Strings truncados con *** sin cerrar — causa de "se queda cargando"

Cuando una app web se queda en pantalla de loading eternamente, **primero verifica sintaxis JS**:

**Síntoma:** Loading spinner infinito, nada se renderiza, consola vacía o error de sintaxis no visible.

**Causa común:** URLs con `***` como placeholder de API key que les falta la comilla de cierre. El JS ni siquiera se parsea → `DOMContentLoaded` nunca se ejecuta → init() nunca se llama → loading nunca se oculta.

**Detección rápida con `execute_code`:**
```python
with open('src/js/app.js', 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if 'uri:' in stripped or 'tiles:' in stripped:
        single_quotes = stripped.count("'")
        if single_quotes % 2 != 0:
            print(f"Línea {i}: string sin cerrar ({single_quotes} comillas simples)")
```

**O con `node -c`:**
```bash
node -c src/js/app.js  # Si falla → error de sintaxis
```

**Fix:** Usar concatenación de variables en vez de strings inline:
```javascript
// ❌ MALO — string sin cerrar
uri: 'https://tiles.stadiamaps.com/styles/...?api_key=***\n\n\n// ✅ BUENO — variable ya definida en el archivo
uri: 'https://tiles.stadiamaps.com/styles/...?api_key=' + API_KEY,
```

**Verificación post-fix:** `node -c` debe pasar → `npm run build` debe compilar → servidor debe responder 200.

**Ver:** `references/truncated-js-strings-napmaps.md` para auditoría completa de NapMaps con 12 casos documentados (edificios procedurales, factor de conversión, satélite roto, coordenadas invertidas, etc.).

### 🔥 Quote collision en ternarias con CSS var() — syntax error silenciosa

**2026-06-14 (MasterFit dieta):** Tres líneas en `renderResumen()` tenían `'var(--danger)")` en vez de `'var(--danger)')`. El `"` de cierre del atributo HTML `style="..."` se mezclaba con la comilla de cierre del string JS, creando un syntax error que impedía que el navegador parseara TODO el `<script>` inline.

**Patrón del bug:**
```javascript
// ❌ MALO — " del HTML attribute cierra el string JS prematuramente
'<span style="font-weight:600;color:' + (total >= obj ? 'var(--success)' : 'var(--danger)") + '">' + val + '</span>'
//                                                      ^^^^^^^^^^^^^^ aquí el string se rompe

// ✅ BUENO — ' cierra solo el valor CSS, ) cierra el ternario
'<span style="font-weight:600;color:' + (total >= obj ? 'var(--success)' : 'var(--danger)') + '">' + val + '</span>'
```

**Por qué es silenciosa:** El navegador no puede parsear el `<script>` → NINGUNA función se define → `typeof doLogin === 'undefined'`. Sin errores visibles en consola (el parser falla antes de ejecutar nada).

**Detección:** Buscar patrón regex:
```bash
grep -n "var(--[a-z]\+)\")" dashboard.html  # Comillas rotas
```

**Regla:** En concatenación de strings con ternarias + CSS `var()`, SIEMPRE verificar que la comilla de cierre del string CSS es `'` (simple), no `"` (doble) que podría confundirse con el delimitador del atributo HTML.

---

### 🔥 Extraer `<script>` inline para `node -c` — técnica de debugging

Cuando un HTML con `<script>` inline no carga JavaScript (todas las funciones `undefined`), **extraer el script a un archivo temporal** para verificar sintaxis con `node -c`:

```python
# Extract inline script from HTML
with open('dashboard.html') as f:
    content = f.read()
start = content.index('<script>') + 8  # skip opening tag
end = content.index('</script>', start)
script = content[start:end]
with open('/tmp/test_script.js', 'w') as f:
    f.write(script)
```

```bash
node -c /tmp/test_script.js  # ← SyntaxError con línea exacta
```

**Ventaja sobre verificar braces en el HTML completo:** `node -c` detecta errores de sintaxis REALES (comillas rotas, tokens inesperados), no solo balance de braces/paréntesis. Un HTML puede tener braces balanceados pero un syntax error que impide la carga.

**Checklist actualizado de debugging de página en blanco:**
1. `node -c` del script extraído → error de sintaxis exacto
2. Contar braces `{` y `}` en el script → diff debe ser 0
3. Contar paréntesis `(` y `)` → diff debe ser 0
4. Buscar `var X` duplicado → `.count('var X')` ≤ 1
5. Verificar `window.charts` → `browser_console(expression='typeof window.charts')`
6. Verificar canvas en DOM → `document.querySelectorAll("canvas").length`

---

### 🔥 `</script>` collision — Inyección de JS rompe script tag externo

**2026-06-16 (ContrataPúblico):** Un script de construcción reemplazó `</script>` en el HTML para inyectar JS de features, pero el `</script>` reemplazado era el del `<script src="js/ley-data.js"></script>` tag. El resultado: el browser ve `<script src="js/ley-data.js">` con contenido inline → ignora el `src` y ejecuta el contenido como JS → el archivo externo nunca se carga → `typeof LEY_DATA === 'undefined'`.

**Síntoma:** HTML carga, CSS aplica, pero todas las funciones que dependen del archivo externo son `undefined`. No hay errores en consola (el parser JS ejecuta el contenido inline sin error, pero el archivo externo nunca se solicita).

**Causa raíz:** Los scripts de construcción que buscan `</script>` y reemplazan con contenido JS, sin verificar si ese `</script>` pertenece a un tag `<script src="...">` externo.

**Fix en 2 pasos:**

1. **NUNCA inyectar contenido DENTRO de un `<script src="...">` tag.** Usar un `<script>` inline separado:
   ```html
   <!-- ❌ MALO — rompe la carga del archivo externo -->
   <script src="js/ley-data.js">
       // contenido inyectado aquí NUNCA se ejecuta correctamente
   </script>
   
   <!-- ✅ BUENO — script externo + inline separado -->
   <script src="js/ley-data.js"></script>
   <script>
       // contenido inyectado aquí SÍ se ejecuta
   </script>
   ```

2. **Al inyectar JS, buscar un marcador seguro:** En vez de buscar `</script>`, buscar un comentario específico:
   ```python
   # ✅ Seguro — buscar un marcador que no existe en el contenido inyectado
   marker = '<!-- TYPES_JS_PLACEHOLDER -->'
   html = html.replace(marker, types_js)
   ```

**Detección rápida:**
```python
import re
html = Path("index.html").read_text()
# Buscar <script src="..."> que tenga contenido entre los tags
match = re.search(r'<script src="([^"]*)">([^<]*)</script>', html)
if match and match.group(2).strip():
    print(f"⚠️ TAG EXTERNO CON CONTENIDO INLINE: {match.group(1)}")
    print(f"   Contenido: {match.group(2)[:100]}...")
```

**Regla:** Cuando un script de construcción inyecte JS en un HTML, SIEMPRE usar un `<script>` inline separado, NUNCA inyectar contenido dentro de un `<script src="...">` tag.

---

### 🔥 JSON con strings que contienen saltos de línea → SyntaxError silencioso en JS

**2026-06-16 (ContrataPúblico):** El archivo `js/ley-data.js` contenía 2184 strings de doble comilla con saltos de línea literales (`"texto con\nsaltos"`). En JavaScript, un string de doble comilla `"` NO puede contener saltos de línea literales. El parser JS falla silenciosamente → `typeof LEY_DATA === 'undefined'`.

**Causa:** `JSON.stringify()` o `json.dumps(indent=2)` produce strings con `\n` reales. Al escribir esto en un archivo `.js`, los saltos de línea dentro de strings rompen la sintaxis JS.

**Fix:** Minificar el JSON con `separators=(",",":")` para eliminar todos los espacios y saltos de línea:
```python
# ❌ MALO — produce strings con saltos de línea
json_str = json.dumps(data, indent=2)

# ✅ BUENO — todo en una línea
json_str = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
```

**Verificación:**
```python
import re
js = Path("js/ley-data.js").read_text()
if re.search(r'"[^"\n]*\n[^"\n]*"', js):
    print("❌ JSON tiene strings con saltos de línea — SyntaxError JS")
```

**Ver:** `references/single-file-spa-large-data.md` para el patrón completo de single-file SPA con datos grandes.

---

### 🔥 Fallback data debe ser idéntica al JSON fuente

Cuando un dashboard carga datos de un JSON externo (`fetch('data.json')`) con fallback embebido en el catch, **los datos del fallback deben ser IDÉNTICOS al JSON**. Si no, el usuario ve datos diferentes según la fuente (CORS → fallback, sin CORS → JSON).

```javascript
// ❌ MALO — fallback tiene 2 entradas, JSON tiene 3
.catch(function() {
  var ENTRIES = [ {id: 1}, {id: 2} ];  // ← desactualizado
  render(ENTRIES);
});

// ✅ BUENO — fallback sincronizado con tokens-log.json
.catch(function() {
  var ENTRIES = [ {id: 1}, {id: 2}, {id: 3} ];  // ← idéntico al JSON
  render(ENTRIES);
});
```

**Regla:** Cuando actualices el JSON fuente, actualiza el fallback en el mismo commit.

**Ver:** `references/debugging-patterns.md` para checklist completo y código de detección automatizada.

---

## 11. Aurora Design System

Design System CSS puro sin dependencias, sin build step, namespaced bajo `.nz`. 1 archivo core + 10 packs opt-in. 5 skins de marca. Liquid glass real con OKLCH. CDN público en jsDelivr.

**Repo:** https://github.com/Ntizar/Ntizar-Aurora
**URL:** https://ntizar.github.io/Ntizar-Aurora/

### Quick Start

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@latest/ntizar.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@latest/ntizar.next.css">

<body class="nz"
      data-nz-theme="light"
      data-nz-skin="aurora"
      data-nz-shape="default"
      data-nz-density="comfortable"
      data-nz-motion="standard"
      data-nz-color-system="oklch">
  ...
</body>
```

### Reglas de Oro

1. **Todo lo público vive bajo `.nz`** — no hay clases globales sueltas
2. **Todos los valores son tokens `--nz-*`** — nunca hardcodes un hex o un `16px`
3. **Sin `!important`** fuera de utilidades
4. **BEM** para componentes: `.nz-card__body--featured`
5. **Si no aparece en `gallery.html`, no existe** — la galería es la única fuente de verdad

### Uso con IA Agents (crucial para ahorrar tokens)

**NO** pegar el CSS en el prompt (170 KB ≈ 50.000 tokens).

**SÍ** hacer:
1. Dar al agent solo `AGENTS.md` + `INDEX.md` (~20 KB / ~5.000 tokens)
2. Linkar el CSS vía CDN en el HTML generado
3. Decir al agent: "Generate HTML only. The CSS is already linked. Use Aurora classes from INDEX.md."

### Pitfalls

- **No JS shipped** — modal/tabs/drawer/dropdown/toast son styled, no behaved
- **WCAG AAA** aplica solo a la skin `contrast`, no a todas
- **No tree-shaking** — una página con 5 componentes carga el pack completo

---

## 12. Geodatos Choropleth (Leaflet + Canvas)

Patrón para dashboards geodatos con miles de polígonos. Basado en España Atlas (8.132 municipios).

**Reglas clave:**
- **Canvas renderer** obligatorio para >500 polígonos (`L.canvas()`)
- **TopoJSON** en vez de GeoJSON (~70% menos de tamaño)
- **Hash index** para acceso O(1): `IDX[cod] = {...}`
- **`setStyle()`** para re-colorear sin reconstruir geometría
- **Pane system** para z-index de capas叠加
- **Lazy loading** de datasets temáticos con `ensureDataset()`

**Ver:** `mastermind/espanatlas-architecture` para referencia completa con código, 10 trucos de rendimiento, y patrones de escalabilidad.

### 🔥 Calidad de dashboards geodatos interactivos — Estándares mínimos

**2026-06-18 (AtlasMadrid2024):** La primera versión del dashboard tenía todos los componentes técnicos correctos (mapa, sankey, rankings, KPIs) pero el usuario la rechazó: "no me gusta, no es todo lo bueno que me gustaría". Causas específicas:
- Mapa sin nombres de municipios → "los CP no tienen el nombre"
- Sankey no se veía bien (error silencioso de ciclos bidireccionales)
- Mapa con poca información → solo dots sin contexto

**Estándares mínimos para un dashboard geodatos interactivo:**
1. **Labels en el mapa** — TODOS los municipios/entidades visibles deben tener nombre. Si hay muchos, filtrar por umbral (>5K trabajadores → label grande, resto → label pequeño o solo en hover)
2. **Flujos/arcs en el mapa** — si hay datos OD, mostrar arcos curvados (bezier cuadrático) entre origen y destino. Grosor proporcional al volumen. Transparencia para que no sature
3. **Panel de detalle al click** — click en cualquier entidad → panel lateral con stats completos + top flujos entrantes/salientes con barras de volumen
4. **Hover tooltips** — tooltip rápido al pasar sobre cualquier elemento
5. **Leyenda visible** — colores, tamaños, significado de cada elemento
6. **Controles de capa** — toggle para mostrar/ocultar nombres, flujos, zonas, densidad
7. **Mínimo 4 KPIs** en hero — total, count de entidades, métrica principal, métrica de calidad

**Patrón de mapa interactivo rico (Leaflet):**
```javascript
// Circle markers con tamaño proporcional
const r = Math.max(4, Math.sqrt(c.total / maxTotal) * 22);
const color = c.net > 0 ? '#10b981' : '#ef4444'; // verde=atractor, rojo=exportador
L.circleMarker([c.lat, c.lng], { radius: r, fillColor: color, ... }).addTo(map);

// Labels condicionales (solo para entidades grandes)
if (c.total > 5000) {
  const label = L.divIcon({ html: `<div class="muni-label">${c.name}</div>`, ... });
  L.marker([c.lat, c.lng], { icon: label, interactive: false }).addTo(labelsLayer);
}

// Arcos de flujo curvados (bezier cuadrático)
const midLat = (from.lat + to.lat) / 2;
const ctrlLat = midLat + (to.lng - from.lng) * 0.02; // offset para curva
for (let t = 0; t <= 1; t += 0.05) {
  const lat = (1-t)**2*from.lat + 2*(1-t)*t*ctrlLat + t**2*to.lat;
  points.push([lat, lng]);
}
L.polyline(points, { color: '#2563eb', weight: weight, opacity: 0.4 }).addTo(map);
```

**Regla:** Un mapa con solo dots sin labels, sin flujos, sin panel de detalle es un mapa informativo, no interactivo. El estándar mínimo es: labels + arcs + click-to-detail + hover tooltip + leyenda + controles.

---

## 12b. Heatmap Matrix — Alternativa a Sankey para datos OD bidireccionales

Cuando la matriz origen-destino tiene flujos significativos en AMBAS direcciones (A→B y B→A), un Sankey pierde información porque solo muestra flujos netos. La **matriz heatmap** es mejor alternativa: muestra ambas direcciones simultáneamente.

### Cuándo usar
- Matrices OD donde los flujos bidireccionales son relevantes (ej: Madrid Centro↔Sur = 286K+91K, no solo neto 195K)
- El usuario quiere ver el detalle completo, no solo la dirección dominante
- Número de entidades ≤20 (11 zonas de Madrid → 11×11 = 121 celdas, legible)

### Implementación

```javascript
// Generar matriz 11×11 de flujos bidireccionales
const zonePairs = {};
Object.entries(zoneFlows).forEach(([key, value]) => {
  const [from, to] = key.split('-');
  if (!zonePairs[from]) zonePairs[from] = {};
  if (!zonePairs[to]) zonePairs[to] = {};
  zonePairs[from][to] = (zonePairs[from][to] || 0) + value;
});

// Renderizar con heatmap coloring
const maxFlow = Math.max(...Object.values(zonePairs).flatMap(r => Object.values(r)));
const cells = zones.map(orig =>
  zones.map(dest => {
    const val = (zonePairs[orig] && zonePairs[orig][dest]) || 0;
    const intensity = val / maxFlow;
    const bg = `rgba(37, 99, 235, ${0.08 + intensity * 0.82})`;
    const fg = intensity > 0.5 ? '#fff' : '#1e293b';
    return `<td style="background:${bg};color:${fg};text-align:right">${formatNum(val)}</td>`;
  })
);
```

### Formato de tabla

```html
<table>
  <thead>
    <tr>
      <th>Origen ↓ / Destino →</th>
      <th>Madrid Centro</th><th>Norte</th>...<!-- 11 zonas -->
      <th>Total Salida</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="font-weight:700">Madrid Centro</td>
      <td style="background:rgba(37,99,235,0.08)">723K</td><!-- diagonal: internos -->
      <td style="background:rgba(37,99,235,0.9);color:#fff">286K</td><!-- celda oscura -->
      ...
      <td style="font-weight:700">1.07M</td><!-- totales fila -->
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td style="font-weight:700">Total Llegada</td>
      ...<!-- totales columna -->
    </tr>
  </tfoot>
</table>
```

### Complemento: Top pares bidireccionales
Debajo de la matriz, mostrar ranking de los pares con mayor volumen total (A→B + B→A):
```javascript
const pairs = [];
zones.forEach(a => zones.forEach(b => {
  if (a < b) {
    const ab = zonePairs[a]?.[b] || 0;
    const ba = zonePairs[b]?.[a] || 0;
    pairs.push({ a, b, total: ab + ba, ab, ba });
  }
}));
pairs.sort((x, y) => y.total - x.total);
// Top 15 con barras proporcionales
```

### Pitfalls
- **Diagonal** (A→A) = flujos internos. A menudo es el valor más alto (Madrid: 723K). Mostrar pero no colorear igual que跨区 flows.
- **Celdas vacías** = 0 flujos. Usar fondo muy claro, no dejar vacío.
- **Overflow en móvil** — La matriz 11×11 necesita `overflow-x: auto` en móvil. Considerar scroll horizontal.

---

## 12c. Inclusión de datos externos en visualizaciones geodatos

Cuando el dataset fuente (Excel, CSV, API) contiene entidades fuera del alcance principal (ej: provincias vecinas en un atlas de Madrid), **incluiras como layer separada** en vez de filtrarlas.

### Cuándo aplicar
- Excel con filas "PROVINCIA DE ÁVILA", "PROVINCIA DE GUADALAJARA", "RESTO DE ESPAÑA"
- Datos que cruzan fronteras administrativas del scope principal
- El usuario no pide filtrar — incluir por defecto

### Patrón de implementación

```javascript
// 1. Detectar entradas externas
const externalEntries = Object.keys(zoneFlows).filter(k => {
  const [from, to] = k.split('-');
  return from > '11' || to > '11'; // zonas 12+ son externas
});

// 2. Crear layer separado (dashed border, distinto estilo)
const externalLayer = L.layerGroup();
externalZones.forEach(z => {
  L.circleMarker([z.lat, z.lng], {
    radius: Math.max(8, Math.sqrt(z.total / maxTotal) * 30),
    fillColor: '#7c3aed', // púrpura para distinguir
    fillOpacity: 0.6,
    color: '#7c3aed',
    weight: 2,
    dashArray: '6,4'  // borde dashed
  }).addTo(externalLayer);
});

// 3. Toggle en controles del mapa
const overlays = { '🌐 Prov. Vecinas': externalLayer };
L.control.layers(null, overlays, { collapsed: false }).addTo(map);
```

### Datos a mostrar por entidad externa
- Nombre de la entidad
- Total de trabajadores que se desplazan hacia municipios del scope
- Top 3 municipios destino
- Porcentaje del total del scope

---

## 13. GTFS Browser Parser

Patron para parsear ficheros GTFS comprimidos directamente en el navegador sin servidor: descompresion en memoria, parsing de CSV, logica completa de calendario GTFS y visualizacion de rutas.

**Repo:** https://github.com/Ntizar/nap-dashboard

### Arquitectura

```
Browser
  -> fflate (descompresion ZIP en memoria)
  -> Parser CSV propio
  -> Deteccion de encoding (UTF-8 -> Windows-1252 fallback)
  -> Logica calendario GTFS
  -> Visualizacion (Leaflet + Recharts)
```

### Parsing GTFS

- **Descompresion en memoria** con `fflate` — sin escribir nada en disco
- **Deteccion de encoding** — fallback UTF-8 -> Windows-1252 cuando se detectan caracteres corruptos
- **Tolerancia a ficheros malformados** — cada fila se parsea en try/catch; las filas con errores se cuentan y se notifican
- **Cap de stop_times** — limitado a 100.000 registros para no bloquear el hilo principal
- **Tipos de ruta europeos extendidos** (NeTEx 100-1700): tren de alta velocidad, cercanias, metro, tranvia, funicular, teleférico, ferry

### Logica de Calendario GTFS

1. Comprueba primero `calendar_dates.txt` (excepciones puntuales — tienen prioridad)
2. Si no hay excepcion, consulta `calendar.txt` (dias de la semana + rango de fechas)
3. Si un servicio solo usa `calendar_dates.txt` (sin `calendar.txt`), funciona igualmente

### Pitfalls

- **Ficheros grandes** (>15 MB descomprimidos) pueden tardar varios segundos
- **stop_times masivo** — limitar a 100.000 registros maximo
- **Encoding corrupto** — detectar caracteres U+FFFD y fallback a Windows-1252
- **calendar_dates sin calendar.txt** — algunos feeds usan solo calendar_dates

---

## 14. Three.js 3D Scenes

Patrón para escenas 3D interactivas con texturas procedurales y sistemas de partículas con identidad individual. Basado en ARENA (reloj de arena 3D con granos individuales por país).

### Materiales y texturas

- `MeshPhysicalMaterial` con `clearcoat` para superficies vítreas/mármol
- CanvasTexture para texturas procedurales (mármol, vetas, motas doradas)
- `PointsMaterial` con `vertexColors` para sistemas de partículas coloreadas por país/equipo
- `sizeAttenuation: true` en PointsMaterial para profundidad realista

### Animación y cámara

- Oscilación suave con `Math.sin(elapsed * speed) * range` en rotation.z
- Ease-out-cubic para animaciones de giro/spin: `1 - Math.pow(1 - progress, 3)`
- Mouse parallax suave con lerp en rotation.y y camera.position.y
- `ACESFilmicToneMapping` para iluminación cinematográfica
- `Fog` para profundidad de campo sutil

### Sistema de partículas con identidad individual

Cada partícula (grano) tiene: ID único, país/color, nombre de dueño, estado (settled/floating), velocidad individual.

```javascript
// Estructura de cada partícula
{
  vx: 0, vy: 0, vz: 0,       // velocidad individual
  countryCode: 'ES',           // para lookup de color
  settled: false,              // si ya cayó al fondo
  id: 4521,                    // ID único del backend
  ownerName: 'David',          // nombre del dueño
  highlighted: false,          // para zoom/selección
}

// Colores por país en Float32Array para vertexColors
const sandColors = new Float32Array(MAX_PARTICLES * 3);
// En el loop de animación, actualizar posición + color
sandMesh.geometry.attributes.position.needsUpdate = true;
sandMesh.geometry.attributes.color.needsUpdate = true;
```

### Zoom a partícula individual

```javascript
function zoomToGrain(grainIdx) {
  const i3 = grainIdx * 3;
  const targetX = sandPositions[i3];
  const targetY = sandPositions[i3 + 1];
  const targetZ = sandPositions[i3 + 2] + 3.5; // offset de cámara

  const start = { x: camera.position.x, y: camera.position.y, z: camera.position.z };
  const startTime = Date.now();
  const duration = 800;

  function updateZoom() {
    const progress = Math.min((Date.now() - startTime) / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    camera.position.x = start.x + (targetX - start.x) * ease;
    camera.position.y = start.y + (targetY - start.y) * ease;
    camera.position.z = start.z + (targetZ - start.z) * ease;
    camera.lookAt(sandPositions[i3], sandPositions[i3 + 1], sandPositions[i3 + 2]);
    if (progress < 1) requestAnimationFrame(updateZoom);
  }
  updateZoom();
}
```

### Highlight de partícula

```javascript
// Al hacer zoom, agrandar temporalmente el tamaño de todas las partículas
// (PointsMaterial no permite tamaño individual fácilmente)
sandMesh.material.size = 0.12; // normal es 0.06

// Para highlight visual más fuerte, cambiar el color de esa partícula a blanco
sandColors[i3] = 1.0; sandColors[i3+1] = 1.0; sandColors[i3+2] = 1.0;
sandMesh.geometry.attributes.color.needsUpdate = true;
```

### Raycasting para seleccionar partículas con click

```javascript
container.addEventListener('click', (e) => {
  const rect = container.getBoundingClientRect();
  const mouse = new THREE.Vector2(
    ((e.clientX - rect.left) / rect.width) * 2 - 1,
    -((e.clientY - rect.top) / rect.height) * 2 + 1
  );
  const raycaster = new THREE.Raycaster();
  raycaster.setFromCamera(mouse, camera);

  let closest = null, closestDist = Infinity;
  for (let i = 0; i < particles.length; i++) {
    const i3 = i * 3;
    const sphere = new THREE.Sphere(
      new THREE.Vector3(sandPositions[i3], sandPositions[i3+1], sandPositions[i3+2]),
      0.1  // radio de detección
    );
    if (raycaster.ray.intersectsSphere(sphere)) {
      const dist = camera.position.distanceTo(sphere.center);
      if (dist < closestDist) { closestDist = dist; closest = i; }
    }
  }
  if (closest !== null) showGrainDetail(particles[closest].id);
});
```

### HTML labels flotantes sobre partículas 3D

```javascript
function updateGrainLabelPosition(idx) {
  const label = document.getElementById('grain-label-' + idx);
  if (!label) return;

  const i3 = idx * 3;
  const pos = new THREE.Vector3(sandPositions[i3], sandPositions[i3+1] + 0.15, sandPositions[i3+2]);
  pos.project(camera);

  const container = document.getElementById('hourglass-container');
  const rect = container.getBoundingClientRect();
  label.style.left = ((pos.x * 0.5 + 0.5) * rect.width) + 'px';
  label.style.top = ((-pos.y * 0.5 + 0.5) * rect.height) + 'px';
  label.style.opacity = pos.z < 1 ? '1' : '0'; // ocultar si está detrás
}
```

### WebSocket + Three.js sync en tiempo real

```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  switch (data.type) {
    case 'grain:added':
      addParticle(data.countryCode, data.posY, data.grainId, data.ownerName);
      break;
    case 'grain:settled':
      const idx = particles.findIndex(p => p.id === data.grainId);
      if (idx !== -1) {
        particles[idx].settled = true;
        sandPositions[idx*3] = data.posX;
        sandPositions[idx*3+1] = data.posY;
        sandPositions[idx*3+2] = data.posZ;
        sandMesh.geometry.attributes.position.needsUpdate = true;
      }
      break;
    case 'spin':
      spinHourglass(3000, 4, pushParticlesUp);
      break;
  }
};
```

### Deep linking a partícula específica

```javascript
const params = new URLSearchParams(window.location.search);
const grainParam = params.get('grano');
if (grainParam && /^\d+$/.test(grainParam)) {
  setTimeout(() => {
    const id = parseInt(grainParam);
    fetch(`/api/grains/${id}`).then(r => r.json()).then(data => {
      if (!data.error) {
        addParticle(data.country_code, data.pos_y, id, data.owner_name);
        setTimeout(() => zoomToGrain(findParticleIndex(id)), 500);
      }
    });
  }, 1000);
}
```

### Pitfalls

- **PointsMaterial no tiene tamaño individual** — para highlight, cambiar el size global o usar un mesh separado para la partícula destacada
- **Raycasting con Points** — no hay `intersectsPoints`, usar `intersectsSphere` con un radio por partícula
- **Actualizar `needsUpdate`** — olvidar poner `position.needsUpdate = true` es el error más común; las partículas se quedan quietas
- **No hacer zoom mientras el reloj gira** — flags `isZooming` + `isSpinning` para evitar conflictos de animación
- **Labels HTML se quedan atrás** — actualizar posición en cada frame del animation loop, no solo al hacer zoom
- **Partículas fuera del array** — verificar `particles.length < MAX_PARTICLES` antes de añadir

**Ver:** `references/threejs-grain-visualization.md` para código completo del sistema ARENA v2 (buscador, panel de detalle, feed en vivo, modo espectador).
**Ver:** `references/threejs-lazy-tab-loading.md` para patrón de Three.js lazy-loaded en tab con verificación `typeof THREE` y retry.

---

## 15. Three.js Ocean Gerstner

Patrón para crear un océano 3D realista con ondas Gerstner en Three.js. Basado en WaveThree (visor marino 3D).

### Arquitectura

```
src/ocean/gerstner.js          — Shader de océano (vertex + fragment)
src/scene/setup.js             — Escena Three.js (cielo, niebla, luces)
apps/web-viewer/index.html     — UI glassmorphism
apps/web-viewer/src/main.js    — Orquestación + escenarios + FPS
```

### Vertex Shader — Ondas Gerstner

Cada onda Gerstner desplaza vértices en X/Z (horizontal) y Y (vertical):

```glsl
for (int i = 0; i < WAVE_COUNT; i++) {
    vec2 dir = vec2(cos(angle), sin(angle));
    float x = dot(pos.xz, dir);
    float wave = amp * sin(freq * x + uTime * speed + phase);

    // Gerstner: desplazamiento horizontal para crestas pronunciadas
    float q = amp * freq * 0.75;
    float cosWave = cos(freq * x + uTime * speed + phase);
    pos.x += q * dir.x * cosWave;
    pos.z += q * dir.y * cosWave;
    pos.y += wave;

    // Steepness para espuma
    float steep = q * sin(freq * x + uTime * speed + phase);
    steepness += abs(steep);
}
```

**Reglas clave:**
- **WAVE_COUNT = 10** mínimo para detalle realista (6 es insuficiente)
- **q = amp * freq * 0.75** — coeficiente de steepness (0.75-0.8 para crestas pronunciadas)
- **Cada onda tiene:** angle, freq, amp, speed, phase — 5 floats por onda
- **Normal aproximada:** `norm.x -= dir.x * steep; norm.z -= dir.y * steep`

### Fragment Shader — 5 capas de renderizado

1. **Color base por altura** — 3 tonos (profundo → medio → somero) en vez de 2
2. **Micro-olas procedurales** — 3 sinusoides de alta frecuencia para detalle
3. **Fresnel Schlick** — `F0 = vec3(0.04)` para agua, mezclado con skybox
4. **Specular Blinn-Phong** — doble pico (sharp 256 + soft 32) para reflejos de sol
5. **Espuma procedural** — steepness threshold + peak height + micro-foam texture

```glsl
// Fresnel Schlick
float fresnelSchlick(float cosTheta, vec3 F0) {
    return F0 + (1.0 - F0) * pow(1.0 - cosTheta, 5.0);
}

// Blinn-Phong specular
float blinnPhong(vec3 normal, vec3 viewDir, vec3 lightDir, float shininess) {
    vec3 halfDir = normalize(lightDir + viewDir);
    return pow(max(dot(normal, halfDir), 0.0), shininess);
}

// Espuma: 3 fuentes
float foam = smoothstep(steepThreshold, steepThreshold + 0.3, vSteepness);
foam = max(foam, peakFoam * 0.5);
foam += microFoam * 0.08 * peakFoam;
```

### Skybox simulado (sin imagen)

Usar un `SphereGeometry(200)` con `side: THREE.BackSide` y shader de gradiente:

```glsl
// Fragment shader del cielo
float h = normalize(vWorldPos).y;
vec3 horizon = vec3(0.45, 0.62, 0.78);
vec3 mid = vec3(0.25, 0.45, 0.65);
vec3 zenith = vec3(0.04, 0.08, 0.18);
vec3 col = mix(horizon, mid, pow(h, 0.5));
col = mix(col, zenith, pow(h, 1.5));
// Sol
col += vec3(1.0, 0.9, 0.6) * pow(sunDot, 128.0) * 2.0;
```

### Escenarios predefinidos

Patrón para cargar configuraciones de oleaje predefinidas:

```javascript
const SCENARIOS = {
  temporal: { amplitude: 3.2, frequency: 0.4, speed: 0.5, direction: 245 },
  marfondo: { amplitude: 1.8, frequency: 0.25, speed: 0.3, direction: 270 },
  calma: { amplitude: 0.5, frequency: 0.15, speed: 0.15, direction: 180 },
};
```

**Carga desde JSON:** `fetch('/data/scenarios/file.json').then(r => r.json())` → extraer `wave.hs`, `wave.tp`, `wave.dir`.

### UI — Glassmorphism para overlays 3D

```css
#ui-overlay {
    background: rgba(8, 16, 36, 0.65);
    backdrop-filter: blur(20px) saturate(1.4);
    border: 1px solid rgba(100, 160, 230, 0.15);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255,255,255,0.05);
}
```

**Paleta:** azul marino `#0a1628` + celeste `#38bdf8` + cyan `#22d3ee`.

### FPS Counter

```javascript
let frameCount = 0;
let lastFpsTime = performance.now();
function updateFPS() {
    frameCount++;
    const now = performance.now();
    if (now - lastFpsTime >= 500) {
        const fps = Math.round(frameCount / ((now - lastFpsTime) / 1000));
        fpsValueEl.textContent = fps;
        // Color dinámico: azul ≥50, naranja ≥30, rojo <30
        frameCount = 0; lastFpsTime = now;
    }
}
```

### Camera tracking en shader

El shader necesita la posición de la cámara para calcular viewDir y reflection. Pasar como uniform:

```javascript
// En gerstner.js
uniforms.uCameraPos = { value: new THREE.Vector3(30, 20, 30) };

// En update()
uniforms.uCameraPos.value.copy(camera.position);

// En main.js
ocean.setCameraPos(camera.position);
```

### Pitfalls

- **WAVE_COUNT bajo (≤6)** → oleaje se ve artificial y repetitivo. Mínimo 10.
- **No actualizar uCameraPos** → fresnel y reflection se ven estáticos, sin importar dónde esté la cámara
- **Transparent: true en ShaderMaterial** → el océano se renderiza mal con depth sorting. Usar `transparent: false`.
- **No pasar params nuevos a update()** → los sliders no actualizan el shader. Llamar `ocean.update(t, params)` con params actualizados.
- **Segmentos bajos en PlaneGeometry** → las ondas Gerstner se ven cuadradas. Mínimo 128x128 para una malla de 64x64.
- **Niebla con FogExp2** → el exponente debe ser bajo (0.006-0.01) para niebla marina suave. Fog normal se ve demasiado abrupto.
- **Luz de relleno azul** → simula reflexión del cielo en el agua. Sin ella, el océano se ve plano y artificial.

### Referencia

Ver `references/threejs-ocean-gerstner.md` para código completo del shader y patrones avanzados.
**Ver:** `references/threejs-ocean-gerstner.md` para código completo del shader y patrones avanzados.

---

## D3-Sankey: Ciclos bidireccionales en matrices OD

### 🔥 `circular link` error — flujos bidireccionales en D3 Sankey

**2026-06-18 (AtlasMadrid2024):** d3-sankey (v0.12) lanza `Error: circular link` cuando los datos contienen ciclos A→B y B→A. Esto es **inevitable** en matrices origen-destino reales — casi todas las zonas tienen flujos en ambas direcciones.

**Síntoma:** SVG creado pero con 0 hijos (nada renderizado). Sin error visible en consola hasta que se intenta re-ejecutar manualmente.

**Causa raíz:** d3-sankey exige un grafo acíclico dirigido (DAG). Cualquier par A→B + B→A crea un ciclo → error fatal.

**Fix — flujos netos:**
```javascript
// ANTES (rompe): flujos bidireccionales directos
const flows = Object.entries(zoneFlows)
  .filter(([k]) => k.split('-')[0] !== k.split('-')[1])
  .sort((a,b) => b[1] - a[1]);

// DESPUÉS (funciona): computar flujos netos A→B
const allFlows = Object.entries(zoneFlows).filter(([k]) => k.split('-')[0] !== k.split('-')[1]);
const netFlows = {};
allFlows.forEach(([k, v]) => {
  const [a, b] = k.split('-');
  const key = a < b ? a + '-' + b : b + '-' + a;
  if (!netFlows[key]) netFlows[key] = { a: key.split('-')[0], b: key.split('-')[1], netAB: 0 };
  if (a === netFlows[key].a) netFlows[key].netAB += v; else netFlows[key].netAB -= v;
});
// Solo dirección con mayor peso, filtrando flujos insignificantes
const flows = Object.values(netFlows)
  .map(f => ({ key: f.netAB > 0 ? f.a + '-' + f.b : f.b + '-' + f.a, value: Math.abs(f.netAB) }))
  .filter(f => f.value > UMBRAL)
  .sort((a, b) => b.value - a.value);
```

**Nodos — usar IDs string, no índices numéricos:**
```javascript
// ❌ MALO — nodeId(d => d.index) + links con índices numéricos → conflictos
const nodes = zoneSet.map(z => ({ name: `Z${z}` }));
const links = flows.map(([k,v]) => ({ source: nodeIndex['Z'+a], target: nodeIndex['Z'+b], value: v }));

// ✅ BUENO — nodeId(d => d.id) + links con códigos de zona string
const nodes = Array.from(zoneSet).map(z => ({ id: z, name: `Z${z} ${zonaName(z)}` }));
const links = flows.map(f => {
  const [a, b] = f.key.split('-');
  return { source: a, target: b, value: f.value };
});
const sankey = d3.sankey().nodeId(d => d.id)...
```

**Checklist rápido de debugging Sankey:**
1. ¿El SVG tiene hijos? → `svg.children.length` debe ser > 0
2. ¿Hay ciclos? → verificar que para cada A→B, B→A no existe también
3. ¿Los node IDs son strings consistentes entre nodes y links?
4. ¿`nodeId(d => d.id)` coincide con el campo `id` de los nodos?

**Regla:** Cualquier visualización Sankey con datos de matriz OD REQUIERE pre-procesamiento de flujos netos. Nunca pasar flujos bidireccionales directamente a d3-sankey.

---

### 🔥 SVG con width negativo en tabs lazy-loaded — d3 charts invisibles

**2026-06-18 (AtlasMadrid2024):** El diagrama Sankey se creaba con `container.clientWidth - 30`, pero `clientWidth` es 0 cuando el tab está oculto (display:none). Resultado: SVG con width="-30" → invisible. Sin errores en consola (el SVG existe, tiene hijos, pero es de 0px de ancho).

**Síntoma:** `svg.getAttribute('width')` devuelve "-30" (o cualquier número negativo). SVG creado pero vacío visualmente.

**Fix — mínimo explícito:**
```javascript
// ❌ MALO — clientWidth=0 cuando el tab está oculto
const width = Math.min(container.clientWidth - 30, 1200);

// ✅ BUENO — mínimo garantizado
const width = Math.max(600, Math.min(container.clientWidth - 30, 1200));
```

**Patrón robusto para dibujar en tabs lazy:**
```javascript
function drawInTab(containerId, drawFn) {
  const container = document.getElementById(containerId);
  if (!container) return;
  // Usar requestAnimationFrame para esperar al layout
  requestAnimationFrame(() => {
    const w = Math.max(600, container.clientWidth);
    if (w > 0) drawFn(container, w);
    else {
      // Fallback: retry tras 100ms
      setTimeout(() => {
        const w2 = Math.max(600, container.clientWidth);
        drawFn(container, w2);
      }, 100);
    }
  });
}
```

**Checklist de debugging SVG invisible:**
1. `svg.getAttribute('width')` → debe ser > 0
2. `svg.childElementCount` → debe ser > 0 (si es 0, el problema es el data flow, no el layout)
3. `container.clientWidth` → verificar antes de dibujar
4. Si el tab estaba oculto al dibujar → forzar `invalidateSize()` o redraw

---
**2026-06-11 — MasterFit (dieta-masterfit):** Tab "Progreso" con Three.js lazy-loaded. El CDN de Three.js (`three.min.js`) estaba en el `<head>` pero **no se ejecutaba antes de que `init3DHuman()` intentara usar `THREE.Scene`**. Resultado: panel 3D en blanco, sin errores en consola.

**Causa raíz:** El browser tool de Hermes tiene cache agresivo del HTML. El script CDN puede tardar en cargar, y si `init3DHuman` se llama antes de que Three.js esté disponible, falla silenciosamente.

**Solución en 3 pasos:**

1. **Declarar variables globales arriba** (no dentro de funciones):
   ```javascript
   var _scene3D, _camera3D, _renderer3D, _humanGroup3D;
   var container3D; // global ref for labels
   ```

2. **Asignar el contenedor en `loadProgreso()`** (no al parseo del HTML, porque el div puede no existir):
   ```javascript
   function loadProgreso() {
     _progLoaded = true;
     container3D = document.getElementById('canvas3d');
     fetch('/api/progreso')
       .then(function(data) {
         init3DHuman(data.datos3D);
         renderComposicionChart(data.datos3D);
         // ...
       })
       .catch(function(err) {
         if (container3D) {
           container3D.innerHTML = '<div style="...">Error cargando datos</div>';
         }
       });
   }
   ```

3. **Verificar `typeof THREE` antes de crear la escena** (con retry automático):
   ```javascript
   function init3DHuman(d) {
     var container = document.getElementById('canvas3d');
     if (!container) return;
     
     // Check Three.js is loaded
     if (typeof THREE === 'undefined') {
       container.innerHTML = '<div style="...">Cargando motor 3D...</div>';
       setTimeout(function(){ init3DHuman(d); }, 1000);
       return;
     }
     
     // ... resto de init
   }
   ```

**Debugging:** Si el 3D sigue en blanco:
- `browser_console(expression='typeof THREE')` → debe ser `"object"`, no `"undefined"`
- `browser_console(expression='document.querySelectorAll("script[src]").length')` → debe ser ≥ 2 (Chart.js + Three.js)
- `browser_console(expression='document.getElementById("canvas3d")?.clientWidth')` → debe ser > 0
- Si `THREE` es `undefined` pero el CDN está en el HTML → el browser tool tiene cache → navegar con `?t=<timestamp>` para forzar recarga

**Ver:** `references/threejs-lazy-tab-loading.md` para código completo y checklist de debugging.

### 2. Three.js Ocean Espectral JONSWAP + FFT 2D

**2026-06-17 (WaveThree Fase 3):** Implementación de un océano espectral usando el espectro JONSWAP y FFT 2D en CPU para generar campos de alturas realistas de superficie oceánica.

#### Arquitectura

```
src/ocean/
├── gerstner.js           — Ondas Gerstner (shader vertex/fragment)
├── fft.js                — FFT 2D CPU (Cooley-Tukey radix-2)
├── spectrum.js           — JONSWAP spectrum + angular spread + height field
├── spectral-ocean.js     — Malla Three.js animada con alturas FFT
└── index.js              — Re-exporta todos los submódulos
```

#### FFT 2D en CPU (`fft.js`)

Cooley-Tukey radix-2 butterfly, in-place. Datos complejos como `Float32Array` entrelazado `[r0, i0, r1, i1, ...]`.

- `fft2d(data, N, inverse=false)` — FFT 2D in-place (filas + columnas)
- `fftShift(data, N)` — Desplaza DC al centro
- `ifftShift(data, N)` — Auto-inverso

**Performance:** 128×128 FFT inversa ~19 ms/frame en JS moderno. Viable para 50+ FPS.

#### Espectro JONSWAP (`spectrum.js`)

```
S(f) = α · Hs² · fp⁴ · f⁻⁵ · exp(-1.25·(f/fp)⁻⁴) · γ^exp(-(f-fp)²/(2·σ²·fp²))
α = 0.076 · (g·Tp / 2π)⁻²
σ = 0.07 si f ≤ fp, 0.09 si f > fp
```

**Generación de campo de alturas:**
1. Crear malla de frecuencias 2D (kx, ky)
2. Calcular S(k) = S_f(f) · D(θ) para cada punto
3. Generar números aleatorios gaussianos (Box-Muller) para fase aleatoria
4. Construir campo complejo: A·exp(i·φ) donde A = √(2·S·Δk²)
5. Aplicar fftShift al espectro
6. FFT inversa 2D → campo de alturas en espacio real
7. Normalizar para que Hs = 4σ

#### Malla Three.js (`spectral-ocean.js`)

Interfaz compatible con `gerstner.js`:

```javascript
const ocean = createSpectralOcean({ hs, tp, dir, N: 128, L: 64, windSpeed, windDir });
scene.add(ocean.mesh);
ocean.update(time);
ocean.update(time, newParams);
```

- Regeneración cada ~100ms + interpolación lineal entre frames
- Normals por diferencia finita
- **Smooth clip `tanh(h/3)*3`** para evitar picos extremos

#### Toggle Gerstner ↔ Espectral

```javascript
const state = { oceanMode: 'gerstner' }; // 'gerstner' | 'spectral'
function createOcean(mode) { /* crear según modo */ }
// Toggle: document.getElementById('ocean-mode-toggle').addEventListener('click', ...)
```

#### Validación

| Métrica | Valor |
|---|---|
| Pico del espectro | f = 0.115 Hz (fp = 1/8.7) |
| Hs calculado (4σ) | 3.200 m (0% error) |
| FFT 128×128 | 19.2 ms/frame |

#### Pitfalls

- **`fftShift` vs `ifftShift`:** `ifftShift` es auto-inverso (aplicar dos veces = identidad). No confundir.
- **Hs = 4σ:** La altura significativa es 4× desviación estándar. Si no se normaliza, Hs será incorrecto.
- **Valores extremos:** Campos espectrales tienen colas pesadas. Usar `tanh(h/3)*3` para suavizar.
- **`type: "module"` en package.json:** Necesario para ESM imports. Sin esto, warnings de parsing.
- **No usar WebGPU compute shaders aún:** FFT CPU 128×128 ~19ms/frame, totalmente viable. WebGPU sería complejidad innecesaria por ahora.
- **Regeneración periódica:** No regenerar cada frame. Regenerar cada ~100ms + interpolar.

---

## 16. Three.js Escenarios JSON — Carga de Datos Externos para Escenas

Patrón para cargar configuraciones de escena desde archivos JSON externos, validarlas contra un schema, normalizarlas, y convertirlas a parámetros de un shader Three.js.

### Arquitectura en 3 capas

1. **Validación** — `validateScenario(data)` comprueba campos requeridos y rangos
2. **Normalización** — `normalizeScenario(raw)` añade valores por defecto a campos opcionales
3. **Conversión** — `scenarioToWaveParams(scenario)` mapea campos JSON → parámetros del shader

### Patrón de carga en main.js

```javascript
// 1. Escanear escenarios disponibles
const scenarios = await loadScenariosList();
populateScenarioSelector(scenarios);

// 2. Cargar primer escenario por defecto
await selectScenario(scenarios[0].id);

// 3. Conectar selector
document.getElementById('scenario-select').addEventListener('change', async (e) => {
  await selectScenario(e.target.value);
});
```

### Reglas clave

- **No usar `readdir` en el navegador** — usar lista hardcodeada de IDs conocidos
- **Validar ANTES de normalizar** — si el JSON tiene campos faltantes, la normalización crea `undefined`
- **Error silencioso en lista** — escenarios inválidos se omiten con `console.warn`, no lanzan excepción
- **Siempre pasar params a `ocean.update(t, params)`** — sin params nuevos, el shader no se actualiza

**Ver:** `references/threejs-scenario-loading.md` para código completo con ejemplos de schema, normalización, conversión y mapeo de parámetros.

---

## 17. ESLint v10 Flat Config

**Error real (2026-06-11):** Botón "Registrar Ejercicio" en MasterFit no hacía nada. El frontend llamaba a `/api/deporte` (POST) pero el endpoint en server.js era `/api/entrenamiento`. No había error en consola porque el fetch a un endpoint 404 fallaba silenciosamente (sin `.catch()` visible).

**Síntoma:** Botón visible, formulario relleno, pero nada pasa al pulsar. Sin errores en consola. Sin mensaje de éxito. Formulario no se resetea.

**Debugging:**
1. `search_files` en `server.js` para ver qué endpoints existen (`app.post|app.get|app.put`)
2. `search_files` en `dashboard.html` para ver qué endpoints llama el frontend
3. Comparar: si no coinciden → ese es el bug
4. Probar endpoint directamente con `curl` para verificar que funciona

**Fix:** Alinear nombre del endpoint en frontend con el que existe en backend. Además, añadir `.catch()` visible en todos los fetches para que los errores se muestren en la UI.

**Regla:** Siempre verificar que el endpoint existe en el backend ANTES de asumir que el frontend está roto. La mayoría de "botones que no funcionan" son endpoints inexistentes o mal nombrados.

---

## 15. ESLint v10 Flat Config

ESLint v10+ ignora completamente `.eslintrc.json` (legacy config). Necesita `eslint.config.js` (flat config).

**Causa raíz de errores:** Los 7 errores `no-undef` (`Plotly`, `Vue`, `C`, `SEF`) aparecen porque los globals definidos en `.eslintrc.json` son ignorados por completo.

**Solución — `eslint.config.js`:**
```javascript
import globals from 'globals';
export default [{
    files: ['js/**/*.js', 'tests/**/*.js'],
    languageOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        globals: {
            ...globals.browser,
            ...globals.es2021,
            ...globals.node,
            SEF: 'readonly',
            Vue: 'readonly',
            Plotly: 'readonly',
            C: 'readonly',
        },
    },
    rules: {
        'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
        'no-console': 'off',
        eqeqeq: ['error', 'always'],
        semi: ['error', 'always'],
        quotes: ['error', 'single'],
    },
}, { ignores: ['node_modules/', 'dist/', '*.min.js'] }];
```

**Pitfalls:**
- `no-undef` aparece cuando los globals no están declarados en flat config
- `no-unused-vars` usa `argsIgnorePattern: '^_'` para permitir `_` y `_idx` como args sin uso
- La sección `{ ignores: [...] }` es obligatoria para no lintear node_modules/dist
- `.eslintrc.json` debe eliminarse o renombrarse para evitar confusión

**Ver:** `references/eslint-v10-flat-config.md`

---

## 16. Dashboard de Estado del Sistema (Static Data Bake)

Patrón para crear un HTML estático que muestra el estado de todos los subsistemas de un sistema — ChromaDB, skills, memoria, crons, grafo de conocimiento, SOUL.md. Los datos se generan por un script Python que lee múltiples fuentes (JSON, filesystem, curl) y los "bakea" en el HTML como un objeto `const DATA = {...}`.

**Cuándo usar:**
- Dashboard de salud del sistema (Mastermind, agente, infraestructura)
- Panel de control que se actualiza periódicamente vía cron
- HTML estático autocontenido sin necesidad de servidor backend

**Cuándo NO usar:**
- Los datos necesitan actualización en tiempo real → usar API REST
- Hay demasiadas fuentes → considerar un backend que agregue

**Arquitectura:**
```
Múltiples fuentes (JSON, filesystem, curl)
  → generate-dashboard.py (recopila datos)
  → mastermind-status.html (const DATA = {...})
  → Navegador (renderizado estático)
```

**Estructura del generador Python:**
```python
def get_<component>_status():
    """Leer estado de un componente específico."""
    try:
        # ... lectura
        return {"status": "ok", "detail": "..."}
    except Exception:
        return {"status": "error", "detail": "unknown"}

def update_dashboard():
    data = {
        "chromadb": get_chromadb_status(),
        "skills": get_skills_stats(),
    }
    html = re.sub(r'const DATA = \{.*?\};', f"const DATA = {json.dumps(data)}", html, flags=re.DOTALL)
    Path(DASHBOARD_HTML).write_text(html, encoding="utf-8")
```

**Reglas clave:**
- Cada componente tiene un dict con campos estables → el HTML siempre funciona
- Fallbacks siempre retornan valores válidos (no None, no undefined)
- El HTML es autocontenido — no necesita servidor, solo abrir en navegador
- Los datos se bakean en el HTML → no hay llamadas AJAX en runtime
- Para actualizar: ejecutar el script Python (vía cron, CLI, o manualmente)

**Referencia:** `/hermes-home/scripts/generate-dashboard.py` y `/root/workspace/Mastermind/dashboard/mastermind-status.html`

---

## 17. Vite HTML Script Processing

Vite **solo transforma scripts que son ES modules** (`type="module"` o `.mjs`). Scripts de página (IIFEs sin `type="module"`) se ignoran completamente → no se transforman → no se hashan → **404 en el deploy**.

### Patrón A — Rutas relativas vs absolutas (scripts ES modules)

Si los scripts son ES modules, Vite los transforma a `/assets/hash.js`. Solo necesita rutas absolutas:

```diff
- <script type="module" src="js/app.js"></script>
+ <script type="module" src="/js/app.js"></script>
```

### Patrón B — Scripts de página (IIFEs, sin type="module")

**Problema:** Vite **no transforma** scripts `<script src="/js/app.js">` aunque tengan ruta absoluta. Los scripts IIFE no son ES modules, así que Vite los ignora.

**Síntoma:**
- HTML desplegado muestra `{{ }}` sin procesar (Vue no carga)
- `dist/` no contiene los archivos JS
- `curl /js/app.js` → 404

**Solución — Post-build script (`postbuild.js`):**

1. Copia los scripts JS/CSS a `dist/js/` y `dist/css/`
2. Transforma las referencias en el HTML (`/js/` → `js/`)
3. Se ejecuta tras `vite build`

```javascript
// postbuild.js
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const distDir = path.join(__dirname, 'dist');
const srcJsDir = path.join(__dirname, 'js');
const srcCssDir = path.join(__dirname, 'css');

const htmlPath = path.join(distDir, 'index.html');
let html = fs.readFileSync(htmlPath, 'utf-8');

const jsFiles = ['app.js', 'simulator.js', 'charts.js', /* ... */];
fs.mkdirSync(path.join(distDir, 'js'), { recursive: true });
for (const js of jsFiles) {
    const src = path.join(srcJsDir, js);
    if (fs.existsSync(src)) fs.copyFileSync(src, path.join(distDir, 'js', js));
}

fs.mkdirSync(path.join(distDir, 'css'), { recursive: true });
const cssFiles = ['app.css', 'ntizar.css'];
for (const css of cssFiles) {
    const src = path.join(srcCssDir, css);
    if (fs.existsSync(src)) fs.copyFileSync(src, path.join(distDir, 'css', css));
}

// Transformar referencias: /js/ → js/ (sin barra leading)
html = html.replace(/src="\/js\//g, 'src="js/');
html = html.replace(/href="\/css\//g, 'href="css/');
fs.writeFileSync(htmlPath, html);
```

En `package.json`:
```json
{
  "scripts": {
    "build": "vite build && node postbuild.js"
  }
}
```

### Patrón D — `rollupOptions.input` + post-build (alternativa)

Si quieres que Vite **incluya** los scripts en el build (para que aparezcan en el `dist/`), puedes añadirlos a `rollupOptions.input` en `vite.config.js`:

```javascript
export default defineConfig({
    build: {
        outDir: 'dist',
        emptyOutDir: true,
        rollupOptions: {
            input: [
                'index.html',
                'js/constants.js', 'js/theme.js', 'js/app.js',
                // ... todos los scripts
            ],
        },
    },
});
```

**Nota:** Esto **no transforma** los scripts IIFE (siguen siendo IIFEs), pero Vite los incluye en el `dist/` como assets con hash. Combinado con el post-build script para transformar referencias, es la solución más robusta.

### Patrón E — Dockerfile + scripts originales

Si usas un Dockerfile que copia todo el repo (`COPY . .`), los scripts `js/` y `css/` ya existen en el contenedor. Solo necesitas que el HTML tenga las rutas correctas.

**Solución:** El HTML del repo puede tener rutas relativas (`src="js/..."`) directamente — el Dockerfile los servirá correctamente. No se necesita Vite para nada.

**Pitfalls:**
- `rollupOptions.input` **NO transforma** scripts IIFE — solo los incluye como assets
- `transformIndexHtml` en plugins personalizados **NO funciona** como handler nativo de Vite
- El post-build script es **la solución más práctica** para proyectos con scripts legacy
- GitHub Pages sirve `dist/` → si los scripts no están en `dist/js/`, dan 404
- NaN.builders sirve el `dist/` del build → mismo problema
- **CRÍTICO:** El HTML del repo debe tener rutas absolutas (`/js/...`) para que Vite al menos las reconozca. El post-build las convierte a relativas (`js/...`) para que funcionen en el deploy.
- **Solo aplica a `index.html` en la raíz del proyecto.** Scripts cargados dinámicamente con `createElement('script')` no se ven afectados.
- **No confundir con CDN scripts.** Los scripts CDN (`https://cdn...`) no necesitan transformación.
- **CSS también aplica.** `<link href="css/app.css">` tampoco se transforma sin la barra.

### Patrón C — Convertir a ES modules (solución elegante)

Si es posible, convertir los IIFEs a ES modules con `export` y usar `type="module"` en el HTML. Vite los transforma automáticamente.

**Pitfalls:**
- `rollupOptions.input` NO funciona para scripts IIFE — Vite no los procesa como assets
- `transformIndexHtml` en plugins personalizados NO funciona como handler nativo
- El post-build script es la solución más práctica para proyectos con scripts legacy
- GitHub Pages sirve `dist/` → si los scripts no están en `dist/js/`, dan 404
- NaN.builders sirve el `dist/` del build → mismo problema
- **CRÍTICO:** El HTML del repo debe tener rutas absolutas (`/js/...`) para que Vite al menos las reconozca. El post-build las convierte a relativas (`js/...`) para que funcionen en el deploy.

**Ver:** `scripts/vite-postbuild.js` para un script reutilizable (actualizar lista de archivos por proyecto).
**Ver:** `references/vite-html-script-processing.md` para diagnóstico completo.
**Ver:** `references/iterative-improvement-workflow.md` para el flujo sistemático de mejora iterativa de proyectos web (análisis → identificar mejora → implementar → verificar → commit).

---

## 18. Full-Stack SPA Audit Pattern

Patrón para auditar aplicaciones SPA con **backend + frontend** (Express + vanilla JS + Docker + data layer). No confundir con `single-page-app-audit` (un solo HTML sin servidor) ni `audit-html-project` (proyectos HTML educativos).

### Cuándo usar

- El usuario dice "audita mi proyecto" o "esto no funciona" en una SPA con servidor
- Proyecto con `server.js` + `dashboard.html` + `data/` + `Dockerfile`
- Botones/features que no funcionan sin errores visibles en consola
- Problemas de responsive reportados solo en ciertas secciones

### Procedimiento

#### 1. Exploración inicial

```bash
# Identificar repos y rama activa
ls -la /root/workspace/ | grep -E 'dieta|proyecto|app'
git log --oneline -10  # ¿Cuál es la versión activa?
```

#### 2. Frontend ↔ Backend cross-reference (PATRÓN CLAVE)

El bug más común en SPA con servidor: **el frontend llama a un endpoint que no existe en el backend** o lo llama con el nombre incorrecto. No hay error en consola porque los fetchs sin `.catch()` fallan silenciosamente.

```bash
# Endpoints que existen en el backend
grep -n "app\.\(post\|get\|put\|delete\)" server.js | grep -oP "'/[^']+'"

# Endpoints que llama el frontend
grep -n "fetch\|axios" dashboard.html | grep -oP "'/[^']+'|`/[^`]+`"
```

**Comparar ambas listas.** Si no coinciden, ese es el bug.

**Problemas clásicos de naming:**
- Frontend usa `'deporte'` pero backend espera `'entrenamientos'`
- Frontend usa `'comidas'` pero backend espera `'comida'`
- El tipo pasado a `borrarRegistro(tipo, idx)` debe coincidir con `allowedTypes` en el servidor

#### 3. indexOf con arrays invertidos (bug silencioso)

```javascript
// ❌ MALO — indexOf busca en el array ORIGINAL, pero d viene del array INVERTIDO
deporte.slice().reverse().forEach(function(d){
  var realIdx = deporte.indexOf(d);  // ← Si hay duplicados, devuelve el PRIMERO, no el correcto
});

// ✅ BUENO — construir el índice real al generar el HTML
deporte.forEach(function(d, i){
  template = template.replace('${IDX}', i);  // índice real como data-attr
});
```

**Verificar en:** `renderDeporteList()`, `renderComidasList()`, y cualquier función que invierta el array antes de iterar.

#### 4. Responsive: auditar TODAS las tabs (no solo la primera)

El error más común: solo se añaden media queries para las tabs visibles inicialmente, ignorando tabs lazy-loaded como "Progreso".

```bash
# Buscar grids sin cobertura responsive
grep -n 'grid-template-columns' dashboard.html

# Buscar heights fijos que desbordan en móvil
grep -n 'height:[0-9]\+px' dashboard.html

# Verificar que los media queries cubren TODOS los grids
grep -n '@media' dashboard.html
grep -n 'max-width:768' dashboard.html
```

**Qué auditar en cada tab:**
- Grids `1fr 1fr` o `repeat(N, 1fr)` con N>2 → deben tener breakpoint a `1fr`
- `heights` fijos en contenedores canvas/3D → `height: 350px` en móvil
- Labels posicionadas con `position:absolute` y porcentajes fijos → revisar en viewports pequeños
- Tabs row con `flex-wrap:wrap` que no se ve → `overflow-x:auto` con scroll en móvil

#### 5. Verificar todos los fetchs tienen .catch() visible

```bash
# Fetch sin catch
grep -n 'fetch(' dashboard.html | grep -v '.catch'
```

Cada fetch debe tener un `.catch()` que muestre el error en la UI, no solo `console.error`.

#### 6. Docker + Infra

```bash
# Verificar EXPOSE coincide con process.env.PORT
cat Dockerfile | grep EXPOSE
cat server.js | head -10 | grep PORT

# Verificar HEALTHCHECK apunta al puerto correcto
cat Dockerfile | grep HEALTHCHECK

# Verificar que no hay secrets en .env
cat .env | head -5
```

### Formato de salida

```markdown
# 🔍 AUDITORÍA — [Nombre del Proyecto]

**Stack:** Express + vanilla JS + [librerías]
**Puerto:** [N]

---

## 🐛 BUGS CRÍTICOS

### 1. [Título]
**Causa raíz:** [Descripción clara]
**Dónde:** [Archivo:línea]
**Solución:** [Cómo arreglarlo]

---

## 🐛 BUGS IMPORTANTES

### 2. [Título]
...

---

## 💡 MEJORAS

| # | Mejora | Prioridad | Dificultad |
|---|--------|-----------|------------|
| 1 | [Mejora] | 🔴 Alta | Fácil |

---

## ✅ LO QUE FUNCIONA BIEN
- [Puntos fuertes del proyecto]

---

## 🛠️ Prioridad
1. **🔴 [Bug 1]** — [Acción]
2. **🔴 [Bug 2]** — [Acción]
...
```

### Reglas

- **Siempre verificar endpoints antes de asumir que el frontend está roto** — la mayoría de "botones que no funcionan" son endpoints mal nombrados
- **indexOf con arrays invertidos es el segundo bug más común** — el índice no corresponde al elemento correcto
- **No asumir que un media query cubre todas las tabs** — verificar explícitamente cada `tab-*`
- **Terminar con "¿Qué te parece? ¿Empezamos con los bugs críticos?"** — el usuario quiere decidir prioridad. **SI el usuario responde "Arregla todo" / "Fix everything" → implementar TODOS los bugs en orden de prioridad SIN re-preguntar**
- **Si hay 3+ bugs, presentarlos en tabla resumen antes del detalle** para que el usuario pueda priorizar
- **Preferencia de usuario detectada: acción sobre discusión** — si el usuario escribe frases cortas e imperativas ("Arregla todo", "Hazlo", "Vale"), asumir ejecución directa sin pausas para aprobación. Solo preguntar si hay ambigüedad real en el enfoque

### Pitfalls

- **🔴 No confundir con single-page-app-audit:** Este skill es para SPA con servidor Node.js + data layer. Si es un solo HTML autónomo sin servidor, usar el otro.
- **🔴 No confundir con audit-html-project:** Ese skill es para proyectos HTML educativos multi-página (10+ archivos). Este es para dashboards SPA con backend.
- **🔴 El browser tool puede mentir:** Si el HTML tiene `?t=<timestamp>` y el browser tool devuelve cached version, los cambios no se ven. Usar `curl` para verificar el HTML real del servidor.
- **🔴 Los fetchs sin `.catch()` son bugs silenciosos** — el usuario nunca sabe que falló. Priorizar añadirlos sobre features nuevas.

**Referencia:** `references/masterfit-fullstack-audit.md` — auditoría completa de MasterFit v3 con bugs reales, lecciones y soluciones paso a paso.

---

## 18. Toast Notifications (Feedback UX)

Sistema de notificaciones toast flotantes para feedback de acciones del usuario. Reemplaza badges inline por toasts con queue, animaciones y auto-dismiss.

### Cuándo usar
- Feedback tras acciones del usuario (crear/editar/borrar registros)
- Mensajes de error de conexión o API
- Confirmaciones de éxito
- Info contextual (editando registro, cargando datos)

### Implementación

**1. HTML — Contenedor:**
```html
<div class="mf-toast-container" id="toastContainer"></div>
```

**2. CSS (añadir en `<style>`):**
```css
.mf-toast-container { position:fixed;top:20px;right:20px;z-index:99999;display:flex;flex-direction:column;gap:8px;pointer-events:none;max-width:380px; }
.mf-toast { pointer-events:auto;display:flex;align-items:flex-start;gap:10px;padding:12px 16px;border-radius:12px;background:rgba(255,255,255,0.95);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,0.6);box-shadow:0 8px 32px rgba(0,0,0,0.12);font-size:0.85rem;color:#1e293b;animation:mfToastIn 0.35s cubic-bezier(0.22,1,0.36,1) forwards; }
.mf-toast--success { border-left:4px solid #22c55e; }
.mf-toast--error { border-left:4px solid #ef4444; }
.mf-toast--info { border-left:4px solid #2563eb; }
.mf-toast--warning { border-left:4px solid #f97316; }
.mf-toast--removing { animation:mfToastOut 0.3s cubic-bezier(0.55,0,1,0.45) forwards; }
.mf-toast__icon { font-size:1.2rem;flex-shrink:0;margin-top:1px; }
.mf-toast__content { flex:1; }
.mf-toast__title { font-weight:700;font-size:0.85rem;margin-bottom:2px; }
.mf-toast__message { font-size:0.8rem;color:#64748b;line-height:1.4; }
.mf-toast__close { background:none;border:none;cursor:pointer;font-size:1rem;color:#94a3b8;padding:0 2px;flex-shrink:0;opacity:0.6;transition:opacity 0.2s; }
.mf-toast__close:hover { opacity:1; }
.mf-toast__progress { position:absolute;bottom:0;left:0;height:3px;border-radius:0 0 12px 0;background:linear-gradient(90deg,#2563eb,#f97316);animation:mfToastProgress 4s linear forwards; }
@keyframes mfToastIn { from { opacity:0;transform:translateX(80px) scale(0.9); } to { opacity:1;transform:translateX(0) scale(1); } }
@keyframes mfToastOut { from { opacity:1;transform:translateX(0) scale(1); } to { opacity:0;transform:translateX(80px) scale(0.9); } }
@keyframes mfToastProgress { from { width:100%; } to { width:0%; } }
@media (max-width:480px) { .mf-toast-container { top:10px;right:10px;left:10px;max-width:none; } .mf-toast { max-width:none;font-size:0.8rem; } }
```

**3. JavaScript (añadir antes de lógica principal):**
```javascript
var _toastQueue = [];
var _toastActive = false;
var TOAST_DURATION = 4000;

function showToast(title, message, type, duration) {
  type = type || 'success';
  duration = duration || TOAST_DURATION;
  var icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  var icon = icons[type] || icons.info;
  var container = document.getElementById('toastContainer');
  if (!container) return;
  _toastQueue.push({ title: title, message: message, type: type, icon: icon, duration: duration });
  if (_toastActive) return;
  _showNextToast();
}

function _showNextToast() {
  if (_toastQueue.length === 0) { _toastActive = false; return; }
  _toastActive = true;
  var toastData = _toastQueue.shift();
  var container = document.getElementById('toastContainer');
  if (!container) return;
  var toast = document.createElement('div');
  toast.className = 'mf-toast mf-toast--' + toastData.type;
  toast.innerHTML =
    '<span class="mf-toast__icon">' + toastData.icon + '</span>' +
    '<div class="mf-toast__content">' +
      '<div class="mf-toast__title">' + toastData.title + '</div>' +
      (toastData.message ? '<div class="mf-toast__message">' + toastData.message + '</div>' : '') +
    '</div>' +
    '<button class="mf-toast__close" onclick="this.parentElement.classList.add(\'mf-toast--removing\');setTimeout(function(){this.parentElement.remove();_showNextToast();},300)">✕</button>' +
    '<div class="mf-toast__progress" style="animation-duration:' + toastData.duration + 'ms"></div>';
  container.appendChild(toast);
  setTimeout(function() {
    if (toast.parentElement) {
      toast.classList.add('mf-toast--removing');
      setTimeout(function() {
        if (toast.parentElement) toast.remove();
        _showNextToast();
      }, 300);
    }
  }, toastData.duration);
}
```

### Uso

```javascript
// Éxito
showToast('Peso registrado', '97.2 kg para hoy', 'success');

// Error
showToast('Error', 'No se pudo conectar', 'error');

// Info
showToast('Editando registro', 'Comida de 2026-06-11 14:00', 'info');

// Warning
showToast('Registro eliminado', 'Comida borrada', 'warning');

// Duración personalizada (6 segundos)
showToast('Procesando...', 'Esto puede tardar un poco', 'info', 6000);
```

### Reglas
- **NUNCA usar `alert()`** — siempre toast o badge inline si el toast no es posible
- **NUNCA usar `console.log` como feedback visible** — el usuario no ve la consola
- **Reemplazar todos los `document.getElementById('xxxMsg').innerHTML = '<span class="nz-badge">...'`** por `showToast()`
- **Los toasts se encadenan** — no hay límite, se muestran secuencialmente
- **Siempre añadir `.catch()` a cada `fetch()`** con `showToast('Error', msg, 'error')`

### Pitfalls
- **El contenedor debe existir antes de llamar `showToast()`** — ponerlo fuera del contenido dinámico
- **No llamar `showToast()` antes de que el DOM esté listo** — verificar `document.getElementById('toastContainer')`
- **No usar `alert()`** — rompe la UX y no es responsive. Siempre toast.
- **No mezclar badges inline Y toasts** — elegir uno. Los toasts son superiores para UX.

**Ver:** `references/toast-notifications-pattern.md` para código completo y variantes.

---

## 19. CSV Export Pattern

Patrón para exportar datos de una app web a formato CSV descargable. Incluye backend endpoint con escape correcto, BOM UTF-8 para Excel, y frontend modal con selección por tipo.

### Backend endpoint

```javascript
app.get('/api/export/csv', (req, res) => {
  const db = readDB();
  const { tipo } = req.query; // 'all', 'peso', 'comidas', 'entrenamientos', 'pasos', 'agua', 'inbody'

  const escapeCSV = (val) => {
    const s = String(val == null ? '' : val);
    if (s.includes(',') || s.includes('"') || s.includes('\n') || s.includes('\r')) {
      return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
  };

  const toCSV = (headers, rows) => {
    const lines = [headers.join(',')];
    for (const row of rows) {
      lines.push(row.map(escapeCSV).join(','));
    }
    return lines.join('\n');
  };

  // ... generar CSV según tipo ...

  res.setHeader('Content-Type', 'text/csv; charset=utf-8');
  res.setHeader('Content-Disposition', 'attachment; filename="masterfit-export.csv"');
  res.send('\uFEFF' + csv); // BOM para Excel
});
```

**Reglas clave:**
- **BOM UTF-8** (`\uFEFF`) es OBLIGATORIO para que Excel reconozca tildes, ñ, acentos
- **Escape de comas** — si el campo contiene `,`, `"`, o saltos de línea → envolver en comillas y duplicar comillas internas
- **Headers descriptivos** — siempre primera fila con nombres de columna
- **Filename descriptivo** — incluir tipo y fecha para que sea identificable

### Frontend modal

```html
<div id="exportModal" style="display:none;position:fixed;inset:0;z-index:100000;background:rgba(0,0,0,0.5);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);align-items:center;justify-content:center;">
  <div style="background:rgba(255,255,255,0.95);backdrop-filter:blur(16px);border-radius:16px;padding:24px;max-width:480px;width:90%;">
    <h3>📥 Exportar Datos a CSV</h3>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
      <button onclick="downloadCSV('all')">📋 Todo</button>
      <button onclick="downloadCSV('peso')">⚖️ Peso</button>
      <!-- más botones -->
    </div>
  </div>
</div>
```

### JS para descargar

```javascript
function downloadCSV(tipo) {
  showToast('Exportando...', 'Preparando CSV', 'info');
  const a = document.createElement('a');
  a.href = '/api/export/csv?tipo=' + encodeURIComponent(tipo);
  a.download = ''; // Server setea el filename
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => {
    showToast('¡Exportado!', 'CSV descargado', 'success');
    closeExportModal();
  }, 800);
}
```

### Cuándo usar
- El usuario quiere analizar sus datos externamente (Excel, Google Sheets, Numbers)
- Compartir datos con un profesional (nutricionista, entrenador, médico)
- Backup de datos antes de un cambio importante
- Migración a otra herramienta

### Pitfalls
- **Sin BOM → Excel no muestra tildes** — siempre añadir `\uFEFF` al inicio
- **Campos con comas** — si no se escapan, el CSV se rompe (columnas desplazadas)
- **No usar `fetch()` para descarga** — `fetch` no dispara descargas de archivos. Usar `<a>` element o `window.location.href`.
- **Modal backdrop click** — añadir listener para cerrar con click fuera del modal
- **Escape key** — añadir listener para cerrar con Escape

**Ver:** `references/csv-export-pattern.md` para código completo y variantes.

---

## 20. Data Integrity & Graceful Degradation

Patrón para dashboards que muestran datos **reales** incluso cuando las fuentes fallan. **NUNCA inventar datos** — un dashboard con datos falsos es peor que uno con secciones vacías.

### Regla de Oro

**NUNCA generar datos sintéticos para rellenar secciones vacías.** Si no hay datos reales, mostrar un empty state honesto. El usuario prefiere ver "Sin actividad reciente" a una lista de eventos inventados.

```javascript
// ❌ MALO — inventar actividad cuando no hay datos
if (agentLog.length === 0) {
  agentLog = patterns.slice(0, 5).map((p, i) => ({
    from: 'mastermind', to: 'planner',
    action: 'Delegó planificación',
    time: new Date(Date.now() - i * 120000).toLocaleTimeString()
  }));
}

// ✅ BUENO — empty state honesto
if (agentLog.length === 0) {
  return res.json({ agents: [...], activity: [], patterns: [...] });
}
```

### Fallback Chains (nunca datos falsos)

Cuando una fuente de datos no está disponible, la cadena de fallback debe terminar en un **empty state honesto**, no en datos inventados:

```
Fuente primaria → Fuente secundaria → Empty state honesto
```

Ejemplo para procesos en contenedores:
```
ps aux → /proc → info del ecosistema (con PID '-' indicando que no es local) → [{ pid: 1, command: 'node server.js' }]
```

Ejemplo para skills:
```
ChromaDB → filesystem → categorías conocidas del ecosistema → { status: 'no_disponible', count: 0 }
```

### Empty States Honestos

Cada sección del dashboard debe tener un empty state que explique POR QUÉ no hay datos:

| Situación | Empty State |
|---|---|
| Sin actividad de agentes | "Esperando actividad... Los agentes se comunican aquí cuando hay tareas en curso" |
| Sin procesos visibles | "Solo el proceso actual visible (contenedor restringido)" |
| Sin crons configurados | "No hay cron jobs configurados en este entorno" |
| ChromaDB no accesible | "ChromaDB no accesible desde este contenedor — corre en la VM local" |

### Limitaciones de Contenedores (NaN.builders)

Los contenedores en NaN.builders tienen restricciones que afectan qué datos se pueden obtener:

| Comando/API | Disponible en contenedor | Alternativa |
|---|---|---|
| `ps aux` | ❌ Solo ve su propio proceso | `/proc` fallback, o info del ecosistema |
| `/proc/[pid]/cmdline` | ⚠️ Solo PID 1 (el propio proceso) | Info estática del ecosistema |
| `chromadb` (localhost:8000) | ❌ ChromaDB corre en VM local | Filesystem fallback, o categorías conocidas |
| `/hermes-home/skills` | ❌ No existe en contenedor | Categorías conocidas del ecosistema |
| `crontab -l` | ❌ No hay cron en contenedor | Array vacío |
| `df -h` | ⚠️ Muestra solo el contenedor | Usar `os.freemem()` de Node.js |
| `free -m` | ⚠️ Muestra solo el contenedor | Usar `os.totalmem()` de Node.js |

### Info del Ecosistema (fallback final para procesos)

Cuando no se pueden leer procesos reales, mostrar una lista estática de los servicios conocidos del ecosistema, marcando claramente que son referencias (PID '-'):

```javascript
res.json([
  { user: 'appuser', pid: 1, cpu: '0.0', mem: '0.0', command: 'node server.js (Dashboard)', isNode: true },
  { user: 'system', pid: '-', cpu: '-', mem: '-', command: 'Hermes Agent (VM local)', isHermes: true },
  { user: 'system', pid: '-', cpu: '-', mem: '-', command: 'ChromaDB (VM local)', isHermes: true },
]);
```

### Categorías Conocidas (fallback final para skills)

Cuando no se puede acceder a ChromaDB ni al filesystem, mostrar las categorías del ecosistema como tags informativos:

```javascript
const knownCats = ['mastermind', 'devops', 'esios', 'frontend', 'data-science', 'mlops', 'testing', 'github', 'creative', 'ia'];
```

### Verificación de Integridad

Antes de desplegar un dashboard, verificar:

1. **Sin datos de prueba:** `grep -r 'patterns.slice' server.js` → no debe haber generación de datos falsos
2. **Empty states:** Cada sección tiene un mensaje cuando no hay datos
3. **Fallback termina en vacío:** La última opción de cada cadena es un array vacío o un mensaje informativo
4. **Contenedor test:** Probar que el dashboard funciona en el contenedor real (no solo en local)

### 🔥 NaN Container Data Isolation — El endpoint que devuelve vacío

**2026-06-11:** Se creó un endpoint `/api/hermes-system` en el dashboard de NaN que intentaba leer archivos de Hermes (`/hermes-home/cron/jobs.json`, `/hermes-home/skills/`, `/hermes-home/sessions/`, `/hermes-home/logs/`). El endpoint devolvió arrays vacíos porque **el contenedor NaN no tiene acceso al filesystem de la microVM**.

**Causa raíz:** Los contenedores NaN están aislados. No pueden acceder a `/hermes-home/`, que vive en la microVM host.

**Regla:** Si un dashboard desplegado en NaN necesita datos de Hermes:
1. **No intentar leer archivos de `/hermes-home/`** desde el contenedor — no funcionará
2. **Opción A:** Crear un dashboard LOCAL en la microVM (puerto 6060) con acceso directo a todo
3. **Opción B:** Exponer un API proxy en la microVM que sirva los datos, y que el dashboard de NaN haga fetch a ese proxy (requiere CORS y networking entre host→contenedor)
4. **Opción C:** Usar el patrón "static data bake" — un script en la microVM genera los datos y los inyecta en un HTML estático que se despliega en NaN

**Verificación:** Si un endpoint devuelve arrays vacíos o nulls en NaN pero funciona en local, el problema es casi siempre aislamiento de contenedor.

### Referencia

Ver `references/data-integrity-pattern.md` para ejemplos completos de implementación.

---

## 25. Vanilla JS SPA Module Extension — Añadir Nuevos Módulos

Patrón para añadir nuevos módulos (tabs) a un dashboard SPA vanilla JS existente. Requiere tocar tres puntos sincronizados: sidebar + tab container + JS load functions.

### Arquitectura de extensión

Cada nuevo módulo necesita 3 cambios sincronizados:

```
1. Sidebar: <a onclick="switchTab('modulo')">           ← navegación
2. HTML:    <div id="tab-modulo" class="tab-content">     ← contenedor
3. JS:      function loadModulo() { ... }                 ← lógica
```

### 1. Sidebar — Añadir link

```html
<a class="nz-sidebar__link" onclick="switchTab('modulo')" data-tab="modulo">
  <span class="nz-sidebar__icon">📦</span>
  <span class="nz-sidebar__label">Módulo</span>
</a>
```

**Reglas:**
- `data-tab="modulo"` debe coincidir con el ID del contenedor (`tab-modulo`)
- `onclick="switchTab('modulo')` navega a la tab
- El icono es opcional pero recomendado para UX
- **Cada** sidebar link debe tener su `data-tab` para que el highlight funcione

### 2. HTML — Añadir contenedor tab

```html
<div id="tab-modulo" class="tab-content" style="display:none">
  <h2>📦 Gestión de Módulos</h2>
  <div class="nz-surface nz-surface--glass-soft">
    <div class="nz-surface__header">
      <h3>Lista de módulos</h3>
      <button class="nz-btn nz-btn--glass-liquid-brand" onclick="mostrarFormularioModulo()">
        ➕ Nuevo
      </button>
    </div>
    <div id="modulosList"></div>
    <div id="modulosLoading" class="nz-empty-state">
      <p>Cargando módulos...</p>
    </div>
  </div>
</div>
```

**Reglas:**
- `id="tab-modulo"` — el switchTab lo usa para mostrar/ocultar
- `class="tab-content"` con `display:none` por defecto (la tab activa se muestra al cargar)
- Elementos `Loading` y `List` para el flujo de carga
- Si usa Aurora: `nz-surface nz-surface--glass-soft` para el contenedor

### 3. JS — Añadir función load

```javascript
function loadModulo() {
  var container = document.getElementById('modulosList');
  var loading = document.getElementById('modulosLoading');
  if (!container) return;  // safety check — puede no existir aún
  
  loading.style.display = 'block';
  
  apiFetch('/api/modulos')
    .then(function(data) {
      loading.style.display = 'none';
      if (!data.modulos || data.modulos.length === 0) {
        container.innerHTML = '<div class="nz-empty-state"><p>Sin módulos registrados</p></div>';
        return;
      }
      var html = '<div class="nz-table-wrapper"><table class="nz-table"><thead><tr>' +
        '<th>Nombre</th><th>Estado</th><th>Acciones</th></tr></thead><tbody>';
      data.modulos.forEach(function(m) {
        html += '<tr>' +
          '<td>' + m.nombre + '</td>' +
          '<td><span class="nz-badge nz-badge--' + (m.activo ? 'success' : 'muted') + '">' + (m.activo ? 'Activo' : 'Inactivo') + '</span></td>' +
          '<td><button class="nz-btn nz-btn--sm" onclick="editarModulo(\'' + m.id + '\')">✏️</button> ' +
          '<button class="nz-btn nz-btn--sm nz-btn--danger" onclick="eliminarModulo(\'' + m.id + '\')">🗑️</button></td>' +
          '</tr>';
      });
      html += '</tbody></table></div>';
      container.innerHTML = html;
    })
    .catch(function(err) {
      loading.style.display = 'none';
      container.innerHTML = '<div class="nz-empty-state nz-empty-state--error"><p>Error al cargar módulos</p></div>';
    });
}
```

**Reglas:**
- **NUNCA usar `const` o `let`** si el proyecto usa `var` consistentemente
- **Siempre verificar null** del contenedor antes de manipularlo
- **Siempre `.catch()`** en cada fetch — error silencioso = bug invisible
- **Empty state honesto** cuando no hay datos, nunca inventar

### 4. Registrar en switchTab

En `switchTab()` (o el controlador de tabs), añadir la tab al registro lazy-load:

```javascript
function switchTab(tabName) {
  // ... ocultar todas, mostrar la activa ...
  
  // Lazy load de tabs específicas
  if (tabName === 'modulo' && !window._moduloLoaded) {
    window._moduloLoaded = true;
    loadModulo();
  }
}
```

### 5. Delegación a subagentes (para 3+ módulos)

Cuando hay que añadir 3+ módulos, delegar en paralelo:
- **Subagente A:** Añade los sidebar links + tab containers al HTML
- **Subagente B:** Añade las funciones JS (load, create, edit, delete)
- **Verificar** que los nombres de tab coincidan entre ambos

### Verificación

```bash
# 1. Sidebar links tienen data-tab
grep -c 'data-tab=' public/index.html

# 2. Tab containers existen
grep -c 'id="tab-' public/index.html

# 3. Funciones load existen
grep -c 'function load' public/js/crm.js

# 4. Compilación limpia
npx tsc --noEmit

# 5. Tests pasan
npm test

# 6. Health check
curl -s https://<url>/api/health | grep '"status":"ok"'
```

### Pitfalls

- **Desincronización HTML↔JS**: Si sidebar y container no usan exactamente el mismo nombre de tab, el switchTab no encuentra el contenedor y no muestra nada
- **Olvidar lazy-load flag**: Sin `window._moduloLoaded`, la tab se recarga cada vez que se visita
- **Olvidar `.catch()`**: Las llamadas API fallan silenciosamente — el usuario ve loading eterno
- **Mezclar `const`/`let` con `var`**: Si el proyecto usa `var`, mantener consistencia o rompe en navegadores antiguos
- **No verificar container null**: Si el JS se ejecuta antes de que el DOM exista, `getElementById` devuelve null → TypeError