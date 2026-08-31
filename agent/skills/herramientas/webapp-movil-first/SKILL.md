---
name: webapp-movil-first
version: "1.0.0"
description: "Use al crear una tool HTML interactiva: táctil-first."
tags: [html, movil-first, tactil, svg, pointer-events, diseño, bottom-sheet, pan-zoom]
---

# WebApp Móvil-First — Patrón obligatorio para tools HTML interactivas

## Lección de origen

Kaizen Procesos v1 se construyó desktop-only (3 columnas, panel lateral, drag fino de ratón). David la probó **en el móvil** y su veredicto fue: *"la versión móvil es bastante basura como está planteada, no es intuitiva"* — y de paso corrigió la paleta: *¿ya no pones color naranja a los proyectos? Es azul y naranja*.

Regla resultante: **toda tool HTML interactiva se diseña táctil-first desde la primera línea**, y el layout de escritorio se añade después con un único media query. Nunca al revés.

## Paleta de color obligatoria

- Azul primario: `#2563eb`
- **Naranja de acento: `#f97316`** — CTA/botón principal, pestaña activa secundaria, KPI de mejora, puntos de conexión en SVG, estados seleccionados.
- Nunca solo azul. Fondo blanco, sombras sutiles, hover/tap con elevación.
- ⚠️ NO confundir con la regla de Aurora v6.1 (titulares azul sólido, donde David rechaza azul→naranja). Esa regla es SOLO para el design system Aurora. Para tools y proyectos normales: azul + naranja.

## Checklist táctil (aplicar siempre)

| Elemento | Regla |
|---|---|
| Botones | mínimo 44×44px |
| Inputs | `font-size: 16px` (evita auto-zoom iOS) |
| Puntos de conexión SVG | `r=10`, borde blanco, + tolerancia de soltado ~16px |
| Zona clicable de flechas/paths SVG | stroke transparente de 20px |
| Paleta/herramientas | chips horizontales scrollables arriba (no columna lateral) |
| Panel de propiedades | bottom-sheet fijo abajo que sube al seleccionar |
| Menú secundario | ☰ → hoja inferior modal |
| Viewport | `user-scalable=no` + `theme-color` |
| Altura | `100dvh` (no `100vh`, que falla con la barra del móvil) |

## Lienzos SVG interactivos (pan + pinch + drag)

Usar **Pointer Events** para que el mismo código sirva a ratón y dedo:

1. `touch-action: none` en el SVG
2. Capas envueltas en `<g id="camara">`; cámara aplicada con `translate(x,y) scale(k)`
3. **Pan con 1 dedo**: map de `pointerId → {x,y}`; en `pointermove` sumar delta a la cámara
4. **Pinch con 2 dedos**: calcular distancia entre los dos pointers, escalar cámara centrando en el punto medio de los dedos, clamp `k` entre 0.4 y 2.5
5. Drag de nodos: `pointerdown` en el nodo → listeners en `document` (no en el SVG) para `pointermove`/`pointerup`/`pointercancel`
6. Al soltar una conexión creada por drag, **abrir automáticamente el panel de propiedades** del elemento creado (ahorra un tap)

```javascript
function puntoMundo(e) {
  const r = svg.getBoundingClientRect();
  return { x: (e.clientX - r.left - vista.x) / vista.k,
           y: (e.clientY - r.top - vista.y) / vista.k };
}
```

## Bottom-sheet de propiedades

```css
.panel-props {
  position: fixed; left: 0; right: 0; bottom: 0; z-index: 30;
  background: #fff; border-radius: 20px 20px 0 0;
  box-shadow: 0 -8px 30px rgba(0,0,0,.18);
  transform: translateY(110%); transition: transform .25s ease;
  max-height: 55dvh; overflow-y: auto;
}
.panel-props.abierto { transform: translateY(0); }
```

En escritorio (`@media (min-width: 900px)`) el mismo elemento pasa a `position: static` como panel lateral — un solo markup, dos layouts.

## Escritorio después: un solo media query

Todo el layout de 3 columnas (paleta lateral, panel estático, hover states) vive dentro de `@media (min-width: 900px)`. Ocultar ahí lo móvil-only (botón ☰, toast de ayuda) con `display: none !important`.

## Verificación

- [ ] ¿Se puede dibujar/editar todo con un pulgar, una mano?
- [ ] ¿Los inputs abren el teclado sin zoom de página?
- [ ] ¿Pan/pinch del lienzo no dispara drags accidentales de nodos?
- [ ] ¿Primera visita muestra ayuda breve (toast) que se puede cerrar?
- [ ] ¿En escritorio >900px se recupera el layout completo?

## Referencias

- Ejemplo aplicado completo (v2 final): repo `~/Projects/kaizen-procesos` — `css/styles.css`, `js/canvas.js` (initPanZoom), `js/ui.js` (renderPanel bottom-sheet)
- Skill relacionada: `ui-animation-taste` (easings y sombras), `browser-local-tools` (zero-install, embebido CDN)

---

Hecho con ❤️ por David Antizar
