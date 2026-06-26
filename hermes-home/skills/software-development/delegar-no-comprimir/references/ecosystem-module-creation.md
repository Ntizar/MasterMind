# Caso real: Ecosistema Adela (6 módulos en paralelo)

**Fecha:** 2026-06-14  
**Meta:** 6 módulos Node.js/TypeScript de utilidad base creados, testeados y pusheados a GitHub en una sola sesión  
**Resultado:** ~5000 líneas TS, 180 tests (175 ✅ 5 ❌), 6 repos en GitHub, sesión de ~40 min

## Arquitectura

Cada módulo es un paquete npm independiente en `github.com/Ntizar/Adela_*`:

| Módulo | Descripción | Tests | Source | Deps runtime |
|--------|-------------|-------|--------|--------------|
| Adela_time | Timezone Madrid: reloj solar, festivos, UTC/MAD | 46 ✅ | esios-dashboard/src/shared/time/madrid.js | 0 |
| Adela_env | Validación y parseo de variables de entorno | 8 ✅ | esios-dashboard/src/config/env.js | 0 |
| Adela_http | Cliente HTTP con batching, retry, backoff, jitter | 20 ✅ | esios-dashboard/src/infra/clients/esios.client.js | 0 |
| Adela_cache | Caché dual memory+disk con métricas TTL | 35 ✅ | esios-dashboard/src/infra/cache/* | 0 |
| Adela_health | Health checks sistema + Express router `/health/readiness` | 30 ✅ | Desde cero, patrón estándar | 0 |
| Adela_auth | Auth: bcrypt + JWT + rate limiting + Express middleware | 41/46 ❌5 | Desde cero (NO MasterFit - PINs plano) | bcryptjs, jsonwebtoken, sql.js |

## Prompts exactos para delegación paralela

Cada subagente recibió un prompt como este:

```
Crea un módulo TypeScript "Adela_<nombre>" en /root/workspace/Adela/Adela_<nombre>/

ESTRUCTURA DE ARCHIVOS:
- package.json (type:module, name: "adela-<nombre>", version: "1.0.0")
- tsconfig.json (strict, ES2022, declarations, sourceMap, rootDir: "src")
- src/index.ts (barrel export)
- src/<nombre>.ts (implementación)
- src/types.ts
- tests/<nombre>.test.ts
- README.md

REQUISITOS:
- TypeScript strict mode
- Zero dependencias runtime (salvo excepción justificada)
- TODO en castellano (nombres, comentarios, errores, README)
- Cobertura mínima 80%
- Build: tsc → dist/
- Test: tsx --test tests/*.test.ts
- Sin default exports (usar named exports)

CÓDIGO FUENTE DE REFERENCIA:
Leer /root/workspace/esios-dashboard/src/<ruta>
Extraer la lógica y generalizarla como módulo independiente

API A EXPONER:
[Lista de funciones/clases con firma completa]

AL TERMINAR:
1. Ejecuta: npm test
2. Ejecuta: npm run build
3. Confirma que ambos pasan sin errores
```

## Fases de la sesión

1. **Plan:** Auditoría del plan existente + estructura raíz + GitHub auth + definir template común
2. **Batch 1 (3 módulos P0):** Adela_time (46 tests), Adela_env (8 tests), Adela_http (20 tests) — creados en paralelo en ~5 min
3. **Fix post-batch:** Ajustes en tsconfig rootDir y package.json paths en Adela_http
4. **Batch 2 (3 módulos P1):** Adela_cache (35 tests), Adela_health (30 tests), Adela_auth (41/46 tests)
5. **Fixes post-batch:** Variables no usadas, tsconfig, strict mode fixes en Adela_auth

## Errores encontrados y soluciones

### 1. tsconfig rootDir incorrecto → dist/src/ en vez de dist/
**Síntoma:** tsc compila a `dist/src/index.js` y `dist/tests/index.js` en vez de `dist/index.js`  
**Causa:** `rootDir: "."` combinado con `include: ["src/**/*.ts", "tests/**/*.ts"]`  
**Fix:** `rootDir: "src"` + `include: ["src/**/*.ts"]` (excluir tests del build)  
**Detectar:** `grep "rootDir" tsconfig.json` — si es `"."`, hay que cambiarlo

