# CSS Coherence Drift — Dibujo Técnico

**Detectado:** 2026-06-10 (Sesión 2 de mejora rápida)
**Impacto:** 42/49 temas con `css_coherence=7` en vez de 10

## Problema

Los temas generados o mejorados en sesiones anteriores terminaron con CSS custom en vez del template base. Esto no rompe la funcionalidad pero crea inconsistencia visual y hace que el score de `css_coherence` sea 7 en vez de 10.

## Patrón de Drift

Los temas con drift tienen estas 5 clases CSS modificadas respecto al template base:

### 1. `.comparison`
```css
/* DRIFT ❌ */
.comparison{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1.5rem 0}
.comparison-side{background:#f8fafc;border-radius:12px;padding:1.5rem;border:2px solid #e2e8f0;text-align:center;transition:all .3s}
.comparison-side:hover{border-color:var(--azul);box-shadow:0 4px 12px rgba(37,99,235,.1)}

/* TEMPLATE ✅ */
.comparison{display:flex;gap:1.5rem;margin:1.5rem 0;flex-wrap:wrap}
.comparison-side{flex:1;min-width:250px;text-align:center}
.comparison-side h4{margin-bottom:.5rem;font-size:.95rem}
.comparison-side.correct-side h4{color:var(--verde)}
.comparison-side.wrong-side h4{color:var(--rojo)}
```

### 2. `.step-indicator` / `.step-dot`
```css
/* DRIFT ❌ */
.step-indicator{display:flex;gap:.5rem;justify-content:center;margin:1rem 0}
.step-dot{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;color:#fff;transition:all .3s;cursor:pointer}
.step-dot:hover{transform:scale(1.2)}
.step-dot.active{box-shadow:0 0 0 4px rgba(37,99,235,.3)}

/* TEMPLATE ✅ */
.step-indicator{display:flex;gap:.5rem;margin:1rem 0;justify-content:center}
.step-dot{width:12px;height:12px;border-radius:50%;background:#e2e8f0;transition:all .3s}
.step-dot.active{background:var(--azul);transform:scale(1.3)}
```

### 3. `.real-world-badge`
```css
/* DRIFT ❌ */
.real-world-badge{display:inline-block;background:linear-gradient(135deg,var(--naranja),#ea580c);color:#fff;padding:.3rem .8rem;border-radius:20px;font-size:.8rem;font-weight:700;margin-bottom:.8rem}

/* TEMPLATE ✅ */
.real-world-badge{display:inline-block;background:var(--naranja);color:#fff;padding:.2rem .6rem;border-radius:12px;font-size:.75rem;font-weight:600;margin-bottom:.5rem}
```

### 4. `.stack-item`
```css
/* DRIFT ❌ */
.stack-item{background:#f8fafc;border:2px solid #e2e8f0;border-radius:10px;padding:1rem;margin:.5rem 0;transition:all .3s;cursor:pointer}
.stack-item:hover{border-color:var(--azul);transform:translateX(4px)}
.stack-item.active{border-color:var(--azul);background:var(--azul-claro)}

/* TEMPLATE ✅ */
.stack-item{border:2px solid var(--azul);background:#fff;border-radius:4px;display:flex;align-items:center;justify-content:center;font-weight:bold;color:var(--azul);transition:all .3s;cursor:pointer}
.stack-item:hover{transform:scale(1.05);box-shadow:0 4px 12px rgba(37,99,235,.2)}
```

### 5. `.feedback` — SIEMPRE FALTANTE
Ningún tema tiene esta clase, pero TODOS la usan en ejercicios:
```css
/* FALTA EN TODOS */
.feedback{font-size:.9rem;margin-top:.5rem;font-weight:600;padding:.4rem .8rem;border-radius:4px}
.feedback.correct{background:var(--verde-claro);color:#065f46}
.feedback.incorrect{background:var(--rojo-claro);color:#991b1b}
```

## Corrección Batch

Para corregir N temas de una vez, reemplazar el bloque de CSS custom con el template base completo.

Ver sección "Batch CSS template" en MODO RÁPIDO del SKILL.md principal.

## Temas corregidos en sesión 2 (2026-06-10)

| Tema | Estado |
|------|--------|
| b02-03-vistas-principales.html | ✅ `.feedback` añadida (CSS ya era coherente) |
| b02-05-abatimiento-ph.html | ✅ Template base + SVG interactivity toggle |
| b02-06-1o-3o-diedro.html | ✅ Template base + `.feedback` |
| b02-07-representacion-piezas.html | ✅ Template base + `.feedback` |

## Temas pendientes de corrección

Todos los temas con `css_coherence=7` que no sean los 4 corregidos arriba.

## Notas

- El drift se introduce probablemente por un generador o script intermedio que usaba CSS custom
- No afecta funcionalidad, solo consistencia visual y score de calidad
- La corrección es 100% segura: las clases template base ya se usan en los HTMLs, solo falta definir su CSS
