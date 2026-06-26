---
name: spa-architecture-audit
description: "Auditoría sistemática de aplicaciones web SPA monolíticas con JavaScript vanilla: detección de inline code, datos duplicados, lazy-loading roto, module boundaries incorrectas, deployment verification y architectural smells. Pensado para proyectos con ~10-50 archivos donde HTML, CSS y JS están mal distribuidos entre módulos."
version: 1.0.0
author: Hermes Agent
tags: [spa, architecture, audit, vanilla-js, quality, deployment]
---

# SPA Architecture Audit — Auditoría de Arquitectura SPA Vanilla JS

Procedimiento sistemático para auditar Single Page Applications vanilla JS que presentan **architectural smells** — código mezclado entre HTML/CSS/JS de forma que el proyecto es difícil de mantener.

## Cuándo usar

- Proyecto SPA vanilla JS (no framework) con ~5-50 archivos y el usuario dice "es una mierda", "está todo roto", "no se mantiene"
- `app.js` o archivo principal de orquestación es proporcionalmente diminuto respecto al HTML
- JavaScript inline masivo en `<script>` tags dentro de HTML
- CSS inline masivo en `<style>` tags
- Lazy-loading que no carga contenido real (skeletons perpetuos)
- Datos duplicados en múltiples funciones/archivos
- Usuario quiere auditar ANTES de refactorizar
- Proyecto deployado con error 404 / página en blanco

## Diferencia con `audit-html-project`

| `audit-html-project` | `spa-architecture-audit` |
|---|---|
| Proyectos educativos masivos (500+ archivos HTML) | SPAs pequeñas/medianas (5-50 archivos JS+HTML) |
| KaTeX, Plotly, navegación por niveles | Lazy-loading, inline code, data duplication |
| Enlaces rotos, atribuciones, navegación secuencial | Module boundaries, architectural smells, deployment |
| Batch fix con scripts Python | Análisis arquitectónico cualitativo + cuantitativo |

## Pasos

### 1. Inventario del proyecto

```bash
cd /path/to/project
echo "=== ARCHIVOS ==="
find . -not -path './.git/*' -not -path './node_modules/*' -type f | sort
echo ""
echo "=== TAMAÑOS ==="
find . -not -path './.git/*' -not -path './node_modules/*' -type f -exec wc -c {} + | sort -n | tail -20
echo ""
echo "=== JS LÍNEAS ==="
wc -l js/*.js js/modules/*.js 2>/dev/null
echo ""
echo "=== MAIN FILE ==="
wc -l index.html
```

**Métricas clave a observar:**
- ratio `index.html lines / app.js lines` — si index tiene 1000+ líneas y app.js tiene <50, **RED FLAG**
- Total JS files size vs HTML size
- Cuántos `<script src=` tags hay en el HTML (más de 10 = muchos módulos)
- Cuántos `<style>` blocks inline hay

### 2. Detección de inline code

**Inline CSS:**
```bash
# Contar bloques <style> en HTML
grep -c '<style' index.html
# Medir líneas de CSS inline
sed -n '/<style/,/<\/style>/p' index.html | wc -l
```

**Inline JS:**
```bash
# Bloques <script> sin src
grep -c '<script[^>]*>[^<]' index.html
# Líneas de JS inline (después de último <script src>)
awk '/<script src/{in_src=1} /<\/script>/{if(in_src) in_src=0} !in_src && /<script[[:space:]]*>{/{inline_start=1} inline_start && /<\/script>/{print NR; inline_start=0}' index.html
```

**Umbral de alertas:**
- >50 líneas de CSS inline → 🟡 Moderado
- >100 líneas de CSS inline → 🔴 Crítico
- >50 líneas de JS inline → 🟡 Moderado
- >150 líneas de JS inline → 🔴 Crítico

### 3. Detección de module boundaries incorrectas

Analizar qué funcionalidad está en cada archivo:

```bash
echo "=== index.html contiene lógica de negocio? ==="
grep -c 'function render\|function calcular\|function show\|var _' index.html | tail -1

echo "=== app.js real work ==="
grep -c 'function \|var \|const \|let \|window\.' app.js 2>/dev/null

echo "=== Funciones globales expuestas por módulo ==="
grep -rh 'window\.\|^function \|^var ' js/modules/*.js 2>/dev/null | grep -oP '\b\w+' | sort | uniq -c | sort -rn | head -20
```

**Pattern de smell: "Tiny orchestrator"**
- `app.js` < 30 líneas
- `index.html` > 500 líneas
- `modules/` con archivos de 200-1000+ líneas

→ El HTML está haciendo el trabajo de orquestación que debería hacer `app.js`

### 4. Detección de data duplication

```bash
# Detectar duplicación de datos entre módulos
# Buscar patrones de datos repetidos (arrays, objetos)
for f in js/modules/*.js; do
  echo "=== $(basename $f) ==="
  grep -n '^\s*var \|^\s*const \|^\s*let \|{\s*nombre:\|{\s*items:\|{\s*datos:\|{\s*CHECKLIST\|{\s*PLAZOS\|{\s*SOLVENCIA\|{\s*GLOSARIO\|{\s*ACTAS\|{\s*PROCEDIMIENTOS' "$f"
done
```

