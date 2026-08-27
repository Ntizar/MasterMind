---
name: mcp-servers-modelcontextprotocol
description: Model Context Protocol (MCP) Servers — catálogo completo de servidores oficiales y de la comunidad para integrar herramientas externas con LLMs.
category: mcp
---

# MCP Servers — Model Context Protocol

## Qué es

Repositorio oficial de servidores MCP de Model Context Protocol (Anthropic). Contiene servidores oficiales para:
- **Filesystem** — acceso a archivos locales
- **GitHub** — operaciones en repositorios
- **GitLab** — operaciones en GitLab
- **PostgreSQL** — consulta de bases de datos
- **Slack** — integración con Slack
- **Google Drive** — acceso a Drive
- **Puppeteer** — navegación web
- **Memory** — sistema de memoria persistente
- Y muchos más...

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/modelcontextprotocol/servers.git
cd servers

# Instalar dependencias
npm install

# Cada servidor se ejecuta como proceso independiente
# Ejemplo: servidor de filesystem
npx @modelcontextprotocol/server-filesystem /path/to/directory
```

## Uso con Hermes

Configurar en `config.yaml`:
```yaml
mcp:
  servers:
    filesystem:
      command: npx
      args: ["@modelcontextprotocol/server-filesystem", "/path/to/directory"]
    github:
      command: npx
      args: ["@modelcontextprotocol/server-github"]
      env:
        GITHUB_TOKEN: "tu-token"
```

## Patrones de uso

1. **Integrar herramientas externas** — cada servidor expone herramientas como si fueran nativas
2. **Sandboxing** — ejecutar servidores en contenedores para aislamiento
3. **Multi-tenant** — múltiples servidores MCP para diferentes contextos

## Pitfalls

- Los servidores se ejecutan como procesos independientes, no como librería
- Cada servidor tiene su propio ciclo de vida
- Los errores de conexión son silenciosos — verificar con `hermes mcp list`
- Algunos servidores requieren variables de entorno (tokens, URLs)
- El servidor de filesystem NO sigue symlinks por defecto

## Referencias

- Repo: `github.com/modelcontextprotocol/servers`
- Docs: `https://modelcontextprotocol.io`
- Hermes native MCP: `native-mcp`
