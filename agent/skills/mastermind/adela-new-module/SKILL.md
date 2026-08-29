---
name: adela-new-module
description: Scaffold y creación de nuevos módulos Adela siguiendo el ecosistema de piezas intercambiables
---

## Adela New Module

Skill para que un LLM cree un nuevo módulo Adela desde cero, siguiendo los estándares del ecosistema (TypeScript strict, zero-deps, TODO en castellano).

### Cuándo usarlo

- El usuario dice "crea un módulo Adela para X"
- Necesitas añadir una nueva pieza al ecosistema Adela
- El usuario pide "otro módulo como los que ya tenemos"
- El usuario da un roadmap multi-fase para mejorar Adela (seguridad, observabilidad, escalabilidad, API) — cargar `references/backend-roadmap.md` para entender las fases y categorías

### ⚠️ Regla CRÍTICA: Todos los repos Adela son PRIVADOS

**Cada módulo Adela se crea como repositorio PRIVADO en GitHub.** El usuario lo exige explícitamente. NO crear repos públicos.

### Categorías de módulos (nuevas desde v2.0)

| Categoría | Descripción | Ejemplos |
|-----------|-------------|----------|
| `infra` | Capa base — sin dependencias de otros Adela | time, env, http, cache, db |
| `core` | Capa funcional — depende de infra | auth, health, ai |
| `export` | Capa de exportación | export |
| `presentation` | Capa de interfaz | i18n, admin |
| `seguridad` | **NUEVA** — Seguridad y validación | security, rateLimit, validation |
| `observabilidad` | **NUEVA** — Logging y errores | logger, errors |
| `escalabilidad` | **NUEVA** — Escalado horizontal | db_pg, cache_redis |
| `api-layer` | **NUEVA** — Capa de API | pagination, router |

### Principio de explicación

El usuario quiere que **le expliques cómo funciona cada módulo**. Al crear un módulo nuevo:
- README.md debe explicar la arquitectura y el flujo
- Explicar por qué se eligió ese enfoque (no solo el qué, sino el porqué)
- Incluir diagramas de flujo ASCII cuando sea relevante

### Pasos

#### 1. Copiar template scaffold

```bash
cp -r /root/workspace/AdelaMasterMind/templates/adela-module-scaffold/ /root/workspace/Adela/Adela_<NOMBRE>/
```

#### 2. Rellenar package.json

Reemplazar placeholders `{{MODULE_NAME}}`, `{{MODULE_NAME_LOWERCASE}}`, `{{MODULE_DESCRIPTION}}`.

Reglas de dependencias:
- **Zero runtime deps** siempre que sea posible
- Si necesita base de datos → `sql.js`
- Si necesita auth → `bcryptjs`, `jsonwebtoken`
- Si necesita export → `csv-parse`, `csv-stringify`, `pdfkit`
- Si necesita fetch → usar `fetch()` nativo de Node (18+)

#### 3. Implementar src/

Estructura estándar:
```
src/
├── index.ts     # Barrel export: exporta todo
├── <modulo>.ts  # Implementación principal con createX() factory
└── types.ts     # Interfaces públicas
```

**Patrón multi-archivo:** Cuando un módulo tiene responsabilidades separadas (ej: implementación + formato de salida), dividir en archivos:
```
src/
├── index.ts        # Barrel export
├── metrics.ts      # Lógica principal (createMetrics, counter, histogram, gauge, middleware)
├── prometheus.ts   # Formato de exportación (toPrometheusFormat, toPrometheusJSON)
└── types.ts        # Tipos públicos
```
Cada archivo debe ser autocontenido y testable por separado. `index.ts` solo re-exporta.

**🔴 PITFALL — Token GitHub enmascarado:**
El `GITHUB_TOKEN` en `/hermes-home/.env` se muestra como `***` (enmascaramiento visual) pero es un PAT real de 40 caracteres. Sin embargo, **puede expirar entre llamadas consecutivas**, causando "Bad credentials" intermitentes.

**Patrón seguro:** siempre sourcear `.env` y usar el token en el mismo bloque de comando:
```bash
source /hermes-home/.env 2>/dev/null
# Usar $GITHUB_TOKEN inmediatamente en el mismo bloque
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" ...
```
Si el token falla, verificar si se expiró y reemplazarlo en `.env` con un nuevo PAT desde GitHub Settings → Developer Settings → Personal access tokens.

**🔴 PITFALL CRÍTICO — JWT en ESM con jsonwebtoken:**

`import * as jwt from 'jsonwebtoken'` crea un **namespace object** donde `jwt.verify` funciona pero `jwt.sign` NO existe como método directo. Esto causa fallos silenciosos: el login genera token OK pero el middleware lo rechaza como "inválido".

