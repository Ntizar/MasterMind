# Auditoría de Aplicación CRM Completa (AdelaTest01)

Patrón para auditar una aplicación CRM completa (no módulos individuales).
Usar cuando el usuario pide auditar el proyecto AdelaTest01 o cualquier app CRM Adela desplegada.

## Metodología

Una auditoría CRM cubre 5 dimensiones. Ejecutar en orden:

```
Proyecto: /root/workspace/AdelaTest01
URL:      https://adelatest01-ntizar-ntizar.apps.nan.builders/
```

**⚠️ Regla de workflow:** diagnosticar TODOS los bugs primero, luego arreglar UNO a UNO. No mezclar cambios de distintos bugs en el mismo commit. Compilar/verificar después de cada fix. Ver "Pitfall: un bug a la vez en la app CRM" en SKILL.md.

### D1 — Responsive Móvil

1. Cargar web en browser con viewport 375x812 (iPhone)
2. Verificar:
   - Sidebar colapsa/hamburger (toggle con clase `.open`)
   - Iconos visibles en modo 60px (emoji directamente en `<a>`, texto en `<span>` que se oculta)
   - Touch targets ≥ 44px (aplicado en media query 768px con `min-height: 48px`)
   - Tablas scroll horizontal
   - Modal ocupa ≤ 95% width
   - iOS zoom prevention: `font-size: 16px` en inputs (línea 277)
3. Inspeccionar CSS `@media (max-width: 768px)` en `crm.css`

**Pitfall conocido (FIXED ✅):** El CSS oculta `.nav-links a span` para que en móvil queden solo los iconos. El HTML ahora tiene `<span>` envolviendo el texto (emoji queda fuera del span). Si en futuras versiones se quita el span, los enlaces se vuelven invisibles en móvil.

### D2 — Marca Blanca / Multi-Tenant

Verificar:
1. ¿Existe tabla `tenants` en BD? → `db.ts` línea ~454
2. ¿Hay rutas CRUD `/api/tenants`? → `tenants.ts`
3. ¿Las queries de datos filtran por `tenantId`? → Buscar `WHERE tenantId` o `AND tenantId` en `db.ts`
4. ¿El frontend usa datos del tenant (logo, colores)? → Buscar `tenant.logo` o `tenant.colores` en `crm.js`
5. ¿El login discrimina por tenant?
6. ¿Hay detección por subdominio/dominio?

**Pitfall:** Si la tabla `tenants` existe pero ninguna tabla de datos tiene columna `tenantId`, el multi-tenant no funciona: todos los datos son globales.

**Estado actual (2026-06-16):** Backend tiene CRUD completo de tenants con campos `logo`, `colores`, `modulosActivos`, `plan`. Pero:
- Ninguna tabla de datos tiene `tenantId` (usuarios, empresas, leads, etc. — todos globales)
- Frontend no carga branding del tenant (sidebar hardcode "🚀 AdelaCRM")
- No hay middleware de tenant en queries
- Para implementar marca blanca real, añadir: `tenantId` a usuarios + todas las tablas → middleware → frontend dinámico

### D3 — Base de Datos y Relaciones

Verificar:
1. `PRAGMA foreign_keys = ON` — Buscar en `db.ts` (línea 47, ✅ presente)
2. `PRAGMA journal_mode = WAL` — Buscar en `db.ts` (línea 48, ✅ presente)
3. ¿Cascade deletes o eliminación manual de hijos? — Buscar `DELETE FROM` previo al DELETE principal.
4. Consistencia TypeScript ↔ SQLite — Comparar nombres de campos en tipos con columnas CREATE TABLE.
5. Índices en FK — `CREATE INDEX IF NOT EXISTS idx_...`
6. Valores por defecto correctos

**Pitfall:** sql.js (SQLite WASM) no activa FK constraints automáticamente. Sin `PRAGMA foreign_keys = ON` al inicio, los hijos huérfanos se acumulan. ✅ Fijado desde v4.0.

### D4 — Bugs Frontend-Backend (Field Mismatch)

Los bugs más comunes en apps CRUD son field name mismatches entre:

| Origen | Archivo |
|--------|---------|
| Frontend envía | `public/js/crm.js` — campos en objetos pasados a `apiFetch` |
| Backend espera | `src/routes/*.ts` — destructuring en body |
| BD almacena | `src/db.ts` — columnas en INSERT/UPDATE |
| TypeScript define | `src/types.ts` — interfaces |
| **DB update function** | `src/db.ts` — key whitelist en `actualizar*` (ver anti-patrón abajo) |

**Proceso:** Para cada entidad (productos, presupuestos, facturas, etc.):
1. En `crm.js` buscar la función que recoge datos del modal y los envía
2. En `routes/*.ts` buscar `req.body` destructuring
3. En `db.ts` buscar los nombres de columna del INSERT/UPDATE
4. En `types.ts` buscar la interfaz
5. **En `db.ts` buscar el key loop del UPDATE** (`for (const k of [...])`)
6. Si los 5 no coinciden → bug

