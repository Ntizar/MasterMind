---
fecha: 2026-03-19
tarea: caedelcielo-multifile-sync
tipo: operaciones
complejidad: baja
clusters: [web]
proyecto: caedelcielo
patron: single-source-propagation
---

# Multi-file sync discipline en sitios estáticos con datos legales

## Decisión clave
Cuando un dato clave (CIF, email, URL, texto legal) aparece en múltiples archivos, existe una única fuente de verdad y un flujo de propagación estricto — nunca editar el destino directamente.

## Patrón reutilizable
sí → **single-source-propagation**

En proyectos web estáticos (sin CMS ni variables compartidas), los datos que deben ser idénticos en todos los archivos se gestionan así:
- **Fuente**: carpeta `webs/` (o equivalente) — aquí se edita
- **Deploy**: carpeta `deploy/` — solo recibe copias de la fuente, nunca ediciones directas
- Al cambiar cualquier dato en un archivo fuente, se buscan todas las ocurrencias en todos los demás archivos fuente y se propagan antes de copiar a deploy

## Qué funcionó
- Tratar `webs/*.html` y `blog/*.php` como la única fuente editable
- Buscar el dato a cambiar en todos los archivos antes de editar (grep/búsqueda global)
- Copiar a `deploy/` solo después de que todos los fuentes estén sincronizados
- Checkear footer, header, canonical, body text y meta tags — son los 5 lugares donde los datos legales suelen repetirse

## Qué evitar
- Editar `deploy/` directamente (se desincroniza de la fuente silenciosamente)
- Asumir que un dato solo aparece una vez — CIF, email y URLs suelen estar en header nav, footer y body
- Cambiar URLs de un subdominio sin buscar en todos los archivos (blog links aparecían en 5 ficheros distintos)

## Skills usados
- ninguno

## Tests/criterios que validaron esto
- Búsqueda grep de la URL antigua tras la migración no devolvía resultados en archivos fuente
- Revisión manual de footer en cada uno de los 5 archivos HTML/PHP fuente

## Conexiones
**Cluster:** #web
**Proyecto:** [[caedelcielo]]
**Aprendizajes relacionados:** [[2026-03-19-caedelcielo-subdomain-to-path]]