**Solución:** usar `createRequire` en TODOS los archivos que usen jsonwebtoken (routes Y middleware):
```typescript
import { createRequire } from 'node:module'
const require = createRequire(import.meta.url)
const jwt = require('jsonwebtoken')
// Ahora jwt.sign Y jwt.verify funcionan
```

**NUNCA mezclar:** un archivo con `import * as jwt` y otro con `require('jsonwebtoken')` = tokens que no se verifican.

**🔴 PITFALL CRÍTICO — JWT_SECRET compartido entre módulos:**

Si cada archivo (routes/auth.ts, middleware/auth.ts) genera su propio `process.env.JWT_SECRET || crypto.randomUUID()`, cada uno crea un UUID diferente. Resultado: el token se firma con el UUID de auth.ts pero se verifica con el UUID de middleware/auth.ts → siempre falla como "Token inválido".

**Solución:** un solo `config.ts` exporta el JWT_SECRET, todos los archivos importan de ahí:
```typescript
// src/config.ts
export const JWT_SECRET = process.env.JWT_SECRET || crypto.randomUUID()

// routes/auth.ts
import { JWT_SECRET } from '../config.js'

// middleware/auth.ts
import { JWT_SECRET } from '../config.js'
```

**NUNCA** generar JWT_SECRET inline en cada archivo. Siempre un módulo compartido.

**🔴 PITFALL — better-sqlite3 vs sql.js:**

`better-sqlite3` requiere compilación nativa (node-gyp + make). Si no hay `make` en el sistema, el `npm install` falla. En entornos sin herramientas de compilación, usar **`sql.js`** (JS puro, sin compilación):
```bash
npm install sql.js
```
Importación: `import initSqlJs from 'sql.js'` (async init).

**🔴 PITFALL — sql.js es en memoria: persistencia en archivo:**

sql.js por defecto guarda todo en memoria. Si el contenedor se reinicia, se pierden TODOS los datos. Para persistencia, exportar a archivo tras cada operación de escritura:

```typescript
import fs from 'fs'
import path from 'path'

const DB_PATH = process.env.DB_PATH || path.join(__dirname, '..', 'data', 'datos.db')

// Al iniciar: cargar desde archivo si existe
if (fs.existsSync(DB_PATH)) {
  const buffer = fs.readFileSync(DB_PATH)
  db = new SQL.Database(buffer)
} else {
  db = new SQL.Database()
}

// Después de CADA db.run() (INSERT, UPDATE, DELETE):
function saveDatabase() {
  const data = db.export()
  const buffer = Buffer.from(data)
  const dir = path.dirname(DB_PATH)
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true })
  fs.writeFileSync(DB_PATH, buffer)
}

// Wrapper que guarda automáticamente:
function run(sql: string, params: any[] = []) {
  db.run(sql, params)
  saveDatabase()  // ← persistir tras cada escritura
}
```

**Dockerfile:** crear directorio de datos y dar permisos:
```dockerfile
RUN mkdir -p /app/data
RUN chown -R appuser:appgroup /app
```

**Env var:** `DB_PATH=/app/data/datos.db` para rutas personalizadas.

**🔴 PITFALL — sql.js INSERT con valores undefined:**

Al hacer INSERT con sql.js, pasar `undefined` como valor de parámetro causa fallos silenciosos o errores de tipo. Siempre usar fallbacks:
```typescript
// ❌ MAL — data.descripcion puede ser undefined
db.run('INSERT INTO table (a, b, c) VALUES (?, ?, ?)',
  [id, data.nombre, data.descripcion])

// ✅ BIEN — fallbacks explícitos
db.run('INSERT INTO table (a, b, c) VALUES (?, ?, ?)',
  [id, data.nombre, data.descripcion || ''])
```
Regla: `|| ''` para strings, `|| 0` para números, `|| null` para NULL explícito.

**🔴 PITFALL — sql.js INSERT column ordering:**

Verificar que las columnas del INSERT coinciden con los valores. Un error común es poner `rol` como entero `1` en vez de string `'admin'` en el INSERT del usuario admin.

**🔴 PITFALL — sql.js db.run() devuelve void/Promise, no el objeto creado:**

`db.run()` NO devuelve el registro insertado. Si una función como `crearLead()` llama `db.run()` y luego construye el objeto manualmente, la función DEBE ser `async` y hacer `await db.run(...)`. Si la función del route no hace `await`, Express serializa la Promise como `{}` → respuesta vacía.