**Patrones típicos de mismatch:**
- Frontend usa nombre simplificado (`precio`, `coste`, `clienteId`) pero BD/tipos usan nombre completo (`precioVenta`, `precioCoste`, `empresaId`)
- Frontend usa `tipoIva` como número pero BD espera string ('general'|'reducido'|etc.)
- Frontend envía `fechaEmision` pero BD columna es `fechaExpedicion`
- Calendario: actividades no tienen campo `estado`, tienen `resultado`
- **🔴 Anti-patrón: ruta envía campos que la función update no acepta.** Ejemplo: `presupuestos.ts` recalcula y envía `{ baseImponible, totalIva, total }`, pero `actualizarPresupuesto()` solo actualiza los keys de `['empresaId','contactoId','fechaEmision','fechaValidez','estado','subtotal','descuentoGlobal','ivaTotal','irpf','recargoEquivalencia','total','moneda','notasInternas','condiciones']`. Así que `baseImponible`/`totalIva` se ignoran silenciosamente. ✅ **Fijado: ahora envía `subtotal`/`ivaTotal`.**

### D5 — Seguridad y Estabilidad

Verificar:
- `JWT_SECRET` — ¿es estable o se regenera en cada reinicio? (Buscar `crypto.randomUUID()` en `config.ts`) → ✅ **Fijado: persistido en `/data/jwt_secret.txt`**
- Rate limiting en login — ¿hay `express-rate-limit` en auth? → ✅ **Fijado 2026-06-16: 5 intentos/min/IP en POST /login**
- SQL injection potencial — ¿template strings en queries? (Buscar `${...}` en SQL) → ⚠️ Verificar dashboard y búsquedas con LIKE
- Paginación — ¿hay `LIMIT` + `OFFSET` en consultas GET? → ⚠️ Solo en actividades (fijado 2026-06-16). El resto trae todo.
- PIN por defecto — Buscar `ADMIN_PIN` en `.env.example`
- Validación de entrada — ¿se sanitiza `req.body`?

**Pre-existing TS lint errors:** Los archivos `middleware/auth.ts` y `routes/auth.ts` usan `createRequire(import.meta.url)` que el linter del workspace flaggea con `error TS1343`, pero con `"module": "ES2022"` en tsconfig compila perfectamente. **Falso positivo del linter.**

## Plantilla de Informe

```markdown
## Auditoría: [Nombre App]

| Dimensión | Estado |
|-----------|--------|
| D1 — Responsive | ✅ / ❌ / ⚠️ |
| D2 — Multi-tenant | ✅ / ❌ / ⚠️ |
| D3 — BD relaciones | ✅ / ❌ / ⚠️ |
| D4 — Field mismatches | N bugs detectados |
| D5 — Seguridad | ✅ / ❌ / ⚠️ |

### Bugs críticos (🔴)
| # | Bug | Archivo | Impacto |
|---|-----|---------|---------|

### Bugs importantes (🟡)
...

### Funcionalidades a añadir
| Prioridad | Funcionalidad | Motivo |
|-----------|--------------|--------|
| 🔴 | ... | ... |
```

## Historial de bugs CRM

| Fecha | Bug | Gravedad | Estado |
|-------|-----|----------|--------|
| 2026-06-16 | Iconos sidebar invisibles en móvil (CSS oculta `a span` sin span) | 🔴 | ✅ Ya fijado antes de la auditoría |
| 2026-06-16 | Productos: frontend envía `precio`/`coste`, BD espera `precioVenta`/`precioCoste` | 🔴 | ✅ Ya fijado |
| 2026-06-16 | Presupuestos: frontend envía `clienteId`, BD espera `empresaId` | 🔴 | ✅ Ya fijado |
| 2026-06-16 | JWT_SECRET regenerado en cada reinicio (`crypto.randomUUID()`) | 🔴 | ✅ Ya fijado (persistido en disco) |
| 2026-06-16 | **Sin rate limiting en login** | 🔴 | ✅ Fijado 2026-06-16 (express-rate-limit, 5/min) |
| 2026-06-16 | Calendar usa `a.estado` pero Actividad tiene campo `resultado` | 🔴 | ✅ Ya fijado |
| 2026-06-16 | **Dashboard sin LIMIT en backend — trae TODAS las actividades** | 🟡 | ✅ Fijado 2026-06-16 (parámetro `?limite=5`) |
| 2026-06-16 | **Presupuestos: recalculo envía `baseImponible`/`totalIva`, update solo acepta `subtotal`/`ivaTotal`** | 🔴 | ✅ Fijado 2026-06-16 |
| 2026-06-16 | Calendar: colores de actividad siempre azul (fallback) porque `a.resultado` no está en `ESTADO_COLORS` | 🟡 | ✅ Fijado 2026-06-16 (añadidos `pendiente`🟡, `completada`🟢, `cancelada`🔴) |
| 2026-06-16 | Oportunidades muestra leadId crudo en vez de nombre | 🟡 | Pendiente |
| 2026-06-16 | Ticket update usa `sla` pero BD tiene `slaLimite` | 🟡 | Falso positivo — era consistente |
| 2026-06-16 | Sin paginación en ninguna lista | 🟡 | Pendiente |
| 2026-06-16 | SQL injection potencial en dashboard (`fecha LIKE '${hoy}%'`) | 🟡 | Pendiente |
| 2026-06-16 | PRAGMA foreign_keys = ON no ejecutado | 🔴 | ✅ Ya fijado (línea 47) |