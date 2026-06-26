# Referencia: Scripts de Auditoría de Skills

## scripts/audit-skills.py

Script Python principal para auditoría del ecosistema de skills.

### Uso

```bash
python3 scripts/audit-skills.py [skills_dir]
# Default: /hermes-home/skills
```

### Qué detecta

- Duplicados de nombre
- Skills sin frontmatter, versión, descripción o tags
- Project-readmes (rutas hardcodeadas + tree structures)
- CLI wrappers (>2 curl commands + <5KB)
- Skills >50KB
- Skills con tablas markdown
- Métricas por categoría

### Health Score

Calcula 8 checks → 0-5 estrellas.

### Salida

Reporte estructurado con secciones: CRITICAL ISSUES, WARNINGS, SIZE BY CATEGORY, LARGEST SKILLS, HEALTH SCORE.
