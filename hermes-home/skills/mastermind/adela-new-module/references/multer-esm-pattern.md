# Patrón ESM para multer — Actualizado 2026-06-15

## Problema

`multer` es un paquete CommonJS (`module.exports`). Al usarlo en un módulo ESM con TypeScript strict:

- `import multer from 'multer'` → error: no default export en ESM
- `import * as multer from 'multer'` → error: `TS1259: can only be default-imported using esModuleInterop`
- `@types/multer` tipos chocan con `@types/express` en strict mode (callback params mismatch)

## Solución: `createRequire` + `any`

```typescript
import { createRequire } from 'node:module'
import type { Multer } from 'multer'

const require = createRequire(import.meta.url)
const multer: any = require('multer')

const upload = multer({
  storage: multer.diskStorage({
    destination: (req, file, cb) => cb(null, './uploads'),
    filename: (req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`)
  })
})
```

## tsconfig.json correcto

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

**¿Por qué `node` y NO `bundler`?**

`moduleResolution: "bundler"` causa **error TS1343** con `import.meta` cuando el código usa `node:*` con default imports (`import crypto from 'node:crypto'`). El compilador no permite `import.meta` con `bundler` + `node:*` default imports simultáneamente.

`moduleResolution: "node"` + `esModuleInterop: true` permite ambos:
- Default imports de `node:crypto`, `node:fs`, `node:path` ✅
- `import.meta.url` ✅
- `createRequire()` ✅
- Multer con `require()` ✅

**`verbatimModuleSyntax: false`** es necesario porque `@types/node` no declara default exports para los módulos `node:*`.

## Callbacks de multer

Como `multer` es `any`, los callbacks no se tipan automáticamente. Añadir `: any` explícito:

```typescript
const storage = multer.diskStorage({
  destination: (_req: any, _file: any, cb: any) => cb(null, './uploads'),
  filename: (_req: any, file: any, cb: any) => cb(null, `${Date.now()}-${file.originalname}`)
})
```

## Historial

- **2026-06-15:** Cambiado de `bundler` a `node` tras crear Adela_files. `bundler` causaba TS1343 con `import.meta` + `node:*` imports.
- Versión anterior recomendaba `bundler` (error de la skill original).
