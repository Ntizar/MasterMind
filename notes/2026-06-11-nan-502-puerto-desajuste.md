# Error 502 en NaN por desajuste de puertos

**Fecha:** 2026-06-11
**Proyecto:** Mastermind Dashboard
**Repo:** Ntizar/Mastermind-Dashboard

## Síntoma

- Build Kaniko exitoso (commit 9a4785c)
- Contenedor aparece como "Running"
- URL devuelve 502 Bad Gateway (Cloudflare: "Host: Error")
- `/healthz` también 502

## Causa

NaN.builders tiene **3 lugares donde se define el puerto**, y NO coincidían:

| Lugar | Valor real | Valor esperado |
|---|---|---|
| Container Port (NaN UI) | **6060** | 6060 |
| `EXPOSE` en Dockerfile | **4040** | ❌ |
| `HEALTHCHECK` en Dockerfile | `localhost:4040/healthz` | ❌ |
| `PORT` default en server.js | `4040` | ❌ |

**Mecanismo:** NaN inyecta `PORT=6060` automáticamente. El servidor escuchaba en 6060, pero el HEALTHCHECK buscaba en `localhost:4040/healthz` → fallaba → NaN mataba el contenedor → 502.

## Fix aplicado

1. **Dockerfile:** `EXPOSE 4040` → `EXPOSE 6060`
2. **Dockerfile:** HEALTHCHECK ahora prueba `localhost:6060/healthz` primero, luego `localhost:4040` como fallback
3. **server.js:** Puerto por defecto cambiado a `6060`, y ahora escucha en **ambos puertos** (6060 y 4040)

## Lecciones aprendidas

1. **Siempre verificar los 3 puertos** antes de desplegar: Container Port (NaN UI), EXPOSE (Dockerfile), PORT default (server.js)
2. **NaN inyecta `PORT=<container-port>` automáticamente** — no hace falta configurarlo en Env
3. **El HEALTHCHECK debe apuntar al mismo puerto** que el servidor escucha
4. **El HEALTHCHECK debe ser un endpoint público** (sin auth), puesto ANTES del middleware de auth
5. **NaN no tiene webhooks** — usa polling cada 1-5 min. Para redeploy inmediato hay que ir al dashboard
6. **Escuchar en ambos puertos** (principal + fallback) da tolerancia a cambios de configuración

## Skill creado

`nan-puerto-desajuste` en `/hermes-home/skills/devops/nan-puerto-desajuste/`