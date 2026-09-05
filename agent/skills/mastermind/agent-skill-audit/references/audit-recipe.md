# Receta de auditoría skills-vs-fuente

Receta paso a paso, reproducida 2026-09-05. Es el "ser agresivo" que David pide:
no solo crear skills, re-verificar los ya creados contra su repo real.

## Paso 1 — Mapear repo → skill desde el registry

`data/stars-registry.json` guarda en `processed` los repos; `skill_created: true` marca
que se generó skill. Resolver cada repo a su skill real con el Python del sistema
(file no `python -c` por el escaping de backslashes en git-bash):

```python
import json, os, re
os.chdir(r"C:/Users/d_ant/Projects/MasterMind")
r = json.load(open('data/stars-registry.json'))
proc = r['processed']
creados = {k: v for k, v in proc.items() if v.get('skill_created')}

def resolve(sname):
    base = re.sub(r'[^a-z0-9-]', '-', sname.lower().rstrip('-'))
    for root, dirs, files in os.walk('agent/skills'):
        if 'SKILL.md' in files:
            rel = os.path.relpath(root, 'agent/skills').replace(os.sep, '/')
            if os.path.basename(root) == base or sname.lower() in rel.lower() or base in rel.lower():
                return rel
    return None

out = [{'repo': k, 'cat': v.get('category'), 'skill': (v.get('skill_name') or k.split('/')[-1]),
        'rel': resolve(v.get('skill_name') or k.split('/')[-1]), 'stars': v.get('stars')}
       for k, v in creados.items()]
open(r"C:/Users/d_ant/AppData/Local/Temp/audit_map.json", 'w').write(json.dumps(out, ensure_ascii=False, indent=2))
```

Ejecutar: `C:/Users/d_ant/AppData/Local/Programs/Python/Python312/python.exe C:/Users/d_ant/AppData/Local/Temp/mapear.py`.
Resultado esperado (2026-09-05): 157 con skill_created → 152 resueltos a skill, 5 sin resolver a mano.

## Paso 2 — Candidatos v1: root-level (sin categoría)

```bash
ls -d agent/skills/*/ | while read d; do [ -f "$d/SKILL.md" ] && echo "$d"; done
```

No todos los root-level son v1 (`mastermind`, `github-workflow`, `pdf-processing`,
`human-loop-control` son legítimos). El marcador real es función-descrita vs real.

## Paso 3 — Verificar contra la fuente real

```bash
TOKEN=$(gh auth token 2>/dev/null)
curl -s "https://api.github.com/repos/<owner>/<repo>" -H "Authorization: token $TOKEN" | \
  python -c "import sys,json;d=json.load(sys.stdin);print(d.get('description'),'|',d.get('language'),'|',d.get('stargazers_count'))"
curl -s "https://api.github.com/repos/<owner>/<repo>/readme" -H "Authorization: token $TOKEN" | \
  python -c "import sys,json,base64;d=json.load(sys.stdin);print(base64.b64decode(d['content']).decode('utf-8','ignore')[:800])"
```

Comparar: función, comandos/CLI, CDN, endpoints, stars, categoría librería-vs-app-web.
No `git clone` (basta curl de 2-3 ficheros del tree, lección 2026-09-04).

## Paso 4 — Barrido en paralelo (delegación)

Repartir ~4-6 skills por child leaf, 3 en paralelo. Contexto por child:
- Ruta del skill: `C:/Users/d_ant/Projects/MasterMind/agent/skills/<...>/SKILL.md`
- Instrucción: leer skill, contrastar afirmaciones concretas contra el repo real vía
  `gh api repos/<repo>` / `curl` + `/readme` (decodificar base64). NO editar. NO `git clone`.
- Output estricto:
  `{"auditoria":[{"repo","veredicto":"OK|NEEDS_PATCH","skill_version","discrepancias":[..],"fix_sugerido","stars_reales","lenguaje_real"}]}`
- Si un repo no tiene README accesible → marcar "sin datos", no inventar.

El padre aplica `skill_manage(patch)` a los `NEEDS_PATCH` y verifica el resultado; los
self-reports de los children no son verdad hasta verificarla.

## Paso 5 — Post-patch

```bash
python scripts/sincronizar-skills.py          # instalación→repo (la instalación es fuente viva)
C:/Users/d_ant/AppData/Local/Programs/Python/Python312/python.exe scripts/indexar-skills.py
git add -A && git commit -m "audit: skills v1 corregidos" && git pull --rebase origin master && git push
```

## REGLA CLAVE

`category: "upgrade"` en el registry **no garantiza** contenido a v2. Verificado
2026-09-05: `minimaps-js` y `gtfs-to-chart` están marcados `upgrade` y cumplen con
`version: 2.0.0` + contenido correcto. Siempre leer la `version` y las afirmaciones
concretas antes de dar por bueno.
