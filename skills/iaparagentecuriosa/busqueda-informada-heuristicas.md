---
name: busqueda-informada-heuristicas
description: Búsqueda informada con heurísticas: Greedy best-first search, A* óptimo, propiedades de heurísticas (consistencia, admisibilidad), distancia Manhattan vs euclídea, variantes de A* (IDA*, SMA*), y aplicación a agentes modernos (MDP, POMDP, MCTS).
---

# Búsqueda Informada y Heurísticas

## Identidad

- **Fuente:** IA para gente curiosa — Fascículo 02, caps. 1-4 (Búsqueda, BFS/DFS/UCS, Greedy/A*, agentes modernos)
- **Autor:** 686f6c61 (CC BY 4.0)
- **Cuadernos Colab:** [BFS, DFS, UCS y A*](https://colab.research.google.com/github/686f6c61/iaparagentecuriosa-notebooks/blob/main/Facs%C3%ADmil%2002/01-busqueda-bfs-dfs-ucs-astar.ipynb)

## El bucle genérico de búsqueda

Todos los algoritmos de búsqueda comparten la misma estructura. La única diferencia es **qué nodo extraemos de la frontera**.

```
buscar(problema):
    frontera  ← { nodo(s0, coste=0, padre=None) }
    visitados ← { }
    mientras frontera no esté vacía:
        n ← extraer(frontera)              # ← aquí decide el algoritmo
        si n.estado ∈ G:
            devolver reconstruir_camino(n)
        si n.estado ∈ visitados:
            continuar
        visitados ← visitados ∪ { n.estado }
        para cada acción a en A(n.estado):
            s' ← f(n.estado, a)
            si s' ∉ visitados:
                g' ← n.coste + c(n.estado, a)
                frontera ← frontera ∪ { nodo(s', g', padre=n) }
    devolver fracaso
```

## Búsqueda ciega (no informada)

Cuando no tienes pistas del dominio, solo estructuras de datos:

| Algoritmo | Estructura | Completitud | Optimalidad | Complejidad espacio |
|-----------|-----------|-------------|-------------|---------------------|
| **BFS** | Cola FIFO | Sí | Sí (coste unitario) | O(bᵈ) |
| **DFS** | Pila LIFO | No (en espacio infinito) | No | O(bm) |
| **UCS** | Cola prioridad g(n) | Sí | Sí | O(bᵈ*) |
| **IDS** | DFS iterativo profundidad | Sí | Sí | O(bᵈ) |

**IDS (Iterative Deepening Search):** Combina lo mejor de BFS y DFS — completitud de BFS, memoria de DFS.

## Búsqueda informada: Greedy vs A*

### Greedy Best-First Search

```
f_Greedy(n) = h(n)
```

Evalúa solo la estimación de lo que falta. Rápido pero:
- ❌ No es completo (puede entrar en ciclos)
- ❌ No es óptimo (ignora g(n), el coste acumulado)
- ✅ Si h(n) es buena, encuentra solución rápido explorando muy pocos estados

**Peligro:** como ir de Madrid a Berlín mirando solo la distancia en línea recta — te empuja hacia una montaña porque "en línea recta" parece más corta.

### A*: coste real + estimación

```
f(n) = g(n) + h(n)
```

- `g(n)` = coste real acumulado desde el inicio hasta n
- `h(n)` = estimación barata de lo que falta hasta la meta

**Propiedad clave:** si h(n) es **admisible** (nunca sobreestima), A* es óptimo.

## Heurísticas: el arte de saber qué ignorar

### Definiciones formales

| Propiedad | Definición | Implicación |
|-----------|-----------|-------------|
| **Admisibilidad** | h(n) ≤ h*(n) para todo n | A* es óptimo |
| **Consistencia** | h(n) ≤ c(n, n') + h(n') para todo arco (n,n') | A* óptimo + no re-expande nodos |
| **Domina** | h₁ domina h₂ si h₁(n) ≥ h₂(n) ∀n (ambas admisibles) | h₁ explora menos nodos |

### Heurísticas comunes por dominio

| Problema | Heurística | Fórmula |
|----------|-----------|---------|
| **Mapa/rutas** | Distancia euclídea | `√((x₁-x₂)² + (y₁-y₂)²)` |
| **Mapa/rejilla** | Distancia Manhattan | `|x₁-x₂| + |y₁-y₂|` |
| **Puzzle 8/15** | Mal colocadas | nº fichas en posición incorrecta |
| **Puzzle 8/15** | Suma distancias | Σ dist_manhattan de cada ficha |

### Auditar una heurística antes de usarla

1. **Comprueba admisibilidad:** ¿puede h(n) sobrestimar h*(n)? Si sí, A* pierde optimalidad.
2. **Mide tasa de coincidencia:** sobre casos conocidos, ¿cuántas veces h(n) = h*(n)? Una tasa alta = heurística potente.
3. **Compara dominancia:** si tienes dos heurísticas admisibles, h_max(n) = max(h₁(n), h₂(n)) siempre domina a ambas.
4. **Mide nodos expandidos:** a menor número, mejor. Un buen problema es sudoku (9×9): h=0 explora millones, h=mal_colocadas explora decenas.

## Variantes de A*

| Variante | Cuándo usar | Ventaja | Desventaja |
|----------|-------------|---------|------------|
| **A\*** | Memoria disponible | Óptimo | O(bᵈ) memoria |
| **IDA\*** | Poca memoria | Memoria O(d) | Re-expande nodos |
| **SMA\*** | Memoria estricta | Óptimo si solución alcanzable | Complejo de implementar |
| **Greedy** | Velocidad > optimalidad | Explora pocos nodos | No óptimo |

### IDA* (Iterative Deepening A*)

```
f_limite = ∞
loop:
    resultado = busqueda_limited(inicio, f_limite)
    if resultado == ENCONTRADO: return camino
    if resultado == SIN_SOLUCION: return fracaso
    f_limite = min(f valores_que_no_encontraron_solucion)
```

Es A* con profundidad iterativa. Usa O(d) memoria en vez de O(bᵈ).

## Búsqueda en agentes modernos

### MDP: decidir con resultado incierto

Cuando la acción no produce un estado único sino una distribución:

```
MDP = (S, A, T, R, γ)
```

- `S` = estados
- `A` = acciones
- `T(s, a, s')` = probabilidad de llegar a s' desde s con acción a
- `R(s, a)` = recompensa
- `γ` = factor de descuento

### POMDP: parcialmente observable

Cuando no ves el estado completo. Usas **belief state** — una distribución de probabilidad sobre los estados que podrías estar.

### MCTS: búsqueda en árbol de decisiones

Monte Carlo Tree Search: explora y explota alternando:
1. **Selección** — recorre el árbol eligiendo nodos con mejor UCB
2. **Expansión** — añade un hijo nuevo
3. **Simulación** — juega aleatoriamente hasta el final
4. **Retropropagación** — actualiza estadísticas hacia arriba

**En agentes LLM:** simular con LLMs no es lo mismo que simular con reglas. El modelo introduce ruido, alucinaciones y sesgos que distorsionan la búsqueda.

## Pitfalls

1. **Greedy sin ver g(n)** — la heurística puede empujarte hacia un mínimo local. Siempre verifica el coste acumulado.
2. **Heurística no admisible** — A* pierde optimalidad. Si h sobreestima, puedes perder la solución óptima.
3. **Recalcular h(n) caro** — la heurística debe ser barata. Si h(n) cuesta más que buscar, pierde el propósito.
4. **Confundir árbol con grafo** — sin memoria de visitados, BFS/UCS pueden quedar en bucles infinitos en espacios con ciclos.
5. **Explosión combinatoria** — N(d) = (b^(d+1) - 1)/(b - 1). Profundidad 10 con b=10 → 11 mil millones de nodos.

## Referencias

- **Capítulos:** F02-C1 (Búsqueda), C2 (BFS/DFS/UCS), C3 (Greedy/A*)
- **Cuaderno:** [Buscar en un mapa: BFS, DFS, coste uniforme y A*](https://colab.research.google.com/github/686f6c61/iaparagentecuriosa-notebooks/blob/main/Facs%C3%ADmil%2002/01-busqueda-bfs-dfs-ucs-astar.ipynb)
- **Referencia teórica:** Russell & Norvig, Chapter 3-4; Pearl, "Heuristics"
