# AdelaCRM v2 — Lecciones Aprendidas (Sesión 2026-06-15)

## Resumen de la sesión

Se construyó AdelaCRM v2 desde cero en una sesión: Node.js + Express + TypeScript + sql.js + SPA vanilla. 7 entidades CRUD completas, Pipeline Kanban drag&drop, Calendario, CSS tokens Aurora.

---

## ✅ Lo que funcionó bien

### 1. Arquitectura de una sesión
- **Schema-first:** diseñar el ER antes de codear evita rework
- **db.ts como fuente de verdad:** un archivo con schema + CRUD para cada entidad
- **Route-per-entity:** un router por tabla, siempre con GET/GET:id/POST/PUT/DELETE
- **Modal genérico en frontend:** `abrirModal(titulo, campos, onConfirm)` genera formularios desde un array declarativo — cero HTML por formulario

### 2. Stack para proyectos rápidos
- **sql.js** (no better-sqlite3): cero compilación nativa, funciona en Docker Alpine
- **JWT via createRequire:** la única forma fiable de usar jsonwebtoken en ESM
- **config.ts compartido:** JWT_SECRET en un solo sitio, todos importan de ahí
- **Dockerfile con build tools:** `apk add python3 make g++` para sql.js

### 3. CSS tokens desde el primer día
Definir `:root` variables ANTES de escribir componentes:
```css
:root {
  --blue: #2563eb;
  --radius: 16px;
  --sp-md: 16px;
}
```
Evita el rework de 580 líneas que hicimos al final.

### 4. Pipeline Kanban con drag & drop nativo
HTML5 Drag API + `dataTransfer` — cero dependencias. Funciona en todos los navegadores modernos.

---

## ⚠️ Pitfalls encontrados (con fix)

### 1. Admin login roto tras migración a bcrypt
**Causa:** Admin creado con `pin_hash: NULL` (código viejo). Nuevo código solo acepta bcrypt.
**Fix:** Migración automática en `initDatabase()`:
```typescript
const adminRow = db.exec("SELECT id, pin_hash FROM usuarios WHERE email = 'admin@adelacrm.local'")
if (adminRow[0]?.values[0][1] === null) {
  const pinHash = bcrypt.hashSync(String(process.env.ADMIN_PIN || '1234'), 10)
  db.run("UPDATE usuarios SET pin_hash = ? WHERE email = 'admin@adelacrm.local'", [pinHash])
}
```
**Regla:** Siempre que cambies el formato de un campo, añadir migración automática.

### 2. Test falla tras cambio de schema
**Causa:** Test usaba `nombre` pero schema v2 usa `titulo`.
**Fix:** Actualizar tests en el MISMO commit que el cambio de schema.
**Regla:** Tests y schema están acoplados — cambiar juntos.

### 3. CSS con hex hardcodes
**Causa:** CSS escrito rápido sin tokens → 580 líneas de rework después.
**Fix:** Definir tokens antes de componentes.

### 4. Datos se pierden en NaN
**Causa:** SQLite en contenedor sin volumen persistente.
**Fix conocido:** NaN SÍ soporta volumes persistentes:
- Checkbox "Persistent storage" en cloud.nan.builders
- Mount point: `/data` (NO `/app/data`)
- Limitación: 1 réplica, sin backup
- Para AdelaCRM: cambiar `DB_PATH` de `/app/data/datos.db` a `/data/datos.db`

### 5. SQL injection por interpolación
**Causa:** `WHERE fecha LIKE '${hoy}%'` en vez de parámetro.
**Fix:** Usar parámetros SIEMPRE, incluso para valores "seguros".

---

## 📐 Patrones reutilizables

### Estructura de proyecto Express + TS + ESM
```
src/
├── server.ts          # Express + rutas
├── db.ts              # Schema + CRUD (todas las entidades)
├── types.ts           # Interfaces TS
├── config.ts          # JWT_SECRET compartido
├── middleware/auth.ts  # JWT verification
└── routes/
    └── [entity].ts    # CRUD por entidad
```

### Route file template
```typescript
import { Router } from 'express'
import { obtenerXs, crearX, actualizarX, eliminarX } from '../db.js'
import type { AuthRequest } from '../middleware/auth.js'

const router = Router()

router.get('/', async (req: AuthRequest, res) => {
  const items = await obtenerXs()
  res.json({ items })
})

router.post('/', async (req: AuthRequest, res) => {
  const item = await crearX(req.body)
  res.status(201).json({ item })
})

// ... PUT, DELETE, GET /:id
export default router
```

