---
name: system-audit
version: "1.0.0"
description: "Procedimiento sistemático para auditar repositorios de sistemas de software — analizar arquitectura, identificar fortalezas, detectar problemas y proponer mejoras con criterios objetivos."
tags: [audit, architecture, code-review, quality-assessment, multi-agent]
---

# System Audit — Auditoría Sistemática de Repositorios

## Resumen

Procedimiento para auditar un repositorio o sistema de software completo: explorar la estructura, leer archivos clave, identificar fortalezas y debilidades, y proponer mejoras priorizadas.

## Cuándo usar

- Usuario pide "auditoría", "review", "qué te parece", "qué mejorarías" de un repositorio o sistema
- Evaluación de calidad antes de integrar un sistema nuevo
- Revisión de un proyecto propio para detectar deuda técnica
- Análisis de un framework o patrón encontrado en otro repo

## Flujo de Auditoría (5 pasos)

### Paso 1: Exploración de estructura

```bash
# Árbol de archivos
find . -maxdepth 2 -type f -o -type d | sort
# Conteo de archivos
find . -name "*.md" | wc -l
# Log reciente
git log --oneline -20
# Remote y branch
git remote -v
git branch -a
```

**Objetivo:** Entender la escala del proyecto, su historia reciente, y su superficie de código.

### Paso 2: Lectura de archivos clave (prioridad)

Leer SIEMPRE estos archivos en orden:

1. **README** → Qué es el proyecto, cómo funciona, badges, estructura
2. **Archivo de entrada principal** (`AGENTS.md`, `README.md`, `index.html`, `main.py`, etc.)
3. **Configuración del sistema** (`config.yaml`, `_system-config.md`, `.env.example`)
4. **Documentación de arquitectura** (`ARCHITECTURE.md`, `docs/`)
5. **Workflow/CI** (`.github/workflows/`)
6. **Índices de conocimiento** (skills index, learnings index, clusters)
7. **Agentes/roles principales** (los que definen el comportamiento central)
8. **Plantillas** (templates que otros siguen)
9. **Estado actual** (session state, TODOs pendientes, tareas sin cerrar)

### Paso 3: Análisis de fortalezas

Evaluar cada dimensión con criterio (MÍNIMO 8 dimensiones):

| Dimensión | Qué buscar |
|-----------|-----------|
| **Arquitectura** | Separación de responsabilidades, patrones de diseño, capas |
| **Memoria/conocimiento** | Cómo se almacena, filtra, recupera y deprecia el conocimiento |
| **Orquestación** | Cómo se coordinan los componentes, flujos adaptativos |
| **Calidad** | Revisión, criticado, validación, tests |
| **Documentación** | README, arquitectura, templates, contribución |
| **Portabilidad** | Rutas absolutas, dependencias de SO, configuración portable |
| **UX/Comunicación** | Checkpoints, formatos de output, protocolos de delegación |
| **Auto-mejora** | Aprendizaje acumulado, reaprendizaje, métricas |
| **Tokens y costes** | Tracking de tokens, costes por sesión, optimización de contexto |
| **Seguridad** | Secrets en repo, .gitignore correcto, credenciales hardcodeadas |
| **Deploy/CI/CD** | Workflows funcionales, branches limpios, CI configurado |
| **Integración móvil** | Telegram, accesibilidad desde móvil, canales de comunicación |

**Regla:** Nunca evaluar menos de 8 dimensiones. Las dimensiones de tokens/costes, seguridad y deploy son OBLIGATORIAS en auditorías de sistemas multi-agente.

### Paso 4: Detección de problemas (categorías)

Clasificar cada problema encontrado en una de estas categorías:

| Categoría | Severidad | Ejemplos |
|-----------|-----------|----------|
| **🔴 Crítico** | Rompe el sistema o la portabilidad | Rutas absolutas hardcodeadas, estado corrupto, datos perdidos |
| **🟡 Importante** | Limita la utilidad o escalabilidad | Sin métricas, mecanismo de auto-mejora sin usar, criterios subjetivos |
| **🟢 Menor** | Mejora la calidad pero no bloquea | Branch naming, falta de CHANGELOG, CSS duplicado |

