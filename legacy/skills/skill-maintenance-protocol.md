---
name: skill-maintenance-protocol
description: Patrón de mantenimiento de skills con reaprendizaje activo. El Librarian detecta skills con sección "## Ciclo de reaprendizaje", acumula learnings y ejecuta el protocolo para enriquecer la tabla del skill con nuevos patrones.
version: 1.0.0
author: Ntizar Brain
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [mantenimiento, reaprendizaje, librarian, auditoría, skills, aprendizaje-continuo]
---

# Protocolo de Mantenimiento de Skills con Reaprendizaje Activo

## Qué es

Patrón de mantenimiento que permite a los skills del sistema **aprender de su propio uso**. Cada skill puede definir una sección `## Ciclo de reaprendizaje` que describe cómo se enriquece con nuevos patrones. El Librarian monitorea los learnings acumulados, detecta cuando ≥2 learnings del mismo tipo se acumulan, y ejecuta el protocolo de reaprendizaje para agregar esos patrones a la tabla del skill.

### ¿Por qué reaprendizaje activo?

- **Los skills se estancan** si solo contienen lo que se escribió al inicio.
- **Los patrones emergen** del uso real del sistema, no de la planificación.
- **El Librarian es el custodio** que detecta cuándo un skill necesita actualizarse.
- **La auditoría periódica** mantiene el sistema consistente y actualizado.

### Estructura de un skill con reaprendizaje

```markdown
# Nombre del Skill

## Qué es
...

## Cuándo usar
...

## Pasos
...

## Tabla de patrones
| Patrón | Descripción | Cuándo aplicar | Ejemplo |
|--------|-------------|----------------|---------|
| patrón-1 | ... | ... | ... |

## Ciclo de reaprendizaje
- **Trigger:** ≥2 learnings del mismo tipo acumulado
- **Tipo de learning a detectar:** [ej: "pattern", "bugfix", "optimization"]
- **Protocolo de actualización:** [cómo se agrega el patrón a la tabla]
- **Quién ejecuta:** Librarian
- **Frecuencia:** [mensual / tras acumulación / on-demand]
```

## Cuándo usar

- **Al inicio de una sesión del Librarian:** Revisar todos los skills activos.
- **Tras acumular ≥2 learnings del mismo tipo:** Ejecutar reaprendizaje inmediatamente.
- **En auditoría periódica:** Revisar consistencia de todos los skills.
- **Cuando el humano solicita:** El humano puede pedir mantenimiento de un skill específico.

## Pasos

### Paso 1 — El Librarian detecta skills con reaprendizaje

```
1. Recorrer todos los skills en la carpeta skills/
2. Identificar los que tienen sección "## Ciclo de reaprendizaje"
3. Para cada skill con reaprendizaje:
   a. Contar learnings del tipo indicado en el trigger
   b. Si count ≥ 2 → marcar para ejecución del protocolo
```

### Paso 2 — Ejecutar el protocolo del skill

```
1. Leer el skill completo y su tabla de patrones actual
2. Leer los learnings acumulados del tipo trigger
3. Extraer los patrones nuevos de los learnings
4. Agregar los patrones a la tabla del skill
5. Actualizar la sección "## Qué es" si es necesario
6. Guardar el skill actualizado
```

### Paso 3 — Registrar el reaprendizaje

```
1. Crear un learning de tipo "maintenance" que registre:
   - Skill actualizado
   - Patrones agregados
   - Fecha de actualización
   - Learnings fuente utilizados
2. Actualizar el índice de skills con la nueva fecha de actualización
```

### Paso 4 — Ejecutar auditoría completa

```
Tras el reaprendizaje, el Librarian emite un reporte de auditoría:

AUDITORÍA DE SKILLS
──────────────
SKILLS_ACTIVOS: [lista de skills con estado]
LEARNINGS_REGISTRADOS: [total por tipo]
ARCHIVABLES: [skills o learnings que pueden archivarse]
TEMPLATES_VIGENTES: [templates que están actualizados]
INCONSISTENCIAS: [problemas detectados]
SKILLS_CON_REAPRENDIZAJE_REVISADOS: [skills actualizados en esta auditoría]
```

## Reporte de auditoría — Formato detallado

