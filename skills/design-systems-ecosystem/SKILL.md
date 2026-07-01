---
name: design-systems-ecosystem
description: "Ecosistema completo de design systems CSS: creación desde cero (scaffold), estilos corporativos flat (Kaizen), glassmorphism liquid (Aurora/Esios), y optimización para LLMs. Incluye Aurora Constellation v5.1, Kaizen v4.0, y patrones de extensión."
version: "1.0.0"
tags: [css, design-system, aurora, kaizen, liquid-glass, glassmorphism, corporate, scaffold]
---

# Design Systems Ecosystem — Ecosistema de Design Systems CSS

## Resumen

Colección de skills para crear, extender y usar design systems CSS en proyectos personales, corporativos y creativos.

## 1. Design System Scaffold (creación desde cero)

Procedimiento completo para crear un design system CSS desde una imagen de referencia:
- Extraer colores de manual de marca PDF o screenshot
- Definir tokens CSS con variables `:root`
- Crear componentes: app shell, cards, tiles, buttons, forms, tables, badges
- Crear index.html galería + index-standalone.html (CSS embebido)
- Crear AGENTS.md para IAs (~8-12KB) + README.md
- Crear repo GitHub + push + CDN jsDelivr

**Reglas críticas:**
- NUNCA cards bordeadas (delata IA) — usar títulos sección + línea 2px + tiles limpios
- Evolucionar DS antes de aplicar — auditar → extender → commit → aplicar
- CDN solo funciona con repos públicos — privados → copiar CSS localmente
- NUNCA usar `read_file()` para copiar contenido CSS/HTML (añade números de línea)

## 2. Kaizen Design System v4.0 (corporativo flat)

CSS corporativo para equipos con colores oficiales de marca. Estilo plano, sin glass, sin gradientes.
- **Colores:** Azul #1A4488, Rojo #CB1823 (Ineco)
- **Prefijo:** `--kz-*` y clases `kz-*`
- **33 secciones:** layout, sidebar, tiles, KPIs, buttons, forms, tables, badges, tabs, notices
- **Sidebar:** `position: fixed` — requiere `margin-left` en contenido o ambos `position:fixed`
- **Responsive:** NO incluido — implementar en CSS custom del proyecto

**Cuándo usar Kaizen vs Aurora:**
- Kaizen: equipos, intranets, colores corporativos oficiales, estilo enterprise
- Aurora: dashboards personales, apps creativas, glass, mesh, dark

## 3. Liquid Glass CSS (glassmorphism)

Efecto Liquid Glass estilo Esios/Aurora — gradientes azul+naranja, backdrop-filter glass, grid patterns.
- **Variables:** `--nz-color-brand: #2563eb`, `--nz-color-accent: #f97316`
- **Glass REAL (4 capas):** base translúcida + saturate backdrop + dual inset shadow + borde cromático
- **Glass genérico ❌:** solo rgba + blur = sin profundidad ni reflejos
- **David prefiere:** tema claro, elegancia > llamatividad, animaciones mínimas
- **Migración Dark→Light:** 7 pasos de inversión de variables

## 4. Aurora Constellation v5.1 (sistema de diseño Ntizar)

CSS-only design system con 11 packs modulares + liquid glass real + OKLCH.
- **Core:** ntizar.css (≈40KB) — tokens, base, objects, componentes, utilities
- **Packs opcionales:** themes, data, charts, maps, viz, motion, forms, ui, patterns, next
- **6 skins:** aurora (default), sunset, midnight, ocean, citrus, contrast (WCAG AAA)
- **Multi-axis theming:** theme, skin, shape, density, motion, color-system via data-*
- **Liquid Glass Real (v5):** specular highlight + chromatic edge + dual inset shadow
- **CSS Houdini @property:** declaraciones FUERA de @layer, reglas DENTRO de @layer
- **Agent-Ready:** dar AGENTS.md + INDEX.md (~5KB) en vez de pegar CSS (170KB ≈ 50K tokens)

### 11 Packs
| Archivo | Contenido | Cargar cuando |
|---------|-----------|---------------|
| ntizar.css | Core (~40KB): tokens, base, objects, componentes | Siempre |
| ntizar.themes.css | 5 skins + paleta charts | Cambiar identidad |
| ntizar.data.css | KPIs, stat-tile, progress, meter, skeletons | Dashboards |
| ntizar.charts.css | nz-chart, legends, tooltips, sparkline | Gráficos |
| ntizar.maps.css | nz-map para Leaflet/Mapbox, overlays HUD | Mapas |
| ntizar.viz.css | Stages full-bleed, aurora orbs, glow rings | 3D/generative |
| ntizar.motion.css | reveal/rise/scale/glow animations | Animaciones |
| ntizar.forms.css | Switch, OTP, file drop, stepper | Formularios |
| ntizar.ui.css | Modal, drawer, tabs, accordion, toast | Overlays |
| ntizar.patterns.css | App-shell, hero, pricing, FAQ, footer | Páginas completas |
| ntizar.next.css | v5: Liquid Glass, OKLCH, multi-axis, mesh | Capa disruptiva |

## 5. Aurora Nightly (mejora continua)

Pipeline automático de mejora continua: 4 jobs nocturnos que investigan tendencias web, analizan gaps y aplican mejoras CSS focalizadas.
- **Schedule:** 01:00-04:00 UTC diarios
- **Workflow:** investigación → análisis gap → 3 mejoras CSS → commit → reaprendizaje
- **Repo:** `/root/workspace/Ntizar-Aurora`

## 6. Aurora LLM Optimization

Optimizar un design system EXISTENTE para consumo por LLMs (reducir tokens, mejorar estructura).

## Pitfalls comunes

- **CDN jsDelivr solo funciona con repos públicos** — privados → 404 silencioso → copiar CSS localmente
- **Sidebar position: fixed** — requiere margin-left en contenido o ambos position:fixed
- **read_file() corrompe CSS** — añade números de línea → usar `open().read()` en Python
- **Glass genérico ≠ Liquid Glass REAL** — el glass genérico es solo blur sin profundidad
- **No mezclar design systems** — Aurora (personal/creativo) vs Kaizen (corporativo/equipo)
- **No sobreingenierizar** — el usuario corrige si tiendes a sobreingenierizar. Preferir simplificar.

## Referencias
- `references/componentes-data-tools.md` — Checklist de 10 componentes que faltan en DS corporativos
- `references/pdf-brand-manual-extraction.md` — Extraer colores de manual de marca PDF
- `references/css-houdini-property-pattern.md` — Patrón CSS Houdini @property
- `references/css-only-dropdown-has-pattern.md` — Patrón dropdown CSS-only con :has()
- `references/ntizar-projects-patterns.md` — Patrones de 6 proyectos Ntizar