### Paso 5: Propuestas de mejora priorizadas

Para cada problema, proponer una mejora concreta:

- **Prioridad Alta** → Afecta portabilidad, funcionalidad o escalabilidad
- **Prioridad Media** → Mejora la utilidad, mantenibilidad o coherencia
- **Prioridad Baja** → Buenas prácticas, consistencia, documentación

## Patrones comunes que debes detectar

### Patrones de arquitectura bien diseñados
- Dos capas (documental + ejecutable) sin duplicación
- Índice inteligente con carga bajo demanda
- Flujo adaptativo basado en complejidad
- Agente de mantenimiento autónomo (bibliotecario/archiver)
- Protocolos de comunicación estructurados

### Patrones de arquitectura problemáticos
- Rutas absolutas hardcodeadas en config
- Mecanismos de auto-mejora sin datos que los alimenten
- Criterios subjetivos donde deberían ser objetivos
- Estado de sesión sin limpieza (tareas "pendientes" que nunca se archivan)
- CSS/estilos duplicados entre componentes
- Verificador de instalación que solo funciona en un SO

### Patrones de memoria/conocimiento
- Índice con señales de relevancia + decay (bueno)
- Learnings individuales cargados siempre (malo — gasta tokens)
- Skills sin "ciclo de reaprendizaje" cuando el mecanismo existe
- Clusters dinámicos vs. estáticos

### Patrones de criticado — activación objetiva
- **Señal de alerta:** El Critic se activa por "dudas" subjetivas del orchestrator
- **Patrón correcto:** 6 criterios objetivos: complejidad ≥4, ≥3 reintentos, ≥3 archivos, impacto alto, reviewer emite WARNINGs, solicitud humana explícita
- **Señal de éxito:** El orchestrator evalúa los criterios automáticamente sin preguntar

## Formato de output

Presentar la auditoría en este formato:

```
# 🔍 Auditoría Completa — [Nombre del Sistema]

## 📊 Panorama General
| Dimensión | Estado |
|-----------|--------|
| ... | ... |

## ✅ Lo que está MUY BIEN
### 1. [Nombre del aspecto positivo]
[Explicación de POR QUÉ es bueno, no solo QUÉ es bueno]

## ⚠️ Problemas detectados
### 🔴 Críticos
[Problema] → [Por qué es crítico]

### 🟡 Importantes
[Problema] → [Por qué es importante]

### 🟢 Menores
[Problema] → [Por qué es menor]

## 💡 Mejoras que propondría
### Prioridad Alta
[A] [Mejora] → [Impacto esperado]

### Prioridad Media
[B] [Mejora] → [Impacto esperado]

### Prioridad Baja
[C] [Mejora] → [Impacto esperado]

## 📈 Veredicto global
**Puntuación: X/10**

[Resumen de 2-3 líneas con tu opinión honesta sobre el sistema]
```

## Post-Audit Execution Pipeline

Cuando el usuario autoriza ejecutar las mejoras propuestas en la auditoría:

### Paso 1: Priorizar por severidad

| Prioridad | Categoría | Acción |
|-----------|-----------|--------|
| **P0** | 🔴 Crítico | Ejecutar inmediatamente (rompe funcionalidad) |
| **P1** | 🟡 Importante | Ejecutar en orden de impacto |
| **P2** | 🟢 Menor | Ejecutar al final o batch |

### Paso 2: Plan de cambios

Antes de ejecutar, presentar plan concreto:
```python
# Para cada problema P0:
- Archivo: path/al/archivo.xyz
- Cambio: descripción exacta del cambio
- Líneas: ~20 afectadas
- Riesgo: bajo/medio/alto

# Para P1-P2, agrupar por dominio (docs, infra, código)
```

**Regla:** NO ejecutar sin presentar plan y obtener ✅ del usuario en cambios >3 archivos.

### Paso 3: Ejecución

