# Responsive Mobile Patterns — DataHub España (2026-06-30)

## 3 Breakpoints + Landscape

### Tablet (≤768px)
```css
#sidebar {
    position: fixed; bottom: 0; left: 0; right: 0;
    height: 50vh; border-radius: 12px 12px 0 0;
    -webkit-overflow-scrolling: touch;
}
.tabs-row {
    flex-wrap: nowrap; overflow-x: auto;
    scroll-snap-type: x proximity;
}
.tab-btn {
    flex-shrink: 0; scroll-snap-align: start;
    font-size: 10px; padding: 3px 7px;
}
.kpi-row { grid-template-columns: repeat(2, 1fr); gap: 6px; }
#map { height: 35vh; min-height: 200px; }
```

### Móvil (≤480px)
```css
#sidebar { height: 55vh; border-radius: 10px 10px 0 0; }
.tabs-row { padding: 4px 6px; gap: 2px; }
.tab-btn { font-size: 9px; padding: 2px 6px; border-radius: 12px; }
.kpi-row { grid-template-columns: 1fr 1fr; gap: 4px; }
.kpi { padding: 5px 6px; border-radius: 6px; }
.kpi-label { font-size: 8px; }
.kpi-value { font-size: 13px; }
#map { height: 30vh; min-height: 180px; }
.info-grid { grid-template-columns: 1fr !important; }
.ccaa-card { font-size: 9px !important; }
```

### Landscape (≤500px alto)
```css
@media (max-height: 500px) and (orientation: landscape) {
    #sidebar { width: 50% !important; border-radius: 0 12px 12px 0; }
    #map { height: 60vh; }
    .kpi-row { grid-template-columns: repeat(4, 1fr); }
}
```

## Key Principles
- `flex-wrap: wrap` for tab bars (not nowrap)
- `scroll-snap` for horizontal swipe on tabs
- `-webkit-overflow-scrolling: touch` on all scrollable containers
- KPIs go from 4col → 2col → 1col as screen shrinks
- Sidebar goes from right panel → bottom sheet on mobile
- Charts: `max-width: 100%; height: auto;`
- Font sizes: labels 8-9px, values 13-15px on mobile

## CCAA Grid Responsive
```css
/* Tablet: 2 columns */
.ccaa-grid { grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }
/* Mobile override: 1 column */
@media (max-width: 480px) {
    .ccaa-grid { grid-template-columns: 1fr !important; }
}
```
