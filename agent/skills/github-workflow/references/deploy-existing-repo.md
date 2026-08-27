# Deploy Pages para Repo Existente

**Lección:** Antes de crear un repo, verificar que no exista con `git clone`.

## Problema

En sesión de 2026-06-17, se confundió `farosspain` (dos S) con `farospain` (una S) y se creó un repo nuevo en vez de usar el existente.

## Flujo seguro

```bash
# 1. Intentar clonar primero
git clone https://github.com/Ntizar/nombre-repo.git
# Si falla → crear desde cero (sección 12 del skill)
# Si funciona → continuar

# 2. Verificar Pages activo
curl -s https://api.github.com/repos/Ntizar/nombre-repo/pages \
  -H "Authorization: token $TOKEN" | jq '.html_url'

# 3. Verificar que sirve
curl -s -o /dev/null -w "%{http_code}" https://Ntizar.github.io/nombre-repo/
# → 200 = OK
# → 404 = Pages activo pero build fallido
```

## Pitfalls

- Nombres similares: `farosspain` ≠ `farospain`
- Pages puede estar activo con build_type diferente (workflow vs legacy)
- Workflow puede existir pero no haber trigger (no se ha hecho push)
- Branch name: verificar `main` vs `master`
