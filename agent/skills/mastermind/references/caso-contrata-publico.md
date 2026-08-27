# Caso: ContrataPúblico — Ley 9/2017 de Contratos del Sector Público

**Fecha inicio:** 2026-06-16
**Proyecto:** Herramienta web para entender y cumplir la LCSPP (Ley 9/2017)
**Repo:** github.com/Ntizar/contrata-publico
**Deploy:** https://ntizar.github.io/contrata-publico/

## Resumen

Proyecto grande (10 módulos/tabs, ~15k líneas estimadas) ejecutado en sesiones de 30 min con crons one-shot. MEGA-PLAN.md como fuente de verdad inyectada en cada cron.

## Sesiones completadas

| # | Sesión | Output | Tamaño |
|---|--------|--------|--------|
| 0 | Crear repo | Ntizar/contrata-publico (público) | — |
| 1 | Parser de la ley | 347 artículos, ley-data.js, ley-texto.json | 733KB + 1MB |
| 2 | Dashboard + Tab 9 | index.html, sistema de tabs, buscador, navegación | 67KB → 48KB |
| 2.5 | Deploy | GitHub Pages activo (HTTP 200) | — |
| 3 | Tab 1 + Tab 2 | Mapa de la Ley (árbol interactivo) + Tipos de Contrato (6 tarjetas + radar Plotly + modal) | — |
| 4 | ⏳ Pendiente | Tab 3 (Procedimientos) + Tab 5 (Calculadora de Plazos) | — |
| 5 | ⏳ Pendiente | Tab 7 (Umbral y Presupuesto) + Tab 8 (Solvencia) | — |
| 6 | ✅ Completada | Tab 4 (Generador de Actas) Parte 1 — 5 actas base | +5KB JS, +2KB CSS |
| 7 | ✅ Completada | Tab 4 (Generador de Actas) Parte 2 — 10 tipos de acta, formulario inteligente con validación en vivo, auto-cálculo %, historial mejorado con preview | +20KB JS |

## Estructura de archivos

```
contrata-publico/
├── MEGA-PLAN.md              ← Fuente de verdad del plan
├── README.md
├── index.html                ← Dashboard SPA (~48KB, 1329 líneas)
├── js/
│   ├── ley-data.js           ← Estructura navegable (733KB)
│   └── modules/
│       └── generador-actas.js ← Tab 4: 10 actas + validación + historial (51KB)
├── data/
│   └── ley-texto.json        ← Texto completo por artículo (1MB)
└── scripts/
    ├── sesion-01-parse-ley.py
    ├── sesion-02-dashboard-base.py
    ├── sesion-03-mapas-tipos.py
    ├── sesion-04-procedimientos-plazos.py
    ├── sesion-05-umbral-solvencia.py
    ├── sesion-06-actas-parte1.py
    ├── sesion-07-actas-parte2.py
    └── sesion-08-checklist-pulido.py
```

## Decisiones técnicas

- **Zero backend:** HTML vanilla + Aurora CDN + Plotly CDN + localStorage
- **Deploy:** GitHub Pages (frontend puro, sin servidor)
- **Orquestación:** 7 crons one-shot (sesiones 3-8), cada uno autocontenido
- **Datos:** 347 artículos parseados del BOE en dos formatos (estructura + texto completo)
- **CSS:** Aurora Design System via CDN + custom CSS inline en index.html
- **Arquitectura de módulos:** JS en `js/modules/` con lazy-load via switch en index.html

## Arquitectura de módulos (patrón aprendido en Sesión 6)

El proyecto usa una **SPA single-file** con la siguiente arquitectura de extensión:

1. **Cada tab** tiene un `<div id="tab-NOMBRE">` en `index.html`
2. **Cada módulo** es un archivo en `js/modules/NOMBRE.js` con IIFE `(function(){ ... })()`
3. **Lazy load:** `switchTab()` carga el módulo con `case 'NOMBRE': renderFunc(); break;`
4. **Script tag:** `<script src="js/modules/NOMBRE.js"></script>` en `<head>`
5. **CSS:** estilos inline en `<style>` de index.html (no archivos externos)
6. **API pública:** funciones expuestas via `window.func = func` para que el HTML las llame

### Patrón del módulo JS

```javascript
(function() {
  'use strict';
  var _state = {};
  function _privateHelper() { ... }
  window.renderNombre = function() {
    // Leer datos, generar HTML, inyectar en DOM
  };
  window.publicaFuncion = function() { ... };
})();
```

### Patrón de actas (Sesión 6 + 7)

Cada acta es un objeto en un diccionario `ACTAS_DB` con:
- `id`, `nombre`, `icono`, `descripcion`, `seccion`
- `articulosRef`: array de artículos LCSPP
- `campos`: array de campos (id, label, tipo, obligatorio, opciones)
- `generar(datos)`: función que devuelve texto del acta

### Formulario inteligente (Sesión 7 — nuevo)

**Patrón de validación en vivo:**
1. CSS classes: `.cp-field-error` (rojo), `.cp-field-success` (verde)
2. `addEventListener('input', ...)` en cada campo → cambia clase según valor
3. Al generar: campos vacíos obligatorios → `.cp-field-error`
4. Resumen visual: `<div id="cpValidationSummary">` con lista de campos faltantes
5. Auto-cálculo: campos como `porcentajeVariacion` se calculan al escribir otros campos

**CSS en index.html:**
```css
.cp-field-error { border-color: var(--nz-color-accent) !important; }
.cp-field-success { border-color: #27ae60 !important; }
.cp-validation-summary { padding: 12px 16px; border-radius: 10px; }
.cp-validation-summary.error { background: rgba(192,57,43,0.08); color: #c0392b; }
.cp-validation-summary.success { background: rgba(39,174,96,0.08); color: #27ae60; }
.cp-auto-calc { font-size: 0.75rem; color: var(--nz-color-brand); font-style: italic; }
```

### Historial mejorado (Sesión 7 — nuevo)

**Patrón de historial en localStorage:**
1. Array en `localStorage.getItem('cp_actas_history')`
2. Entrada: `{ id: timestamp, actaId, actaNombre, fecha ISO, texto }`
3. Render: icono + nombre + fecha + preview (80 chars) + botones
4. `limpiarHistorial()` con confirm para borrar todo
5. Límite: máximo 50 entradas

## Pitfalls

1. **f-string + JS collision:** Python f-strings interpretan `{string}` como variable → NameError. Fix: `.replace()` con `{PLACEHOLDER}`.
2. **Regex JSON a 700KB+:** `r'const VAR = (\\{.*\\});'` falla. Fix: brace counting manual.
3. **Token inline en curl:** puede fallar. Fix: script Python que lee `.env` directamente.
4. **NO usar subagentes para HTML >10KB** — write_file/patch directo. Subagentes fallan con timeout.
5. **NO usar `const` para variables globales** — usar `var` (window scope).
6. **Python script con JS embebido:** `\n` y `\` interpretados por Python → errores de sintaxis. Fix: usar `patch`/`write_file` directo en lugar de script con JS incrustado.

## Lecciones

- MEGA-PLAN.md debe ser autocontenido para que un cron lo entienda sin contexto
- Scripts de sesión autocontenidos: leer del filesystem, no variables de entorno
- Deploy verificar inmediatamente tras push — GitHub Pages tarda ~1-2 min
- SPA single-file: módulos JS en `js/modules/` con lazy-load, no todo inline
- Validación en vivo con CSS classes + auto-cálculo es reutilizable para cualquier formulario
