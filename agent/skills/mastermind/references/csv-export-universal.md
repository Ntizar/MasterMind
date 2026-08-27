# CSV Export Universal — CRM Multi-entidad

## Resumen

Patrón para añadir exportación CSV a **cualquier tab/entidad** de un CRM monojs (SPA vanilla JS con Express backend). La idea: un solo sistema universal con mapa de columnas, botón inyectado dinámicamente, y descarga compatible con Excel español (UTF-8 BOM + `;` como separador).

## Arquitectura

```
crm.js
├── CSV_DATA_MAP     ← Object { entidad: { columnas: [col1, col2,...] } }
├── inyectarBtnCSV() ← Busca el contenedor del tab activo y añade botón 📥 CSV
├── descargarCSV()   ← Genera Blob con UTF-8 BOM + sep `;` + salto CRLF
└── Globales (all*)  ← Arrays donde cada cargar*() guarda los datos fetcheados
```

## Implementación paso a paso

### 1. Mapa de columnas

```javascript
const CSV_DATA_MAP = {
  empresas: { columnas: ['Nombre', 'CIF/NIF', 'Email', 'Teléfono', 'Dirección', 'Ciudad'] },
  contactos: { columnas: ['Nombre', 'Email', 'Teléfono', 'Cargo', 'Empresa', 'Departamento'] },
  leads: { columnas: ['Título', 'Contacto', 'Email', 'Teléfono', 'Fuente', 'Estado', 'Valor'] },
  oportunidades: { columnas: ['Título', 'Empresa', 'Contacto', 'Valor', 'Estado', 'Probabilidad'] },
  productos: { columnas: ['Nombre', 'SKU', 'Precio Venta', 'Precio Coste', 'Stock', 'Categoría'] },
  presupuestos: { columnas: ['Número', 'Cliente', 'Fecha', 'Total', 'Estado'] },
  facturas: { columnas: ['Número', 'Cliente', 'Fecha', 'Base', 'IVA', 'Total', 'Estado', 'Pendiente'] },
  cobros: { columnas: ['Fecha', 'Factura', 'Cliente', 'Importe', 'Método', 'Estado'] },
  proveedores: { columnas: ['Nombre', 'CIF', 'Email', 'Teléfono', 'Dirección'] },
  pedidos: { columnas: ['Número', 'Proveedor', 'Fecha', 'Total', 'Estado'] },
  almacenes: { columnas: ['Nombre', 'Ubicación', 'Responsable'] },
  proyectos: { columnas: ['Nombre', 'Cliente', 'Fecha Inicio', 'Fecha Fin', 'Presupuesto', 'Estado'] },
  tickets: { columnas: ['Título', 'Cliente', 'Prioridad', 'Estado', 'Creado', 'Asignado'] },
  empleados: { columnas: ['Nombre', 'Email', 'Rol', 'Departamento', 'F. Alta'] },
}
```

### 2. Variables globales

```javascript
// Al inicio de crm.js, junto a las otras globales:
let allEmpresas = []
let allContactos = []
let allLeads = []
let allOportunidades = []
let allProductos = []
let allPresupuestos = []
let allFacturas = []
let allCobros = []
let allProveedores = []
let allPedidos = []
let allAlmacenes = []
let allProyectos = []
let allTickets = []
let allEmpleados = []
let allContabilidad = []
let allMarketing = []
let allUsuarios = []
let allAutomatizaciones = []
let allTenants = []
```

### 3. Poblar los globales en cada cargar*()

**⚠️ PITFALL:** Sin esto, el botón CSV existe pero descarga vacío.

```javascript
// En CADA función cargarX(), justo DESPUÉS del fetch:
async function cargarEmpresas() {
  const data = await apiFetch('/api/empresas')
  const empresas = data.empresas || data.data || []
  allEmpresas = empresas   // ← ESTA LÍNEA (la que falta)
  // ... resto (renderizar tabla)
}

async function cargarProductos() {
  const data = await apiFetch('/api/productos')
  const productos = data.productos || data.data || []
  allProductos = productos   // ← ESTA LÍNEA
  // ...
}
```

### 4. Inyectar el botón CSV

