---
name: lieflat-charts-dataviz
description: "Use al convertir datos en gráficos HTML editoriales."
version: "1.0.0"
author: "David Antizar (Ntizar) — vía stars-explorer"
license: "Ver licencia del repo original (NOASSERTION antes de redistribuir)"
metadata:
  hermes:
    tags: [dataviz, charts, html, editorial, report]
    related_skills: [graficos-jongonzlz-style, baoyu-infographic, aurora-design-system]
tags: [dataviz, charts, html, editorial, svg, chartjs, echarts, report, design-tokens]
related_skills: [graficos-jongonzlz-style, baoyu-infographic, aurora-design-system, educational-html-pipeline]
---

# Lieflat Charts — Dataviz Editorial con Contratos

## Qué es

**lieflat-charts** (github.com/larashero3-dotcom/lieflat-charts, ~2.600⭐) es un *Agent Skill* (formato SKILL.md, compatible con Claude Code/Codex/Hermes) que convierte datos en gráficos HTML autocontenidos con estilo de publicación. Su valor no son los gráficos: es el **sistema de decisión** que los genera.

Enfoque único: cada figura del catálogo está etiquetada por **forma de datos** (clave primaria de selección), **ocasión** y **tiempo de lectura del lector**. La selección de gráfico es determinista a partir de los datos, no del gusto.

## When to Use (cuándo usar este skill)

- El usuario da datos y pide "visualiza esto / hazme un gráfico / dashboard / página de datos" **sin** nombrar un estilo concreto → aplicar la metodología Lieflat.
- Para gráficos macro/demográficos españoles con estilo periodístico específico → usar primero `graficos-jongonzlz-style` (más ajustado a ese caso).
- Para infografías de marketing → `baoyu-infographic`. Lieflat es para **datos con contrato de verdad**: unidades reales, fuentes, notas al pie.

## Arquitectura del repo (qué reutilizar)

```
SKILL.md              ← código legal del método: modos de salida + contratos de selección
catalog.md            ← 64 figuras en tablas: nombre, título interno, forma de datos, ocasión,
                        tiempo de lectura, motor (Chart.js/ECharts/SVG), figura hermana
report-catalog.md     ← 12 plantillas de informe completo (R01-R12, ZH/EN)
mono-tokens.js        ← ÚNICA fuente de verdad del estilo: colores/typografía/animación (window.MONO)
color-presets.js      ← 3 presets de color + lógica de selección automática
templates/            ← galerías multi-tarjeta por familia (lupi, glance, basics, maps, big-*)
examples/             ← ejemplos terminados con datos reales
scripts/validate.mjs  ← verificación de coherencia tokens vs plantillas
```

## Las 5 familias visuales

| Familia | Trazo | Tiempo de lectura | Uso |
|---------|-------|-------------------|-----|
| **Lupi Editorial** | línea fina, puntos, registro secuencial, mucho espacio en blanco | lectura lenta | papers, informes anuales, historias de datos |
| **Glance** | barras gruesas, números grandes, bloques de color, orden claro | <10s | informes semanales, paneles, conclusiones primero |
| **Basics** | barras/líneas/donut familiares + escalas legibles y hairlines editoriales | medio | contenido simple, fallback elegante |
| **Maps** | mapas | — | SOLO si el usuario pide mapa o distribución geográfica explícitamente |
| **Interactive/Big** | gráficos grandes interactivos (redes, flujos, trayectorias) | demo | presentaciones, vídeo |

## Contratos duros del método (las reglas que lo hacen reutilizable)

