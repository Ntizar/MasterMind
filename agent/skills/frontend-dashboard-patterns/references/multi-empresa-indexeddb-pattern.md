# Multi-Empresa IndexedDB Pattern

**Session:** PLANDEMOVILIDAD Fase 3A (2026-07-14)

## Concepto

Arquitectura para apps que gestionan datos de múltiples "empresas" (o clientes, proyectos, etc.) con persistencia local usando IndexedDB. Cada empresa tiene su propio sub-árbol de datos, y se puede cambiar entre ellas sin perder estado.

## Architecture

```
IndexedDB v3 (DB: 'PlanDeMovilidadDB')
├── empresas          → [{ id, nombre, cif, ... }]       (meta)
├── datosEmpresa      → { [empresaId]: { centro, empleados, ... } }  (datos)
├── respuestas        → { [empresaId]: { encuesta, ... } }           (encuestas)
└── kpiMatrix         → { [empresaId]: { [year]: [...] } }           (KPIs)
```

## Key Pattern: State Module

Centralize all state access in a single `state.js` module:

```javascript
// js/state.js — singleton state + IndexedDB persistence
let db = null;
let empresaActiva = null;

export async function initState() {
    db = await openDB('PlanDeMovilidadDB', 3, {
        upgrade(db) {
            if (!db.objectStoreNames.contains('empresas')) db.createObjectStore('empresas', { keyPath: 'id' });
            if (!db.objectStoreNames.contains('datosEmpresa')) db.createObjectStore('datosEmpresa');
            if (!db.objectStoreNames.contains('respuestas')) db.createObjectStore('respuestas');
            if (!db.objectStoreNames.contains('kpiMatrix')) db.createObjectStore('kpiMatrix');
        }
    });
    // Load last active empresa
    const lastId = localStorage.getItem('pmst_empresa_activa');
    if (lastId) empresaActiva = await get('datosEmpresa', lastId);
}

// Generic CRUD
async function get(store, key) { return db.get(store, key); }
async function put(store, key, val) { return db.put(store, key, val); }

// Empresa management
export function getEmpresaActiva() { return empresaActiva; }
export async function cambiarEmpresa(id) { /* load + set active */ }
export async function crearEmpresa(data) { /* create + switch */ }
export async function eliminarEmpresa(id) { /* delete + switch fallback */ }
export async function listarEmpresas() { return db.getAll('empresas'); }

// Data access by path (dot notation)
export function actualizarCampo(ruta, valor) {
    const partes = ruta.split('.');
    let obj = empresaActiva;
    for (let i = 0; i < partes.length - 1; i++) {
        if (!obj[partes[i]]) obj[partes[i]] = {};
        obj = obj[partes[i]];
    }
    obj[partes[partes.length - 1]] = valor;
    // Auto-save with debounce
    debouncedSave();
}
```

## Key Pattern: Export to Global

Module-level variables (`empresaActiva`) are private. Export via `window.pmstApp` for access from inline scripts and other modules:

```javascript
export function exportToGlobal() {
    window.pmstApp = window.pmstApp || {};
    Object.assign(window.pmstApp, {
        crearEmpresa, listarEmpresas, cambiarEmpresa, eliminarEmpresa,
        getEmpresaActiva, importarEncuesta, getEncuesta
    });
}
```

**Pitfall:** If `window.pmstApp` is defined AFTER static imports execute, the static import's `window.pmstApp.gbfs = ...` assignment creates a NEW object that gets overwritten. Solution: use dynamic imports (`import('./js/api-gbfs.js')`) AFTER `window.pmstApp` is fully defined.

## Key Pattern: Empresa Selector in Header

```html
<div id="empresaSelector" style="display:inline-flex;align-items:center;gap:8px"></div>
<button onclick="pmstUI?.abrirModalEmpresas?.()">⚙️ Empresas</button>
```

```javascript
function renderSelector() {
    const selector = document.getElementById('empresaSelector');
    const empresas = await listarEmpresas();
    selector.innerHTML = `<select onchange="pmstApp.cambiarEmpresa(this.value)">
        ${empresas.map(e => `<option value="${e.id}" ${e.id === activa?.id ? 'selected' : ''}>🏢 ${e.nombre}</option>`)}
    </select>`;
}
```

