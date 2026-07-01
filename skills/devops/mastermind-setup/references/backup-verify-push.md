# Backup — Verificación de Push y Estado del Repo

**Creado:** 2026-07-01

## Verificar que el backup fue realmente pushado

Tras hacer `git add -A && git commit -m "Backup..."`, NUNCA asumir que el push funciona. Verificar explícitamente:

```bash
cd /root/workspace/Mastermind

# 1. Comparar HEAD local vs origin/main (o origin/master)
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main 2>/dev/null)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "✅ Pushed a origin/main"
else
    echo "⚠️ NO pushado — divergencia detectada"
    echo "Local: $LOCAL"
    echo "Remote: $REMOTE"
fi
```

## Verificar branch divergence

El repo puede tener **dos ramas en remoto** (`main` y `master`) que divergen:

```bash
# Ver ramas locales y remotas
git branch -v
git branch -r

# Ver qué commits están en remote pero no en local
git log --oneline origin/master..HEAD 2>/dev/null | wc -l  # commits locales no en remote
git log --oneline HEAD..origin/master 2>/dev/null | wc -l  # commits remote no en local
```

**Patrón típico del repo Mastermind:**
- `origin/main` → rama del backup cron (sincronizada con local)
- `origin/master` → rama con commits adicionales (ej. Stars Explorer)
- Local `main` = `origin/main` → push OK
- `origin/master` puede tener commits que local no tiene → divergencia benigna

## Verificar git status después de rsync

Tras rsync, `git status` puede mostrar 0 cambios incluso si rsync "corrió". Esto es normal:

```bash
# Si git status muestra 0 cambios → rsync detectó que todo estaba igual
# Si muestra cambios → hay archivos nuevos o modificados
git status --short | wc -l
```

**Caso normal:** rsync -av compara timestamps y tamaños. Si los archivos son idénticos, rsync no copia nada y git status queda limpio.

## Contar archivos copiados

```bash
# Skills en destino
find /root/workspace/Mastermind/hermes-home/skills -type f | wc -l

# Source skills
find /hermes-home/skills -type f | wc -l

# Notes
find /root/workspace/Mastermind/hermes-home/notes -type f 2>/dev/null | wc -l

# Memories
find /root/workspace/Mastermind/hermes-home/memories -type f 2>/dev/null | wc -l

# Scripts
find /root/workspace/Mastermind/hermes-home/scripts -type f 2>/dev/null | wc -l
```

## Reporte de estado post-backup

Después de cada backup, verificar y reportar:
1. Skills files en repo vs source (comparar conteos)
2. Notes files en repo vs source
3. Memories files (deben coincidir)
4. Scripts files en repo vs source
5. config.yaml: ¿diferente entre source y repo?
6. Git status: ¿0 cambios?
7. Push status: ¿HEAD = origin/main?
8. Total files en repo (excl .git)

## Pitfalls

- **rsync con --delete es destructivo:** Elimina archivos del destino que ya no existen en origen. Solo usar si se quiere espejo exacto. Para backup incremental seguro, usar `rsync -av` SIN `--delete`.
- **0 cambios post-rsync no significa fallo:** rsync solo copia archivos diferentes. 0 cambios = backup ya actualizado.
- **Branch divergence es normal:** Si el cron de Stars Explorer y el backup cron corren en paralelo, pueden crear commits divergentes en diferentes ramas. Verificar con `git log --oneline` local/remote.
- **origin/main vs origin/master:** El repo tiene ambas ramas. El backup cron usa `origin/main`, pero otros procesos pueden usar `origin/master`. No confundir.
- **`git push origin HEAD` puede decir "Everything up-to-date" incluso con divergence:** Si `origin/main` existe y coincide con HEAD, el push dice "up-to-date" aunque `origin/master` diverja. Verificar ambas ramas.
