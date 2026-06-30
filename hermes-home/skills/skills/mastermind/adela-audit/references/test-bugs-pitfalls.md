# Bug patterns conocidos en tests Adela

## 1. Test runner mismatch (2026-06-15)

**Síntoma:** `TypeError: Cannot read properties of undefined (reading 'config')` o `Suite test failed` con vitest runner en tsx.

**Causa:** `package.json` dice un runner pero los tests importan de otro framework.

**Módulos afectados:** Adela_security, Adela_logger (vitest imports + node:test runner).

**Fix:** Cambiar `package.json` scripts.test para que coincida con los imports:
- `import { describe, it } from 'vitest'` → `"test": "vitest run"`
- `import { describe, it } from 'node:test'` → `"test": "tsx --test tests/*.test.ts"`

**Verificación rápida:**
```bash
cd /root/workspace/Adela/Adela_<NOMBRE>
head -1 tests/*.test.ts  # Ver qué importa
grep '"test"' package.json  # Ver qué runner ejecuta
```

## 2. Object.assign con mocks de funciones (2026-06-15)

**Síntoma:** `assert.ok(next.called)` falla aunque la función sí se ejecutó.

**Causa:** `Object.assign(fn, { called: false })` copia el valor primitivo `false` a la función. Cuando `ctx.called = true` se ejecuta dentro del closure, cambia `ctx.called` pero NO `fn.called` (son copias independientes).

**Fix — usar getters:**
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

## 3. TypeScript readonly vs runtime writable (2026-06-15)

**Síntoma:** `assert.equal(desc.writable, false)` falla — `writable` es `true`.

**Causa:** TypeScript `readonly` es solo compile-time check. En runtime, `this.status = status` en el constructor asigna normalmente (writable: true por defecto).

**Fix — test correcto:**
```typescript
// ❌ MAL — readonly TS no pone writable:false
const desc = Object.getOwnPropertyDescriptor(err, 'status');
assert.equal(desc!.writable, false);

// ✅ BIEN — verificar que es propiedad propia
assert.ok(Object.prototype.hasOwnProperty.call(err, 'status'));
assert.equal(err.status, 400);
```

**Si necesitas readonly real en runtime:** usar `Object.defineProperty` en el constructor:
```typescript
Object.defineProperty(this, 'status', { value: status, writable: false, enumerable: true });
```