Síntoma: `{"lead":{}}` en POST, `{"leads":{}}` en GET, `{"stats":{}}` en stats. El objeto se construye bien internamente pero Express lo serializa vacío porque la función devuelve una Promise sin await.

**✅ Fix:** TODAS las funciones de route que llaman a `db.*()` deben ser `async` + `await`. TODAS las funciones en db.ts que llaman `db.run()` o `db.exec()` deben ser `async` + `await`.

**🔴 PITFALL — Template literal SQL: backtick de cierre al añadir tablas con patch:**

Al añadir un nuevo bloque `db.run(\`...\`)` al final de un bloque SQL existente usando `patch()`, el `old_string` DEBE incluir el backtick de cierre `\`)` del bloque anterior. Si no, se deja un `db.run()` sin cerrar, causando TS1005 '`,` expected' en todas las líneas SQL siguientes.

```typescript
// ❌ MAL — old_string sin el backtick de cierre del bloque anterior
// old_string: "CREATE INDEX ... ;\n\n  // Admin user"
// Resultado: el db.run() de las tablas base se queda abierto → TS1005 en todas las tablas nuevas

// ✅ BIEN — old_string incluye el cierre del bloque anterior
// old_string: "CREATE INDEX ... ;\n  `)\n\n  // Admin user"
// Resultado: el bloque anterior se cierra correctamente, el nuevo abre su propio db.run()

// new_string correcto:
// "CREATE INDEX ... ;\n  `)\n\n  // === Nuevo módulo ===\n  db.run(`\n    ...\n  `)\n\n  // Admin user"
```

**🔴 PITFALL — createRequire no va en types.ts:**

`createRequire` es para archivos runtime (db.ts, routes, middleware). Si se pone en `types.ts`, causa error TS1343: `import.meta` meta-property only allowed with module es2020/esnext/node16+. types.ts solo debe tener interfaces y tipos, nunca imports de runtime.

**🔴 PITFALL — Migración de datos al cambiar schema (admin pin_hash NULL):**

Cuando se actualiza el código para usar bcrypt en PINs, los usuarios existentes tienen `pin_hash = NULL` (creados con el código viejo). El login falla silenciosamente porque `bcrypt.compareSync(pin, null)` siempre devuelve false.

**Solución — migración automática en initDatabase():**
```typescript
// Después de CREATE TABLE, detectar y migrar:
const adminRow = db.exec("SELECT id, pin_hash FROM usuarios WHERE email = 'admin@adelacrm.local'")
if (adminRow[0]?.values[0][1] === null) {
  const pinHash = bcrypt.hashSync(String(process.env.ADMIN_PIN || '1234'), 10)
  db.run("UPDATE usuarios SET pin_hash = ? WHERE email = 'admin@adelacrm.local'", [pinHash])
  saveDatabase()
}
```

**Regla:** Siempre que se cambie el formato de un campo (plain → hash, string → enum, etc.), añadir migración automática en initDatabase() que detecte el formato viejo y lo actualice. Nunca asumir que la BD está vacía.

**🔴 PITFALL — API devuelve campos sensibles (pin_hash, password):**

Nunca devolver `pin_hash`, `password`, ni otros campos sensibles en respuestas API. Crear un helper `sanitizeUser()` en la ruta:

```typescript
function sanitizeUser(u: any) {
  const { pin_hash, ...rest } = u
  return rest
}

// En GET /usuarios:
const usuarios = await obtenerUsuarios()
res.json({ usuarios: usuarios.map(sanitizeUser) })

// En POST /usuarios (respuesta):
res.status(201).json({ usuario: sanitizeUser(usuario) })
```

**🔴 PITFALL — Admin PIN hardcodeado:**

Nunca hardcodear PINs de admin en el código fuente. Usar variable de entorno:
```typescript
// En db.ts, al crear el admin inicial:
const adminPin = process.env.ADMIN_PIN || '1234'
const pinHash = bcrypt.hashSync(String(adminPin), 10)
db.run("INSERT INTO usuarios ... VALUES (?, ?, ?, ?, ?, ?, ?)",
  ['admin-001', 'Administrador', 'admin@adelacrm.local', pinHash, 'admin', 1, ahora])
```

Documentar en `.env.example`:
```
ADMIN_PIN=1234
JWT_SECRET=tu-secreto-super-seguro
DB_PATH=/app/data/datos.db
```

**🔴 PITFALL — PIN visible en HTML (login hint):**

Nunca mostrar el PIN real en el HTML del login. En vez de `Demo: admin@local / 1234`, usar:
```html
<p class="hint">Credenciales de demostración en el README</p>
```

**🔴 PITFALL — Healthcheck en Dockerfile apunta a endpoint inexistente:**

Verificar que el healthcheck del Dockerfile usa el endpoint REAL del servidor. Error común: Dockerfile dice `/healthz` pero el servidor expone `/health`.
```dockerfile
# ❌ MAL — endpoint no existe
CMD wget -qO- http://localhost:9000/healthz || exit 1

