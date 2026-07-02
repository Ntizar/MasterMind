# NTA Spain — Análisis de Diseño y Arquitectura

**URL:** https://www.nta-spain.es/
**Autor:** Pablo García Guzmán (@pablogguz_)
**Stack:** Vercel + Highcharts 11.4.1 + Vanilla JS + CSS puro (39KB)
**Propósito:** Visualización interactiva de Cuentas Nacionales de Transferencia — perfiles fiscales por edad en España

---

## 🎨 Filosofía de Diseño: "Fiscal Broadsheet"

El diseño evoca un **periódico financiero de los años 1920 traducido a digital**. No es tech/startup, no es glass/Aurora. Es **editorial, académico, sofisticado**. La descripción en CSS lo define perfectamente:

> "Warm paper + ink, editorial serif headings, monospace ledger labels, crisp hairline rules."

### Paleta de Color

| Token | Valor | Uso |
|---|---|---|
| `--bg-primary` | `#f2eee5` | Papel cálido (fondo principal) |
| `--bg-secondary` | `#fbf9f4` | Papel elevado (cards, sidebar) |
| `--bg-tertiary` | `#e7e1d3` | Relleno muted |
| `--text-primary` | `#211b12` | Tinta principal |
| `--text-secondary` | `#574e40` | Tinta secundaria |
| `--text-muted` | `#8a8073` | Tinta十 |
| `--accent` | `#0f6d7e` | **Petrol teal** — deep, sofisticado |

> **Clave:** El color corporate NO es azul ni naranja. Es un **verde azulado profundo (teal/petrol)** que transmite seriedad académica, no startup.

### Tipografía — Sistema Triple

```css
--font-sans: 'Hanken Grotesk', ...sans-serif;      /* UI, textos */
--font-serif: 'Fraunces', Georgia, ...serif;         /* Títulos editoriales */
--font-display: 'IBM Plex Mono', ...monospace;       /* Ledger, labels, datos */
```

- **Fraunces** (serif): Títulos del hero, chart titles, headers. Con peso 560 (soft weight) e italic para el acento. Tiene `opsz` (optical sizing) para adaptarse al tamaño.
- **Hanken Grotesk** (sans): Cuerpo, párrafos, UI general. Limpia, moderna, legible.
- **IBM Plex Mono** (mono): Kickers, labels de chart, tabs de navegación, datos tabulares. Da el "look ledger/contable".

### Texturas y Fondos

1. **Paper grain:** SVG noise filter aplicado al body via `::before`:
   ```css
   body::before {
     background-image: url("data:image/svg+xml,%3Csvg...%3EfeTurbulence...%3C/svg%3E");
     opacity: 0.028;
     mix-blend-mode: multiply;
   }
   ```
2. **Ledger grid** (solo landing): Líneas horizontales/verticales sutiles con máscara radial:
   ```css
   .bg-grid {
     background-image: linear-gradient(rgba(33,27,18,0.05) 1px, transparent 1px),
                       linear-gradient(90deg, rgba(33,27,18,0.035) 1px, transparent 1px);
     background-size: 100% 2.5rem, 4rem 100%;
     mask-image: radial-gradient(ellipse 90% 75% at 50% 42%, black 20%, transparent 95%);
   }
   ```
3. **Radial glow** sutil en hero:
   ```css
   background: radial-gradient(130% 90% at 50% -12%, rgba(15,109,126,0.07), transparent 55%), var(--bg-primary);
   ```
4. **Orbs explícitamente desactivados:** `bg-gradient-orbs { display: none; }` — rechazo deliberado del look "tech/glass".

### Componentes Visuales Clave

#### Hero Landing
- **Kicker:** texto mono + `::before`/`::after` con líneas horizontales finas
- **Título:** Fraunces, `clamp(2.5rem, 7.5vw, 5rem)`, letter-spacing -0.025em
- **Palabra acento:** Fraunces italic en color teal
- **Subtítulo:** max-width 46ch, color text-secondary
- **Botones:** `btn-primary` (fondo teal) y `btn-secondary` (outline sutil)
  - Hover: translateY(-2px) + shadow-md
  - Iconos SVG inline que se mueven 2px a la derecha en hover
- **Animaciones escalonadas:** kicker 0.7s → title 0.8s → subtitle 0.8s+0.25s → actions 0.8s+0.5s → meta 0.8s+0.7s

#### Sidebar Explorer (30% del layout)
- **Cards sin fondo:** `background: transparent; border-radius: 0; border-bottom: 1px solid var(--hairline)`
- **Títulos de card:** Mono, 0.62rem, uppercase, + dot teal antes del texto
- **Segmented controls:** bg-primary, border, padding 3px, gap 3px, active = bg-secondary + shadow-sm
- **Checkboxes series:** 2-column grid, border sutil, acento bg cuando checked
- **Group filters:** Pill buttons (border-radius 999px), active = fondo teal + texto blanco
- **Quick presets:** 2x2 grid, hover = translateY(-1px)

#### Chart Area (70% del layout)
- **Título chart:** Fraunces 1.85rem, weight 560, letter-spacing -0.015em
- **Contenedor chart:** bg-secondary, border-radius 7px, padding 1.35rem, shadow-md
- **Info panel:** bg-secondary, border-left: 3px solid var(--accent) + hover cambia a accent-ink
- **Icono info:** Cuadrado 34x34 con bg accent-dim + color accent

### Sombras (soft, warm, low)
```css
--shadow-sm: 0 1px 2px rgba(33,27,18,0.05);
--shadow-md: 0 4px 16px rgba(33,27,18,0.07);
--shadow-lg: 0 18px 42px rgba(33,27,18,0.11);
```

