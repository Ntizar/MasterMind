# Patrón de implementación por tandas

## Flujo estándar por tanda

Basado en la Tanda 1 (Productos + Presupuestos) del proyecto AdelaCRM.

### 1. Verificar qué ya existe

Antes de implementar, leer:
- `src/types.ts` — interfaces de la entidad
- `src/db.ts` — schema SQL + funciones CRUD
- `src/routes/` — archivos existentes
- `src/server.ts` — qué rutas están montadas

### 2. Añadir schema SQL (si no existe)

Añadir al final del **último** bloque `db.run(\`...\`)` en `initDatabase()`:

```typescript
// === MI NUEVO MÓDULO ===
db.run(`
  CREATE TABLE IF NOT EXISTS nueva_tabla (
    id TEXT PRIMARY KEY,
    ...,
    creado TEXT NOT NULL,
    actualizado TEXT NOT NULL
  );
`)

// ⚠️ PITFALL: al usar patch() entre bloques de db.run():
// old_string debe incluir el backtick de cierre `)` del bloque ANTERIOR
// Si no, dejas un db.run() sin cerrar → TS1005 en todas las líneas SQL siguientes
//
// ✅ old_string correcto:
//   "CREATE INDEX ... ;\n  `)\n\n  // Admin user"
// ✅ new_string:
//   "CREATE INDEX ... ;\n  `)\n\n  // === Nuevo módulo ===\n  db.run(`\n    ...\n  `)\n\n  // Admin user"
```

### 3. Añadir funciones CRUD en db.ts

Tras el schema SQL, añadir funciones siguiendo el patrón:

```typescript
// ═══════════════════════════════════════
// NUEVA ENTIDAD
// ═══════════════════════════════════════

async function obtenerEntidades(filtro?: { ... }): Promise<Entidad[]> {
  await initDatabase()
  let sql = 'SELECT * FROM entidades WHERE 1=1'
  const params: any[] = []
  if (filtro?.campo) { sql += ' AND campo = ?'; params.push(filtro.campo) }
  sql += ' ORDER BY creado DESC'
  return all<Entidad>(sql, params)
}

async function obtenerEntidadPorId(id: string): Promise<Entidad | undefined> {
  await initDatabase()
  return get<Entidad>('SELECT * FROM entidades WHERE id = ?', [id])
}

