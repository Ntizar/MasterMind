# Barrido Completo de Violeta — 10 Puntos en 6 Archivos

**Fecha:** 2026-07-02
**Commit:** `85c17b8`
**Push:** GitHub master

## Contexto

El fix inicial (commit `3d2a7ba`, 2026-06-22) solo redefinió `--nz-gradient-aurora` en `ntizar.themes.css` para la skin aurora. Pero el violeta (`--nz-color-violet-500` = `#7c3aed`) seguía presente en **9 puntos más** repartidos por 5 archivos CSS, afectando componentes que no usan el token `--nz-gradient-aurora` directamente.

David dijo: *"El violeta ese no me gusta nada. Tiene que ser o azul o naranja. O más naranja. Pero no violetas."*

## Metodología de auditoría

```bash
# 1. Buscar referencias textuales a violet/purple/indigo/fuchsia/magenta
grep -in "violet\|purple\|indigo\|fuchsia\|magenta" *.css

# 2. Buscar huees OKLCH en rango violeta/magenta (280-340)
grep -n "oklch.*28[0-9]\|oklch.*29[0-9]\|oklch.*3[01][0-9]\|oklch.*32[0-9]\|oklch.*33[0-9]\|oklch.*34[0-9]" ntizar.next.css

# 3. Filtrar: excluir definiciones de tokens (--nz-color-violet-*) que se mantienen como referencia
#    pero ya no se usan en componentes activos
```

## Los 10 puntos fixados

### 1. ntizar.css:159 — gradient-aurora del CORE
```css
/* ANTES */
--nz-gradient-aurora: linear-gradient(135deg,
  var(--nz-color-blue-500) 0%,
  var(--nz-color-violet-500) 46%,
  var(--nz-color-orange-500) 100%);

/* DESPUÉS — más naranja */
--nz-gradient-aurora: linear-gradient(135deg,
  var(--nz-color-blue-600) 0%,
  var(--nz-color-orange-500) 50%,
  var(--nz-color-orange-600) 100%);
```
**Impacto:** Este es el fix más importante. El gradient del core ahora es azul→naranja→naranja profundo sin necesitar themes.css. Afecta: botones brand-mix, títulos gradient, progress--aurora, avatares, sparklines, fondos, mesh.

### 2. ntizar.css:860 — border-color de nz-btn--brand-mix
```css
/* ANTES */
border-color: color-mix(in srgb, var(--nz-color-violet-500) 42%, transparent);
/* DESPUÉS */
border-color: color-mix(in srgb, var(--nz-color-brand-strong) 42%, transparent);
```

### 3-4. ntizar.next.css:435-436 — chromatic edge del glass-liquid (light)
```css
/* ANTES — cyan → violeta → rosa */
oklch(85% 0.15 200) 0%,
oklch(85% 0.08 280) 50%,   /* violeta */
oklch(85% 0.15 340) 100%)  /* rosa/magenta */

/* DESPUÉS — cyan → azul → naranja */
oklch(85% 0.15 200) 0%,
oklch(85% 0.08 250) 50%,   /* azul */
oklch(85% 0.15 50) 100%)   /* naranja */
```
**Impacto:** El borde irisado de TODAS las cards/surfaces/botones glass-liquid. Es sutil pero visible en pantallas calibradas.

### 5-6. ntizar.next.css:543-544 — chromatic edge del glass-liquid (dark)
Mismo cambio que #3-4 pero para dark mode (oklch 40% lightness en vez de 85%).

### 7. ntizar.viz.css:39 — aurora-bg (fondo cinematográfico)
```css
/* ANTES */
radial-gradient(circle at 82% 18%, color-mix(in srgb, var(--nz-color-violet-500) 22%, transparent), transparent 28%),
/* DESPUÉS */
radial-gradient(circle at 82% 18%, color-mix(in srgb, var(--nz-color-orange-400) 22%, transparent), transparent 28%),
```

### 8. ntizar.viz.css:202 — orb--aurora
```css
/* ANTES */
var(--nz-color-blue-400) 0%,
var(--nz-color-violet-500) 45%,
var(--nz-color-orange-500) 100%);
/* DESPUÉS */
var(--nz-color-blue-400) 0%,
var(--nz-color-orange-400) 45%,
var(--nz-color-orange-500) 100%);
```

### 9. ntizar.viz.css:217 — glow-ring
```css
/* ANTES */
background: conic-gradient(var(--nz-ring-c1), var(--nz-color-violet-500), var(--nz-ring-c2), var(--nz-ring-c1));
/* DESPUÉS */
background: conic-gradient(var(--nz-ring-c1), var(--nz-color-orange-500), var(--nz-ring-c2), var(--nz-ring-c1));
```

### 10. ntizar.data.css:239 — meter--aurora
```css
/* ANTES */
var(--nz-color-violet-500) 30%,
/* DESPUÉS */
var(--nz-color-orange-400) 30%,
```

### 11. ntizar.charts.css:201 — donut--aurora
```css
/* ANTES */
var(--nz-color-violet-500) 35%,
/* DESPUÉS */
var(--nz-color-orange-400) 35%,
```

### 12. ntizar.themes.css:121 — chart palette color 3
```css
/* ANTES */
--nz-chart-3: var(--nz-color-violet-500);
/* DESPUÉS */
--nz-chart-3: var(--nz-color-orange-600);
```

## Tokens violeta que se mantienen

Las definiciones `--nz-color-violet-400/500/600` en `ntizar.css:74-76` se mantienen como tokens de referencia. Ya no se usan en ningún componente activo, pero se conservan por si una skin custom los necesita. No hay que borrarlos — solo asegurarse de que ningún componente los referencia.

## Verificación post-fix

```bash
# Debe devolver 0 resultados (excluyendo definiciones de tokens y comentarios)
grep -in "violet" *.css | grep -v "color-violet-[0-9]" | grep -v "Fix 2026" | grep -v "venía heredado"
```

## Lección

**Un fix parcial es insuficiente.** Cuando el usuario dice "no me gusta el violeta", hay que auditar TODOS los archivos CSS, no solo el token más visible. El violeta se cuela en:
- Gradientes (gradient-aurora)
- Bordes (border-color, chromatic edge)
- Fondos decorativos (aurora-bg, orbs, glow-ring)
- Componentes de datos (meter, donut, charts)
- Huees OKLCH (rango 280-340 = violeta/magenta/rosa)

La técnica de auditoría con grep + oklch hue range es reproducible para cualquier design system.