- **P0 individuales** → directo (terminator, patch)
- **P0 paralelos independientes** → `delegate_task` en paralelo
- **P1-P2 relacionados** → agrupar en un `delegate_task` con todas las instrucciones
- **Documentación** → Mastermind directo (no requiere delegación)
- **CI/Deploy** → revisar primero, luego ejecutar

### Paso 4: Verificación

Por cada grupo de cambios ejecutado:
1. `git diff --stat` para confirmar archivos tocados
2. Esanear referencias residuales con `search_files`
3. `git commit` con mensaje en castellano y descriptivo
4. `git push`

### Paso 5: Medir delta

Al final de la ejecución:
```diff
- Pre-auditoría: 5.6/10
+ Post-ejecución: ~7.5/10
+ Delta: +1.9 puntos
```

Incluir el delta en el resumen final para que el usuario vea el progreso tangible.

### Alternativa: Pipeline de Crons Secuenciales

Cuando el usuario no puede estar presente para supervisar la ejecución en vivo (o las mejoras son muchas y deben ejecutarse una por una):

1. **Crear crons `once` escalonados** (15-20 min de separación), cada uno autocontenido
2. **Cada cron hace UNA mejora concreta**: lee archivos → ejecuta cambio → verifica → commit → resumen
3. **Todos con `deliver: origin`** para que el usuario vea el progreso en tiempo real
4. **Último cron = REVISIÓN FINAL**: verifica checklist completo, y si algo falla → crea cron de reparación
5. **Independientes**: si uno falla, el siguiente igual funciona (no hay dependencias entre ellos)
6. **Idempotentes**: re-ejecutar uno no rompe nada

**Formato del prompt de cada cron:**
```
Eres Mastermind. TAREA: [descripción concreta]
PASOS:
1. [leer/verificar]
2. [ejecutar cambio]
3. [verificar cambio]
4. [commit + push]
RESUMEN: [qué cambió antes→después]
```

**Patrón probado:** 14 crons secuenciales para ejecutar mejoras de auditoría, divididos en dos fases:
- **Fase 1 (8 crons):** Infraestructura y limpieza — README real, Mastermind disclaimer, ChromaDB auto-start, ChromaDB re-index, SOUL.md integration, skill dedup, skill priority consolidation, crons pausados eliminados
- **Fase 2 (6 crons):** Inteligencia — memoria decay (Ebbinghaus), knowledge graph, skill lifecycle, delegation flows, dashboard HTML, revisión final
- **Cada cron es autocontenido** (lee → ejecuta → verifica → commit → resumen) e **idempotente** (re-ejecutar no rompe nada)
- **El cron de revisión final** verifica checklist completo y crea un **cron de mantenimiento semanal** que re-ejecuta todo los domingos
- **Fase 2 depende de Fase 1** — los crons de inteligencia usan scripts/paths creados en Fase 1. Separar en fases evita que un fallo en infra destruya features de inteligencia

## Post-Migration Cleanup Execution

Cuando una migración de plataforma/paradigma ya se completó (v3.1→v4.0, de Obsidian→GitHub, etc.), a menudo quedan **referencias residuales** en los archivos activos. El ejecutable de limpieza sigue este flujo:

### Paso 1: Escaneo sistemático de referencias legacy

Usar `search_files` con los nombres de la plataforma antigua para encontrar TODAS las referencias en archivos activos (excluyendo `legacy/` y `.git/`):

```python
patterns = ['obsidian', 'opencode', 'ebbinghaus', 'wikilink', '[[', 'slash command']
for root, dirs, files in os.walk(base):
    # excluir .git, legacy/, learning-platform/
    for fname in files:
        if fname.endswith(('.md', '.json', '.html', '.yml', '.sh', '.bat', '.js')):
            # buscar cada patrón, reportar línea exacta
```

### Paso 2: Clasificar cada referencia

