# dieta-masterfit — Arquitectura completa (v4.0.0)

## Estructura

```
dieta-masterfit/
├── server.js              ← Express backend (SQLite + auth + APIs + IA + sync GitHub)
├── dashboard.html         ← SPA vanilla JS + Chart.js + Aurora (3 tabs + overflow)
├── data/
│   ├── database.json      ← Backup legacy (se migra a SQLite al primer arranque)
│   └── masterfit.db       ← SQLite (fuente de verdad)
├── .env                   ← NAN_API token (NO en git, SÍ en Docker via COPY)
├── Dockerfile             ← NaN Builders deploy (node:20-alpine, non-root)
├── .dockerignore          ← node_modules, .git, .gitignore (NO .env)
├── .gitignore             ← node_modules, npm-debug.log*, .env
├── package.json           ← express + sql.js
└── scripts/               ← CLIs de registro rápido
```

**Repo:** `github.com/Ntizar/dieta`
**URL NaN:** `dieta-ntizar-ntizar.apps.nan.builders`
**Versión:** v4.0.0 (SQLite + auth simplificada + dashboard reestructurado)

## Base de datos SQLite (sql.js)

### Tablas
- `usuarios` — id, nombre, created_at
- `sesiones` — id, usuario_id, token, expires_at
- `comidas` — id, usuario_id, fecha, comida, kcal, proteinas, hidratos, grasas, created_at
- `pesos` — id, usuario_id, fecha, peso_kg, created_at
- `pasos` — id, usuario_id, fecha, pasos, created_at
- `entrenamientos` — id, usuario_id, fecha, tipo, duracion_min, kcal, created_at
- `inbody` — id, usuario_id, fecha, peso_kg, grasa_kg, musculo_kg, agua_pct, grasa_pct, created_at

### Migración automática
Al primer arranque, si existe `database.json` pero no `masterfit.db`, se migra automáticamente:
```javascript
if (!dbExists && fs.existsSync(JSON_FALLBACK)) {
  await migrateFromJSON();  // Importa todos los registros del JSON
}
```

## Auth: Nombre simple (sin contraseña)

- Login por nombre: si el usuario es nuevo, se crea; si ya existe, se verifica el nombre
- Sesión: token de 32 bytes hex, almacenado en localStorage, expira en 7 días
- Limpieza automática de sesiones expiradas (cada hora)
- Middleware: `requireAuth` comprueba header `X-Session-Id`

## Endpoints API

### Auth
- `POST /api/auth/login` → Login/registro por nombre
- `GET /api/auth/me` → Info del usuario actual

### Datos (CRUD completo)
- `GET /api/datos` → Todos los datos del usuario
- `POST /api/peso` → Registrar peso (+ sync GitHub)
- `POST /api/comida` → Registrar comida (+ sync GitHub)
- `POST /api/deporte` → Registrar ejercicio (+ sync GitHub)
- `PUT /api/:tipo/:index` → Editar registro genérico (+ sync GitHub)
- `DELETE /api/:tipo/:index` → Borrar registro genérico (+ sync GitHub)

### IA
- `POST /api/ia/consejo` → Coach "Amadeo Llados" (chat contextual)
- `POST /api/estimar-comida` → Estima kcal/macros desde descripción
- `POST /api/estimar-ejercicio` → Estima kcal quemadas desde descripción

## Dashboard: 3 tabs + overflow

### Tabs principales (siempre visibles)
1. **Registrar** — Acción rápida (comida, peso, pasos, ejercicio)
2. **Coach IA** — Chat WhatsApp-style con Amadeo
3. **Proyecciones** — Gráfico de peso con predicción por regresión lineal

### Tabs secundarios (☰ Más)
4. Resumen del día
5. Historial
6. Progreso
7. Exportar
8. Configuración

**Pitfall:** Los tabs del menú "Más" son lazy-loaded — NO ejecutar loadXxx() al inicio.

## Sync a GitHub

```javascript
async function syncGitHub() {
  const token = getNanToken();
  if (!token) return;
  const dbData = fs.readFileSync(DB_PATH);
  const b64 = dbData.toString('base64');
  // GET SHA → PUT base64 content
}
```

Llamar en TODOS los endpoints de mutación. NaN containers pierden filesystem en redeploy.

## Dependencias
- `express` — HTTP server + routing
- `sql.js` — SQLite puro JS (WASM), sin compilación nativa

## Deploy NaN
- `.env` se copia al contenedor via `COPY . .` (no va en .dockerignore)
- Usuario no-root en Dockerfile (`USER appuser`)
- Puerto 5050 (process.env.PORT || 5050)
- Healthcheck: `/healthz` (público, sin auth)
- NaN hace auto-deploy por polling cada 1-5 min tras push a `main`

## Datos de referencia (David)
- Edad: 36 años
- Altura: 174 cm
- Peso objetivo: 88 kg
- Peso inicial: 98.6 kg
- TMB ~1838 kcal, TDEE ~2527 kcal (ligero)
- Macros objetivo: ~155g prot, ~221g hidr, ~78g grasa (déficit 500)