**Pattern de smell: "Data duplicated across files"**
- El mismo dato aparece en 2+ archivos (ej: checklistData y checklistDataForType devolviendo los mismos datos)
- Un módulo define arrays de datos y otro módulo redefine los mismos datos
- Se detecta comparando claves/IDs de datos entre archivos

### 5. Detección de lazy-loading incompleto

```bash
# Buscar función de tab switching y verificar callbacks registrados
grep -A 20 'function switchTab\|function cambiarTab\|function loadTab' index.html | grep -E 'case |render|load|init'
```

**Pattern de smell: "Skeleton perpetuo"**
- Tab content tiene `skeleton` placeholder HTML
- `switchTab()` tiene lazy-load pero NO tiene callback para esa tab
- El módulo existe (`modules/x.js`) pero su `renderX()` nunca se llama
- Resultado: el usuario ve skeleton forever cuando abre la tab

### 6. Detección de deployment issues

```bash
# Verificar configuración de Git
git remote -v
git branch -a
git log --oneline -3

# Verificar si hay .nojekyll (GitHub Pages)
ls -la .nojekyll 2>/dev/null

# Verificar si hay archivo CNAME
ls -la CNAME 2>/dev/null
```

**Checklist deployment:**
- ¿Hay `.nojekyll`? (necesario para GitHub Pages con JS)
- ¿La rama main tiene contenido?
- ¿Configuración de GitHub Pages apunta a la rama correcta?
- ¿Hay `CNAME` personalizado?

### 7. Análisis de arquitectura de módulos

Para cada módulo JS, verificar:
1. **Namespace pollution**: ¿expone funciones con `window.X = function()`? → Contamina global scope
2. **IIFE**: ¿usa `(function(){ ... })();` para encapsular? → Mejor práctica
3. **Dependencias implícitas**: ¿usa `window.LEY_DATA`, `window.showToast`, `window.switchTab`? → acoplamiento fuerte
4. **Tamaño**: >1000 líneas en un solo archivo → debe dividirse
5. **Responsabilidad única**: ¿un módulo hace 3 cosas diferentes? → debe separarse

```bash
# Verificar IIFE usage
for f in js/modules/*.js; do
  if grep -q '^\(function\|(\s*function' "$f"; then
    echo "✅ $(basename $f) usa IIFE"
  else
    echo "❌ $(basename $f) NO usa IIFE — polución global"
  fi
done

# Verificar dependencias implícitas (globals)
echo "=== Global dependencies ==="
grep -rh 'window\.\|window_\|window_\|typeof window\.' js/modules/*.js 2>/dev/null | grep -oP 'window\.\w+' | sort -u

# Verificar IIFE usage
for f in js/modules/*.js; do
  if grep -q '^\(function\|(\s*function' "$f"; then
    echo "✅ $(basename $f) usa IIFE"
  else
    echo "❌ $(basename $f) NO usa IIFE — polución global"
  fi
done

# Verificar dependencias implícitas (globals)
echo "=== Global dependencies ==="
grep -rh 'window\.\|typeof window\.' js/modules/*.js 2>/dev/null | grep -oP 'window\.\w+' | sort -u
```

### 8. Verificación de versionado inconsistente

```bash
# Buscar versiones en todo el proyecto
grep -rhn 'v[0-9]\.[0-9]\.[0-9]\|version.*=.*['\''"]' . --include='*.js' --include='*.html' --include='*.md' 2>/dev/null | grep -v '.git/'
```

**Smell:** Diferentes versiones en diferentes archivos (ej: app.js dice v0.2.0, index.html sidebar dice v0.1.0)

### 9. Verificación de error handling

```bash
# Buscar try/catch globales
grep -rhn 'try {' js/ --include='*.js' | wc -l

# Buscar console.log (o su ausencia)
grep -rhn 'console\.' js/ --include='*.js' | wc -l

# Buscar window.onerror
grep -rhn 'window.onerror\|window.addEventListener.*error' js/ --include='*.js'
```

**Smell:** Cero error handling global → cualquier fallo silencioso rompe la app

### 10. Reporte final

Clasificar hallazgos por severidad y crear plan de acción:

| Severidad | Criterio |
|-----------|----------|
| 🔴 Crítico | Deploy roto, inline JS >150 líneas, CSS inline >100 líneas, lazy-loading roto, duplicación de datos |
| 🟡 Moderado | app.js diminuto, namespace pollution, >1000 líneas en un módulo, versión inconsistente |
| 🟢 Funcional | Lógica de negocio correcta, datos legales precisos, funcionalidades útiles |

**Formato de salida:** Ver sección "Formato de salida" más abajo.

---

## Arquitectura de referencia para SPA vanilla JS

Este es el estado ideal al que aspirar:

