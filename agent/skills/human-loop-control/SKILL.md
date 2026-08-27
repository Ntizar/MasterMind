---
name: human-loop-control
version: "1.0.0"
description: "Sistema de control y human loop para cambios críticos — checkpoints, approval gates, y rollback."
tags: [human-loop, control, approval, safety, gates]
---

# Human Loop Control — Sistema de Control y Human Loop

## Qué es

Sistema de control que garantiza que los cambios críticos pasan por aprobación humana antes de ejecutarse. Reemplaza los checkpoints manuales del v3.1 con un patrón estructurado y reutilizable.

## Cuándo se activa

| Criterio | Umbral | Acción |
|----------|--------|--------|
| Archivos modificados | >5 archivos | Human loop obligatorio |
| Decisiones de arquitectura | Cualquiera | Human loop obligatorio |
| Deploy a producción | Cualquier deploy | Human loop obligatorio |
| Migraciones | Cualquier migración | Human loop obligatorio |
| Reestructuración | Cualquier reestructuración | Human loop obligatorio |
| Usuario lo solicita | Siempre | Human loop obligatorio |

## Patrón de Ejecución

### Fase 1: Planificar

```
Mastermind presenta:
> 📋 PLAN [NOMBRE]
> ARCHIVOS: lista de archivos a modificar
> CAMBIOS: resumen de cada cambio
> RIESGOS: posibles problemas
> ROLLBACK: cómo revertir si falla
> 
> ¿Aprobado? ✅ o feedback
```

### Fase 2: Implementar

```
Mastermind ejecuta los cambios con diffs visibles:
> 🔧 IMPLEMENTANDO [NOMBRE]
> ARCHIVO 1: cambio A → B
> ARCHIVO 2: cambio C → D
> ...
> 
> ¿Aprobado? ✅ o feedback
```

### Fase 3: Verificar

```
Mastermind verifica que todo funciona:
> ✅ VERIFICADO
> ARCHIVOS MODIFICADOS: N
> TESTS: PASS/FAIL
> BUILD: OK/FAIL
> 
> ¿Aprobado? ✅ para continuar
```

### Fase 4: Sintetizar

```
Mastermind presenta resultado final:
> 📊 RESULTADO
> HECHO: resumen
> CAMBIOS: diff final
> SIGUIENTE: próximos pasos
> 
> ¿Aprobado? ✅ para archivar
```

## Reglas

1. **Nunca silenciar** — terminar fase, presentar resultado, continuar inmediatamente
2. **Máximo 2 reintentos** — si falla 2x, escalar al humano
3. **Rollback siempre disponible** — git reset --hard si algo va mal
4. **Diffs siempre visibles** — nunca commit sin mostrar cambios
5. **Aprobación explícita** — ✅ o feedback, nunca asumir

## Implementación en Mastermind

Mastermind usa este patrón en su SOUL.md:

```markdown
## Human Loop
Cuando la tarea es crítica:
1. PLANIFICAR → presentar diffs al humano
2. ESPERAR → ✅ o feedback
3. IMPLEMENTAR → ejecutar con diffs visibles
4. ESPERAR → ✅ o feedback
5. SINTEZAR → presentar resultado
6. ESPERAR → ✅ para archivar
```

## Referencias

- **`references/execution-cases.md`** — Casos reales de human loop aplicado: cuándo se aplicó, cuándo no, patrón de conversación.

## Pitfalls

- **No omitir checkpoints** — siempre presentar resultado antes de continuar
- **No asumir aprobación** — siempre pedir ✅ explícito
- **No hacer rollback en silencio** — notificar al humano si hay que revertir
- **No sobrecargar con human loop** — tareas simples (1-3 tool calls) no lo necesitan
