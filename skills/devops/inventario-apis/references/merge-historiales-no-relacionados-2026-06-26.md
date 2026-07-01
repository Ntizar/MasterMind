# Sesión de merge 2026-06-26: Unir historiales no relacionados

## Contexto
El cron de inventario-apis ejecutó `procesar-apis.py 5` desde `/tmp/inventario-apis/` que tenía un historial git independiente del remote GitHub (commits 0055-0075, total 75 APIs). El remote tenía 3688 APIs de ejecuciones previas con historial separado.

## Síntomas
- `git pull --rebase origin master` → conflictos masivos (118 archivos)
- `git merge origin/master` → `fatal: refusing to merge unrelated histories`
- El script local no sabía de las 3600+ APIs del remote

## Resolución completa

```bash
# 1. Abortar cualquier rebase en curso
git rebase --abort

# 2. Fetch del remote
git fetch origin

# 3. Merge con historiales no relacionados
git merge origin/master --no-edit --allow-unrelated-histories
# → 118 conflictos add/add en APIs duplicadas

# 4. Resolver conflictos: aceptar versión remota (más completa)
git diff --name-only --diff-filter=U | xargs -I {} git checkout --theirs {}

# 5. Commit del merge
git add -A && git commit --no-edit

# 6. Push con upstream tracking
git push --set-upstream origin master
```

## Resultado
- Merge exitoso: 3688 APIs del remote + 75 locales = 3693 APIs
- Push exitoso a origin/master
- Configurado upstream tracking para futuros pushes

## Lecciones
- `--allow-unrelated-histories` es necesario cuando dos repos se inicializan por separado
- Siempre usar `--theirs` (versión remota) porque tiene más datos
- Tras el merge, configurar upstream con `--set-upstream` para evitar errores futuros
- No usar `pull --rebase` en este escenario — genera conflictos innecesarios