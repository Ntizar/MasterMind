# MasterFit v4 — Auditoría completa (2026-06-14)

## Contexto
App Node.js + Express + sql.js (SQLite) + frontend vanilla JS inline. 1600+ líneas dashboard.html, 980+ líneas server.js. El usuario dice "no me deja ni entrar".

## Pass 1 — Fix obvio (2 bugs encontrados)
- `sendChat()` sin cerrar `}` → rompía todo el JS
- 3 errores de comillas en ternarias `'var(--danger)")` → syntax error

**Resultado:** El JS compila, el dashboard carga, el login funciona. El agente dice "arreglado".

## Pass 2 — Deep audit via delegate_task (10 bugs más)

### CRÍTICOS (3)
1. **Chat history key mismatch** — SQL devolvía `rol`/`contenido`, frontend esperaba `role`/`content`. Chat vacío al recargar página.
   - Fix: `SELECT rol AS role, contenido AS content`
2. **`perfil` undefined en `renderResumen()`** — variable `perfil` no existía en scope, debería ser `perfilData`
   - Fix: Cambiar referencia
3. **`totalAgua` undefined en `renderResumen()`** — nunca se calculaba el total de agua
   - Fix: Añadir `var totalAgua = aguaToday.reduce(...)`

### ALTOS (2)
4. **Delete roto para comida/entrenamiento** — frontend envía singulares (`comida`), backend solo acepta plurales (`comidas`)
   - Fix: Añadir aliases en `ALLOWED` map: `{comida:'comidas', ...}`
5. **JSON.parse sin try-catch en inbody_history** — datos corruptos → 500
   - Fix: Wrap en try-catch + filter(Boolean)

### MEDIOS (3)
6. **XSS en chat** — assistant messages pasaban por `formatMarkdown()` sin `escapeHtml()` previo
   - Fix: `escapeHtml(stripThink(m.content))` antes de formatMarkdown
7. **SQL injection en PUT /api/:tipo/:index** — columnas de user input directo a SQL
   - Fix: Whitelist de columnas por tabla
8. **Cutout duplicado en Chart.js doughnut** — `cutout: '65%'` en datasets[0] Y en options
   - Fix: Eliminar de datasets[0]

### BAJOS (2)
9. **escapeHtml sin single quotes** — faltaba `&#39;`
10. **initDB() sin mkdirSync** — deploys nuevos fallan si no existe `data/`
11. **syncGitHub() sin await** — no garantiza persistencia antes de respuesta

## Lecciones

### 1. "No funciona" = auditoría completa, no fix rápido
El primer fix visible (braces) era 2 de 12 bugs. Los otros 10 estaban debajo.

### 2. Patrones de bugs recurrentes en Node+HTML apps
- **Key mismatch** entre SQL y frontend (bilingüe: español/inglés mezclado)
- **Singular vs plural** en rutas REST (comida vs comidas)
- **Variables undefined** en funciones de render (scope leakage)
- **JSON.parse sin try-catch** en datos de BD
- **XSS** en chat/markdown renderers

### 3. delegate_task para auditorías
Manual: 2 bugs en ~10 min. delegate_task: 12 bugs en ~5 min. ROI claro para proyectos >500 líneas.

### 4. Verificación post-fix
Siempre: syntax check → brace balance → grep de funciones clave → test funcional en navegador.
