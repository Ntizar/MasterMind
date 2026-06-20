# Pedidos de Venta — Patrón completo

## Tablas SQL

```sql
CREATE TABLE IF NOT EXISTS pedidos (
  id TEXT PRIMARY KEY, numero TEXT NOT NULL, presupuestoId TEXT,
  empresaId TEXT NOT NULL, fechaPedido TEXT NOT NULL,
  estado TEXT DEFAULT 'pendiente', total REAL DEFAULT 0,
  creado TEXT NOT NULL, actualizado TEXT NOT NULL,
  FOREIGN KEY (presupuestoId) REFERENCES presupuestos(id),
  FOREIGN KEY (empresaId) REFERENCES empresas(id)
);

CREATE TABLE IF NOT EXISTS lineas_pedido (
  id TEXT PRIMARY KEY, pedidoId TEXT NOT NULL,
  productoId TEXT, descripcion TEXT NOT NULL,
  cantidad REAL DEFAULT 1, precioUnitario REAL DEFAULT 0,
  descuento REAL DEFAULT 0, tipoIva TEXT DEFAULT 'general',
  importe REAL DEFAULT 0, orden INTEGER DEFAULT 0,
  FOREIGN KEY (pedidoId) REFERENCES pedidos(id)
);
```

## Funciones DB necesarias

```ts
// En src/db.ts, importar tipos:
import type { Pedido, LineaPedido } from './types.js'

// Funciones:
async function obtenerPedidos(filtros?: { estado?: string; empresaId?: string }): Promise<Pedido[]>
async function obtenerPedidoPorId(id: string): Promise<Pedido | undefined>
async function crearPedido(data: Omit<Pedido, 'id' | 'creado' | 'actualizado'>): Promise<Pedido>
async function actualizarPedido(id: string, data: Partial<Pedido>): Promise<Pedido | undefined>
async function eliminarPedido(id: string): Promise<boolean>
async function obtenerLineasPedido(pedidoId: string): Promise<LineaPedido[]>
async function crearLineaPedido(data: Omit<LineaPedido, 'id'>): Promise<LineaPedido>
async function eliminarLineaPedido(id: string): Promise<boolean>
```

## Generación de número automático

```ts
const ahora = new Date().toISOString()
const year = ahora.slice(0, 4)
const monthDay = ahora.slice(5, 10).replace('-', '')
const counter = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
const numero = `PED-${year}${monthDay}-${counter}`
```

## Cálculo de totales al añadir/eliminar línea

```ts
const lineas = await obtenerLineasPedido(pedidoId)
const baseImponible = lineas.reduce((s: number, l: any) => s + (l.importe || 0), 0)
const totalIva = lineas.reduce((s: number, l: any) => s + (l.importe || 0) * 0.21, 0)
await actualizarPedido(pedidoId, { baseImponible, totalIva, total: baseImponible + totalIva })
```

## Eliminación condicional

Solo se puede eliminar un pedido si `estado === 'pendiente'`:

```ts
const pedido = await obtenerPedidoPorId(id)
if (!pedido) { res.status(404).json({ error: 'Pedido no encontrado' }); return }
if (pedido.estado !== 'pendiente') { res.status(400).json({ error: 'Solo se pueden eliminar pedidos en estado pendiente' }); return }
```
