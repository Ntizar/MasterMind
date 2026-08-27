---
name: node-backend-patterns
description: "Patrones completos para aplicaciones backend en Node.js — autenticación con sesiones, SQLite/sql.js, ESM/CommonJS interop, migración a fullstack."
version: "1.0.0"
author: Hermes Agent
tags: [nodejs, backend, express, sqlite, auth, esm, commonjs, fullstack]
---

# Node.js Backend Patterns

Colección de patrones para construir y mantener aplicaciones backend en Node.js.

## 1. Autenticación con Sesiones (SQLite + bcrypt)

Patrón completo de autenticación web con Node.js + SQLite + bcrypt + sesiones HTTP.

### Resumen
- Registro con validación (username, email, password)
- Login con bcrypt comparison
- Sesiones con express-session + cookie-parser
- Esquema de BD: users + sessions con foreign keys e índices
- Middleware: requireAuth, optionalAuth
- Frontend: tabs login/register con fetch

### Pitfalls
- `CREATE INDEX IF NOT EXISTS` — el typo `IF NOT` (sin EXISTS) causa crash silencioso
- Usar `bcryptjs` (pure JS), no `bcrypt` (requiere compilación C++)
- `npm ci` necesita package-lock.json sincronizado
- No exponer password_hash en respuestas

Ver `references/auth-patterns.md` para código completo.

## 2. ESM / CommonJS Interoperabilidad

Patrones para cargar módulos legacy (IIFE) en Node.js ESM.

### Resumen
- `new Function()` + `globalThis` para cargar módulos SEF en ESM
- `eval()` no funciona en ESM para módulos que usan `globalThis`
- Orden de carga secuencial (dependencias)
- CLI headless con parser de argumentos robusto

### Pitfalls
- `eval()` en ESM no tiene acceso a `globalThis` scope
- `globalThis.window` necesario para módulos que hacen `window.SEF`
- Parser debe soportar `--flag valor` (sin =) además de `--flag=valor`

Ver `references/esm-interop-patterns.md` para código completo.

## 3. Fullstack App con SQLite (sql.js)

Guía para crear/migrar apps Node.js/Express a SQLite con sql.js.

### Resumen
- sql.js (WASM) vs better-sqlite3 (nativo) — usar sql.js en contenedores
- Helper functions: `sql_get`, `sql_run` para evitar bugs de sql.js
- Auth simplificada (single-user o token)
- Frontend reestructuración: tabs principales + overflow menu
- NaN Builders: syncGitHub para persistencia entre redeploy
- Dockerfile para sql.js

### Pitfalls
- `stmt.run(arg1, arg2)` falla en sql.js — usar `stmt.run([arg1, arg2])`
- Key mismatch SQL/frontend (español vs inglés)
- JSON.parse sin try-catch → 500 silencioso
- XSS en chat: escapeHtml ANTES de markdown
- SQL injection en PUT dinámico: whitelist por tabla

Ver `references/sqljs-patterns.md` para código completo.

## 4. Express CRUD Route Files

Patrón para crear ficheros de rutas REST CRUD en Express/TypeScript con functions de base de datos. Incluye GET (lista+filtros), GET/:id, POST, PUT, DELETE.

### Convenciones del proyecto
- ID param: `req.params.id as string`
- Auth: `AuthRequest` del middleware local
- Errores: 400 (validación), 404 (no encontrado), 409 (UNIQUE conflict), 500 (genérico)
- POST → 201, DELETE → `{ mensaje }`, GET → `{ <entidad>s }`

### Pitfalls
- Hacer `return` explícito tras `res.status(X).json(...)` para evitar `ERR_HTTP_HEADERS_SENT`
- Booleanos en query params requieren parse explícito (`typeof req.query.X === 'string'`)
- Capturar UNIQUE con `error?.message?.includes('UNIQUE')` para 409

Ver `references/express-crud-routes.md` para plantilla completa y todos los pitfalls.

## 6. Pedidos de Venta vs Pedidos de Compra — Dos módulos distintos

En AdelaCRM existen **dos** módulos de pedidos completamente separados:

| | Pedidos de Compra (PC) | Pedidos de Venta (PED) |
|---|---|---|
| Tabla | `pedidos_compra` | `pedidos` |
| Tabla líneas | `lineas_pedido_compra` | `lineas_pedido` |
| Router | `pedidosCompra.ts` → `/api/pedidos-compra` | `pedidos.ts` → `/api/pedidos` |
| Funciones DB | `obtenerPedidosCompra`, `crearPedidoCompra`... | `obtenerPedidos`, `crearPedido`... |
| Tipo TS | `PedidoCompra` | `Pedido` |
| Número | `PC-0001` | `PED-YYYYMMDD-XXXX` |
| Estado inicial | `borrador` | `pendiente` |
| Estados | `borrador` → `enviado` → `recibido_parcial` → `recibido_total` | `pendiente` → `confirmado` → `en_proceso` → `enviado` → `entregado` |

