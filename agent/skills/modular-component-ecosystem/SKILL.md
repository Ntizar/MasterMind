---
name: modular-component-ecosystem
version: "1.0.0"
description: "Diseñar un ecosistema de módulos base reutilizables (@namespace/*) para construir proyectos multi-usuario sin arrastrar deuda técnica — desde análisis de señales (GitHub stars, proyectos existentes) hasta definición de paquetes con principios de diseño."
tags: [architecture, modular, reusable-components, npm-packages, design-system, backend-modules, ecosystem-design, multi-tenant]
---

# Modular Component Ecosystem — Diseño de Módulos Base Reutilizables

## Cuándo cargar esta skill

Cuando el usuario pida:
- "Crear piezas reutilizables para construir proyectos más grandes"
- "Módulos base como LEGO para montar ERPs"
- "Extraer código compartido entre proyectos"
- "Crear un ecosistema de componentes como Aurora pero para backend"
- "Diseñar un sistema de paquetes internos"
- "No arrastrar deuda técnica entre proyectos"

## Concepto

Crear un ecosistema de paquetes npm internos (`@namespace/*`) que encapsulen responsabilidades únicas, probadas y reutilizables. Cada proyecto nuevo se construye ensamblando estos módulos, no copiando código.

**Analogía:** Aurora es el "design system visual" (`@nous/aurora`). Este skill es el "design system de backend" (`@nous/time`, `@nous/http`, etc.).

## Principios de diseño

1. **Cada módulo = una responsabilidad única** — nunca más de una razón para cambiar
2. **Zero dependencies entre módulos** — cada módulo funciona standalone
3. **TypeScript first** — tipos para todo, JS vanilla compatible con JSDoc
4. **Tests obligatorios** — sin tests, no se publica
5. **SemVer estricto** — breaking changes = nueva versión mayor
6. **README con ejemplos** — cada módulo tiene "quick start"
7. **TODO en castellano** — nombres de funciones, docs, comentarios
8. **No extraer deuda** — si el código fuente tiene bugs, reescribir desde cero

## Flujo de trabajo (5 pasos)

### Paso 1: Analizar señales de interés

Antes de diseñar módulos, entender hacia dónde va el usuario:

```bash
# GitHub stars del usuario — señales de dirección
curl -s "https://api.github.com/users/{USER}/starred?per_page=100&page=1" | \
  python3 -c "
import json, sys
for repo in json.load(sys.stdin):
    print(f\"{repo['full_name']:45s} | ⭐{repo['stargazers_count']:5d} | {repo.get('description','')[:80]}\")
"
```

**Qué buscar en las stars:**
- **Arquitectura modular/plugin-based** → QueAI, NocoBase, Huly
- **Multi-tenant/multi-usuario** → Twenty, EspoCRM, SuiteCRM
- **API integrations** → Nango, Postgres MCP
- **Data privacy/security** → Microsoft Presidio
- **3D + geoespacial** → GeoLibre, Three.js, maptalks.three

### Paso 2: Auditar proyectos existentes

Analizar los proyectos activos del usuario para identificar:
- Módulos que ya existen (código reutilizable)
- Deuda técnica (código que NO se puede extraer)
- Patrones repetidos entre proyectos (candidatos a módulo)

**Comandos clave:**
```bash
# Estructura de directorios
find /path/to/project -type f -name "*.js" -o -name "*.ts" | head -50

# Líneas por archivo (monolitos)
wc -l /path/to/project/server.js

# Código duplicado entre proyectos
diff -rq /path/to/project1/src /path/to/project2/src | grep "Only in"
```

**Categorizar hallazgos:**
| Categoría | Acción | Ejemplo |
|-----------|--------|---------|
| ✅ Código limpio y probado | Extraer como módulo | ESIOS http client con tests |
| ⚠️ Funcional pero con deuda | Reescribir desde cero | MasterFit PINs en texto plano |
| ❌ No existe | Crear desde cero | Módulo de notificaciones |

### Paso 2.5: Auditoría detallada módulo por módulo (Plan vs Código)

Cuando el plan indica módulos basados en código existente, hacer auditoría POR CADA módulo candidato:

**Checklist por módulo:**
1. ✅ **¿Existe en GitHub?** — `curl -s "https://api.github.com/users/{USER}/repos?per_page=100" | jq '.[].name' | grep -i "modulo"`
2. ✅ **¿Existe en local?** — `find /root/workspace -type d -name "*{modulo}*" 2>/dev/null`
3. ✅ **Código fuente real** — Leer archivos clave (no asumir, leer línea a línea)
4. ✅ **Líneas totales** — `wc -l source/file.js` (monolito o módulo limpio)
5. ✅ **Tests existentes** — `find tests/ -name "*.test.js" -exec wc -l {} +`
6. ✅ **Calidad del código** — Patrones limpios vs deuda técnica
7. ✅ **Seguridad** — PINs plano, SQL injection, secrets hardcodeados
8. ✅ **Dependencias externas** — ¿Usa librerías? ¿Se pueden eliminar?

