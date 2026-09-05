---
name: mcp-servers-modelcontextprotocol
description: "Usa a conectar servidores MCP activos con npx."
version: "2.0.0"
tags: [mcp, modelcontextprotocol, servers, npx, herramientas, agentes]
related_skills: [native-mcp, mcp-servers-modelcontextprotocol, hub-skill-discovery]
---

# Servidores MCP oficiales (activos) — instalación vía npx

> ⚠️ Corrección 2026-09-05 (auditoría): GitHub/GitLab/PostgreSQL/Slack/Google Drive/Puppeteer están **ARCHIVADOS** (movidos a `servers-archived`). Servidores de referencia **activos**: Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking, Time. Instalación: `npx -y @modelcontextprotocol/server-<name>`. Env var: `GITHUB_PERSONAL_ACCESS_TOKEN`.

**Repo:** `https://github.com/modelcontextprotocol/servers` (~90K⭐).

## When to Use

- Cuando conectes **servidores MCP** en Hermes/Claude (stdio/HTTP) y quieras los oficiales activos.

## Servidores de referencia ACTIVOS

- Everything · Fetch · Filesystem · Git · Memory · Sequential Thinking · Time

*(GitHub, GitLab, PostgreSQL, Slack, Google Drive, Puppeteer, etc. están archivados en `servers-archived` — referencia histórica.)*

## Instalación (npx)

```bash
npx -y @modelcontextprotocol/server-filesystem /ruta/a/servir
npx -y @modelcontextprotocol/server-fetch
```

Config (ej. Git):

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "<token>" }
    }
  }
}
```

## Pitfalls

- La env var es **`GITHUB_PERSONAL_ACCESS_TOKEN`**, no `GITHUB_TOKEN`.
- Instalación **`npx -y ...`**, no `git clone && npm install`.
- Los servidores de la v1 (GitHub/GitLab/PostgreSQL/Slack/Drive/Puppeteer) están archivados.

## Verificación

- `npx -y @modelcontextprotocol/server-fetch` y probar un tool en el cliente MCP.
