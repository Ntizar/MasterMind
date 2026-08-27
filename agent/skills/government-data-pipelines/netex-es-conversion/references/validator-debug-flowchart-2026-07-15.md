# Flujo de depuración del validador español (Jul 2026)

## Estrategia general

Cuando el validador español reporta errores, seguir este orden:

```
1. ES_ID_FORMAT (formato de IDs)
   ↓
2. NETEX_ID_5 (referencias no resueltas)
   ↓
3. SERVICE_JOURNEY_3/15 (estructura de viajes)
   ↓
4. ROUTE_3/4, LINE_4, JP_2 (estructura de rutas/líneas)
   ↓
5. XPATH_1, COMPOSITE_FRAME (wrapper)
   ↓
6. Warnings (44 restantes, todos opcionales)
```

## Causas raíz típicas

### ES_ID_FORMAT (~460 errores)
- **Causa 1 (95%):** IDs con minúsculas en el tipo. El regex del validador es `^ES:[A-Z_]+:[A-Z0-9_]+:[A-Z0-9_:]+$` — los tipos deben ser UPPER_SNAKE_CASE (`COMPOSITE_FRAME`, no `CompositeFrame`).
- **Causa 2 (5%):** IDs sin operador o con más de 4 segmentos. `_make_id()` debe sanitizar `:` en la secuencia reemplazándolos por `_`.
- **Solución:** Centralizar generación de IDs en `_make_id()` con conversión CamelCase→UPPER_SNAKE_CASE + sanitizado de `:`.

### NETEX_ID_5 (~2.600 errores)
- **Causa 1 (80%):** Referencias que apuntan a IDs con formato diferente al de la definición. Si la definición usa `f-string` y la referencia usa `_make_id()`, no coinciden.
- **Causa 2 (15%):** Elementos que no se generan (viajes sin stop_times, etc.) pero se referencian.
- **Causa 3 (5%):** Referencias hardcodeadas al formato antiguo (ej: `f"{prefix}:Line:..."` en lugar de `_make_id("Line", ...)`).
- **Solución:** TODAS las definiciones y referencias deben usar `_make_id()` con los mismos argumentos. Misma función, mismos parámetros → mismo ID.

### SERVICE_JOURNEY_3/15 (~136 errores)
- **Causa 1 (50%):** Usar `<calls>`/`<Call>` en lugar de `<passingTimes>`/`<TimetablePassingTime>`. El estándar NeTEx usa `passingTimes`, el validador español valida contra esto.
- **Causa 2 (50%):** `Arrival`/`Departure` anidados en `<Time>` en lugar de `ArrivalTime`/`DepartureTime` con texto directo. El validador busca `.//ArrivalTime`.
- **Solución:** Estructura correcta: `passingTimes` → `TimetablePassingTime` → `ArrivalTime`/`DepartureTime` (texto HH:MM:SS directo).

### ROUTE_3/4, LINE_4, JP_2 (~44 errores)
- **Causa (100%):** Elementos que faltan o nombres incorrectos:
  - `lineRef` faltante en Route → añadir `ref(route_elem, "lineRef", _make_id("Line", ...))`
  - `TransportMode` faltante en Line (o mal escrito) → el validador busca PascalCase
  - `journeyPatternElements` en lugar de `pointsInSequence` en JourneyPattern
  - `routeElements` en lugar de `pointsInSequence` en Route (bug del validador)
- **Solución:** El generador debe emitir estos elementos, y el validador debe buscarlos con PascalCase.

## Regla de oro cuando algo falla

1. **No asumir que el generador está mal** — primero verificar qué nombre de elemento busca exactamente el validador (grep en semantic_validator.py)
2. **No asumir que el validador está bien** — varios nombres de elementos están en minúscula cuando deberían ser PascalCase
3. **Verificar con lxml** antes de cambiar el generador: parsear el XML y buscar el elemento con `find("netex:ElementName", NS)` 
4. **Caso más común:** el generador produce `OperatorRef` pero el validador busca `operatorRef` (minúscula). Arreglar el validador, no el generador.