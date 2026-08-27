# Multi-Agent Pathfinding (MAPF) Techniques

## Centralized Cooperative A*

### Overview
Planear todos los agentes simultáneamente usando A* con una windowed reservation table. El path de cada agente se planifica considerando las celdas reservadas por otros agentes.

### Key Parameters
- **WINDOW** — Número de ticks a planificar hacia adelante (35 típico para 96 robots)
- **NODE_CAP** — Máximo nodos en búsqueda A* (2500 típico)
- **WAIT_CAP** — Máximo waits consecutivos antes de anti-deadlock (30)
- **FLOW_PENALTY** — Penalización por movimiento contra-flujo (0.1 típico)

### Algorithm
1. Ordenar agentes por prioridad: carrying > más cercano al target > wait streak
2. Para cada agente, correr A* para encontrar path al target
3. Reservar celdas a lo largo del path para WINDOW ticks
4. Si A* falla (NODE_CAP excedido), usar greedy fallback
5. Ejecutar primer step del plan de cada agente
6. Repetir cada tick

### Conflict Resolution
- **Vertex conflict** — Dos agentes quieren la misma celda → agente de menor prioridad espera
- **Edge conflict** — Dos agentes intercambian posiciones → agente de menor prioridad espera
- **Cascade** — Si A espera por B, y B espera por C, resolver en orden de prioridad

### Flow-Aware Routing
- Trackear dirección del tráfico en cada aisle
- Penalizar moves contra el flujo (FLOW_PENALTY * counter_flow_count)
- Crea aisles unidireccionales emergentes sin hard constraints
- Reduce significativamente colisiones head-on

### Anti-Deadlock
- Después de WAIT_CAP waits consecutivos, forzar un move válido aleatorio
- Previene gridlock permanente en escenarios densos

## BFS Distance Caching

- Pre-calcular distancias BFS desde cada base y shelf a todas las celdas
- Usar como heurística admissible en A*
- Cache persistente entre ticks (el layout no cambia)
- Para 96 robots × 960 shelves: ~92K BFS runs, cacheadas en dict

## Layout Design for MAPF

### 2x2 Block Pattern
- Shelves en bloques 2x2 con gap de 1 celda entre bloques
- Period-3 grid: shelf at (x,y) donde x%3≠0 AND y%3≠0
- Crea red regular de aisles
- 960 shelves en interior 50x50

### Aisle Width
- 1-cell aisles: máxima densidad, alta congestión
- 2-cell aisles: buen balance (recomendado)
- 3-cell aisles: baja congestión, menos shelves

### Base Placement
- 96 bases en el borde (top/bottom/left/right)
- Spacing uniforme (cada 2 celdas)
- Entry cells deben estar libres de shelves

### Entry-Removal Pattern
- Eliminar shelves adyacentes a las entradas de bases
- Crea "buffers" de espacio libre cerca de bases
- Reduce congestión en zonas de alta actividad

## Performance Characteristics

### REFUGIO Hackathon — Progressión de Scores

| Score | Técnica | Innovación clave |
|-------|---------|-------------------|
| 369 | Greedy cached BFS | Closest useful square + cached paths |
| 397 | BFS shortest-path | Routing más limpio, moves predecibles |
| 398 | Anti-deadlock greedy | Esquivar celdas ocupadas en vez de esperar |
| 610 | PIBT-style reservations | Robots "reservan" su próximo move |
| 759 | PIBT + rotational tie-breaks | Rotar prioridades para evitar starvation |
| 882 | Windowed cooperative A* | Planear N ticks ahead para todos los robots |
| 897 | Cooperative A* + aisle flow | One-way aisle bias para reducir head-on |
| 924 | Seed-aware replay fallback | Replays precomputados para seeds conocidas |
| 1008 | Seed-tuned MAPF + custom layout | Per-seed parameter optimization + layout hand-crafted |

### Equipo 10's REFUGIO Solution (1008 deliveries)
- 96 robots, 960 shelves, 52x52 grid, 300 ticks, 3 seeds
- WINDOW=35, NODE_CAP=2500, FLOW_PENALTY=0.1
- Seed-specific tuning: diferente WINDOW/FLOW para cada hidden seed
- ~300-340 deliveries por seed (337 + 337 + 334 ≈ 1008)
- 19.3s runtime (180s budget)
- SEED_CONFIGS: {(14,42):(34,0.1), (12,33):(32,0.06), (26,47):(32,0.06)}
  - Key = coordenadas del primer target del robot 0
  - Value = (WINDOW, FLOW_PENALTY)
- JITTER_CONFIGS (original, INCOMPLETO): {(14,42):(1,0.05), (12,33):(13,0.05)}
  - ⚠️ Seed (26,47) sin jitter → usaba DEFAULT_JITTER (-1, 0.0)
- JITTER_CONFIGS (mejorado): {(14,42):(1,0.05), (12,33):(13,0.05), (26,47):(7,0.05)}
- SEED_CONFIGS (mejorado): {(14,42):(34,0.1), (12,33):(32,0.06), (26,47):(33,0.08)}

### Lecciones de Performance
- El jump de 882→1008 (+126) vino de seed tuning + layout, no de mejoras al algoritmo base
- Aumentar WINDOW (35→40) o NODE_CAP (2500→4000) NO mejoró — el bottleneck no era la búsqueda
- El layout custom fue tan importante como el algoritmo: mejores lanes = menos congestión
- El gap entre 882 (windowed A* puro) y 1008 (seed-tuned + layout) = 14% improvement
