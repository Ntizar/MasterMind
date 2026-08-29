# Adela Express Project Template

Plantilla para crear proyectos Express + TypeScript + ESM con frontend estático.

## Uso

1. Copiar el directorio completo a tu nuevo proyecto
2. `npm install`
3. Renombrar en package.json (name, description)
4. Actualizar `src/server.ts` con tus rutas
5. `npm run build && npm run dev`

## Stack

- TypeScript ES2022 + moduleResolution: node
- ESM native (import/export, import.meta)
- Express + sql.js (sin compilación nativa)
- jsonwebtoken via createRequire (pitfall ESM)
- Frontend estático en public/

## Pitfalls conocidos

- JWT: usar createRequire, NUNCA import * as jwt
- SQLite: sql.js en vez de better-sqlite3 (no necesita make)
- tsconfig: module=ES2022, moduleResolution=node

## Estructura

```
src/
├── server.ts          # Express + rutas
├── db.ts              # Capa datos (SQL.js)
├── types.ts           # Tipos TS
├── middleware/
│   └── auth.ts        # Middleware JWT con createRequire
└── routes/
    ├── auth.ts        # Login + perfil
    ├── leads.ts       # CRUD + stats
    ├── usuarios.ts    # CRUD usuarios
    └── oportunidades.ts # CRUD opps
public/
├── index.html         # SPA
├── css/               # Estilos
└── js/                # Lógica frontend
```
