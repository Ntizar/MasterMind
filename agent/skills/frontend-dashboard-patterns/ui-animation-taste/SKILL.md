---
name: ui-animation-taste
version: "1.0.0"
description: "Use al animar UIs: easings y sombras con buen gusto."
tags: [ui, animacion, css, diseño]
---

# UI Animation Taste — Emil Kowalski (emilkowalski/skills)

Fuente: https://github.com/emilkowalski/skills (33k+ stars). Reglas destiladas de su experiencia en Vercel y Linear, pensadas para corregir los errores típicos que cometen los agentes al diseñar interfaces.

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

## Aplicación en proyectos de David
- Complementa las preferencias del usuario: fondo blanco, sombras sutiles, hover con elevación — usar sombras difusas suaves, nunca bordes marcados.
- En dashboards (Aurora, DataHubEspaña): aplicar expo-out a entradas de paneles y gráficos, duraciones 150–250 ms.

## Pitfalls
- No usar `ease` genérico por defecto: casi siempre la elección correcta es ease-out (entrada) o ease-in (salida).
- Escalar (scale) de 0.95→1 se nota más elegante que fade puro para elementos emergentes.
- No animar el primer render de toda la página: sensación lenta. Solo elementos interactivos.

## Verificación
- Revisar una animación: ¿la dirección temporal es correcta (ease-out entra, ease-in sale)? ¿La duración es <300 ms? ¿Usa sombra en vez de borde para separar?

## Referencias
- Repo: https://github.com/emilkowalski/skills (skills/emil-design-eng/SKILL.md)
- Artículos: https://emilowal.ski/ui/7-practical-animation-tips · "Agents with Taste"

---
Hecho con ❤️ por David Antizar
