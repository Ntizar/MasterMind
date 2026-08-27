---
name: nta-spain-design-pattern
version: "1.0.0"
description: "Patrón de diseño 'Fiscal Broadsheet' de NTA Spain (nta-spain.es) — diseño editorial académico para dashboards de datos. Papel cálido, teal petrol, triple tipografía, sin glass/tech aesthetic. Replicable para proyectos de transporte, demografía y datos públicos."
author: Mastermind
tags: [nta-spain, design-pattern, fiscal-broadsheet, editorial, data-viz, dashboard, transport, publishing]
related_skills: [espanatlas-architecture, frontend-dashboard-patterns, aurora-design-system]
---

# NTA Spain — Patrón de Diseño "Fiscal Broadsheet"

## Referencia

**Web:** https://www.nta-spain.es/
**Autor:** Pablo García Guzmán (@pablogguz_)
**Análisis completo:** `/root/workspace/Mastermind/notes/2026-07-02-nta-spain-design-analysis.md`

## Filosofía de Diseño

> "Warm paper + ink, editorial serif headings, monospace ledger labels, crisp hairline rules."

Estilo **periódico financiero de los años 1920 traducido a digital**. Rechaza deliberadamente el aesthetic tech/startup (sin glass, sin orbs, sin gradientes agresivos).

## Paleta de Color

```css
--bg-primary: #f2eee5;      /* Papel cálido (fondo principal) */
--bg-secondary: #fbf9f4;    /* Papel elevado (cards, sidebar) */
--bg-tertiary: #e7e1d3;     /* Relleno muted */
--text-primary: #211b12;     /* Tinta principal */
--text-secondary: #574e40;   /* Tinta secundaria */
--text-muted: #8a8073;       /* Tinta tenue */
--accent: #0f6d7e;           /* Petrol teal (deep, sofisticado) */
--accent-ink: #0a4f5c;       /* Teal oscuro hover */
--accent-dim: rgba(15,109,126,0.10);
--hairline: rgba(33,27,18,0.12);      /* Líneas finas cálidas */
--hairline-strong: rgba(33,27,18,0.22);
--shadow-sm: 0 1px 2px rgba(33,27,18,0.05);
--shadow-md: 0 4px 16px rgba(33,27,18,0.07);
--shadow-lg: 0 18px 42px rgba(33,27,18,0.11);
```

