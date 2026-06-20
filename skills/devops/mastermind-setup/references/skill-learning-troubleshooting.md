# Skill Learning Script — Troubleshooting

## Problem: State desincronizado con disco

El archivo `.skill-learning-state.json` marca skills como "learned" pero no existen en `/hermes-home/skills/`.

### Causa

El script avanza el índice y actualiza el state JSON antes de que la instalación se complete realmente. Si `hermes skills install` falla o timeouta, el state ya se actualizó pero el skill no se instaló.

### Verificación

```bash
python3 -c "
import json, subprocess
with open('/hermes-home/skills/.skill-learning-state.json') as f:
    state = json.load(f)
for skill in state.get('learned', []):
    result = subprocess.run(
        ['find', '/hermes-home/skills', '-name', 'SKILL.md', '-path', f'*{skill}*'],
        capture_output=True, text=True
    )
    if result.stdout and 'quarantine' not in result.stdout:
        print(f'OK: {skill}')
    else:
        print(f'MISSING: {skill}')
"
```

### Solución

1. Eliminar skills problemáticos del state:
```python
import json
with open('/hermes-home/skills/.skill-learning-state.json') as f:
    data = json.load(f)
# Quitar skills que no existen en disco
import subprocess, os
new_learned = []
for skill in data.get('learned', []):
    result = subprocess.run(
        ['find', '/hermes-home/skills', '-name', 'SKILL.md', '-path', f'*{skill}*'],
        capture_output=True, text=True
    )
    if result.stdout and 'quarantine' not in result.stdout:
        new_learned.append(skill)
data['learned'] = new_learned
with open('/hermes-home/skills/.skill-learning-state.json', 'w') as f:
    json.dump(data, f, indent=2)
print(f'Restored to {len(new_learned)} skills')
```

2. Avanzar el índice al siguiente skill no instalado:
```python
import json
with open('/hermes-home/skills/.skill-learning-state.json') as f:
    data = json.load(f)
# El índice debería ser len(learned) si no hay gaps
data['current_index'] = len(new_learned)
with open('/hermes-home/skills/.skill-learning-state.json', 'w') as f:
    json.dump(data, f, indent=2)
```

## Problem: Skill en quarantine — reintentos infinitos

### Causa

`hermes skills install` falló y el skill se movió a `.hub/quarantine/`. El script `skill-learning.sh` sigue intentando instalar el mismo skill en cada ejecución.

### Verificación

```bash
ls /hermes-home/skills/.hub/quarantine/
```

### Solución

```bash
# 1. Eliminar de quarantine
rm -rf /hermes-home/skills/.hub/quarantine/<skill-name>

# 2. Avanzar el índice en el state
python3 -c "
import json
with open('/hermes-home/skills/.skill-learning-state.json') as f:
    data = json.load(f)
data['current_index'] = data['current_index'] + 1
with open('/hermes-home/skills/.skill-learning-state.json', 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Problem: Timeout en instalación

### Causa

`hermes skills install` tarda más de 120s (timeout del cron). El script falla pero no avanza el índice.

### Verificación

```bash
grep "timeout\|TIMED OUT\|FAIL" /hermes-home/skills/skill-learning.log | tail -5
```

### Solución

Normalmente se resuelve solo en la siguiente ejecución. Si persiste:
1. Verificar que `hermes` funciona: `hermes skills list | head -5`
2. Instalar manualmente: `hermes skills install <skill-id>`
3. Si funciona, avanzar el índice manualmente como arriba.
