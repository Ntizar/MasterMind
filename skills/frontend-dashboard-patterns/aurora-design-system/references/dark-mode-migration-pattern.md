---
name: dark-mode-migration-pattern
description: Patrón de migración de dark mode desde body.mf-dark al sistema data-nz-theme de Aurora.
---

# Dark Mode Migration — body.mf-dark → data-nz-theme

**Fecha:** 2026-06-13
**Proyecto:** MasterFit (dieta-masterfit)
**Contexto:** Migrar dashboard existente con dark mode custom al sistema de temas de Aurora.

## Patrón de migración

### Antes (incorrecto)
```html
<body class="nz mf-dark">
```
```css
body.mf-dark { background: #0f172a; color: #e2e8f0; }
body.mf-dark .nz-card { background: rgba(30,41,59,0.85) !important; }
body.mf-dark .nz-kpi__value { color: #f1f5f9 !important; }
/* 30+ líneas de overrides con !important */
```
```js
body.classList.toggle('mf-dark');
body.classList.contains('mf-dark') ? dark : light;
```

### Después (correcto)
```html
<body class="nz" data-nz-theme="light">
```
```css
body[data-nz-theme="dark"] { background: var(--nz-c-bg); color: var(--nz-text); }
body[data-nz-theme="dark"] .nz-card { background: var(--nz-surface); border-color: var(--nz-border-medium); }
/* 15 líneas usando tokens Aurora */
```
```js
body.setAttribute('data-nz-theme', isDark ? 'light' : 'dark');
body.getAttribute('data-nz-theme') === 'dark' ? dark : light;
```

## Checklist de verificación
- [ ] `grep -c "mf-dark" archivo.html` → 0
- [ ] `grep -c "mf-toast" archivo.html` → 0
- [ ] `grep -c "mf-comida" archivo.html` → 0
- [ ] `grep -c "!important" archivo.css` → mínimo posible
- [ ] CSS custom < 30 líneas de código

## Migración de CSS custom a tokens (2026-06-13)

Patrón probado para reducir CSS custom en proyectos existentes:

1. **Eliminar `!important`** → reemplazar por tokens `var(--nz-*)`
2. **Eliminar `backdrop-filter: blur(8px)` inline** → Aurora ya lo maneja con `nz-surface--glass`
3. **Eliminar `rgba()` hardcode** → `var(--nz-surface)`, `var(--nz-border-light)`, `var(--nz-shadow-sm)`
4. **Eliminar `font-size: 0.7rem !important`** → `var(--nz-size-xs)`
5. **Eliminar `position: fixed; inset: 0` custom** → usar `nz-aurora-mesh--animated` nativo
6. **Eliminar wrapper `div.mf-content`** → usar `nz-stack nz-stack--lg` con `z-index: 1`

**Métrica de éxito:** CSS custom < 30 líneas de código (excluyendo comentarios).
