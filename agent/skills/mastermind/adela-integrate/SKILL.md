---
name: adela-integrate
description: Integrar módulos Adela en un proyecto Express o añadir nuevos tabs/frontend a un CRM Adela existente
---

## Adela Integrate

Skill para integrar módulos Adela en un proyecto Express existente o nuevo, y para añadir nuevos tabs al frontend de un CRM Adela.

### Cuándo usarlo

- El usuario dice "quiero una web con login y panel admin"
- El usuario dice "añade Adela_auth a mi proyecto Express"
- El usuario dice "crea un proyecto Express con Adela integrado"
- El usuario dice "añade un nuevo tab/módulo al CRM" (ej: automatizaciones, contabilidad, etc.)

### Patrón de integración

#### 1. Identificar qué módulos necesita

Según la petición del usuario, seleccionar del registry.json:

```bash
cat /root/workspace/AdelaMasterMind/registry.json
```

Módulos típicos y para qué sirven:
- `Adela_auth` → Login con PIN + JWT + sesiones
- `Adela_admin` → Panel admin + tracking de visitas
- `Adela_health` → Endpoints /health y /ready
- `Adela_i18n` → Internacionalización
- `Adela_db` → Base de datos
- `Adela_cache` → Caché
- `Adela_http` → Cliente HTTP
- `Adela_ai` → Proxy LLM

#### 2. Instalar dependencias

```bash
cd /ruta/del/proyecto
npm install adela-db adela-auth adela-health adela-admin
```

Si los módulos no están publicados en npm, usar path local:
```bash
npm install /root/workspace/Adela/Adela_db
```

#### 3. Configurar módulos

Patrón típico de inicialización:

```typescript
import { createDatabase } from 'adela-db'
import { createAuth, authRouter } from 'adela-auth'
import { createHealthRouter } from 'adela-health'
import { createAdminPanel } from 'adela-admin'
import { createI18n } from 'adela-i18n'
import express from 'express'

async function main() {
  const app = express()
  app.use(express.json())

  // 1. Base de datos (primero — otros dependen de ella)
  const db = await createDatabase({ driver: 'sqlite', path: './datos.db' })
  await db.connect()

  // 2. Internacionalización
  const i18n = await createI18n({ defaultLocale: 'es-ES' })

  // 3. Autenticación
  const auth = createAuth({ db })
  app.use('/auth', authRouter(auth))

  // 4. Health checks
  app.use('/health', createHealthRouter({ version: '1.0.0' }))

  // 5. Admin panel
  const admin = createAdminPanel({ auth, db, prefix: '/admin' })
  app.use('/admin', admin.getRouter())

  // 6. Arrancar
  app.listen(3000, () => console.log('Servidor iniciado en :3000'))
}

main().catch(console.error)
```

#### 4. Rutas públicas vs protegidas

```typescript
// Rutas públicas (no requieren auth)
app.use('/health', healthRouter)
app.use('/login', authRouter)
app.get('/public/*', (req, res) => res.send('Público'))

// Middleware de auth para rutas protegidas
import { requireAuth } from 'adela-auth'

// Rutas protegidas (requieren token JWT)
app.use('/admin', requireAuth, adminRouter)
app.use('/api', requireAuth, apiRouter)
app.get('/perfil', requireAuth, (req, res) => { ... })
```

#### 5. Verificar integración

```bash
# Health check
curl http://localhost:3000/health

# Login
curl -X POST http://localhost:3000/login -H 'Content-Type: application/json' \
  -d '{"pin":"1234"}'

# Admin (requiere token)
curl http://localhost:3000/admin -H 'Authorization: Bearer <token>'
```

### Proyecto completo de ejemplo

Usar el template `adela-express-app`:

```bash
cp -r /root/workspace/AdelaMasterMind/templates/adela-express-app/ /root/workspace/mi-proyecto/
cd /root/workspace/mi-proyecto/
npm install
npm run dev
```

### Dependencias entre módulos

```
Adela_admin → Adela_auth → Adela_db
Adela_admin → Adela_i18n
Adela_health → Adela_time
Adela_auth → Adela_db
```

Siempre inicializar en orden: primero los que no dependen de nadie, luego los que dependen de ellos.

### Seguridad post-integración

Después de integrar módulos, verificar que el proyecto cumple estas normas:

