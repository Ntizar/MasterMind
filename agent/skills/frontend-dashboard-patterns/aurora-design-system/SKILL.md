---
name: aurora-design-system
description: Design System Ntizar Aurora v6.1 Constellation — CSS puro, 12 packs opt-in, namespaced .nz, liquid glass interactivo, escenas Three.js reutilizables, azul monocromo (sin mezcla azul→naranja), OKLCH, agent-ready con CDN público. Derivado de Ntizar-Aurora.
version: "6.1.0"
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
ntizar.three.css      -> v6: contenedores .nz-three para escenas Three.js (hero/md/sm/glass-frame/interactive)
three-scenes.js       -> v6: librería ES de escenas (icosaedro · grafo · particulas · anillos), fallback sin WebGL
aurora-live.js        -> v6: specular del liquid glass que sigue al cursor (.nz-glass-liquid-live)
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

**Aurora es el sistema de diseño por defecto para artefactos visuales generados por el agente.** No se usan CSS custom sueltos, ni estilos inline generales, ni otros frameworks.

### ⚠️ EXCEPCIÓN — Design systems corporativos de equipo (2026-06-25)

**Cuando un equipo pide un CSS compartido para unificar el estilo de sus herramientas**, NO usar Aurora. En su lugar, crear un **design system propio** alineado con la marca corporativa del equipo.

**Señales de que NO es Aurora:**
- "Queremos un CSS que usen todos del equipo"
- "Que se parezca al intranet de la empresa"
- "Colores de [Empresa]"
- Hay un manual de marca oficial con colores propios

**Flujo correcto:** Usar `design-system-scaffold` para crear un design system desde cero con los colores oficiales de la marca. Ver también `references/design-system-corporativo-workflow.md` para el Kaizen de Ineco y cómo convertir proyectos existentes.