**Evaluar cada módulo con semáforo:**
| Señal | Significado | Acción |
|-------|-------------|--------|
| 🟢 **Listo para extraer** | Código limpio, modular, con tests | Extraer con mejoras menores |
| 🟡 **Funcional con reparos** | Código usable pero con deuda moderada | Extraer + refactorizar |
| 🔴 **REWRITE necesario** | Deuda crítica (seguridad, monolito, sin tests) | Reescribir desde cero |
| ❌ **No existe** | Ni plan ni código | Crear desde cero |

**Ejemplo de evaluación granular (caso real Adela/ESIOS):**
```
Adela_time   → 🟢 ESIOS madrid.js (215 líneas, 9 funciones, tests 62 líneas, edge cases)
Adela_http   → 🟢 ESIOS esios.client.js (236 líneas, batching+retries+backoff+jitter)
Adela_cache  → 🟢 ESIOS memory-cache.js + disk-cache.js (184 líneas, métricas TTL stats)
Adela_env    → 🟡 ESIOS env.js (35 líneas, funcional pero hardcodea ESIOS_API_TOKEN)
Adela_health → 🟡 ESIOS server.js (~20 líneas healthz/readyz, mínimo pero sirve)
Adela_auth   → 🔴 MasterFit (PINs texto plano, SQL injection potencial, sin bcrypt)
Adela_export → 🟡 ESIOS csv.repository.js (65 líneas, solo CSV, pdfkit en deps sin usar)
Adela_ai     → 🟡 ESIOS report.service.js (210 líneas, específico de ESIOS)
Adela_db     → ❌ No existe en ningún lado
Adela_i18n   → ❌ No existe en ningún lado
```

### Paso 2.6: Detectar fuentes complementarias

A veces el código está distribuido en VARIOS proyectos. Mapear:

```markdown
### Módulo: Adela_X
| Fuente | Archivo | Líneas | Calidad | 
|--------|---------|--------|---------|
| Proyecto A | src/algo.js | 150 | 🟢 |
| Proyecto B | server.js (líneas 200-250) | 50 | 🟡 |
```

Para módulos parcialmente existentes, verificar si la funcionalidad está completa o falta algo:
- `Adela_export`: ESIOS tiene CSV ✅, pero falta PDF (pdfkit está en package.json pero sin usar)
- `Adela_ai`: ESIOS tiene proxy LLM para NaN, pero solo soporta ESIOS, no genérico
- `Adela_auth`: MasterFit tiene login/PIN, pero en texto plano = inservible

### Paso 2.7: Documentar deuda técnica de los proyectos fuente

No solo evaluar módulos — documentar los problemas ESTRUCTURALES de los proyectos fuente:

| Proyecto | Problema | Severidad | Impacto en extracción |
|----------|----------|-----------|----------------------|
| MasterFit | Monolito 1022 líneas | 🔴 | No extraer nada directo |
| MasterFit | PINs texto plano | 🔴 | Reescribir auth completo |
| MasterFit | SQL injection potencial | 🔴 | No usar queries existentes |
| MasterFit | Sin tests | 🟡 | No hay contrato verificable |
| ESIOS | env.js hardcodea ESIOS_API_TOKEN | 🟢 | Fácil de generalizar |
| ESIOS | esios.client.js hardcodea ESIOS URL | 🟢 | Fácil de generalizar |

### Paso 3: Definir módulos

Para cada candidato, definir:

```markdown
### Módulo: @nous/{nombre}
- **Responsabilidad:** Qué hace (una sola cosa)
- **Funciones públicas:** API exacta (import x from '@nous/nombre')
- **Dependencias:** Ninguna (o stdlib solo)
- **Tests:** Qué cubre
- **Fuente:** De dónde viene (proyecto existente o nuevo)
- **Prioridad:** P0/P1/P2
```

**Ejemplos reales de la sesión:**
| Módulo | Responsabilidad | Prioridad | Fuente |
|--------|----------------|-----------|--------|
| `@nous/env` | Variables de entorno con validación | P0 | Crear desde cero |
| `@nous/time` | Timezone Madrid, parsing | P0 | Extraer de ESIOS |
| `@nous/http` | Fetch con reintentos, backoff, batch | P0 | Extraer de ESIOS |
| `@nous/cache` | Memory + Disk cache con métricas | P1 | Extraer de ESIOS |
| `@nous/auth` | Sesiones + PIN + JWT | P1 | Reescribir (MasterFit no sirve) |
| `@nous/health` | Health + Readiness checks | P1 | Extraer de ESIOS |
| `@nous/export` | CSV, PDF, JSON export | P2 | Extraer de MasterFit |
| `@nous/ai` | Proxy genérico LLM | P2 | Extraer de MasterFit+ESIOS |
| `@nous/db` | Abstracción DB (SQLite → PostgreSQL) | P2 | Crear desde cero |

