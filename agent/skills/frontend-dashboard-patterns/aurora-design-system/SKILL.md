---
name: aurora-design-system
description: Design System Ntizar Aurora v5.1 Constellation — CSS puro, 11 packs opt-in, namespaced .nz, 5 skins, liquid glass real, OKLCH, multi-axis theming, agent-ready con CDN público. Derivado de Ntizar-Aurora.
version: "5.1.1"
tags: [css, design-system, aurora, liquid-glass, ntizar]
---

# Aurora Design System — Patrón Ntizar CSS

## Descripción

Design System CSS puro sin dependencias, sin build step, namespaced bajo `.nz`. 1 archivo core + 10 packs opt-in. 5 skins de marca. Liquid glass real con OKLCH. CDN público en jsDelivr.

## Origen

Derivado del repositorio [Ntizar-Aurora](https://github.com/Ntizar/Ntizar-Aurora) v5.1.

## Arquitectura

```
ntizar.css            -> core (siempre)
ntizar.themes.css     -> 5 skins (aurora · sunset · midnight · ocean · citrus)
ntizar.data.css       -> KPIs, dashboards, progress, meter, skeleton, avatar, timeline
ntizar.charts.css     -> contenedores para Chart.js/Apex/D3, sparkline + donut CSS-only
ntizar.maps.css       -> Leaflet/Mapbox/MapLibre con look Ntizar
ntizar.viz.css        -> stages para three.js, fondos aurora, orbs, glow ring
ntizar.motion.css     -> reveal, glow-pulse, aurora-pan, shimmer, marquee, typing, hover-lift
ntizar.forms.css      -> switch, custom check/radio, range, OTP, file drop, stepper, search
ntizar.ui.css         -> modal, drawer, tabs, accordion, dropdown, toast, tooltip, command-bar
ntizar.patterns.css   -> app-shell, hero, pricing, features, faq, footer, auth-shell, empty/error
ntizar.next.css       -> v5: liquid glass real, OKLCH, multi-axis theming, mesh, forced-colors, skin AAA
```

## Quick Start

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.next.css">

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

## Reglas de Oro

1. **Todo lo público vive bajo `.nz`** — no hay clases globales sueltas
2. **Todos los valores son tokens `--nz-*`** — nunca hardcodes un hex o un `16px`
3. **Sin `!important`** fuera de utilidades
4. **BEM** para componentes: `.nz-card__body--featured`
5. **Si no aparece en `gallery.html`, no existe** — la galería es la única fuente de verdad de la API pública

## Uso con IA Agents (crucial para ahorrar tokens)

**NO** pegar el CSS en el prompt (170 KB ≈ 50.000 tokens).

**SÍ** hacer:
1. Dar al agent solo `AGENTS.md` + `INDEX.md` (~20 KB / ~5.000 tokens)
2. Linkar el CSS vía CDN en el HTML generado
3. Decir al agent: "Generate HTML only. The CSS is already linked. Use Aurora classes from INDEX.md."

## Drop-in Files para AI Tooling

- `AGENTS.md` — estándar abierto para agents (OpenAI, Sourcegraph, Anthropic)
- `.github/copilot-instructions.md` — auto-loaded por GitHub Copilot
- Para Claude Code: copiar `AGENTS.md` a `CLAUDE.md`
- Para Cursor: `.cursor/rules/aurora.mdc`

## Default Usage Policy (Agente — obligatorio)

**Aurora es el ÚNICO sistema de diseño aceptable para artefactos visuales generados por el agente.** No se usan CSS custom sueltos, ni estilos inline generales, ni otros frameworks.

### Reglas de branding para todo artefacto HTML generado

1. **CDN obligatorio** — siempre linkar ntizar.css + ntizar.next.css + packs necesarios desde CDN. Nunca CSS embebido o archivos locales.
2. **Skin por defecto: aurora** — data-nz-skin=aurora (azul #2563eb + naranja #f97316 + liquid glass)
3. **Theme por defecto: light** — `data-nz-theme="light"`. David prefiere fondos claros: son más elegantes, mejor legibles y más profesionales. Dark solo si el usuario lo pide explícitamente.
4. **Responsive SIEMPRE** — toda landing/artefacto debe incluir media queries para móvil (<768px). Grids deben adaptar columnas (2 col → 1 col), nav debe tener hamburger, tablas scroll horizontal. Responsive no es opcional.
5. **Atribucion exacta** — el footer DEBE poner EXACTAMENTE: `Hecho con (L) por David Antizar`. Sin variaciones. Sin "Analisis por". Sin "via Mastermind Agent". Sin "via Mastermind". Literal exacto.
6. **David Antizar es el autor**, Mastermind el agente ejecutor. Esto aplica a HTML, posts, informes, notas. Nunca al reves.
7. **Sin ingles** — todo en castellano: etiquetas, contenido, titulos, atributos

### Verificacion pre-entrega (OBLIGATORIA)

Antes de dar por terminado cualquier artefacto HTML, verificar:

1. Footer dice EXACTAMENTE: `Hecho con (L) por David Antizar`
2. Sin "Analisis", sin "via Mastermind Agent", sin "via", sin variantes
3. body class="nz" presente
4. data-nz-skin="aurora" presente
5. **data-nz-theme="light"** (no dark por defecto)
6. CDN links correctos y funcionales
7. **Responsive CSS presente** — media queries, grids adaptables, hamburger nav
8. Sin CSS custom >30 lineas
9. Sin hex hardcodes (usar var(--nz-*))
10. **Glass-liquid check:** Cards usan `nz-card--glass-liquid`, botones usan `--glass-liquid-*`, fondo tiene `nz-aurora-mesh--animated`, hay al menos 1 `nz-orb`, hay `nz-anim-fade-in` en secciones principales. Si alguna de estas falta → corregir antes de entregar.

### Vinculación con skills pipeline

Los skills de pipeline (ej: `pdf-to-artifacts-david-antizar`) consumen Aurora pero NO duplican su configuración. Deben referenciar este skill como pre-requisito y solo añadir lo específico de su flujo.

## Workflow para Agentes (CRÍTICO)

### Pasos obligatorios cuando se pida "usa Aurora" o se genere HTML visual:

1. **CARGAR INDEX.md** del repo Ntizar-Aurora — es la fuente de verdad de la API de clases
2. **CARGAR CHEATSHEET.md** — resumen de las 321 clases extraídas de gallery.html
3. **USAR SOLO** componentes listados en INDEX.md/CHEATSHEET.md
4. **CSS custom máximo 30 líneas** — solo para lo específico del artefacto
5. **NUNCA hardcodear hex** — siempre `var(--nz-c-*)`
6. **SIEMPRE** `body class="nz" data-nz-skin="aurora"`

### ⚠️ ERROR CRÍTICO #1 — CSS custom en vez de Aurora (2026-06-03)

Los agentes tienden a **intentar recrear el look de Aurora con CSS custom** en vez de usar los componentes reales. Esto produce HTMLs que "dicen" Aurora pero no lo usan.

**Síntomas de fallo:**
- Más de 50 líneas de CSS custom `<style>`
- Clases inventadas (`.step`, `.arrow`, `.decision`, etc.)
- Hex hardcodes (`#0f172a`, `#2563eb`, `#f97316`)
- Sin `body class="nz"`
- Sin `data-nz-skin="aurora"`
- Sin `nz-card`, `nz-glass`, `nz-badge`, etc.

**Causa raíz:** No cargar INDEX.md ni CHEATSHEET.md como referencia.

**Solución:** Cargar INDEX.md (fuente de verdad) y CHEATSHEET.md (resumen rápido) ANTES de generar cualquier HTML. Usar SOLO componentes listados.

### ⚠️ ERROR CRÍTICO #2 — "Aurora flat" en vez de glass-liquid (2026-06-11)

Incluso cuando el agent SÍ usa clases Aurora, tiende a elegir las variantes **planas/básicas** (`nz-card`, `nz-btn--primary`) en vez de las **glass-liquid** que dan el look premium. David lo describió como "puro croissant" — funcional pero sin alma.

**Síntomas de fallo:**
- `nz-card` sin variante glass → card blanca plana, sin profundidad
- `nz-btn--primary` en vez de `nz-btn--glass-liquid-brand` → botón genérico
- Sin `nz-aurora-mesh--animated` → fondo blanco sin vida
- Sin `nz-orb` → nada de decoración atmosférica
- Sin `nz-anim-fade-in` → todo aparece de golpe sin transición
- Sin `nz-hover-lift` → cards sin interacción visual
- Sin `nz-gradient-text` → títulos sin personalidad
- `nz-kpi` sin `--accent` → tiles planos
- `nz-chart` sin `--glass` → gráficos en cajas blancas
- `nz-surface` sin `--glass*` → superficies opacas

**Causa raíz:** El agent elige la primera variante que encuentra en el CHEATSHEET en vez de la variante visualmente rica. Falta una guía de "qué variante usar según el contexto visual".

**Solución:** Para dashboards, apps, landings y cualquier artefacto visual → **SIEMPRE preferir las variantes glass-liquid y animadas.** Ver tabla rápida abajo.

### ⚠️ ERROR CRÍTICO #3 — Usar Aurora al 40% (2026-06-13)

El agent usa los componentes básicos de Aurora (cards glass, botones glass, mesh) pero **ignora 20+ componentes disponibles** que dan el look disruptivo y profesional.

**Síntomas de fallo:**
- Gráficos sin `nz-chart--glass` → gráficos en cajas blancas
- Barras de progreso custom → no usar `nz-progress`
- Navegación de tabs custom → no usar `nz-nav--glass`
- Layouts de KPIs planos → no usar `nz-bento-grid`
- Formularios con grid inline → no usar `nz-form-grid`
- Listas con divs → no usar `nz-table`
- Modal custom → no usar `nz-modal`
- `nz-btn--glass-liquid-secondary` → clase que NO existe en Aurora
- Inline styles con hex/px → no usar tokens `--nz-*`
- Clases custom inventadas (`mf-*`, `ia-*`) → usar Aurora

**Checklist ANTES de entregar cualquier artefacto visual:**
1. [ ] Todos los gráficos envueltos en `nz-chart nz-chart--glass`
2. [ ] Barras de progreso usan `nz-progress nz-progress--accent`
3. [ ] Navegación usa `nz-nav--glass` con `nz-nav-item`
4. [ ] Layouts de datos usan `nz-bento-grid` con `__cell--span-*`
5. [ ] Formularios usan `nz-form-grid` con `nz-field` + `nz-input`
6. [ ] Listas/tablas usan `nz-table`
7. [ ] Modales usan `<dialog class="nz-modal">`
8. [ ] KPIs usan `nz-kpi nz-kpi--accent`
9. [ ] Botones usan `nz-btn--glass-liquid-brand` / `nz-btn--glass`
10. [ ] Superficies usan `nz-surface--glass`
11. [ ] Sin clases inventadas (`nz-btn--glass-liquid-secondary` NO EXISTE)
12. [ ] Sin inline styles con hex/px (usar `--nz-*` tokens)
13. [ ] Mínimo 100 clases Aurora únicas (no 70)

**Causa raíz:** El agent se queda en lo básico y no explora todos los componentes del sistema.

**Solución:** Cargar INDEX.md completo, recorrer TODOS los componentes, y verificar el checklist antes de entregar.

### ⚠️ ERROR CRÍTICO #3 — "Aurora al 40%" — usar solo lo básico y olvidar el resto (2026-06-13)

El agent carga la skill de Aurora, usa cards glass + botones glass + mesh, y **se detiene ahí**. Deja en el tintero TODO lo que viene después: componentes de datos, layouts avanzados, formularios, modales, progress, charts, skeletons. El resultado es un dashboard que "dice" Aurora pero se queda en la superficie.

**Síntomas de fallo:**
- Solo usa nz-card, nz-btn, nz-aurora-mesh, nz-orb (los 4 más obvios)
- NO usa nz-chart--glass, nz-progress, nz-meter, nz-surface, nz-bento-grid, nz-hero, nz-stack, nz-table, nz-modal, nz-skeleton, nz-kpi--accent
- 100+ líneas de CSS custom en vez de tokens Aurora
- 150+ inline styles con hex/px hardcode en vez de var(--nz-*)
- Clases inventadas que no existen en Aurora (`nz-btn--glass-liquid-secondary`)

**Causa raíz:** El agent confunde "usar Aurora" con "usar los componentes más visibles de Aurora". No hace un **inventory completo** de qué componentes de INDEX.md podrían aplicarse al artefacto.

**Solución — Checklist post-diseño OBLIGATORIA:**
Antes de entregar cualquier artefacto visual, verificar CADA categoría:

| Categoría | ¿Usado? | Componente correcto |
|---|---|---|
| Cards | ✅ | nz-card--glass-liquid |
| Botones | ✅ | nz-btn--glass-liquid-brand (NO inventar) |
| Fondo | ✅ | nz-aurora-mesh--animated + nz-orb |
| KPIs | ❌ | nz-kpi--accent (NO nz-kpi plano) |
| Gráficos | ❌ | nz-chart--glass (NO divs custom) |
| Progreso | ❌ | nz-progress, nz-meter |
| Superficies | ❌ | nz-surface--glass (NO divs con estilos) |
| Layouts | ❌ | nz-bento-grid, nz-stack, nz-hero |
| Tablas | ❌ | nz-table |
| Modales | ❌ | nz-modal (NO divs custom) |
| Loading | ❌ | nz-skeleton |
| Animaciones | ✅ | nz-anim-fade-in, nz-hover-lift |
| Tipografía | ✅ | nz-gradient-text |

**Regla de oro:** Si un artefacto tiene más de 3 categorías vacías → NO está usando Aurora correctamente. Revisar INDEX.md y reemplazar componentes custom por los de Aurora.

### ⚠️ ERROR CRÍTICO #5 — Dark mode con `body.mf-dark` en vez de `data-nz-theme` (2026-06-13)

Cuando se migra un proyecto existente que usa dark mode con `body.mf-dark` o `body.dark`, el agent tiende a mantener ese patrón en vez de usar el sistema de temas de Aurora.

**Síntomas de fallo:**
- `body.classList.toggle('mf-dark')` en JS
- `body.mf-dark .nz-*` en CSS (30+ líneas de overrides con `!important`)
- `body.classList.contains('mf-dark')` para detectar tema
- Clases custom `mf-toast`, `mf-comida-row`, `mf-mesh`, `mf-content`
- Hex hardcode en overrides (`#0f172a`, `#e2e8f0`, `rgba(30,41,59,0.85)`)

**Solución — Migración completa (5 pasos):**
1. **HTML body:** `data-nz-theme="light"` / `data-nz-theme="dark"` (NO `class="mf-dark"`)
2. **JS toggle:** `body.classList.toggle('mf-dark')` → `body.setAttribute('data-nz-theme', isDark ? 'light' : 'dark')`
3. **JS detección:** `body.classList.contains('mf-dark')` → `body.getAttribute('data-nz-theme') === 'dark'`
4. **CSS:** `body.mf-dark` → `body[data-nz-theme="dark"]`
5. **Tokens:** `rgba(30,41,59,0.85)` → `var(--nz-surface)`, `rgba(71,85,105,0.5)` → `var(--nz-border-medium)`

**Eliminar clases custom:** `mf-toast` → `toast`, `mf-comida-row` → `nz-table__row`, `mf-mesh` → `nz-aurora-mesh--animated`, `mf-content` → `nz-stack nz-stack--lg`

**Verificación post-migración:**
- `grep -c "mf-dark" archivo.html` → 0
- `grep -c "mf-toast" archivo.html` → 0
- `grep -c "mf-comida" archivo.html` → 0
- CSS custom < 30 líneas de código

**Referencia:** Ver `references/dark-mode-migration-pattern.md`

### ⚠️ ERROR CRÍTICO #6 — Dark mode innecesario en apps de uso frecuente (2026-06-13)

Cuando el usuario dice "la parte dark no creo que aporte mucho", **eliminar el dark mode completamente** en vez de migrarlo.

**Señales de que hay que quitarlo:**
- Usuario menciona que dark mode "no aporta"
- La app es de uso frecuente/rápido (dieta, tracking, registro)
- El hero/header se ve demasiado grande en móvil y el dark mode añade complejidad visual

**Acción:**
1. Eliminar botón de toggle dark mode del HTML
2. Eliminar `data-nz-theme` del body (Aurora usa light por defecto)
3. Eliminar toda la sección CSS de `body[data-nz-theme="dark"]`
4. Eliminar función `toggleDarkMode()` del JS
5. Eliminar `localStorage.getItem('aurora-dark-mode')` del init
6. Eliminar detección dark mode en Three.js u otros subsistemas
7. Asegurar que todo se ve bien en tema claro (es el único tema)

**Verificación post-eliminación:**
- `grep -c "darkMode\|dark-mode\|data-nz-theme" archivo.html` → 0
- El dashboard debe funcionar perfectamente sin ningún tema oscuro

### ⚠️ ERROR CRÍTICO #7 — Hero/KPIs demasiado grandes en móvil (2026-06-13)

En apps de uso frecuente (dieta, tracking), el hero y los KPIs ocupan demasiado espacio en móvil.

**Solución — Compactación progresiva:**
- Desktop: hero `nz-size-3xl`, KPI value `nz-size-2xl`
- ≤768px: hero `nz-size-2xl`, KPI value `nz-size-xl`
- ≤480px: hero `nz-size-xl`, KPI value `nz-size-lg`
- Eyebrow/subtitle también escalan: `xs → 2xs`

**Pad de KPIs en móvil:** reducir de `var(--nz-space-3) var(--nz-space-2)` a `var(--nz-space-1) var(--nz-space-0)`.

**Acción principal primero:** cuando una acción es la más usada (registrar peso, enviar mensaje, etc.), ponerla como primer tab y tab activo por defecto.

### ⚠️ ERROR CRÍTICO #8 — Botón de acción secundaria en el hero (2026-06-13)

Botones como "Exportar CSV" no deben estar en el hero — compiten con la acción principal y ocupan espacio valioso en móvil.

**Solución:**
- Acciones principales (registro, enviar, crear) → primer tab activo o botón grande visible
- Acciones secundarias (exportar, configuración, ayuda) → footer como botón ghost discreto
- El hero solo debe contener: título + info esencial + avatar

**Verificación:** En móvil, el hero debe tener máximo 2 elementos interactivos (avatar + info). Nada más.

### ⚠️ ERROR CRÍTICO #9 — Auditoría de diseño: detectar proyectos "Aurora parcial" (2026-06-16)

Cuando David dice "revisa el diseño", "se parece más a aurora", "haz una auditoría", o cualquier variante que implique **evaluar cuánto usa Aurora un HTML existente**, NO hacer la auditoría a mano con ojos. Usar el script automatizado primero, luego presentar resultados.

**Flujo de auditoría (OBLIGATORIO):**

1. **Ejecutar script automatizado:**
   ```bash
   curl -s <url> | python3 agent/skills/frontend-dashboard-patterns/aurora-design-system/scripts/audit-aurora.py -
   ```
   O desde archivo local:
   ```bash
   python3 agent/skills/frontend-dashboard-patterns/aurora-design-system/scripts/audit-aurora.py /path/al/index.html
   ```

2. **Presentar resultados en formato tabla** con métricas clave:
   - CSS custom líneas (límite: 30)
   - Clases custom count (ideal: <=5)
   - Hex hardcodes (ideal: 0)
   - Inline styles (ideal: <=3)
   - Clases Aurora únicas (mínimo: 100)
   - Packs cargados vs packs necesarios
   - Componentes premium usados (de 21 posibles)

3. **Categorizar por gravedad:**
   - 🔴 CRÍTICO: CSS custom >50 líneas, >10 clases custom, 0 componentes premium
   - 🟡 PARCIAL: CSS custom 30-50 líneas, 5-10 clases custom, 50-70% componentes premium
   - 🟢 OK: CSS custom <=30 líneas, <=5 clases custom, >=70% componentes premium

4. **Presentar checklist visual** de los 21 componentes premium con ✅/❌

5. **Si el proyecto está en un repo**, verificar también:
   - `grep -c "nz-" index.html` → clases Aurora
   - `grep -c "data-nz-theme=" index.html` → tema configurado
   - `grep -c "data-nz-skin=" index.html` → skin configurado
   - `grep -c "nz-aurora-mesh" index.html` → fondo premium
   - `grep -c "nz-orb" index.html` → decoración premium

**Caso real (ContrataPúblico, 2026-06-16):**
- 578 líneas CSS custom (❌ 19x el límite)
- 54 clases custom `.cp-*` (❌)
- 0 de 21 componentes premium (❌)
- 2 packs cargados de 10 necesarios (❌)
- 42 clases Aurora (❌ mínimo 100)
- Veredicto: "AURORA PARCIAL ~15% — necesita rediseño completo"

**Causa raíz:** El agent usa los componentes más visibles de Aurora (hero, sidebar, botones) pero ignora TODO lo demás, creando CSS custom propio. Es la combinación de ERROR CRÍTICO #1 + #2 + #3.

**Solución:** Script automatizado + checklist de 21 componentes + migrar TODO a clases Aurora.

**Referencia:** Ver `references/audit-checklist.md` para el checklist completo de 21 componentes premium.

El agent inventa nombres de clases Aurora que **no existen**, como `nz-btn--glass-liquid-secondary`. Esto produce botones sin estilo o estilos rotos.

**Clases que NO existen (lista negra):**
- `nz-btn--glass-liquid-secondary` → usar `nz-btn--glass` o `nz-btn--ghost`
- `nz-btn--glass-liquid-brand-soft` → usar `nz-btn--tonal-brand-soft`
- `nz-tabs__tab` → usar `nz-tab`
- `nz-card--glass-liquid-brand` → no existe como variante, usar `nz-card--glass-liquid` con `data-nz-skin`

**Solución:** Si no encuentras una clase en INDEX.md o CHEATSHEET.md, NO la inventes. Usa un token `var(--nz-*)` en inline style o busca la clase equivalente documentada.

### 📋 Tabla rápida: variantes Aurora para apps/dashboards visuales

| Componente | ❌ Básico (evitar) | ✅ Premium (usar siempre) |
|---|---|---|
| Card | `nz-card` | `nz-card--glass-liquid` |
| Botón brand | `nz-btn--primary` | `nz-btn--glass-liquid-brand` |
| Botón accent | `nz-btn--accent` | `nz-btn--glass-liquid-accent` |
| Superficie | `nz-surface` | `nz-surface--glass` o `--glass-brand` |
| KPI | `nz-kpi` | `nz-kpi--accent` sobre `nz-card--glass-liquid` |
| Chart | `nz-chart` | `nz-chart--glass` con `nz-hover-lift` |
| Badge | `nz-badge` | `nz-badge--glass` o `--glass-brand` |
| Form input | `nz-field` + `nz-input` | `nz-input` dentro de `nz-card--glass-liquid` |
| Tabs | `nz-tabs` sueltos | `nz-tabs__list` dentro de `nz-card--glass-liquid` |
| Título | `nz-text-h1` | `nz-gradient-text` |
| Avatar | `nz-avatar` | `nz-avatar--aurora` |
| Loading | texto "Pensando..." | `nz-spinner--accent` |
| Tips/callout | div custom | `nz-callout--tip` |

**Fondo obligatorio para apps visuales:**
```html
<!-- Mesh animado fijo detrás de todo -->
<div class="nz-aurora-mesh nz-aurora-mesh--animated" style="position:fixed;inset:0;z-index:0;pointer-events:none;"></div>
<!-- Orbs decorativos -->
<div class="nz-orb nz-orb--aurora nz-orb--sm" style="position:fixed;top:10%;left:5%;z-index:0;"></div>
<div class="nz-orb nz-orb--accent" style="position:fixed;bottom:15%;right:8%;z-index:0;"></div>
<!-- Contenido sobre el mesh -->
<div style="position:relative;z-index:1;">...</div>
```

**Animaciones de entrada (pack motion):**
- `nz-anim-fade-in` + `nz-anim--delay-2/3/4` para escalonar elementos
- `nz-hover-lift` en cards interactivos
- `nz-anim-glow-pulse` en elementos destacados

**CDN extra necesario para glass-liquid + motion:**
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.next.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.motion.css">
```

### Repo local

El repo Ntizar-Aurora debe estar clonado en `/root/workspace/Ntizar-Aurora/`:
- `INDEX.md` — API completa de clases por pack
- `CHEATSHEET.md` — Resumen de las 321 clases
- `gallery.html` — Referencia visual completa
- `AGENTS.md` — Reglas duras (5 hard rules)

### Referencias incluidas
- `references/dark-mode-migration-pattern.md` — Patrón de migración de dark mode custom → data-nz-theme
- `references/mobile-compact-pattern.md` — Compactación progresiva de hero/KPIs en móvil + patrón de acciones principales
- `references/audit-checklist.md` — Checklist de 21 componentes premium + veredictos de auditoría
### Scripts
- `scripts/audit-aurora.py` — Auditoría automática: CSS custom, clases custom, hex hardcodes, componentes premium usados, packs cargados. Uso: `python3 audit-aurora.py <archivo.html>` o `curl -s <url> | python3 audit-aurora.py -`

### CDN correcto

**Mínimo (landing/simple):** siempre estos 4:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.next.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.data.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.ui.css">
```

**Dashboard/app completa:** añadir estos 4 additionally:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.charts.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.forms.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.motion.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.patterns.css">
```

**Pitfall:** Si usas `nz-chart`, `nz-input`, `nz-anim-*`, o `nz-cluster` sin cargar el pack correspondiente, los estilos no aplican y el resultado se ve roto. Carga TODOS los packs que necesites.

## Pitfalls

- **No JS shipped** — modal/tabs/drawer/dropdown/toast son styled, no behaved. Hay que togglear clases manualmente
- **WCAG AAA** aplica solo a la skin `contrast`, no a todas
- **No tree-shaking** — una página con 5 componentes carga el pack completo
- **Sin releases taggeados** — pin a `@master` hasta que se taggee v5.1.0
- **Error común:** generar CSS custom standalone en vez de linkar Aurora CDN. Siempre CDN. Siempre Aurora. Sin excepción.
- **ERROR CRÍTICO #1:** Intentar recrear el look de Aurora con CSS custom en vez de usar componentes reales. Cargar INDEX.md + CHEATSHEET.md antes de generar HTML.
- **ERROR CRÍTICO #2:** Usar variantes básicas de Aurora (`nz-card`, `nz-btn--primary`) en vez de glass-liquid (`nz-card--glass-liquid`, `nz-btn--glass-liquid-brand`) para dashboards y apps visuales. El resultado se ve "plano" y sin personalidad. Ver tabla de variantes en la sección de errores críticos.
- **Verificación visual:** Si el dashboard tiene >3 cards blancas planas sin glass effect, algo va mal. Revisar que se usan variantes `--glass-liquid` o `--glass`.
- **Tab class names:** La estructura correcta de tabs es `nz-tabs > nz-tabs__list > nz-tab.nz-tab--active`. NO usar `nz-tabs__tab` (no existe). Ejemplo correcto:
  ```html
  <div class="nz-tabs">
    <div class="nz-tabs__list">
      <div class="nz-tab nz-tab--active" data-tab="tab1">Tab 1</div>
      <div class="nz-tab" data-tab="tab2">Tab 2</div>
    </div>
  </div>
  ```
  Para el JS de toggle: `tab.classList.add('nz-tab--active')` / `classList.remove('nz-tab--active')`.
- Botones tonales inventados: NO usar `nz-btn--tonal-brand-soft` ni variantes inventadas. Usar solo las documentadas en CHEATSHEET: `--primary`, `--secondary`, `--accent`, `--danger`, `--ghost`, `--glass`, `--glass-brand`, `--glass-accent`, `--glass-liquid`, `--glass-liquid-brand`, `--glass-liquid-accent`.
- **Auditoría automática:** cuando se pida revisar/auditar un HTML contra Aurora, ejecutar SIEMPRE `python3 agent/skills/frontend-dashboard-patterns/aurora-design-system/scripts/audit-aurora.py` primero para obtener métricas objetivas. No hacer auditoría manual a ciegas.