1. **PIN/contraseña hasheado con bcrypt** — nunca texto plano en BD
2. **JWT_SECRET compartido** — un solo `config.ts` exporta el secreto, todos importan de ahí
3. **API sin campos sensibles** — `pin_hash`, `password` nunca en respuestas. Usar `sanitizeUser()`
4. **Admin PIN desde env var** — `process.env.ADMIN_PIN`, nunca hardcodeado
5. **PIN no visible en HTML** — no mostrar credenciales en el frontend
6. **Healthcheck coincide** — Dockerfile `/health` = servidor `/health`
7. **.env.example documentado** — todas las variables de entorno visibles
8. **Migración automática** — si cambia el formato de un campo (plain → hash), detectar y migrar en `initDatabase()`

### CRM v2 Schema (7 entidades)

Para proyectos CRM completos, usar el schema v2 documentado en `references/adela-crm-v2-schema.md`:
- **empresas** (CIF, sector, dirección) → **contactos** (cargo, departamento)
- **leads** con pipeline Kanban (nuevo → ganado/perdido)
- **oportunidades** (valor €, fechas cierre)
- **actividades** calendario (llamada/email/reunion/tarea/nota)
- **notas** polimórficas (lead/empresa/contacto/oportunidad)

### CSS consistente — Preferencia de David

⚠️ **David odia diseños que no encajan** — especificamente mencionó "cuadrados" en el login que no combinaban con el resto.

**Reglas para CSS en apps CRM/internas:**
1. **Tokens CSS primero** — definir `:root` variables ANTES de escribir componentes. Retroactive tokenization = 580 líneas de rework
2. Tokens consistentes (sin hex hardcodes): `--blue: #2563eb`, `--orange: #f97316`
3. Glass cards sutiles (`backdrop-filter: blur(12px)`) — no blancos planos
4. Border radius consistente: `--radius: 16px` para cards, `--radius-sm: 10px` para inputs
5. Responsive SIEMPRE
6. **NO** hacer cuadrados con bordes duros que no combinen con el estilo glass del resto
7. Si hay sidebar + main content, asegurar que ambos usan los mismos tokens
8. Botones: ghost para secundarios, primary para acciones principales
9. Modales: mismo estilo glass que las cards
10. Badges de color por estado (colores definidos en tokens, no inline)

### Deploy en NaN — Persistent Volumes

⚠️ **NaN soporta volúmenes persistentes, pero SOLO al crear la app nueva.**

| Feature | Detalle |
|---------|---------|
| Configuración | Checkbox "Persistent storage" al crear app |
| Mount point | `/data` (NO `/app/data`) |
| Tamaño | `500Mi`, `5Gi`, `1Ti` (Kubernetes format) |
| Réplicas | Máximo 1 efectiva |
| Backup | NO — "Data is lost — there is no backup" |

**Para activar:**
1. cloud.nanBuilders → Crear nueva app → Persistent storage ON
2. Volume size: `1Gi` mínimo
3. DB_PATH: `/data/datos.db`
4. Dockerfile: `RUN mkdir -p /data`

**Si la app ya existe sin volumen:** crear app NUEVA con Persistent ON. No se puede añadir a una existente.

### Añadir nuevos tabs al frontend CRM

Cuando se necesita añadir un nuevo módulo/tab a un CRM Adela existente (AdelaTest01), seguir este patrón de 4 pasos:

#### Paso 1: Añadir nav link en index.html

Insertar en `<ul class="nav-links">`, después del último `<li>`:
```html
<li><a href="#" data-tab="nuevo-tab">🔣<span> Nombre Tab</span></a></li>
```

#### Paso 2: Añadir tab div en index.html

Insertar en `<main class="main-content">`, en la posición deseada (orden visual del sidebar). Tres patrones:

**Patrón tabla** (para listas de datos):
```html
<div id="tab-nuevo-tab" class="tab">
  <div class="tab-header">
    <h1>Título</h1>
    <button id="btn-new-entidad" class="btn btn-primary">+ Nueva Entidad</button>
  </div>
  <div class="table-container glass-card">
    <table class="data-table">
      <thead><tr><th>Col1</th><th>Col2</th><th>Acciones</th></tr></thead>
      <tbody id="entidades-table-body"></tbody>
    </table>
  </div>
</div>
```

**Patrón cards grid** (para visualización tipo kanban/cards):
```html
<div id="tab-nuevo-tab" class="tab">
  <div class="tab-header">
    <h1>Título</h1>
    <button id="btn-new-entidad" class="btn btn-primary">+ Nueva Entidad</button>
  </div>
  <div class="cards-grid" id="entidades-grid"></div>
</div>
```

