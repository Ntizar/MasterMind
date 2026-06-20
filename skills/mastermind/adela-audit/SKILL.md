---
name: adela-audit
description: Auditoría de calidad de módulos Adela — verifica que cumplen los estándares del ecosistema
---

## Adela Audit

Skill para auditar un módulo Adela existente y verificar que cumple los estándares del ecosistema.

### Cuándo usarlo

**Auditoría de MÓDULOS (paquetes individuales):**
- Acabas de crear un módulo Adela y quieres verificar calidad
- El usuario pregunta "¿este módulo está bien?"
- Quieres hacer un barrido de calidad de todos los módulos
- Antes de publicar un módulo en GitHub
- **Después de implementar un módulo del backend roadmap** (seguridad, observabilidad, escalabilidad, api-layer)

**Auditoría de APLICACIÓN CRM (proyecto completo AdelaTest01):**
- El usuario pregunta "audita el CRM, mira qué errores ves"
- Quieres verificar responsive, multi-tenant, BD, bugs frontend-backend
- Antes de un deploy a producción o demo a cliente
- Ver referencias `references/crm-application-audit.md` para el checklist completo

### ⚠️ Regla CRÍTICA: Todos los repos Adela deben ser PRIVADOS

Verificar en la auditoría que el repo GitHub es privado. Si no, el usuario lo exige.

### Checklist de auditoría

Ejecutar para cada módulo:

```bash
MODULO=/root/workspace/Adela/Adela_<NOMBRE>
```

#### 1. ✅ TypeScript strict

```bash
grep -q '"strict": true' $MODULO/tsconfig.json && echo "✅ strict mode" || echo "❌ No strict"
grep '"noUnusedLocals": true' $MODULO/tsconfig.json || echo "⚠️  Sin noUnusedLocals"
```

#### 2. ✅ package.json correcto

Verificar campos:
- `name`: debe empezar por `adela-`
- `version`: semver
- `type`: `"module"` — **⚠️ pitfall frecuente: módulos creados sin este campo** (Adela_auth, Adela_metrics)
- `main` y `types`: apuntan a `dist/`
- `scripts`: debe tener `build` y `test`
- `devDependencies`: debe tener `typescript` y `tsx` (o vitest/jest)

**Paso 2b — verificación visual rápida:**
```bash
node -e "const p=require('$MODULO/package.json');console.log(p.type==='module'?'✅ type:module':'❌ FALTA type:module')"
```

```bash
node -e "
const p = require('$MODULO/package.json');
const checks = {
  name: p.name?.startsWith('adela-'),
  version: !!p.version,
  type: p.type === 'module',
  main: p.main?.includes('/dist/') || p.main?.startsWith('dist/'),
  types: p.types?.includes('/dist/') || p.types?.startsWith('dist/'),
  buildScript: !!p.scripts?.build,
  testScript: !!p.scripts?.test,
  typescript: !!p.devDependencies?.typescript,
  tsx: !!p.devDependencies?.tsx
};
Object.entries(checks).forEach(([k,v]) => console.log(v ? '✅' : '❌', k));
"
```

**🔴 PITFALL — `startsWith('dist/')` falla con `"./dist/..."`:**

Los módulos Adela usan `\"./dist/index.js\"` como valor de `main` y `types`. `\"./dist/index.js\".startsWith(\"dist/\")` devuelve `false` → **falso negativo en la auditoría**.

**Solución:** usar `.includes('/dist/')` en vez de `.startsWith('dist/')`. Esto funciona tanto para `"./dist/index.js"` como para `"dist/index.js"`.

#### 3. ✅ Tests pasan

**Pitfall:** Los módulos Adela usan `tests/` (plural), NO `test/`. No buscar en `test/`.

```bash
# Verificar que existe directorio de tests
ls -d $MODULO/tests/ && echo "✅ Directorio tests/ existe" || echo "❌ Falta tests/"

# Contar archivos de test
find $MODULO/tests/ -name "*.test.ts" | wc -l

# Ejecutar tests
cd $MODULO && npm test 2>&1 | tail -5
```

