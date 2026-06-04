---
fecha: 2026-03-19
tarea: software-skill-md
tipo: conocimiento
complejidad: media
clusters: [sistema]
proyecto: ninguno
patron: extended-skill
---

# Creación del skill universal de desarrollo de software

## Decisión clave
Un skill de dominio amplio necesita secciones adicionales al template base
para ser accionable: "Fases universales" y "Decisiones clave" son obligatorias
en cualquier skill de dominio técnico complejo.

## Patrón reutilizable
sí → **extended-skill**
Cuando el dominio es lo suficientemente rico (software, research profundo,
operaciones complejas), el template base de 5 secciones es insuficiente.
Añadir: "Fases universales" + "Decisiones clave" antes de las Reglas.

## Qué funcionó
- Separar las fases universales de las reglas: las fases dan secuencia,
  las reglas dan calidad — son conceptos distintos y deben vivir por separado
- La tabla de "Decisiones clave" es más scannable que una lista de preguntas
- El límite de tokens en la spec funciona bien como restricción de diseño:
  obliga a priorizar y elimina el relleno

## Qué evitar
- Poner límites de tokens como criterio de aceptación duro cuando el dominio
  es inherentemente rico — mejor usarlo como WARNING orientativo
- Mezclar el "qué hacer" (fases) con el "cómo hacerlo bien" (reglas)

## Skills usados
- ninguno (este ciclo los creó)

## Tests/criterios que validaron esto
REVIEWER REPORT PASS — todos los criterios de aceptación de la spec verificados.
El único hallazgo fue WARNING no bloqueante sobre token count (~650 vs 600 estimado).

## Conexiones
**Cluster:** #sistema
**Aprendizajes relacionados:** [[2026-03-19-dashboard-skill-md]] · [[2026-03-19-system-gaps-fix]]
