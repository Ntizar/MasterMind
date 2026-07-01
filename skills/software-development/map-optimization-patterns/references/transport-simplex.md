# Transporte — Método Simplex de Transporte

## Vogel's Approximation Method (VAM)

VAM es el método más usado para obtener una solución inicial buena para el problema de transporte.

### Algoritmo

```
1. Calcular penalización por fila = diferencia entre 2 menores costos
2. Calcular penalización por columna = diferencia entre 2 menores costos
3. Seleccionar fila/columna con MAYOR penalización
4. En esa fila/columna, asignar el máximo posible a la celda de menor costo
5. Actualizar supply/demand restante
6. Si supply o demanda llega a 0, eliminar fila/columna
7. Repetir hasta que todo esté asignado
```

### Implementación

```javascript
function vam(supply, demand, costMatrix) {
  const m = supply.length, n = demand.length;
  const flows = Array.from({length: m}, () => new Array(n).fill(0));
  const sup = [...supply], dem = [...demand];
  const rowActive = new Array(m).fill(true);
  const colActive = new Array(n).fill(true);

  for (let iter = 0; iter < m + n - 1; iter++) {
    // Penalizaciones fila
    const rowPen = [];
    for (let i = 0; i < m; i++) {
      if (!rowActive[i]) { rowPen.push(-1); continue; }
      const costs = [];
      for (let j = 0; j < n; j++) {
        if (colActive[j]) costs.push({ cost: costMatrix[i][j], j });
      }
      costs.sort((a, b) => a.cost - b.cost);
      rowPen.push(costs.length >= 2 ? costs[1].cost - costs[0].cost : costs[0]?.cost || 0);
    }

    // Penalizaciones columna
    const colPen = [];
    for (let j = 0; j < n; j++) {
      if (!colActive[j]) { colPen.push(-1); continue; }
      const costs = [];
      for (let i = 0; i < m; i++) {
        if (rowActive[i]) costs.push({ cost: costMatrix[i][j], i });
      }
      costs.sort((a, b) => a.cost - b.cost);
      colPen.push(costs.length >= 2 ? costs[1].cost - costs[0].cost : costs[0]?.cost || 0);
    }

    // Seleccionar mayor penalización (fila o columna)
    const maxRowPen = Math.max(...rowPen);
    const maxColPen = Math.max(...colPen);

    let bestI, bestJ;
    if (maxRowPen >= maxColPen) {
      bestI = rowPen.indexOf(maxRowPen);
      // En esa fila, buscar columna con menor costo activa
      let minCost = Infinity;
      for (let j = 0; j < n; j++) {
        if (colActive[j] && costMatrix[bestI][j] < minCost) {
          minCost = costMatrix[bestI][j];
          bestJ = j;
        }
      }
    } else {
      bestJ = colPen.indexOf(maxColPen);
      let minCost = Infinity;
      for (let i = 0; i < m; i++) {
        if (rowActive[i] && costMatrix[i][bestJ] < minCost) {
          minCost = costMatrix[i][bestJ];
          bestI = i;
        }
      }
    }

    // Asignar máximo posible
    const qty = Math.min(sup[bestI], dem[bestJ]);
    flows[bestI][bestJ] = qty;
    sup[bestI] -= qty;
    dem[bestJ] -= qty;

    if (sup[bestI] === 0) rowActive[bestI] = false;
    if (dem[bestJ] === 0) colActive[bestJ] = false;
  }

  return flows;
}
```

## MODI (Modified Distribution) — Optimización de la solución

Después de VAM, MODI verifica si la solución es óptima o si hay mejora posible.

```javascript
function modi(supply, demand, costMatrix, flows) {
  const m = supply.length, n = demand.length;
  // 1. Calcular variables duales u[i] y v[j]
  // 2. Para cada celda vacía, calcular reduced cost = c[i][j] - u[i] - v[j]
  // 3. Si todos los reduced costs ≥ 0 → solución óptima
  // 4. Si alguno < 0 → entrar esa celda, reasignar (stepping stone), repetir
  // (implementación completa ~80 líneas, ver literatura OR)
}
```

## Alternativa: Transportation como LP genérico

Para problemas más complejos (costes no lineales, restricciones adicionales), usar un LP solver:

```javascript
// Con glpk-wasm (GLPK compilado a WebAssembly, ~500KB)
import initGLPK from 'glpk-wasm';
const glpk = await initGLPK();

// Definir el problema LP
const lp = {
  name: 'transportation',
  objective: { direction: glpk.GLP_MIN, coeffs: flatCosts },
  constraints: [
    // supply constraints
    ...supply.map((s, i) => ({
      type: glpk.GLP_UP, bnd: s,
      coeffs: flatFlow.filter((_, idx) => Math.floor(idx / n) === i)
    })),
    // demand constraints
    ...demand.map((d, j) => ({
      type: glpk.GLP_LO, bnd: d,
      coeffs: flatFlow.filter((_, idx) => idx % n === j)
    }))
  ],
  binaries: flatFlow // x_ij ∈ {0,1} o continuous para transportation
};

const result = glpk.solve(lp);
```

## Costes de transporte: euclidiana vs real

El problema de transporte original usa distancia como coste unitario. Opciones:

1. **Euclidiana:** `c[i][j] = haversine(supply[i], demand[j])` — rápido, gratis
2. **Real (ORS):** `c[i][j] = routeDistance(supply[i], demand[j])` — realista, rate limited
3. **Híbrida:** Euclidiana × factor (1.3 para urbano, 1.5 para interurbano) — buena aproximación

```javascript
function buildCostMatrix(supply, demand, mode = 'euclidean', distFn = haversine) {
  return supply.map(s =>
    demand.map(d => distFn(s.lat, s.lng, d.lat, d.lng))
  );
}
```

## Infactibilidad del problema

Si Σsupply < Σdemand → no se puede satisfacer toda la demanda.
Si Σsupply > Σdemand → sobra capacidad.

```javascript
function checkFeasibility(supply, demand) {
  const totalSupply = supply.reduce((a, b) => a + b, 0);
  const totalDemand = demand.reduce((a, b) => a + b, 0);

  if (totalSupply < totalDemand) {
    return { feasible: false, deficit: totalDemand - totalSupply,
      message: `Déficit de ${totalDemand - totalSupply} unidades` };
  }
  if (totalSupply > totalDemand) {
    return { feasible: true, surplus: totalSupply - totalDemand,
      message: `Sobran ${totalSupply - totalDemand} unidades (origen sobrante)` };
  }
  return { feasible: true, balanced: true, message: 'Oferta = Demanda (balanceado)' };
}

// Si no es balanceado, añadir origen/destino ficticio para balancear
function balanceProblem(supply, demand) {
  const totalS = supply.reduce((a, b) => a + b, 0);
  const totalD = demand.reduce((a, b) => a + b, 0);
  if (totalS === totalD) return { supply, demand };

  if (totalS < totalD) {
    // Añadir origen ficticio con capacidad = déficit, coste 0
    return {
      supply: [...supply, totalD - totalS],
      demand: [...demand],
      virtualSupply: supply.length
    };
  } else {
    // Añadir destino ficticio con demanda = exceso, coste 0
    return {
      supply: [...supply],
      demand: [...demand, totalS - totalD],
      virtualDemand: demand.length
    };
  }
}
```