| Tipo | Acción | Ejemplo |
|------|--------|---------|
| **Contexto de migración** (CHANGELOG, tablas comparativas) | ✅ Mantener | "v3.1 usaba OpenCode + Obsidian" |
| **Instrucciones activas** (CONTRIBUTING, guías de inicio) | 🔄 Reescribir | "Abrir como vault de Obsidian" |
| **Landing page desactualizada** | 🔄 Reescribir | index.html con 11 agentes, Ebbinghaus |
| **Scripts de verificación obsoletos** | 🔄 Actualizar o 🗑️ eliminar | verify-system.bat que chequea .opencode/ |
| **Documentación en otro idioma desactualizada** | 🔄 Simplificar o 🗑️ eliminar | README_EN.md que v3.1 |
| **READMEs y docs que comparan versiones** | ✅ Mantener | Las comparativas dan contexto |

### Paso 3: Ejecutar cambios por archivo

Para cada archivo que necesita cambios:
- **Landing page**: Reescribir entera (cambia el mensaje, el branding, los KPIs)
- **CONTRIBUTING**: Reescribir entero (las instrucciones de instalación cambian completamente)
- **CHANGELOG**: Traducir/actualizar manteniendo el historial
- **Scripts de sistema**: Actualizar estructura de verificación al nuevo layout
- **Workflows CI**: Actualizar excludes de paths que ya no existen

### Paso 4: Verificación final

Re-escanear para confirmar que no quedan referencias activas:
```bash
grep -rl "obsidian\|opencode\|ebbinghaus" --include="*.md" --include="*.html" . | grep -v legacy/ | grep -v .git/
```

Luego: `git add -A && git commit` con mensaje descriptivo + push.

Ver `references/post-migration-cleanup.md` para el caso real de limpieza del Mastermind v3.1→v4.0.

## Adjunto: Auditoría de apps Node.js multi-usuario (Express + SQLite)

Cuando el proyecto auditado es una **aplicación web Node.js con Express, SQLite (sql.js) y autenticación multiusuario**, añadir estas dimensiones específicas al flujo de 5 pasos:

### Dimensiones adicionales obligatorias

| Dimensión | Qué buscar | Patrón problema | Referencia |
|-----------|-----------|-----------------|------------|
| **Helpers SQL** | ¿`sql_run`, `sql_all`, `sql_get` existen? ¿Se usan correctamente? | `sql_run()` para SELECT → datos perdidos silenciosamente | Patrón 1 |
| **Aislamiento multi-tenant** | ¿Los datos de cada usuario están aislados por `usuario_id`? | `getMeta('nombre')` global en vez de `usuarios.nombre` | Patrón 2 |
| **Auth** | Token en header vs cookie. ¿Limpieza de sesiones expiradas? | Token en URL (logs), sin cleanup periódico | Patrón 3 |
| **Onboarding** | ¿Formulario fijo o conversacional? ¿Se adapta al usuario? | Pasos fijos sin IA, sin personalidad de coach | Patrón 4 |
| **Persistencia de chat** | ¿Mensajes de IA en servidor o solo localStorage? | Chat perdido al cambiar navegador/dispositivo | Patrón 5 |

### Cómo leer la referencia

El archivo `references/nodejs-multiuser-audit-patterns.md` contiene 5 patrones detallados con:
- Síntoma (cómo lo detecta un usuario)
- Causa (qué código lo produce)
- Detección automática (comandos grep/curl)
- Verificación funcional (cómo confirmar el bug)
- Lección (cómo prevenirlo en el futuro)

### Checklist rápido para auditoría Node.js multi-usuario

```bash
# 1. Verificar helpers SQL
grep -n "function sql_run\|function sql_all\|function sql_get" server.js

# 2. Buscar sql_run usado para SELECT (antipattern)
grep -n "sql_run.*SELECT" server.js

# 3. Buscar getMeta() en funciones perfilUsuario
grep -n "getMeta" server.js | grep -i "nombre\|perfil\|user"

# 4. Verificar auth: limpieza de sesiones
grep -n "DELETE FROM sesiones" server.js

# 5. Verificar si chat tiene persistencia en servidor
grep -n "chat\|mensaje\|conversacion" server.js

# 6. Verificar aislamiento multi-tenant en todas las queries
grep -n "usuario_id" server.js | head -20

# 7. Verificar onboarding
grep -n "onboarding\|onboard" server.js
```

