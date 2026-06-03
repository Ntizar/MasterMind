---
nombre: Web Deploy Shared Hosting
tipo: skill
clusters: [web, github]
aplica_a: deploy, migración
creado: 2026-03-19
---

# Skill: Web Deploy — Sitios Estáticos y PHP en Shared Hosting

## Aplica cuando
- La tarea implica desplegar o migrar un sitio web a shared hosting (Raiola, cPanel, etc.)
- Hay múltiples páginas con datos legales compartidos (CIF, email, URLs)
- La estructura de URLs cambia (subdominios → paths, o reorganización de carpetas)
- El proyecto tiene archivos fuente (`webs/`, `blog/`) separados del paquete de deploy (`deploy/`)

---

## Fases universales

1. **Audit de fuentes** — Identificar todos los archivos fuente y listar todos los datos que aparecen en más de un lugar (URLs, CIF, email, textos legales). No tocar nada todavía.

2. **Edición en fuente** — Hacer todos los cambios en los archivos fuente (`webs/`, `blog/`). Nunca editar `deploy/` directamente. Usar búsqueda global para encontrar todas las ocurrencias de cada dato antes de editar.

3. **Propagación a deploy** — Copiar los archivos fuente editados a la estructura de `deploy/`. Verificar que `deploy/` refleja exactamente la fuente — no tiene ediciones propias.

4. **Verificación de `.htaccess`** — En shared hosting Apache, confirmar que el `.htaccess` del dominio raíz tiene las directivas necesarias para PHP en subdirectorios y DirectoryIndex correcto.

5. **Commit y push** — `git add .` (no parcial) para que Git detecte renames. Commit con mensaje descriptivo del cambio estructural. Push a remote.

---

## Decisiones clave

| Pregunta | Por qué es bloqueante |
|----------|-----------------------|
| ¿Qué subdominios o rutas se mantienen sin cambios? | Si se mueve algo que no debía moverse (ej. forms con JotForm), el formulario deja de funcionar |
| ¿Cuál es la carpeta fuente y cuál es deploy? | Confundirlas produce desincronización silenciosa |
| ¿El hosting necesita declaración explícita de PHP en subdirectorios? | En Raiola/shared hosting sí — sin esto, PHP no ejecuta en subcarpetas |
| ¿Hay datos legales (CIF, email, URLs) en más de 3 archivos? | Si sí, hay que hacer grep global antes de editar para no dejar archivos desincronizados |

---

## Reglas
- Edita siempre en la fuente, nunca en deploy
- Antes de cambiar cualquier URL o dato legal, haz grep global para encontrar todas las ocurrencias
- En Apache shared hosting, declara explícitamente PHP y DirectoryIndex en `.htaccess` del dominio raíz cuando uses subdirectorios con PHP
- Mantén separados los subdominios con lógica de terceros (JotForm, servicios externos) — no los muevas sin validar primero
- Usa `git add .` completo para que Git detecte renames como renames, no como delete+create

---

## Patrones preferidos
- **single-source-propagation**: `webs/` es la única fuente editable; `deploy/` solo recibe copias
- **subdomain-to-path-apache**: para consolidar subdominios bajo rutas, crear subcarpetas en deploy + declarar PHP en `.htaccess` raíz
- **grep-before-edit**: buscar el dato a cambiar en todos los archivos antes de modificar ninguno

---

## Anti-patrones (nunca hacer)
- Editar `deploy/` directamente — se desincroniza de la fuente y el error no es visible hasta el siguiente deploy
- Asumir que un dato (URL, CIF, email) solo aparece en un archivo — en sitios con header/footer compartido están en al menos 5 lugares
- Hacer `git add [archivo específico]` en migraciones de carpetas — Git no detecta los renames y el historial se rompe
- Mover un subdominio con servicios de terceros embebidos sin verificar que el servicio acepta el nuevo origen

---

## Creado
Fecha: 2026-03-19
Revisado: —
Origen: caedelcielo-deploy — migración de subdominios a path-based routing en Raiola Networks
