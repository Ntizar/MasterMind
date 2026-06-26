---
name: kaizen-design-system
description: >-
  Kaizen Design System v4.0 — CSS corporativo para Equipo Kaizen de Ineco.
  Colores oficiales del manual de marca: Azul #1A4488, Rojo #CB1823.
  Estilo flat corporativo, sin glass, sin gradientes, sin sombras.
version: "1.0.0"
tags: [css, design-system, kaizen, ineco, corporate, flat]
related_skills: [aurora-design-system, rebranding-proyecto-web]
---

# Kaizen Design System v4.0

## Descripción

CSS corporativo para el **Equipo Kaizen de Ineco**. 33 secciones de componentes, estilo flat limpio inspirado en la intranet real de Ineco. Derivado del repositorio [kaizen-design-system](https://github.com/Ntizar/kaizen-design-system).

## ⚠️ Cuándo usar Kaizen vs Aurora

**Usar Kaizen cuando:**
- El equipo pide un CSS compartido para unificar estilo
- Hay colores corporativos oficiales (manual de marca)
- El diseño debe parecerse a la intranet/infraestructura de la empresa
- El usuario dice "colores de [Empresa]" o "estilo corporativo"

**Usar Aurora cuando:**
- Dashboards personales, apps creativas, landings
- El estilo visual es flexible
- El usuario pide glass, mesh, dark, aurora explícitamente

**Referencia:** Ver `aurora-design-system` para la excepción documentada (2026-06-25).

## Colores oficiales

| Color | Hex | Pantone | Uso |
|-------|-----|---------|-----|
| Azul principal | `#1A4488` | 7687 C | Header, botones primarios, acentos |
| Rojo | `#CB1823` | 485 C | Complementario, alertas, badges error |
| Azul medio | `#3463AC` | — | Complementario secundario |
| Azul claro | `#6B96CF` | — | Complementario terciario |

## Variables CSS

Todas usan prefijo `--kz-`:

```css
/* Colores */
--kz-azul: #1A4488;
--kz-rojo: #CB1823;
--kz-azul-medio: #3463AC;
--kz-azul-claro: #6B96CF;

/* Escala de azules */
--kz-azul-900 a --kz-azul-50

/* Escala de rojos */
--kz-rojo-600 a --kz-rojo-50

/* Neutrales */
--kz-negro: #1a1a2e;
--kz-gris-900 a --kz-gris-50;
--kz-blanco: #ffffff;

/* Semi-transparentes */
--kz-overlay: rgba(0,0,0,0.45);
--kz-backdrop: rgba(255,255,255,0.8);

/* Tipografía */
--kz-font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--kz-font-mono: 'JetBrains Mono', 'Fira Code', monospace;
--kz-text-xs a --kz-text-3xl;

/* Espaciado */
--kz-gap-xs: 4px;
--kz-gap-sm: 8px;
--kz-gap-md: 16px;
--kz-gap-lg: 24px;
--kz-gap-xl: 32px;
--kz-gap-2xl: 48px;

/* Radio */
--kz-radius-sm: 4px;
--kz-radius-md: 6px;
--kz-radius-lg: 8px;

/* Layout */
--kz-sidebar-width: 380px;
--kz-header-height: 60px;
--kz-banner-height: 44px;
```

## Clases principales

**Layout:** `.kz-sidebar`, `.kz-header`, `.kz-banner`, `.kz-grid`, `.kz-grid-sidebar`
**Sidebar:** `.kz-sidebar-category`, `.kz-sidebar-item`
**Tiles/KPIs:** `.kz-tile`, `.kz-tile-icon`, `.kz-tile-label`, `.kz-tile-value`, `.kz-tile-unit`
**Stats:** `.kz-stats-row`, `.kz-stat-box`, `.kz-stat-val`, `.kz-stat-lbl`
**Botones:** `.kz-btn-primary`, `.kz-btn-secondary`, `.kz-btn-accent`, `.kz-btn-ghost`
**Tabla:** `.kz-table`
**Forms:** `.kz-input`, `.kz-select`, `.kz-textarea`, `.kz-checkbox`, `.kz-radio`, `.kz-toggle`
**Filtros:** `.kz-chips`, `.kz-chip`, `.kz-chip-active`
**Slider:** `.kz-slider`, `.kz-slider-row`, `.kz-slider-value`
**Carga:** `.kz-dropzone`, `.kz-progress`, `.kz-progress-fill`
**Loading:** `.kz-spinner`, `.kz-loading-overlay`, `.kz-skeleton`
**Búsqueda:** `.kz-search-dropdown`, `.kz-search-dropdown-item`
**Paneles:** `.kz-panel`, `.kz-panel-bottom`, `.kz-panel-right`, `.kz-panel-open`
**Feedback:** `.kz-toast`, `.kz-status`, `.kz-empty`
**Badges:** `.kz-badge`, `.kz-badge-success`, `.kz-badge-warning`, `.kz-badge-error`
**Tabs:** `.kz-tab`, `.kz-tab-active`
**Avisos:** `.kz-notice`, `.kz-notice-error`, `.kz-notice-success`
**Noticias:** `.kz-news`, `.kz-carousel`

## Cómo incluir

```html
<!-- Opción 1: CDN (SOLO si el repo es PÚBLICO) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/kaizen-design-system@master/kaizen.css">

<!-- Opción 2: Archivo local (RECOMENDADO — siempre funciona) -->
<link rel="stylesheet" href="css/kaizen.css">

<!-- Opción 3: Ruta relativa (proyectos locales) -->
<link rel="stylesheet" href="../../kaizen-design-system/kaizen.css">
```

### ⚠️ CDN no funciona con repos privados

jsDelivr **NO sirve archivos de repos privados de GitHub**. Si `kaizen-design-system` es privado, la URL CDN devuelve **404 silencioso** → la app carga sin estilos (HTML crudo).

**Fix:** Copiar `kaizen.css` al directorio `css/` del proyecto y referenciarlo localmente. Verificar con:
```bash
curl -sI "https://cdn.jsdelivr.net/gh/Ntizar/kaizen-design-system@master/kaizen.css" | head -3
# Si devuelve 404 → repo privado → copiar localmente
```

### ⚠️ Layout sidebar: `position: fixed`

`.kz-sidebar` usa `position: fixed` (fuera del flow del grid). Esto significa que el contenido principal (mapa, etc.) **se solapa con el sidebar** a menos que se añada `margin-left`:

```css
/* En el CSS custom del proyecto */
.kz-map {
  margin-left: var(--kz-sidebar-width);  /* 380px */
  width: calc(100% - var(--kz-sidebar-width));
  height: 100vh;
}
```

**Síntoma sin fix:** El mapa cubre todo el viewport, el sidebar es invisible aunque el DOM lo tiene. Los controles (input, botones) aparecen transparentes sobre el mapa.

**Verificación:** `getComputedStyle(document.querySelector('.kz-sidebar')).position` debe devolver `fixed`. Si es `fixed`, el `margin-left` es obligatorio.

### Mejor enfoque: ambos `position:fixed`

En vez de `margin-left` (que puede causar doble compensación con CSS Grid), hacer que **tanto sidebar como mapa sean `position:fixed`**:

```css
/* Desktop: sidebar fijo izquierda, mapa llena el resto */
.kz-sidebar { position: fixed; left: 0; top: 0; bottom: 0; width: var(--kz-sidebar-width); z-index: 100; }
.kz-map { position: fixed; left: var(--kz-sidebar-width); right: 0; top: 0; bottom: 0; }

/* Mobile (<768px): sidebar → bottom-sheet, mapa full-width */
@media (max-width: 768px) {
  .kz-sidebar { top: auto; bottom: 0; left: 0; right: 0; height: 48px; overflow: hidden; transition: height 0.3s; }
  .kz-sidebar.kz-sidebar-open { height: 55vh; overflow-y: auto; }
  .kz-map { left: 0; }
}
```

En mobile, el sidebar se colapsa a una barra de 48px (peek handle) y se expande con swipe-up o botón flotante.

## Estilo flat — Reglas

1. **NO** cards bordeadas pesadas
2. **NO** sombras (box-shadow)
3. **NO** gradientes complejos
4. **NO** bordes gruesos (>1px)
5. **SÍ** diseño plano y limpio
6. **SÍ** separadores sutiles (1px o whitespace)
7. **SÍ** títulos de sección en azul con línea debajo

## Pitfalls

1. **Ruta relativa del CSS** — al linkar kaizen.css desde un subdirectorio, calcular bien la ruta. Desde `proyecto/visor/` hasta `kaizen-design-system/` son `../../kaizen-design-system/kaizen.css`, NO `../kaizen-design-system/kaizen.css`. Verificar con el servidor local antes de commit.
2. **Prohibido:** usar colores fuera de la paleta, cards con bordes gruesos, gradientes en fondos de componentes, mezclar estilos de otros design systems.
3. **Variables CSS** — todas las clases usan `var(--kz-*)`. Nunca hardcodear hex en CSS custom.
4. **Máximo CSS custom** — al integrar Kaizen en un proyecto, el bloque `<style>` propio debe ser <60 líneas. Lo demás lo da Kaizen.
5. **Responsive no viene con Kaizen** — El CSS base NO incluye media queries. El layout responsive (sidebar → bottom-sheet en mobile) debe implementarse en el CSS custom del proyecto. Kaizen solo da las variables y componentes.

## Fuentes

- Repo: `github.com/Ntizar/kaizen-design-system` (privado)
- CSS local: `/root/workspace/kaizen-design-system/kaizen.css`
- AGENTS.md del repo: reglas para agentes IA
