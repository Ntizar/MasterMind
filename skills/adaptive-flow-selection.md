---
name: adaptive-flow-selection
description: Patrón de selección de flujo adaptativo basado en complejidad de la tarea. 3 niveles (corto/medio/largo) con agentes específicos para cada nivel, garantizando eficiencia sin sacrificar calidad.
version: 1.0.0
author: Ntizar Brain
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [flujo-adaptativo, complejidad, selección, eficiencia, calidad]
---

# Patrón de Flujo Adaptativo Basado en Complejidad

## Qué es

Patrón de selección de flujo que determina qué secuencia de agentes ejecutar según la complejidad estimada de la tarea. El clasificador evalúa la tarea al inicio y asigna un nivel de complejidad (1-5), que mapea a uno de 3 flujos: corto, medio o largo.

### Niveles de complejidad

| Complejidad | Descripción | Ejemplo |
|-------------|-------------|---------|
| 1 | Tarea trivial, un archivo, sin dependencias | Cambiar un color en un componente |
| 2 | Tarea simple, 1-2 archivos, sin análisis previo | Corregir un bug conocido |
| 3 | Tarea moderada, requiere contexto o planificación | Implementar una nueva funcionalidad |
| 4 | Tarea compleja, múltiples archivos, decisiones de diseño | Crear un nuevo módulo con arquitectura |
| 5 | Tarea crítica, alto riesgo, múltiples stakeholders | Migrar base de datos, refactorizar núcleo |

### Los 3 flujos

```
FLUJO CORTO (complejidad 1-2):
  ORCH → CLASSIFY → IMPLEMENT → REVIEW → SYNTHESIZE

FLUJO MEDIO (complejidad 3):
  ORCH → CLASSIFY → EXPLORE → PLAN → IMPLEMENT → REVIEW → SYNTHESIZE → ARCHIVE

FLUJO LARGO (complejidad 4-5):
  ORCH → CLASSIFY → EXPLORE → PLAN → SPEC → IMPLEMENT → REVIEW → CRITICIZE → SYNTHESIZE → ARCHIVE
```

### ¿Por qué 3 flujos y no uno solo?

Un flujo único para todo es ineficiente: las tareas simples se sobrecuestan con agentes innecesarios, y las complejas se subestiman con agentes faltantes. Los 3 flujos equilibran **cobertura** y **eficiencia**.

## Cuándo usar

- **Siempre:** Cada tarea nueva pasa por el clasificador para determinar el flujo.
- **En la fase CLASSIFY:** El orchestrator evalúa complejidad y selecciona el flujo.
- **Si la tarea cambia de naturaleza:** Re-clasificar y ajustar el flujo en curso.
- **NUNCA:** Saltar un agente del flujo seleccionado, incluso si parece innecesario.

## Pasos

### Paso 1 — Clasificar la tarea

```
1. El orchestrator recibe la tarea del humano
2. Evalúa: número de archivos implicados, dependencias, riesgo, novedad
3. Asigna complejidad 1-5
4. Selecciona el flujo correspondiente
```

### Paso 2 — Ejecutar el flujo seleccionado

```
FLUJO CORTO:
  1. CLASSIFY → confirma modelo y flujo
  2. IMPLEMENT → implementa directamente
  3. REVIEW → valida la implementación
  4. SYNTHESIZE → comunica resultado

FLUJO MEDIO:
  1. CLASSIFY → confirma modelo y flujo
  2. EXPLORE → analiza contexto del repositorio
  3. PLAN → diseña estrategia y pasos
  4. IMPLEMENT → ejecuta el plan
  5. REVIEW → valida la implementación
  6. SYNTHESIZE → comunica resultado
  7. ARCHIVE → destila aprendizaje

FLUJO LARGO:
  1. CLASSIFY → confirma modelo y flujo
  2. EXPLORE → analiza contexto del repositorio
  3. PLAN → diseña estrategia y pasos
  4. SPEC → genera especificación ejecutable
  5. IMPLEMENT → ejecuta la spec
  6. REVIEW → valida la implementación
  7. CRITICIZE → revisión adversarial
  8. SYNTHESIZE → comunica resultado
  9. ARCHIVE → destila aprendizaje
```