**Ejemplo real:** Equipo Kaizen de Ineco. David pidió un CSS compartido con colores de Ineco. Se creó `kaizen-design-system` con colores oficiales del manual de marca (#1A4488, #CB1823), NO con Aurora.

**Aurora es para:** dashboards personales, apps creativas, landings, proyectos donde el estilo visual es flexible.
**Design system propio es para:** equipos corporativos, empresas con marca definida, herramientas internas que deben ser coherentes con la identidad corporativa.

### ⚠️ EXCEPCIÓN — Presentaciones corporativas / consulting (2026-06-20)

**David rechazó Aurora explícitamente para presentaciones de caso de negocio / propuestas internas.** Pidió "fondo blanco", "elegante", "no parezca hecho por IA". Aurora (mesh, glass, orbs, gradientes) se percibe como "tech/startup" y no como "consulting corporativo".

**Cuándo NO usar Aurora:**
- Presentaciones de caso de negocio (Kaizen, propuestas)
- Informes ejecutivos para stakeholders externos
- Roadmaps y planes de inversión
- Cualquier cosa con estética McKinsey/BCG

**Cuándo SÍ usar Aurora:**
- Dashboards interactivos
- Apps personales
- Landing pages creativas
- El usuario pide glass, mesh, dark, aurora explícitamente

**Estilo alternativo:** Ver `popular-web-designs/references/consulting-corporate-style.md` para el patrón de fondo blanco, tipografía Inter, tablas limpias, KPI tiles, sin glass/mesh/orbs.

### Reglas de branding para todo artefacto HTML generado

1. **CDN obligatorio** — siempre linkar ntizar.css + ntizar.next.css + packs necesarios desde CDN. Nunca CSS embebido o archivos locales.
2. **Skin por defecto: aurora** — data-nz-skin=aurora (azul #2563eb + naranja #f97316 + liquid glass). Ver ERROR CRÍTICO #10 para el fix del violeta.
3. **Theme por defecto: light** — `data-nz-theme="light"`. David prefiere fondos claros: son más elegantes, mejor legibles y más profesionales. Dark solo si el usuario lo pide explícitamente.
4. **Mobile-first OBLIGATORIO** — toda landing/artefacto debe ser mobile-first, NO desktop-first. Base: 1 columna (≤600px), tablet: 2 columnas (601–900px), desktop: 3+ columnas (901px+). NO usar @media (max-width) como estrategia principal. Responsive no es opcional.
5. **Touch targets mínimo 44px** — en móvil, todos los botones, links, inputs, tabs deben tener min-height: 44px (accesibilidad táctil).
6. **Atribucion exacta** — el footer DEBE poner EXACTAMENTE: `Hecho con ❤️ por David Antizar`. El ❤️ es el emoji de corazón (U+2764), NO `(L)`. Sin variaciones. Sin "Analisis por". Sin "via Mastermind Agent". Sin "via Mastermind". Literal exacto con emoji.
7. **David Antizar es el autor**, Mastermind el agente ejecutor. Esto aplica a HTML, posts, informes, notas. Nunca al reves.
8. **Sin ingles** — todo en castellano: etiquetas, contenido, titulos, atributos

### ⚠️ ESTILO "AURORA LIMPIO" — Diseño moderno, no IA (2026-06-22)

**Señal del usuario:** David rechazó el primer HTML demo. Dijo: "el fondo no me gusta nada", "los números son demasiado grandes", "no es suficientemente liquid glass", "todo debería ser más responsive", "mucho más moderno y elegante en blanco naranja y azul sin gradientes raros ni cards típicos de IA".

**Lo que NO es Aurora limpio:**
- ❌ Fondo gradiente naranja/azul que cubre toda la pantalla
- ❌ Orbs decorativos flotantes intrusivos
- ❌ Mesh aurora animado intrusivo
- ❌ Números gigantes (KPIs de 2.5rem+)
- ❌ Cards típicas de IA con gradientes llamativos
- ❌ Desktop-first con media queries al final

**Lo que SÍ es Aurora limpio (estilo iOS 26 / Apple):**
- ✅ **Fondo blanco limpio** (`#ffffff`) con solo toques sutiles de color
- ✅ **Liquid glass REAL** con 4 capas:
  1. Base translúcida con gradiente sutil (rgba 255,255,255,0.72 → 0.62)
  2. `backdrop-filter: blur(24px) saturate(180%)`
  3. Dual inset shadow (luz arriba + profundidad abajo)
  4. Borde cromático con `::before` (specular highlight) y `::after` (chromatic edge)
- ✅ **Números compactos** — KPIs de 1.1–1.25rem, no 2.5rem+
- ✅ **Mobile-first** — base 1 col, tablet 2 col, desktop 3 col
- ✅ **Botones estilo iOS** — brand (azul), accent (naranja), glass, ghost
- ✅ **Badges pill** — colores sutiles, no saturados
- ✅ **Progress bars finas** — 4px de alto, no gruesas
- ✅ **Sin gradientes radiales intrusivos** — solo un toque sutil de color en el fondo

**Implementación del liquid glass real (4 capas):**
```css
.glass-panel {
  position: relative;
  background: linear-gradient(135deg,
    rgba(255,255,255,0.72) 0%,
    rgba(241,245,249,0.55) 50%,
    rgba(255,255,255,0.62) 100%);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  box-shadow:
    inset 0 1px 0 0 rgba(255,255,255,0.9),
    inset 0 -1px 0 0 rgba(0,0,0,0.04),
    0 8px 32px rgba(0,0,0,0.06),
    0 2px 8px rgba(0,0,0,0.03);
  border: 1px solid rgba(255,255,255,0.6);
  border-radius: 16px;
  overflow: hidden;
}
.glass-panel::before {
  content: "";
  position: absolute; inset: 0;
  border-radius: inherit;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%,
    rgba(255,255,255,0.08) 40%,
    transparent 60%);
  pointer-events: none; z-index: 1;
}
.glass-panel::after {
  content: "";
  position: absolute; inset: 0;
  border-radius: inherit;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.35),
    inset 0 0 20px rgba(37,99,235,0.03),
    inset 0 0 40px rgba(249,115,22,0.02);
  pointer-events: none; z-index: 1;
}
```

**Ejemplo de referencia:** Ver `demo-aurora-fix.html` en el repo Ntizar-Aurora.

### Verificacion pre-entrega (OBLIGATORIA)

Antes de dar por terminado cualquier artefacto HTML, verificar:

1. Footer dice EXACTAMENTE: `Hecho con ❤️ por David Antizar` (emoji real, NO `(L)`)
2. Sin "Analisis", sin "via Mastermind Agent", sin "via", sin variantes
3. body class="nz" presente
4. data-nz-skin="aurora" presente
5. **data-nz-theme="light"** (no dark por defecto)
6. CDN links correctos y funcionales
7. **Mobile-first presente** — base 1 col, tablet 2 col, desktop 3+ col. NO desktop-first con max-width
8. **Touch targets 44px** en móvil para botones, links, inputs, tabs
9. **Glass-liquid REAL** — 4 capas (base, backdrop-filter, dual inset shadow, borde cromático)
10. **Números compactos** — KPIs ≤1.25rem
11. **Fondo blanco limpio** — sin gradientes intrusivos, sin orbs flotantes
12. Sin CSS custom >30 lineas
13. Sin hex hardcodes (usar var(--nz-*))

### Vinculación con skills pipeline

Los skills de pipeline (ej: `pdf-to-artifacts-david-antizar`) consumen Aurora pero NO duplican su configuración. Deben referenciar este skill como pre-requisito y solo añadir lo específico de su flujo.

## Workflow para Agentes (CRÍTICO)

### Pasos obligatorios cuando se pida "usa Aurora" o se genere HTML visual:

1. **CARGAR INDEX.md** del repo Ntizar-Aurora — es la fuente de verdad de la API de clases
2. **USAR SOLO** componentes listados en INDEX.md
3. **CSS custom máximo 30 líneas** — solo para lo específico del artefacto
4. **NUNCA hardcodear hex** — siempre `var(--nz-*)`
5. **SIEMPRE** `body class="nz" data-nz-skin="aurora"`

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
- Sin `u-nz-text-brand` en el titular → título sin acento (NOTA: `nz-gradient-text` NO existe, nunca la uses)
- `nz-kpi` sin `--accent` → tiles planos
- `nz-chart` sin `--glass` → gráficos en cajas blancas
- `nz-surface` sin `--glass*` → superficies opacas

**Causa raíz:** El agent elige la primera variante que encuentra en el CHEATSHEET en vez de la variante visualmente rica. Falta una guía de "qué variante usar según el contexto visual".

**Solución:** Para dashboards, apps, landings y cualquier artefacto visual → **SIEMPRE preferir las variantes glass-liquid y animadas.** Ver tabla rápida abajo.

### ⚠️ PREFERENCE — Glass borders como "look de IA" (2026-06-20)

**Señal del usuario:** David rechazó explícitamente cards con bordes glass-liquid visibles (la línea decorativa superior de `nz-card--glass-liquid`). Dijo: "La línea esa en las cards, no me gusta nada. Parece hecho por IA."

**Matiz importante:** David NO rechaza glass en general. Le gustan las cards con profundidad, sombra sutil y backdrop-filter. Lo que rechaza es el **borde decorativo superior** (la línea glass brillante que algunos templates ponen arriba de la card). Es un patrón que se ha vuelto icónico de diseños "AI-generated" (lo mismo ocurre con gradientes neón exagerados, mesh backgrounds con muchas orbs, y horizontal lines decoratives).

**Regla práctica:**
- ✅ `backdrop-filter: blur()` + sombra sutil + bg semitransparente = **elegante**
- ❌ Bordes glass visibles arriba de la card = **"parece hecho por IA"**
- ✅ Usar `nz-card--glass-liquid` pero **sin** la línea decorativa de borde superior si el contexto es presentación ejecutiva o algo que se entrega a stakeholders
- ❌ Evitar horizontal lines decorativas entre secciones en presentaciones (David las rechazó directamente)
- ❌ Evitar elementos que se repitan en cada card (badges decorativos, líneas de color repetitivas) — David los asocia con "AI aesthetic"

**Contexto:** En presentaciones Kaizen/Ineco (v1.0→v2.0→v3.0), la evolución fue: dark mode con glass borders (rechazado) → light mode Aurora con glass borders (rechazado) → light mode Aurora sin glass borders visibles (aceptado con entusiasmo). El factor decisivo fue QUITAR las líneas glass decorativas, no el tema ni los componentes.

**Aplicación general:** Cuando el output es para un stakeholder externo (presentación empresa, informe cliente, landing profesional) → glass sutil sin bordes decorativos. Cuando es interno (dashboard propio, app personal) → glass-liquid completo con borders está OK.

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
| Tipografía | ✅ | u-nz-text-brand (azul sólido en titulares) |

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
   curl -s <url> | python3 /hermes-home/skills/frontend-dashboard-patterns/aurora-design-system/scripts/audit-aurora.py -
   ```
   O desde archivo local:
   ```bash
   python3 /hermes-home/skills/frontend-dashboard-patterns/aurora-design-system/scripts/audit-aurora.py /path/al/index.html
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
| Título | `nz-text-h1` | `u-nz-text-brand` en el span destacado (azul sólido) |
| Avatar | `nz-avatar` | `nz-avatar--aurora` |
| Loading | texto "Pensando..." | `nz-spinner--accent` |
| Tips/callout | div custom | `nz-callout--tip` |
| **Glass interactivo (v6)** | glass estático | `nz-glass-liquid-live` (specular que sigue al cursor, requiere cargar `aurora-live.js`) |
| **Escena 3D (v6)** | canvas Three.js a mano | `data-nz-three="icosaedro\|grafo\|particulas\|anillos"` en `.nz-three` (requiere `ntizar.three.css` + import de `three-scenes.js`) |

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

El repo Ntizar-Aurora está clonado en `C:\Users\d_ant\Projects\Ntizar-Aurora\` (Windows local):
- `INDEX.md` — API completa de clases por pack
- `CHEATSHEET.md` — Resumen de las 321 clases
- `gallery.html` — Referencia visual completa
- `AGENTS.md` — Reglas duras (5 hard rules)
- `LLM.md` — Guía de decisión LLM (~2 KB, "necesito X → packs Y → clases Z")
- `components.json` — Spec machine-readable de todos los componentes
- `examples/` — 5 ejemplos completos con shell CSS propio (login, dashboard, landing, ui-components, forms)

### Referencias incluidas
- `references/dark-mode-migration-pattern.md` — Patrón de migración de dark mode custom → data-nz-theme
- `references/mobile-compact-pattern.md` — Compactación progresiva de hero/KPIs en móvil + patrón de acciones principales
- `references/audit-checklist.md` — Checklist de 21 componentes premium + veredictos de auditoría
- `references/contradiction-audit-gradient-aurora.md` — Auditoría completa de contradicciones en --nz-gradient-aurora (violeta → fix azul+naranja)
- `references/aurora-clean-style.md` — Patrón "Aurora limpio": fondo blanco, glass real 4 capas, mobile-first, números compactos (2026-06-22)
- `references/shell-patterns.md` — 5 patrones de shell CSS (login, dashboard, landing, UI catalog, forms) para que los ejemplos nunca se vean "pelados" (2026-06-22)
- `references/multi-project-audit-unification.md` — Procedimiento para auditar y unificar diseño de múltiples proyectos con Aurora (2026-06-23)
### Scripts
- `scripts/audit-aurora.py` — **v2**: auditoría automática con whitelist de prefijos de shell (patrón ERROR #13), inline styles con tokens no penalizan, componentes premium v6 (`nz-glass-liquid-live`, `nz-three`, `data-nz-three`) y perfil landing (umbral 60 clases). Uso: `python3 audit-aurora.py <archivo.html>` o `curl -s <url> | python3 audit-aurora.py -`. NO valida existencia de clases — una clase inventada en texto puede colarse; la verificación visual en preview es complementaria obligatoria.

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

### Uso del pack Three.js v6 (receta mínima)

```html
<!-- 1. CSS del pack -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.three.css">
<!-- 2. Contenedor con data-nz-three; SIEMPRE incluir .nz-three__fallback para sin WebGL -->
<div class="nz-three nz-three--md nz-three--interactive nz-three--glass-frame"
     data-nz-three="grafo" data-nz-three-nodos="22">
  <canvas class="nz-three__canvas"></canvas>
  <div class="nz-three__fallback">Contenido estático si no hay WebGL</div>
</div>
<!-- 3. importmap + inicialización -->
<script type="importmap">
{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.164/build/three.module.js" } }
</script>
<script type="module">
  import { crearEscenasAuto } from 'https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/three-scenes.js';
  crearEscenasAuto();
</script>
```

Glass interactivo: añadir `nz-glass-liquid-live` a cualquier superficie glass + `import 'https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/aurora-live.js'`. Opt-out global: `data-nz-glass-live="off"` en `<html>`. Respetan `prefers-reduced-motion` ambos.

**Pitfalls v6:**
- Los módulos ES no cargan por `file://` — para probar localmente, servir por HTTP (`python -m http.server`) y hacer copia del HTML con `sed` apuntando al repo local en vez del CDN
- jsDelivr cachea `@master`: si el CDN no refleja un push reciente, verificar con `curl -s -o /dev/null -w "%{http_code}" https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/<fichero>` y purgar si hace falta

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
- **Auditoría automática:** cuando se pida revisar/auditar un HTML contra Aurora, ejecutar SIEMPRE `python3 /hermes-home/skills/frontend-dashboard-patterns/aurora-design-system/scripts/audit-aurora.py` primero para obtener métricas objetivas. No hacer auditoría manual a ciegas.

### ⚠️ ERROR CRÍTICO #10 — Skin aurora con violeta en --nz-gradient-aurora (2026-06-22)

**Señal del usuario:** David dice "se ve morado", "no me gusta el morado", "esto parece morado y no quiero eso".

**Problema:** La skin `aurora` (default) heredaba de `ntizar.css` un `--nz-gradient-aurora` con violeta intermedio: `blue-500 → violet-500 → orange-500` (#3b82f6 → #8b5cf6 → #f97316). Esto creaba un efecto "morado" en botones blend, títulos gradient, barras de progreso, avatares, sparklines, fondos y mesh aurora.

**Causa raíz:** La skin `aurora` en `ntizar.themes.css` NO redefinía `--nz-gradient-aurora`, confiando en la herencia de `ntizar.css`.

**Solución aplicada (commit 3d2a7ba):** La skin aurora ahora redefine explícitamente:
```css
.nz[data-nz-skin="aurora"] {
  --nz-gradient-aurora: linear-gradient(135deg,
    var(--nz-color-blue-600) 0%,
    var(--nz-color-orange-500) 100%);
}
```
Resultado: `#2563eb → #f97316` (azul → naranja directo, sin violeta).

**⚠️ IMPORTANTE PARA FUTURAS SESIONES:** Si al generar un HTML con Aurora se ve algún morado/violeta, verificar:
1. Que se esté cargando `ntizar.themes.css` (donde está el fix)
2. Que el body tenga `data-nz-skin="aurora"`
3. Que no se esté overriding `--nz-gradient-aurora` con CSS custom
4. Si se usa `ntizar.next.css` con `data-nz-color-system="oklch"`, el gradiente aurora usa `hue+50°` que sigue produciendo violeta. En ese caso, redefinir `--nz-gradient-aurora` manualmente.

**Referencia completa:** `references/contradiction-audit-gradient-aurora.md`

### ⚠️ ERROR CRÍTICO #13 — Ejemplos "pelados" sin CSS shell (2026-06-22)

**Señal del usuario:** David dijo "la versión que has hecho de ejemplos las veo demasiado simples y hay botones que no tienen el mismo diseño". Los ejemplos generados con componentes sueltos (nz-btn, nz-card sin contexto) se ven rotos/feos.

**Problema:** Los componentes Aurora necesitan un **CSS shell** de contexto para verse correctos. Un botón `nz-btn--primary` solo, sin un contenedor con bordes, sombras, gradientes de fondo y espaciado propio, se ve como un botón genérico sin el estilo premium de Aurora.

**Lo que NO funciona:**
- ❌ Componentes sueltos en un div blanco sin estilo
- ❌ Botones sin contenedor con padding, border-radius, shadow
- ❌ Formularios sin card wrapper con glass
- ❌ Dashboards sin sidebar, sin stat tiles, sin tablas estilizadas

**Lo que SÍ funciona — Patrón "Shell + Componentes":**

1. **Definir un shell CSS** con su propio `<style>` (máximo 100-200 líneas) que proporcione:
   - Layout (grid, flex, sticky sidebar)
   - Espaciado (padding, margins, gaps)
   - Superficies (bordes, sombras, glass, gradientes de fondo)
   - Tipografía contextual (títulos, labels, breadcrumbs)
   - Iconos SVG inline para navegación
   - Hover states y transiciones
   - Responsive (mobile-first)

2. **Colocar componentes Aurora dentro** del shell como contenido, no como estructura.

3. **El shell hace el 80% del trabajo visual**, los componentes Aurora hacen el 20% (colores, badges, KPIs, tabs, forms).

**Ejemplo mínimo de shell (login):**
```css
.login-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: radial-gradient(ellipse at 30% 20%, var(--nz-surface-glass-brand) 0%, transparent 60%),
              radial-gradient(ellipse at 70% 80%, var(--nz-surface-glass-accent) 0%, transparent 60%);
}
.login-card {
  width: 100%;
  max-width: 26rem;
}
```

**Ejemplo de shell (dashboard):**
```css
.dash-shell {
  display: grid;
  grid-template-columns: 16rem minmax(0, 1fr);
  min-height: 100vh;
}
.dash-sidebar {
  position: sticky; top: 0; height: 100vh;
  background: var(--nz-surface-soft);
  border-right: 1px solid var(--nz-border-soft);
}
```

**Shell templates por tipo de página:**
- **Login:** centered card + aurora radial bg + brand icon
- **Dashboard:** sidebar sticky + main scrollable + stat tiles
- **Landing:** container max-width + hero aurora orbs + features grid + pricing cards
- **UI Catalog:** demo cards + interactive sections + JS for tabs/dropdown/modal/toast
- **Forms:** card wrapper + 2-col grid + custom switch/segmented/otp/range

**Regla:** Si generas un HTML con Aurora, SIEMPRE incluye un shell CSS propio. Nunca entregues componentes "pelados". El shell es lo que hace que los componentes se vean premium.

### ⚠️ ERROR CRÍTICO #12 — "Aurora limpio" — fondo blanco, glass real 4 capas, mobile-first (2026-06-22)

**Señal del usuario:** David rechazó el primer HTML demo. Dijo: "el fondo no me gusta nada", "los números son demasiado grandes", "no es suficientemente liquid glass", "todo debería ser más responsive", "mucho más moderno y elegante en blanco naranja y azul sin gradientes raros ni cards típicos de IA".

**Lo que NO es Aurora limpio:**
- ❌ Fondo gradiente naranja/azul que cubre toda la pantalla
- ❌ Orbs decorativos flotantes intrusivos
- ❌ Números gigantes (KPIs de 2.5rem+)
- ❌ Desktop-first con media queries al final

**Lo que SÍ es Aurora limpio (estilo iOS 26 / Apple):**
- ✅ Fondo blanco limpio (`#ffffff`) con toques sutiles de color
- ✅ Liquid glass REAL con 4 capas: base translúcida, `backdrop-filter: blur(24px) saturate(180%)`, dual inset shadow, borde cromático (`::before` specular + `::after` chromatic edge)
- ✅ Números compactos — KPIs de 1.1–1.25rem
- ✅ Mobile-first — base 1 col, tablet 2 col, desktop 3 col
- ✅ Touch targets 44px mínimo en móvil
- ✅ Sin gradientes radiales intrusivos

**Implementación del liquid glass real (4 capas):** Ver `references/aurora-clean-style.md`

**Referencia:** `references/aurora-clean-style.md`

### ⚠️ ERROR CRÍTICO #11 — Información contradictoria en AGENTS.md y skills (2026-06-22)

**Señal del usuario:** David pregunta "¿es posible que tengas muchos agents.md que te den datos contradictorios?"

**Problema identificado:** Hay múltiples fuentes de verdad que pueden contradecirse:
- `Ntizar-Aurora/AGENTS.md` — reglas del repo
- `Ntizar-Aurora/.github/copilot-instructions.md` — reglas de Copilot
- `Mastermind/AGENTS.md` — reglas generales del sistema
- `aurora-design-system` SKILL.md — reglas del skill Hermes
- `liquid-glass-css` SKILL.md — reglas del skill Hermes

**Riesgo:** Si un skill dice una cosa y el AGENTS.md del repo dice otra, el agente puede generar HTML inconsistente.

**Solución:** Siempre verificar contra el **repo en vivo** (`Ntizar-Aurora/`) como fuente de verdad última. Los skills y AGENTS.md son guías, pero el CSS real es lo que importa. Si hay discrepancia, el CSS del repo gana.

**Verificación rápida:** Si el resultado visual no coincide con lo que describe un skill, ejecutar `grep` en el repo para ver el código real.

### ⚠️ ERROR CRÍTICO #14 — Gradiente azul→naranja rechazado (2026-08-28)

**Señal del usuario:** David sobre el landing rediseñado de MasterMind: *"las cosas con el gradiente este de azul a anaranjado no me gustan nada. Creo que los diseños podían ser mucho más elegantes"*.

**Qué pasó:** La corrección del ERROR #10 (azul→naranja directo, sin violeta) seguía produciendo un degradado de dos tonos que David percibe como poco elegante. **La regla real no es "sin morado", es "sin mezclar azul y naranja en un gradiente"**.

**Solución aplicada (v6.1, repo Ntizar-Aurora):** `--nz-gradient-aurora` es monocromo azul en core y en la skin aurora:
```css
--nz-gradient-aurora: linear-gradient(135deg,
  var(--nz-color-brand) 0%,
  var(--nz-color-brand-strong) 100%);
```

**Regla para futuros artefactos:**
- ❌ NUNCA gradiente que interpole azul→naranja (ni directo ni con pasos intermedios) — David lo rechaza explícitamente
- ✅ Títulos destacados: azul sólido con `u-nz-text-brand` (azul puro) — NO gradiente
- ✅ El azul es primary y el naranja secondary, en elementos separados (regla de acento de AGENTS.md), nunca fundidos
- ✅ Si hace falta un gradiente, monocromo (azul→azul fuerte)

### ⚠️ ERROR CRÍTICO #15 — Clase inventada `nz-gradient-text` (2026-08-28)

`nz-gradient-text` **NO existe en Aurora** (ni en core ni en next) — ha aparecido en el propio skill y en outputs de agentes durante meses. La utilidad documentada es **`u-nz-text-brand`** (texto azul sólido) o `u-nz-text-gradient` (usa `--nz-gradient-aurora`).

**Lección doble:**
1. Antes de usar una clase `nz-*`, verificar que existe en INDEX.md o con `grep` en el repo. Las tablas de este skill pueden contener errores heredados — el repo en vivo manda (ERROR #11).
2. Las clases inventadas en texto/HTML no las detecta bien `audit-aurora.py` (cuenta clases únicas pero no valida existencia) — la verificación visual en preview es la única que las caza.