# ✅ BIEN — coincide con el servidor
CMD wget -qO- http://localhost:9000/health || exit 1
```

**🔴 PITFALL — Express req.params.id es string | string[], no string:**

Al leer parámetros de ruta en Express, `req.params.id` devuelve `string | string[]` (el tipo de Express), no `string` directamente. Si se pasa a una función que espera `string`, TypeScript lanza TS2345.

```typescript
// ❌ MAL
const item = await obtenerPorId(req.params.id)  // TS2345: string | string[] no asignable a string

// ✅ BIEN — castear siempre
const id = req.params.id as string
const item = await obtenerPorId(id)
```

Regla: SIEMPRE hacer `const id = req.params.id as string` en handlers de rutas Express, tanto en GET/PUT/DELETE de una entidad como en rutas anidadas (`req.params.presupuestoId`, `req.params.lineaId`, etc.).

Las rutas estáticas (ej: `/stats`) deben definirse ANTES de las rutas con parámetros (ej: `/:id`). Si no, Express captura `/stats` como un ID. Esto es la causa #1 de "endpoint no encontrado" en Express.

**🔴 PITFALL — TypeScript module resolution:**

La combinación que funciona para proyectos ESM con `import.meta`, `createRequire`, y default imports depende del tipo de módulo:

**Para módulos backend (Express, sql.js, JWT):**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true
  }
}
```

**Para módulos CLI o con dynamic imports (`import()` en tests, `__dirname`):**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true
  }
}
```
- `"bundler"` funciona con `import()` dinámico en tests, `__dirname` implícito, y default imports
- `module: "NodeNext"` + `esModuleInterop: true` = conflicto
- `module: "Node16"` + `import.meta` = error de compilación
- **Siempre verificar con `npx tsc --noEmit`** — el linter del editor a veces da falsos positivos con `@types/node`

**🔴 PITFALL — Importar paquetes CommonJS en ESM (ws, nodemailer, bullmq, multer):**

Paquetes como `ws`, `nodemailer`, `bullmq`, `multer` son CommonJS (`module.exports`). Con `module: "ES2022"` + `moduleResolution: "bundler"`, un `import X from 'ws'` falla porque los tipos no coinciden con default import.

**Solución:** usar `createRequire` + `any`:
```typescript
import { createRequire } from 'node:module'
import type { ServerOptions, Server as WSServer, WebSocket as WSWebSocket } from 'ws'

const require = createRequire(import.meta.url)
const wsModule: any = require('ws')

// Uso:
const wss = new wsModule.Server({ noServer: true })
// Tipos se importan como type-only desde 'ws'
```

**Reglas:**
- **NUNCA** `import WebSocket from 'ws'` — el default import no existe en ESM para este paquete
- **NUNCA** `import * as ws from 'ws'` — da `TS1259: can only be default-imported using esModuleInterop`
- **SIEMPRE** `createRequire` + `any` para la parte runtime
- **SIEMPRE** `import type { ... }` para los tipos
- El `any` cast es seguro: `require('ws')` devuelve el namespace completo con `Server`, `WebSocket`, etc.

**Ejemplo completo:**
```typescript
import { createRequire } from 'node:module'
import type { ServerOptions, Server as WSServer } from 'ws'

const require = createRequire(import.meta.url)
const wsModule: any = require('ws')

class MyServer {
  private wss: WSServer | null = null
  attach() {
    this.wss = new wsModule.Server({ noServer: true })
  }
}
```

**🔴 PITFALL — Multer en ESM: `require('multer')` vs `import * as multer`:**

`multer` es CommonJS y `@types/multer` tiene tipos que chocan con `@types/express` en strict mode. `import * as multer from 'multer'` falla porque multer no tiene un default export en ESM.

**Solución:** `createRequire` + `any`, con `moduleResolution: "node"` en tsconfig:
```typescript
import { createRequire } from 'node:module'
import type { Multer } from 'multer'

const require = createRequire(import.meta.url)
const multer: any = require('multer')