```
AUDITORÍA DE SKILLS — [fecha]
──────────────

SKILLS ACTIVOS:
  ✅ [skill-1] — actualizado: [fecha] — patrones: [número]
  ✅ [skill-2] — actualizado: [fecha] — patrones: [número]
  ⚠️ [skill-3] — actualizado: [fecha] — patrones: [número] — reaprendizaje pendiente

LEARNINGS REGISTRADOS:
  - pattern: [número]
  - bugfix: [número]
  - feature: [número]
  - decision: [número]
  - maintenance: [número]

ARCHIVABLES:
  - [skill/learning] — motivo: [razón del archivado]

TEMPLATES VIGENTES:
  ✅ template-skill.md — actualizado: [fecha]
  ✅ template-learning.md — actualizado: [fecha]

INCONSISTENCIAS:
  - [inconsistencia 1]: [descripción]
  - [inconsistencia 2]: [descripción]

SKILLS CON REAPRENDIZAJE REVISADOS:
  - [skill-1]: [número] patrones agregados, [número] learnings fuente
  - [skill-2]: [número] patrones agregados, [número] learnings fuente
```

## Ejemplo de ciclo de reaprendizaje

### Skill: `multi-agent-orchestration`

```markdown
## Ciclo de reaprendizaje
- **Trigger:** ≥2 learnings de tipo "pattern" acumulados
- **Tipo de learning a detectar:** "pattern"
- **Protocolo de actualización:**
  1. Leer los learnings de tipo "pattern" acumulados
  2. Extraer el patrón identificado en cada learning
  3. Agregar una fila a la tabla de patrones del skill
  4. Actualizar la columna "cuándo aplicar" con el contexto del learning
  5. Eliminar los learnings fuente (ya están incorporados)
- **Quién ejecuta:** Librarian
- **Frecuencia:** Tras acumulación de ≥2 learnings
```

### Ejecución del ejemplo

```
1. Librarian detecta 3 learnings de tipo "pattern" acumulados
2. Learning 1: "Patrón de reintentos con backoff exponencial"
3. Learning 2: "Patrón de delegación en cascada para tareas paralelas"
4. Learning 3: "Patrón de checkpoint para tareas de larga duración"
5. Librarian agrega 3 filas a la tabla de patrones del skill
6. Librarian marca los 3 learnings como "incorporados"
7. Librarian actualiza la fecha de actualización del skill
8. Librarian emite reporte de auditoría
```

## Pitfalls

| Pitfall | Síntoma | Solución |
|---------|---------|----------|
| Trigger demasiado bajo | Se reaprende con 1 learning | Mínimo 2 learnings del mismo tipo |
| Trigger demasiado alto | Se acumulan learnings sin procesar | Revisar frecuencia de auditoría |
| Patrón duplicado | La tabla tiene patrones idénticos | Verificar unicidad antes de agregar |
| Skill sin tabla de patrones | No hay dónde agregar patrones | Crear tabla de patrones al definir el skill |
| Sin sección de reaprendizaje | El Librarian no sabe cómo actualizar | Todo skill debe tener "## Ciclo de reaprendizaje" |
| Auditoría sin inconsistencias | No se detectan problemas | Incluir sección de inconsistencias siempre |
| Learnings no eliminados tras incorporación | Duplicación de conocimiento | Marcar como "incorporados" y archivar |

## Verificación

Para verificar que el protocolo de mantenimiento se ejecuta correctamente:

1. **Skills con reaprendizaje identificados:** El Librarian reporta todos los skills con sección "## Ciclo de reaprendizaje".
2. **Trigger respetado:** Ningún skill se reaprende con menos de 2 learnings del tipo trigger.
3. **Tabla actualizada:** Los patrones agregados aparecen en la tabla del skill con todas las columnas.
4. **Learnings fuente procesados:** Los learnings que dispararon el reaprendizaje se marcan como incorporados.
5. **Auditoría completa:** El reporte incluye las 7 secciones: activos, registrados, archivables, templates, inconsistencias, reaprendizaje revisados.
6. **Inconsistencias detectadas:** La sección de inconsistencias no está vacía si hay problemas.
7. **Índice actualizado:** La fecha de actualización del skill se refleja en el índice de skills.
