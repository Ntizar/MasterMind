# Validación de fuentes de verdad — Inventario de APIs

**Fecha:** 2026-06-22  
**Contexto:** Sesión de diagnóstico de divergencia entre repos `/tmp/` y `/opt/`

## Problema

Dos repos git independientes apuntan al mismo remote GitHub:
- `/tmp/inventario-apis/` → working copy (cron ejecuta aquí)
- `/opt/hermes-work/inventario-apis/` → repo persistente (script procesa aquí)

Cada uno tiene su propio `.git`, sus propios commits, y su propio `estado.json`.

## Diagnóstico paso a paso

### 1. Identificar cuál repo está sync'd con GitHub

```bash
# Obtener HEAD de cada repo
git -C /tmp/inventario-apis rev-parse HEAD
git -C /opt/hermes-work/inventario-apis rev-parse HEAD

# Obtener HEAD del remote
git -C /tmp/inventario-apis fetch origin
git -C /tmp/inventario-apis rev-parse origin/main

# Comparar: si HEAD local == origin/main, ese repo está sync'd
```

**Resultado 2026-06-22:** `/tmp/` está sync'd con GitHub. `/opt/` tiene historia divergente.

### 2. Verificar ancestralidad

```bash
# ¿HEAD de A es ancestro de HEAD de B?
git -C /opt/hermes-work/inventario-apis merge-base --is-ancestor <head-a> HEAD
# exit 0 = sí es ancestro, exit 1 = no
```

### 3. Contar commits reales

```bash
git -C /tmp/inventario-apis rev-list --count HEAD
git -C /opt/hermes-work/inventario-apis rev-list --count HEAD
```

### 4. Validar estado.json vs directorios reales

```python
# Para cada repo:
total_dirs = sum(
    len([d for d in os.listdir(f"{repo}/{cat}") if os.path.isdir(f"{repo}/{cat}/{d}")])
    for cat in os.listdir(repo)
    if os.path.isdir(f"{repo}/{cat}") and cat != '.git'
)
# Comparar total_dirs con estado.json['procesadas']
```

## Reglas de verdad (orden de fiabilidad)

1. **Directorios reales** (`find`/`os.listdir`) — lo que físicamente existe
2. **Remote GitHub** (`git rev-parse origin/main`) — lo que está publicado
3. **estado.json** — puede estar desfasado si el script no lo actualizó
4. **README.md** — puede incluir texto que no son APIs reales

## Hallazgos de 2026-06-22

| Aspecto | /tmp/ | /opt/ |
|---------|-------|-------|
| Commits | 931 | 757 |
| APIs (estado.json) | 505 | 3,648 |
| Directorios reales | 4,097 | 3,611 |
| Sync'd con GitHub | ✅ Sí | ❌ No |
| Última actividad | 2026-06-22 | 2026-06-17 |
| Rama | main | master |

**Conclusión:** `/tmp/` es la copia activa y sync'd. `/opt/` es un fork divergente con más datos en estado.json pero menos commits git. Las categorías de `/opt/` son más completas para el desglose, pero el conteo real debe basarse en directorios de `/tmp/`.
