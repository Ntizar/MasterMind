# Importar paquetes CommonJS en módulos ESM TypeScript

## El problema

Paquetes CommonJS (`module.exports`) como `ws`, `nodemailer`, `bullmq` no se pueden importar con sintaxis ESM estándar en TypeScript con `module: "ES2022"` + `moduleResolution: "bundler"`.

### Lo que FALLA

```typescript
// ❌ Error TS1259: can only be default-imported using esModuleInterop
import WebSocket from 'ws'

// ❌ Error TS2694: Namespace 'WebSocket' has no exported member 'Server'
import * as ws from 'ws'
const wss = new ws.Server(...)
```

### Lo que FUNCIONA

```typescript
import { createRequire } from 'node:module'
import type { ServerOptions, Server as WSServer, WebSocket as WSWebSocket } from 'ws'

const require = createRequire(import.meta.url)
const wsModule: any = require('ws')

const wss = new wsModule.Server({ noServer: true })
// wsModule.WebSocket, wsModule.createWebSocketStream, etc.
```

## Por qué funciona

- `createRequire(import.meta.url)` crea un `require()` en contexto ESM
- `require('ws')` devuelve el namespace completo del paquete CommonJS
- El `any` cast es necesario porque TypeScript no conoce el tipo de `require()`
- Los tipos se importan por separado con `import type` desde `@types/ws`
- En runtime, `require('ws')` devuelve `{ Server, WebSocket, createWebSocketStream, ... }`

## Patrón reutilizable para cualquier paquete CJS

```typescript
import { createRequire } from 'node:module'
import type { SomeType } from 'algún-paquete-cjs'

const require = createRequire(import.meta.url)
const pkg: any = require('algún-paquete-cjs')

// Uso:
const instance = new pkg.Constructor(options)
```

## Paquetes conocidos que necesitan este patrón

| Paquete | Uso típico |
|---------|-----------|
| `ws` | WebSocket server |
| `nodemailer` | Envío de emails |
| `bullmq` | Colas de trabajo |
| `ioredis` | Cliente Redis |