Buscar: `# pass N` y `# fail 0`

#### 4. ✅ Build compila

```bash
cd $MODULO && npm run build 2>&1
```

Debe terminar con exit code 0.

#### 5. ✅ README completo

```bash
grep -q "Quick Start" $MODULO/README.md && echo "✅ Quick Start" || echo "❌ Falta Quick Start"
grep -q "## API" $MODULO/README.md && echo "✅ API section" || echo "❌ Falta API section"
grep -q "Integración con otros Adela" $MODULO/README.md && echo "✅ Integración" || echo "❌ Falta Integración"
```

#### 6. ✅ Zero deps o justificadas

```bash
DEPS=$(node -e "console.log(Object.keys(require('$MODULO/package.json').dependencies||{}).length)")
echo "Dependencias runtime: $DEPS"
[ "$DEPS" -gt 3 ] && echo "⚠️  Más de 3 deps, revisar"
```

#### 7. ✅ Código en castellano

```bash
grep -rn "console.log\\|console.error" $MODULO/src/ | grep -v "castellano\\|español" | head -5
# Verificar que errores y comentarios están en español
```

#### 8. ✅ README explica la arquitectura

```bash
grep -qi "arquitectura\|cómo funciona\|flujo\|flow" $MODULO/README.md && echo "✅ Explica arquitectura" || echo "⚠️  Sin explicación de arquitectura"
# El usuario valora que se explique el porqué, no solo el qué
```

#### 9. ✅ Repo PRIVADO en GitHub

```bash
source /hermes-home/.env 2>/dev/null
NOMBRE=$(basename $MODULO)
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/Ntizar/$NOMBRE" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print('✅ PRIVADO' if d.get('private') else '❌ PÚBLICO')" 2>/dev/null || echo "⚠️  No se pudo verificar (sin token?)"
```

#### 10. ✅ Test runner consistency

**⚠️ Pitfall CRÍTICO:** Los módulos Adela usan test runners distintos. Los módulos legacy (time, env, http, cache, health, auth) pueden usar `vitest` o `jest`; los nuevos (export, ai, db, i18n, admin, api, metrics) usan `tsx --test` o `vitest`. Hay que detectarlo y reportarlo.

```bash
# Detectar qué test runner usa cada módulo
cd $MODULO
RUNNER=$(node -e "
const p = require('./package.json');
const t = p.scripts?.test || '';
if (t.includes('vitest')) console.log('vitest');
else if (t.includes('jest')) console.log('jest');
else if (t.includes('tsx --test') || t.includes('node --test')) console.log('tsx');
else console.log('unknown: ' + t);
")
echo "Test runner: $RUNNER"
case "$RUNNER" in
  vitest|tsx) echo "✅ Runner moderno" ;;
  jest) echo "⚠️  Jest — legacy, considerar migrar" ;;
  *) echo "⚠️  Runner no reconocido" ;;
esac
```

Para auditoría batch, reportar también la consistencia:
```bash
# Desde /root/workspace/Adela/, listar runners de todos los módulos
for m in Adela_*; do 
  r=$(node -e "const p=require('./$m/package.json');const t=p.scripts?.test||'';console.log(t.includes('vitest')?'vitest':t.includes('jest')?'jest':t.includes('tsx --test')?'tsx (node)':'?')" 2>/dev/null)
  echo "$m → $r"
done | sort -k2
```

#### 11. ✅ Index.ts barrel export completo

**⚠️ Pitfall:** Adela_auth tuvo bugs porque el index.ts no exportaba correctamente `docs/` ni `types`. Verificar que el barrel export cubre TODO:

```bash
# Verificar que index.ts exporta TODOS los .ts de src/ (excepto types.ts que va aparte)
cd $MODULO
SRC_FILES=$(find src/ -name "*.ts" ! -name "types.ts" ! -name "index.ts" | sort)
EXPORTED=$(grep "^export" src/index.ts | grep -oP "'[^']+'" | tr -d "'" | sort)
DIFF=$(diff <(echo "$SRC_FILES" | sed 's|^src/||;s|\.ts$||') <(echo "$EXPORTED" | sed 's|^\./||') 2>&1)
[ -z "$DIFF" ] && echo "✅ Todos los módulos exportados" || echo "⚠️  Módulos no exportados o extras en index.ts:"
[ -z "$DIFF" ] || echo "$DIFF"
```