```
proyecto/
├── index.html              ← ~200-400 líneas: estructura HTML limpia, sin JS/CSS inline significativo
├── css/
│   ├── custom.css          ← Todos los estilos custom (no Aurora/CDN)
├── js/
│   ├── app.js              ← Orquestador: router de tabs, init lifecycle, estado global, error handling
│   ├── ley-data.js         ← Datos puros (sin lógica)
│   ├── modules/
│   │   ├── tipos-contrato.js    ← IIFE, render + modal, datos + lógica
│   │   ├── generador-actas.js   ← Templates en datos, renderer en UI
│   │   ├── procedimientos.js    ← IIFE, datos + render
│   │   ├── calculadora-plazos.js
│   │   ├── umbral-presupuesto.js
│   │   ├── solvencia.js
│   │   ├── checklist-expediente.js
│   │   └── glosario.js
│   └── api.js              ← localStorage, fetch helpers, utilidades
└── data/
    └── ley-texto.json      ← Datos externos (si los hay)
```

**Reglas de module boundary:**
1. **index.html** = estructura HTML + CDN links + `<style>` mínimo (solo layout)
2. **app.js** = orquestación: tab router, init lifecycle, toast system, error handling global
3. **modules/x.js** = IIFE encapsulado, datos + lógica + render local. Expone SOLO si es necesario via `window.X = X`
4. **Datos puros** nunca contienen lógica de renderizado ni manipulación de DOM

---

## Common Architectural Smells (cheat sheet)

| Smell | Detección | Severidad | Fix |
|-------|-----------|-----------|-----|
| **Tiny orchestrator** | `wc -l app.js` < 30, `wc -l index.html` > 500 | 🔴 | Mover lógica inline a módulos |
| **Inline JS/CSS** | `grep -c '<script[^>]*>[^<]' index.html` | 🔴 | Mover a archivos externos |
| **Skeleton perpetuo** | `switchTab()` sin callback + skeleton HTML | 🔴 | Registrar callback en switchTab |
| **Data duplication** | Mismos IDs/keys en 2+ archivos | 🟡 | Unificar en archivo de datos |
| **Namespace pollution** | No IIFE, `window.X = function()` | 🟡 | Envolver en IIFE |
| **Module too large** | >1000 líneas en un módulo | 🟡 | Separar datos de UI |
| **Version mismatch** | Diferentes `vX.Y.Z` en archivos | 🟡 | Unificar |
| **No error handling** | Cero try/catch globales | 🟡 | Añadir global handler |

## Pitfalls

- **🔴 No confundir "proyecto grande" con "proyecto mal arquitecturado"** — Un proyecto educativo de 500+ HTML bien estructurados NO es un SPA con arquitectura rota. Son problemas distintos.
- **🔴 Los módulos pueden estar bien pero el sistema de lazy-loading puede estar roto** — Si `switchTab()` no llama a la función render, el módulo existe pero no se usa. Verificar el callback registration, no solo que el archivo exista.
- **🔴 No asumir que `app.js` vacío = problema** — En algunos proyectos el orquestador es mínimo y todo está en index.html (monolítico). El problema es cuando hay módulos en `modules/` que NUNCA se invocan.
- **🟡 El deploy puede estar roto por configuración de GitHub Pages, no por código** — Verificar branch configurado, .nojekyll, y que el contenido esté en la rama correcta ANTES de culpar al código.
- **🟡 Data duplication puede ser intencional** — Algunos patrones duplican datos para evitar mutaciones. Verificar si los duplicados tienen modificaciones independientes antes de marcarlo como bug.

## Formato de salida

El informe debe seguir este formato:

```markdown
# 🔍 AUDITORÍA [Nombre del Proyecto] — SPA Architecture Audit

**Proyecto:** [Descripción]
**Stack:** [ej: HTML vanilla + JS modules + Plotly.js]
**Archivos:** N total, M JS, N HTML

---

## 📊 RESUMEN

| Severidad | Hallazgos |
|-----------|-----------|
| 🔴 Críticos | N |
| 🟡 Moderados | N |
| 🟢 Positivos | N |

---

## 🔴 HALLAZGOS CRÍTICOS

### 1. [Título del hallazgo]
**Detección:** [Qué comando/verificación lo encontró]
**Líneas afectadas:** [archivo:linea]
**Impacto:** [Qué le pasa al usuario]
**Fix:** [Solución concreta]

---

## 🟡 HALLAZGOS MODERADOS

[Similar formato]

---

## 🟢 LO QUE FUNCIONA BIEN

[Bullet points positivos]

---

## 📋 PLAN DE ACCIÓN

### Fase 1 — Bloqueante (URGENTE)
1. [Acción]
2. [Acción]

### Fase 2 — Refactorización
1. [Acción]

### Fase 3 — Mejora
1. [Acción]

---

**Tiempo estimado de refactorización:** [X-Y horas]
```

**Regla:** SIEMPRE terminar con "¿Quieres que ponga mano al tornillo?" — el usuario quiere acción.

## Linked Files

- `references/contrata-publico-audit-2026-06-24.md` — Caso de estudio completo: ContrataPúblico, 10 módulos, lazy-loading roto, 600+ líneas JS inline, deploy 404
