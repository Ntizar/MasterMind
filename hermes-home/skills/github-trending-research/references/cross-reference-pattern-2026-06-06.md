# Cross-reference trending con skills existentes — Patrón correcto

**Creado:** 2026-06-06

## El problema

INDEX.md usa tablas markdown con niveles profundos (`||||| [repo](path)`) y URLs embebidas. `grep` simple produce 0 coincidencias (falsas negativas).

## Solución correcta

Un solo script Python que lee el contenido real de cada SKILL.md:

```python
import os, re

trending_repos = ['OWNER/REPO1', 'OWNER/REPO2', ...]
skills_dir = '/root/workspace/Mastermind/skills'
existing = {}
new = []

for repo in trending_repos:
    found = False
    for root, dirs, files in os.walk(skills_dir):
        for fname in files:
            if fname == 'SKILL.md':
                with open(os.path.join(root, fname), 'r') as f:
                    content = f.read()
                if repo.lower() in content.lower():
                    found = True
                    existing[repo] = os.path.join(root, fname)
                    break
        if found:
            break
    if not found:
        new.append(repo)
```

## Por qué funciona

- Lee el contenido real de cada SKILL.md, no hace regex sobre tablas
- Encuentra skills aunque el repo aparezca como `OWNER/REPO` sin prefijo
- Un solo paso, no tres fases de grep
- Rápido: lee ~50-100 archivos como máximo

## No usar

- `grep -r "OWNER/REPO" skills/` — falla con tablas anidadas
- `grep "github.com/OWNER/REPO"` — falla con paths relativos
- Parsear INDEX.md con regex — formato inconsistente

## Referencias

- Sesión 2026-06-03: primer intento con grep (fallido)
- Sesión 2026-06-05: refinamiento del patrón
- Sesión 2026-06-06: validación definitiva con script Python