## Audit de Skills del Ecosistema

Cuando el usuario pide auditar el ecosistema de skills (detectar duplicados, project-readmes, CLI wrappers, skills sin tags), usar el patrón `skill-audit-pattern` como subsección:

### Pasos
1. **Inventario**: contar skills, verificar frontmatter (version, description, tags)
2. **Detectar project-readmes**: skills con rutas absolutas de proyecto (>5 rutas = project-readme)
3. **Detectar CLI wrappers**: skills con >3 comandos curl y <5KB
4. **Detectar duplicados**: comparar nombres y descripciones entre agent/ y repo
5. **Detectar skills >30KB**: deberían usar refs pattern
6. **Generar informe**: resumen con hallazgos categorizados por severidad

### Criterios de limpieza
- **Eliminar**: project-readmes, CLI wrappers, duplicados
- **Fusionar**: skills que cubren lo mismo
- **Refactorizar**: skills >30KB → usar refs pattern

### Pitfalls
- Subagentes fallan silenciosamente en `terminal rm` — siempre verificar post-ejecución
- `agent/skills` ≠ `/root/workspace/Mastermind/skills` — siempre sync después
- No todos los project-readmes son malos — los que contienen patrones de diseño tienen valor educativo

## Referencias

- **`references/webapp-integration-testing.md`** — Patrón para testear APIs externas (ORS, Nominatim, GTFS) durante auditorías de web apps: validar keys, detectar datos simulados, verificar calidad de datasets cacheados.
- **`references/multi-agent-patterns.md`** — Banco de conocimiento sobre patrones de sistemas multi-agente.
- **`references/audit-cases.md`** — Casos reales de auditoría con hallazgos, métricas antes/después. Incluye caso Mastermind v3.1→v4.0.
- **`references/migration-audit.md`** — Checklist de auditoría de migración.
- **`references/post-migration-cleanup.md`** — Caso real: limpieza de Mastermind v3.1→v4.0, eliminando referencias residuales a Obsidian, OpenCode y Ebbinghaus de todos los archivos activos.
- **`references/nodejs-multiuser-audit-patterns.md`** — 5 patrones de bugs en apps Node.js multi-usuario (Express + SQLite): `sql_run` vs `sql_all`, `getMeta()` global, auth por token, onboarding conversacional, persistencia de chat.
- **`references/terran-architecture-audit.md`** — Caso TerrAn iter 116: patrón "fixed pero no aplicado al schema base". 9 issues activos en una fase con 36 fijados. Verificar que los fixes documentados en comentarios realmente modificaron el schema base, no solo que exista una sección de FIX.
- **`references/rls-gap-detection.md`** — Caso TerrAn v25: 24 issues SEC por RLS enabled sin policy. Detección sistemática con regex + set difference. Fixes: org_id en 7 tablas, 14 policies nuevas, superadmin_bypass corregido, encriptación DNI/NSS.

## Ejecución combinada Auditoría + Corrección

Cuando el usuario pide "auditoría + soluciona todo" (o similar), ejecutar el pipeline completo en una sola sesión:

1. **Auditar** (pasos 1-5 del flujo de auditoría)
2. **Presentar** el informe completo con hallazgos priorizados
3. **Crear plan de corrección** como todo list con IDs
4. **Ejecutar correcciones** en orden P0 → P1 → P2, mostrando progreso en tiempo real
5. **Verificar** con el script de verificación del sistema
6. **Commit + push** con mensaje descriptivo
7. **Medir delta** de calidad pre/post

**Regla:** NO parar entre fases. Terminar un paso, empezar el siguiente inmediatamente. Si el usuario tiene que preguntar "¿por qué has parado?", algo va mal.

### Técnica: reemplazo masivo con execute_code

Para limpieza post-auditoría que requiere reemplazar un patrón en múltiples archivos, usar `execute_code` con un bucle Python:

