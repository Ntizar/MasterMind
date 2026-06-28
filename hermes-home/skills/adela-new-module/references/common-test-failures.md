# Fallos comunes de tests en módulos Adela

## 1. Test runner mismatch (el más común)

**Síntoma:** `TypeError: Cannot read properties of undefined (reading 'config')` o `no tests` o `suites 0`

**Causa:** Tests importan de `'vitest'` pero package.json dice `"tsx --test"` (o viceversa).

**Fix:** Cambiar el script en package.json para que coincida con los imports:
```json
// Si tests importan vitest:
"test": "vitest run"

// Si tests importan node:test:
"test": "tsx --test tests/*.test.ts"
```

**Detección rápida:**
```bash
head -3 tests/*.test.ts | grep "from 'vitest\|from 'node:test'"
grep '"test"' package.json
```

## 2. mockNext con Object.assign

**Síntoma:** Test verifica `next.called` pero siempre es `false`, aunque la función sí se ejecuta.

**Causa:** `Object.assign(next, ctx)` copia valores primitivos (`false`, `null`) como propiedades estáticas. Cuando `ctx.called = true` se ejecuta dentro de la función, cambia `ctx.called` pero NO `next.called` (son copias independientes).

**Fix:** Usar `Object.defineProperty` con getters:
```typescript
function mockNext() {
  const ctx = { called: false, arg: null as unknown };
  const next = ((err?: unknown) => {
    ctx.called = true;
    ctx.arg = err;
  }) as NextFunction & { called: boolean; arg: unknown };
  Object.defineProperty(next, 'called', { get: () => ctx.called, configurable: true });
  Object.defineProperty(next, 'arg', { get: () => ctx.arg, configurable: true });
  return next;
}
```

**Patrón alternativo más simple:**
```typescript
function mockNext() {
  const calls: unknown[] = [];
  const next = ((err?: unknown) => { calls.push(err); }) as NextFunction & { calls: unknown[] };
  return next;
}
// Assert: expect(next.calls).toHaveLength(1); expect(next.calls[0]).toBeInstanceOf(AppError);
```

## 3. TypeScript readonly ≠ runtime readonly

**Síntoma:** Test verifica `Object.getOwnPropertyDescriptor(err, 'status').writable === false` pero falla.

**Causa:** TypeScript `readonly` es solo compile-time. En runtime, `this.status = status` en el constructor crea una propiedad writable normal.

**Fix:** No testear `writable`. En su lugar, verificar que las propiedades existen y son propias:
```typescript
assert.ok(Object.prototype.hasOwnProperty.call(err, 'status'));
assert.equal(err.status, 400);
```

Si necesitas readonly real en runtime, usar `Object.defineProperty` en el constructor:
```typescript
Object.defineProperty(this, 'status', { value: status, writable: false, enumerable: true });
```

## 4. ESM import paths con `.js`

**Síntoma:** `Cannot find module './errors.js'` o `MODULE_NOT_FOUND`

**Causa:** En ESM TypeScript, los imports DEBEN terminar en `.js` (no `.ts`):
```typescript
// ✅ Correcto
import { createErrorModule } from './errors.js';

// ❌ Falla en ESM
import { createErrorModule } from './errors';
```

Aunque el archivo sea `errors.ts`, el import usa `.js`. TypeScript lo resuelve correctamente.

## 5. UNIQUE constraint en SQLite: datos de test colisionan entre runs

**Síntoma:** Test que crea un registro con nombre fijo falla con 500 (o error de constraint) en runs sucesivos, pero pasa en el primero.

**Causa:** La DB SQLite persiste entre runs (ej: `/data/datos.db`). Si el test crea un registro con `nombre: 'colabora_con'` y la tabla tiene `UNIQUE` en `nombre`, el segundo run intenta insertar un duplicado → error.

**Fix:** Siempre usar datos únicos en tests:
```typescript
// ❌ MAL — colisiona en el segundo run
.send({ nombre: 'colabora_con', ... })

// ✅ BIEN — Timestamp hace el nombre único
.send({ nombre: `colabora_con_${Date.now()}`, ... })
```

**Regla general:** Cualquier campo con constraint `UNIQUE` o `PRIMARY KEY` en tests debe incluir `Date.now()` o `Math.random()` como sufijo. Aplica a: nombres de entidades, emails de prueba, CIFs, etc.

**Detección:** Si un test pasa la primera vez pero falla después, buscar `UNIQUE` en la definición de la tabla y verificar que el test no reutiliza el mismo valor.
