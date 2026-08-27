# Caso de Estudio: ContrataPúblico (2026-06-24)

Proyecto: Herramienta web para Ley 9/2017 de Contratos del Sector Público
Stack: HTML vanilla + Aurora Design System (CDN) + Plotly.js + localStorage
Deploy: GitHub Pages (roto — 404)

## Estructura Real vs Esperada

### Estructura real:
```
index.html              → 1119 líneas (931 HTML + 209 JS inline)
app.js                  → 14 líneas (casi vacío)
ley-data.js             → datos de la ley
modules/
  generador-actas.js    → 1074 líneas (MÓDULO MÁS COMPLEJO)
  checklist-expediente.js → 526 líneas (con duplicación masiva)
  procedimientos.js     → 252 líneas
  calculadora-plazos.js → 250 líneas
  umbral-presupuesto.js → 227 líneas
  solvencia.js          → 229 líneas
  glosario.js           → 169 líneas
css/custom.css          → probablemente vacío
data/ley-texto.json     → texto completo de la ley
```

### Estructura esperada:
```
index.html              → ~200-400 líneas (estructura limpia)
app.js                  → ~200-300 líneas (orquestador real)
modules/tipos-contrato.js → 200 líneas (datos + render + modal)
modules/generador-actas.js → 400 líneas (solo lógica de generación)
modules/generador-actas-templates.js → 600 líneas (solo templates)
...
```

## Hallazgos Clave

### 1. Tiny Orchestrator (🔴 Crítico)
- `app.js` tiene 14 líneas de código real
- `index.html` tiene 209 líneas de JavaScript inline (funciones de tipos de contrato, radar, modal)
- El HTML está haciendo el trabajo de orquestación

### 2. Inline Code (🔴 Crítico)
- 205 líneas de CSS en `<style>` tag
- 189 líneas de JavaScript en `<script>` tag
- `css/custom.css` probablemente vacío

### 3. Lazy-Loading Roto (🔴 Crítico)
- `switchTab()` registra callbacks SOLO para 'mapa' y 'texto'
- Las tabs 2-10 tienen skeleton HTML pero nunca se llama a su función render
- Resultado: skeletons perpetuos

### 4. Data Duplication (🟡 Moderado)
- `checklist-expediente.js`: `checklistData` y `checklistDataForType()` devuelven los mismos datos
- Duplicación de ~140 líneas de datos idénticos

### 5. Module Too Large (🟡 Moderado)
- `generador-actas.js` tiene 1074 líneas: mezcla templates, lógica de generación, y renderizado
- Debería separarse en templates + renderer

### 6. Version Mismatch (🟡 Moderado)
- `app.js` dice v0.2.0
- `index.html` sidebar dice v0.1.0

### 7. Deployment Broken (🔴 Crítico)
- GitHub Pages devuelve 404
- No se puede determinar la causa exacta sin acceso a settings

### 8. No Error Handling (🟡 Moderado)
- Cero error handling global
- `try/catch` solo en localStorage
- Si `LEY_DATA` no está definido, todo se cae silenciosamente

## Lecciones Aprendidas

1. **Los módulos pueden existir pero no usarse** — Tener 8 archivos en `modules/` no significa que se usen. Verificar que `switchTab()` registra callbacks para TODAS las tabs.
2. **El tamaño de app.js es un indicador clave** — Si app.js es diminuto y index.html es enorme, hay inline code que debe moverse.
3. **Los datos duplicados son difíciles de detectar con grep** — Requieren análisis semántico (comparar IDs, claves, estructura).
4. **El deploy puede estar roto por configuración, no por código** — Siempre verificar settings de GitHub Pages antes de culpar al código.
5. **Un proyecto puede tener buen contenido pero mala arquitectura** — El contenido legal de ContrataPúblico está bien pensado (actas, checklist, solvencia), pero la implementación es un desastre arquitectónico.
