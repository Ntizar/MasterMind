# Checklist: Qué buscar en Code Review

Fuente: google/eng-practices — review/reviewer/looking-for.md

## Checklist de Code Review (Google Standard)

Cuando revises código, verifica estas 8 áreas:

### 1. ✅ Diseño
- ¿El código está bien diseñado para el sistema?
- ¿La arquitectura es apropiada o over-engineered?
- ¿Se sigue el principio de responsabilidad única?

### 2. ✅ Funcionalidad
- ¿El código se comporta como se esperaba?
- ¿Cubre los casos edge?
- ¿Es bueno para los usuarios finales?

### 3. ✅ Complejidad
- ¿Se puede simplificar?
- ¿Otro desarrollador lo entendería en 6 meses?
- ¿Hay lógica redundante?

### 4. ✅ Tests
- ¿Hay tests automáticos?
- ¿Cubren los casos críticos?
- ¿Los tests son claros y mantenibles?
- ¿Hay tests para los edge cases?

### 5. ✅ Naming
- Nombres de variables claros y descriptivos
- Nombres de clases que reflejen su rol
- Nombres de métodos que indiquen acción

### 6. ✅ Comentarios
- ¿Explican el "por qué", no el "qué"?
- ¿Hay docstrings en funciones públicas?
- ¿Los comentarios están actualizados?

### 7. ✅ Estilo
- ¿Sigue el style guide del proyecto?
- ¿Consistente con el código existente?
- ¿Sin código muerto?

### 8. ✅ Documentación
- ¿Se actualizaron los docs relevantes?
- ¿Hay CHANGELOG entry si es breaking change?
- ¿README actualizado si hay cambios de API?

## Principio de Oro de Google

> **Aprobar una CL una vez que mejora definitivamente la code health del sistema, incluso si no es perfecta.**

No busques perfección. Busca **mejora continua**. Si algo es solo un "nit" (pulido menor), marca el comentario como "Nit:" para que el autor sepa que es opcional.

## Resolviendo Conflictos

1. Primero: diálogo directo developer ↔ reviewer
2. Si no: reunión cara a cara / video call
3. Si no: escalar a Tech Lead / Maintainer / Eng Manager
4. **Nunca dejes una CL estancada por desacuerdo**

## Ejemplos de Comentarios Útiles

```
✅ BUENO: "Considera extraer esta lógica en una función separada.
          La función actual tiene 80 líneas y hace 3 cosas distintas."

✅ BUENO: "Nit: podrías renombrar 'x' a 'userCount' para claridad."

✅ BUENO: "¿Hay tests para el caso donde el usuario no existe?
          Creo que fallaría silenciosamente."

❌ MALO: "No me gusta este nombre."
❌ MALO: "Cambia esto a como lo haría yo."
❌ MALO: "Esto está mal." (sin explicación)
```

## Cuándo NO Aprobar

- El código empeora la code health del sistema
- No hay tests para funcionalidad crítica
- Hay bugs evidentes
- Breaking change sin migración planificada
- Seguridad comprometida (SQL injection, XSS, etc.)

## Cuándo SÍ Aprobar (aunque tenga issues menores)

- El código mejora la code health general
- Los issues menores se pueden tratar en follow-up CLs
- El autor explica por qué eligió un enfoque sobre otro
- Hay tests para la funcionalidad principal
