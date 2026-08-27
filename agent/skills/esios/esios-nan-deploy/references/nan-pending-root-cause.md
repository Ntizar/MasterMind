# NaN "Build Succeeded → Pending Forever" — Root Cause Analysis

## Síntoma

1. Build Kaniko exitoso (se ve "succeeded" en build history)
2. Current Image se genera con SHA
3. Status se queda en "pending" para siempre (> 10 min)
4. URL devuelve 404 de Cloudflare (no 502, no timeout)
5. No hay logs de contenedor porque nunca arrancó

## Causa Raíz

**El contenedor ejecuta como root.** NaN.builders **bloquea** pods que corren como root por seguridad. Kaniko construye la imagen perfectamente (por eso el build es "succeeded"), pero el orquestador de NaN rechaza el pod al intentar arrancarlo.

## Diagnóstico Rápido

```bash
# Verificar si el Dockerfile tiene USER appuser
grep -n 'USER' Dockerfile
# Si no aparece → es la causa
```

## Fix

```dockerfile
# Añadir ANTES del CMD:
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

USER appuser
```

## También verificar

- **`.dockerignore`** existe? Sin él, `COPY . .` mete `node_modules/` y `.git/`.
- **Puerto coincide?** `EXPOSE` en Dockerfile = puerto configurado en NaN.
- **`package.json` sin `"type": "module"`?** Si tiene + `require()` en server.js → crash ESM/CJS.
- **`package-lock.json` sincronizado?** Si no, `npm ci` falla silenciosamente.
- **Healthcheck público?** Si el healthcheck apunta a un endpoint con auth, el contenedor se reinicia en bucle.

## Caso real: Mastermind Dashboard

### Iteración 1 — Root container
- Build succeeded con commit `adf8a66`
- Status "pending" durante horas
- Dockerfile no tenía `USER appuser`
- Fix: commit `638ff94` añadió `.dockerignore` + `USER appuser`

### Iteración 2 — Puerto desalineado
- Tras fix de root, URL pasó de 404 a 502 (mejor, contenedor arrancaba)
- NaN inyecta `PORT=4040` automáticamente (del Container Port configurado)
- El server.js tenía `PORT || '6060'` y el Dockerfile `EXPOSE 6060`
- El contenedor escuchaba en 4040 (por la env var) pero NaN esperaba en 6060
- Fix: alinear todo a 4040 (commit `ea98e6c`)

### Iteración 3 — Healthcheck con auth
- Tras fix de puerto, seguía 502
- El HEALTHCHECK apuntaba a `/api/summary` que requiere Basic Auth
- NaN healthcheck devolvía 401 → contenedor considerado unhealthy → reinicio en bucle
- Fix: crear endpoint público `/healthz` y apuntar healthcheck ahí (commit `9a4785c`)

### Lecciones
1. NaN bloquea contenedores root → siempre `USER appuser`
2. NaN inyecta `PORT=<container-port>` como env var → alinear EXPOSE, server default y NaN UI
3. Healthcheck necesita endpoint público sin auth → crear `/healthz` antes del middleware de auth
4. La progresión de códigos HTTP revela el problema: 404 (Cloudflare, no hay backend) → 502 (hay backend pero algo falla) → 200 (todo ok)