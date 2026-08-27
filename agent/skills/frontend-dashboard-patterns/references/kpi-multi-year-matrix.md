# Multi-Year KPI Tracking Matrix

## Pattern
Interactive matrix table where rows = KPIs, columns = years, cells = editable values with trend indicators.

## Architecture
- Data stored in `appState.kpiMatrix = { "2024": { "co2e": 7.9, "sostenible": 20 }, "2025": {...} }`
- Each KPI has a definition: `{ key, label, unit, format, goodDirection: 'up'|'down' }`
- Rendering: dynamic `<thead>` with year columns + `<tbody>` with KPI rows
- Cells are `<input type="number">` with `onchange` handlers that save to appState
- Trend arrows: compare current year vs previous year, apply color classes

## Trend Logic
```javascript
// For each cell, compare with previous year
const prev = kpiMatrix[prevYear]?.[kpi.key];
const curr = kpiMatrix[year]?.[kpi.key];
if (prev !== undefined && curr !== undefined) {
    const delta = curr - prev;
    // goodDirection matters: for CO2, going DOWN is good
    if (kpi.goodDirection === 'down') {
        trend = delta < 0 ? 'up' : delta > 0 ? 'down' : 'stable';
    } else {
        trend = delta > 0 ? 'up' : delta < 0 ? 'down' : 'stable';
    }
}
```

## CSS Classes
```css
.kpi-up { background: #dcfce7; color: #16a34a; }    /* green = improving */
.kpi-down { background: #fef2f2; color: #dc2626; }  /* red = worsening */
.kpi-stable { background: var(--gray-100); color: var(--gray-500); }
```

## Features
- **Add year column**: button creates next year, re-renders
- **Auto-fill from diagnostic**: populates current year from calculated data
- **Export CSV**: generates comma-separated file with all years
- **Evolution chart**: Chart.js line chart with all KPIs over time

## PMST Example KPIs
| Key | Label | Unit | goodDirection |
|-----|-------|------|---------------|
| sostenible | % modos sostenibles | % | up |
| motorizado | % modos motorizados | % | down |
| teletrabajo | % teletrabajo | % | up |
| co2e | CO₂e total | t | down |
| distancia | Distancia media | km | down |
| ocupacion | Ocupación media vehículo | personas | up |
| encuestados | Empleados encuestados | nº | up |
| plazasBici | Plazas bicicleta | nº | up |
| usoBici | % uso bicicleta | % | up |
| paradasTP | Paradas TP en 500m | nº | up |

## Pitfalls
- **Year ordering**: sort years numerically, not alphabetically ("2024" < "2025" works, but "9" > "10" alphabetically)
- **Chart.js re-render**: destroy previous chart instance before creating new one, or get "Canvas already in use" error
- **Input change events**: use `onchange` not `oninput` for number inputs to avoid excessive saves during typing
- **goodDirection inversion**: CO₂ and motorizado are "lower is better" — must invert trend logic
