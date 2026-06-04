---
nombre: Caedelcielo
alias: caedelcielo
tipo: proyecto
clusters: [web, github]
repo_local: C:\Ntizar_Obsidian\Ntizar_Brain\Github\Caedelcielo
estado: activo
---

# Caedelcielo

Sitio web corporativo de la empresa CAE del Cielo. Incluye landing principal, formularios de contacto y blog. Desplegado en shared hosting Apache (Raiola Networks).

## Stack
- HTML5 + CSS3 (sin frameworks)
- PHP (blog y páginas legales)
- Apache shared hosting (Raiola Networks)
- JotForm (formularios — subdominio separado)
- Git para control de versiones

## Estructura del proyecto
```
Caedelcielo/
├── webs-source/     ← fuente editable (NUNCA editar deploy directamente)
├── blog/            ← fuente del blog PHP
├── deploy/          ← paquete listo para subir al hosting
├── branding/        ← assets de marca
└── webs/            ← versiones publicadas
```

## Decisiones arquitectónicas permanentes
- `webs-source/` y `blog/` son la única fuente editable
- `deploy/` solo recibe copias — nunca editar directamente
- Subdominios de contenido migrados a paths (`/blog`, `/privacidad`, `/cookies`, `/avisolegal`)
- `forms.caedelcielo.com` se mantiene como subdominio separado (JotForm — no mover)
- PHP en subdirectorios requiere declaración explícita en `.htaccess` raíz (Raiola shared hosting)
- Antes de cambiar cualquier dato (CIF, email, URL legal): grep global en todos los fuentes

## Regla de sincronización
Cuando se corrige un dato en cualquier archivo fuente, propagarlo inmediatamente a todos los demás antes de copiar a deploy. Los datos críticos (CIF, email, URLs) aparecen en header, footer, body y meta tags — mínimo 5 ubicaciones.

## Learnings de este proyecto
- [[2026-03-19-caedelcielo-subdomain-to-path]]
- [[2026-03-19-caedelcielo-multifile-sync]]