```python
from hermes_tools import read_file, write_file
import os

base = "/path/to/repo"
for root, dirs, files in os.walk(base):
    if '.git' in root or 'legacy/' in root:
        continue
    for fname in files:
        fpath = os.path.join(root, fname)
        try:
            content = open(fpath).read()
            if 'PATTERN' in content:
                write_file(fpath, content.replace('PATTERN', 'REPLACEMENT'))
        except (UnicodeDecodeError, PermissionError):
            pass
```

Más eficiente que `patch` individual para 5+ archivos. Usar `patch` para ediciones quirúrgicas, `execute_code` para barrido masivo.

## Pitfalls

- **No ser genérico** — Cada auditoría debe referenciar archivos específicos, líneas concretas, patrones reales del código
- **No inventar problemas** — Si algo funciona bien, decirlo. La credibilidad depende de la honestidad.
- **No solo listar — explicar POR QUÉ** — "Tienes rutas absolutas" es menos útil que "La ruta `C:\\Users\\d_ant\\` en `_system-config.md` rompe la portabilidad porque cualquier clon tendrá esa ruta hardcodeada"
- **No dar mejoras vagas** — "Añadir tests" es vago. "Un script que simule un ciclo completo con un prompt de prueba y verifique que todos los agentes emiten output en el formato esperado" es accionable
- **No ignorar el contexto del usuario** — Si es un proyecto propio, ser constructivo pero honesto. Si es un repo ajeno, ser objetivo y menos prescriptivo
- **Verificar auditorías previas contra estado actual** — Si el repo ya tiene un `audit-*.md`, leerlo pero verificar cada hallazgo. Las auditorías previas pueden tener findings ya resueltos (ej: CDN cambió de `@master` a `@latest` entre auditorías). No copiar findings sin validar.
- **Detectar directorios completos stale, no solo referencias de texto** — El Post-Migration Cleanup se centra en referencias de texto, pero a menudo hay directorios ENTEROS de código v3.1 que nunca se movieron a `legacy/`. Escanear la estructura de directorios buscando código que referencia la plataforma antigua completa (no solo menciones sueltas).
- **No parar en "bueno suficiente"** — Si la puntuación es 7/10, presentar los items P2/P3 restantes y ofrecer ejecutarlos. El usuario decide cuándo parar, no el agente. Si presentas 7/10 como "hecho", el usuario frustrado pregunta "¿por qué no luchas por más?".
- **Un tema = una fuente** — Si SOUL.md, AGENTS.md y README.md repiten los mismos niveles de ejecución, human loop o arquitectura, es deuda técnica. Cada pieza de información debe vivir en UN solo archivo con cross-references. Detectar esto como hallazgo "🟡 Importante: documentación duplicada".
- **Verify debe ser funcional, no solo existencia** — `check_file "SOUL.md"` solo verifica que existe. Añadir `check_content "SOUL.md" "Mastermind"` verifica que contiene lo esperado. Un verify de 27 checks (existencia + contenido + consistencia + JSON válido) es más valioso que uno de 11 checks de existencia.
- **`set -uo pipefail`, NO `set -euo pipefail` en scripts de test** — El flag `-e` causa que el script se cuelgue cuando `grep` no encuentra un patrón (exit code 1). Los scripts de verificación y test SIEMPRE usan `set -uo pipefail` para que los fallos se reporten sin abortar el script. Ejemplo real: un grep de secrets que no encuentra nada retorna exit 1, y con `-e` el script muere silenciosamente antes de llegar al resumen.
- **Detección de secrets: patrones específicos, no genéricos** — `grep "token\|password\|secret"` produce falsos positivos con código legítimo (`token-tracking`, `input_tokens`, `href="tokens/"`). Usar patrones de formatos reales: `sk-[a-zA-Z0-9]{20,}` (API keys), `ghp_[a-zA-Z0-9]{36,}` (GitHub tokens), `AKIA[A-Z0-9]{16,}` (AWS keys). Separar en greps individuales y sumar, no usar OR en un solo grep (causa problemas con `wc -l`).
- **Sobreingeniería: detectar y cortar** — El usuario corregirá explícitamente si el agente tiende a sobreingenierizar ("ten cuidado con la sobreingeniería que te gusta mucho"). Señales: arquitectura documentada que no se implementa, N agentes cuando M bastan, fórmulas complejas sin código, features descritas como "activas" cuando son diseños conceptuales. **Regla:** En cada auditoría, preguntar activamente "¿esto es funcional o es documentación aspiracional?" y marcar explícitamente la diferencia. Preferir simplificar sobre extender.
- **Deployment ≠ Integración** — Que un componente esté desplegado y funcional técnicamente no significa que esté integrado en el flujo de trabajo. Ejemplo clásico: ChromaDB corriendo con 190 skills indexados pero Mastermind nunca lo consulta. En auditorías, verificar SIEMPRE que cada componente tiene un trigger real que lo invoca, no solo que existe. Añadir una dimensión de auditoría: "¿Se usa de verdad?"

