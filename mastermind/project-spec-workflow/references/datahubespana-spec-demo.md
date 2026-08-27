# Demo: SPEC.md generado para DataHubEspana

> Ejemplo real del flujo `project-spec-workflow` aplicado a un proyecto existente.
> DataHubEspana era un monolito de 11.538 líneas en index.html. Esta spec define
> la arquitectura modular objetivo y el plan de extracción por fases.

## Contexto del proyecto

- **Repo:** Ntizar/DataHubEspana (PÚBLICO)
- **Estado actual:** Monolito — 1 archivo index.html de 588KB, 151 funciones, 62 fetch calls
- **Objetivo:** Extraer a arquitectura modular sin romper funcionalidad existente

## Lo que el agente detectó automáticamente

Al aplicar el flujo `project-spec-workflow`, el agente:

1. **Leyó el proyecto** — `wc -l index.html` (11.538 líneas), `grep -c 'function '` (151), `grep -c 'fetch('` (62)
2. **Consultó memoria** — encontró que DataHubEspana es un proyecto conocido (17 pestañas, 30+ gráficos, 12+ APIs)
3. **Identificó el problema** — monolito imposible de iterar sin regresiones
4. **Generó la spec** — con arquitectura objetivo + plan de extracción por fases

## Estructura de la spec generada

La spec incluye:

- **Visión** — 1 frase: qué es y para qué
- **Alcance** — qué hace y qué NO hace (non-goals explícitos)
- **Pantallas** — 17 pestañas documentadas
- **Datos** — tabla de 15 fuentes con tipo, frecuencia y volumen
- **Arquitectura** — estado actual (problema) vs objetivo (modular)
- **Capas** — tabla de 8 capas con responsabilidad y límites
- **Estado global** — diseño del objeto Estado centralizado
- **Interfaces** — qué expone cada módulo (funciones públicas)
- **Stack** — tecnologías y deploy
- **Criterios de éxito** — métricas medibles
- **Anti-patrones** — lo que se evita (con referencias a SOUL.md)
- **Plan de extracción** — 8 fases, una pestaña por commit

## Lecciones clave

1. **El monolito no se refactoriza de golpe** — se extrae por capas, una fase por commit
2. **Cada fase es verificable** — después de cada extracción, comprobar que todo sigue funcionando
3. **Los anti-patrones vienen de SOUL.md** — el agente los conoce y los incluye en la spec
4. **La spec es el contrato** — si una iteración futura se desvía, volver a la spec
5. **Una pestaña = un archivo** — cada panels/*.js es independiente y testable

## Ver también

- Skill: `project-spec-workflow` (skill principal)
- Skill: `frontend-dashboard-patterns` (patrones de dashboard)
- Skill: `software-development` → sección "Safe Refactoring"
- SOUL.md → sección "Pitfalls críticos" (anti-patrones de ESIOS, charts, tabs)
