# Auditoría Frontend↔Backend — AdelaCRM (2026-06-16)

## Resultado de la auditoría

Auditoría completa de las 80+ llamadas `apiFetch`/`apiPost`/`apiPut`/`apiDelete` en `public/js/crm.js` contra las rutas registradas en `src/app.ts`.

### Rutas que FALLABAN (frontend llamaba, backend no tenía)

| Frontend llamaba | Backend tenía | Estado |
|---|---|---|
| `GET /api/ausencias` | Solo `GET /api/empleados/:id/ausencias` | ✅ Convenience route añadida |
| `POST /api/ausencias` | Solo `POST /api/empleados/:id/ausencias` | ✅ Convenience route añadida |
| `PUT /api/ausencias/:id` | Solo `PUT /api/empleados/:id/ausencias/:ausenciaId` | ✅ Convenience route añadida |
| `DELETE /api/ausencias/:id` | Solo `DELETE /api/empleados/:id/ausencias/:ausenciaId` | ✅ Convenience route añadida |
| `GET /api/contabilidad` (asientos) | Solo `GET /api/contabilidad/asientos` | ✅ Convenience route añadida |
| `POST /api/contabilidad` (asientos) | Solo `POST /api/contabilidad/asientos` | ✅ Convenience route añadida |
| `PUT /api/contabilidad/:id` | Solo `PUT /api/contabilidad/asientos/:id` | ✅ Convenience route añadida |
| `DELETE /api/contabilidad/:id` | Solo `DELETE /api/contabilidad/asientos/:id` | ✅ Convenience route añadida |
| `POST /api/stock` | Solo `POST /api/stock/ajustar` | ✅ Redirección añadida |
| `GET /api/vacaciones` (sin param) | Solo `GET /api/vacaciones/:empleadoId` | ✅ GET / añadido en router |

### Rutas que SÍ funcionaban (sin cambios)

Todas las demás llamadas del frontend mapeaban correctamente a rutas del backend:
- `/api/auth/login`, `/api/auth/registro` ✅
- `/api/empresas/*` ✅
- `/api/contactos/*` ✅
- `/api/leads/*` ✅
- `/api/oportunidades/*` ✅
- `/api/productos/*` ✅
- `/api/presupuestos/*` ✅
- `/api/facturas/*` ✅
- `/api/cobros/*` ✅
- `/api/proyectos/*` ✅
- `/api/tareas/*` ✅
- `/api/tickets/*` ✅
- `/api/empleados/*` ✅
- `/api/cv/*` ✅
- `/api/conexiones/*` ✅
- `/api/resumen` ✅

## Convenience routes añadidas en app.ts

### Ausencias (GET/POST/PUT/DELETE)

```typescript
// Import de funciones de db.js
import { obtenerAusencias, crearAusencia, aprobarAusencia, eliminarAusencia } from './db.js'

// GET /api/ausencias — Listar ausencias (con filtro opcional por empleadoId)
app.get('/api/ausencias', async (req, res) => {
  try {
    const items = await obtenerAusencias(String(req.query.empleadoId))
    res.json({ items })
  } catch (error) {
    res.status(500).json({ error: 'Error al obtener ausencias' })
  }
})

// POST /api/ausencias — Crear ausencia
app.post('/api/ausencias', async (req: AuthRequest, res) => {
  try {
    const item = await crearAusencia({ ...req.body, creadoPor: req.usuario?.id })
    res.status(201).json({ item })
  } catch (error) {
    res.status(500).json({ error: 'Error al crear ausencia' })
  }
})

// PUT /api/ausencias/:id — Aprobar/rechazar ausencia
app.put('/api/ausencias/:id', async (req, res) => {
  try {
    const item = await aprobarAusencia(String(req.params.id), req.body.estado)
    if (!item) { res.status(404).json({ error: 'No encontrada' }); return }
    res.json({ item })
  } catch (error) {
    res.status(500).json({ error: 'Error al actualizar ausencia' })
  }
})

// DELETE /api/ausencias/:id — Eliminar ausencia
app.delete('/api/ausencias/:id', async (req, res) => {
  try {
    await eliminarAusencia(String(req.params.id))
    res.json({ mensaje: 'Eliminada' })
  } catch (error) {
    res.status(500).json({ error: 'Error al eliminar' })
  }
})
```

### Contabilidad (GET/POST/PUT/DELETE)

```typescript
// Import
import { obtenerAsientos, crearAsiento, actualizarAsiento, eliminarAsiento } from './db.js'

// GET /api/contabilidad — Listar asientos
app.get('/api/contabilidad', async (req, res) => {
  try {
    const items = await obtenerAsientos(String(req.query.cuentaId))
    res.json({ items })
  } catch (error) {
    res.status(500).json({ error: 'Error al obtener asientos' })
  }
})

// POST /api/contabilidad — Crear asiento
app.post('/api/contabilidad', async (req: AuthRequest, res) => {
  try {
    const item = await crearAsiento({ ...req.body, creadoPor: req.usuario?.id })
    res.status(201).json({ item })
  } catch (error) {
    res.status(500).json({ error: 'Error al crear asiento' })
  }
})

// PUT /api/contabilidad/:id — Actualizar asiento
app.put('/api/contabilidad/:id', async (req, res) => {
  try {
    const item = await actualizarAsiento(String(req.params.id), req.body)
    if (!item) { res.status(404).json({ error: 'No encontrado' }); return }
    res.json({ item })
  } catch (error) {
    res.status(500).json({ error: 'Error al actualizar' })
  }
})

// DELETE /api/contabilidad/:id — Eliminar asiento
app.delete('/api/contabilidad/:id', async (req, res) => {
  try {
    await eliminarAsiento(String(req.params.id))
    res.json({ mensaje: 'Eliminado' })
  } catch (error) {
    res.status(500).json({ error: 'Error al eliminar' })
  }
})
```

### Stock (POST)

```typescript
// POST /api/stock → redirige a /api/stock/ajustar
app.post('/api/stock', async (req, res) => {
  // Redirigir al endpoint de ajuste
  req.url = '/ajustar'
  stockRouter(req, res, () => {})
})
```

## Fix en vacaciones.ts (GET / sin empleadoId)

```typescript
// Añadido al final del router, antes de export default
router.get('/', async (req: AuthRequest, res) => {
  try {
    const items = await obtenerTodasSolicitudesVacaciones()
    res.json({ items })
  } catch (error) {
    res.status(500).json({ error: 'Error al obtener solicitudes' })
  }
})
```
