# Levenshtein Swap Bug — Caso de Estudio

## Contexto

Al crear el módulo `Adela_search` (2026-06-15), la implementación de la distancia de Levenshtein con optimización de dos filas contenía un bug que causaba distancias incorrectas cuando las cadenas tenían longitudes diferentes.

## Síntoma

```
levenshtein('adla', 'adela') → 3 (esperado: 1)
levenshtein('catl', 'cataluña') → 5 (esperado: 4)
```

Los tests de `sugerencias()` fallaban porque la distancia inflada hacía que no se alcanzara el umbral de `maxDistance`.

## Causa Raíz

La optimización de dos filas usa swap cuando `m < n`:

```typescript
const swap = m < n
const fuente = swap ? b : a        // fuente = más corto si m < n
const objetivo = swap ? a : b       // objetivo = más largo si m < n

for (let i = 1; i <= lenA; i++) {  // lenA = max(m,n)
  for (let j = 1; j <= lenB; j++) {
    const costo = objetivo[i - 1] === fuente[j - 1] ? 0 : 1
    // BUG: objetivo[i-1] accede más allá del array cuando i > lenB
  }
}
```

El problema: `fuente` tiene longitud `lenB` (el más corto) pero el loop exterior itera hasta `lenA` (el más largo). Cuando `i > lenB`, `fuente[i-1]` accede fuera de límites.

Además, los índices están intercambiados: `objetivo[i-1]` debería ser `objetivo[j-1]` y `fuente[j-1]` debería ser `fuente[i-1]`.

## Fix

```typescript
const lenA = Math.max(m, n)
const lenB = Math.min(m, n)

// fuente = string más largo (iterado con i), objetivo = más corto (iterado con j)
const fuente = m >= n ? a : b
const objetivo = m >= n ? b : a

for (let i = 1; i <= lenA; i++) {
  for (let j = 1; j <= lenB; j++) {
    const costo = objetivo[j - 1] === fuente[i - 1] ? 0 : 1
    // ✅ i-1 < lenA = fuente.length, j-1 < lenB = objetivo.length
  }
}
```

## Resultado

- 77/77 tests pasando
- `levenshtein('adla', 'adela')` → 1 ✅
- `levenshtein('catl', 'cataluña')` → 4 ✅

## Lección

La optimización de dos filas es sutil. El swap de strings debe acompañarse de un swap de los índices de acceso. Siempre verificar con un caso de prueba donde `|a.length - b.length| >= 2`.