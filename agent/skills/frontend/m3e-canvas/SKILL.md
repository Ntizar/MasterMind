---
name: m3e-canvas
description: "Usa al sketchear Material 3 y sacar prompt de AI coding."
version: "1.0.0"
author: "Web clonada de lnkiai/m3e-canvas"
license: "MIT"
tags: [frontend, design-tool, material3, vibe-coding, browser-local, prompt]
related_skills: [browser-local-tools, claude-design, design-md, sketch, popular-web-designs]
---

# M3E Canvas — sketch Material 3 → prompt de AI coding

## Qué es

Tipo de **diseñador en el navegador, sin backend**: dibujas pantallas de una app, las enlazas para navegar entre ellas, las retemas (Material 3 Expressive) y copias un **prompt listo para pegarlo en una herramienta de AI coding** (Codex, Claude Code, etc.), que construye la app.

- **Repo original:** `https://github.com/lnkiai/m3e-canvas` (3.6K⭐, MIT) · **Demo:** `https://lnkiai.github.io/m3e-canvas/`
- **Stack:** Next.js 16 + React 19 + TypeScript + Tailwind + `motion` + `html-to-image` + Vitest.
- **Dato clave:** **No tiene backend** — todo vive en `localStorage`. Es un artefacto 100% estático desplegable en GitHub Pages.

## Cuándo usarlo

Cuando David pida:
1. Un **tool de diseño en el navegador** para prototipar pantallas sin código y de ahí sacar un prompt para la IA.
2. Algo tipo "sketch → APP" (vibe-coding): dibujar UI, retemarla, y generar el prompt de construcción.
3. Un **browser-local tool** que funcione sin servidor (patrón `browser-local-tools`).

## Flujo del patrón (lo realmente reutilizable)

1. **Canvas de sketching**: un área donde se colocan pantallas/tarjetas arrastrables (interacción táctil-first, estilo `webapp-movil-first`).
2. **Enlazar pantallas**: flechas/clicks para navegar entre vistas (proto-flow navegable).
3. **Retema Material 3 Expressive**: sistema de colores/tipografía dinámicos al estilo Material Design (paleta heredada de Material 3, "Expressive").
4. **Exportar prompt**: serializa el estado (pantallas + tema + acciones) a un **texto de prompt autocontenido** que un modelo de coding puede ejecutar.
5. **Sin estado de servidor**: persiste en `localStorage`; no hay DB ni auth.

## Integración con Mastermind

- Es un **skill de referencia/tool**, no un workflow que Mastermind ejecute de serie. Añádelo como entrada al ecosistema `browser-local-tools` cuando David pida "herramienta que genera prompts desde un sketch".
- No sustituye a `claude-design` (diseño de artefactos HTML) ni a `design-md` (specs DESIGN.md): M3E Canvas es un **artefacto concreto** que puedes clonar como base si David quiere su propio sketch-tool.

## Pitfalls

- Depende de `motion` y `html-to-image` para exportar la previsualización a imagen — si clonas y lo simplificas, esos dos son los puntos de fuga de "visto bonito pero se rompe".
- El prompt exportado es para **tools de AI coding externas**, no directamente para Hermes: si se reutiliza, adaptar el prompt al contexto del proyecto.
- Está en web estándar; si se importa a un repo JS nativo no hace falta normalizar saltos.

## Verificación

- En local clonado: `npm install && npm run dev` (o `--build` para Pages). El demo publicado genera un prompt que, pegado en Codex/Claude Code, produce una app funcional — ese es el test de humo.
