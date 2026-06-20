# Cross-Reference Fix — 2026-06-05

## Problema

El enfoque de 3 fases (grep INDEX.md → grep SKILL.md → Python dedup) produce **0 coincidencias** cuando hay skills existentes.

**Causa:** INDEX.md usa tablas markdown con niveles profundos:
```
||||||| [headroom](ia/headroom/SKILL.md) | 🆕 **Nuevo** — ...
||||||| [compound-engineering-plugin](ia/compound-engineering-plugin.md) | 🆕 **Nuevo** — ...
```

Los patterns `github.com/OWNER/REPO` y `OWNER/REPO` no coinciden porque:
1. Las rutas son relativas (`ia/headroom/SKILL.md`) no URLs completas
2. Los niveles de tabla (`|||||||`) rompen los regex simples
3. Algunos paths terminan en `.md` no en `/SKILL.md`

## Solución

Un solo script Python que lee el contenido de cada SKILL.md y busca el repo name (case-insensitive):

```python
import os

trending_repos = ['affaan-m/ECC', 'chopratejas/headroom', ...]
skills_dir = '/root/workspace/Mastermind/skills'

for repo in trending_repos:
    for root, dirs, files in os.walk(skills_dir):
        for fname in files:
            if fname == 'SKILL.md':
                with open(os.path.join(root, fname), 'r') as f:
                    if repo.lower() in f.read().lower():
                        # Found it
```

**Resultado en sesión 2026-06-05:**
- 15 de 20 trending repos ya tenían skill (encontrados con el nuevo enfoque)
- 5 eran realmente nuevos
- El enfoque grep anterior habría reportado 0 existentes (100% falso negativo)
