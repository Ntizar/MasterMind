# Audit de Skills — Real-World Reference (2026-07-01)

## Hallazgos reales de la auditoría mensual

### Métricas del ecosistema
- **238 skills** en **44 categorías**
- **2.54 MB** total en SKILL.md files
- **189/238** con versión (79%), **49/238** sin versión (21%)
- **0/238** con tags manuales (100% auto-tags)
- **17 skills >30KB**, **6 >50KB**, **1 >100KB**

### Problemas detectados y resueltos

| Problema | Impacto | Acción |
|----------|---------|--------|
| Index.json stale (143 vs 238) | 95 skills sin indexar | ✅ Regenerado manualmente con Python |
| Quarantine stale `fastmcp` | 21 días sin resolver | ✅ Eliminado |
| Index-cache huérfano | 38 MB sin referencias | ✅ Eliminado |
| Curator backups acumulados | 14 MB, 5 backups | ✅ Mantener solo 2 recientes |
| 1 duplicado nombre `static-digest-pipeline` | frontend-dashboard-patterns + devops | ⏳ Pendiente fusión |
| 49 skills sin versión | Principalmente stem/ | ⏳ Pendiente |
| 0 tags manuales | ChromaDB scoring subóptimo | ⏳ Pendiente top-20 skills |

### Scripts y paths de utilidad

```bash
# Contar SKILL.md files
find agent/skills/ -name 'SKILL.md' -not -path '*/.hub/quarantine/*' | wc -l

# Detectar duplicados de nombre
python3 -c "
import glob, os
by_name = {}
for f in glob.glob('agent/skills/**/SKILL.md', recursive=True):
    if '.hub/quarantine' not in f:
        name = os.path.basename(os.path.dirname(f))
        by_name.setdefault(name, []).append(f)
for name, paths in by_name.items():
    if len(paths) > 1:
        print(f'{name}: {len(paths)} instances')
        for p in paths: print(f'  → {p}')
"

# Detectar project-readmes (>5 absolute paths)
python3 -c "
import glob, os, re
for f in glob.glob('agent/skills/**/SKILL.md', recursive=True):
    if '.hub/quarantine' not in f:
        content = open(f).read()
        abs_paths = re.findall(r'(repo raíz/[^ \"\x27\s]+|/root/workspace/[^ \"\x27\s]+)', content)
        if len(abs_paths) > 5:
            print(f'{os.path.basename(os.path.dirname(f))}: {len(abs_paths)} abs paths')
"

# Verificar si index.json está stale
python3 -c "
import json
index = json.load(open('agent/skills/index.json'))
actual = len([f for f in __import__('glob').glob('agent/skills/**/SKILL.md', recursive=True) if '.hub/quarantine' not in f])
print(f'Index: {index.get(\"total_skills\", \"?\")} | Real: {actual} | Delta: {actual - index.get(\"total_skills\", 0)}')
"

# Limpiar quarantine >7 días
find agent/skills/.hub/quarantine/ -maxdepth 1 -type d -mtime +7 -exec rm -rf {} +

# Limpiar curator backups (mantener 2 más recientes)
ls -1t agent/skills/.curator_backups/ | tail -n +3 | xargs -I{} rm -rf agent/skills/.curator_backups/{}
```

### Tamaño de componentes
- `.hub/`: 38 MB → 24 KB (tras eliminar index-cache)
- `.curator_backups/`: 14 MB → 6.5 MB
- `agent/skills/`: 20 MB total
