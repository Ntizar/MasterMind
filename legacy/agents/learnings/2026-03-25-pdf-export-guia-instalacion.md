---
fecha: 2026-03-25
tarea: pdf-export-guia-instalacion
tipo: software
complejidad: media
clusters: [sistema, web]
proyecto: learning-platform
patron: one-page-pdf-export
---

# Learning Platform v2 — Export a PDF con Guía de Instalación

## Decisión clave
Reemplazar export JSON por PDF de 1 página con: nombre del usuario, perfil, pasos de instalación esenciales, y QR para volver a la plataforma. Usar jsPDF desde CDN.

## Patrón reutilizable
**Nombre:** one-page-pdf-export
**Descripción:** Para plataformas educativas: generar PDF compacto (1 página) con (1) datos del usuario, (2) pasos esenciales, (3) QR code, (4) recursos clave. Usar jsPDF + jsPDF-AutoTable desde CDN, sin backend.

## Qué funcionó
- jsPDF desde CDN (sin build step)
- PDF estructurado: header con logo, secciones claras, footer con QR
- Contenido útil: pasos de instalación, no solo stats
- QR code apunta a la plataforma Vercel

## Qué evitar
- No hacer PDF de múltiples páginas — solo 1 página
- No incluir todo el progreso — solo lo esencial para empezar
- No usar librerías pesadas — jsPDF es suficiente

## Skills usados
- software-dev.md (integración de librerías desde CDN)

## Criterios que validaron el éxito
- Botón "Exportar Guía PDF" en finish modal
- PDF se descarga automáticamente
- 1 página, <500KB
- Incluye: nombre, perfil, 4 pasos de instalación, links, QR

## Contexto de la tarea
- Flujo ejecutado: orchestrator → implementer → archiver
- Reintentos necesarios: ninguno
- Tiempo estimado: medio (~15min)

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-25-platform-v2-simplificado-robusto]]