**Clave:** El color corporate NO es azul ni naranja. Es **teal petrol** (#0f6d7e) — transmite seriedad académica, no startup.

## Tipografía — Sistema Triple

| Uso | Fuente | Características |
|-----|--------|----------------|
| **Títulos editoriales** | Fraunces (serif) | weights 400-600, italic para acentos, optical sizing |
| **UI / cuerpo** | Hanken Grotesk (sans) | weights 400-700, limpia y legible |
| **Ledger / labels / datos** | IBM Plex Mono (mono) | weights 400-600, uppercase con letter-spacing amplio |

**Patrón de título con acento:**
```html
<h1>
  <span class="title-line">Cuentas Nacionales de <span class="title-accent">Transferencia</span></span>
</h1>
```
El acento es Fraunces italic en color teal.

## Texturas y Fondos

### Paper Grain (SVG Noise)
```css
body::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.028;
  mix-blend-mode: multiply;
}
```

### Ledger Grid (solo landing)
```css
.bg-grid {
  background-image:
    linear-gradient(rgba(33,27,18,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(33,27,18,0.035) 1px, transparent 1px);
  background-size: 100% 2.5rem, 4rem 100%;
  mask-image: radial-gradient(ellipse 90% 75% at 50% 42%, black 20%, transparent 95%);
}
```

### Radial Glow Hero
```css
.landing-body {
  background:
    radial-gradient(130% 90% at 50% -12%, rgba(15,109,126,0.07), transparent 55%),
    var(--bg-primary);
}
```

## Layout Explorer (30/70)

```css
.main-container {
  display: grid;
  grid-template-columns: 30% 1fr;
  min-height: calc(100vh - 56px);
}

/* Responsive */
@media (max-width: 900px) {
  .main-container { grid-template-columns: 1fr; }
  .sidebar { display: none; position: fixed; ... }
  .sidebar.open { display: flex; }
}
@media (min-width: 1400px) {
  .main-container { grid-template-columns: 440px 1fr; }
}
@media (min-width: 1600px) {
  .main-container { grid-template-columns: 500px 1fr; }
}
```

## Componentes Clave

### Sidebar Cards (sin fondo, solo hairline inferior)
```css
.card {
  background: transparent;
  border-radius: 0;
  padding: 0.35rem 0 0.9rem;
  border: none;
  border-bottom: 1px solid var(--hairline);
}
.card-header::before {
  content: ''; width: 7px; height: 7px; background: var(--accent);
}
```

### Segmented Control
```css
.chart-type-toggle {
  display: flex;
  background: var(--bg-primary);
  border-radius: var(--border-radius-sm);
  padding: 3px; gap: 3px;
  border: 1px solid var(--hairline-strong);
}
.chart-type-btn.active {
  background: var(--bg-secondary);
  color: var(--accent);
  box-shadow: var(--shadow-sm);
}
```

### Series Checkboxes (2-column grid)
```css
.series-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.3rem;
}
.series-item {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.42rem 0.55rem;
  border: 1px solid var(--hairline);
  border-radius: var(--border-radius-sm);
}
.series-item.checked {
  background: var(--accent-dim);
  border-color: rgba(15,109,126,0.3);
}
```

### Pill Buttons (group filter)
```css
.group-filter-btn {
  border: 1px solid var(--hairline-strong);
  border-radius: 999px;
  padding: 0.36rem 0.7rem;
}
.group-filter-btn.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fbf9f4;
}
```

### Quick Presets (2x2)
```css
.presets {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.4rem;
}
.preset-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-dim);
  transform: translateY(-1px);
}
```

### Info Panel (borde izquierdo)
```css
.info-panel {
  border-left: 3px solid var(--accent);
  padding: 0.95rem 1.15rem;
  box-shadow: var(--shadow-md);
}
.info-panel:hover { border-left-color: var(--accent-ink); }
```

## Hero Landing Patterns

### Animaciones Escalonadas
```css
.hero-kicker { animation: fadeInDown 0.7s ease-out; }
.hero h1    { animation: fadeInUp 0.8s ease-out backwards; }
.subtitle   { animation: fadeInUp 0.8s ease-out 0.25s backwards; }
.actions    { animation: fadeInUp 0.8s ease-out 0.5s backwards; }
.hero-meta  { animation: fadeInUp 0.8s ease-out 0.7s backwards; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### Kicker con líneas decorativas
```css
.hero-kicker::before,
.hero-kicker::after {
  content: '';
  width: 28px; height: 1px;
  background: var(--hairline-strong);
}
@media (max-width: 640px) {
  .hero-kicker::before,
  .hero-kicker::after { display: none; }
}
```

### Botones
```css
.btn {
  padding: 0.9rem 1.6rem;
  font-family: var(--font-display);
  font-size: 0.72rem; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.1em;
}
.btn-primary {
  background: var(--accent);
  color: #fbf9f4;
  border: 1px solid var(--accent);
}
.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--hairline-strong);
}
.btn:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
```

## i18n Pattern
```javascript
const translations = { es: {...}, en: {...} };
let currentLang = localStorage.getItem('nta-lang') ||
  (navigator.language.startsWith('es') ? 'es' : 'en');

function setLang(lang) {
  currentLang = lang;
  localStorage.setItem('nta-lang', lang);
  applyTranslations();
}
```

## Stack Técnico
```
Frontend: Highcharts 11.4.1 + Vanilla JS (sin framework)
CSS: Design system propio en 1 archivo (39KB)
Hosting: Vercel (con Vercel Insights analytics)
Fuentes: Google Fonts (Fraunces, Hanken Grotesk, IBM Plex Mono)
Backend: 0 — todo estático, datos inline en HTML
```

## Mapeo Transporte (cómo aplicarlo)

| NTA Spain | → Proyecto Transporte |
|---|---|
| Transfer inflows | Viajeros por modo / línea |
| Taxes | Costes, emisiones, tiempos |
| Age breakdown | Hora del día / día semana |
| Per capita / Total | Por ruta / total red |
| Year evolution | Evolución horaria / estacional |
| Quick views | Hora punta / finde / festivo |
| Chart type (line/bar) | Series temporales / comparativas |
| Sidebar cards | Control de filtros |
| Info panel | "¿Qué estoy viendo?" contextual |

## Pitfalls

- **NO usar glass effects** — NTA rechaza orbs, glass, blur backgrounds
- **NO usar gradientes agresivos** — solo radial sutil en hero
- **NO dark mode por defecto** — implementado pero desactivado deliberadamente
- **Sombras cálidas** — usar `rgba(33,27,18, ...)` NO `rgba(0,0,0,...)`
- **Cards sin fondo** — NTA usa `background: transparent` + hairline inferior, no cards con bg
- **Triple tipografía** — NO usar una sola fuente para todo
- **Mobile sidebar overlay** — a 900px la sidebar se vuelve overlay fixed
- **Nav-links ocultos en móvil** — no hay hamburguesa para navegación, los links desaparecen