### 2. package.json main apunta a ruta incorrecta
**Síntoma:** Al hacer `import { x } from 'adela-modulo'`, falla porque no encuentra el módulo  
**Causa:** `"main": "dist/src/index.js"` pero tsc compila a `dist/index.js`  
**Fix:** `"main": "dist/index.js"`, `"types": "dist/index.d.ts"`

### 3. Vitest vs node:test — no mezclar
**Síntoma:** Tests que usan `describe`/`it` de `node:test` fallan con vitest  
**Causa:** Algunos módulos usan `node:test` (`import { describe, it } from 'node:test'`) y el script de test intenta vitest  
**Fix:** Usar `"test": "tsx --test tests/*.test.ts"` cuando los tests importan de `node:test`. Usar vitest solo si los tests importan de `vitest`.

### 4. Tests HTTP reales en Adela_auth — rate limiting interfiere
**Síntoma:** 5 tests fallan por código HTTP incorrecto (espera 200, recibe 429)  
**Causa:** Los tests de rate limiting activan el contador, y los tests siguientes (POST /login, GET /me) se bloquean porque el rate limit no se limpia entre tests  
**Fix:** Resetear rate limiter entre tests o usar rate limit con Redis desactivado en tests

### 5. Variables no usadas en TypeScript strict
**Síntoma:** `tsc --noEmit` falla por variables declaradas pero no usadas  
**Causa:** TypeScript strict mode activa `noUnusedLocals: true`  
**Fixes posibles:**
- Eliminar la variable (mejor)
- Prefijar con `_` (ej: `_userId` vs `userId`) cuando el parámetro es requerido por interfaz
- Usar `// @ts-expect-error` solo como último recurso (ensucia el código)



## Lecciones aprendidas (Batch 1 — Fase 1+2)

1. **3 módulos en paralelo = ~5 min cada uno.** Hacerlo secuencial tomaría 15-20 min. La ganancia es real.
2. **Los módulos zero-deps (time, env, http, cache, health) se crean más rápido** que los con dependencias (auth).
3. **Siempre fijar rootDir en tsconfig.** Es el error más común.
4. **Los tests de auth HTTP con rate limiting necesitan reset entre tests.** No asumir que Express se comporta como mock.
5. **Incluir README.md con "Integración con otros Adela"** — esto fuerza a pensar en cómo se relacionan los módulos entre sí y mejora la documentación.
6. **Push a GitHub al final** — mejor esperar a tener todos los módulos funcionando antes de exponerlos públicamente.
7. **El patrón es replicable para cualquier ecosistema** — no solo Adela. Sirve para crear un sistema de plugins, un SDK, o una colección de utilidades.

---

## Fase 3: Auth fixes + export + ai + db (2026-06-14)

**Batch 3 (3 módulos P2 + auth fixes):** Se delegaron 3 subagentes en paralelo para crear `Adela_export`, `Adela_ai`, `Adela_db`. Paralelamente se hicieron fixes en `Adela_auth`.

### Resultados finales: 274/274 tests ✅ — 9 módulos

| Módulo | Tests | Creado | Fuente |
|--------|-------|--------|--------|
| Adela_export | 61 ✅ | Subagente | Exportación CSV/JSON/PDF (pdf-lib) |
| Adela_ai | 21 ✅ | Subagente | Proxy LLM OpenAI-compatible con SSE |
| Adela_db | 7 ✅ | Subagente | sql.js adapter con transacciones |
| Adela_auth (fixes) | 46 ✅ (subió de 41) | Directo | 4 bugs corregidos (ver abajo) |

### Auth fixes: 4 bugs en Adela_auth

#### Bug 1: Fecha ISO vs SQLite
**Problema:** `createSession` guardaba fechas en ISO 8601 (`2026-06-14T21:37:00.000Z`), pero `cleanExpiredSessions` comparaba con `datetime('now')` de SQLite (formato `YYYY-MM-DD HH:MM:SS`). La comparación fallaba porque SQLite no entiende la 'T' ni los milisegundos ISO.