- **FIXED pero NO aplicado al schema base** — Cuando un documento de arquitectura tiene secciones de "FIX" documentadas (comentarios, secciones al final), verificar que el schema base (CREATE TABLEs principales) fue realmente modificado. Es muy común que las soluciones se documenten en comentarios pero el schema original se quede sin cambios. Esto produce:
  - RLS policies que referencian funciones/columnas inexistentes → RLS roto en runtime
  - CHECK constraints que deberían eliminarse pero siguen en el schema → bloquean personalización
  - Dos documentos inconsistentes (ARQUITECTURA.md tiene el fix, RENDIMIENTO-Y-NEGOCIO.md no) → si se implementa con el segundo, se crea un sistema roto
  - **Verificación obligatoria:** Para cada issue marcado como "fixed", leer la definición original de la tabla/columna y verificar que fue modificada, no solo que existe una sección de FIX en otro lugar del mismo documento.
  - Ver `references/terran-architecture-audit.md` para el caso real de auditoría TerrAn (iter 116).

- **RLS enabled ≠ RLS policy existe** — Patrón crítico detectado en TerrAn/GeoAsset (24 issues SEC): tener `ALTER TABLE x ENABLE ROW LEVEL SECURITY` NO significa que exista una `CREATE POLICY` para esa tabla. Una tabla con RLS enabled pero sin policy **deniega TODAS las operaciones** (incluyendo SELECT) porque la política por defecto es DENY. Detección sistemática:
  1. Buscar `ALTER TABLE \w+ ENABLE ROW LEVEL SECURITY` → lista de tablas con RLS activado
  2. Buscar `CREATE POLICY \w+ ON \w+` → lista de tablas con policy
  3. Diferencia = tablas rotas (RLS enabled sin policy = sistema bloqueado)
  4. También verificar que cada tabla con org_id tiene policy, aunque RLS no esté explícitamente enabled (algunas tablas nuevas pueden no tener ALTER TABLE pero sí necesitan policy)
  5. Verificar que las policies referencian columnas que realmente existen (ej: `usuarios` con policy que usa `org_id` pero la tabla no tiene columna `org_id`)
  - Ver `references/rls-gap-detection.md` para el caso real de 24 issues SEC en TerrAn v25.

- **audit-state.json como fuente de verdad de issues** — Algunos proyectos (TerrAn/GeoAsset) usan un JSON estructurado (`audit-state.json`) en vez de markdown para trackear issues de auditoría. Formato: fases → issues_found con id, title, severity, description, status (fixed/unknown), fixed_in, fixed_note. Al ejecutar fixes:
  1. Leer JSON, filtrar issues por fase y status != 'fixed'
  2. Agrupar por categoría (RLS, org_id, encryption, etc.)
  3. Ejecutar fixes en execute_code con patch/write_file directo
  4. Actualizar todos los issues a status='fixed' con fixed_note descriptivo
  5. Incrementar iteration y actualizar last_run
  6. Contar active/fixed para reporte final
  - Los fixes se hacen directo con execute_code (patch/write_file), NUNCA subagentes — los archivos son grandes (>100KB) y los subagentes timeout.
