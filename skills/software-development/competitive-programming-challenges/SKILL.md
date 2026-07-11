---
name: competitive-programming-challenges
version: "1.0.0"
category: software-development
description: "Resolver retos de programación competitiva — hackathons, competiciones Kaggle-style, coding contests con scoring público y leaderboard. Incluye MAPF (Multi-Agent Pathfinding), reverse-engineering de seeds ocultas, y validación local."
---

# Competitive Programming Challenges

Resolver retos de programación competitiva: hackathons, competiciones Kaggle-style, coding contests con scoring público y leaderboard.

## When to use

- Hackathons con leaderboard público y scoring determinista
- Competiciones Kaggle-style (submit → evaluar → puntuar)
- Optimización multi-agente o multi-objetivo con scoring competitivo
- Retos donde hay que maximizar/minimizar un metric sobre seeds o test cases ocultos

## Workflow

1. **Estudiar las reglas** — Leer instrucciones con atención. Extraer: tamaño del grid, constraints, fórmula de scoring, límites de tiempo, formato de submission.
2. **Examinar el leaderboard** — Si es público, estudiar el código de los top solutions. Entender QUÉ técnicas usan, NO copiar su código.
3. **Entender la evaluación** — ¿Cómo se puntúa? ¿Qué parámetros están ocultos (seeds, test cases)? ¿Se pueden reverse-engineer?
4. **Escribir código original** — Implementar tu propia solución usando técnicas aprendidas del estudio. NUNCA copiar-pegar una solución del leaderboard y presentarla como tuya.
5. **Construir validador local** — Replicar la evaluación lo más fielmente posible para iterar rápido.
6. **Iterar** — Tunear parámetros, probar algoritmos distintos, medir mejoras.
7. **Ser honesto** — Reportar lo que TU código consigue, no lo que el código de otro consigue.

## Pitfalls

### CRÍTICO: Copiar vs. Aprender
- **NUNCA copiar una solución del leaderboard y presentarla como logro propio.** El usuario pide "lograr" un score — eso significa escribir código original que lo consiga.
- Estudiar top solutions para entender técnicas (A* MAPF, flow routing, seed tuning) es BUENO. Copiar su código verbatim es MALO.
- Si no puedes superar el top score con código original, dilo honestamente. No reclames el score de otro como tuyo.
- El usuario lo detectará. Preguntará "¿cuántos has conseguido?" y tendrás que admitir que copiaste.
- **Esta regla aplica a cualquier reto competitivo, no solo hackathons.**

### Seed Reverse-Engineering
- Las seeds ocultas pueden estar embebidas en el payload de la web (React/Next.js RSC data, `__NEXT_DATA__`, `__next_f` script tags)
- Buscar keys como `global_seed`, `seed`, `run_seed` en el RSC payload
- Las seeds pueden ocultarse post-competición (`"global_seed":"hidden"`) — el reverse-engineering solo funciona durante competiciones activas
- Un equipo encontró seeds en los atributos `key` de elementos `<tr>` del payload React

### Gap entre simulación local y evaluador oficial
- Las simulaciones locales con mocks pueden no replicar el evaluador oficial
- Diferencias en asignación de targets, resolución de colisiones, y timing causan gaps significativos (ej: 890 local vs 1008 oficial)
- Siempre documentar el gap entre scores locales y oficiales
- El validador local sirve para iterar, no para confirmar el score oficial

### Sistema de scoring triangular
- Fórmula típica: `points = T(current-C) - T(previous-C)` donde `T(n) = n(n+1)/2`
- Solo superar el frontier actual da puntos; empatar da 0
- El primer sprint (primeras submissions) acumula más puntos que mejoras tardías
- Si el baseline es muy bajo, los equipos que llegan tarde no pueden ganar → considerar esto al planificar submissions

### Incomplete config coverage
- Al estudiar código de top solutions, auditar SIEMPRE que todas las seeds/scenarios tengan config completa
- Un seed sin jitter, o con config copiada de otra seed, es una oportunidad de mejora inmediata
- Ejemplo: Equipo 10 tenía JITTER_CONFIGS para 2 de 3 seeds — la tercera usaba default. Añadir jitter faltante es una mejora trivial que el equipo original no hizo
- Buscar configs asimétricas: si seed A tiene (X, Y) y seed B tiene (X, Y) idéntico, probablemente una de ellas no fue tuneda independientemente

## Key Techniques

### Multi-Agent Pathfinding (MAPF)
- **Centralized cooperative A*** — Planear todos los agentes simultáneamente con reservation table
- **Windowed reservation** — Reservar celdas para cada agent N ticks adelante (WINDOW=35 típico)
- **Flow-aware routing** — Penalizar movimiento contra-flujo para crear aisles unidireccionales (FLOW_PENALTY=0.1)
- **Priority-based conflict resolution** — Carrying primero → más cercano al target → wait-streak boost
- **Fallback greedy** — Para agentes sin plan completo
- Ver `references/mapf-techniques.md` para detalle algorítmico

### Layout Design
- **2x2 shelf blocks** con period-3 aisles maximizan accesibilidad
- **Aisles anchos** (2-3 celdas) reducen congestión
- **Base entries** deben estar libres de shelves
- **One-way flow** — Diseñar layout para fomentar patrones circulares de tráfico

### Seed-Specific Tuning
- Identificar seed activa comparando el primer target del robot 0
- Mapear coordenadas de target a sets de parámetros optimizados (WINDOW, FLOW_PENALTY)
- Default config para seeds desconocidos

## References

- `references/mapf-techniques.md` — Notas detalladas de algoritmos MAPF (A* reservation, flow routing, conflict resolution, performance characteristics)
- `references/refugio-challenge.md` — Caso de estudio: REFUGIO Warehouse Challenge (reglas, leaderboard, seed reverse-engineering, lecciones)
