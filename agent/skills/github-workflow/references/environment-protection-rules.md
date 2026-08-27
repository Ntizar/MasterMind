# GitHub Pages Environment Protection Rules

## Problema

Cuando un workflow de GitHub Pages usa `environment: github-pages`, el entorno puede tener reglas de protección de rama (`deployment_branch_policy` con `type: branch_policy`) que solo permiten la rama original (`master`). Al renombrar a `main`, el deploy falla inmediatamente con:

```
Branch "main" is not allowed to deploy to github-pages due to environment protection rules.
```

## Señales de diagnóstico

- El workflow termina en **2-5 segundos** (demasiado rápido para un deploy real)
- El job termina en `failure` con la anotación sobre protection rules
- El workflow fue creado automáticamente por GitHub al activar Pages por primera vez
- El error aparece inmediatamente, sin ejecutar ningún step

## Soluciones

### Opción A: Eliminar el entorno (recomendado para proyectos personales)

```python
import urllib.request, json

token = '...'  # leer de .env
req = urllib.request.Request(
    f'https://api.github.com/repos/{owner}/{repo}/environments/{env_name}',
    headers={'Authorization': f'token {token}'},
    method='DELETE'
)
urllib.request.urlopen(req)  # 204 = OK
```

Luego quitar `environment:` del workflow YAML.

### Opción B: Usar workflow sin environment

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    # Sin environment: ni environment protection rules
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
          exclude: |
            .git/
            agents/
            .opencode/
            learning-platform/
            design-system/
            docs/
            assets/
            scripts/
            verify-system.bat
            verify-system.sh
            CONTRIBUTING.md
            README.md
            README_EN.md
            LICENSE
            CHANGELOG.md
            skills/
      - uses: actions/deploy-pages@v4
```

## Casos reales

- **NtizarBrainMasterMind** (Junio 2026): Renombrado de `master` a `main`, workflow con `environment: github-pages` falló porque el entorno solo permitía `master`. Solución: eliminar entorno + quitar `environment:` del workflow.
- **Deploy inicial:** GitHub crea automáticamente el entorno `github-pages` con protección de rama. Si sabes que vas a renombrar la rama, mejor usar workflow sin environment desde el inicio.

## Referencias

- [GitHub Docs: Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [GitHub Docs: Deployment branch policies](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment#deployment-branch-policies)