**Fix:** Normalizar en el origen (`createToken`):
```typescript
toISOString().replace('T', ' ').replace(/\.\d+Z$/, '')
```

**Lección:** SIEMPRE que guardes fechas en SQLite para comparar con `datetime('now')`, usa formato SQLite (`YYYY-MM-DD HH:MM:SS`). No confíes en que SQLite parsea ISO.

#### Bug 2: rateLimitStore global (contaminación entre tests)
**Problema:** `rateLimitStore` era una variable global del módulo. Los tests de rate limiting dejaban contadores sucios, y los tests siguientes (POST /login, GET /me) recibían 429 Too Many Requests.

**Fix:** Mover `rateLimitStore` al closure de `createAuth()`:
```typescript
export function createAuth(cfg) {
  const rateLimitStore: Map<string, RateLimitEntry> = new Map();
  // ... cfg usa rateLimitStore desde el closure
}
```

**Lección:** En módulos con estado mutable y tests HTTP, la función factory (`createX()`) debe encapsular TODO el estado interno. Nada global. Esto permite instancias aisladas en tests.

#### Bug 3: Refresh token buscaba por token, no por refresh_token
**Problema:** El endpoint `/api/auth/refresh` buscaba la sesión por `refreshToken` (el JWT principal), no por `refresh_token` (el token de refresh largo). `deleteSession` borraba por el token equivocado.

**Fix:** Añadir `findSessionByRefreshToken` a la interfaz `AuthDB` y usarlo en el refresh handler:
```typescript
export interface AuthDB {
  findSessionByRefreshToken(token: string): Promise<Sessión | null>;
  // ...
}
```

**Lección:** Cuando tienes dual-token (access + refresh), la DB debe tener métodos específicos para cada tipo. No asumir que `findSession(token)` funciona para ambos.

#### Bug 4: JWT sin jti → UNIQUE constraint en mismo segundo
**Problema:** Dos JWTs creados en el mismo segundo tenían el mismo `iat` y `sub` (usuario), violando el constraint UNIQUE de la DB.

**Fix:** Generar `jti` aleatorio en cada token:
```typescript
const jti = Math.random().toString(36).slice(2, 14) + Date.now().toString(36);
```

**Lección:** SIEMPRE incluir `jti` (JWT ID) en tokens JWT si la DB tiene constraints de unicidad. No confiar en `iat` + `sub` como par único.

### Sibling file conflict (nuevo pitfall)

**Problema:** Los subagentes de `Adela_export`, `Adela_ai`, y `Adela_db` se ejecutaron en paralelo. El subagente de `db` y un hermano (de `export`) crearon ambos archivos en `/root/workspace/Adela/Adela_db/src/`:
- `src/sqlite.ts` (correcto, del subagente de db)
- `src/database.ts` (extra, de otro subagente)
- `tests/sqlite-adapter.test.ts` (correcto, del subagente de db)
- `tests/sqlite.test.ts` (extra, de otro subagente)

Los tests fallaban con TS error porque importaban archivos duplicados.

**Fix:** `rm -f database.ts pg-adapter.ts sqlite-adapter.ts migrations.ts` — limpiar archivos huérfanos post-delegación.

**Lección:** Los subagentes no respetan límites de directorio. Si dos subagentes escriben al mismo directorio, pueden solaparse. **Siempre verificar** que cada módulo tenga EXACTAMENTE los archivos esperados después de delegación paralela.

### GitHub repo creation via API

Para crear repos y pushear desde cero:

```bash
# 1. Verificar que el repo no existe
curl -s -o /dev/null -w "%{http_code}" \
  "https://api.github.com/repos/Ntizar/Adela_<module>"

# 2. Crear repo vía API
curl -s -X POST "https://api.github.com/user/repos" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"name":"Adela_<module>","description":"...","private":false}'

# 3. Push con token en URL remota
git remote add origin "https://Ntizar:$TOKEN@github.com/Ntizar/Adela_<module>.git"
git push -u origin main

# 4. Verificar
curl -s "https://api.github.com/repos/Ntizar/Adela_<module>" | head -5
```

**Pitfall:** El token DEBE ir en la URL del remote. `git push` sin token en la URL falla en modo no-interactivo.