#### 12. ✅ Docs folder (si aplica)

```bash
# Algunos módulos (auth, admin) tienen carpeta docs/ con documentación
[ -d "$MODULO/docs" ] && echo "✅ docs/ existe" || echo "ℹ️  Sin docs/ (opcional)"
```

### Casos conocidos de bugs (historial de auditorías)

| Módulo | Bug | Fecha | Solución |
|--------|-----|-------|----------|
| Adela_auth | index.ts no exportaba docs/ ni tipos | 2026-06-14 | Añadido export `./docs/index`, `./types` |
| Adela_auth | README.md incompleto sin sección Integración | 2026-06-14 | Añadida sección |
| Adela_auth | package.json sin `"type": "module"` | 2026-06-14 | Añadido |
| Adela_security | Test runner: package.json decía `tsx --test` pero tests importaban de `vitest` | 2026-06-15 | Cambiar script a `vitest run` |
| Adela_logger | Test runner: package.json decía `node --test` pero tests importaban de `vitest` | 2026-06-15 | Cambiar script a `vitest run` |
| Adela_errors | `mockNext()` usaba `Object.assign(next, ctx)` — copia valores primitivos, `next.called` siempre `false` | 2026-06-15 | Usar `Object.defineProperty` con getters |
| Adela_errors | Test verificaba `writable: false` en AppError pero TypeScript `readonly` es solo compile-time | 2026-06-15 | Cambiar test a verificar `hasOwnProperty` |
| Adela_metrics | package.json sin `"type": "module"` — el checklist lo menciona en paso 2 pero no se verifica en el checklist visual de reporte final | 2026-06-16 | Añadido paso 2b con verificación explícita en reporte |
| Adela_jobs | Auditoría flaggeaba `main` y `types` como ❌ con `startsWith('dist/')` aunque el valor era `"./dist/index.js"` (correcto) | 2026-06-16 | Cambiado a `.includes('/dist/')` en paso 2b |

### ⚠️ Pitfall: no intentar hacer todo de golpe

**David ha corregido explícitamente** el patrón de "auditar/fixear 16 módulos de una vez". El problema: respuestas largas que se cortan por timeout, o subagentes que no terminan.

**Patrón correcto para módulos:**
1. Primero diagnóstico rápido (ver qué falla)
2. Fix UN módulo, verificar que pasa
3. Siguiente módulo
4. Resumen al final

Nunca: "voy a arreglar todos los módulos, crear READMEs, y hacer el starter template" en una sola iteración.

### ⚠️ Pitfall: un bug a la vez en la app CRM

**David ha corregido explícitamente** también para la aplicación CRM: "Vete de una en una para no romper el proyecto."

**Patrón correcto para CRUD app:**
1. Diagnosticar todos los bugs primero (sin tocar código)
2. **⚠️ Re-verificar ANTES de reportar:** el proyecto puede haber evolucionado desde la última auditoría. Por cada bug identificado:
   - Leer el código actual (no confiar en el diagnóstico inicial)
   - Verificar commits recientes: `git log --oneline -10` para ver si hubo fixes
   - Confirmar que el bug sigue presente (ej: sidebar responsive roto → leer el CSS/HTML actual)
   - Reportar solo bugs CONFIRMADOS, no presuntos
3. Priorizar por gravedad
4. Arreglar UN bug, compilar/verificar
5. Siguiente bug
6. Resumen al final con estado actualizado

**Caso real (2026-06-25):** Auditoría encontró 6 bugs "frescos" que ya estaban arreglados en una tanda anterior. El sidebar responsive, productos `precio`/`coste` → `precioVenta`/`precioCoste`, presupuestos `clienteId` → `empresaId`, JWT_SECRET volátil, calendar `a.estado` → `a.resultado`, y `PRAGMA foreign_keys` ya funcionaban. Solo 2 bugs eran reales (rate limiting y dashboard LIMIT). La re-verificación ahorró reportar 4 falsos positivos.

