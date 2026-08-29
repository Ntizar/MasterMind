# CRM Tab Addition Pattern — Referencia

## Contexto

Añadir nuevos tabs al frontend de AdelaCRM (AdelaTest01) — `index.html` + `crm.js`.

## Archivos modificados

- `/root/workspace/AdelaTest01/public/index.html` — estructura HTML
- `/root/workspace/AdelaTest01/public/js/crm.js` — lógica JS

## Patrones de tab

### Patrón tabla (listas)
- `tab-header` con título + botón "+ Nueva X"
- `table-container glass-card` con `data-table`
- `tbody id="entidades-table-body"`

### Patrón cards grid (kanban/cards)
- `tab-header` con título + botón
- `cards-grid` con `id="entidades-grid"`
- Cada card: `empresa-card glass-card` con header, contacto, meta

### Patrón complejo (dashboard + tablas)
- `charts-row` con `chart-section glass-card` para resumen
- Múltiples `table-container glass-card` para tablas
- Múltiples botones en `tab-actions`

## Helpers disponibles en crm.js

| Función | Uso |
|---------|-----|
| `apiFetch(url, options)` | Fetch con auth bearer |
| `formatEuro(n)` | "1.234€" |
| `formatDate(d)` | "15 jun 2026" |
| `formatDateTime(d)` | "15 jun 2026, 10:30" |
| `estadoBadge(estado)` | Span con color por estado |
| `abrirModal(titulo, campos, onConfirm)` | Modal genérico |
| `cerrarModal()` | Cierra modal |

## Implementación reciente: Automatizaciones

- **Tipo**: cards grid
- **API**: `GET /api/automatizaciones`
- **Campos**: nombre, descripcion, activo, disparadorTipo, disparadorConfig, accionTipo, accionConfig
- **Modal**: nombre, descripcion, activo (select), disparadorTipo (select), disparadorConfig (textarea JSON), accionTipo (select), accionConfig (textarea JSON)
- **Render**: cards con iconos por tipo de disparador/acción, badges de estado

## Implementación reciente: Contabilidad

- **Tipo**: complejo (resumen + tablas)
- **APIs**: `GET /api/contabilidad`, `GET /api/contabilidad/cuentas`
- **Resumen**: cuentas totales, asientos mes, debe total, haber total
- **Bancos**: filtro por tipo='banco' o codigo empieza con '57'
- **Asientos tabla**: numero, fecha, concepto, debe, haber, estado, acciones
- **Cuentas tabla**: codigo, nombre, tipo, nivel, estado
- **Modales**: nuevo asiento (fecha, concepto, debe, haber, estado), nueva cuenta (codigo, nombre, tipo, nivel)

## Checklist post-implementación

- [ ] Nav link en sidebar con `data-tab`
- [ ] Tab div con `id="tab-nombre"` y clase `tab`
- [ ] `cambiarTab()` registra la función de carga
- [ ] Botón con `?.addEventListener` (optional chaining)
- [ ] Función de carga con try/catch + console.error
- [ ] Renderizado con empty-state si no hay datos
- [ ] Helpers existentes reutilizadas (no reimplementar)
- [ ] Backend endpoints disponibles para data fetching