### Pitfall: no confundir las funciones DB
`obtenerPedidosCompra` y `obtenerPedidos` son funciones **diferentes** que operan sobre tablas distintas. Si importas la errónea, los datos no coinciden.

### Generación de número de pedido de venta
```ts
const ahora = new Date().toISOString()
const year = ahora.slice(0, 4)
const monthDay = ahora.slice(5, 10).replace('-', '')
const counter = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
const numero = `PED-${year}${monthDay}-${counter}`
```

## 7. Añadir funciones DB cuando faltan

Cuando se crean rutas para una entidad nueva y las funciones DB no existen:

1. **Crear tabla** en el schema de `initDatabase()` si no existe
2. **Añadir funciones** en `db.ts` ANTES de la sección siguiente (orden alfabético/temático)
3. **Importar tipos** en el `import type { ... }` de db.ts
4. **Exportar** en el bloque `export { ... }` al final del fichero

### Pitfalls
- **`run`/`all`/`get` NO se exportan** de db.ts → si una ruta necesita SQL crudo, añadir una función helper en db.ts (ej: `actualizarCobro`, `conciliarCobro`) en lugar de hacer `import('../db.js').then(db => db.run(...))` — eso da error TS.
- **`await obtenerX()` → `.then()` no funciona** → `obtenerX()` ya es async, el `.then()` devuelve un `Promise`, no el valor. Usar `const items = await obtenerX()` y luego `.find()`.
- **Tipos TS incompletos** → verificar que la interface en `types.ts` coincide con la tabla SQL (ej: `LineaPedido` necesita `orden` si la tabla tiene columna `orden`).

## 8. Express App/Server Separation for Testability

Patrón para separar la configuración de Express (`app`) del arranque del servidor (`listen()`), de modo que los tests puedan importar la app sin que se ejecute `app.listen()`.

### Problema

```ts
// server.ts ❌ — app.listen() se ejecuta al importar
import express from 'express'
const app = express()
app.use(/* ... */)
app.listen(PORT, () => console.log(`Server on port ${PORT}`))
export default app  // test import → puerto ocupado, timeout
```

Cuando un test importa `server.ts`, `app.listen()` se ejecuta inmediatamente, ocupando el puerto y causando timeouts en supertest.

### Solución — Separar app.ts de server.ts

**`src/app.ts`** — Solo configuración Express, exporta `app`:

```ts
import express from 'express'
import cors from 'cors'
// importar rutas...

const app = express()
app.use(cors())
app.use(express.json())
// registrar rutas...
// app.listen() NO AQUÍ

export default app
```

**`src/server.ts`** — Solo arranque, importa `app`:

```ts
import app from './app.js'

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`🚀 Servidor en puerto ${PORT}`)
})

export default app  // opcional, para compatibilidad
```

**Tests importan `app.ts`** en vez de `server.ts`:

```ts
import app from '../src/app.js'  // ✅ — no arranca servidor
```

### Verificación

1. `npx tsx --test tests/*.test.ts` → tests pasan sin timeout
2. `npm run build` → 0 errores de compilación
3. `node dist/server.js` → servidor arranca correctamente

### Pitfalls

- **No olvidar exportar `app` desde `server.ts`** si hay código legacy que lo importa
- **Actualizar todos los imports de tests** de `server.js` a `app.js`
- **Verificar que Dockerfile/commands de producción usan `server.js`** (el que hace listen), no `app.js`
- **No mover middlewares que necesitan acceso a `req`/`res`** (middleware de error global) — dejarlos en app.ts

### Cuándo usar

- Siempre que la app Express tenga tests con supertest
- Siempre que se separe la preocupación de configuración del arranque
- Proyectos con TypeScript y `strict: true`

## 9. CRUD Update Key Whitelist Mismatch — Anti-Patrón

Cuando una función `actualizarX()` usa una whitelist explícita de campos actualizables, el route handler puede enviar campos que la whitelist ignora silenciosamente.

### El Anti-Patrón

```ts
// db.ts — la función update tiene una whitelist
async function actualizarPresupuesto(id: string, data: Partial<Presupuesto>) {
  const campos: string[] = []; const valores: any[] = []
  for (const k of ['empresaId','contactoId','fechaEmision','fechaValidez','estado',
                   'subtotal','descuentoGlobal','ivaTotal','total','moneda']) {
    if ((data as any)[k] !== undefined) { campos.push(`${k} = ?`); valores.push((data as any)[k]) }
  }
  if (campos.length > 0) { /* UPDATE con campos */ }
}

// routes/presupuestos.ts — el handler envía campos CON OTRO NOMBRE
await actualizarPresupuesto(id, { baseImponible, totalIva, total }) // ❌ baseImponible y totalIva NO están en la whitelist
```

**Resultado:** `baseImponible` y `totalIva` se descartan silenciosamente. El `total` sí se actualiza pero los desgloses quedan stale.

### Por qué ocurre

