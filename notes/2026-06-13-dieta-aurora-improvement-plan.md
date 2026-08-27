# Plan de Mejora Visual — MasterFit (Dieta)

> Objetivo: pasar de "Aurora al 40%" a "Aurora al 100%" — usar TODOS los componentes relevantes del sistema de diseño.
> Fecha: 2026-06-13

---

## Diagnóstico actual

- **CSS custom:** 103 líneas (objetivo: ~30)
- **Inline styles hardcode:** 152 de 252
- **Clases Aurora usadas:** 72 únicas
- **Componentes Aurora NO usados:** 20+

---

## Mapeo: Componente no usado → Dónde encaja

### 1. `nz-chart--glass` (charts.css)
**Dónde:** Todos los 10 charts del dashboard
- `#chartPeso`, `#chartMacrosVsObj`, `#chartKcal`, `#chartMacros`, `#chartPasos`
- `#chartDeficit`, `#chartProyeccion`, `#chartComposicion`, `#chartPesoEvo`, `#chartEntrenos`

**Qué cambia:** Envolver cada `<canvas>` en `<div class="nz-chart nz-chart--glass">` y usar paleta `--nz-chart-*` en vez de hex.

**Impacto:** Alto — los gráficos pasan de "cajas blancas" a glass con tooltips nativos.

---

### 2. `nz-progress` (data.css)
**Dónde:** Barras de macros (proteína, carb, grasa) en tab-resumen y tab-progreso
- `#macro-protein-fill`, `#macro-carb-fill`, `#macro-fat-fill`

**Qué cambia:** Reemplazar los `<div>` con `style="width: X%"` por:
```html
<div class="nz-progress nz-progress--accent">
  <div class="nz-progress__bar" style="width: 75%"></div>
</div>
```

**Impacto:** Alto — barras con gradiente, labels, y animación nativa.

---

### 3. `nz-surface--glass` (core)
**Dónde:** Superficies de fondo de secciones y cards que no usan `nz-card`
- Sección header, área de chat IA, listas de comidas/deporte

**Qué cambia:** Usar `class="nz-surface nz-surface--glass"` en vez de `div` con estilos inline.

**Impacto:** Medio — uniformiza la estética glass en zonas no-card.

---

### 4. `nz-bento-grid` (patterns.css)
**Dónde:** Tab-progreso — layout de KPIs 3D InBody
- Grasa %, IMC, peso, ritmo, score, semanas, visceral

**Qué cambia:** Grid asimétrico tipo Apple/Linear:
```html
<div class="nz-bento-grid">
  <div class="nz-bento-grid__cell nz-bento-grid__cell--tall">
    <!-- Score (grande) -->
  </div>
  <div class="nz-bento-grid__cell">
    <!-- Grasa -->
  </div>
  <div class="nz-bento-grid__cell">
    <!-- IMC -->
  </div>
  ...
</div>
```

**Impacto:** Alto — layout visualmente disruptivo, diferencia MasterFit de "otro dashboard".

---

### 5. `nz-hero` (patterns.css)
**Dónde:** Header del dashboard
- Título "MasterFit" + objetivo + avatar

**Qué cambia:** Envolver en `class="nz-hero nz-hero--centered"` con `__eyebrow`, `__title`, `__sub`, `__cta`.

**Impacto:** Medio — el header pasa de "div con h1" a hero section con estructura Aurora.

---

### 6. `nz-stack` / `nz-cluster` (core)
**Dónde:** Layouts de KPIs, formularios, filas de comidas

**Qué cambia:** Reemplazar `style="display:grid;gap:12px"` por `class="nz-stack nz-stack--md"`.

**Impacto:** Bajo-Medio — mejora consistencia de spacing, elimina inline styles.

---

### 7. `nz-skeleton` (data.css)
**Dónde:** Loading states del tab-progreso (Three.js tarda en cargar)
- `#canvas3d-loading`

**Qué cambia:** Reemplazar spinner/texto por skeleton blocks:
```html
<div class="nz-skeleton nz-skeleton--block" style="height:300px"></div>
```

**Impacto:** Medio — loading states profesionales.

---

### 8. `nz-modal` (ui.css)
**Dónde:** Export modal (`#exportModal`)
- Actualmente es un `<div>` con estilos inline

**Qué cambia:** Usar `<dialog class="nz-modal">` nativo con `:open` pseudo-class.

**Impacto:** Bajo-Medio — modal con backdrop nativo, focus trap, y animaciones.

---

### 9. `nz-table` (core)
**Dónde:** Listas de comidas, entrenos, agua
- `#comidasList`, `#deporteList`, `#entrenos-list`, `#waterList`

**Qué cambia:** Usar `<table class="nz-table">` con `nz-table__head`, `nz-table__body`, `nz-table__row`.

**Impacto:** Alto — tablas con glass, hover states, y ordenación visual.

---