const upload = multer({ storage: multer.diskStorage({ ... }) })
```

**Callbacks de multer sin tipos:** Como `multer` es `any`, los callbacks de `diskStorage` y `fileFilter` no se tipan automáticamente. Añadir `: any` explícito:
```typescript
const storage = multer.diskStorage({
  destination: (_req: any, _file: any, cb: any) => cb(null, './uploads'),
  filename: (_req: any, file: any, cb: any) => cb(null, `${Date.now()}-${file.originalname}`)
})
```

**tsconfig.json para proyectos con multer:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "verbatimModuleSyntax": false
  }
}
```
- `moduleResolution: "node"` (NO `bundler`) — `bundler` causa error TS1343 con `import.meta` cuando se usan `node:*` con default imports (`import crypto from 'node:crypto'`)
- `verbatimModuleSyntax: false` — necesario porque `node:*` módulos no tienen default exports en los tipos de `@types/node`
- `bundler` era el error anterior: funciona para `import.meta` pero rompe los imports de `node:crypto`, `node:fs`, `node:path`
- **Siempre verificar con `npx tsc`** — el linter del editor a veces da falsos positivos con `@types/node`

**🔴 PITFALL — Tipos de flags de parseArgs (`string | boolean`):**

Al parsear argumentos de CLI, `parsed.flags[key]` tiene tipo `string | boolean`. Si se asigna directamente a un campo `string` en una interfaz de config, TypeScript lanza error:

```typescript
// ❌ MAL — Type 'string | true' is not assignable to type 'string'
if (parsed.flags.author) {
  config.author = parsed.flags.author  // ERROR: boolean no assignable a string
}
```

**Solución:** siempre hacer type guard antes de asignar:
```typescript
// ✅ BIEN
if (parsed.flags.author) {
  config.author = typeof parsed.flags.author === 'string' ? parsed.flags.author : ''
}
```

**NUNCA** asignar `parsed.flags.*` directamente a campos typed de config — siempre verificar el tipo.

**🔴 PITFALL — Tipos exportados entre archivos del mismo módulo:**

Si un archivo importa un tipo desde otro archivo del mismo módulo (`import type { Foo } from './types.js'`), pero ese tipo no se re-exporta desde `index.ts`, los archivos que importan desde `index.js` no tendrán acceso al tipo.

**Solución:** si un tipo es usado por múltiples archivos internos, re-exportarlo desde `index.ts`:
```typescript
export type { TemplateContext } from './types.js'
```

**🔴 PITFALL — Sort: numeric comparison BEFORE date parsing:**

Cuando un módulo de ordenación (`sort`) intenta detectar fechas ISO, `new Date(30)` (un número pequeño) se convierte en una fecha válida (epoch 30ms). Si la comprobación de fechas se ejecuta ANTES de la comprobación numérica, los números se clasifican erróneamente como fechas.

**Solución:** En `compareValues()`, siempre verificar numérico ANTES de fechas:
```typescript
function compareValues(a: unknown, b: unknown, direction: SortDirection): number {
  // 1. Normalizar null/undefined
  if (a === null || a === undefined) a = ''
  if (b === null || b === undefined) b = ''

  // 2. NUMÉRICO PRIMERO — antes de fechas
  const numA = typeof a === 'number' ? a : parseFloat(String(a))
  const numB = typeof b === 'number' ? b : parseFloat(String(b))
  if (!isNaN(numA) && !isNaN(numB) && typeof a !== 'boolean' && typeof b !== 'boolean') {
    return direction === 'asc' ? numA - numB : numB - numA
  }

  // 3. FECHAS DESPUÉS
  const dateA = parseDateValue(a)
  const dateB = parseDateValue(b)
  if (dateA !== null && dateB !== null) {
    return dateA.getTime() - dateB.getTime()
  }

  // 4. Strings como fallback
  ...
}
```

**🔴 PITFALL — Cursor-based pagination: hash no es invertible:**

Usar un hash (MD5, SHA, simpleHash) para generar cursores a partir de offsets crea un problema: el hash es unidireccional, no puedes revertirlo para obtener el offset original. Si el cliente envía un cursor generado por tu API, no puedes saber qué offset representa.

**Solución:** Usar formato numérico directo `c_<offset>` para cursores explícitos. Los cursores generados internamente se tratan como "inicio" (offset 0). Si necesitas cursores verdaderamente seguros (no manipulables), firmar el cursor con HMAC:
```typescript
function generateCursor(offset: number, secret: string): string {
  const payload = `${offset}`
  const hmac = createHmac('sha256', secret).update(payload).digest('hex').slice(0, 16)
  return `c_${hmac}_${offset}`
}

function parseCursor(cursor: string, secret: string): number {
  const parts = cursor.split('_')
  if (parts.length !== 3 || parts[0] !== 'c') return 0
  const expectedHmac = createHmac('sha256', secret).update(parts[2]).digest('hex').slice(0, 16)
  if (parts[1] !== expectedHmac) return 0 // Cursor manipulado → rechazar
  return parseInt(parts[2], 10)
}
```