```javascript
function inyectarBtnCSV(tab) {
  if (document.querySelector('.btn-export')) return  // Evitar duplicados

  const container = document.querySelector(`#tab-${tab}`)
  if (!container) return

  const TAB_VAR_MAP = {
    empresas: { key: 'empresas', var: 'allEmpresas' },
    contactos: { key: 'contactos', var: 'allContactos' },
    leads: { key: 'leads', var: 'allLeads' },
    oportunidades: { key: 'oportunidades', var: 'allOportunidades' },
    productos: { key: 'productos', var: 'allProductos' },
    presupuestos: { key: 'presupuestos', var: 'allPresupuestos' },
    facturas: { key: 'facturas', var: 'allFacturas' },
    cobros: { key: 'cobros', var: 'allCobros' },
    proveedores: { key: 'proveedores', var: 'allProveedores' },
    pedidos: { key: 'pedidos', var: 'allPedidos' },
    almacenes: { key: 'almacenes', var: 'allAlmacenes' },
    proyectos: { key: 'proyectos', var: 'allProyectos' },
    tickets: { key: 'tickets', var: 'allTickets' },
    empleados: { key: 'empleados', var: 'allEmpleados' },
    'stock-mov': { key: 'stock', var: 'allStock' },
    contabilidad: { key: 'contabilidad', var: 'allContabilidad' },
    marketing: { key: 'marketing', var: 'allMarketing' },
    usuarios: { key: 'usuarios', var: 'allUsuarios' },
  }

  const info = TAB_VAR_MAP[tab]
  if (!info || !CSV_DATA_MAP[info.key]) return

  const btn = document.createElement('button')
  btn.className = 'btn btn-ghost btn-export'
  btn.dataset.var = info.var
  btn.dataset.key = info.key
  btn.textContent = `📥 CSV`
  const header = container.querySelector('.tab-header')
  if (header) header.appendChild(btn)
}
```

### 5. Descarga CSV

```javascript
function descargarCSV(entidad, datos, columnas) {
  if (!datos || datos.length === 0) { alert('No hay datos para exportar'); return }
  const keyMap = CSV_DATA_MAP[entidad]?.keyMap || mapearColumnas(entidad, columnas)
  let csv = '\uFEFF'  // BOM para Excel
  csv += columnas.join(';') + '\r\n'
  datos.forEach(row => {
    const vals = columnas.map(col => {
      const key = keyMap[col]
      let val = key ? String(row[key] ?? '') : ''
      if (val.includes(';') || val.includes('"') || val.includes('\n')) {
        val = `"${val.replace(/"/g, '""')}"`
      }
      return val
    })
    csv += vals.join(';') + '\r\n'
  })
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${entidad}-${new Date().toISOString().slice(0, 10)}.csv`
  a.click()
  URL.revokeObjectURL(url)
}
```

### 6. Mapear columnas a campos BD

Cada columna en español se mapea a su campo real en la BD:

```javascript
function mapearColumnas(entidad, columnas) {
  const MAPS = {
    empresas: { 'Nombre': 'nombre', 'CIF/NIF': 'cif', 'Email': 'email', 'Teléfono': 'telefono', 'Dirección': 'direccion', 'Ciudad': 'ciudad' },
    contactos: { 'Nombre': 'nombre', 'Email': 'email', 'Teléfono': 'telefono', 'Cargo': 'cargo', 'Empresa': 'empresaNombre', 'Departamento': 'departamento' },
    leads: { 'Título': 'titulo', 'Contacto': 'contactoNombre', 'Email': 'email', 'Teléfono': 'telefono', 'Fuente': 'fuente', 'Estado': 'estado', 'Valor': 'valor' },
  }
  const keyMap = {}
  columnas.forEach(col => { keyMap[col] = MAPS[entidad]?.[col] || col.toLowerCase() })
  CSV_DATA_MAP[entidad].keyMap = keyMap
  return keyMap
}
```

### 7. Integración en mostrarTab()

```javascript
// Al final de mostrarTab(tab):
inyectarBtnCSV(tab)
```

### 8. Delegación de clics (event delegation)

```javascript
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.btn-export')
  if (!btn) return
  const key = btn.dataset.key
  const varName = btn.dataset.var
  const data = eval(varName) || []
  const columnas = CSV_DATA_MAP[key]?.columnas || []
  descargarCSV(key, data, columnas)
})
```

## Pitfalls

- **⚠️ Arrays globales vacíos:** el error más común. Si `inyectarBtnCSV` se llama pero `allProductos` está vacío porque `cargarProductos()` no lo guardó, el botón aparece pero descarga 0 filas. **Verificar después de cada cargar*() que el global se pobló.**
- **Botón duplicado:** sin el `if (document.querySelector('.btn-export')) return;` al inicio, cada cambio de tab añade otro botón.
- **Excel no abre el CSV:** falta BOM (`\uFEFF`) al inicio. Sin BOM, Excel en español asume ANSI y los acentos/ñ se rompen.
- **Separador `;` para Excel español:** Excel España usa `;` como separador de listas en CSV (no `,`). Sin esto, todo aparece en una columna.
- **Comillas escapadas:** si un campo contiene `;`, `"`, o `\n`, envolverlo en `""` y escapar `"` como `""`.
- **Patrón `eval()` vs acceso directo:** si los globales se almacenan en un objeto `window._DATA = {}`, usar `window._DATA[entidad]` evita `eval()`. Decisión de diseño: `eval()` es más fácil de añadir sin reestructurar todo el código existente.

## Referencia

- Implementación completa en: `public/js/crm.js` del proyecto CRM Mastermind (`/root/workspace/AdelaTest01/`)
- 22 tabs con CSV export funcional a junio 2026
- Añadido en Tanda 9 del proyecto