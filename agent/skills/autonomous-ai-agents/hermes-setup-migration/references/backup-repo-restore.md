# Backup Repo Restore — Concrete Recipe (Windows, git-bash)

From a real restore: repo `Ntizar/MasterMind` (formerly NtizarBrainMasterMind) → `%LOCALAPPDATA%\hermes\`.

## 1. Clone & inventory

```bash
git clone --depth 1 https://github.com/<user>/<repo> "$LOCALAPPDATA/Temp/<repo>"
# check both skill trees — root skills/ often has .curator_state / .usage.json (LIVE copy)
ls <repo>/hermes-home/skills | wc -l;  ls <repo>/skills | wc -l
du -sh */  # spot heavy legacy dirs
```

## 2. Skills add-only copy

```bash
H="$LOCALAPPDATA/hermes"; added=0; skipped=0
for src in "$R/hermes-home/skills" "$R/skills"; do
  for d in "$src"/*/; do
    n=$(basename "$d")
    [ -e "$H/skills/$n" ] && { skipped=$((skipped+1)); continue; }
    cp -r "$d" "$H/skills/$n" && added=$((added+1))
  done
done
echo "added: $added, skipped: $skipped"
```

Verify: `find "$H/skills" -maxdepth 3 -iname SKILL.md | wc -l`.

## 3. Memory union-merge (§ format)

Memory entries are separated by `§` lines, CRLF-laden. Union both trees, dedupe on normalized first-80-chars:

```python
def union(f1, f2, out):
    a = open(f1, encoding='utf-8-sig').read()
    b = open(f2, encoding='utf-8-sig').read()
    parts = [p.strip() for p in (a.split('§') + b.split('§'))]
    seen, uniq = set(), []
    for p in parts:
        key = p.replace('\r','').replace('\n',' ')[:80]
        if p and key not in seen:
            seen.add(key); uniq.append(p.strip())
    open(out, 'w', encoding='utf-8', newline='\n').write('\n§\n'.join(uniq) + '\n')
    print(out, '->', len(uniq), 'entries')
```

If the live install has no `MEMORY.md`/`USER.md` yet, plain `cp` is fine (check with `wc -c` first).

## 4. Identity & scripts

- `SOUL.md` / `user.md` from repo → `memories/SOUL.repo.md`, `memories/USER.repo.md` (never overwrite live `SOUL.md` without asking).
- Scripts → `$H/scripts/restored/` (20 scripts in the reference case: ChromaDB index/query, backup, Ebbinghaus, BiciMAD, stars-explorer...). Flag Linux-only paths (`/root/workspace/...`, `python3` only) for Windows rework.

## 5. Repo rename + reorganization

```bash
cd ~/Projects/<repo> && gh repo rename MasterMind --yes   # updates remote
```

If the local folder name must change and `mv` fails with "Device or resource busy" (Project workspace lock): `cp -a` old new, verify, `rm -rf` old (needs separate approval).

Target structure used:

```
agent/    skills/ + MEMORY.md + USER.md + SOUL.md + config.yaml
scripts/  motor scripts (chromadb, stars-explorer, backup, control-m/)
notes/    learning notes (YYYY-MM-DD-*.md)
data/     stars-registry.json
index.html + assets/ + design-system/   (public Pages site)
AGENTS.md SOUL.md README.md
```

Sequence: `git mv` skill trees into `agent/skills` → move non-duplicate files → diff both trees; for dirs that DIFFER, prefer the copy with fresher curator state → `rm -rf` empty/duplicate trees (separate command, explicit user confirmation) → single `git add -A` commit.

## 6. What does NOT migrate (report to user)

- **Cron jobs** — lived in the old machine's Hermes. Recreate with the cronjob tool (e.g. mastermind-scout every 6h for GitHub stars learning, weekly digest).
- **ChromaDB + embeddings** — needs `pip install chromadb` + re-indexing all skills on the new machine.
- **Old config.yaml** — provider/model/keys: current install keeps its own; extract only requested settings via `hermes config set`.
- **API keys** — old machine's `.env` is not in the repo (correct); user must re-enter keys.
