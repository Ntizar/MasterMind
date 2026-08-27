# Ronda 2 — Patrón de selección cuando todos están en score 9

## Contexto

En ronda 2, tras la ronda 1 de mejoras, la mayoría de temas tienen score 9 en todas las dimensiones. El criterio "scores más bajos" deja de ser útil.

## Criterio de desempate ronda 2

Cuando todos los temas tienen `avg_score >= 9`:

1. **`improvement_count` ASC** — los que tienen menos rondas de mejora primero
2. **`last_improved` más antiguo** — entre los mismos improvement_count, elegir el mejorado hace más tiempo
3. **Bloque temático** — priorizar bloques avanzados (b04-b09) sobre básicos (b01-b02)

## Ejemplo práctico (DibujoTecnico, 2026-06-15)

40 temas candidatos, todos con score 9 en todas las dimensiones:
- improvement_count=3: 12 temas → elegir por last_improved más antiguo
- improvement_count=4: 28 temas → siguiente prioridad

Temas seleccionados: b07-04 (improvement_count=3, last_improved=2026-06-13-ronda2-s1) y b04-01 (improvement_count=3, last_improved=2026-06-13-ronda2-s5).

## Progresión típica ronda 2

| Dimensión | Ronda 1 | Ronda 2 |
|-----------|---------|---------|
| svg_interactive | 7-9 | 9-10 |
| exercises | 7-9 | 9-10 |
| text_explanation | 7-9 | 9-10 |
| real_world | 7-9 | 9-10 |
| error_common | 7-9 | 9-10 |
| css_coherence | 9-10 | 10 |

Objetivo ronda 2: llevar todo a 10.
