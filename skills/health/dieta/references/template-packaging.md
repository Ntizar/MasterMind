# Template Packaging — Procedimiento completo

Procedimiento para empaquetar un proyecto personal de dieta como template público para distribución.

## Ejemplo real: FitTrack (DietaNan)

**Fecha:** 2026-06-11
**Proyecto original:** `/root/workspace/dieta-masterfit/`
**Template creado:** `/root/workspace/dieta-template/`
**Repo público:** https://github.com/Ntizar/DietaNan
**GitHub Pages:** https://ntizar.github.io/DietaNan/

### Archivos del template (11 + 2 directorios)

```
dieta-template/
├── index.html              → Landing page (CSS puro, sin Aurora)
├── dashboard.html          → Dashboard interactivo (Chart.js + Aurora)
├── server.js               → Backend Express + APIs REST + Coach IA
├── package.json            → Solo Express.js
├── Dockerfile              → Deploy en NaN.builders
├── .gitignore              → Excluye .env y node_modules
├── .env.example            → Plantilla de config (sin tokens)
├── README.md               → Guía de instalación paso a paso
├── screenshot.png          → Captura del dashboard para landing
├── peso.sh                 → Atajo terminal
├── comida.sh               → Atajo terminal
├── deporte.sh              → Atajo terminal
├── data/
│   └── database.json       → Estructura vacía, lista para personalizar
└── scripts/
    └── registro.py         → CLI para registrar desde terminal
```

### Limpiar datos personales

**Método:** copiar original → reemplazar cadenas en lote → verificar con grep

```python
# Reemplazos necesarios:
"MasterFit" → "FitTrack"
"Amadeo Llados" → "Coach IA"
"David" → "Usuario" (en textos visibles)
"KoldoFit" → "FitTrack"
"Hecho con ❤️ por David Antizar" → "Hecho con ❤️ por tu nombre"

# NO reemplazar:
# Referencias CDN de Aurora (Ntizar/Aurora) → son públicas
# NTIZAR_API en server.js → es nombre de variable de entorno, no token
```

### Verificación de seguridad

**Escanear con grep:**
```bash
grep -rniE '(David|Ntizar|Amadeo|Koldo|antizar)' --include='*.js' --include='*.html' --include='*.md' .
```

**Falsos positivos aceptados:**
- `Ntizar/Aurora` en CSS → CDN público
- `NTIZAR_API` en server.js → nombre de variable, no contiene token
- Créditos al autor en README → intencional

**Falsos positivos NO aceptados:**
- `sk-[a-zA-Z0-9]{20,}` → API key real
- Nombres propios en database.json
- Emails

### Subir a GitHub via API

**Crear repo:**
```bash
curl -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"name":"DietaNan","description":"Dashboard de seguimiento de dieta con IA","public":true}' \
  https://api.github.com/user/repos
```

**Subir archivos (API Contents):**
```bash
# Para cada archivo:
curl -X PUT -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/json" \
  -d '{"message":"Add <filename>","content":"<base64_content>"}' \
  https://api.github.com/repos/Ntizar/DietaNan/contents/<filename>

# Para directorios: primero el archivo dentro, luego se crea implícitamente
```

**Squash commits (opcional):**
```bash
git clone https://$TOKEN@github.com/Ntizar/DietaNan.git
cd DietaNan
git reset --soft $(git rev-list --max-parents=0 HEAD)
git commit -m "FitTrack — Dashboard de seguimiento de dieta con IA"
git push --force origin main
```

### Activar GitHub Pages

```bash
curl -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/json" \
  -d '{"source":{"branch":"main","path":"/"}}' \
  https://api.github.com/repos/Ntizar/DietaNan/pages
```

**Estado:** `building` → `built` (1-3 minutos)
**URL:** `https://ntizar.github.io/DietaNan/`

Si devuelve 409: "GitHub Pages is already enabled" → ya está activo.

### Landing page — CSS puro vs Aurora

**Problema:** Aurora usa variables CSS (`--nz-space-16`, `--nz-c-accent`...) que no se definen en una landing page estática. Sin servidor Express, el CSS de Aurora no se carga correctamente en GitHub Pages.

**Solución:** CSS puro con variables propias en `:root`:
```css
:root {
  --blue: #2563eb;
  --orange: #f97316;
  --bg: #f8fafc;
  --card: #ffffff;
  --text: #0f172a;
  --radius: 16px;
}
```

**Estructura de la landing:**
1. Nav con logo + links
2. Hero con badges, título, descripción, botones CTA
3. Screenshot del dashboard en frame de navegador
4. Grid de feature cards (6 features)
5. CTA final
6. Footer con créditos

### README como guía de instalación

Debe incluir:
1. Qué es el proyecto (1 párrafo)
2. Qué incluye (lista de features)
3. Demo en vivo (link a GitHub Pages)
4. Guía de instalación paso a paso (10+ pasos)
5. Estructura del proyecto
6. Solución de problemas
7. Créditos

### GitHub Pages — API endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/repos/{owner}/{repo}/pages` | GET | Ver estado de Pages |
| `/repos/{owner}/{repo}/pages` | POST | Crear sitio (primera vez) |
| `/repos/{owner}/{repo}/pages` | PATCH | Actualizar configuración |

**Respuesta GET incluye:**
- `status`: "building" | "built" | "error" | "failed"
- `html_url`: URL pública del sitio
- `source.branch`: rama configurada
- `source.path`: ruta de origen

### Token de GitHub

Se almacena en `/hermes-home/.env` como `GITHUB_TOKEN`.
No usar `gh` CLI (no instalado). Usar curl con `-H "Authorization: token $TOKEN"`.
