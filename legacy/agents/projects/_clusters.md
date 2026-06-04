# Mapa de Clusters — Red de Conocimiento

> Indice vivo de clusters. Un cluster agrupa learnings y proyectos por dominio de conocimiento.
> Se crean dinámicamente — cada nuevo dominio genera un cluster. No hay lista cerrada.

---

## Cómo funciona la red

- Cada **learning** tiene `clusters:` en su frontmatter → conexiones en Graph View
- Cada **proyecto hub** lista sus learnings como wikilinks → el proyecto es el nodo central
- Este archivo es el **meta-nodo** que conecta todo → Obsidian Graph View (Ctrl+G)

---

## Clusters activos

### #sistema
El propio sistema de agentes: diseño, gaps, mejoras, evolución

**Learnings:**
- [[2026-03-19-software-skill-md]] · [[2026-03-19-dashboard-skill-md]] · [[2026-03-19-system-gaps-fix]]
- [[2026-03-24-sistema-v2-index-inteligente]]
- [[2026-03-25-learning-platform-vercel-deploy]] · [[2026-03-25-learning-platform-v2-planificacion-ordenada]]
- [[2026-03-25-profiles-json-5-perfiles]] · [[2026-03-25-modules-json-estructura-perfiles]]
- [[2026-03-25-modules-v2-placeholders-personalizacion]] · [[2026-03-25-platform-v2-js-perfiles-gamificacion]]
- [[2026-03-25-start-bat-v2-browser-auto]] · [[2026-03-25-platform-v2-simplificado-robusto]]
- [[2026-03-25-pdf-export-guia-instalacion]] · [[2026-03-25-fase-1-perfiles-gamificacion-completa]]
- [[2026-03-25-liquid-glass-effects-visual]] · [[2026-03-25-contenido-calidad-m1-m2-mejorado]]
- [[2026-03-25-modules-v2-contenido-completo-enriquecido]] · [[2026-03-25-modulos-m6-m8-contenido-perfiles]]
- [[2026-03-25-fase-2-contenido-perfiles-completa]] · [[2026-03-25-fase-3-roadmap-creado]]
- [[2026-03-25-sandbox-integrado-semana-1]] · [[2026-03-25-fase-3-semana-1-sandbox-archivado]]
- [[2026-03-25-leccion-trabajar-ordenado-por-partes]] · [[2026-03-25-cierre-sesion-archivar-proyecto]]

---

### #web
Frontend, HTML/CSS, Apache, hosting, Vercel, SEO, sitios estáticos, plataformas educativas

**Learnings:**
- [[2026-03-19-caedelcielo-subdomain-to-path]] · [[2026-03-19-caedelcielo-multifile-sync]]
- [[2026-03-25-learning-platform-vercel-deploy]] · [[2026-03-25-learning-platform-v2-planificacion-ordenada]]
- [[2026-03-25-profiles-json-5-perfiles]] · [[2026-03-25-modules-json-estructura-perfiles]]
- [[2026-03-25-modules-v2-placeholders-personalizacion]] · [[2026-03-25-platform-v2-js-perfiles-gamificacion]]
- [[2026-03-25-start-bat-v2-browser-auto]] · [[2026-03-25-platform-v2-simplificado-robusto]]
- [[2026-03-25-pdf-export-guia-instalacion]] · [[2026-03-25-fase-1-perfiles-gamificacion-completa]]
- [[2026-03-25-liquid-glass-effects-visual]] · [[2026-03-25-contenido-calidad-m1-m2-mejorado]]
- [[2026-03-25-modules-v2-contenido-completo-enriquecido]] · [[2026-03-25-modulos-m6-m8-contenido-perfiles]]
- [[2026-03-25-fase-2-contenido-perfiles-completa]] · [[2026-03-25-fase-3-roadmap-creado]]
- [[2026-03-25-sandbox-integrado-semana-1]] · [[2026-03-25-fase-3-semana-1-sandbox-archivado]]
- [[2026-03-25-cierre-sesion-archivar-proyecto]]

---

### #github
CI/CD, GitHub Actions, GitHub Pages, Git, deploy, Vercel

**Learnings:**
- [[2026-03-20-montecarlo-github-pages-subdirectory]] · [[2026-03-20-montecarlo-deploy-sin-verificar]]
- [[2026-03-19-caedelcielo-subdomain-to-path]]
- [[2026-03-25-learning-platform-vercel-deploy]]

---

### #arquitectura-software
CORS, APIs, proxies, patrones de arquitectura, integración de servicios

**Learnings:**
- [[2026-03-19-nap-dashboard-ciclo5]] · [[2026-03-19-nap-dashboard-ciclo6]]
- [[2026-03-20-montecarlo-v35-context-pdf-screener]]

---

### #datos
Dashboards, visualización, limpieza de datos, Open Data

**Learnings:**
- [[2026-03-19-dashboard-skill-md]] · [[2026-03-19-nap-dashboard-ciclo6]]

---

### #finanzas-tech
Análisis financiero con código, simulaciones, screeners

**Learnings:**
- [[2026-03-20-montecarlo-v35-context-pdf-screener]]
- [[2026-03-20-montecarlo-github-pages-subdirectory]] · [[2026-03-20-montecarlo-deploy-sin-verificar]]

---

### #mobile
Apps móviles, PWA, APK, instalación sin stores

**Proyecto:** [[medvisit]]
**Skill:** [[pwa-android]]

---

## Proyectos activos

| Proyecto | Hub | Clusters | Repo local |
|---------|-----|---------|-----------|
| MonteCarloInversion | [[montecarlo]] | #github #finanzas-tech #arquitectura-software | `GitHub/MonteCarloInversion` |
| NAP Dashboard | [[nap-dashboard]] | #arquitectura-software #datos | `Github/nap-dashboard` |
| Caedelcielo | [[caedelcielo]] | #web #github | `Github/Caedelcielo` |
| medvisit | [[medvisit]] | #web #mobile | `Github/medvisit` |
| learning-platform | [[learning-platform]] | #web #github #sistema | `MASTERTMIND/learning-platform` |

---

## Cómo añadir un cluster nuevo

1. Nombre: minúsculas, sin espacios, kebab-case → `#nombre-cluster`
2. Añadir sección `### #nombre` bajo "Clusters activos" con descripción y learnings
3. Añadir cluster al frontmatter del learning que lo origina
4. Si hay proyecto asociado → añadir fila en "Proyectos activos"

**Clusters futuros** (se crean cuando aparecen, no antes):
`#saas` · `#youtube` · `#excel` · `#ia` · `#automatizacion` · `#negocio` · `#escritura` · `#research`

---

## Mantenido por
[[10-librarian]] — actualiza este archivo cuando detecta nuevos clusters o proyectos.
Última actualización: 2026-03-26 (revisión completa — sesión Opus 4.6)
