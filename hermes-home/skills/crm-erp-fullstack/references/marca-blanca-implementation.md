# Marca Blanca Multi-tenant — CRM

## Resumen

Patrón para implementar marca blanca (white-label) en un CRM multi-tenant: cada cliente (tenant) tiene su propio logo, colores, y nombre de aplicación, sin que el usuario final vea referencias al software base.

El patrón cubre: migración de `tenantId` en usuarios, endpoint de branding, inyección dinámica de CSS variables en frontend, y persistencia en localStorage.

## Flujo completo

```
1. Login: backend autentica usuario + obtiene tenantId
2. Backend devuelve { token, usuario: {...tenantId...} }
3. Frontend, tras login, llama GET /api/tenants/{tenantId}
4. Backend devuelve { logo, nombre, colores: { primario, secundario, fondo } }
5. Frontend: inyecta CSS variables + actualiza sidebar/logo/nombre
6. Persiste en localStorage para sobrevida a recargas
```

## Backend

### 1. Migración de BD — tenantId en usuarios

```sql
-- Ya en CREATE TABLE (nuevos proyectos):
CREATE TABLE IF NOT EXISTS usuarios (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  pin_hash TEXT,
  rol TEXT NOT NULL DEFAULT 'gestor',
  activo INTEGER NOT NULL DEFAULT 1,
  tenantId TEXT,                     -- ← MARCA BLANCA
  creado TEXT NOT NULL
);

-- Migración para tablas existentes (ejecutar en initDatabase):
const usuariosCols = db.exec("PRAGMA table_info(usuarios)").flatMap(r => r.values.map(v => v[1]))
if (!usuariosCols.includes('tenantId')) {
  db.run("ALTER TABLE usuarios ADD COLUMN tenantId TEXT")
}
```

### 2. Endpoint GET /api/tenants/:id — branding

```typescript
router.get('/:id', async (req, res) => {
  try {
    const tenant = await obtenerTenantPorId(req.params.id as string)
    if (!tenant) { res.status(404).json({ error: 'Tenant no encontrado' }); return }
    // Devolver SOLO branding, nunca secrets internos
    res.json({
      id: tenant.id,
      nombre: tenant.nombre,
      logo: tenant.logo,
      colores: (() => {
        // Intentar parsear JSON, fallback a valores por defecto
        try { return JSON.parse(tenant.colores || '{}') } catch { return {} }
      })()
    })
  } catch (error) {
    res.status(500).json({ error: 'Error al obtener tenant' })
  }
})
```

### 3. Login devuelve tenantId

```typescript
// En src/routes/auth.ts — al hacer login exitoso:
res.json({
  token,
  usuario: {
    id: usuario.id,
    nombre: usuario.nombre,
    email: usuario.email,
    rol: usuario.rol,
    tenantId: usuario.tenantId    // ← NUEVO
  }
})
```

## Frontend

### 4. Fetch de branding tras login

```javascript
// En crm.js — dentro del handler de login exitoso:
async function cargarBranding(user) {
  if (!user.tenantId) return  // Sin tenant → usar defaults
  try {
    const { tenant } = await apiFetch(`/api/tenants/${user.tenantId}`)
    if (!tenant) return
    aplicarBranding(tenant)
    localStorage.setItem('crmmastermind_branding', JSON.stringify(tenant))
  } catch (err) {
    console.warn('Branding no disponible:', err)
  }
}
```

### 5. Aplicar branding (CSS variables + elementos)

