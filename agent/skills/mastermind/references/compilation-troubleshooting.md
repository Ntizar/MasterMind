# Troubleshooting de compilación TypeScript en CRM+ERP

## Escenario típico

Al añadir nuevos módulos o tandas, la compilación falla con **tres fuentes de error** concatenadas:

```
1. db.ts no exporta las funciones que las rutas importan
   → 81 errores: Module '../db.js' has no exported member 'obtenerX'

2. types.ts no coincide con los campos reales de db.ts
   → ~370 errores: Type 'X' has no properties in common with type 'Y'

3. Las rutas usan nombres de campo antiguos del parametro de la funcion
   → ~16 errores: Argument of type '{ campo_antiguo: ... }' is not assignable
```

## Principio fundamental

**db.ts (la implementación SQL) es la fuente de verdad**, no types.ts. Cuando haya conflicto, alinear types.ts con db.ts, no al revés. No cambies el SQL ni las funciones de db.ts a menos que el bug esté allí.

## Proceso de reparación (3 pasos ordenados)

### Paso 1: Export block en db.ts

El bloque `export { ... }` al final de db.ts debe incluir TODAS las funciones CRUD de todos los módulos. Si al añadir una tanda nueva olvidas exportar las funciones, las rutas dan error.

```typescript
export {
  // Base
  ... funciones base (usuarios, empresas, contactos, leads, ...),
  // Módulos comerciales
  obtenerProductos, ..., crearPresupuesto, ...,
  // Módulos operaciones
  obtenerProveedores, ..., ajustarStock, ...,
  // Módulos servicio
  obtenerTickets, ..., crearContrato, ...,
  // RRHH
  obtenerEmpleados, ..., crearAusencia, ...
}
```

Cada tanda nueva amplía este export. Si el compilador dice `'obtenerX' has no exported member` → mira el export block primero.

### Paso 2: Type imports en db.ts

db.ts importa tipos desde `types.ts`. Cuando añades nuevos módulos, NECESITAS importar los tipos de esas entidades aunque db.ts los use solo en firmas de función:

```typescript
import type {
  // ... tipos base ...
  Producto, Factura, Presupuesto, Proveedor,
  PedidoCompra, LineaPedidoCompra, Proyecto, Tarea,
  Ticket, Contrato, Empleado, Stock, MovimientoStock,
  // ... cualquier tipo que aparezca en firmas de función
} from './types.js'
```

**Pitfall:** Si falta un tipo aquí, el compilador da errores `Cannot find name 'Producto'` similares a los de falta de definición en types.ts, pero el problema real está en los imports.

### Paso 3: Alinear tipos (types.ts → db.ts)

Cuando db.ts usa campos que no coinciden con types.ts:

1. **Lee el schema SQL** en `initDatabase()` para ver los nombres de columna reales
2. **Compara con la interfaz** en types.ts
3. **Actualiza la interfaz** para que coincida con db.ts (conversiones comunes documentadas abajo)

Las rutas (POST /) envían un objeto cuyos nombres de campo deben coincidir con la interfaz de types.ts. Si types.ts está alineada con db.ts, las rutas funcionan.

### Paso 4: Corregir rutas

Después de alinear types.ts, las rutas pueden fallar porque usan los nombres antiguos:

```typescript
// ❌ MAL — campo antiguo de types.ts previa
router.post('/', async (req, res) => {
  const { asunto, ... } = req.body  // 'asunto' no existe en la interfaz actual
})

// ✅ BIEN — campo actual de db.ts reflejado en types.ts
router.post('/', async (req, res) => {
  const { titulo, ... } = req.body  // coincide con { titulo: string } en types.ts
})
```

## Mapa de conversiones de campos (v2 → v2+)

Campos que CAMBIARON entre la versión inicial de types.ts y la implementación real de db.ts en AdelaCRM v2:

### CategoriaProducto
| Campo antiguo | Campo real (db.ts) |
|--------------|-------------------|
| `padreId: string \| null` | `activo: number` (1/0) |

### Presupuesto
| Campo antiguo | Campo real (db.ts) |
|--------------|-------------------|
| `serie` | `numero` |
| `fecha` | `fechaEmision` |
| `baseImponible` | `subtotal` |
| `totalIva` | `ivaTotal` |
| `irpf` (no existía) | `irpf: number` |
| — | `recargoEquivalencia: number` |
| `notasInternas` | — (eliminado) |
| `condiciones` | — (eliminado) |

### Factura
| Campo antiguo | Campo real (db.ts) |
|--------------|-------------------|
| `facturaRectificadaId` | `pedidoId` |
| `serie` | se mantiene pero en la ruta se auto-asigna o no se envía |
| `baseImponible` | `total` (sin desglose en la tabla) |
| `totalIva` | se recalcula en backend |
| `totalIrpf` | — |
| `notas` | — |
| — | `pendienteCobro: number` |