### Paso 3 — Checkpoints humanos en los puntos correctos

```
FLUJO CORTO:
  - Después de CLASSIFY (confirmar modelo)
  - Después de REVIEW (aprobar con ✅)

FLUJO MEDIO:
  - Después de CLASSIFY (confirmar modelo)
  - Después de PLAN (aprobar estrategia)
  - Después de REVIEW (aprobar con ✅)

FLUJO LARGO:
  - Después de CLASSIFY (confirmar modelo)
  - Después de PLAN (aprobar estrategia)
  - Después de SPEC (aprobar especificación)
  - Después de REVIEW (aprobar con ✅)
  - Después de CRITICIZE (considerar recomendaciones)
```

### Paso 4 — Re-clasificar si la tarea cambia

```
Si durante la ejecución se descubre que la tarea es más compleja de lo estimado:
  1. El orchestrator re-clasifica
  2. Sube al flujo correspondiente
  3. Añade los agentes faltantes al flujo
  4. Comunica el cambio al humano
```

## Regla de PASS SIN HALLAZGOS

**Ningún agente se salta del flujo, aunque emita "PASS SIN HALLAZGOS".**

Cada agente debe:
1. Ejecutar su fase completa
2. Emitir su reporte estructurado
3. Si no encuentra problemas, emitir: `RESULTADO: PASS | MOTIVO: SIN HALLAZGOS | DETALLE: [por qué no hay hallazgos]`

### Ejemplo de PASS SIN HALLAZGOS

```
REVIEWER REPORT
──────────────
TAREA_REVISADA: Implementar botón de exportar PDF
CRITERIOS:
  ✅ Funcionalidad implementada correctamente
  ✅ Manejo de errores incluido
  ✅ Pruebas realizadas y pasando
RESULTADO: PASS
MOTIVO: SIN HALLAZGOS
DETALLE: La implementación cumple todos los criterios de la spec v1.
```

**Esta regla es innegociable.** Un agente que se salta la fase introduce un punto ciego en el flujo.

## Pitfalls

| Pitfall | Síntoma | Solución |
|---------|---------|----------|
| Subestimar complejidad | Flujo corto para tarea compleja | Re-clasificar al primer síntoma de problema |
| Sobreestimar complejidad | Flujo largo para tarea simple | Ineficiencia, pero no pérdida de calidad |
| Agente saltado | Flujo incompleto en el log | Verificar regla de PASS SIN HALLAZGOS |
| No re-clasificar | Flujo incorrecto durante ejecución | Re-clasificar si se descubre complejidad oculta |
| Checkpoints faltantes | Humano no sabe el estado | Incluir checkpoint en cada punto de decisión |
| ARCHIVE omitido | No se acumula conocimiento | ARCHIVE siempre en flujos medio y largo |

## Verificación

Para verificar que el flujo adaptativo se ejecuta correctamente:

1. **Complejidad asignada:** El orchestrator reporta la complejidad (1-5) y el flujo seleccionado.
2. **Agentes ejecutados:** Cada agente del flujo aparece en el log de ejecución.
3. **Regla PASS SIN HALLAZGOS:** Ningún agente fue omitido; cada uno emitió su reporte.
4. **Checkpoints humanos:** Cada punto de decisión humano está presente en el log.
5. **Re-clasificación:** Si la complejidad cambió, hay un registro de re-clasificación.
6. **ARCHIVE presente:** En flujos medio y largo, el archiver ejecutó su fase.
7. **Tiempo total:** Flujo corto < 2 min, medio < 5 min, largo < 10 min (orientativo).
