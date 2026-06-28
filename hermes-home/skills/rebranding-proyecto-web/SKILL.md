---
name: rebranding-proyecto-web
description: >
  Patrón sistemático para hacer rebranding de un proyecto web completo:
  búsqueda y reemplazo en HTML, JS, server, README, Docker, favicon.
  Incluye checklist y verificación post-cambio.
version: "1.0.0"
tags:
  - rebranding
  - rename
  - checklist
  - html
  - nodejs
---

# Rebranding de Proyecto Web

Checklist sistemático para renombrar un proyecto completo.

## Pasos

### 1. Búsqueda de referencias
```bash
grep -rni "NOMBRE_VIEJO" --include="*.js" --include="*.html" --include="*.json" --include="*.md" --include="*.yml" --include="*.yaml" --include="Dockerfile" .
```

### 2. Archivos a revisar (en orden)
1. **README.md** — título, descripción, links
2. **package.json** — name, description
3. **HTML** — `<title>`, headings, header, footer, meta tags
4. **JS** — comments, console.log prefixes, download filenames
5. **Server** — DB path, CORS origin, meta tags
6. **Dockerfile** — labels, EXPOSE comments
7. **CSS** — comment headers
8. **.env** — variable names si aplican
9. **GitHub** — repo name, description, topics

### 3. Reemplazo
```bash
# En HTML/JS/MD:
sed -i 's/OldName/NewName/g' file.html

# Pero cuidado con:
# - URLs que contienen el nombre (cambiarlas solo si el repo cambió)
# - DB filenames (requieren migración o symlink)
# - CSV export filenames (cambiar solo el prefijo)
```

### 4. Verificación
```bash
# Syntax check
node -c server.js
python3 -c "
with open('dashboard.html') as f: c = f.read()
s = c[c.index('<script>',300)+8:c.index('</script>')]
with open('/tmp/check.js','w') as f: f.write(s)
" && node -c /tmp/check.js

# Brace balance
python3 -c "
for f in ['server.js','dashboard.html']:
    c=open(f).read()
    o,cl=c.count('{'),c.count('}')
    print(f'{f}: {o}/{cl} balanced={o==cl}')
"
```

## Conversión a Design System corporativo

Cuando el usuario pide convertir un proyecto a un design system existente (Kaizen, Aurora, etc.), seguir este flujo:

### Flujo de conversión

1. **Localizar el CSS del design system** — buscar en `/root/workspace/<nombre-design-system>/` o en CDN. No asumir rutas.
2. **Leer el CSS completo** — entender variables (`--kz-*`, `--nz-*`), clases disponibles y reglas de uso.
3. **Mapear CSS actual → clases del DS** — crear tabla de correspondencias antes de tocar código:
   - Variables CSS custom → tokens del DS
   - Clases custom → clases del DS
   - Colores hardcodeados → paleta del DS
4. **Sustituir el `<style>` block** — linkar el CSS del DS y reducir el CSS custom al mínimo (solo layout/posición que el DS no cubre).
5. **Alias de compatibilidad** — si el JS referencia variables CSS antiguas (ej: `--azul`), crear aliases: `:root { --azul: var(--kz-azul); }`
6. **Preservar JavaScript intacto** — NUNCA modificar la sección `<script>`. Solo cambiar CSS y clases HTML.
7. **Backup** — guardar `index.html.bak` antes de modificar.

### Pitfall crítico: rutas relativas CSS al delegar

Cuando se delega la conversión a un subagente, **SIEMPRE verificar la ruta relativa del CSS linkado**. Los subagentes calculan mal las rutas relativas entre directorios que no son hermanos directos.

```bash
# Verificar ruta correcta:
# Si visor está en /workspace/proyecto/visor/index.html
# Y CSS está en /workspace/design-system/kds.css
# La ruta correcta es ../../design-system/kds.css (subir 2 niveles)
grep -n "design-system" /workspace/proyecto/visor/index.html
```

**Regla:** Si el CSS no carga, abrir DevTools → Network → ver si el CSS da 404. Es el error más común post-conversión.

### ⚠️ Solución definitiva: copiar CSS local (2026-06-25)

**Las rutas relativas a CSS externo SIEMPRE dan problemas** — cuando el usuario abre el HTML directamente (doble clic, file://), cuando lo sirve un subdirectorio diferente, cuando otro usuario lo clona a otro sitio. En vez de calcular rutas frágiles:

**COPIAR el CSS del design system al directorio del proyecto:**
```bash
cp /root/workspace/kds/kds.css /root/workspace/proyecto/visor/kds.css
```
Y linkarlo localmente:
```html
<link rel="stylesheet" href="kds.css">
```

**Ventajas:**
- Funciona siempre, sin importar cómo se abra el archivo
- Sin dependencia de estructura de directorios externa
- El proyecto es autocontenido
- Sin 404s en Network tab

**Desventaja:** si el CSS del DS se actualiza, hay que copiar de nuevo. Pero eso es mejor que un CSS roto.

### Standalone HTML para apertura directa (2026-06-25)

Incluso con el CSS copiado localmente, hay casos donde el usuario abre el HTML directamente (doble clic, arrastra al navegador) y espera que funcione sin servidor. Para esos casos, crear un **`index-standalone.html`** con el CSS embebido inline:

```python
# Script para generar standalone
with open('index.html') as f: html = f.read()
with open('kds.css') as f: css = f.read()
html = html.replace('<link rel="stylesheet" href="kds.css">', '<style>\n' + css + '\n</style>')
with open('index-standalone.html', 'w') as f: f.write(html)
```

**Resultado:** dos archivos en el repo:
- `index.html` → versión normal (referencia CSS local)
- `index-standalone.html` → autocontenido, funciona al abrir directamente

**Cuándo usar:** cuando el usuario va a compartir el HTML (email, chat, USB) o lo abre sin servidor local.

### Verificación post-conversión

1. Abrir en navegador → verificar que el CSS carga (no 404 en Network)
2. `grep -c "kz-\|nz-\|ds-" index.html` → debe haber referencias al DS
3. `grep -c "function " index.html` → JS intacto
4. Consola del navegador → 0 errores JS
5. Probar funcionalidad principal (clics, formularios, carga de datos)

## Pitfalls

1. **CSS externo → copiar local** — NO usar rutas relativas a CSS de otros directorios. Copiar el CSS al directorio del proyecto y linkarlo localmente. Las rutas relativas rompen cuando el HTML se abre directamente (file://), se sirve desde otro contexto, o otro usuario lo clona.
2. **DB filename** no cambiar sin plan de migración. Mejor dejar el path viejo o crear symlink.
3. **CSV export** — el filename descargado usa el nombre del proyecto. Cambiarlo.
4. **Meta tags** — `<meta name="description">` y Open Graph tags.
5. **Console logs** — prefijo `[NOMBRE_APP]` en el server.
6. **Version bump** — subir de v4.0.1 a v5.0.0 si hay breaking changes.
7. **README** — reescribir completo, no solo buscar/reemplazar.
8. **Git commit** — mensaje claro que es rebranding + qué otros cambios incluye.
