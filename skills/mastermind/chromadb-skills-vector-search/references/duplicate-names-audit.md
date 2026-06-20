# Audit de nombres duplicados en skills (2026-06-14)

## Problema

230 SKILL.md files pero solo 228 nombres únicos en frontmatter `name:`. Dos pares de skills comparten el mismo nombre:

### `dieta` (2 archivos)
- `/hermes-home/skills/health/dieta/SKILL.md` — v4.0.2, sistema completo de base de datos + dashboard
- `/hermes-home/skills/health/dieta-tracking/SKILL.md` — v1.0.0, seguimiento nutricional básico

### `static-digest-pipeline` (2 archivos)
- `/hermes-home/skills/devops/static-digest-pipeline/SKILL.md`
- `/hermes-home/skills/frontend-dashboard-patterns/static-digest-pipeline/SKILL.md`

## Solución

El indexador usa **path relativo** como ID de ChromaDB:
- `health--dieta`
- `health--dieta-tracking`
- `devops--static-digest-pipeline`
- `frontend-dashboard-patterns--static-digest-pipeline`

## Script de detección

```bash
grep -rh "^name:" /hermes-home/skills/ --include="SKILL.md" | sort | uniq -d
```

## Impacto

- ChromaDB: 229 docs (todos indexados correctamente)
- `consultar-skills.py`: devuelve `name` en metadata (puede haber duplicados), pero los IDs son únicos
- `skill_view(name)`: funciona porque busca por nombre frontmatter, no por ID ChromaDB