```javascript
function aplicarBranding(tenant) {
  if (!tenant) return
  const root = document.documentElement

  // Colores: defaults si no definidos
  const colores = tenant.colores || {}
  const primario = colores.primario || '#2563eb'
  const secundario = colores.secundario || '#f97316'
  const fondo = colores.fondo || '#f1f5f9'

  root.style.setProperty('--brand-primary', primario)
  root.style.setProperty('--brand-secondary', secundario)
  root.style.setProperty('--brand-bg', fondo)

  // También sobreescribir los tokens CSS del sistema si el tenant los define
  root.style.setProperty('--blue', primario)
  root.style.setProperty('--naranja', secundario)

  // Nombre de la app (si el tenant tiene nombre propio)
  if (tenant.nombre) {
    document.querySelectorAll('.app-name, .sidebar h1, .sidebar h2').forEach(el => {
      el.textContent = tenant.nombre
    })
    document.title = tenant.nombre
  }

  // Logo (URL del tenant o emoji por defecto)
  if (tenant.logo) {
    const logoImgs = document.querySelectorAll('.sidebar-logo img, .login-logo img')
    logoImgs.forEach(img => { img.src = tenant.logo })
    const logoTxt = document.querySelectorAll('.sidebar-logo, .logo')
    logoTxt.forEach(el => { el.style.display = 'none' })  // ocultar texto, mostrar img
    // Alternativamente: crear/actualizar <img>
  }
}
```

### 6. Persistencia en localStorage

```javascript
// Al cargar la app, restaurar branding previo:
const saved = localStorage.getItem('crmmastermind_branding')
if (saved) {
  try { aplicarBranding(JSON.parse(saved)) } catch {}
}
```

Esto permite que entre recargas de página el branding se mantenga sin llamada API extra.

## Estructura de la tabla tenants

```sql
CREATE TABLE IF NOT EXISTS tenants (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  logo TEXT,
  colores TEXT,       -- JSON: {"primario":"#...","secundario":"#...","fondo":"#..."}
  modulosActivos TEXT,-- JSON array: ["productos","presupuestos","facturas",...]
  plan TEXT DEFAULT 'basic',  -- basic, professional, enterprise
  activo INTEGER DEFAULT 1,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL
);
```

## CSS — Variables obligatorias en el frontend

```css
:root {
  --blue: #2563eb;
  --naranja: #f97316;
  --fondo: #f1f5f9;
  --brand-primary: var(--blue);      /* ← se sobreescribe dinámicamente */
  --brand-secondary: var(--naranja); /* ← se sobreescribe dinámicamente */
  --brand-bg: var(--fondo);          /* ← se sobreescribe dinámicamente */
}
```

**⚠️ Importante:** El CSS debe usar `var(--brand-primary)` y `var(--brand-secondary)` en vez de `var(--blue)` y `var(--naranja)` directamente, para que los valores dinámicos del tenant tengan efecto.

## Pitfalls

- **❌ Sin fallback de colores:** si el tenant no tiene `colores` definidos o el JSON es inválido, el frontend se queda sin colores. **Siempre tener defaults** (`primario: '#2563eb'`, `secundario: '#f97316'`).
- **❌ No persistir errores:** si la API de tenants falla (500, 404), el branding no se aplica. **No guardar en localStorage** si la respuesta fue error — mantiene el branding anterior.
- **❌ CSS duro con `--blue` en vez de `--brand-primary`:** los tokens del sistema (`--blue`, `--naranja`) no se sobreescriben automáticamente. Verificar que el CSS usa `var(--brand-*)` en los lugares clave (botones, headers, enlaces activos).
- **❌ Logos rotos:** si `tenant.logo` es una URL que no carga (CORS, dominio caído, enlace roto), mostrar un fallback visual (emoji 🔤 o iniciales del tenant).
- **❌ Olvidar la migración:** si la BD existente no tiene la columna `tenantId`, el login crashea al devolver `undefined`. Siempre ejecutar `ALTER TABLE` con `PRAGMA table_info` check.
- **❌ localStorage + múltiples tenants:** si el usuario cambia de tenant (superadmin), hay que limpiar el branding previo y cargar el nuevo.

## Referencia

- Implementación completa en: `src/routes/auth.ts`, `src/routes/tenants.ts`, `public/js/crm.js`, `src/db.ts` del proyecto CRM Mastermind (`/root/workspace/AdelaTest01/`)
- Añadido en Tanda 9 (junio 2026)