# TerrAn Auditor Tool Usage

## `terran-auditor.py log-issue`

### Sintaxis
```bash
python3 /hermes-home/scripts/terran-auditor.py log-issue <PHASE_ID> <JSON_ISSUE>
```

### Parámetros

- **PHASE_ID**: El ID completo de la fase como aparece en `audit-state.json` → `phases[].id`.
  - Ejemplo: `06-security-compliance`, `07-business-logic`, `08-ux-workflow`
  - **NO usar prefijos cortos** como `SEC`, `DATA`, `PERM`. Devuelve `❌ Fase 'SEC' no encontrada`.

- **JSON_ISSUE**: JSON con las claves: `id`, `title`, `severity`, `description`, `impact`, `proposed_solution`.

### Pitfall: JSON encoding (iter 90+)

El script usa `sys.argv[3]` con `json.loads()` — **no acepta comillas simples dentro del JSON**. Si el JSON contiene `"` o `'`, el shell las escapa mal y `json.loads()` falla con `Unterminated string`.

**Solución (recomendada):** Usar `execute_code` con un script Python temporal:
```python
import json, subprocess
issue = {"id": "SEC-064", "title": "Usuarios sin org_id", "severity": "alta", "description": "...", "impact": "...", "proposed_solution": "..."}
json_str = json.dumps(issue, ensure_ascii=False)
result = subprocess.run(
    ["python3", "/hermes-home/scripts/terran-auditor.py", "log-issue", "06-security-compliance", json_str],
    capture_output=True, text=True
)
print(result.stdout)
```

**Solución 2:** Usar unicode escapes (`\u2014` para `—`, `\u201c` para `"`).

### Pitfall: Fase ya existe

Si se loguea un issue con ID que ya existe, devuelve `⏭️ Issue ya existe (ID: XXX-XXX)`. No es error, es un skip.

## `terran-auditor.py run`

Devuelve el estado actual con:
- `iteration`: número de iteración
- `phase`: objeto con `id`, `name`, `issues_found[]`, `issues_fixed[]`, `clear`
- `completed`: boolean

### Estructura variable (iter 106+)

En algunas iteraciones, el `run` devuelve `phase` como un objeto plano con `issues_already_found` directamente. En otras, devuelve `phases` como array. **Siempre verificar ambas estructuras** al parsear la salida.

## `terran-auditor.py advance`

Avanza a la siguiente fase. Solo funciona si la fase actual tiene 0 issues abiertos.

## `audit-state.json` structure

- Usa `phases[].issues_found[]` — No usar `findings[].sub_findings[]`.
- La fase activa es la que tiene `clear: false` (o ausencia del flag). No hay key `current_phase` en la raíz.
- `config.max_issues_per_phase`: por defecto 20, pero fases de seguridad pueden tener 30-50 issues. **Subir a 100+** para evitar confusiones.
- `status: "fixed"` no es garantía — los fixes documentados pueden tener errores estructurales. Siempre verificar en los documentos.