**🔴 PITFALL — TypeScript generics: filter/sort necesitan `T extends Record<string, unknown>`:**

La interfaz `ApiHelpers` debe declarar `filter<T extends Record<string, unknown>>` y `sort<T extends Record<string, unknown>>` para que coincidan con las implementaciones reales. Si se declara como `filter<T>` simple, TypeScript rechaza asignar la implementación porque `T[]` no es assignable a `Record<string, unknown>[]`.

```typescript
// ❌ MAL — type mismatch
interface ApiHelpers {
  filter<T>(items: T[], options: FilterOptions): T[]
  sort<T>(items: T[], options: SortOptions): T[]
}

// ✅ BIEN — con constraint
interface ApiHelpers {
  filter<T extends Record<string, unknown>>(items: T[], options: FilterOptions): T[]
  sort<T extends Record<string, unknown>>(items: T[], options: SortOptions): T[]
}
```

#### 3b. Template de proyecto completo (Express + TypeScript + ESM)

Para proyectos que necesitan backend Express + frontend estático (CRM, dashboards, etc.), usar el template en `references/adela-express-template.md`. Incluye:
- tsconfig.json con `module: "ES2022"`, `moduleResolution: "node"` (combinación que funciona)
- Patrón `createRequire` para jsonwebtoken en middleware y routes
- sql.js como driver de base de datos (sin compilación nativa)
- Estructura de rutas Express con auth middleware
- Dockerfile para NaN (puerto configurable, USER appuser, healthcheck)
- Patrón db.ts con initDatabase() singleton
- Reglas de oro para evitar los 5 pitfalls más comunes

#### Referencias

- `references/multer-esm-pattern.md` — Patrón ESM para multer: createRequire + bundler moduleResolution + any cast
- `references/jwt-esm-pattern.md` — Patrón seguro para jsonwebtoken en ESM (createRequire, no import *)
- `references/adela-api-reference.md` — Referencia completa del módulo Adela_api (pagination, filter, sort patterns, pitfalls)
- `references/common-test-failures.md` — Errores comunes de tests
- `references/adela-express-template.md` — Template completo para proyectos Express + TypeScript + ESM + sql.js + JWT (CRM, dashboards)
- `references/prometheus-pattern.md` — Patrón para módulos que exponen métricas Prometheus-compatible
- `references/adela-cli-lessons.md` — Lecciones de la creación de Adela_cli: moduleResolution, type exports, parseArgs types
- `templates/adela-express-project/` — Template proyecto Express + TS + ESM
- `templates/adela-express-project/` — Template proyecto Express + TS + ESM

Factory pattern:
```typescript
export async function createMiModulo(config?: MiModuloOptions): Promise<MiModulo> {
  const impl = new MiModuloImpl(config)
  // setup async si necesario
  return impl
}
```

#### 4. Escribir tests

Mínimo 8 tests. **Test runner:** usar `vitest` (recomendado) o `tsx --test` (node:test nativo).

**🔴 PITFALL CRÍTICO — Test runner mismatch (CAUSA EL 50% DE FALLOS):**

El script en `package.json` **DEBE** coincidir EXACTAMENTE con los imports del archivo de test. Si no coinciden, los tests fallan con errores crípticos (`TypeError: Cannot read properties of undefined`, `no tests`, o `suites 0`).

| Imports del test | Script en package.json |
|------------------|----------------------|
| `import { describe, it } from 'vitest'` | `"test": "vitest run"` |
| `import { describe, it } from 'node:test'` | `"test": "tsx --test tests/*.test.ts"` |

**NUNCA mezclar.** Ejemplo de lo que FALLA:
```typescript
// ❌ FALLO: imports de vitest + runner de node:test
import { describe, it, expect } from 'vitest';
// package.json: "test": "tsx --test tests/*.test.ts"  ← WRONG
```

```typescript
// ✅ OK: ambos coinciden
import { describe, it, expect } from 'vitest';
// package.json: "test": "vitest run"  ← CORRECT
```

**Después de crear tests, SIEMPRE verificar la alineación** (ver paso 5b).

```typescript
// Opción A: vitest (recomendado para módulos nuevos)
import { describe, it, expect } from 'vitest';
// package.json: "test": "vitest run"

// Opción B: node:test
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
// package.json: "test": "tsx --test tests/*.test.ts"
```

#### 5. Verificar

```bash
cd /root/workspace/Adela/Adela_<NOMBRE>/
npm test
npm run build
```

#### 5b. Verificar alineación test runner (OBLIGATORIO post-creación)

