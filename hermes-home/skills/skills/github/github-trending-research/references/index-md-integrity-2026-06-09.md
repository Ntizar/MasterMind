# INDEX.md Integrity Issues — 2026-06-09

## Problema detectado

El INDEX.md puede contener referencias a skills que **no existen como skills cargables** en el sistema.

### Ejemplo: `ecc-agent-harness`

- **INDEX.md línea 80:** `|||| [ecc-agent-harness](ia/ecc-agent-harness/SKILL.md)`
- **Skill cargable:** NO existe (`skill_view(name='ecc-agent-harness')` falla)
- **Real:** El repo ECC se documentó con nombre `everything-claude-code` en `ia/everything-claude-code/SKILL.md`

### Ejemplo: `revfactory-harness`

- **INDEX.md línea 109:** `|||| [revfactory-harness](multi-agent/revfactory-harness/SKILL.md)`
- **Skill cargable:** NO existe
- **Real:** El repo se documentó como `harness` en `multi-agent/harness/SKILL.md`

## Causa

Los nombres en INDEX.md no siempre coinciden con los nombres de skill reales. Esto pasa porque:
1. El nombre del skill se decide al crearlo (a veces se usa el nombre del repo, a veces no)
2. INDEX.md se actualiza manualmente y puede quedar desfasado
3. Los nombres de skill deben ser únicos en el sistema de skills cargable

## Solución

Al crear un skill nuevo:
1. Verificar que el nombre del skill sea consistente con INDEX.md
2. Usar `skill_view(name='...')` para verificar que el skill es cargable
3. Cuando se cree un skill nuevo, actualizar INDEX.md con el nombre correcto

## Patrón de verificación

```python
import os

# Verificar que un skill referenced en INDEX.md existe
def verify_skill_exists(skill_path):
    full_path = f"/root/workspace/Mastermind/skills/{skill_path}"
    return os.path.exists(full_path)

# Ejemplo: verificar ecc-agent-harness
print(verify_skill_exists("ia/ecc-agent-harness/SKILL.md"))  # False
print(verify_skill_exists("ia/everything-claude-code/SKILL.md"))  # True
```
