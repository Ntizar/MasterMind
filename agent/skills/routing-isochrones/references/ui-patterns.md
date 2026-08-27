# TimeIneco — Patrón de CSS para herramientas de movilidad

## Principio
Simple y elegante. NO Aurora glass. NO dark mode. NO neón.

## Estructura base

```css
/* Reset mínimo */
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f8f9fa;
  color: #1a1a2e;
  overflow: hidden;
  height: 100vh;
}
```

## Layout de 3 zonas

```
┌─────────────────────────────────────────────┐
│ Header (56px, fondo #1a1a2e)                │
├──────────┬──────────────────────────────────┤
│ Sidebar  │  Mapa                             │
│ (320px)  │  (flex: 1)                       │
│          │                                   │
│ Sidebar  │                                   │
│ (auto)   │                                   │
│          │                                   │
└──────────┴──────────────────────────────────┘
```

```css
.app-header {
  height: 56px;
  background: #1a1a2e;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.app-sidebar {
  position: fixed;
  top: 56px;
  left: 0;
  width: 320px;
  height: calc(100vh - 56px);
  overflow-y: auto;
  background: white;
  border-right: 1px solid #e5e7eb;
  padding: 16px;
}

.app-map {
  margin-left: 320px;
  height: calc(100vh - 56px);
}
```

## Botones de modo

```css
.mode-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.mode-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.15s ease;
}

.mode-btn--active {
  border-color: #2563eb;
  background: #eff6ff;
  color: #1d4ed8;
  font-weight: 600;
}
```

## Slider de tiempo

```css
.time-slider {
  width: 100%;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: #e5e7eb;
  border-radius: 2px;
}

.time-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #2563eb;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 1px 4px rgba(37,99,235,0.3);
}

.time-presets {
  display: flex;
  gap: 6px;
}

.preset-btn.active {
  background: #2563eb;
  border-color: #2563eb;
  color: white;
}
```

## KPIs en resultados

```css
.result-kpis {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.result-kpi {
  background: #f9fafb;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
}

.result-kpi__value {
  font-size: 20px;
  font-weight: 700;
  color: #2563eb;
}

.result-kpi__label {
  font-size: 10px;
  color: #6b7280;
  text-transform: uppercase;
}
```

## Colores por modo

```css
/* Coche */ -- color: #2563eb;
/* Bicicleta */ -- color: #f97316;
/* Peatón */ -- color: #22c55e;
/* Bus */ -- color: #a855f7;
```

## Mapa

```css
/* CARTO light tiles — mejor que osm estándar */
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '© OpenStreetMap © CARTO',
  maxZoom: 19
});

/* Canvas renderer para rendimiento */
L.map('map', {
  preferCanvas: true,
  zoomSnap: 0.25,
  zoomDelta: 0.25
});
```

## Responsive

```css
@media (max-width: 600px) {
  .app-sidebar {
    width: 100%;
    height: auto;
    max-height: 50vh;
    position: relative;
    border-right: none;
    border-bottom: 1px solid #e5e7eb;
  }
  .app-map {
    margin-left: 0;
    height: 50vh;
  }
}
```
