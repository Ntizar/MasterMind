# Kaizen Executive Presentation — Reference Patterns

Patterns from Kaizen Ineco presentations (v1-v5).
Reusable for any business case / methodology presentation.

**David's preferences (updated June 2025):**
- White background, clean corporate style (McKinsey/BCG)
- NO dark mode for business presentations
- NO icon+title+text card pattern (instantly reads as AI-generated)
- Annual costs, not per-minute rates
- Inter font, blue #2563eb accent, light gray #f9fafb alternating sections

## Section Architecture (5 sections — clean and focused)

1. **Hero** — Tag line, 4 KPI tiles (coste actual vs TimeIneco, 50 informes comparison)
2. **Problema** — Side-by-side: manual process (6 steps, 92-136h) vs automated (6 steps, 30s)
3. **Ejemplo Real** — Embedded report preview with real tables (coste anual por modo, escenarios teletrabajo)
4. **Modelo de Negocio** — Horizontal split: left = investment % (5%/2%/0%), right = numerical example (200K€ project)
5. **Por Qué** — Numbered argument blocks (01-06) with title + paragraph, NOT cards
6. **Inversión** — Investment split + 3-phase roadmap (Consolidación → Producción → Escalamiento)
7. **Cierre** — 4 KPI tiles + closing question

## Reusable Component Patterns

### Numbered Argument Block (replaces AI cards)
```html
<div class="arg-block">
  <div class="arg-num">01</div>
  <div class="arg-body">
    <h4>Title</h4>
    <p>Description with concrete data</p>
  </div>
</div>
```
```css
.arg-block { display: flex; gap: 1.2rem; align-items: flex-start; padding: 1rem 0; border-bottom: 1px solid #e5e7eb; }
.arg-num { font-size: 1.6rem; font-weight: 900; color: #d1d5db; min-width: 40px; text-align: right; }
.arg-body h4 { font-size: 0.92rem; font-weight: 700; }
.arg-body p { font-size: 0.84rem; color: #6b7280; }
```

### Horizontal Split Panel (for proposal + example)
```html
<div class="invest-split">
  <div class="invest-left"><!-- proposal, percentages --></div>
  <div class="invest-right"><!-- numerical example --></div>
</div>
```
```css
.invest-split { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; }
.invest-left { padding: 1.5rem; border-right: 1px solid #e5e7eb; }
.invest-right { padding: 1.5rem; background: #f9fafb; }
```

### Embedded Report Preview
```html
<div style="background:white;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;">
  <div style="background:#2563eb;color:white;padding:1rem 1.5rem;">Report header</div>
  <div style="padding:1.5rem;">
    <!-- KPIs grid + tables + callout -->
  </div>
</div>
```

### Step List (for process comparison)
```html
<div class="step">
  <div class="step-num">1</div>
  <div class="step-content">
    <h4>Step title</h4>
    <p>Description</p>
    <div class="step-time">⏱ Time indicator</div>
  </div>
</div>
```

## CSS Variables (white corporate)

```css
:root {
  --blue: #2563eb;
  --blue-light: #eff6ff;
  --green: #059669;
  --green-light: #ecfdf5;
  --red: #dc2626;
  --red-light: #fef2f2;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-800: #1f2937;
  --gray-900: #111827;
}
```

## Economic Data Tables

Always show annual totals, not per-minute:
```
| Modo     | €/mes | €/año  | Sueldo neto | % sueldo en transporte | Sueldo tras transporte |
|----------|-------|--------|-------------|----------------------|----------------------|
| 🚇 Metro | 55€   | 655€   | 19.806€     | 3,3%                 | 19.151€              |
| 🚗 Coche | 704€  | 8.448€ | 19.806€     | 42,7% 🔴             | 11.358€              |
```

Callout below explains: "Un empleado que va en coche gasta X€ al año. De su sueldo neto de Y€, solo le quedan Z€ reales."

## Key Narrative Patterns

- **The Paradox**: Most counterintuitive finding as a callout box
- **The Closing Question**: "The question isn't if we can afford this. It's if we can afford NOT to."
- **Side-by-Side Comparison**: Red-themed panel (manual, slow, expensive) vs Green-themed panel (automated, fast, cheap)
- **Investment Model**: % per project → numerical example → 3-year projection table

## Pitfalls

- **NO dark mode for business decks** — white background always
- **NO icon+title+text cards** — use numbered blocks, horizontal splits, or tables
- **Annual costs, not per-minute** — "8.448€/año" is clear, "0,31€/minuto" confuses business audiences
- **Animated counters need IntersectionObserver** — `requestAnimationFrame` alone won't trigger on scroll
- **Bar chart minimum width** — set to `Math.max(width, 2)%` so tiny values are still visible
- **Mobile nav** — hide links on `< 768px`, keep logo + badge
- **Tables need horizontal scroll wrapper** on mobile
