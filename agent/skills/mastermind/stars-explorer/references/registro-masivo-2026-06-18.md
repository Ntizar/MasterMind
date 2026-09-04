# Registro Masivo de Stars — 2026-06-18

## Contexto

David pidió procesar **todas sus stars de GitHub** (117 repos) en vez de esperar 30+ días al cron de a 3/noche.

## Lo que funcionó

### Registro masivo en vez de `--all`

```python
# NO USAR: se timeout a 300s
bash run-stars-explorer.sh --all  # ❌ Timeout

# USAR: fetch paginado + 1 req/repo para registro
for repo_name in all_repos:
    url = f"https://api.github.com/repos/{repo_name}"
    headers = {"Authorization": f"token {TOKEN}"}
    resp = urlopen(req, timeout=10)
    data = json.loads(resp.read())
    reg['processed'][repo_name] = {
        'category': 'pending',
        'stars': data.get('stargazers_count', 0),
        'language': data.get('language'),
    }
    time.sleep(0.3)  # 50 repos cada 15s
```

### Clasificación en 4 tiers

| Tier | Criterio | Acción |
|------|----------|--------|
| **high** | >= 3000⭐ | Subagent prioritario |
| **medium** | 500-3000⭐ | Subagent si hay slots |
| **low** | < 500⭐ | Cron |
| **skip** | "awesome" en el nombre | Marcar y olvidar |

### 3 subagentes en paralelo con 6-8 repos cada uno

Cada subagente recibió en `context` una lista explícita de skills que YA EXISTEN para evitar investigaciones redundantes.

### Skills creados (8)

1. `spec-driven-development` (development/) — github/spec-kit, 113K⭐
2. `qlib-quant` (data-science/) — microsoft/qlib, 44K⭐
3. `timesfm-forecast` (data-science/) — google-research/timesfm, 22K⭐
4. `presidio-pii` (security/) — microsoft/presidio, 8.6K⭐
5. `huly-crm-erp-platform` (backend/) — hcengineering/platform, 26K⭐
6. `nocobase-nocode-backend` (backend/) — nocobase/nocobase, 22K⭐
7. `liteparse-document-ai-parsing` (ia/) — run-llama/liteparse, 10K⭐
8. `agent-reach` (ia/) — Panniantong/Agent-Reach, 34K⭐

### GitHub sync

```bash
cd /root/workspace/Mastermind
mkdir -p skills/{development,data-science,security,backend,ia}
cp -r /hermes-home/skills/*/ spec-name*/ skills/*/
git add -A && git commit -m "✨ N skills nuevos de stars" && git push
```

## Tiempos reales

| Fase | Tiempo real |
|------|-------------|
| Registrar 50 repos en registry | ~15s |
| 3 subagentes analizando 18 repos (primer batch) | ~5 min |
| Crear 8 skills | ~5 min |
| Indexar ChromaDB | ~1 min |
| GitHub push | ~10s |
| **Total** | **~12 min** |

## Lecciones

- Los subagentes necesitan context con skills existentes para no duplicar trabajo
- La creación de skills debe ser RÁPIDA (SKILL.md pequeños, no novelas)
- GitHub es obligatorio — David lo pide explícitamente
- Los repos "awesome-*" siempre skip (ahorran tiempo de subagentes)
- `--all` del script NO USAR para >50 repos — mejor registro manual