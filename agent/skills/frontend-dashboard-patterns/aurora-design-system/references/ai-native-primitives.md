# Primitivas AI-native — pack `ntizar.ai.css` (v6.2)

Fuente de inspiración: **Beautiful UI** (beautifului.dev) — primitivas para interfaces AI-native (chat, agentes, dashboards de datos). Adaptadas al lenguaje de Aurora: **Núcleo limpio** (sólido, compacto, sin gradientes azul→naranja), **monocromo azul**, **light por defecto** con soporte `data-nz-theme="dark"`, **mobile-first**, touch targets 44px en controles interactivos, tokens `--nz-*`.

## CDN

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.ai.css">
```

Depende de `ntizar.css`. Complementa `ntizar.data.css`, `ntizar.ui.css`, `ntizar.motion.css`.

## Los 20 primitivos

| # | Componente | Clases | Cuándo usarlo |
|---|---|---|---|
| 01 | Loading State | `.nz-loader[--pixel\|--dots\|--orbit\|--surfer\|--sweep]` + `.nz-loader__time` | Cargas de datos / análisis; elapsed time en mono tabular |
| 02 | Thinking | `.nz-thinking[.is-open]` + `__toggle/__label/__body/__traces/__tabs/__trace[--reasoning\|--search\|--coding]` | Trazas de agente expandibles |
| 03 | Streaming | `.nz-stream` + `__text/__source/__actions/__followups/__caret` | Respuestas en streaming con fuentes y acciones |
| 04 | Approval | `.nz-approval[.is-open]` + `__question/__sub/__entity/__pill/__options/__option/__actions/__meta` | Human-in-the-loop |
| 05 | Tool Chips | `.nz-toolchips[.is-open]` + `.nz-toolchip[--edit\|--ok]` + `__icon/__label` | Llamadas a tool / ediciones como chips |
| 06 | Task Rows | `.nz-taskrow[--completed\|--running\|--failed\|--pending][.is-open]` + `__icon/__label/__count/__status/__detail/__metric` | Estado de tareas de agente |
| 07 | Chat | `.nz-chat` + `__tabs/__tab[.is-active]/__thread/__msg[--user\|--agent]/__bubble/__composer/__send` | Paneles de chat |
| 08 | Prompt Bar | `.nz-promptbar` + `__box/__field/__send/__bar/__chips/__chip[--command]/__model` | Composer con @sources, /comandos, model picker |
| 09 | Recommendation | `.nz-recommend[.is-open]` + `__title/__sub/__entity/__pill/__options/__option/__confidence/__footer` | Sugerencia con confidence meter |
| 10 | Context Cards | `.nz-contextcard` + `__head/__name/__chars/__body/__source` | Chunks recuperados con fuente |
| 11 | Diff Table | `.nz-difftable` + `__title/__table/__cell--add/--del/--change/__diff-glyph` | Ediciones propuestas por IA |
| 12 | Records Table | `.nz-recordtable` + `__table/__name/__tag[--brand\|--accent]/__strength[--strong\|--weak\|--none]` | Grid CRM con tags y relación |
| 13 | Filter Table | `.nz-filtertable` + `__chip[.is-active]/__table/__status[--todo\|--progress\|--done]` | Chips de estado que reorganizan datos |
| 14 | Sidebar Nav | `.nz-sidenav[.is-collapsed]` + `__section/__label/__item[.is-active]/__icon/__text/__badge` | Nav de workspace colapsable |
| 15 | Search | `.nz-command` + `__input-row/__input/__list/__item[.is-active]/__item-group/__empty` | Command palette |
| 16 | Flowchart | `.nz-flow` + `__step[--trigger\|--condition]/__connector/__branch/__branch-item` | Workflows trigger/condición |
| 17 | Insight Cards | `.nz-insight` + `__head/__pager/__text/__stat/__chart/__bar[--brand\|--accent]/__toggle` | Insights paginados con charts |
| 18 | Code Block + Diff | `.nz-codeblock[--lines\|--diff]` + `__line[--add\|--del]/__diff-glyph[--add\|--del]` | Listing con números de línea y diff |
| 19 | Fine-tune Card | `.nz-finetune` + `__head/__title/__adjust/__row/__row-icon/__control` | Inspector de propiedades |
| 20 | Selection Actions | `.nz-selection` + `__highlight/__bar/__bar-btn[--primary]/__bar-label` | Seleccionar pasaje → reescribir |

## Patrones de markup

### Colapsables (thinking, approval, toolchips, taskrow, recommend)

Usan animación `grid-template-rows` + `.is-open` (JS togglea la clase):

```html
<div class="nz-thinking is-open">
  <button class="nz-thinking__toggle" onclick="this.closest('.nz-thinking').classList.toggle('is-open')">
    <svg class="nz-thinking__spark">…</svg>
    <span class="nz-thinking__label">Pensando</span>
    <svg class="nz-thinking__chevron">…</svg>
  </button>
  <div class="nz-thinking__body"><div class="nz-thinking__inner">
    <div class="nz-thinking__traces">…</div>
  </div></div>
</div>
```

El chevron rota con `.is-open` (regla CSS). Los traces y pestañas son estáticos — no se shippea JS.

### Estado de color (semántico, no de marca)

Usa el sistema de estado de Aurora (`--nz-status-{success,danger,warning,info}-{soft,border,text}`) y `--nz-surface-{success,danger,warning,info}-soft`. **Nunca** mezclar azul y naranja como protagonistas simultáneos (regla de acento de AGENTS.md).

### Touch targets

Los toggles principales (`.nz-thinking__toggle`, `.nz-taskrow__toggle`, `.nz-toolchips__toggle`, `.nz-command__input-row`) tienen `min-height:44px`. Los chips/acciones secundarios (`.nz-toolchip`, `.nz-stream__action`) son compactos (34px) — usar solo en contexto denso; si son acciones principales, subir a 44px.

## Verificación

- `demo-ai.html` (raíz del repo) muestra los 20 primitivos en una grid.
- `gallery.html` sección `#pack-ai` muestra los representativos.
- Regla: si un componente no está en la galería, no existe en la API pública.
