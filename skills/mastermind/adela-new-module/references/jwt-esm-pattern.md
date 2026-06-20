# JWT en ESM con jsonwebtoken

## El problema

`import * as jwt from 'jsonwebtoken'` crea un **namespace object** en ESM:
- `jwt.verify()` → funciona (existe como método en el namespace)
- `jwt.sign()` → **NO funciona** → `TypeError: jwt.sign is not a function`

Esto causa fallos silenciosos: el login genera token OK pero el middleware lo rechaza.

## Solución: createRequire

Usar `createRequire` de `node:module` en **TODOS** los archivos que usen jsonwebtoken:

```typescript
import { createRequire } from 'node:module'
const require = createRequire(import.meta.url)
const jwt = require('jsonwebtoken')

// Ahora jwt.sign Y jwt.verify funcionan correctamente
const token = jwt.sign(payload, secret, { expiresIn: '24h' })
const decoded = jwt.verify(token, secret)
```

## Regla

**Si un archivo usa `require('jsonwebtoken')`, TODOS los archivos del proyecto deben usar `require('jsonwebtoken')`.** Mezclar `import * as jwt` con `require('jsonwebtoken')` = tokens que no se verifican entre sí.

## Referencia

- jsonwebtoken no tiene default export → `import jwt from 'jsonwebtoken'` falla con `TS1192`
- `import * as jwt` funciona para verify pero NO para sign
- `createRequire` es el patrón seguro para ESM + jsonwebtoken
