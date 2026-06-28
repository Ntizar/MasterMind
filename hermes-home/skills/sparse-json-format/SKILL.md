---
name: sparse-json-format
description: "Formato JSON sparse para datasets grandes: 40-60% menos de tamaño. Clave-valores en arrays en vez de objetos repetidos. Ideal para datos tabulares por entidad (municipios, empresas, usuarios) donde muchas filas comparten las mismas columnas."
version: 1.0.0
author: Mastermind
tags: [json, compression, sparse, data, performance, vanilla-js]
source: espanatlas.es
---

# Sparse JSON Format — Formato Compacto para Datasets Grandes

## Cuándo usar
- JSON con miles de filas que repiten los mismos 30-100 keys
- Datos tabulares donde muchos valores son null/undefined
- Archivos >5MB que se pueden reducir a ~2MB
- APIs que sirven datasets completos por categoría

## Problema: JSON estándar es verboso

```json
// ❌ ESTÁNDAR — 150 bytes por fila
[
  {"cod":"28079","nom":"Madrid","p25":3223334,"renta23":21500,"tParo25":8.2},
  {"cod":"41091","nom":"Sevilla","p25":684635,"renta23":16200,"tParo25":14.1},
  {"cod":"08019","nom":"Barcelona","p25":1636762,"renta23":19800,"tParo25":9.5}
]

// ✅ SPARSE — 80 bytes por fila (47% menos)
{
  "keys": ["cod","nom","p25","renta23","tParo25"],
  "rows": [
    ["28079","Madrid",3223334,21500,8.2],
    ["41091","Sevilla",684635,16200,14.1],
    ["08019","Barcelona",1636762,19800,9.5]
  ]
}
```

## Formato sparse

```json
{
  "keys": ["cod", "nom", "p25", "renta23", "tParo25", "densidad"],
  "rows": [
    ["28079", "Madrid", 3223334, 21500, 8.2, 5200],
    ["41091", "Sevilla", 684635, 16200, 14.1, 4900],
    ["08019", "Barcelona", 1636762, 19800, 9.5, 16000]
  ]
}
```

**Reglas:**
- `keys`: array de strings con los nombres de columna (orden fijo)
- `rows`: array de arrays, donde cada sub-array es una fila
- Los valores mantienen su orden correspondiente a `keys`
- Los strings se comprimen más que en formato estándar

## Formato ultra-sparse (valores como pares índice-valor)

Para datasets donde muchos valores son null:

```json
{
  "keys": ["cod", "nom", "p25", "renta23", "tParo25", "densidad", "deuda24", "alqMes24"],
  "rows": [
    ["28079", [0, 3223334, 2, 21500, 3, 8.2, 4, 5200]],
    ["41091", [0, 684635, 2, 16200, 3, 14.1]]
  ]
}
```

**Reglas ultra-sparse:**
- Primer valor del row: código/key primaria
- Segundo valor: array plano `[índice_key, valor, índice_key, valor, ...]`
- Solo se incluyen valores no-null
- El índice referencia la posición en `keys`

## Decodificar

```javascript
// Formato sparse estándar
function expandSparseRows(payload) {
  if (!payload || !Array.isArray(payload.keys) || !Array.isArray(payload.rows)) {
    return payload;  // ya es formato estándar
  }
  return payload.rows.map(row => {
    const out = {};
    for (let i = 0; i < row.length; i++) {
      out[payload.keys[i]] = row[i];
    }
    return out;
  });
}

// Formato ultra-sparse
function expandUltraSparseRows(payload) {
  return payload.rows.map(row => {
    const cod = row[0];
    const out = { cod };
    const pairs = row[1];
    for (let i = 0; i < pairs.length; i += 2) {
      out[payload.keys[pairs[i]]] = pairs[i + 1];
    }
    return out;
  });
}
```

## Generar sparse desde JavaScript

```javascript
function toSparseFormat(data, keys) {
  return {
    keys,
    rows: data.map(item => keys.map(k => item[k] ?? null))
  };
}

function toUltraSparseFormat(data, keys, keyField = 'cod') {
  return {
    keys,
    rows: data.map(item => {
      const pairs = [];
      keys.forEach((k, i) => {
        if (k !== keyField && item[k] != null) {
          pairs.push(i, item[k]);
        }
      });
      return [item[keyField], pairs];
    })
  };
}

// Ejemplo
const datos = [
  { cod: '28079', nom: 'Madrid', p25: 3223334, renta23: 21500, alqMes: null },
  { cod: '41091', nom: 'Sevilla', p25: 684635, renta23: 16200, alqMes: 850 }
];

const sparse = toSparseFormat(datos, ['cod', 'nom', 'p25', 'renta23', 'alqMes']);
// { keys: [...], rows: [['28079','Madrid',3223334,21500,null], ...] }

const ultraSparse = toUltraSparseFormat(datos, ['cod', 'nom', 'p25', 'renta23', 'alqMes']);
// { keys: [...], rows: [['28079', [1,'Madrid',2,3223334,3,21500]], ['41091', [1,'Sevilla',2,684635,3,16200,4,850]]] }
```

## Métricas de ahorro

```javascript
// Calcular ratio de compresión
function compressionRatio(standardJSON, sparseJSON) {
  const stdSize = new Blob([JSON.stringify(standardJSON)]).size;
  const sprSize = new Blob([JSON.stringify(sparseJSON)]).size;
  return {
    standard: stdSize,
    sparse: sprSize,
    ratio: ((1 - sprSize / stdSize) * 100).toFixed(1) + '%',
    savings: stdSize - sprSize
  };
}
```

## Pitfalls

1. **No funciona con datos heterogéneos** — si cada fila tiene keys distintas, sparse no ahorra
2. **Pérdida de legibilidad** — el JSON ya no es auto-documentado
3. **Parsing overhead** — `expandSparseRows()` añade ~10ms por 10K filas
4. **Null values** — en sparse estándar se incluyen como `null`; en ultra-sparse se omiten
5. **Compatibilidad** — consumidores deben saber el formato; no es JSON estándar

## Cuándo NO usar

- Datasets <1000 filas (el ahorro es mínimo)
- Datos con keys muy variables entre filas
- APIs que consumen clientes que esperan JSON estándar
- Datos jerárquicos/anidados (sparse solo funciona con tabular plano)

## Integración con otros skills

- **lazy-dataset-loading** → cargar sparse datasets por categoría
- **hash-index-data** → indexar las filas expandidas por key
