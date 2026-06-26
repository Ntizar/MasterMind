# TSP Heurísticas — Implementación Detallada

## Nearest Neighbor + 2-opt: Resultados esperados

| Ciudades | Nearest Neighbor | + 2-opt | Óptimo exacto |
|---|---|---|---|
| 10 | ~130% óptimo | ~105% óptimo | 100% |
| 20 | ~125% | ~103% | 100% |
| 50 | ~120% | ~102% | 100% |
| 100 | ~115% | ~101% | 100% |

2-opt converge típicamente en < 100 iteraciones para ≤ 50 puntos.

## 3-opt (para > 50 puntos)

3-opt elimina 3 aristas y reconnecta el tour. Es O(n³) por iteración pero da mejor calidad que 2-opt.

```javascript
// 3-opt: eliminar 3 aristas, probar todas las reconexiones posibles
function tsp3Opt(tour, distMatrix) {
  let improved = true;
  while (improved) {
    improved = false;
    for (let a = 0; a < tour.length - 2; a++) {
      for (let b = a + 2; b < tour.length - 1; b++) {
        for (let c = b + 2; c < tour.length; c++) {
          // Probar las 8 formas de reconectar (simplificado a las más comunes)
          const segments = [
            tour.slice(0, a + 1),
            tour.slice(a + 1, b + 1),
            tour.slice(b + 1, c + 1),
            tour.slice(c + 1)
          ];
          // Intercambiar y reconectar...
          // (implementación completa: probar 2-opt-like swaps entre segmentos)
        }
      }
    }
  }
}
```

## Simulated Annealing (para > 100 puntos)

```javascript
function tspSA(points, distMatrix, temp0 = 10000, cooling = 0.9995, minTemp = 1) {
  let tour = tspNearestNeighbor(points, (a, b) => distMatrix[a.id][b.id]);
  let bestTour = [...tour];
  let bestDist = tourDistance(tour, distMatrix);
  let currentDist = bestDist;
  let temp = temp0;

  while (temp > minTemp) {
    // Generar vecino: intercambiar 2 ciudades aleatorias
    const i = Math.floor(Math.random() * tour.length);
    const j = Math.floor(Math.random() * tour.length);
    const newTour = [...tour];
    [newTour[i], newTour[j]] = [newTour[j], newTour[i]];
    const newDist = tourDistance(newTour, distMatrix);

    // Aceptar o rechazar
    const delta = newDist - currentDist;
    if (delta < 0 || Math.random() < Math.exp(-delta / temp)) {
      tour = newTour;
      currentDist = newDist;
      if (currentDist < bestDist) {
        bestTour = [...tour];
        bestDist = currentDist;
      }
    }
    temp *= cooling;
  }
  return bestTour;
}
```

## TSP Abierto vs Cerrado

- **Circuito cerrado:** El proyecto original cierra el tour (vuelta al inicio). Más natural para delivery/rutas de reparto
- **Ruta abierta:** No vuelve al inicio. Más natural para inspecciones/visitas donde empiezas y terminas en sitios distintos

```javascript
// Cerrado: tour.push(tour[0]) al final
// Abierto: no cerrar, o especificar inicio/fijo
function solveTSP(points, distFn, closed = true) {
  const tour = tspNearestNeighbor(points, distFn);
  const optimized = tsp2Opt(tour, points, distFn);
  if (closed) optimized.push(optimized[0]);
  return optimized;
}
```

## TSP con punto fijo (inicio)

Algunas rutas requieren empezar en un punto concreto (ej: almacén):

```javascript
function tspFixedStart(points, startIdx, distFn) {
  // Fijar el primero, optimizar el resto
  const rest = points.filter((_, i) => i !== startIdx);
  const restTour = tspNearestNeighbor(rest, distFn);
  return [startIdx, ...restTour.map(i => i >= startIdx ? i + 1 : i)];
}
