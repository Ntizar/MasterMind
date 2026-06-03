---
fecha: 2026-03-19
tarea: dashboard-skill-md
tipo: datos
complejidad: alta
clusters: [sistema, datos]
proyecto: ninguno
patron: skill-con-memoria-dinamica
---

# Creación del skill universal de dashboards

## Decisión clave
Un skill de datos necesita separar explícitamente las reglas de ingesta/limpieza
de las reglas de visualización, y añadir un protocolo de memoria dinámica
que lo haga mejorar con cada proyecto ejecutado.

## Patrón reutilizable
sí → **skill-con-memoria-dinámica**
Cuando un skill se va a usar repetidamente en proyectos del mismo dominio,
añadir dos secciones al final del núcleo:
- "Ciclo de reaprendizaje": protocolo para archiver (qué capturar) y
  librarian (cuándo y cómo actualizar)
- "Patrones aprendidos de proyectos": tabla vacía con cabeceras definidas
  que el librarian rellena tras acumular ≥ 2 proyectos del mismo tipo

## Qué funcionó
- Separar "Reglas de datos" de "Reglas de visualización" — son fases distintas
  del pipeline y errores en una no deben contaminar la otra
- Definir el umbral del librarian (≥ 2 proyectos) de forma explícita en el skill
  evita ambigüedad sobre cuándo actuar
- El campo `encoding_encontrado` en el archiver es clave para datos españoles:
  captura el problema más frecuente en la primera iteración

## Qué evitar
- No definir el límite máximo de filas en la tabla de patrones — el índice
  crece sin control y se vuelve ruido en lugar de señal
- Mezclar el protocolo del archiver con el del librarian en la misma sección —
  son dos actores distintos con momentos de activación distintos

## Skills usados
- software-dev.md (referencia de calidad y estructura)
- Patrón extended-skill (learnings ciclo 1)

## Tests/criterios que validaron esto
REVIEWER REPORT PASS — 10 de 10 criterios verificados.
WARNING no bloqueante: ~900-950 tokens sobre orientativo de 800,
justificado por la densidad estructural del protocolo de reaprendizaje.

## Dashboard: datos del proyecto
fuente: N/A (este ciclo no procesó datos reales, creó el skill)
encoding_encontrado: N/A
problema_principal: N/A
solucion_aplicada: N/A
tipo_artefacto: N/A

## Conexiones
**Clusters:** #sistema · #datos
**Aprendizajes relacionados:** [[2026-03-19-software-skill-md]] · [[2026-03-19-system-gaps-fix]] · [[2026-03-19-nap-dashboard-ciclo6]]
