---
name: maple-observability
description: "Usa a observar apps con Maple observability."
version: "2.0.0"
tags: [observabilidad, maple, open-source, logging, tracing, self-host]
related_skills: [maple-observability, devops-operations]
---

# Maple — observabilidad open-source (arquitectura real)

> ⚠️ Corrección 2026-09-05 (auditoría): el repo tiene `apps/ios` (SwiftUI nativo, Clerk + v2 API), no `apps/mobile` (Expo); además `apps/landing` (Astro) y `apps/electric-sync`. Comandos: `bun dev` y `docker compose -f docker-compose.yml up --build`.

**Repo:** `https://github.com/MapleTechLabs/maple` (TypeScript, ~1.8K⭐). (`Makisuo/maple` redirige aquí.)

## When to Use

- Cuando pidas **observabilidad open-source** (logs, tracing, métricas) para una app, self-hosted.

## Qué es

Plataforma de observabilidad open-source. Monorepo con apps web/mobile/nativo:
- `apps/ios` — app nativa **SwiftUI** (Clerk + v2 API)
- `apps/landing` — Astro
- `apps/electric-sync` — sync
- *(no hay `apps/mobile` Expo)*

## Uso

```bash
bun dev                                    # (no bun run dev)
docker compose -f docker-compose.yml up --build
```

## Pitfalls

- App móvil: **`apps/ios` (SwiftUI)**, no Expo/mobile.
- Dev: **`bun dev`**; Docker: **`docker compose -f docker-compose.yml up --build`**.
- Repo real: **MapleTechLabs/maple**.

## Verificación

- `bun dev` y abrir la UI; o `docker compose -f docker-compose.yml up --build`.