async function crearEntidad(data: Omit<Entidad, 'id' | 'creado' | 'actualizado'>): Promise<Entidad> {
  await initDatabase()
  const id = `prefijo-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  const ahora = new Date().toISOString()
  run('INSERT INTO entidades (...) VALUES (?, ...)', [id, data.campo, ahora, ahora])
  return { ...data, id, creado: ahora, actualizado: ahora } as Entidad
}

async function actualizarEntidad(id: string, data: Partial<Entidad>): Promise<Entidad | undefined> {
  await initDatabase()
  const campos: string[] = []
  const valores: any[] = []
  for (const key of ['campo1', 'campo2']) {
    if ((data as any)[key] !== undefined) { campos.push(`${key} = ?`); valores.push((data as any)[key]) }
  }
  if (campos.length > 0) {
    campos.push('actualizado = ?')
    valores.push(new Date().toISOString())
    valores.push(id)
    run(`UPDATE entidades SET ${campos.join(', ')} WHERE id = ?`, valores)
  }
  return obtenerEntidadPorId(id)
}

async function eliminarEntidad(id: string): Promise<boolean> {
  await initDatabase()
  run('DELETE FROM entidades WHERE id = ?', [id])
  // Si tiene tablas hijas:
  run('DELETE FROM tabla_hija WHERE entidadId = ?', [id])
  return true
}
```

### 4. Actualizar export block

Añadir al final del `export { ... }`:

```typescript
export {
  // ... existentes ...,
  // Nueva Entidad
  obtenerEntidades, obtenerEntidadPorId, crearEntidad, actualizarEntidad, eliminarEntidad,
  // Tabla hija
  obtenerTablasHijas, crearTablaHija, eliminarTablaHija
}
```

### 5. Crear archivo de rutas

`src/routes/entidades.ts`:

```typescript
import { Router } from 'express'
import { funciones } from '../db.js'
import type { AuthRequest } from '../middleware/auth.js'
import type { Request } from 'express'

const router = Router()

router.get('/', async (req: AuthRequest, res) => {
  try {
    const q = req.query
    const filtro = typeof q.filtro === 'string' ? q.filtro : undefined
    const items = await funciones.obtener({ filtro })
    res.json({ items })
  } catch (error) {
    res.status(500).json({ error: 'Error al obtener' })
  }
})

router.get('/:id', async (req: Request, res) => {
  try {
    const id = req.params.id as string  // ← OBLIGATORIO el cast
    const item = await funciones.obtenerPorId(id)
    if (!item) { res.status(404).json({ error: 'No encontrado' }); return }
    res.json({ item })
  } catch (error) {
    res.status(500).json({ error: 'Error' })
  }
})

router.post('/', async (req: AuthRequest, res) => {
  try {
    if (!req.body.campoRequerido) { res.status(400).json({ error: 'campoRequerido es obligatorio' }); return }
    const item = await funciones.crear({ ...req.body, creadoPor: req.usuario?.id })
    res.status(201).json({ item })
  } catch (error: any) {
    if (error?.message?.includes('UNIQUE')) { res.status(409).json({ error: 'Ya existe' }); return }
    res.status(500).json({ error: 'Error al crear' })
  }
})

router.put('/:id', async (req: AuthRequest, res) => {
  try {
    const id = req.params.id as string
    const item = await funciones.actualizar(id, req.body)
    if (!item) { res.status(404).json({ error: 'No encontrado' }); return }
    res.json({ item })
  } catch (error) {
    res.status(500).json({ error: 'Error al actualizar' })
  }
})

router.delete('/:id', async (req: AuthRequest, res) => {
  try {
    const id = req.params.id as string
    await funciones.eliminar(id)
    res.json({ mensaje: 'Eliminado correctamente' })
  } catch (error) {
    res.status(500).json({ error: 'Error al eliminar' })
  }
})

export default router
```

### 6. Actualizar server.ts

```typescript
// Añadir al bloque de imports:
import entidadesRouter from './routes/entidades.js'

// Añadir tras los montajes existentes:
app.use('/api/entidades', requerirAuth, entidadesRouter)
```

### 7. Compilar y verificar

```bash
cd /root/workspace/AdelaTest01
npx tsc   # ← SIN --noEmit (da falsos positivos LSP)
# Si output es vacío y exit_code=0 → ✅ limpio
```

### 8. Mostrar resultados

Después de cada tanda, resumir:
- Qué archivos se crearon/modificaron
- Endpoints disponibles
- Estado de compilación (síntomas si falló)
- Siguiente tanda preparada
- NO parar entre tandas — el usuario interpreta las pausas como "se ha bloqueado"

## ⚠️ Pitfalls adicionales de Tanda 2 (Facturación)

### Omit type mismatch con campos auto-generados

Cuando una función en db.ts usa `Omit<Entidad, 'id' | 'creado' | 'actualizado'>` pero también auto-genera campos adicionales (como `numero`, `hashActual`, `huellaDigital`, `codigoQr`, `pendienteCobro`), el tipo del parámetro EXIGE esos campos aunque la función los sobrescriba.

```typescript
// ❌ MAL — error TS2345: faltan 'numero', 'pendienteCobro', 'verifactuEnviado'
const factura = await crearFactura({ empresaId, fechaExpedicion, ... })

// ✅ BIEN — pasar valores dummy que la función ignorará/sobrescribirá
const factura = await crearFactura({
  empresaId, fechaExpedicion, ...,
  numero: '',           // ← se genera automáticamente dentro
  pendienteCobro: 0,     // ← se calcula en creación
  verifactuEnviado: 0    // ← se pone a 0 por defecto
})
```

**Regla:** al crear en rutas, pasar SIEMPRE todos los campos que el Omit type requiere aunque sean auto-generados. Poner string vacío para strings, 0 para números, null para opcionales.

### verifactuEnviado es number (0/1), no boolean

El campo `verifactuEnviado` en el schema SQL es `INTEGER DEFAULT 0` (sql.js no tiene boolean). En TypeScript se tipa como `number`. En las rutas, pasar `0` o `1`, NUNCA `true`/`false`:

```typescript
// ❌ MAL — verifactuEnviado: false  → TS2322: Type 'boolean' is not assignable to type 'number'
// ✅ BIEN — verifactuEnviado: 0
```

### Credenciales en HTML (login hint)

NUNCA mostrar el PIN real en el HTML del login. En vez de `Demo: admin@local / 1234`, usar:
```html
<p class="hint">Credenciales de demostración en el README</p>
```

### Import crypto para hashes

En proyectos que generan hashes SHA-256 (VeriFactu), añadir al inicio de `db.ts`:

```typescript
import crypto from 'crypto'
```

No usar `require('crypto')` — en ESM no existe `require` global. Usar `import` directo.

```typescript
// ✅ BIEN — ESM nativo
import crypto from 'crypto'
const hash = crypto.createHash('sha256').update(data).digest('hex')

// ❌ MAL — ReferenceError: require is not defined en ESM
const hash = require('crypto').createHash('sha256').update(data).digest('hex')
```

## Patrones de negocio

### Cobro → Factura: sincronización bidireccional

Al registrar o eliminar un cobro, el sistema debe actualizar automáticamente la factura asociada:

```typescript
// Al CREAR cobro:
async function crearCobro(data): Promise<Cobro> {
  // 1. Insertar cobro
  run('INSERT INTO cobros ...', [...])
  
  // 2. Sumar todos los cobros de la factura
  const totalCobrado = get<any>(
    'SELECT SUM(importe) as total FROM cobros WHERE facturaId = ? AND estado != ?',
    [data.facturaId, 'anulado']
  )?.total || 0
  
  // 3. Calcular pendiente
  const factura = get<any>('SELECT total FROM facturas WHERE id = ?', [data.facturaId])
  const pendiente = factura ? Math.max(0, factura.total - totalCobrado) : 0
  
  // 4. Transicionar estado automáticamente
  const nuevoEstado = pendiente <= 0 ? 'cobrada' : totalCobrado > 0 ? 'parcialmente_cobrada' : 'emitida'
  run('UPDATE facturas SET pendienteCobro = ?, estado = ? WHERE id = ?', [pendiente, nuevoEstado, data.facturaId])
}
```

**Estados de factura con cobros:**
| Estado | Condición |
|--------|-----------|
| `borrador` | Sin emitir |
| `emitida` | Factura emitida, sin cobros |
| `parcialmente_cobrada` | Al menos un cobro registrado, pendiente > 0 |
| `cobrada` | pendienteCobro ≤ 0 (total cobrado ≥ total factura) |
| `vencida` | Pasada fechaVencimiento y pendiente > 0 |
| `anulada` | Factura anulada |

### Emisión de factura (→ VeriFactu)

El endpoint de emisión recalcula totales desde líneas y cambia estado:

```typescript
router.post('/:id/emitir', async (req: AuthRequest, res) => {
  const factura = await obtenerFacturaPorId(id)
  if (!factura) { res.status(404)...; return }
  if (factura.estado !== 'borrador') { 
    res.status(400).json({ error: 'Solo facturas en borrador pueden emitirse' }); return 
  }
  
  // Recalcular desde líneas (la verdadera fuente)
  const lineas = await obtenerLineasFactura(id)
  const baseImponible = lineas.reduce((s, l) => s + (l.importe || 0), 0)
  const totalIva = lineas.reduce((s, l) => s + (l.cuotaIva || 0), 0)
  const total = baseImponible + totalIva
  
  await actualizarFactura(id, { estado: 'emitida', baseImponible, totalIva, total, pendienteCobro: total })
  res.json({ factura, mensaje: 'Factura emitida con hash VeriFactu' })
})
```

**Reglas de emisión:**
- Solo facturas en `borrador` pueden emitirse (no re-emitir ni modificar emitidas)
- Los totales se recalculan SIEMPRE desde las líneas, no se confía en los valores enviados
- Al emitir, se genera el hash encadenado SHA-256 + huella digital + QR (en `crearFactura()`)
- Una vez emitida, NO se puede eliminar (la función `eliminarFactura()` lo bloquea)

### Hash encadenado VeriFactu

```typescript
import crypto from 'crypto'

// En crearFactura():
const ultimoHash = get<any>(
  'SELECT hashActual FROM facturas ORDER BY creado DESC LIMIT 1'
)?.hashActual || '0000000000000000000000000000000000000000000000000000000000000000'

const datosFactura = `${numero}|${fechaExpedicion}|${baseImponible}|${total}`
const hashActual = crypto.createHash('sha256').update(ultimoHash + datosFactura).digest('hex')
const huellaDigital = `VF-${hashActual.substring(0, 16)}`
const codigoQr = JSON.stringify({ n: numero, f: fechaExpedicion, bi: baseImponible, t: total, h: hashActual.substring(0, 8) })

// Guardar en BD: hashAnterior (el de la factura previa), hashActual (el calculado ahora)
// La cadena es: factura1.hashActual → factura2.hashAnterior → factura2.hashActual → ...
```

El hash cero (`'00...0'`) es el hash de la primera factura (no tiene anterior). Cada factura nueva:
1. Lee el hash de la última factura → `hashAnterior`
2. Calcula SHA-256(hashAnterior + datosFactura) → `hashActual`
3. Guarda ambos en la BD
4. Genera QR con resumen de datos + primeros 8 chars del hash

## Tandas para CRM+ERP completo (agrupación real)

| Tanda | Módulos | Archivos a crear |
|-------|---------|------------------|
| 1 | Productos + Presupuestos | `routes/productos.ts`, `routes/presupuestos.ts` |
| 2 | Facturación + VeriFactu + **Cobros** | `routes/facturas.ts` (cobros como subrutas `/:id/cobros`) |
| 3 | Proveedores + Compras + **Inventario** | `routes/proveedores.ts`, `routes/pedidosCompra.ts`, `routes/stock.ts` |
| 4 | Proyectos + Tareas + Time Tracking | `routes/proyectos.ts`, `routes/tareas.ts` |
| 5 | Tickets + Contratos | `routes/tickets.ts`, `routes/contratos.ts` |
| 6 | RRHH + Marketing + Automatizaciones | `routes/empleados.ts`, `routes/marketing.ts`, `routes/automatizaciones.ts` |
| 7 | Contabilidad + Informes + SuperAdmin | `routes/contabilidad.ts`, `routes/superadmin.ts`, `routes/config.ts` |

**⚠️ Los cobros NO son archivo separado.** Van dentro de `facturas.ts` porque:
- Cambian `pendienteCobro` y `estado` de la factura automáticamente
- La state machine (emitida→parcial→cobrada) está en el mismo archivo
- Evita dependencia circular entre routes

**⚠️ El inventario incluye 3 features en 1 archivo (routes/stock.ts):**
- Gestión de almacenes (CRUD)
- Stock global/por almacén/por producto (GET)
- Ajuste con movimiento automático (POST /ajustar)

Cada tanda sigue exactamente los 8 pasos del flujo estándar.