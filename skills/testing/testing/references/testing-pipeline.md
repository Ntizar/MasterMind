# Pipeline de Testing — 3 Niveles

## Nivel 1: Unit Testing + Mocks

**Skill:** `testing-jest-mocks-api`

```
tests/
├── summary.test.js      # Tests del servicio con mocks HTTP
├── time.test.js         # Tests de timezone/DST
├── conversion.test.js   # Tests de conversión de unidades
└── api.test.js          # Smoke tests de endpoints REST
```

**Cobertura objetivo:** 80%+ de líneas en código de dominio.

## Nivel 2: Property-Based Testing

**Skill:** `testing-property-based-fast-check`

Añadir propiedades invariantes para funciones críticas:

```javascript
// En tests/conversion.test.js (junto a los unit tests)
const fc = require('fast-check');

describe('conversion properties', () => {
  it('factor 10: convertido * 10 <= original', () => {
    fc.assert(
      fc.property(fc.integer({ min: 0, max: 1000000 }), (raw) => {
        const converted = Math.floor(raw / 10);
        expect(converted * 10).toBeLessThanOrEqual(raw);
      }),
    );
  });
});
```

**Regla:** Añadir propiedades para TODAS las funciones de transformación que operen sobre datos externos.

## Nivel 3: Mutation Testing

**Skill:** `testing-mutation-stryker`

```bash
# Ejecutar semanalmente o en merge a main
npx stryker run

# Verificar mutation score
# Objetivo: >70% en código de dominio
# Umbral de fallo: <50%
```

**Config mínima para CI:**
```javascript
// stryker.config.mjs
config.mutationScoreThreshold = 50;
config.coverageThreshold = 'break';
```

## Frecuencia

| Nivel | Frecuencia | Cuándo |
|-------|-----------|--------|
| Unit + mocks | Cada PR | Siempre |
| Property-based | Cada PR (para funciones críticas) | Solo funciones de transformación |
| Mutation | Weekly / merge a main | Nunca en cada PR |
