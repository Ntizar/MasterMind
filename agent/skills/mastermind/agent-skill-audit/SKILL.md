---
name: agent-skill-audit
description: "Usa al auditar que los skills describan bien su repo fuente."
version: "1.0.0"
author: "Mastermind"
license: "MIT"
tags: [skills, auditoria, verificacion, fuente-verdad, github, registry]
related_skills: [stars-explorer, mastermind-system-ops, skillopt, skillspector]
---

# Auditoría de skills vs su repo fuente

Clase de tarea: **verificar que un SKILL.md no mienta sobre el proyecto que documenta
/comandos inventados, CDN falsos, función mal descrita, categoría errónea.** Nace del
pipeline stars-explorer (que a veces creó skills en lote sin leer el README), pero
aplica a CUALQUIER skill cuyo contenido deba corresponder a una fuente real (repo, API,
herramienta). Es el paso que David llama "ser agresivo": no solo crear, re-verificar lo
creado, periódicamente.

## When to Use

- Al re-auditar skills que el pipeline generó desde repos star-eados.
- Cuando un skill describe una herramienta y dudas de que los comandos/CLI/CDN sean reales.
- Antes de confiar en un skill "herencia" (creado en batch sin leer su README).
- Cuando David pide repasar la base de skills por calidad/veracidad.

## Reglas que no se pueden saltar

1. **`category: "upgrade"` en el registry ≠ contenido arreglado.** Marcar "upgrade"
   significa que el dedup decidió mejorar, no que el SKILL.md esté reescrito a v2.
   Verificar SIEMPRE la `version` del frontmatter y las afirmaciones concretas.
2. **No editar por editar.** Los root-level no son todos v1 (mastermind, github-workflow,
   pdf-processing son legítimos sin categoría). El marcador es función-descrita vs real,
   no la ubicación.
3. **Los children verifican, el orquestador parchea.** Subagentes investigan y devuelven
   JSON; el padre aplica `skill_manage(patch)` y lo verifica. Nunca asumir el self-report
   de un child como verdad.
4. **No `git clone`** para auditar un repo pequeño: basta curl de 2-3 ficheros clave del
   tree (lección 2026-09-04). Un child con repo sin README debe marcar "sin datos", no inventar.

## Método (receta completa en `references/audit-recipe.md`)

### 1. Mapear repo → skill desde el registry
Leer `data/stars-registry.json`, subdict `processed`, filtrar `skill_created: true`,
resolver `skill_name`/basename contra `agent/skills/**` hasta el `SKILL.md`. Volcar a
`C:/Users/d_ant/AppData/Local/Temp/audit_map.json`.

### 2. Identificar candidatos v1
Root-level (sin categoría) = candidatos del maratón. Listar con
`ls -d agent/skills/*/ | while read d; do [ -f "$d/SKILL.md" ] && echo "$d"; done`.

### 3. Verificar contra la fuente real
`gh api repos/<repo>` / `curl -s https://api.github.com/repos/<repo>` y `/readme`.
Comparar función, comandos, CDN, endpoints, stars, categoría librería-vs-app.

### 4. Barrido en paralelo (delegación)
Repartir ~4-6 skills por child (leaf), 3 en paralelo. Cada child devuelve
`{"auditoria":[{"repo","veredicto":"OK|NEEDS_PATCH","skill_version","discrepancias",...,"stars_reales","lenguaje_real"}]}`.
El padre parchea los `NEEDS_PATCH`.

## Pitfalls de entorno (Windows)

- **`python -c` con backslashes/rutas Windows en git-bash** → `SyntaxError: unterminated
  string literal`. Y `python.exe` nativo NO lee `/tmp` (MSYS) → `FileNotFoundError`.
  Usar `write_file` en `C:/Users/d_ant/AppData/Local/Temp/<>.py` y ejecutarlo con el
  Python del sistema `C:/Users/d_ant/AppData/Local/Programs/Python/Python312/python.exe`.
- **Post-patch siempre**: `python scripts/sincronizar-skills.py` (inst→repo) +
  `python scripts/indexar-skills.py` (Python del sistema) + commit/push.

## Estado verificado (2026-09-05)

Barrido de 12 skills (TTS/OCR/PDF/routing/scraping) en 3 subagentes. `minimaps-js` y
`gtfs-to-chart` (los señalados como fabricados) ya estaban a v2 correcto → la incidencia
original del maratón quedó cerrada. Ver antagonista del pipeline en el skill
`stars-explorer` (user-owned) y sus pitfalls de v1.
