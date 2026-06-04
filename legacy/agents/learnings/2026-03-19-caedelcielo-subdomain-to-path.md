---
fecha: 2026-03-19
tarea: caedelcielo-subdomain-to-path
tipo: software
complejidad: media
clusters: [web, github]
proyecto: caedelcielo
patron: subdomain-to-path-apache
---

# CAE del Cielo — Migración de subdominios a rutas de path

## Decisión clave
Eliminar todos los subdominios de contenido (blog, privacidad, cookies, avisolegal) y servirlos como subcarpetas bajo el dominio raíz en Apache/shared hosting (Raiola Networks).

## Patrón reutilizable
sí → **subdomain-to-path-apache**

Cuando un sitio en shared hosting Apache (Raiola u otro) tiene páginas en subdominios separados y se quiere consolidar bajo un único dominio con rutas `/seccion/`, el patrón es:
1. Crear subcarpetas en `deploy/[dominio]/[seccion]/`
2. Poner `index.html` o `index.php` en cada subcarpeta
3. En el `.htaccess` del dominio raíz añadir declaración explícita de PHP y DirectoryIndex
4. Actualizar todos los enlaces internos y canonicals en los archivos fuente

## Qué funcionó
- Añadir en `.htaccess` raíz:
  ```apache
  <IfModule mime_module>
      AddType application/x-httpd-php .php
  </IfModule>
  <IfModule mod_dir.c>
      DirectoryIndex index.php index.html index.htm
  </IfModule>
  ```
  Esto es necesario en Raiola shared hosting para que PHP funcione en subdirectorios
- Mantener `forms.caedelcielo.com` como subdominio separado (formularios con JotForm tienen lógica propia, no mover)
- `git add .` detecta renames correctamente cuando las carpetas se mueven dentro del mismo repo
- Editar siempre los archivos fuente (`webs/`, `blog/`) y luego copiar a `deploy/` — nunca editar `deploy/` directamente

## Qué evitar
- No editar archivos en `deploy/` directamente; siempre editar en la fuente y propagar
- No asumir que PHP funciona en subdirectorios sin declararlo en `.htaccess` en shared hosting
- No mover subdominios que tienen lógica de terceros (JotForm, formularios embebidos) sin validar primero

## Skills usados
- Software Development Universal

## Tests/criterios que validaron esto
- `git status` mostraba renames correctos (no delete + create)
- `git push` sin errores a `origin/master`
- Estructura `deploy/caedelcielo.com/` con subcarpetas `blog/`, `privacidad/`, `cookies/`, `avisolegal/` verificada

## Conexiones
**Clusters:** #web · #github
**Proyecto:** [[caedelcielo]]
**Aprendizajes relacionados:** [[2026-03-19-caedelcielo-multifile-sync]]
