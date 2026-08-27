# Human Loop — Casos Reales de Ejecución

## Caso: Migración Mastermind v3.1 → v4.0

**Contexto:** Migración de 221 archivos con 108 movidos a legacy/, 5 archivos creados, 3 actualizados.

**Human loop aplicado:** NO se aplicó porque fue una decisión del usuario ("Necesito que migres todo el proyecto"). El usuario dio permiso explícito al ejecutar la tarea completa.

**Patrón seguido:**
1. Análisis completo del sistema (skill_view + terminal)
2. Creación de SOUL.md, AGENTS.md, SKILLS-INDEX.md
3. Movimiento de legacy/ con git mv (preservando historial)
4. Commit con mensaje descriptivo
5. Push al remoto

**Lección:** Cuando el usuario dice "migra todo" o "haz la migración completa", es una decisión de arquitectura que el usuario ya aprobó implícitamente. No hay human loop necesario porque el scope está definido por el usuario.

## Cuándo SÍ aplicar human loop

| Situación | ¿Human loop? | Por qué |
|-----------|-------------|---------|
| Usuario dice "migra todo" | NO | Scope definido por usuario |
| Usuario dice "haz X" sin contexto | NO | Tarea específica y limitada |
| Usuario dice "revisa y dime qué mejorarías" | NO | Solo análisis, no ejecución |
| Cambios >5 archivos no solicitados | SÍ | El usuario no pidió esos cambios |
| Decisión de arquitectura no solicitada | SÍ | El usuario no pidió ese diseño |
| Deploy a producción no solicitado | SÍ | Impacto irreversible |

## Patrón de human loop en conversación

```
Mastermind: "📋 PLAN: [nombre]
  ARCHIVOS: [N archivos]
  CAMBIOS: [resumen]
  
  ¿Aprobado? ✅ o feedback"

Humano: "✅"

Mastermind: ejecuta...

Mastermind: "🔧 IMPLEMENTADO
  ARCHIVOS: [lista]
  RESULTADO: [qué se hizo]
  
  ¿Aprobado? ✅ o feedback"

Humano: "✅"

Mastermind: "📊 HECHO
  [resumen final]"
```
