---
name: ui-animation-taste
version: "1.1.0"
description: "Use al animar UIs: easings, sombras y efectos GPU con buen gusto."
tags: [ui, animacion, css, shader, diseño]
---

# UI Animation Taste — Emil Kowalski (emilkowalski/skills)

Fuente: https://github.com/emilkowalski/skills (33k+ stars). Reglas destiladas de su experiencia en Vercel y Linear, pensadas para corregir los errores típicos que cometen los agentes al diseñar interfaces. Complemento GPU: v2space-labs/shader-for-interfaces (consultado 2026-09-01).

## Reglas clave

### Easing (el error #1 de los agentes)
- **Animaciones de ENTRADA (enter/aparecer):** `ease-out` — arranca rápido, desacelera. `cubic-bezier(0.16, 1, 0.3, 1)` (expo-out) es el estándar de calidad.
- **Animaciones de SALIDA (exit/desaparecer):** `ease-in` — arranca lento, acelera al salir.
- El fallo clásico de IA: usar `ease-in` en entradas. Se percibe "raro" aunque no se sepa explicar por qué.
- Interacciones dirigidas por el usuario (drag, seguimiento de cursor): `ease-out` suave o casi lineal.

### Duraciones
- Microinteracciones (hover, toggles): 100–200 ms.
- Elementos que aparecen (toasts, modales, dropdowns): 150–300 ms.
- NUNCA animar con la misma duración entrada y salida — la salida suele ser más corta.

### Sombras vs bordes
- Para separar elementos: prefiere **sombras semi-transparentes** sobre bordes sólidos (`border: 1px solid` grita "hecho por IA").
- Capas de sombra (shadow stacking) para profundidad realista: sombra pequeña nítida + sombra grande difusa.

### Transiciones y percepción
- Optimistic UI: aplicar el cambio al instante y revertir si falla, no esperar al servidor.
- Animar solo `transform` y `opacity` (composite). Evitar animar `width/height/top/left` (layout).
- `prefers-reduced-motion`: respetarlo siempre.
- Los toasts deben pausar su countdown al hacer hover; los diálogos, cerrarse con la misma transición inversa.

## Efectos GPU en interfaces de producto (regla de contención)

Aprendido de shader-for-interfaces (skill agentivo MIT para efectos GPU en UI) y coherente con la corrección de David en GlamourSurf:

- **Un shader es fondo, nunca interfaz**: todo el texto, controles y focus ring viven en el DOM; el canvas va detrás con `pointer-events: none`. El shader no sustituye componentes de UI.
- **Efecto enfocado**: un solo efecto por zona (header, hero), no una escena 3D completa donde basta un ripple. Escalera de renderer: CSS → SVG → Canvas 2D → WebGL/Three.js → WebGPU/WGSL; subir de nivel solo cuando la decisión de renderer lo justifique (complejidad visual, densidad de partículas, datos por GPU).
- **Reduced motion = uTime congelado**, no animación "más lenta": el fallback debe ser estático y legible (evita capturas headless que parecen rotas).
- **Rendimiento**: un solo requestAnimationFrame compartido, DPR limitado (≤2), detener el loop con `IntersectionObserver` cuando el efecto sale del viewport.
- **Verificación real**: capturar la página en desktop y móvil antes de dar el efecto por bueno — nunca declarar validado un shader sin verlo renderizado.

## Aplicación en proyectos de David
- Complementa las preferencias del usuario: fondo blanco, sombras sutiles, hover con elevación — usar sombras difusas suaves, nunca bordes marcados.
- En dashboards (Aurora, DataHubEspaña): aplicar expo-out a entradas de paneles y gráficos, duraciones 150–250 ms.
- En landings de marca con shader (ver `creative/brand-shader-landing`): aplicar la regla de contención — arte vivo sí, pero DOM por encima y reduced motion obligatorio.

## Pitfalls
- No usar `ease` genérico por defecto: casi siempre la elección correcta es ease-out (entrada) o ease-in (salida).
- Escalar (scale) de 0.95→1 se nota más elegante que fade puro para elementos emergentes.
- No animar el primer render de toda la página: sensación lenta. Solo elementos interactivos.
- No meter WebGL para lo que resuelve una `transition` CSS: cada contexto GPU cuesta memoria y batería en móvil.

## Verificación
- Revisar una animación: ¿la dirección temporal es correcta (ease-out entra, ease-in sale)? ¿La duración es <300 ms? ¿Usa sombra en vez de borde para separar?
- Revisar un efecto GPU: ¿el texto y los controles siguen en el DOM? ¿`prefers-reduced-motion` congela el shader? ¿El loop se detiene fuera de viewport? ¿Verificado en página real desktop + móvil?
