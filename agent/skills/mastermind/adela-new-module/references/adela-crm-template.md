# AdelaCRM v2 — Plantilla de proyecto CRM con 7 entidades CRUD

## Estructura del proyecto (v2)

```
AdelaTest01/
├── Dockerfile                    # Deploy en NaN con volumen persistente /data
├── .dockerignore                 # node_modules, .git, .env
├── .env.example                  # PORT, JWT_SECRET, ADMIN_PIN, DB_PATH
├── package.json                  # express, sql.js, bcryptjs, typescript
├── tsconfig.json                 # ES2022 module, node resolution
├── docs/
│   └── SCHEMA.md                 # Diagrama ER + descripción de tablas
├── src/
│   ├── types.ts                  # 7 interfaces: Lead, Empresa, Contacto, Oportunidad, Actividad, Nota, Usuario
│   ├── db.ts                     # SQL.js init + CRUD para 7 entidades (~570 líneas)
│   ├── config.ts                 # JWT_SECRET compartido (single source of truth)
│   ├── server.ts                 # Express app, 8 routers, static files, SPA fallback
│   ├── middleware/
│   │   └── auth.ts               # JWT verification middleware (requerirAuth)
│   └── routes/
│       ├── auth.ts               # POST /api/auth/login (bcrypt compare)
│       ├── leads.ts              # CRUD /api/leads + /api/leads/stats
│       ├── empresas.ts           # CRUD /api/empresas (CIF, sector, dirección)
│       ├── contactos.ts          # CRUD /api/contactos (cargo, departamento)
│       ├── oportunidades.ts      # CRUD /api/oportunidades
│       ├── actividades.ts        # CRUD /api/actividades (calendario)
│       ├── notas.ts              # CRUD /api/notas (polimórficas)
│       └── usuarios.ts           # CRUD /api/usuarios (admin only, sanitize pin_hash)
├── public/
│   ├── index.html                # SPA con 7 tabs: Dashboard, Pipeline, Empresas, Contactos, Oportunidades, Calendario, Usuarios
│   ├── css/crm.css               # CSS tokens Aurora (~260 líneas, sin hex hardcodes)
│   └── js/crm.js                 # Frontend vanilla JS (~540 líneas, modal genérico declarativo)
└── tests/
    └── api.test.ts               # Flujo completo: login → crear → listar → stats → opp → usuarios
```

## Schema v2 (7 entidades)

```
usuarios (独立)
empresas (1) ──── (N) contactos
   │                    │
   └──── (N) leads ────┘
            │
            ├──── (N) oportunidades
            ├──── (N) actividades
            └──── (N) notas
```

Ver `references/adela-crm-v2-schema.md` para el schema completo con todos los campos y endpoints.

## Pitfalls críticos (v2)

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

### 3. Express route ordering
- `/stats` (named) MUST come BEFORE `/:id` (parameterized)
- Otherwise `GET /leads/stats` → id='stats' → "Lead no encontrado"

### 4. SQL.js undefined values
- `data.descripcion || ''`, `data.valor || 0`, `data.fechaCierre || null`
- Never pass undefined to sql.js INSERT parameters

### 5. NaN persistent volumes
- NaN soporta volumes persistentes, pero SOLO al crear la app nueva
- Mount point: `/data` (NO `/app/data`)
- DB_PATH debe ser `/data/datos.db`
- Limitación: 1 réplica efectiva, sin backup automático
- Si la app ya existe sin volumen → crear nueva app con Persistent ON