### 10. `nz-badge--glass` / `nz-tag` (core)
**Dónde:** Badges de estado, etiquetas de tipo de comida/deporte
- `#iaEstimarBadge`, badges de tipo en comidas/deporte

**Qué cambia:** Reemplazar badges custom por `nz-badge nz-badge--glass-brand`.

**Impacto:** Bajo — pero elimina CSS custom.

---

### 11. `nz-callout--tip` (core)
**Dónde:** Tips container (`#tipsContainer`), consejos en formularios

**Qué cambia:** Usar `class="nz-callout nz-callout--tip"` en vez de divs custom.

**Impacto:** Bajo — pero consistente.

---

### 12. `nz-stepper` (forms.css)
**Dónde:** Proyecciones de peso — mostrar semanas como pasos
- `#proyeccionesContainer`

**Qué cambia:** Si hay datos de progreso temporal, usar stepper visual.

**Impacto:** Bajo.

---

### 13. `nz-divider--label` (ui.css)
**Dónde:** Separadores entre secciones de tabs

**Qué cambia:** Reemplazar `<hr>` o divs separadores por `class="nz-divider nz-divider--label"`.

**Impacto:** Bajo.

---

### 14. `nz-avatar--aurora` (data.css)
**Dónde:** Avatar del usuario en header

**Qué cambia:** Ya se usa `nz-avatar nz-avatar--aurora` ✅ — verificar que esté bien.

---

### 15. `nz-data-card` (data.css)
**Dónde:** Tarjetas de datos individuales (agua, pasos, calorías)

**Qué cambia:** Usar `nz-data-card` para datos con contexto temporal.

**Impacto:** Bajo.

---

### 16. `nz-search` (forms.css)
**Dónde:** Búsqueda de comidas en tab-comidas

**Qué cambia:** Si hay input de búsqueda, usar `class="nz-search"`.

**Impacto:** Bajo.

---

### 17. `nz-form-grid` (forms.css)
**Dónde:** Formularios de registro (peso, comida, deporte, pasos)
- `#formPeso`, `#formComida`, `#formDeporte`, `#formPasos`

**Qué cambia:** `class="nz-form-grid nz-form-grid--2"` en vez de `style="display:grid;grid-template-columns:1fr 1fr"`.

**Impacto:** Medio — formularios con estilo Aurora nativo.

---

### 18. `nz-field` + `nz-input` (forms.css)
**Dónde:** Inputs de todos los formularios

**Qué cambia:** `class="nz-field"` con label + `class="nz-input"` en vez de inputs sueltos.

**Impacto:** Medio — inputs con estilo Aurora, validación visual, focus states.

---

### 19. `nz-checkbox` / `nz-radio` (forms.css)
**Dónde:** Opciones de tipo de comida, tipo de deporte

**Qué cambia:** `class="nz-check"` y `class="nz-radio"` en vez de inputs nativos.

**Impacto:** Bajo.

---

### 20. `nz-nav--glass` (patterns.css)
**Dónde:** Navegación de tabs (la fila de tabs)

**Qué cambia:** Envolver tabs en `class="nz-nav--glass"` con `__brand`, `__links`.

**Impacto:** Alto — la navegación pasa de "fila de botones" a nav glass con estilo premium.

---

## Priorización

### Fase A — Alto impacto visual (hacer primero):
1. **`nz-chart--glass`** — todos los gráficos
2. **`nz-bento-grid`** — layout progreso InBody
3. **`nz-nav--glass`** — navegación de tabs
4. **`nz-table`** — listas de comidas/deporte
5. **`nz-progress`** — barras de macros

### Fase B — Medio impacto:
6. **`nz-hero`** — header
7. **`nz-form-grid` + `nz-input`** — formularios
8. **`nz-surface--glass`** — superficies no-card
9. **`nz-modal`** — export modal
10. **`nz-stack`** — layouts de KPIs

### Fase C — Bajo impacto pero limpieza:
11. **`nz-skeleton`** — loading states
12. **`nz-badge--glass`** — badges
13. **`nz-callout--tip`** — tips
14. **`nz-divider--label`** — separadores
15. **`nz-checkbox` / `nz-radio`** — opciones

---

## Objetivos finales

- **CSS custom:** de 103 → ~30 líneas
- **Inline styles hardcode:** de 152 → ~20 (solo para JS dinámico)
- **Clases Aurora usadas:** de 72 → 120+
- **Glass-liquid:** 100% de componentes interactivos
- **Consistencia:** 0 clases custom inventadas

---

## Notas técnicas

- NO tocar la lógica JS — solo HTML/CSS
- Mantener Three.js en tab-progreso (es parte del valor del proyecto)
- Mantener dark mode (aunque sea opt-in)
- Mantener todos los IDs existentes (el JS los usa)
- CDN: usar `@master` (no pinzar versión)
- Responsive: mantener media queries actuales + añadir responsive de bento grid