### Declarative modal system (frontend JS)
```javascript
abrirModal('Título', [
  { name: 'campo', label: 'Etiqueta', type: 'text', required: true },
  { name: 'select', label: 'Opción', type: 'select', options: ['a','b'], optionLabels: ['A','B'] },
], async (data) => {
  await apiFetch('/api/endpoint', { method: 'POST', body: JSON.stringify(data) })
  cerrarModal(); reloadList()
})
```

### Dynamic query builder (db.ts)
```typescript
async function buscar(filtro?: { estado?: string; buscador?: string }) {
  let sql = 'SELECT * FROM tabla WHERE 1=1'
  const params: any[] = []
  if (filtro?.estado) { sql += ' AND estado = ?'; params.push(filtro.estado) }
  if (filtro?.buscador) { sql += ' AND (campo LIKE ?)'; params.push(`%${filtro.buscador}%`) }
  return all(sql, params)
}
```

---

## 🔧 NaN.builders — Persistent Volumes

| Feature | Detalle |
|---------|---------|
| Soportado | ✅ Sí |
| Configuración | Checkbox "Persistent storage" al crear app |
| Mount point | `/data` (NO `/app/data`) |
| Tamaño | `500Mi`, `5Gi`, `1Ti` (Kubernetes format) |
| Réplicas | Máximo 1 efectiva |
| Backup | NO — "Data is lost — there is no backup" |
| Marketplace | postgres-pgvector, qdrant, chromadb |

### Para activar en AdelaCRM:
1. cloud.nanBuilders → app AdelaTest01 → Persistent storage ON
2. Volume size: `1Gi`
3. Cambiar `DB_PATH` en Dockerfile: `/data/datos.db`
4. Crear `/data` en Dockerfile: `RUN mkdir -p /data`

---

## 📊 Métricas de la sesión

| Métrica | Valor |
|---------|-------|
| Entidades CRUD | 7 |
| Tablas DB | 7 |
| Índices DB | 8 |
| Endpoints API | ~25 |
| Archivos fuente | 13 |
| Tests | 5 (todos pasan) |
| Líneas CSS | 258 |
| Líneas JS frontend | 534 |
| Commits | 8 |

---

## 📋 Actualización v2.2 (Sesión 2026-06-16)

### Features añadidas
- **VeriFactu AEAT**: Hash SHA-256 + cadena de facturación + endpoint verificación + anulación
- **Frontend**: 3 nuevos tabs — CV Empleados, Vacaciones, Conexiones (grafo SVG)
- **Tests**: 111 tests en 10 suites, 0 fallos

### Pitfalls nuevos descubiertos

#### 1. Datos de test colisionan con DB persistente
**Síntoma:** Test pasa la primera vez, falla en runs sucesivos con error 500.
**Causa:** SQLite persiste en `/data/datos.db`. Campo con `UNIQUE` constraint recibe el mismo valor → duplicado.
**Fix:** Siempre `Date.now()` o `Math.random()` en datos de test para campos UNIQUE.
```typescript
.send({ nombre: `colabora_con_${Date.now()}`, ... })  // ✅
.send({ nombre: 'colabora_con', ... })                  // ❌ colisiona
```

#### 2. VeriFactu: orden DESC vs ASC en verificación de cadena
**Causa:** `obtenerFacturas()` ordena `creado DESC` por defecto. La verificación de cadena necesita orden ASC cronológico.
**Fix:** `.sort((a, b) => a.creado.localeCompare(b.creado))` después de filtrar emitidas.

#### 3. VeriFactu: hash incluye total que cambia al emitir
**Causa:** Hash se calcula con `total` al crear. Al emitir, `total` se recalcula desde líneas de factura → hash ya no verifica.
**Diseño aceptado:** Solo verifica facturas recién emitidas. Las anteriores con total modificado no verificarán — el test lo acepta.

#### 4. Reutilizar factura emitida en tests
**Causa:** Test 6 marca factura como `emitida`. Test 17 intenta emitir la misma → falla (solo borradores se emiten).
**Fix:** Crear factura nueva para cada test de emisión, no reutilizar la del `before()` hook.