## Pitfalls

1. **ES module init order:** Static imports execute before inline script body. If module A does `window.pmstApp.X = ...` and inline script later does `window.pmstApp = { ... }`, the module's assignment is lost. Fix: dynamic imports after `window.pmstApp` is defined.
2. **IndexedDB versioning:** Changing version number triggers `upgrade()` callback. Don't bump version unnecessarily — it wipes data on some browsers.
3. **Auto-save debounce:** Don't write to IndexedDB on every keystroke. Use 500ms debounce.
4. **Cross-tab sync:** `localStorage` events fire across tabs, but IndexedDB doesn't. If multi-tab is needed, use `BroadcastChannel`.
5. **Spread operator ID leaking (CRITICAL):** When building a datos object with `...childObject`, if the child has an `id` field (e.g., center ID), it overwrites the parent's `id` (empresa ID). This causes the entire app to misidentify the record.
   ```javascript
   // BUG: centroData.id ('renfe-sevilla') overwrites empresa ID
   await dbPut('datosEmpresa', { empresaId: renfeId, datos: { ...centroData, empresaPadre: {...} } });
   // FIX: explicitly set the parent ID after spread
   await dbPut('datosEmpresa', { empresaId: renfeId, datos: { ...centroData, id: renfeId, empresaPadre: {...} } });
   ```
6. **Dual data structure readers:** When demo/seed data uses a different structure than production data, dashboard KPI readers need dual fallback paths:
   ```javascript
   // Support both structures with nullish coalescing
   const sostenible = res.porcentajeSostenible ?? diag.porcentajeSostenible ?? 0;
   const co2 = diag.co2e?.totalToneladas ?? diag.huellaCO2e?.totalCo2eTon ?? 0;
   ```
7. **State sync between IndexedDB module and UI:** See `references/state-sync-indexeddb-pattern.md` — the `empresaActiva` object loaded from IndexedDB and the `appState` object used by inline UI scripts are separate and need explicit sync.

## Multi-Center Hierarchy (Empresa → Centros)

**Session:** PLANDEMOVILIDAD Fase 8 (2026-07-14)

### Concepto

Evolución del patrón multi-empresa: una **empresa** puede tener múltiples **centros de trabajo**. Cada centro tiene su propio diagnóstico, encuesta, huella de carbono y plan de medidas. La empresa ve un consolidado global.

### Data Model

```
empresa (datosEmpresa store)
├── id: UUID
├── nombre: "Renfe Viajeros"
├── cif: "..."
├── centros: [
│   { id: "sevilla", nombre: "Santa Justa", lat: 37.39, lon: -5.98, ... },
│   { id: "madrid",  nombre: "Chamartín",  lat: 40.47, lon: -3.68, ... },
│ ]
├── centroActivo: "sevilla"   ← center selected in UI
└── empresaPadre: null        ← top-level empresa (null)
```

### IndexedDB Schema Extension

```javascript
// state.js — add centroActivo to schema
async function actualizarCampo(ruta, valor) {
    if (ruta === 'centroActivo') {
        empresaActiva.centroActivo = valor;
        debouncedSave();
        return;
    }
    // ... existing dot-notation logic
}

// CRUD for centers within an empresa
export async function crearCentro(centroData) {
    const empresa = getEmpresaActiva();
    if (!empresa.centros) empresa.centros = [];
    const id = centroData.id || slugify(centroData.nombre);
    empresa.centros.push({ id, ...centroData });
    empresa.centroActivo = id;
    await saveEmpresa(empresa);
    return id;
}

export async function eliminarCentro(id) {
    const empresa = getEmpresaActiva();
    empresa.centros = empresa.centros.filter(c => c.id !== id);
    if (empresa.centroActivo === id) {
        empresa.centroActivo = empresa.centros[0]?.id || null;
    }
    await saveEmpresa(empresa);
}
```

### UI Pattern: Center Tabs

