---
name: hermes-setup-migration
description: "Restore a Hermes backup repo into an install."
version: 1.0.0
author: Hermes Agent + David Antizar
license: MIT
tags: [hermes, migration, restore, backup, windows, skills, memory]
metadata:
  hermes:
    tags: [hermes, migration, restore, backup, windows, skills, memory]
    related_skills: [hermes-agent]
---

# Hermes Setup Migration / Restore

## When to Use

Use when the user wants to bring an old Hermes installation (usually a backup repo containing `hermes-home/`, `skills/`, `memories/`, `scripts/`) into the current Hermes install, or move their agent setup to a new machine. Typical trigger: "quiero meter mi configuración antigua en Hermes". Not for: generic git repo cleanup unrelated to a Hermes home.

Use when the user wants to bring an old Hermes installation (usually a backup repo containing `hermes-home/`, `skills/`, `memories/`, `scripts/`) into the current Hermes install, or move their agent setup to a new machine. Typical trigger: "quiero meter mi configuración antigua en Hermes".

## Workflow

1. **Inventory the source first, never guess.** Clone the backup repo to a scratch dir and list: `hermes-home/skills/`, `hermes-home/memories/`, root-level `skills/`, `scripts/`, `SOUL.md`, `config.yaml`. Backup repos often have DUPLICATED trees (root `skills/` + `hermes-home/skills/`) with different freshness — check internal state files (`.curator_state`, `.usage.json` mtimes) to identify which copy is the live one.
2. **Resolve the target home.** On Windows the Hermes home is `%LOCALAPPDATA%\hermes\` (NOT `~/.hermes`). Profiles live under `AppData\Local\hermes\profiles\<name>\`.
3. **Ask the merge policy before copying** (clarify): add-only (skip skills that already exist locally — usually right when the local install is newer), overwrite-all, or staged. Never silently overwrite.
4. **Copy skills add-only.** Loop over source skill dirs, skip names that already exist in target `skills/`. Count added/skipped and report both.
5. **Union-merge memory files, never replace.** Hermes memory files (`MEMORY.md`, `USER.md`) use a `§`-delimited entry format. Merge by splitting on `§`, deduping on a normalized key (strip `\r`/`\n`, first ~80 chars), joining back with `\n§\n`. Full recipe in references.
6. **SOUL / identity files:** copy old `SOUL.md`/`user.md` in as `SOUL.repo.md`/`USER.repo.md` references — do not overwrite the live `SOUL.md` unless the user says so.
7. **Scripts:** copy to `<hermes-home>/scripts/` (a subfolder like `scripts/restored/` avoids clobbering). Flag Linux-only assumptions (`/root/...` paths, chromadb, systemd cron) — they need rework on Windows.
8. **Do NOT restore the old `config.yaml`.** The current install has its own provider/model config. Only extract individual settings the user explicitly asks for (`hermes config set ...`, never hand-edit).
9. **Report the gap list:** cron jobs do NOT live in the backup (they were on the old machine's Hermes instance); vector DBs (ChromaDB) and API keys need re-setup. Offer to recreate crons via the cronjob tool.

## Repo maintenance (if the backup repo itself is being cleaned/renamed)

- Rename on GitHub + local: `gh repo rename <new-name> --yes` (updates the remote automatically). Do the rename FIRST, before restructuring, so the local remote is correct.
- Restructure with `git mv` where possible to preserve history; for cross-tree merges plain `mv` + one big `git add -A` commit is fine — git records the content change either way.
- Deleting tracked files is safe (history preserves them), but destructive `rm -rf` from the agent requires explicit user confirmation — see pitfalls.

## Pitfalls (all hit in practice — Windows/git-bash)

- **`project_create` / an open Project locks the folder.** `mv` on the workspace dir fails with "Device or resource busy". Workaround: `cp -a` to the new name, verify, then remove the old dir. Don't retry `mv` in a loop.
- **Destructive `rm -rf` from terminal needs interactive approval.** If bundled into a long command chain, the approval prompt can time out and the whole command is BLOCKED ("Silence is not consent"). Split deletes into their own command and get explicit confirmation (clarify) first. If a blocked-command error appears, do NOT rephrase/retry the same destructive action — ask the user once.
- **Python heredocs via terminal may be flagged/approved unpredictably.** Prefer `python -c` one-liners or a temp `.py` file for merge logic.
- **git-bash cwd quirk:** after `cd`, a later `git -C <path>` in the SAME session may fail spuriously; entering with `cd <path> && git ...` works.
- **Both memory trees may differ** (root vs `hermes-home/memories/`) — union-merge instead of picking one, or you silently lose entries.
- **Temp dirs are bad homes:** clones in `$LOCALAPPDATA/Temp` get cleaned; move real repos to `~/Projects/` (or the user's preferred root) as part of the job.

## References

- `references/backup-repo-restore.md` — concrete end-to-end recipe from a real restore (paths, merge script, reorg sequence, cron recreation notes).