> Nota: Los colores de sombra usan el mismo `#211b12` (text-primary) con opacidad — todo es cromáticamente coherente.

---

## 🏗️ Arquitectura de la App

### Estructura de Archivos
```
/ (Landing: index.html ~11KB)
/explorer.html (Explorador interactivo ~94KB con datos inline)
/docs.html (Metodología con TOC sticky)
/brief.html (El informe)
/assets/css/style.css (39KB — único CSS, todo el design system)
/assets/icons/ (favicon set completo)
/_vercel/insights/script.js (Analytics)
```

### Dependencias Externas
- **Highcharts 11.4.1** (charting vía CDN)
- **Highcharts modules:** exporting, offline-exporting, export-data
- **Google Fonts:** Fraunces, Hanken Grotesk, IBM Plex Mono
- **Vercel Insights** (analytics)
- **0 frameworks** — vanilla JS puro

### i18n (ES/EN)
- Objeto `translations` con todas las strings en ambos idiomas
- Persistencia vía `localStorage.setItem('nta-lang', lang)`
- Detección automática: `navigator.language.startsWith('es')`
- Botones de idioma con toggle visual (border + bg-secondary cuando active)
- Las traducciones incluyen HTML (ej: footer tiene `<a>` tags)

### Dark Mode
- Implementado pero **desactivado**: `initTheme()` comenta todo y fuerza light
- Clase `.dark-mode` en body cambia todos los tokens CSS
- Botón de toggle existe en HTML pero comentado `<!-- -->`

### Responsive Design
- **≤900px:** Sidebar se convierte en overlay (fixed, top:56px, full screen)
  - Botón hamburguesa `mobile-toggle` visible
  - `sidebar-close` (X button) visible
  - Overlay semi-transparente detrás
- **≤768px:** Padding reducido, títulos escalan
- **≤640px:** Hero compacto, kicker sin líneas, title 2.4rem, acciones en columna
- **≥1400px:** Sidebar 440px
- **≥1600px:** Sidebar 500px

### Componentes de Interacción
| Componente | Descripción |
|---|---|
| Chart type | Line / Bar (segmented control) |
| Breakdown | Average / Education / Sex / Origin (2x2 grid) |
| Scale | Per capita / Synthetic profile / Total 2024 / Evolution 2010-2050 (pills) |
| Year slider | Range input, min 2010 max 2050, con label animado |
| Series checkboxes | 2-column grid con color dots + hover/active states |
| Quick views | Totals / Fiscal balance / Transfers / Taxes (presets 2x2) |
| Stack toggle | Checkbox para apilar componentes en bar chart |
| Export button | Pill con icono download |
| Info panel | ¿Qué estoy viendo? con icono de bombilla |

---

## 📊 Patrón Replicable para Transporte

El layout sidebar-controls + chart-content es PERFECTO para datos de transporte. Mapeo mental:

| NTA Spain | → Transporte |
|---|---|
| Transfer inflows (pensiones, sanidad...) | Viajeros por modo (metro, bus, Cercanías...) |
| Taxes (labor, capital, consumption) | Costes, emisiones, tiempo de viaje |
| Age breakdown | Hora del día / Día de semana |
| Per capita / Total | Per trip / Per route / Total network |
| Year evolution 2010-2050 | Evolución horaria / Semanal / Mensual |
| Quick views | Hora punta / Fin de semana / Festival |

### Elementos a Robar Directamente

1. **Sistema de tokens CSS** — paper+ink philosophy para transporte ("map room" aesthetic)
2. **Triple tipografía** — serif para títulos, sans para UI, mono para datos
3. **Layout sidebar-controls-left + chart-right** — 30/70 que se adapta a móvil
4. **Sidebar overlay en móvil** — botón hamburguesa despliega controles
5. **Checkboxes de series en 2-column grid** — selección de rutas/líneas
6. **Segmented controls** — chart type, breakdown selector
7. **Pill buttons** — scale selector, group filter
8. **Info panel contextual** — "¿Qué estoy viendo?" con borde izquierdo
9. **i18n ES/EN** — con localStorage persistence
10. **Export button** — descarga de datos
11. **Paper grain texture** — textura sutil de fondo
12. **Sombras cálidas** — usando --text-primary como color base

### Cosas que EVITAR (porque NTA las rechaza explícitamente)

- ❌ Glass effects / blur / "liquid glass"
- ❌ Orbs flotantes decorativos
- ❌ Gradientes agresivos
- ❌ Dark mode (desactivado)
- ❌ Tech/startup aesthetic
- ❌ Frameworks pesados

### Stack Técnico Recomendado para Réplica

```
Frontend: Highcharts (o Chart.js si se prefiere open-source) + Vanilla JS
CSS: Design system propio con tokens (39KB es viable)
Hosting: Vercel / GitHub Pages / NaN.builders
Mapa: Leaflet (si se necesita componente geográfico)
Sin bundler, sin framework, sin build step
```

---

## 📝 Lecciones de Arquitectura

1. **Single HTML con datos inline** — explorer.html tiene ~94KB con los datos de perfiles fiscales embebidos. No hay llamada API, todo está en el HTML. Para transporte, los datos GTFS/estáticos pueden ir en JSON aparte y cargarse lazy.
2. **Un solo CSS de 39KB** — todo el design system en un archivo. Sin SASS, sin PostCSS, sin build step.
3. **Translations como objeto JS** — no como archivos separados. Simple, efectivo, sin tooling.
4. **Dark mode desactivado pero implementado** — el código está, los tokens están, solo hay que activarlo. Decisión de diseño deliberada.
5. **Datos y visualización en el mismo HTML** — evita CORS, evita latencia de API, permite compartir URLs (Vercel + analytics).
6. **No hay backend** — todo es estático. Los datos son públicos y están pre-procesados.