```html
<!-- Inside empresa management modal -->
<div class="center-tabs">
    <button class="center-tab active" data-center="sevilla">🏢 Santa Justa</button>
    <button class="center-tab" data-center="madrid">🏢 Chamartín</button>
    <button class="center-tab add-center" onclick="pmstApp.crearCentro()">+ Añadir</button>
</div>
```

### Consolidated View (Global KPIs)

```javascript
// consolidado.js — KPIs globales across all centers
function calcularKPIsGlobales(empresa) {
    const centros = empresa.centros || [];
    return {
        totalCentros: centros.length,
        totalEmpleados: centros.reduce((s, c) => s + (c.empleados?.length || 0), 0),
        mediaSostenible: centros.reduce((s, c) => s + (c.diagnostico?.porcentajeSostenible || 0), 0) / centros.length,
        ranking: centros
            .map(c => ({ id: c.id, nombre: c.nombre, score: c.diagnostico?.porcentajeSostenible || 0 }))
            .sort((a, b) => b.score - a.score)
    };
}
```

### Pitfall: Spread Operator ID Leaking (Multi-Center)

When building center data with `...centerObject`, the center's `id` field overwrites the empresa's `id`:

```javascript
// BUG: center.id ('renfe-sevilla') becomes the empresa's id
const datos = { ...centerData, empresaPadre: empresa };
await dbPut('datosEmpresa', { empresaId: empresa.id, datos });

// FIX: explicitly set empresa ID AFTER spread
const datos = { ...centerData, id: empresa.id, empresaPadre: empresa };
await dbPut('datosEmpresa', { empresaId: empresa.id, datos });
```

## Demo Data Generation Pattern

**Session:** PLANDEMOVILIDAD demo Renfe (2026-07-14)

### Concepto

Script standalone que genera datos ficticios pero realistas directamente en IndexedDB. Útil para demos, testing y presentaciones. El script se ejecuta una vez y la app carga los datos normalmente.

### Pattern

```javascript
// demo-empresa.js — Generador de datos demo
(async function() {
    const DB_NAME = 'PlanDeMovilidadDB';
    const DB_VERSION = 3;

    // 1. Open IndexedDB
    const db = await new Promise((resolve, reject) => {
        const req = indexedDB.open(DB_NAME, DB_VERSION);
        req.onupgradeneeded = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains('empresas')) db.createObjectStore('empresas', { keyPath: 'id' });
            if (!db.objectStoreNames.contains('datosEmpresa')) db.createObjectStore('datosEmpresa');
        };
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
    });

    // 2. Guard: skip if data exists
    if ((await db.count('empresas')) > 0) {
        console.log('⚠️ Data already exists, skipping demo');
        return;
    }

    // 3. Generate empresa + centers
    const empresaId = crypto.randomUUID();
    const centros = [
        { id: 'sevilla', nombre: 'Santa Justa', latitud: 37.392, longitud: -5.977, empleados: generateEmpleados(200) },
        { id: 'madrid',  nombre: 'Chamartín',  latitud: 40.472, longitud: -3.682, empleados: generateEmpleados(350) },
    ];

    // 4. Write to IndexedDB
    const tx = db.transaction(['empresas', 'datosEmpresa'], 'readwrite');
    tx.objectStore('empresas').put({ id: empresaId, nombre: 'Renfe Viajeros', cif: 'F12345678', centros });
    tx.objectStore('datosEmpresa').put(empresaId, {
        centros, centroActivo: 'sevilla',
        empresa: { nombre: 'Renfe Viajeros' },
    });
    await new Promise((resolve, reject) => { tx.oncomplete = resolve; tx.onerror = reject; });

    // 5. Trigger UI refresh
    window.dispatchEvent(new CustomEvent('empresaCambiada'));
    console.log('✅ Demo data loaded');
})();
```

### Key Rules

1. **Generate realistic data**: Use actual city coordinates, realistic employee counts (50-500), real mode splits (60-70% car in Spain)
2. **Fix the empresa ID**: After spreading center data, explicitly set `id: empresaId` (see pitfall above)
3. **Dispatch `empresaCambiada`**: The UI syncs on this event. Without it, the dashboard shows stale data
4. **One-shot generation**: Check if data already exists and skip if so
