# ChromaDB: Fix de duplicados en indexación (2026-06-14)

## Problema

El indexador `indexar-skills.py` usaba el nombre del frontmatter (`name:`) como ID de ChromaDB. Cuando dos directorios de skills tenían el mismo `name:` en su frontmatter, el segundo daba `DuplicateIDError` al hacer `collection.add()`.

### Duplicados encontrados

1. **`dieta`** → `health/dieta/` y `health/dieta-tracking/`
2. **`static-digest-pipeline`** → `devops/` y `frontend-dashboard-patterns/`

Total: 230 SKILL.md files → 228 nombres únicos → 2 pares duplicados.

## Solución

Cambiar el ID de ChromaDB de usar el nombre frontmatter a usar el **path relativo** del directorio del skill:

```python
rel_path = str(Path(skill_dir).relative_to(SKILLS_DIR))
unique_id = rel_path.replace("/", "--")
# Ejemplo: "health--dieta", "health--dieta-tracking"
```

## Archivos modificados

- `/hermes-home/scripts/indexar-skills.py` — líneas 158-169: usar path relativo como ID

## Resultado

- 229 skills indexados correctamente
- Ambos duplicados coexisten con IDs únicos
- Consulta semántica funciona correctamente
