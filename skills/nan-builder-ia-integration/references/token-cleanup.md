# Token cleanup — eliminar token accidentalmente subido a Git

## Escenario

Se hizo `git add -f .env` y el token quedó en el historial de Git. Esto es un problema de seguridad: cualquier persona con acceso al repo puede ver el token en el historial.

## Solución

### 1. Reset suave al commit anterior

```bash
cd /path/to/project
git reset --soft HEAD~1        # Quitar el commit pero mantener cambios
git reset HEAD .env             # Quitar .env del staging
git commit -c HEAD --amend      # Re-commit sin .env
git push --force                # Forzar push para actualizar remoto
```

### 2. Verificar que el token ya no está

```bash
git show HEAD:.env 2>&1 || echo "NO ENCONTRADO"  # Debe dar error
git ls-files | grep env  # No debe mostrar .env
```

### 3. Restaurar .env local

```bash
echo "NAN_API=$NAN_API" > .env  # Recrear localmente
```

### 4. Verificar repo privado

```bash
curl -s -X PATCH "https://api.github.com/repos/USER/REPO" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"private": true}'
```

## Regla de oro

**NUNCA** hacer `git add -f .env` ni `git add .env` bajo ninguna circunstancia. El token debe estar en `.gitignore` y solo existir en el entorno local.

## Si ya se subió en un commit anterior (no el último)

Usar `git filter-branch`:

```bash
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all
git push --force --all
git push --force --tags
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

O usar `git filter-repo` (más moderno, recomendado si está disponible).