1. **Modo gráfico es el predeterminado.** Datos + "analiza esto" → gráficos (o 2-3 gráficos de evidencia). El modo informe SOLO si el usuario dice explícitamente "informe / anual / mensual / libro blanco / póster / one-pager". Ante ambigüedad: modo gráfico.
2. **Prioridad de selección de plantilla:** auditar primero Lupi Editorial → luego Basics → Glance solo si ninguno encaja o si se pide lectura de 3s/panel. Maps solo bajo petición explícita.
3. **Un entregable = un sistema de color.** Mono (tinta #1C1C1A sobre papel #F0EFEB) es el garante; presets: celadón azul, palmera verde, rojo redacción; o paleta personalizada del usuario. Nunca mezclar. **La luminosidad ES el dato:** lo más importante = lo más oscuro.
4. **Tokens centralizados:** cualquier color/fuente/animación que contradiga `mono-tokens.js` pierde. Al entregar un HTML de archivo único, los tokens se inlinean.
5. **Unidades reales y proveniencia:** cada figura conserva unidades, título, nota al pie, fuente y crédito participando en la expresión — prohibido "índice sin sentido".
6. **Figuras hermanas** = pares mismo tema distinto tipo, solo para comparar contratos de datos, no para generar las dos.

## Cómo aplicarlo sin clonar el repo

```bash
# El repo ES un skill instalable — se puede leer directo de GitHub:
curl -sL https://raw.githubusercontent.com/larashero3-dotcom/lieflat-charts/main/SKILL.md
curl -sL https://raw.githubusercontent.com/larashero3-dotcom/lieflat-charts/main/catalog.md
curl -sL https://raw.githubusercontent.com/larashero3-dotcom/lieflat-charts/main/mono-tokens.js
# Para trabajo intensivo, clonar:
git clone https://github.com/larashero3-dotcom/lieflat-charts
```

Para buscar el código de referencia de una figura: catalog.md → tipo de figura → abrir la galería de la familia → localizar el `<div class="card">` por el título interno → buscar en `<script>` el bloque de comentarios `// ════` con el mismo nombre. **Nunca copiar la página completa** — las galerías son páginas multi-tarjeta; lo que se entrega siempre es un archivo único ensamblado con el esqueleto del SKILL.md.

## Integración con los proyectos de David

- **DataHub España / paneles ESIOS:** usar la lógica datos→tipo de gráfico (forma de datos como clave) para elegir visualizaciones automáticamente por pestaña.
- **Informes PDF de presupuestos/BOE:** report-catalog R01-R12 como referencia de estructura de página (portada + gráficos + pie de fuente).
- **Aurora:** los tokens de Lieflat son CSS puro — patrón portable: design system → `<script src="tokens.js">` con todo en `window.*` para permitir inlining.
- **Páginas de afiliación (Kit72h):** la familia Glance (barras gruesas, números grandes, <10s) es perfecta para páginas de comparativa.

## Comparativa con skills existentes

- `graficos-jongonzlz-style`: paleta concreta para macro España. Lieflat es el genérico con árbol de decisión. Si el pedido es estilo jongonzlz → aquel skill; cualquier otro dataviz → Lieflat.
- `baoyu-infographic`: infografía decorativa de layouts. Lieflat es dataviz con contrato de verdad sobre los datos.
- `pretext` / `popular-web-designs`: patrones de UI, no de selección de gráficos.

## Pitfalls

- **Licencia NOASSERTION (custom)** — verificar términos antes de redistribuir plantillas o copiar código literal a productos propios; citar el repo SIEMPRE.
- Las galerías son de **múltiples tarjetas por página**: copiarlas enteras rompe el entregable de archivo único.
- Sin `mono-tokens.js` inlineado, el HTML depende de red para fuentes/Chart.js — para entrega offline, inlinear dependencias o preferir SVG escrito a mano.
- La prioridad Lupi→Basics→Glance es contraintuitiva (va contra el gusto "de dashboard"): respetarla — está calibrada para legibilidad editorial.
- Modo informe no es "dibujar varios gráficos": las plantillas R01-R12 determinan la estructura de página completa; los gráficos internos siguen catalog.md.
- El README y el catálogo están en chino (hay README.en.md) — la semántica de las tablas se lee por columnas, no hace falta traducir todo.

## Verificación

Entrega correcta cuando:
1. Modo de salida decidido explícitamente (gráfico vs informe) y justificable por las palabras del usuario
2. Familia elegida siguiendo prioridad Lupi→Basics→Glance (o excepciones L17/L20/F15-F17 del catálogo)
3. Un solo sistema de color en todo el archivo
4. Cada gráfico conserva unidades reales + fuente + crédito visibles
5. HTML de archivo único que abre con doble clic (dependencias inlineadas o requisito de red declarado)
6. El tipo de gráfico trazable a una fila de catalog.md (forma de datos coincide)
