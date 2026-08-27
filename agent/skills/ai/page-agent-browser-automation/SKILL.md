---
name: page-agent-browser-automation
version: "1.0.0"
description: "Page Agent — Agente GUI de Alibaba que vive en tu página web. Controla interfaces web con lenguaje natural desde JavaScript. Chrome extension + npm package."
tags: [browser-automation, agent, ai, gui, javascript, chrome-extension, web, mcp]
---

# Page Agent — Agente GUI para Navegador

## Resumen

[Page Agent](https://github.com/alibaba/page-agent) (⭐25K) de Alibaba es un agente de IA que vive DENTRO de la página web. Un script da a cualquier web su propio agente de IA que controla interfaces con lenguaje natural.

**Diferencia clave**: A diferencia de otros agentes que controlan el navegador externamente, Page Agent vive DENTRO del DOM — interactúa con elementos web directamente desde JavaScript.

## Cuándo usar

- Automatizar flujos de trabajo en páginas web existentes
- Crear asistentes IA que operen dentro de dashboards
- Automatización de formularios y flujos web
- Integrar IA en aplicaciones web existentes

## Patrón de uso

```bash
# Instalar como paquete npm
npm install page-agent

# O como Chrome extension
# Descargar desde Chrome Web Store
```

```javascript
// Como script inline en la página
import { PageAgent } from 'page-agent';

// Inicializar agente en la página actual
const agent = new PageAgent({
  instructions: "Ayuda al usuario a completar el formulario",
  llm: "claude",  // o "gpt", "gemini"
  mcp: true  // soporte MCP integrado
});

// El agente escucha comandos del usuario
agent.on("command", async (cmd) => {
  console.log("Comando:", cmd);
  // El agente ejecuta acciones en el DOM
});

// Ejemplo: "Haz clic en el botón de enviar"
// El agente encuentra el botón y lo hace clic
```

```javascript
// Como Chrome Extension
// La extensión inyecta el agente en cualquier página
// Controla elementos, lee contenido, navega por la web
```

## Features clave

| Feature | Descripción |
|---------|-------------|
| In-page agent | Vive dentro del DOM, no fuera |
| Natural language | Controla UI con lenguaje natural |
| Chrome Extension | Disponible como extensión |
| npm package | Usar como librería Node.js |
| MCP support | Soporte Model Context Protocol |
| Bundle < 50KB | Muy ligero (bundlephobia minzip) |

## Integración con otros skills

- **crawlee**: Complemento — Crawlee scrapear, Page Agent automatizar flujos interactivos
- **adaptive-web-scraping**: Scraping + Page Agent para flujos completos
- **ai-patterns**: Patrón de agentes IA en aplicaciones web

## Pitfalls

- **Solo funciona en páginas que lo cargan**: No es un agente universal — necesita inyectarse en la página
- **Limitaciones de seguridad**: CSP puede bloquear la inyección de scripts
- **Dependencias de LLM**: Necesita acceso a una API de LLM (Claude, GPT, etc.)
- **Chrome Web Store**: La extensión está en Chrome Web Store — verificar ratings y permisos

## Referencias
- Demo: https://alibaba.github.io/page-agent/
- Docs: https://alibaba.github.io/page-agent/docs/introduction/overview
- Chrome Extension: https://chromewebstore.google.com/detail/page-agent-ext/
- npm: https://www.npmjs.com/package/page-agent

---

**Hecho con ❤️ por David Antizar**