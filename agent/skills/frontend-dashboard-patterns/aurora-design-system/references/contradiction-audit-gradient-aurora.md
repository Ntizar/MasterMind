# Auditoría de Contradicciones de Gradientes Aurora

**Fecha:** 2026-06-22  
**Problema:** `--nz-gradient-aurora` usaba violeta (#8b5cf6 / #7c3aed) en la skin aurora (default), creando el efecto "morado" que el usuario rechaza.

## Diagnóstico

La skin `aurora` en `ntizar.themes.css` NO redefinía `--nz-gradient-aurora`, así que heredaba de `ntizar.css` línea 159:

```css
/* ntizar.css L159 — HEREDADO por skin aurora */
--nz-gradient-aurora: linear-gradient(135deg,
  var(--nz-color-blue-500) 0%,
  var(--nz-color-violet-500) 46%,  /* ← VIOLETA */
  var(--nz-color-orange-500) 100%);
```

Esto producía: `#3b82f6 → #8b5cf6 → #f97316` (azul → violeta → naranja)

## Dónde afecta

`--nz-gradient-aurora` se usa en 7 componentes:

| Componente | Clase | Efecto visual |
|---|---|---|
| Botones blend | `nz-btn--brand-mix` | Gradiente azul→morado→naranja |
| Títulos gradient | `u-nz-text-gradient` | Texto con gradiente morado |
| Barras progreso | `nz-progress--aurora` | Barra con morado |
| Avatares | `nz-avatar--aurora` | Avatar con morado |
| Sparklines | `nz-sparkline--aurora` | Gráfico con morado |
| Fondos | `u-nz-bg-aurora` | Fondo completo |
| Mesh aurora | `nz-aurora-mesh` | Fondo decorativo |

## Contradicciones entre archivos

| Archivo | Definición | ¿Violeta? |
|---|---|---|
| `ntizar.css` L159 | blue-500 → violet-500 → orange-500 | ✅ Sí |
| `ntizar.themes.css` aurora | (hereda de ntizar.css) | ✅ Sí |
| `ntizar.themes.css` sunset | orange → pink → blue | ✅ Sí |
| `ntizar.themes.css` midnight | deep-blue → indigo → orange | ✅ Sí |
| `ntizar.themes.css` ocean | cyan → blue → orange | ❌ No |
| `ntizar.themes.css` citrus | yellow → orange → blue | ❌ No |
| `ntizar.next.css` L209 | oklch hue+50° (~290°) | ✅ Sí |
| `gallery.html` L464 | blue → violet intenso → orange | ✅ Sí |

## Solución aplicada

**Archivo:** `ntizar.themes.css`  
**Commit:** `3d2a7ba`  
**Push:** GitHub master

```css
.nz[data-nz-skin="aurora"] {
  /* Fix 2026-06-22: Sin violeta/morado. Solo azul → naranja. */
  --nz-gradient-aurora: linear-gradient(135deg,
    var(--nz-color-blue-600) 0%,
    var(--nz-color-orange-500) 100%);
}
```

Resultado: `#2563eb → #f97316` (azul → naranja directo, sin violeta)

## Lecciones

1. **Las skins deben redefinir TODO lo que quieren controlar.** No confiar en herencia para tokens visuales.
2. **Los skills de Hermes tienen información desactualizada.** El skill `aurora-design-system` mostraba ejemplos con violeta en una parte. Hay que verificar siempre contra el repo.
3. **Múltiples AGENTS.md pueden dar información contradictoria.** El repo Aurora tiene AGENTS.md, copilot-instructions.md, y el skill Hermes tiene su propia versión. Si difieren, el agente se confunde.
4. **El usuario nota los colores "raro" antes que el agente.** Cuando David dice "esto se ve morado y no me gusta", es una señal fuerte de que hay que auditar los gradientes, no ignorar la queja.

## Demo

HTML de ejemplo del look correcto: `demo-aurora-fix.html` en el repo Ntizar-Aurora.