### Paso 4: Decidir arquitectura del ecosistema

Presentar al usuario las decisiones clave:

| Decisión | Opciones | Recomendación |
|----------|----------|---------------|
| **Namespace** | `@nous/*`, `@ntizar/*`, `@mastermind/*` | `@nous/*` (NosUnus) |
| **Monorepo vs Multi-repo** | Turborepo workspace / Cada repo independiente | Monorepo primero (más fácil) |
| **TS vs JS vanilla** | TS con build / JS con JSDoc | TS first (tipos = contrato) |
| **Deploy** | npm privado / Local only | npm privado en NaN |

### Paso 5: Template de cada módulo

```
@nous/{nombre}/
├── package.json          # name: "@nous/{nombre}", version: "1.0.0"
├── README.md             # Quick start + API reference
├── src/
│   ├── index.ts          # Exports públicos
│   ├── impl.ts           # Implementación
│   └── types.ts          # Interfaces públicas
├── tests/
│   └── impl.test.ts      # Tests obligatorios
└── dist/                 # Build output (JS + .d.ts)
```

### Paso 6: Plan de implementación por fases

Después de auditar y definir todos los módulos, crear un plan de implementación PRIORIZADO por semanas/fases. Cada fase debe ser autocontenida y entregar valor tangible.

**Criterios de priorización:**
| Prioridad | Criterio | Ejemplo |
|-----------|----------|---------|
| 🔴 P0 | Dependencia de proyectos activos, código listo para extraer | env, time, http |
| 🟡 P1 | Importante pero no bloqueante, requiere refactor | cache, health, auth |
| 🟢 P2 | Mejora continua, requiere extracción+ampliación | export, ai, db |
| 🔵 P3 | Nice to have, creación desde cero | i18n |

**Formato del plan por fases:**

```markdown
## Fase 1: P0 — Base (semana 1)
Módulos: Adela_env + Adela_time + Adela_http

### Adela_env — Gestión de ENV con validación
- ✅ Validación estricta con tipos
- ✅ Defaults + required diferenciados
- ✅ Validadores custom (puerto, ruta, regex)
- ✅ Soporte `.env` automático
- 🔧 Código fuente: ESIOS env.js (35 líneas, generalizar)

### Adela_time — Utilidades de tiempo
- Extraer de ESIOS madrid.js (215 líneas, 9 funciones, tests 62 líneas)
- Añadir: isWeekend(), nextBusinessDay(), timeAgo()
- TypeScript + tests al 100%

### Adela_http — Cliente HTTP genérico
- Extraer de ESIOS esios.client.js (236 líneas)
- Hacer genérico: configurable URL, headers, auth
- Mantener: retry con backoff + jitter, timeout, batching
```

**Regla:** Cada fase son 7 días reales. NO intentar meter 4 fases en 1 semana. Una semana por fase, y si sobra tiempo, mejorar tests y docs.

## Pitfalls

### ❌ NO extraer código con deuda técnica
Si el código fuente tiene bugs críticos (SQL injection, datos en texto plano, monolito), **no extraer**. Reescribir el módulo desde cero con buenas prácticas. Extraer deuda = distribuir deuda.

### ❌ NO crear módulos por crear
Solo crear módulos que usen **2+ proyectos**. Si solo un proyecto lo necesita, es código específico, no módulo base.

### ❌ NO hacer todo de golpe
Empezar con P0 (env, time, http). Validar que el patrón funciona antes de escalar.

### ✅ SÍ mantener zero dependencies
Cada módulo debe funcionar standalone. Si `@nous/http` necesita `@nous/cache`, algo va mal.

### ✅ SÍ testear cada módulo
Sin tests, no hay contrato verificable. Cada módulo debe tener tests unitarios que cubran la API pública.

### ✅ SÍ documentar con ejemplos
Cada módulo debe tener un "quick start" en el README con 3-5 líneas de código que demuestren su uso.

## Referencias

- **`references/modular-ecosystem-plan.md`** — Plan completo de ecosistema `@nous/*` con 10 módulos propuestos, análisis de GitHub stars, auditoría de proyectos, y decisiones pendientes.
- **`references/nodejs-multiuser-audit-patterns.md`** (de `system-audit`) — Patrones de bugs en apps Node.js multi-usuario, útil para validar módulos antes de extraerlos.

## Overlap con otros skills

- **`refactor-nodejs-monolith`** — cubre refactorizar un monolito en módulos DENTRO de un proyecto. Este skill cubre crear módulos que COMPARTIR entre proyectos. Complementarios.
- **`geospatial-asset-platform`** — cubre la plataforma TerrAn con sus módulos de dominio (residuos, policía, sanidad). Este skill cubre los módulos BASE que TerrAn usaría (env, time, http, auth). Complementarios.
- **`aurora-nightly`** — cubre mejora continua nocturna del design system visual. Este skill es el equivalente para el backend. Complementarios.
