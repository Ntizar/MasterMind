---
name: personal-archive-sqlite-mcp
version: "1.0.0"
description: "Usa para archivar historial de Twitter/X en SQLite y MCP."
tags: [sqlite, twitter, archive, mcp, local-first]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [sqlite, twitter, archive, mcp, local-first]
    related_skills: [native-mcp, batch-file-download]
---
# Birdclaw — Archivo personal de Twitter/X en SQLite (Local-first + MCP)

## Resumen
`Birdclaw` importa archivos de Twitter/X en SQLite local, añade lecturas en vivo cacheadas, y expone el resultado vía web app, CLI y un servidor MCP **solo lectura** opcional. Para gente que quiere su propio historial buscable, DMs, posts guardados y grafo de seguidos sin backend cloud.

## Uso (comandos reales del README)

```bash
# Instalación
brew install steipete/tap/birdclaw          # macOS/Linux
npm install -g birdclaw                       # alternativa npm

# Quick start demo
birdclaw init --demo
birdclaw search tweets "local-first" --limit 3 --json
birdclaw serve
# abrir http://localhost:3000

# Usar tu propio archivo
birdclaw import archive ~/Downloads/twitter-archive.zip --json
```

## Patrones / Arquitectura
- Importa tweets, DMs, likes, bookmarks, perfiles, media y edges de follow a SQLite local.
- Imports idempotentes que mergean filas destino-only.
- Web app, CLI, y servidor MCP read-only opcional.
- Backend sin cloud: TODO local (searchable history, DMs, saved posts, follow graph).
- El demo (`--demo`) seedea tweets, DMs, perfiles y links sin credenciales ni requests de red.

## Pitfalls
- Node público `>=26.5.1 <27`; toolchain de fuente usa Bun 1.4.0-canary.1 pinneado con checksum (Node como lane de compatibilidad testeada).
- `birdclaw serve` abre en `http://localhost:3000`.
- Para archivos reales usar `birdclaw import`; el demo no requiere credenciales.

## Verificación
- `birdclaw search tweets "local-first" --limit 3 --json` devuelve los tweets del demo.
- `birdclaw serve` abre `http://localhost:3000` con la Home timeline local.

## Referencia
README de https://github.com/steipete/birdclaw. Docs: birdclaw.sh. npm: birdclaw. Homebrew tap: steipete/tap.
