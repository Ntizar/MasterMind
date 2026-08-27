# Patrón de Ajuste de Stock con Trazabilidad

## Propósito

Gestionar entradas y salidas de inventario con trazabilidad completa (stockAnterior → stockPosterior), auto-creación de registros, y sin stock negativo.

## Función principal (`ajustarStock`)

```typescript
async function ajustarStock(
  productoId: string, almacenId: string, cantidad: number,
  tipo: string,                         // 'entrada_compra' | 'salida_venta' | 'ajuste' | 'merma' | 'devolucion_cliente'
  referenciaTipo?: string,              // 'pedido' | 'factura' | 'manual'
  referenciaId?: string,
  notas?: string,
  creadoPor?: string
): Promise<Stock> {
  await initDatabase()

  // 1. Obtener o auto-crear el registro de stock
  let stock = get<Stock>('SELECT * FROM stock WHERE productoId = ? AND almacenId = ?', [productoId, almacenId])
  if (!stock) {
    const id = `stk-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    run('INSERT INTO stock (id, productoId, almacenId, cantidad, stockMinimo, ubicacion) VALUES (?,?,?,0,0,?)',
      [id, productoId, almacenId, null])
    stock = get<Stock>('SELECT * FROM stock WHERE id = ?', [id])!
  }

  // 2. Calcular valores
  const ahora = new Date().toISOString()
  const stockAnterior = stock.cantidad
  const stockPosterior = Math.max(0, stockAnterior + cantidad)  // nunca negativo

  // 3. Actualizar stock
  run('UPDATE stock SET cantidad = ? WHERE id = ?', [stockPosterior, stock.id])

  // 4. Registrar movimiento (trazabilidad)
  const movId = `mov-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  run(
    'INSERT INTO movimientos_stock (id, productoId, almacenId, tipo, cantidad, stockAnterior, stockPosterior, referenciaTipo, referenciaId, notas, creado, creadoPor) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
    [movId, productoId, almacenId, tipo, cantidad, stockAnterior, stockPosterior, referenciaTipo || null, referenciaId || null, notas || null, ahora, creadoPor || null]
  )

  return { ...stock, cantidad: stockPosterior }
}
```

## Rutas Express

```typescript
// GET /api/stock — Stock global, por almacén o por producto
router.get('/', async (req: AuthRequest, res) => {
  const almacenId = typeof req.query.almacenId === 'string' ? req.query.almacenId : undefined
  const productoId = typeof req.query.productoId === 'string' ? req.query.productoId : undefined

  if (productoId && almacenId) {
    const stock = await obtenerStockProducto(productoId, almacenId)
    res.json({ stock })
  } else if (almacenId) {
    const items = await obtenerStockPorAlmacen(almacenId)
    res.json({ items })
  } else {
    const items = await obtenerStockGlobal()
    res.json({ items })
  }
})

// POST /api/stock/ajustar — Ajuste manual con movimiento automático
router.post('/ajustar', async (req: AuthRequest, res) => {
  const { productoId, almacenId, cantidad, tipo, notas } = req.body
  if (!productoId || !almacenId) { res.status(400).json({ error: 'productoId y almacenId son obligatorios' }); return }
  if (cantidad === undefined || cantidad === 0) { res.status(400).json({ error: 'cantidad debe ser distinto de 0' }); return }
  if (!tipo) { res.status(400).json({ error: 'tipo de movimiento es obligatorio' }); return }

  const stock = await ajustarStock(productoId, almacenId, cantidad, tipo, 'manual', undefined, notas, req.usuario?.id)
  res.json({ stock, mensaje: `Stock ajustado: ${cantidad > 0 ? '+' : ''}${cantidad}` })
})

// GET /api/stock/movimientos — Historial con filtros
router.get('/movimientos', async (req: AuthRequest, res) => {
  const filtro: any = {}
  if (typeof req.query.productoId === 'string') filtro.productoId = req.query.productoId
  if (typeof req.query.almacenId === 'string') filtro.almacenId = req.query.almacenId
  if (typeof req.query.tipo === 'string') filtro.tipo = req.query.tipo
  const movimientos = await obtenerMovimientosStock(filtro)
  res.json({ movimientos })
})

// Almacenes CRUD
router.get('/almacenes', async (req, res) => {
  const items = await obtenerAlmacenes()
  res.json({ items })
})

router.post('/almacenes', async (req: AuthRequest, res) => {
  if (!req.body.nombre) { res.status(400).json({ error: 'nombre es obligatorio' }); return }
  const item = await crearAlmacen(req.body.nombre, req.body.direccion, req.body.ciudad)
  res.status(201).json({ almacen: item })
})

router.delete('/almacenes/:id', async (req: AuthRequest, res) => {
  const id = req.params.id as string
  await eliminarAlmacen(id)
  res.json({ mensaje: 'Almacén eliminado' })
})
```

## Reglas del patrón

1. **Auto-creación**: Si no existe registro de stock producto+almacén, se crea automáticamente con cantidad 0
2. **Stock mínimo seguro**: `Math.max(0, anterior + cantidad)` evita stock negativo
3. **Trazabilidad completa**: Cada movimiento guarda stock anterior y posterior (permite auditoría)
4. **Referencia opcional**: Vincular a pedido de compra, factura, o ajuste manual
5. **Sin doble escritura**: La ruta de stock NO actualiza líneas de pedido. La recepción se maneja como movimiento separado
6. **Filtros GET**: productoId, almacenId, tipo — el historial se consulta con query params

## Esquema SQL

```sql
CREATE TABLE IF NOT EXISTS almacenes (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  direccion TEXT,
  ciudad TEXT,
  activo INTEGER DEFAULT 1,
  creado TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stock (
  id TEXT PRIMARY KEY,
  productoId TEXT NOT NULL,
  almacenId TEXT NOT NULL,
  cantidad REAL NOT NULL DEFAULT 0,
  stockMinimo REAL DEFAULT 0,
  stockMaximo REAL,
  ubicacion TEXT,
  FOREIGN KEY (productoId) REFERENCES productos(id),
  FOREIGN KEY (almacenId) REFERENCES almacenes(id),
  UNIQUE(productoId, almacenId)
);

CREATE TABLE IF NOT EXISTS movimientos_stock (
  id TEXT PRIMARY KEY,
  productoId TEXT NOT NULL,
  almacenId TEXT NOT NULL,
  tipo TEXT NOT NULL,
  cantidad REAL NOT NULL,
  stockAnterior REAL NOT NULL,
  stockPosterior REAL NOT NULL,
  referenciaTipo TEXT,
  referenciaId TEXT,
  lote TEXT,
  notas TEXT,
  creado TEXT NOT NULL,
  creadoPor TEXT,
  FOREIGN KEY (productoId) REFERENCES productos(id),
  FOREIGN KEY (almacenId) REFERENCES almacenes(id)
);
```