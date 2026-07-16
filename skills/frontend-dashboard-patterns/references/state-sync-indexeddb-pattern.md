# State Sync: IndexedDB → UI State

**Session:** PLANDEMOVILIDAD demo Renfe (2026-07-14)

## Problem

Vanilla JS apps without a framework often have TWO separate state objects:

1. **`empresaActiva`** (or similar) — loaded from IndexedDB by a state module (`state.js`)
2. **`appState`** — defined inline in `index.html`, used by UI rendering functions

When the page loads, `empresaActiva` gets populated from IndexedDB, but `appState` stays empty. The UI reads from `appState`, so KPIs show 0/empty even though data exists.

## Root Cause

```
initState() → loads IndexedDB → sets empresaActiva (module scope)
initApp()   → calls getEmpleados() → populates appState.empleados (from empty DB)
initDashboard() → reads appState → shows 0s because appState was never synced
```

The demo script wrote data to IndexedDB AFTER the page loaded, so the initial `initApp()` didn't find it. Even on reload, `empresaActiva` loaded correctly but `appState` was never updated from it.

## Fix: Explicit Sync

Add sync in two places:

### 1. On page load (after empresaActiva is ready)

```javascript
// In DOMContentLoaded, after initApp/initEmpresas:
setTimeout(() => {
    const emp = window.pmstApp.getEmpresaActiva?.();
    if (emp && window.pmstApp.appState) {
        window.pmstApp.appState.centro = emp.centro || {};
        window.pmstApp.appState.empresa = emp.empresa || {};
        window.pmstApp.appState.empleados = emp.empleados || [];
        window.pmstApp.appState.diagnostico = emp.diagnostico || {};
        window.pmstApp.appState.dafo = emp.dafo || {};
        window.pmstApp.appState.medidas = emp.medidas || [];
        window.pmstApp.appState.objetivos = emp.objetivos || [];
        // Re-render dashboard
        if (typeof updateDashboard === 'function') updateDashboard();
    }
}, 500); // Wait for async IndexedDB loads
```

### 2. On empresa change event

```javascript
window.addEventListener('empresaCambiada', async () => {
    const emp = window.pmstApp.getEmpresaActiva?.();
    if (emp && window.pmstApp.appState) {
        Object.keys(emp).forEach(k => {
            if (k !== 'id') window.pmstApp.appState[k] = emp[k];
        });
    }
});
```

## Pitfall: Dual State Is the Anti-Pattern

The ROOT fix is to eliminate `appState` and have the UI read directly from `empresaActiva`. But in large inline HTML files with many `getElementById` calls, refactoring is expensive. The sync approach is the pragmatic fix.

**If building new:** Use a single reactive state object. Never maintain two.

## Related

- `multi-empresa-indexeddb-pattern.md` — IndexedDB schema and CRUD
- `defer-scope-pitfall.md` — Script loading order issues
