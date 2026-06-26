# TerrAn — Sistema de Auto-Auditoría Cíclica

## Concepto

Cron loop que audita cíclicamente la arquitectura del proyecto hasta que no encuentra más issues. Cada iteración audita UNA fase (de 8). Cuando una fase está limpia, avanza a la siguiente. Cuando las 8 fases están limpias, el proyecto se considera auditado.

```bash
Cada día a las 10:00 UTC
         │
         ▼
┌─────────────────────────────────┐
│  1. Leer estado + docs          │
│  2. Auditar FASE ACTIVA         │
│  3. ¿Issues encontrados?        │
│     ├── Sí → registra + reporta │
│     └── No → avanza fase        │
│  4. Reporta resultados          │
└─────────────────────────────────┘
         │
         ▼
   Siguiente iteración ♻️
```

## Archivos del sistema

| Archivo | Propósito |
|---------|-----------|
| `/root/workspace/geoasset/audit-state.json` | Estado: fase actual, issues encontrados/fijados, iteraciones |
| `/hermes-home/scripts/terran-auditor.py` | Motor de auditoría: leer docs, loguear issues, avanzar fases |
| Cron `terran-audit-loop` | Programación diaria a las 10:00 UTC |

## 8 Fases de auditoría

| # | Fase | Qué audita |
|---|------|-----------|
| 01 | Estructura del Schema | Normalización, constraints, tipos, FKs, soft delete, particiones |
| 02 | Permisos y RBAC | Roles, RLS, multi-tenant, jerarquía, admin override, lock release |
| 03 | Modelo de Datos Avanzado | JSONB vs tablas, índices, audit log size, cache invalidation |
| 04 | API y Backend | Validación, rate limiting, idempotencia, WebSocket, plugins |
| 05 | Rendimiento | Query plans, N+1, 3D LOD, heightmap, PostgreSQL config |
| 06 | Seguridad y Compliance | GDPR, Ley 39/2015, soft delete recovery, data retention |
| 07 | Lógica de Negocio | Importación Excel, export, pricing, onboarding |
| 08 | UX y Flujos | Empty states, formularios dinámicos, mobile, error recovery |

## Comandos de gestión

```bash
# Ver estado
python3 /hermes-home/scripts/terran-auditor.py status

# Ejecutar iteración manual (lo mismo que hace el cron)
hermes cron run terran-audit-loop

# Ver estado del cron
hermes cron list | grep terran

# Pausar/reanudar
hermes cron pause terran-audit-loop
hermes cron resume terran-audit-loop

# Reiniciar auditoría desde 0
python3 /hermes-home/scripts/terran-auditor.py reset
```

## Uso interno del script (para el cron)

```bash
# Obtener estado + docs para auditar
python3 /hermes-home/scripts/terran-auditor.py run

# Registrar un issue encontrado
python3 /hermes-home/scripts/terran-auditor.py log-issue <phase_id> '{"id": "PERM-001", "title": "...", "severity": "alta|media|baja", "description": "...", "impact": "...", "proposed_solution": "..."}'

# Marcar issue como fijado
python3 /hermes-home/scripts/terran-auditor.py log-fix <phase_id> <issue_id> '<resolution>'

# Avanzar a siguiente fase
python3 /hermes-home/scripts/terran-auditor.py advance
```

## Reglas del cron

1. **Sé exhaustivo, no benevolente** — cada issue potencial es un issue real
2. **Cada issue debe tener solución concreta** — no "hay que mejorarlo"
3. **No avances de fase si hay issues activos** — cada fase debe quedar 100% limpia
4. **El ADMIN debe poder editar/crear cualquier cosa** — si el sistema de permisos lo impide, es issue crítico
5. **Lee los documentos literalmente** — no asumas que algo "seguro que está bien"

## Pitfalls del sistema de auditoría

### max_issues_per_phase debe ser 100+

La config `max_issues_per_phase: 20` es insuficiente. Una fase de seguridad puede tener 30-50 issues reales. **Subir a 100+** para evitar confusiones.

### Formato de salida de `run` varía

En algunas iteraciones, `phase` es un objeto plano con `issues_already_found`. En otras, es un array `phases[]`. **Siempre verificar ambas estructuras** al parsear la salida.

### JSON encoding en `log-issue`

El script usa `sys.argv[3]` con `json.loads()` — **no acepta comillas simples dentro del JSON**. Si el JSON contiene `"` o `'`, el shell las escapa mal y `json.loads()` falla con `Unterminated string`.

**Solución:** Usar `execute_code` con `json.dumps(issue, ensure_ascii=False)` para generar el JSON, luego pasarlo al comando. O usar unicode escapes (`\u2014` para `—`, `\u201c` para `"`).

## Cuándo reutilizar este patrón

Este patrón (state file + script auditor + cron cíclico) se puede aplicar a cualquier proyecto donde:
- Haya múltiples aspectos que auditar (fases/secuencias)
- Se quiera asegurar que cada aspecto queda limpio antes de avanzar
- Se necesite seguimiento a largo plazo (no solo una auditoría puntual)
- El usuario quiera "no parar hasta que no queden issues"

## Referencias cruzadas

- `references/security-compliance-issues-detailed.md` — Listado completo de los 36 issues de seguridad (iter 90-106) con distribución por categoría.