**Este paso ha causado el 50% de los fallos en el ecosistema.** No saltárselo.

```bash
# Extraer runner del package.json
RUNNER=$(grep -o '"test": "[^"]*"' package.json | cut -d'"' -f4)

# Extraer imports del primer archivo de test
IMPORTS=$(head -5 tests/*.test.ts | grep "from 'vitest\|from 'node:test")

# Verificar coherencia
if echo "$IMPORTS" | grep -q "vitest" && echo "$RUNNER" | grep -q "vitest"; then
  echo "✅ vitest alignment OK"
elif echo "$IMPORTS" | grep -q "node:test" && echo "$RUNNER" | grep -q "tsx --test"; then
  echo "✅ node:test alignment OK"
else
  echo "❌ MISMATCH — imports: $IMPORTS | runner: $RUNNER"
  echo "   FIX: cambiar el script en package.json para que coincida con los imports"
fi
```

Si hay mismatch, arreglar el `package.json` ANTES de hacer commit.

### ⚠️ Pitfall: Subagent timeout en módulos grandes

Los subagentes (delegate_task) tienen timeout de 600s con ~27 calls. Si el módulo es grande (Admin, Auth, Export), el subagente **crea todos los archivos pero no llega a verificar tests/build**.

**Patrón seguro para módulos grandes (>8 archivos fuente):**

1. Delegar SOLO la escritura de archivos al subagente (src/, tests/, package.json, tsconfig)
2. **Siempre verificar manualmente después:**
   ```bash
   find /root/workspace/Adela/Adela_<NOMBRE> -type f -not -path "*/node_modules/*" -not -path "*/dist/*" | sort
   ```
3. Ejecutar tests y build directamente (NO delegar de nuevo):
   ```bash
   cd /root/workspace/Adela/Adela_<NOMBRE>
   npm test
   npm run build
   ```
4. Si tests fallan o build no compila, arreglar con patch/write_file directo

**Nunca re-delegar** una verificación que el primer subagente no completó — es más rápido hacerlo directo y evita otro timeout.

### ⚠️ Pitfall: Archivos de test >1200 líneas causan timeout

**Señal:** delegate_task con goal de crear 20+ tests falla con timeout (>600s). El subagente crea el archivo pero no verifica.

**Solución:** Archivos de test grandes (>1200 líneas, >15 tests) crearlos directamente con `write_file`, NO delegar. delegate_task funciona bien para ≤15 tests por subagente.

**Patrón de tests CRM con node:test + supertest:**
```typescript
import { describe, it, before } from 'node:test'
import assert from 'node:assert/strict'
import request from 'supertest'
import app from '../src/app.js'
import { initDatabase } from '../src/db.js'

describe('Módulo', () => {
  let token = ''
  before(async () => {
    await initDatabase()
    const login = await request(app)
      .post('/api/auth/login')
      .send({ email: 'admin@adelacrm.local', pin: '1234' })
    token = login.body.token
  })
  it('1) crear', async () => { /* ... */ })
})
```

Package.json: `"test": "tsx --test tests/*.test.ts"` (debe coincidir con imports de `node:test`).

#### 6. Actualizar registry.json

Añadir entrada en `/root/workspace/AdelaMasterMind/registry.json` con:
```json
{
  "id": "Adela_<NOMBRE>",
  "version": "1.0.0",
  "status": "stable",
  "description": "...",
  "tests": N,
  "runtimeDeps": [...],
  "dependsOn": [...],
  "github": "https://github.com/Ntizar/Adela_<NOMBRE>",
  "exports": [...],
  "category": "infra|core|export|presentation|seguridad|observabilidad|escalabilidad|api-layer"
}
```

#### 7. Crear repo PRIVADO en GitHub

**IMPORTANTE: Siempre privado.** El usuario lo exige.

```bash
source /hermes-home/.env 2>/dev/null
MODULO="Adela_<NOMBRE>"

# Crear repo privado vía API
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$MODULO\",\"private\":true,\"description\":\"...\",\"auto_init\":false}" > /dev/null

# Configurar remote y push
cd /root/workspace/Adela/$MODULO
git init
git remote add origin "https://Ntizar:$GITHUB_TOKEN@github.com/Ntizar/$MODULO.git"
git add .
git commit -m "feat: initial commit $MODULO v1.0.0"
git branch -M main
git push -u origin main

# Verificar que es privado
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/Ntizar/$MODULO" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print('PRIVADO ✅' if d.get('private') else 'PÚBLICO ❌')"
```

#### 8. Actualizar módulos dependientes

