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

## Pitfalls

1. **DB filename** no cambiar sin plan de migración. Mejor dejar el path viejo o crear symlink.
2. **CSV export** — el filename descargado usa el nombre del proyecto. Cambiarlo.
3. **Meta tags** — `<meta name="description">` y Open Graph tags.
4. **Console logs** — prefijo `[NOMBRE_APP]` en el server.
5. **Version bump** — subir de v4.0.1 a v5.0.0 si hay breaking changes.
6. **README** — reescribir completo, no solo buscar/reemplazar.
7. **Git commit** — mensaje clarissant que es rebranding + qué otros cambios incluye.
