---
fecha: 2026-03-25
tarea: learning-platform-vercel-deploy
tipo: contenido
complejidad: media
clusters: [web, github, sistema]
proyecto: learning-platform
patron: static-deploy-with-downloadable-assets
---

# Learning Platform — Deploy en Vercel con activos descargables

## Decision clave
Desplegar la plataforma educativa en Vercel con enlaces reales de descarga a los archivos del sistema (AGENTS.md, session-prompt.md, _system-config.md).

## Patron reutilizable
Nombre: static-deploy-with-downloadable-assets
Descripcion: Para plataformas educativas que necesitan ofrecer archivos descargables:
1. Copiar archivos al directorio de build
2. Usar enlaces con atributo `download` en HTML
3. Deploy con Vercel CLI: `vercel --prod --yes`
4. Verificar todos los endpoints con curl o webfetch

## Que funciono
- Dividir contenido grande en micro-cambios (modelos de baja latencia)
- Enlaces reales `href='archivo.md' download` vs alertas JavaScript
- Deploy en una tirada con Vercel CLI autenticado
- Módulo 4 simplificado a 4 pasos claros

## Que evitar
- No compartir API keys en texto plano (siempre rotar si se expone)
- No hardcodear rutas absolutas en archivos del sistema
- No usar `href="#" onclick='alert()'` para descargas reales
- No intentar reescrituras completas con modelos limitados

## Archivos modificados
- modules.json (M4 y M5 actualizados)
- vercel.json (creado para deploy)
- AGENTS.md, session-prompt.md, _system-config.md (copiados para descarga)
- agents/*.md (copiados para descarga)

## URL de produccion
https://learning-platform-roan-six.vercel.app

## Senal de relevancia
Cuando necesites desplegar contenido educativo estático con archivos descargables en Vercel.

## Conexiones
[[learning-platform]] [[vercel-deploy]] [[static-assets]] [[educational-content]]
