# Template: Proyecto Express + TypeScript + ESM para Adela

## Estructura de archivos

```
proyecto/
├── Dockerfile              # Deploy en NaN (puerto configurable)
├── .dockerignore           # node_modules, .git, .env
├── .env.example            # Variables de entorno documentadas
├── package.json
├── tsconfig.json
├── src/
│   ├── types.ts            # Interfaces públicas
│   ├── db.ts               # Capa de base de datos (sql.js)
│   ├── server.ts           # Express app + rutas + listen
│   ├── middleware/
│   │   └── auth.ts         # JWT verification middleware
│   └── routes/
│       ├── auth.ts         # POST /login
│       ├── leads.ts        # CRUD principal
│       ├── usuarios.ts     # CRUD usuarios (admin)
│       └── oportunidades.ts # CRUD oportunidades
├── public/
│   ├── index.html          # Frontend SPA
│   ├── css/
│   │   └── crm.css         # Estilos Aurora
│   └── js/
│       └── crm.js          # Lógica frontend
└── tests/
    └── api.test.ts         # Tests integración
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

## package.json

```json
{
  "name": "adelacrm",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "tsx watch src/server.ts",
    "test": "tsx --test tests/*.test.ts"
  },
  "dependencies": {
    "bcryptjs": "^2.4.3",
    "express": "^4.21.0",
    "jsonwebtoken": "^9.0.2",
    "sql.js": "^1.10.3"
  },
  "devDependencies": {
    "@types/bcryptjs": "^2.4.6",
    "@types/express": "^5.0.0",
    "@types/jsonwebtoken": "^9.0.7",
    "@types/supertest": "^6.0.2",
    "supertest": "^7.0.0",
    "typescript": "^5.6.0",
    "tsx": "^4.19.0"
  }
}
```

## Dockerfile

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY dist/ ./dist/
COPY public/ ./public/
RUN mkdir -p /data
ENV PORT=9000
ENV DB_PATH=/data/datos.db
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown -R appuser:appgroup /app
USER appuser
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:9000/health || exit 1
EXPOSE 9000
CMD ["node", "dist/server.js"]
```

> ⚠️ Verificar que el healthcheck usa `/health` (no `/healthz`) — tiene que coincidir con el endpoint real del servidor.

## Patrón config.ts (JWT_SECRET compartido)

```typescript
// src/config.ts — una sola fuente de verdad
export const JWT_SECRET = process.env.JWT_SECRET || crypto.randomUUID()
```

## Patrón auth middleware

```typescript
import { createRequire } from 'node:module'
import { JWT_SECRET } from '../config.js'
import express from 'express'
const jwt = createRequire(import.meta.url)('jsonwebtoken')

export interface AuthRequest extends express.Request {
  usuario?: { id: string; email: string; rol: string }
}

export function requerirAuth(req: AuthRequest, res: express.Response, next: express.NextFunction) {
  const authHeader = req.headers.authorization
  if (!authHeader?.startsWith('Bearer ')) {
    res.status(401).json({ error: 'No autenticado' })
    return
  }
  try {
    const token = authHeader.split(' ')[1]
    const decoded = jwt.verify(token, JWT_SECRET) as { id: string; email: string; rol: string }
    req.usuario = decoded
    next()
  } catch {
    res.status(401).json({ error: 'Token inválido' })
  }
}
```

> ⚠️ NUNCA generar JWT_SECRET inline en cada archivo. Siempre importar de `config.ts`.

## Patrón db.ts con sql.js + persistencia en archivo

```typescript
import initSqlJs from 'sql.js'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
// En NaN con volumen persistente: DB_PATH=/data/datos.db (montado por PVC)
// En local: DB_PATH=./data/datos.db
const DB_PATH = process.env.DB_PATH || '/data/datos.db'

let db: any = null
let sqlReady = false

export async function initDatabase() {
  if (sqlReady && db) return db
  const SQL = await initSqlJs()

  // Cargar desde archivo si existe
  if (fs.existsSync(DB_PATH)) {
    const buffer = fs.readFileSync(DB_PATH)
    db = new SQL.Database(buffer)
  } else {
    db = new SQL.Database()
  }

  // CREATE TABLE...
  // INSERT admin (con bcrypt, PIN desde env var):
  const bcrypt = await import('bcryptjs')
  const adminPin = process.env.ADMIN_PIN || '1234'
  const pinHash = bcrypt.hashSync(String(adminPin), 10)
  // db.run("INSERT INTO usuarios ...", [..., pinHash, ...])

  sqlReady = true
  saveDatabase()
  return db
}

function saveDatabase() {
  if (!db) return
  const dir = path.dirname(DB_PATH)
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true })
  const data = db.export()
  fs.writeFileSync(DB_PATH, Buffer.from(data))
}

function run(sql: string, params: any[] = []) {
  if (!db) throw new Error('Database not initialized')
  db.run(sql, params)
  saveDatabase()  // persistir tras cada escritura
}
```

## Deploy en NaN con volumen persistente

1. Crear app en `cloud.nanBuilders` desde GitHub repo
2. **Activar "Persistent storage"** al crear (no se puede añadir después)
3. Volume size: `1Gi` mínimo
4. Container Port: `9000`
5. NaN monta `/data` automáticamente via PersistentVolumeClaim
6. DB_PATH debe ser `/data/datos.db` (coincide con el mount point)
7. Push a GitHub → NaN auto-despliega, `/data` se mantiene entre reinicios
8. **⚠️ Borrar la app = borrar el volumen** (sin backup automático)

> Si la app ya existe sin volumen → crear app NUEVA con Persistent ON, no se puede añadir a una existente.

## Reglas de oro

1. **TODAS las funciones en db.ts que llaman `db.run()` deben ser `async` + `await`**
2. **TODAS las funciones de route que llaman `db.*()` deben ser `async` + `await`**
3. **Rutas estáticas ANTES de rutas con parámetros** (`/stats` antes de `/:id`)
4. **sql.js INSERT: nunca pasar undefined** → usar `|| ''`, `|| 0`, `|| null`
5. **jsonwebtoken: usar `createRequire`** en TODOS los archivos (routes Y middleware)
6. **JWT_SECRET: un solo config.ts** — NUNCA generar inline en cada archivo
7. **Puerto: alinear 3 sitios** → Dockerfile ENV, server.ts default, healthcheck
8. **Dockerfile: siempre USER appuser + EXPOSE correcto + healthcheck `/health`**
9. **Admin PIN desde env var** (`ADMIN_PIN`) — nunca hardcodear
10. **API: filtrar pin_hash** con `sanitizeUser()` — nunca devolver campos sensibles
11. **sql.js: persistir en archivo** con `saveDatabase()` tras cada `db.run()`
