# Principios de Code Review de Google

Fuente: google/eng-practices — review/reviewer/standard.md

## El Principio de Oro

> **Aprobar una CL una vez que mejora definitivamente la code health del sistema, incluso si no es perfecta.**

Este es el principio más importante. No busques perfección — busca **mejora continua**.

## Trade-offs del Code Review

El code review equilibra dos necesidades:

1. **Los devs deben avanzar**: Si nunca envías cambios, el código nunca mejora
2. **La calidad no debe bajar**: Cada CL debe mejorar, no empeorar, la code health

## Principios Fundamentales

### 1. Datos sobre opiniones
> "Technical facts and data overrule opinions and personal preferences."

Si hay debate, usa benchmarks, métricas, o datos. No "yo creo que X es mejor".

### 2. Style guide es la autoridad
> "On matters of style, the style guide is the absolute authority."

Si el style guide no cubre algo, sigue el estilo del código existente. Si no hay estilo previo, acepta el del autor.

### 3. Diseño ≠ estilo personal
> "Aspects of software design are almost never a pure style issue."

Las decisiones de diseño se basan en principios. Si el autor demuestra que múltiples enfoques son válidos, acepta su preferencia.

### 4. Consistencia como fallback
> "If no other rule applies, be consistent with what's in the current codebase."

Si nada más aplica, sigue el estilo existente (siempre que no empeore la code health).

## Mentoring a través de Code Review

El code review es una herramienta de enseñanza:

- ✅ Dejar comentarios educativos está bien
- ✅ Compartir conocimiento mejora la code health del sistema
- Prefija comentarios educativos con "Nit:" o "Educational:" para indicar que no son obligatorios
- No bloquees una CL por un comentario educativo

## Resolviendo Conflictos

1. **Diálogo directo** developer ↔ reviewer
2. **Reunión** (cara a cara o video) si el diálogo no funciona
3. **Escalar** a Tech Lead / Maintainer / Eng Manager
4. **NUNCA** dejar una CL estancada por desacuerdo

## "Nit:" — Cuándo Usarlo

Usa "Nit:" para comentarios que son:
- Pulido cosmético (naming, spacing, formatting)
- Educativo (enseña algo nuevo pero no crítico)
- Sugerencia opcional (mejora pero no bug)

Ejemplo:
```
Nit: podrías renombrar 'data' a 'userData' para mayor claridad.
```

## Lo que NO Justifica Bloquear una CL

- Preferencias personales de estilo (si no hay style guide)
- "Lo haría diferente" (si el enfoque actual es válido)
- Código que podría mejorarse en el futuro (dejar como follow-up)
- Comentarios educativos importantes (explicar, pero no bloquear)

## Lo que SÍ Justifica Bloquear

- Bugs evidentes
- Problemas de seguridad
- Performance degradada sin compensación
- Falta de tests para funcionalidad crítica
- Breaking change sin plan de migración
- Código que empeora la code health del sistema
