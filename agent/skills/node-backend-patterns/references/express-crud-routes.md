# Express CRUD Route Files — Patrón de Routes con Router + DB Functions

Patrón para crear ficheros de rutas REST CRUD en Express/TypeScript con funciones de base de datos importadas.

## Estructura básica

```
src/routes/<entidad>.ts
```

## Plantilla

```ts
import { Router } from 'express'
import { obtener<Entidad>s, obtener<Entidad>PorId, crear<Entidad>, actualizar<Entidad>, eliminar<Entidad> } from '../db.js'
import type { AuthRequest } from '../middleware/auth.js'

const router = Router()

// GET / — Lista (soporta filtros opcionales vía query params)
router.get('/', async (req: AuthRequest, res) => {
  try {
    // Parsear filtros desde req.query
    const activo = typeof req.query.activo === 'string'
      ? (req.query.activo === 'true' ? true : req.query.activo === 'false' ? false : undefined)
      : undefined
    const items = await obtener<Entidad>s(activo !== undefined ? { activo } : undefined)
    res.json({ <entidadLower>s: items })
  } catch (error) {
    res.status(500).json({ error: 'Error al obtener <entidadLower>s' })
  }
})

// GET /:id — Obtener por ID
router.get('/:id', async (req, res) => {
  try {
    const id = req.params.id as string
    const item = await obtener<Entidad>PorId(id)
    if (!item) { res.status(404).json({ error: '<Entidad> no encontrado' }); return }
    res.json({ <entidadLower>: item })
  } catch (error) {
    res.status(500).json({ error: 'Error al obtener <entidadLower>' })
  }
})

// POST / — Crear
router.post('/', async (req: AuthRequest, res) => {
  try {
    const { campo1, campo2, campoObligatorio } = req.body
    if (!campoObligatorio) { res.status(400).json({ error: 'El campo obligatorio es requerido' }); return }
    const item = await crear<Entidad>({ campo1, campo2, campoObligatorio })
    res.status(201).json({ <entidadLower>: item })
  } catch (error: any) {
    if (error?.message?.includes('UNIQUE')) {
      res.status(409).json({ error: 'Ya existe un registro con ese identificador' }); return
    }
    res.status(500).json({ error: 'Error al crear <entidadLower>' })
  }
})

// PUT /:id — Actualizar (parcial)
router.put('/:id', async (req: AuthRequest, res) => {
  try {
    const id = req.params.id as string
    const item = await actualizar<Entidad>(id, req.body)
    if (!item) { res.status(404).json({ error: '<Entidad> no encontrado' }); return }
    res.json({ <entidadLower>: item })
  } catch (error) {
    res.status(500).json({ error: 'Error al actualizar <entidadLower>' })
  }
})

// DELETE /:id — Eliminar
router.delete('/:id', async (req: AuthRequest, res) => {
  try {
    const id = req.params.id as string
    await eliminar<Entidad>(id)
    res.json({ mensaje: '<Entidad> eliminado' })
  } catch (error) {
    res.status(500).json({ error: 'Error al eliminar <entidadLower>' })
  }
})

export default router
```

## Registro en server.ts

```ts
import <entidadLower>Router from './routes/<entidadLower>.js'
// ...
app.use('/api/<entidadLower>s', requerirAuth, <entidadLower>Router)
```

## Convenciones del proyecto (AdelaCRM)

| Aspecto | Convención |
|---------|-----------|
| ID param | `req.params.id as string` |
| Auth | `AuthRequest` del middleware local, req.usuario?.id |
| Error 404 | `res.status(404).json({ error: '...' }); return` |
| Error 409 (UNIQUE) | Capturar `error?.message?.includes('UNIQUE')` |
| Error 500 | `res.status(500).json({ error: 'Error al ...' })` |
| POST resp | `res.status(201).json({ <entidadLower>: item })` |
| DELETE resp | `res.json({ mensaje: '<Entidad> eliminado' })` |
| Filtros query | Parse manual desde `typeof req.query.X === 'string' ? ... : undefined` |
| Idioma | Mensajes en español |

## Funciones DB esperadas

Asumiendo que `src/db.ts` exporta para cada entidad:

- `obtener<Entidad>s(filtros?)` → `Promise<Tipo[]>`
- `obtener<Entidad>PorId(id)` → `Promise<Tipo | undefined>`
- `crear<Entidad>(data)` → `Promise<Tipo>`
- `actualizar<Entidad>(id, data)` → `Promise<Tipo | undefined>`
- `eliminar<Entidad>(id)` → `Promise<boolean>`

## Pitfalls

- **TypeScript `params.id`**: Express tipa `req.params.id` como `string` en tiempo de ejecución pero TS puede quejarse. Usar `req.params.id as string` para silenciar.
- **Return después de send**: Siempre hacer `return` explícito tras `res.status(X).json(...)` para evitar `ERR_HTTP_HEADERS_SENT`.
- **Error sin tipar**: En catch, el error es `unknown`. Usar `error: any` solo donde se necesite acceder a `.message`.
- **Query params booleanos**: `req.query.activo` es `string | undefined` en Express, no hay parseo automático de booleanos. Hacer parse explícito.