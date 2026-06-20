---
name: testing
description: "Patrones completos de testing para proyectos Node.js/JavaScript — unit testing, mocking de APIs, property-based testing, mutation testing, CI/CD. Complementa el skill testing-jest-mocks-api con enfoques avanzados."
version: 1.0.0
author: Mastermind
tags: [testing, jest, property-based, mutation, quality, ci-cd]
---

# Testing — Patrones Completos

Colección de patrones de testing para proyectos Node.js/JavaScript. Organizado en 3 niveles de profundidad.

## Niveles de testing

| Nivel | Qué cubre |
|-------|-----------|
| **Básico** | Mocks HTTP, fixtures, degradación de servicios, smoke tests |
| **Avanzado** | Generación automática de inputs, shrinking, model-based testing |
| **Calidad** | Mutation testing, medir calidad real de tests, CI/CD |

## 1. Jest + Mocks de API (Básico)

Patrón para testear servicios que dependen de APIs HTTP externas usando Jest con mocks.

### Mock del cliente HTTP
```javascript
const mockFetchIndicator = jest.fn();
jest.mock('../src/infra/clients/esios.client', () => ({
  fetchIndicator: (...args) => mockFetchIndicator(...args),
}));
```

### Fixtures de datos
```javascript
function createBaseResponses() {
  return new Map([
    [1001, { indicator: { values: [{ datetime: '2026-05-25T00:00:00+02:00', value: 52.4 }] } }],
    [1293, { indicator: { values: [{ datetime: '2026-05-25T00:00:00+02:00', value: 30000 }] } }],
    // ... más indicadores
  ]);
}
```

### Buenas prácticas
1. **Mock del cliente HTTP** — no llamar a la API real en tests unitarios
2. **Mapa de respuestas** — fixture centralizado, fácil de extender
3. **Valores crudos** — testear que la conversión de unidades funciona
4. **Degradación graceful** — probar que indicadores opcionales fallan sin romper
5. **DST edge cases** — probar cambios de hora de verano e invierno
6. **Smoke tests** — verificar que las rutas HTTP responden con supertest

### Pitfalls
- ❌ Tests que llaman a API real → lentos, frágiles, dependen de token
- ❌ No testear valores convertidos → la conversión puede estar mal
- ❌ Mock demasiado simple → no captura errores reales (null, undefined)
- ❌ No testear DST → en marzo/octubre el dashboard muestra datos desplazados

## 2. Property-Based Testing (Avanzado)

## Flujo recomendado

```
1. Escribir test unitario con mocks → testing-jest-mocks-api
2. Añadir propiedades invariantes → testing-property-based-fast-check
3. Verificar calidad con mutation testing → testing-mutation-stryker
```

## Referencias

- `references/testing-pipeline.md` — Pipeline completo de testing con los 3 niveles
- `references/esios-testing-examples.md` — Ejemplos concretos del proyecto ESIOS

## Pitfalls

- ❌ No confundir coverage con quality — 100% coverage puede tener mutation score de 30%
- ❌ No ejecutar mutation testing en cada PR — es caro. Usar en merge a main o nightly
- ❌ No usar `fc.pre()` en exceso en fast-check — si filtras >50% de inputs, es lento
- ❌ No mezclar `expect()` con `return` en fast-check puro — usar `return boolean` para fast-check puro, `expect()` dentro de `fc.context()` para Jest