Nunca: hacer 5 cambios en 5 archivos distintos en una sola iteración — si falla, no sabes cuál lo rompió.

### 13. ✅ registry.json actualizado

```bash
grep -q '"id": "Adela_<NOMBRE>"' /root/workspace/AdelaMasterMind/registry.json && echo "✅ En registry" || echo "❌ No está en registry"
```

**Pitfall:** El campo en registry.json es `"id"`, no `"name"`. La búsqueda debe ser `"id": "Adela_<NOMBRE>"`.

### Reporte de auditoría

Formato de salida:

```markdown
## Auditoría: Adela_<NOMBRE>

| Aspecto | Estado |
|---------|--------|
| TypeScript strict | ✅ |
| package.json | ✅ |
| type: module | ✅ |
| Tests | ✅ (N pass, 0 fail) |
| Build | ✅ |
| README | ✅ |
| README explica arquitectura | ✅ |
| Zero deps | ⚠️ (N deps) |
| Castellano | ✅ |
| Repo PRIVADO | ✅ |
| En registry | ✅ |

**Estado general:** ✅ Aprobado / ❌ Necesita revisión
```

### Auditoría batch de todos los módulos

Cuando el usuario pide "audita el proyecto Adela" (todos los módulos), usar `execute_code` en vez de bash uno por uno — mucho más eficiente.

```python
# execute_code: escanear todos los módulos de golpe
from hermes_tools import read_file
import json, os

modulos = ["Adela_time", "Adela_env", "Adela_http", "Adela_cache", "Adela_db",
           "Adela_auth", "Adela_health", "Adela_ai", "Adela_export", "Adela_i18n",
           "Adela_admin", "Adela_mailer", "Adela_api", "Adela_metrics", "Adela_jobs",
           "Adela_ws", "Adela_cli", "Adela_search"]

for mod in modulos:
    path = f"/root/workspace/Adela/{mod}"
    # Verificar: package.json, tsconfig.json, README.md, src/, tests/
    # tests/ usa plural (NO test/)
    # tsconfig debe tener "strict": true
    # package.json name debe empezar por "adela-"
    ...
```

Verificar en cada módulo:
- `package.json` existe y `name` empieza por `adela-`
- `tsconfig.json` tiene `"strict": true`
- `README.md` existe
- `src/` existe
- `tests/` existe (⚠️ plural, no `test/`)
- Contar archivos `*.test.ts` en `tests/`
- Contar `dependencies` runtime en `package.json`
- **Detectar test runner** (vitest/jest/tsx) y reportar consistencia
- **Verificar index.ts barrel export** cubre todos los src/*.ts
- **Verificar `"type": "module"`** en package.json
- Verificar `registry.json` en `/root/workspace/AdelaMasterMind/registry.json` — el campo es `"id"`, no `"name"`

### 14. ✅ Auditoría de aplicación CRM (referencia externa)

Para auditar la aplicación CRM completa (AdelaTest01), cargar el reference:

```
skill_view(name='adela-audit', file_path='references/crm-application-audit.md')
```

Cubre 5 dimensiones:
- **D1** — Responsive móvil (viewport, sidebar, touch targets)
- **D2** — Marca blanca / multi-tenant (aislamiento de datos, UI dinámica)
- **D3** — Base de datos y relaciones (FK enforcement, orfandad, índices)
- **D4** — Field mismatches frontend↔backend (el bug más común)
- **D5** — Seguridad (JWT, rate limiting, SQL injection, paginación)

Ver el reference para checklist completo, pitfall conocido por dimensión, y plantilla de informe.

| Problema | Solución |
|----------|----------|
| No strict mode | Añadir `"strict": true` al tsconfig.json |
| Tests fallan | Revisar y arreglar tests |
| Build falla | Leer error de tsc y corregir tipos |
| Falta README | Copiar de template y rellenar |
| No en registry | Añadir entrada al registry.json |
| Faltan exports | Verificar src/index.ts barrel export |