**Patrón complejo** (dashboard con resumen + tablas múltiples, ej: Contabilidad):
```html
<div id="tab-nuevo-tab" class="tab">
  <div class="tab-header">
    <h1>Título</h1>
    <div class="tab-actions">
      <button id="btn-new-a" class="btn btn-primary">+ Nueva A</button>
      <button id="btn-new-b" class="btn btn-ghost">+ Nueva B</button>
    </div>
  </div>
  <div class="charts-row" style="margin-bottom:24px">
    <div class="chart-section glass-card">
      <h3>Resumen</h3>
      <div id="resumen-container" style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;padding:12px">
        <div><small>Label1</small><br><strong id="res-val1">0</strong></div>
        <div><small>Label2</small><br><strong id="res-val2">0</strong></div>
      </div>
    </div>
  </div>
  <div class="table-container glass-card">
    <h3>Tabla 1</h3>
    <table class="data-table">
      <thead><tr><th>Col</th><th>Acciones</th></tr></thead>
      <tbody id="tabla1-body"></tbody>
    </table>
  </div>
</div>
```

#### Paso 3: Añadir JS en crm.js

**3a. Registrar en cambiarTab():**
```javascript
if (tab === 'nuevo-tab') cargarEntidades()
```

**3b. Función de carga:**
```javascript
async function cargarEntidades() {
  try {
    const data = await apiFetch('/api/entidades')
    const entidades = data.entidades || data.data || []
    const tbody = document.getElementById('entidades-table-body')
    tbody.innerHTML = entidades.length === 0
      ? '<tr><td colspan="N" class="empty-state">Sin datos</td></tr>'
      : entidades.map(e => `<tr>...`).join('')
  } catch (err) { console.error('Error entidades:', err) }
}
```

**3c. Botón crear:**
```javascript
document.getElementById('btn-new-entidad')?.addEventListener('click', () => {
  abrirModal('Nueva Entidad', [
    { name: 'campo1', label: 'Campo 1', type: 'text', required: true },
    { name: 'campo2', label: 'Campo 2', type: 'number' }
  ], async (data) => {
    await apiFetch('/api/entidades', { method: 'POST', body: JSON.stringify(data) })
    cerrarModal(); cargarEntidades()
  })
})
```

**3d. Helpers disponibles** (ya definidas en crm.js, usar sin reimplementar):
- `apiFetch(url, options)` — fetch con auth bearer
- `formatEuro(n)` → "1.234€"
- `formatDate(d)` → "15 jun 2026"
- `estadoBadge(estado)` → span con color según estado
- `abrirModal(titulo, campos, onConfirm)` → modal genérico
- `cerrarModal()` → cierra modal

#### Paso 4: Verificar

- Nav link aparece en sidebar
- Tab div tiene `id="tab-nombre"` y clase `tab`
- `cambiarTab()` llama la función de carga
- Botón tiene listener con `?.addEventListener` (optional chaining — previene errores si el botón no existe en otro contexto)
- Usar helpers existentes: `apiFetch()`, `formatEuro()`, `formatDate()`, `estadoBadge()`, `abrirModal()`, `cerrarModal()`

**Nota:** El backend necesita los endpoints API correspondientes (`/api/entidades`, etc.) para que funcione el data fetching. El frontend es la capa de presentación; la lógica de negocio está en el servidor.

#### Paso 5: Auditar compatibilidad Frontend↔Backend

**⚠️ OBLIGATORIO tras añadir tabs.** Verificar que TODAS las llamadas `apiFetch` del nuevo tab tienen rutas backend equivalentes. Ver procedure completa en `crm-erp-fullstack` → "Auditoría de compatibilidad Frontend↔Backend".

Resumen rápido:
```bash
grep -oP "apiFetch\(['\"]([^'\"]+)" public/js/crm.js | sed "s/apiFetch(['\"]//g" | sort -u > /tmp/frontend-rutas.txt
grep -oP "\"(/api/[^\"]+)\"" src/app.ts | tr -d '"' | sort -u > /tmp/backend-rutas.txt
comm -23 /tmp/frontend-rutas.txt /tmp/backend-rutas.txt
```

Si hay rutas sin match → crear convenience routes en `app.ts` o añadir la ruta en el router correspondiente.

### Ejemplo reciente: Automatizaciones + Contabilidad (2026-06-16)

Se añadieron dos tabs al CRM:
- **Automatizaciones**: patrón cards grid, con disparador/acción, modal con JSON config
- **Contabilidad**: patrón complejo (resumen financiero + bancos + asientos + cuentas), dos botones (asiento/cuenta)

Ver `references/crm-tab-addition-pattern.md` para los detalles completos de la implementación.