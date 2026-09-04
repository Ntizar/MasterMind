# Git push con GITHUB_TOKEN — Patrón de credenciales

## Problema

El token de GitHub (`GITHUB_TOKEN` en `/hermes-home/.env`) puede funcionar para la API REST pero fallar con git push. Sintomas:
- `gh` CLI no instalado o no funciona con el token
- `git push` pide contraseña y falla
- `credential.helper store` no funciona
- `GIT_ASKPASS=true` no funciona

## Solución: credential helper inline

```bash
source /hermes-home/.env
GIT_TERMINAL_PROMPT=0 git -c 'credential.helper=!f() { echo "username=oauth2"; echo "password='$GITHUB_TOKEN'"; }; f' push -u origin main
```

## Por qué funciona

El `credential.helper` inline inyecta las credenciales directamente sin pasar por el sistema de credenciales de git. `oauth2` como username es el formato que GitHub espera para tokens.

## Pitfalls

- **Primer push OK, siguientes fallan:** El credential helper inline se pasa en el comando, no se guarda. Siempre usar el mismo patrón `-c 'credential.helper=...'` en cada push.
- **Token de instalación vs user token:** Si el token es de instalación, puede funcionar con la API REST pero NO con git. Verificar con `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user` — si devuelve 200, funciona para ambas cosas.
- **Token con caracteres especiales:** Los tokens tienen formato `ghp_xxxxxxxx` y pueden contener caracteres que rompen URLs. NUNCA usar `https://TOKEN@github.com/...`.
- **`credential.helper store` no funciona:** Escribir credenciales en `~/.git-credentials` puede fallar si el token es de instalación o tiene permisos limitados.

## Verificar si el token funciona para git

```bash
source /hermes-home/.env
curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
# 200 = token válido, puede funcionar con git
# 401 = token inválido o sin permisos
```

## Referencias

- Sesión 2026-06-17: proyecto Nogal 9 — se usó este patrón para push al repo Ntizar/nogal9
