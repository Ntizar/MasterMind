---
name: biblia-tests-primero
description: "Use al iniciar proyectos: biblia de tests antes del código."
version: "1.0.0"
tags: [tdd, tests, auditoria, calidad, vibecode]
---

# Biblia de Tests Primero

Metodología de David Antizar (nacida en Water3J, 2026-08-30): **los tests son la biblia del proyecto** — se escriben ANTES que el código y auditan el programa de forma continua.

## Reglas invariables

1. Tests con criterios **numéricos medibles** (tolerancias, unidades, fps, % error). Nunca "se ve bien".
2. IDs únicos secuenciales (`PROY-T01`…). Test nuevo = ID nuevo + entrada en la biblia. Nunca reciclar ni borrar.
3. Jamás relajar un criterio para que pase el código. Modificar un test solo si el criterio estaba mal especificado, con justificación en sección "Historial".
4. Cada módulo nuevo entra con su test antes que con su código. Un commit que rompe un test verde se rechaza.
5. Evidencia obligatoria: cada resultado registra valor medido vs criterio (`tests/registro.json`).

## Artefactos estándar (plantilla probada en Water3J)

- `docs/XX-biblia-tests.md` — documento maestro. Cada test: ID, categoría, prioridad (P0 bloqueante/P1 core/P2 deseable), requisito GWT (Dado-Cuando-Entonces), procedimiento exacto, criterio medible, evidencia.
- `tests/suite.js` — array `TESTS` con `{id, nombre, categoria, prioridad, estado: PENDING/PASS/FAIL, run}` + utilidades comunes (solver de referencia independiente, errRel, NaN check, medidor FPS).
- `tests/runner.html` — runner en navegador: tabla con estado/medida/criterio, descarga de registro.
- `tests/registro.json` — última auditoría (fecha, commit, resultado por test). README muestra contador "X/N tests pasando".

## Claves de diseño de buenos tests

- Resolver las fórmulas de referencia **independientemente en el test** (p.ej. Newton-Raphson propio), nunca reutilizando el código de la app.
- Incluir test de **robustez** (valores extremos, NaN, clamps) y de **rendimiento** (fps sostenidos, draw calls) desde el principio.
- Validar contra literatura/papers (p.ej. Fraccarollo & Toro para presa rota, Green's law, Snell).
- Tests de serialización round-trip y determinismo (dos ejecuciones → mismo resultado).
- Matriz de trazabilidad requisito→test al final de la biblia.
- "Definición de hecho": fase completa solo cuando sus P0/P1 pasan en hardware de referencia y el registro está actualizado.

## Flujo de trabajo

1. Diseñar tests del MVP con el usuario (exigente, casos de uso reales).
2. Implementar módulos guiándose por el criterio de su test (cada test declara su fase).
3. Ejecutar runner → commit del registro → README actualizado.
4. Ampliar con vibecode: el contrato hace que cualquier agente sepa qué implementar y cómo se valida.

## Referencia viva

Ejemplo completo funcionando: `~/Projects/Water3J` (docs/09-biblia-tests.md + tests/). Copiar estructura de ahí para nuevos proyectos.