- El nombre del campo en el flujo de datos cambia entre etapas (ruta usa un nombre conceptual, BD usa la columna exacta)
- Al refactorizar nombres de columnas en la BD, se actualiza la whitelist pero no los callers
- Al añadir un nuevo campo calculado al recalculo, se añade en la ruta pero no en la whitelist

### Cómo detectarlo (auditoría)

1. En `db.ts`, buscar `for (const k of [`. Esa lista es la whitelist de actualización
2. En `routes/*.ts`, buscar los objetos que se pasan a `actualizarX(id, { ... })`
3. Comparar nombres: si la ruta envía un campo que no está en la whitelist → **BUG**

**No basta con comparar frontend↔backend:** el mismatch puede estar entre ruta y función DB, no visible desde el frontend.

### Cómo arreglarlo

1. **Opción A — Renombrar en la ruta:** cambiar el payload de la ruta para que use los nombres exactos de la whitelist
   ```ts
   // Antes (roto)
   await actualizarPresupuesto(id, { baseImponible, totalIva, total })
   // Después (correcto)
   await actualizarPresupuesto(id, { subtotal, ivaTotal, total })
   ```
2. **Opción B — Añadir a la whitelist:** si el nuevo campo merece persistencia real, añadirlo al array
3. **Opción C — Refactorizar:** cambiar la whitelist por un `Object.keys(data).filter(k => ALLOWED_FIELDS.has(k))` para que sea más difícil de desincronizar

### Prevención

- Al crear una nueva función update, documentar la whitelist como comentario junto a la función
- Al añadir un recalculo en la ruta, verificar que los campos enviados existen en la whitelist
- Tests de integración que verifiquen que los valores calculados persisten correctamente

### ⚠️ Este bug es silencioso

No lanza error, no da 500, no hay stack trace. Los valores simplemente no se guardan. Solo se detecta leyendo el código o comparando estado antes/después del update en BD.

## 10. Módulos ES (type="module") — CONFIG global no funciona

En proyectos con `type: "module"` en `package.json`, **las variables `const`/`let`/`class` definidas en un módulo NO son globales**. Cada `.js` tiene scope propio.

### El Bug Silencioso

```js
// config.js
const CONFIG = Object.freeze({ ORS: { baseUrl: '...' } });
// ❌ No hace window.CONFIG = CONFIG — queda atrapada en el scope del módulo

// ors.js
import { addIsochroneLayer } from './map.js';
// ❌ No importa CONFIG

// Dentro de ors.js, CONFIG es `undefined`
// CONFIG.ORS.key → TypeError: Cannot read property 'key' of undefined
// Pero si hay un fallback `CONFIG.ORS.key || 'fallback'`, el error se enmascara
```

### Síntomas
- La app funciona parcialmente (los módulos que no usan CONFIG van bien)
- Las llamadas a API fallan silenciosamente porque la key/config es `undefined`
- No hay errores en consola si hay fallbacks (`|| default`)
- El debug es difícil porque `typeof CONFIG` es `undefined` y no hay stack trace

### Solución

**Opción A — Importar CONFIG explícitamente en cada módulo que lo use:**
```js
// ors.js
import { CONFIG } from './config.js';
import { addIsochroneLayer } from './map.js';
// ✅ CONFIG ahora accesible
```

**Opción B — Exponer CONFIG globalmente desde el entry point:**
```js
// main.js (entry point, type="module")
import { CONFIG } from './config.js';
window.__CONFIG = CONFIG;  // Expone al scope global
// Ahora otros módulos pueden usar CONFIG si se importan como script tag
```

**Opción C — Usar un módulo de servicios con funciones en vez de datos:**
```js
// api.js
import { CONFIG } from './config.js';
export async function callORS(endpoint, body) {
  const resp = await fetch(`${CONFIG.ORS.baseUrl}${endpoint}`, {
    headers: { 'Authorization': CONFIG.ORS.key },
    body: JSON.stringify(body)
  });
  return resp.json();
}
// Los consumidores importan funciones, no CONFIG
```

### Pitfalls
- **`typeof process !== 'undefined'` en el navegador:** en algunos entornos (Webpack, Vite, NaN) `process` puede estar definido como polyfill. Verificar siempre que la lectura de env vars funciona en el browser real.
- **`path.extname('file.css?v=2')` devuelve `.css?v=2`:** siempre limpiar query params antes de calcular el content-type en servidores estáticos.
- **Los imports ES son estáticos:** no puedes hacer `import()` condicional dentro de un bloque `if` y esperar que el tree-shaker lo resuelva — usa `import()` dinámico.

## Referencias
- `references/auth-patterns.md` — Código completo de autenticación con sesiones
- `references/esm-interop-patterns.md` — Patrones de carga ESM de módulos IIFE
- `references/sqljs-patterns.md` — Patrones de sql.js, helpers, bug fixes
- `references/express-crud-routes.md` — Plantilla CRUD genérica
- `references/query-params-path-extname.md` — Bug de path.extname() con query strings y cache-busting
- `references/pedidos-venta-pattern.md` — Pedidos de venta: tablas, funciones DB, generación de número, cálculo de totales
