---
nombre: MonteCarloInversion
alias: montecarlo
tipo: proyecto
clusters: [finanzas-tech, github, arquitectura-software]
repo_local: C:\Users\d_ant\Documents\GitHub\MonteCarloInversion
repo_remoto: https://github.com/ntizar/MonteCarloInversion
live_url: https://ntizar.github.io/MonteCarloInversion/
estado: activo
---

# MonteCarloInversion

Simulador de inversión basado en Monte Carlo. Herramienta web que permite analizar activos financieros combinando simulaciones estocásticas con datos fundamentales, macro, técnicos, opciones, insiders y sentimiento Reddit.

## Stack
- HTML5 + CSS3 + JS vanilla (sin frameworks)
- Web Workers para simulaciones en background
- IndexedDB para persistencia local
- GitHub Actions → GitHub Pages (rama `gh-pages`)
- jsPDF + html2canvas para exportación PDF

## Versión actual
v3.1 — PDF export completo (8 secciones), fix bugs llamadas rotas, deploy workflow GitHub Actions

## Decisiones arquitectónicas permanentes
- Los archivos estáticos viven en `/public` → deploy vía `peaceiris/actions-gh-pages` con `publish_dir: ./public`
- GitHub Pages no puede servir desde `/public` directamente — siempre GitHub Actions
- CORS proxies en cascada: allorigins → corsproxy.io → codetabs → thingproxy
- Flags booleanos (`_optionsLoaded`, `_redditLoaded`, `_insidersLoaded`) para estado de carga asíncrona — no comprobar `!== undefined`
- README debe actualizarse con cada versión — incluir número en título y Changelog detallado

## Pendientes conocidos
- Tab Contexto: actualización individual de `div` en lugar de re-render completo
- PDF: secciones Noticias y Backtest sin párrafos interpretativos
- Test con API key real en producción (Vercel deploy)

## Learnings de este proyecto
- [[2026-03-20-montecarlo-github-pages-subdirectory]]
- [[2026-03-20-montecarlo-deploy-sin-verificar]]
- [[2026-03-20-montecarlo-v35-context-pdf-screener]]
