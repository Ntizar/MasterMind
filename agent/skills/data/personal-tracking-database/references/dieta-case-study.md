# Dieta v3 — Caso de Estudio: Sistema de Seguimiento Personal

## Resumen

Implementación concreta del patrón `personal-tracking-database` para seguimiento de dieta/peso/deporte/pasos. Incluye:
- Base de datos SQLite (masterfit.db) como fuente de verdad de LladosApp
- Dashboard HTML con Chart.js + Aurora Design System
- Scripts CLI de registro rápido
- Proyecciones con regresión lineal
- Estimación IA de macros (Amadeo coach)
- Multi-usuario con onboarding IA
- Deploy en NaN Builders con syncGitHub

## Arquitectura

```
dieta-masterfit/
├── data/masterfit.db          ← SQLite, fuente de verdad de LladosApp
├── data/database.json         ← Legacy JSON (NO usar en producción)
├── dashboard.html             ← Dashboard interactivo
├── server.js                  ← Express backend + IA
├── scripts/registro.py        ← CLI registro
├── Dockerfile                 ← NaN Builders deploy
└── .env                       ← NAN_API token
```

## Patrones Clave

### 1. SQLite como fuente de verdad (NO database.json)
LladosApp lee de `masterfit.db` (SQLite), no de `database.json`. Siempre verificar la DB real de la app antes de escribir datos.

### 2. Estimación IA con Preview-Edit-Confirm
- Frontend llama a `/api/estimar-comida` → IA devuelve JSON
- Frontend muestra preview editable (inputs en vez de spans)
- Usuario confirma → se registra con valores editados

### 3. Multi-usuario con Onboarding IA
- Login → si nuevo usuario, Amadeo entrevista paso a paso (5 preguntas)
- Datos aislados por `usuario_id` en todas las tablas

### 4. Proyecciones con Regresión Lineal
- Filtrar solo pesajes de mañana (consistencia)
- Regresión lineal (mínimos cuadrados) sobre TODOS los puntos
- 5 escenarios: Real, Sostenible, Normal, Acelerado, Agresivo

### 5. Sync GitHub para persistencia en NaN
- `syncGitHub()` tras cada mutación en NaN Builders
- `downloadGitHubDB()` al iniciar contenedor

## Pitfalls Documentados

- LladosApp usa SQLite, NO database.json
- Peso hardcodeado en prompts IA → usar `contextoPerfil(db)`
- `const charts` vs `var charts` en frontend
- Duplicación de `const` causa SyntaxError silencioso
- Endpoint faltante en backend → botón no funciona
- Nombre de campo mismatch frontend/backend
- CDN Aurora: `Ntizar/Ntizar-Aurora` (con guion), no `Ntizar/Aurora`
- Index.html = dashboard para GitHub Pages (no landing estática)
- Verificar deploy ANTES de confirmar "hecho"
- `readDB()` obligatorio antes de usar `contextoPerfil(db)`