Si el nuevo módulo está en la categoría `seguridad`, `observabilidad`, `escalabilidad` o `api-layer`:
- Revisar qué módulos existentes podrían beneficiarse de integrarlo
- Actualizar sus dependencias en package.json si procede
- Registrar en el roadmap los módulos actualizados

### 📦 Memoria: mantener compacta

El módulo nuevo y sus stats (tests, archivos, bugs conocidos) deben caber en una entrada de memoria existente. Si la memoria está llena:
- **NO añadir entrada nueva** — reemplazar la existente de Adela, condensando info
- Patrón: `[adela] Ecosistema Adela vX: N módulos (~N tests). <nuevos>. <bugs>.`
- Priorizar: qué módulos existen > tests totales > bugs conocidos

### ⚠️ Pitfall: Algoritmos de distancia de cadenas (Levenshtein)

Si el módulo incluye fuzzy matching o distancia de cadenas, **cuidado con el swap en la optimización de dos filas de Levenshtein**:

- `fuente` debe ser el string **más largo** (iterado con `i`)
- `objetivo` debe ser el string **más corto** (iterado con `j`)
- El costo compara `objetivo[j-1]` vs `fuente[i-1]`
- Verificar con `levenshtein('a', 'abc')` → debe ser 2, no 3

Ver `references/levenshtein-swap-bug.md` en el skill `systematic-debugging` para el patrón correcto.

### 🔴 PITFALL — Cadena de hash VeriFactu: orden y datos mutables

**Cadena de hash SHA-256** — Las facturas se encadenan con `verifactuHashAnterior` → `verifactuHash`. Para verificar la integridad:

**Pitfall 1 — Orden de consulta:** `obtenerFacturas()` ordena por `creado DESC` por defecto. La verificación necesita orden cronológico ASC. Solución: `.sort((a, b) => a.creado.localeCompare(b.creado))` después de filtrar facturas emitidas.

**Pitfall 2 — Hash incluye datos mutables:** El hash se calcula al crear la factura con `total`. Si el total cambia después (ej: al emitir se recalcula desde líneas de factura), la verificación falla porque el hash ya no coincide con los datos actuales.

**Solución de diseño (si se necesita verificación fiable a largo plazo):**
- Opción A: No incluir `total` en el hash (solo campos inmutables: `id`, `numero`, `empresaId`, `creado`)
- Opción B: Almacenar el raw data que se hashó originalmente, y verificar contra ese snapshot
- Opción C: Solo verificar facturas que no han sido modificadas después de la primera emisión

**En la práctica (AdelaCRM):** La verificación funciona para facturas recién emitidas. Facturas anteriores cuyo `total` cambió no verificarán — el test lo acepta como esperado.

**Ruta de verificación (Express):**
```typescript
// Las rutas estáticas DEBEN ir ANTES de /:id
router.get('/verifactu/verificar', ...)  // ← PRIMERO
router.get('/:id', ...)                  // ← DESPUÉS
// Si no, Express captura "verifactu" como un :id
```

**Endpoint de anulación:**
```typescript
router.post('/:id/anular', async (req, res) => {
  // Solo facturas emitidas/cobradas se anulan (no borradores — esos se eliminan)
  // El hash chain se mantiene: la factura anulada conserva su hash
})
```

### Checklist de calidad

- [ ] TypeScript strict mode
- [ ] package.json correcto (name, version, type, scripts)
- [ ] **Test runner ALINEADO** con imports (vitest↔vitest, node:test↔tsx --test)
- [ ] Tests pasan
- [ ] Build compila
- [ ] README con Quick Start + API + Integración + explicación de arquitectura
- [ ] Zero deps o justificadas
- [ ] TODO en castellano
- [ ] registry.json actualizado (con categoría correcta)
- [ ] Repo PRIVADO en GitHub ✅
- [ ] Push a GitHub exitoso
- [ ] Si es nueva categoría (seguridad/observabilidad/escalabilidad/api-layer): roadmap actualizado

### Creación en batch vía cron jobs

Cuando hay múltiples módulos nuevos, **NO crear todos de golpe** — causa crashes por contexto saturado. Usar cron jobs secuenciales:

```
Cada cron job:
1. Carga skill adela-new-module
2. Crea UN solo módulo
3. Verifica tests + build
4. Actualiza registry.json
5. Push a GitHub privado
6. Notifica resultado
```

**Configuración típica:** `every 2h` entre módulos para dar tiempo a completar.
**Prompt del cron:** Debe ser autocontenido — incluir convenciones, estructura, y el módulo específico a crear.

**Plan documentado:** `/root/workspace/Adela/PLAN-MODULOS-NUEVOS.md` con análisis por proyecto y prioridades.