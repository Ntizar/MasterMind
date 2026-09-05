---
name: opencut
description: "Usa al editar vídeo open-source con OpenCut (CapCut alt)."
version: "2.0.0"
tags: [video-editor, opencut, capcut, web, rust, moon, edicion-video]
related_skills: [video-processing, video-use-agentic-editing, hyperframes-html-video, agentic-video-pipeline]
---

# OpenCut — editor de vídeo open-source (alternativa a CapCut)

> ⚠️ Corrección 2026-09-05 (auditoría): la v1 lo describía como "editor de documentos/texto con IA" con API npm `import { OpenCut }` y `editor.ai.*`. **Falso.** Es un **editor de VÍDEO** open-source (alternativa a CapCut) para web/desktop/móvil, con core en Rust y build vía proto/moon.

**Repo:** `https://github.com/OpenCut-app/OpenCut` (TypeScript + Rust, ~89K⭐).

## When to Use

- Cuando pidas **editar vídeo** en el navegador/desktop/móvil con una alternativa open-source a CapCut (timeline, cortes, efectos).

## Qué es

`A free and open source video editor for web, desktop, and mobile` / `The open-source CapCut alternative`. **No es una librería npm** ni un editor de documentos.

## Uso (build / development)

- Proyecto gestionado con **proto + moon**; la web se arranca con `moon run web:dev`.
- El proyecto está en reescritura activa — la versión utilizable actual vive en **`opencut-classic`**.
- **No existe** `npm install opencut` ni `npm run build` para usarlo como librería.

## Pitfalls

- **No** hay `import { OpenCut } from 'opencut'`, ni `new OpenCut({container, ai:{...}})`, ni `editor.ai.summarize()`/`editor.export("pdf")` — todo eso es inventado.
- Es un **editor de vídeo**, no de documentos.
- Build: `moon run web:dev` (proto/moon), no `npm run build` genérico.

## Verificación

- Abrir la web de dev (`moon run web:dev`) y comprobar que carga un timeline de edición de vídeo (no un editor de texto).