### LineaFactura / LineaPresupuesto / LineaPedidoCompra
| Campo antiguo | Campo real (db.ts) |
|--------------|-------------------|
| `importe` | eliminado (se calcula como cantidad * precioUnitario) |
| `cuotaIva` | — |
| `cantidadRecibida` | — |
| `pedidoCompraId` | `pedidoId` |
| — | `orden: number` |

### PedidoCompra
| Campo antiguo | Campo real (db.ts) |
|--------------|-------------------|
| `fecha` | `fechaPedido` |
| `fechaEntrega` | `fechaPrevista` |
| `serie` | `numero` |
| `baseImponible` | `subtotal` |
| `totalIva` | `ivaTotal` |

### Proyecto
| Campo antiguo | Campo real (db.ts) |
|--------------|-------------------|
| `fechaFin` | `fechaFinPrevisto` |
| `fechaFin` (también) | `fechaFinReal` |
| `prioridad` | — (eliminado, se controla por estado) |
| `presupuestoReal` | `presupuesto` |

### Tarea
| Campo antiguo | Campo real (db.ts) |
|--------------|-------------------|
| `estimacionHoras` | `horasEstimadas` |
| `tiempoReal` | `horasReales` |

### Ticket
| Campo antiguo | Campo real (db.ts) |
|--------------|-------------------|
| `asunto` | `titulo` |
| `proyectoId` | — |
| `slaHoras` | `slaLimite` |
| `origen` | `fuente` |
| — | `asignadoA` |
| — | `categoria` |

### MensajeTicket
| Campo antiguo | Campo real (db.ts) |
|--------------|-------------------|
| `tipo` | — |
| `creadoPor` | `usuarioId` |

## Pitfalls de noImplicitReturns en Express

Con `noImplicitReturns: true` en tsconfig.json, todas las ramas de una función deben devolver `void` o un valor explícitamente:

```typescript
// ❌ MAL — la rama 'if (!item)' no devuelve nada
router.put('/:id', async (req, res) => {
  const item = await obtenerPorId(id)
  if (!item) { res.status(404).json({ error: 'No encontrado' }) } // ← sin return
  res.json({ item })
})

// ✅ BIEN — return explícito en cada rama
router.put('/:id', async (req, res) => {
  const item = await obtenerPorId(id)
  if (!item) { res.status(404).json({ error: 'No encontrado' }); return }
  res.json({ item })
})
```

En catch blocks igual:

```typescript
// ❌ MAL
router.delete('/:id', async (req, res) => {
  try {
    await eliminar(id)
    res.json({ mensaje: 'Eliminado' })
  } catch (error) {
    res.status(500).json({ error: 'Error' }) // ← sin return
  }
})

// ✅ BIEN
router.delete('/:id', async (req, res) => {
  try {
    await eliminar(id)
    res.json({ mensaje: 'Eliminado' })
  } catch (error) {
    res.status(500).json({ error: 'Error' }); return
  }
})
```

## Variables no usadas (noUnusedLocals)

Con `noUnusedLocals: true`, las variables declaradas y no leídas causan error. Esto suele ocurrir al desestructurar `req.body`:

```typescript
// ❌ MAL — 'serie', 'notas' declaradas pero no usadas
const { clienteId, fecha, serie, notas, total } = req.body

// ✅ BIEN — solo desestructurar lo que realmente se pasa a la función
const { clienteId, fecha, total } = req.body
```

## Verificación

```bash
cd /root/workspace/AdelaTest01

# Primera pasada: errores completos con --noEmit (rápido)
npx tsc --noEmit

# Si son errores reales, ejecutar compilación completa para verificar
npx tsc

# Output vacío + exit_code=0 → ✅ limpio
```

**Nota:** A veces `npx tsc --noEmit` reporta errores de `import.meta` o `esModuleInterop` que no aparecen en `npx tsc`. Si `npx tsc` da exit_code=0 y output vacío, está limpio aunque `--noEmit` se queje.

## Ejemplo completo del flujo

```
1. npx tsc --noEmit → 81 errores "has no exported member"
   → Mirar export block de db.ts → Faltan funciones nuevas → Añadir al export

2. npx tsc → ~370 errores "Cannot find name 'Producto'"
   → Faltan types import en db.ts → import type { Producto, Factura, ... }

3. npx tsc → ~370 errores "Type 'X' is not assignable to type 'Y'"
   → types.ts tiene campos que no coinciden con db.ts SQL schema
   → Leer schema SQL en db.ts initDatabase()
   → Actualizar interfaces en types.ts para que coincidan
   → Ver tabla de conversiones arriba

4. npx tsc → ~16 errores en rutas "campo_nuevo does not exist"
   → Las rutas usan nombres de campo antiguos
   → Actualizar destructuring y objetos en rutas para usar nombres reales

5. npx tsc → 2 errores "declared but never read"
   → Eliminar variables no usadas del destructuring en rutas

6. npx tsc → output vacío, exit_code=0 ✅
```