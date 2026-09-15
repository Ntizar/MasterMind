---
name: wow-clean-design
description: "Úsalo si un diseño limpio queda plano: falta el wow."
version: "1.1.0"
author: Mastermind (agente de David Antizar)
license: MIT
metadata:
  hermes:
    tags: [diseno, ui, wow, design-system, antidrift]
    related_skills: [aurora-design-system, ui-animation-taste]
---

# Wow en diseño limpio — el patrón anti "demasiado igual"

## When to Use

- David percibe un entregable "limpio" como plano: dice "sin wow", "demasiado igual", "todo igual", "sin alma".
- Al construir design systems, catálogos de componentes, landings o dashboards con restricciones estrictas (sin gradientes/glass): evitar la uniformidad.
- NO aplicarlo en presentaciones corporativas/consulting — allí el blanco sobrio ES el objetivo.

## El problema (caso Aurora 7, 2026-09-08)

Al aplicar reglas anti-slop (sin gradientes, sin glass, sin orbs, sin bordes decorativos), el agente sobre-corrigió: entregó 20 tarjetas grises idénticas, sin jerarquía, sin movimiento, sin interacción. David: *"está limpio, pero ha perdido el efecto wow... ¿no es todo demasiado igual?"*.

**Lección central:** las reglas anti-slop definen qué QUITAR (decoración), no qué AÑADIR. Cumplirlas todas puede producir salida plana y uniforme. El wow NO se recupera violando prohibiciones — viene por vías que no son decoración.

## Test de control (antes de entregar cualquier diseño "limpio")

> Si el entregable cumple TODAS las prohibiciones pero dos pantallas son intercambiables entre sí, está MAL.

- Prohibido = decoración (gradientes, glass, orbs, bordes decorativos, líneas horizontales).
- Esperado = movimiento, jerarquía, interacción. La contención nunca es excusa para la uniformidad.

## Las 5 vías del wow (receta validada y aprobada por David)

1. **Momento firma** — UNA interacción memorable por página. Validado: constelación en canvas de fondo (puntos azules que se tejen con líneas de proximidad, chispas naranjas, explosión de partículas al clic). Contención intacta: el canvas es FONDO (DOM encima), DPR ≤ 2, pausa en `visibilitychange`, `prefers-reduced-motion` = renderizar UN fotograma estático (nunca canvas vacío).
2. **Jerarquía de escenarios** — hero display + manifiesto + grid con UNA celda destacada (wide) y el resto atenuado. NUNCA una lista plana de tarjetas iguales.
3. **Hover con elevación** — translateY(-3px) + sombra que sube de nivel + detalles (flechas) que aparecen SOLO en hover.
4. **Entradas escalonadas** — expo-out ≤ 300 ms con delay por elemento (variable CSS `--d`). Fill `backwards`, NUNCA `both` (ver pitfall abajo).
5. **Demos vivas** — componentes que responden de verdad: split pane arrastrable (pointer capture), botón que cicla estados, contadores animados, switches funcionales.

## Pitfall de cascada: fill backwards vs both

Las animaciones de entrada con fill `both`/`forwards` mantienen el transform final del keyframe tras terminar y BLOQUEAN las transiciones de hover sobre transform (las animations ganan a las transitions en la cascada CSS). Patrón correcto:

```css
.nz-in { animation: nzIn .3s var(--ease-out) backwards; animation-delay: var(--d, 0s); }
@keyframes nzIn { from { opacity: 0; transform: translateY(10px); } }
```

Al acabar, el elemento vuelve a su estado natural y el hover funciona.

## Paleta reactiva al tema

Si hay efecto canvas y toggle light/dark: leer el tema activo (atributo en `<html>`) en CADA frame, no cachearlo al iniciar — así el fondo reacciona al toggle sin recargar.

## Cuándo aplicar

- David pide "diseño limpio/elegante" Y el resultado queda plano → añadir vías 1–5.
- Design systems nuevos o versiones mayores (v6→v7) → momento firma + jerarquía desde el día 1.
- NO aplicar en presentaciones corporativas/consulting (ahí el blanco sobrio ES el objetivo).

## Referencias

- `references/aurora-7-wow-pattern.md` — receta completa validada: arquitectura Aurora 7 (tokens.css + packs + páginas), shell del catálogo con clases, recipe JS de la constelación, decisiones del usuario (dark día 1, cero glass total).
