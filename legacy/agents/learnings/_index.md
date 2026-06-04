# Learnings Index

> Este índice es la primera y única fuente que el orchestrator lee para decidir qué learnings cargar.
> Está diseñado para que en el 80% de los casos no sea necesario abrir ningún learning completo.
> Cada fila responde: ¿cuándo es relevante este learning? ¿qué patrón aporta? ¿vale la pena cargarlo?

---

## Cómo usa este índice el orchestrator

1. Lee el índice completo al arrancar (coste bajo — una sola tabla)
2. Para cada tarea nueva, identifica filas donde `señal_de_relevancia` coincide con la situación
3. Calcula la relevancia efectiva R(t) usando la curva de Ebbinghaus (ver fórmula abajo)
4. Carga solo learnings donde R(t) > 0.3 Y la señal coincide
5. Si `cuando_cargar` es "siempre" → carga sin evaluar (pero decay sigue aplicando al peso)
6. Bajo presión de tokens → subir umbral a 0.5

## Curva de olvido de Ebbinghaus (adaptada)

Fórmula: `R(t) = a / (log(t+1))^b + c`
Donde t = días desde la fecha del learning.

| Tipo decay   | a    | b    | c    | R(30d) | R(90d) | R(180d) | Uso                                    |
|-------------|------|------|------|--------|--------|---------|----------------------------------------|
| permanente  | —    | —    | 1.0  | 1.0    | 1.0    | 1.0     | Reglas del sistema, nunca decaen       |
| lento       | 0.7  | 0.8  | 0.25 | ~0.71  | ~0.58  | ~0.48   | Patrones técnicos reutilizables        |
| normal      | 0.8  | 1.2  | 0.15 | ~0.52  | ~0.37  | ~0.29   | Soluciones a problemas específicos     |
| rápido      | 0.9  | 1.5  | 0.05 | ~0.30  | ~0.18  | ~0.12   | Fixes puntuales, contexto temporal     |

Learnings con R(t) < 0.2 durante 60+ días → marcar como "archivable".
El librarian los moverá a learnings/archive/ con aprobación humana.

---

## Tabla de learnings

| Fecha | Tarea | Tipo | Clusters | Proyecto | Patrón | Señal de relevancia | Cuándo cargar | Decay | Archivo |
|-------|-------|------|---------|---------|--------|---------------------|---------------|-------|---------|
| 2026-03-19 | software-skill-md | conocimiento | #sistema | — | extended-skill | Crear o mejorar un skill de dominio técnico complejo con muchas dimensiones | Solo si la tarea es crear/mejorar un skill | lento | [[2026-03-19-software-skill-md]] |
| 2026-03-19 | dashboard-skill-md | datos | #sistema #datos | — | skill-con-memoria-dinamica | Crear un skill que se va a usar repetidamente en proyectos del mismo dominio | Solo si la tarea es crear un skill con reaprendizaje | lento | [[2026-03-19-dashboard-skill-md]] |
| 2026-03-19 | system-gaps-fix | operaciones | #sistema | — | gap-fix-short-flow | Corregir múltiples gaps estructurales del sistema en un solo ciclo | Solo si es un ciclo de mantenimiento del sistema | normal | [[2026-03-19-system-gaps-fix]] |
| 2026-03-19 | nap-dashboard-ciclo5 | software | #arquitectura-software | [[nap-dashboard]] | api-proxy-with-client-key | API con CORS bloqueado que requiere API key en el cliente | Si la tarea implica API externa con CORS + autenticación | lento | [[2026-03-19-nap-dashboard-ciclo5]] |
| 2026-03-19 | nap-dashboard-ciclo6 | software | #arquitectura-software #datos | [[nap-dashboard]] | dual-proxy-cors-pattern | Dos fuentes de CORS distintas en el mismo proyecto (API REST + archivos binarios externos) | Si la tarea tiene múltiples orígenes CORS o descarga de ZIPs desde browser | lento | [[2026-03-19-nap-dashboard-ciclo6]] |
| 2026-03-19 | caedelcielo-subdomain-to-path | software | #web #github | [[caedelcielo]] | subdomain-to-path-apache | Migrar subdominios a rutas de path en Apache shared hosting | Si la tarea es migración de estructura de URLs en hosting Apache | normal | [[2026-03-19-caedelcielo-subdomain-to-path]] |
| 2026-03-19 | caedelcielo-multifile-sync | operaciones | #web | [[caedelcielo]] | single-source-propagation | Dato clave (CIF, email, URL legal) que aparece en múltiples archivos y hay que mantener sincronizado | Si la tarea toca datos que se repiten en varios archivos de un proyecto estático | lento | [[2026-03-19-caedelcielo-multifile-sync]] |
| 2026-03-20 | montecarlo-github-pages-subdirectory | software | #github | [[montecarlo]] | static-site-subdirectory-deploy | Archivos estáticos en /public o subcarpeta que GitHub Pages no puede servir directamente | Si la tarea implica deploy a GitHub Pages desde un subdirectorio | lento | [[2026-03-20-montecarlo-github-pages-subdirectory]] |
| 2026-03-20 | montecarlo-deploy-sin-verificar | operaciones | #github | [[montecarlo]] | verify-before-deliver | Cualquier ciclo que termina con un deploy — recordatorio de verificar el site live antes de entregar | Siempre que la tarea incluya un deploy a producción | permanente | [[2026-03-20-montecarlo-deploy-sin-verificar]] |
| 2026-03-20 | montecarlo-v35-context-pdf-screener | software | #arquitectura-software #finanzas-tech | [[montecarlo]] | async-loading-flags-pattern | Múltiples fetches asíncronas que alimentan un render que puede ejecutarse antes de que terminen | Si la tarea tiene estado de carga asíncrona complejo con múltiples fuentes | lento | [[2026-03-20-montecarlo-v35-context-pdf-screener]] |
| 2026-03-24 | sistema-v2-index-inteligente | conocimiento | #sistema | — | on-demand-context-loading | Mejorar la gestión de tokens del sistema: carga bajo demanda, degradación de modelos por fase | Solo si la tarea es mantenimiento o evolución del sistema de agentes | permanente | [[2026-03-24-sistema-v2-index-inteligente]] |
| 2026-03-25 | learning-platform-vercel-deploy | contenido | #web #github #sistema | [[learning-platform]] | static-deploy-with-downloadable-assets | Desplegar plataforma educativa en Vercel con archivos descargables reales | Si la tarea es deploy de contenido estático educativo con activos descargables | normal | [[2026-03-25-learning-platform-vercel-deploy]] |
| 2026-03-25 | learning-platform-v2-planificacion-ordenada | operaciones | #sistema #web | [[learning-platform]] | iterative-development-with-context-limits | Proyectos complejos: dividir en micro-tareas <15min, archivar cada learning, usar índice para recuperar contexto | Siempre en proyectos grandes de múltiples fases | permanente | [[2026-03-25-learning-platform-v2-planificacion-ordenada]] |
| 2026-03-25 | profiles-json-5-perfiles | software | #sistema #web | [[learning-platform]] | user-profile-personalization | Plataformas multi-usuario: definir perfiles con vocabulario, ejemplos, casos de uso y duración por módulo | Si la tarea es personalizar contenido educativo por tipo de usuario | normal | [[2026-03-25-profiles-json-5-perfiles]] |
| 2026-03-25 | modules-json-estructura-perfiles | software | #sistema #web | [[learning-platform]] | single-source-personalization | Plataformas multi-perfil: contenido base único + inyección dinámica de ejemplos/vocabulario según perfil | Si la tarea es crear contenido adaptable sin duplicar archivos | normal | [[2026-03-25-modules-json-estructura-perfiles]] |
| 2026-03-25 | modules-v2-placeholders-personalizacion | software | #sistema #web | [[learning-platform]] | placeholder-injection-pattern | Contenido multi-perfil: usar placeholders {{VARIABLE}} en JSON base y reemplazar en runtime según perfil | Si la tarea es personalizar contenido educativo sin duplicar archivos | normal | [[2026-03-25-modules-v2-placeholders-personalizacion]] |
| 2026-03-25 | platform-v2-js-perfiles-gamificacion | software | #sistema #web | [[learning-platform]] | stateful-personalization-engine | Motor JS para plataformas: carga perfiles, reemplaza placeholders, guarda estado (perfil, XP, nivel) en localStorage | Si la tarea es crear plataforma educativa con personalización y gamificación | lento | [[2026-03-25-platform-v2-js-perfiles-gamificacion]] |
| 2026-03-25 | start-bat-v2-browser-auto | operaciones | #sistema #web | [[learning-platform]] | local-dev-with-auto-open | Start.bat verifica archivos v2 y abre navegador automáticamente al iniciar servidor local | Si la tarea es mejorar testing local con apertura automática | rápido | [[2026-03-25-start-bat-v2-browser-auto]] |
| 2026-03-25 | platform-v2-simplificado-robusto | software | #sistema #web | [[learning-platform]] | simplify-and-retry | Reescribir platform.js con menos código, más logging, clear de estado v1, y manejo explícito de errores | Si la tarea es debuggear plataforma que no avanza del onboarding | normal | [[2026-03-25-platform-v2-simplificado-robusto]] |
| 2026-03-25 | pdf-export-guia-instalacion | software | #sistema #web | [[learning-platform]] | one-page-pdf-export | Export a PDF de 1 página con guía de instalación: nombre, perfil, 4 pasos, links, QR code | Si la tarea es crear export útil en vez de JSON técnico | normal | [[2026-03-25-pdf-export-guia-instalacion]] |
| 2026-03-25 | fase-1-perfiles-gamificacion-completa | software | #sistema #web | [[learning-platform]] | phased-development | FASE 1 completa: 5 perfiles, personalización dinámica, 7 badges, PDF export, responsive, start.bat | Al completar fase completa del roadmap — resumen y verificación | lento | [[2026-03-25-fase-1-perfiles-gamificacion-completa]] |
| 2026-03-25 | liquid-glass-effects-visual | software | #sistema #web | [[learning-platform]] | liquid-glass-enhancement | Efectos liquid glass: refracción en profiles, finish modal glow, animación liquid gradient, hover effects | Si la tarea es mejorar visual con glass-refract y animaciones liquid | normal | [[2026-03-25-liquid-glass-effects-visual]] |
| 2026-03-25 | contenido-calidad-m1-m2-mejorado | software | #sistema #web | [[learning-platform]] | interactive-content-enrichment | Contenido enriquecido: diagramas interactivos M1 (8 tipos tarea), cards agentes M2 (11 agents con detalles), ejemplos por perfil M3-M5, quizzes educativos | Si la tarea es mejorar contenido educativo con interactividad y ejemplos contextualizados | normal | [[2026-03-25-contenido-calidad-m1-m2-mejorado]] |
| 2026-03-25 | modules-v2-contenido-completo-enriquecido | software | #sistema #web | [[learning-platform]] | modular-content-creation | Modules-v2.json definitivo: ~500 líneas, 33 elementos interactivos, 34 glass cards, 14 quizzes con feedback educativo | Al completar contenido completo enriquecido para toda la plataforma | normal | [[2026-03-25-modules-v2-contenido-completo-enriquecido]] |
| 2026-03-25 | modulos-m6-m8-contenido-perfiles | software | #sistema #web | [[learning-platform]] | profile-specific-guided-projects | M6-M8 prácticos: M6 (primer proyecto real), M7 (12 ejemplos por perfil), M8 (replicar sistema + plantillas skill/learning) | Si la tarea es crear contenido práctico para que usuarios repliquen el sistema sin conocimiento técnico | normal | [[2026-03-25-modulos-m6-m8-contenido-perfiles]] |
| 2026-03-25 | fase-2-contenido-perfiles-completa | software | #sistema #web | [[learning-platform]] | phased-development | FASE 2 completa: PDF fix, M6 (primer proyecto), M7 (12 ejemplos), M8 (replicar + plantillas), todo lenguaje natural | Al completar fase completa del roadmap — resumen y verificación | lento | [[2026-03-25-fase-2-contenido-perfiles-completa]] |
| 2026-03-25 | fase-3-roadmap-creado | operaciones | #sistema #web | [[learning-platform]] | phased-roadmap-creation | FASE 3 roadmap: 6 features (Sandbox, Mermaid, Analytics, Demo, Comparador, Misiones), 6 semanas, stack CDN sin build | Al crear roadmap de fase nueva — visión global y tareas inmediatas | normal | [[2026-03-25-fase-3-roadmap-creado]] |
| 2026-03-25 | sandbox-integrado-semana-1 | software | #sistema #web | [[learning-platform]] | interactive-simulation-pattern | Sandbox completado: chat interface, 6 respuestas predefinidas (sop/csv/landing/onboarding/debug/articulo), typing indicator, agent-flow animation | Si la tarea es crear simulador interactivo para practicar sin instalar herramienta real | normal | [[2026-03-25-sandbox-integrado-semana-1]] |
| 2026-03-25 | fase-3-semana-1-sandbox-archivado | operaciones | #sistema #web | [[learning-platform]] | feature-archived-but-ready | Sandbox oculto (consume tokens): archivos intactos, navbar link quitado, documentado por qué se archivó, reactivable fácilmente | Si la tarea es archivar feature que funciona pero no se quiere activar | rápido | [[2026-03-25-fase-3-semana-1-sandbox-archivado]] |
| 2026-03-25 | leccion-trabajar-ordenado-por-partes | conocimiento | #sistema | [[learning-platform]] | iterative-development-with-context-limits | Lección principal: división por fases, learnings archivados, _index.md como puerta de entrada, nunca exceder contexto, planificar y volver | SIEMPRE en proyectos complejos — ventaja competitiva del sistema | permanente | [[2026-03-25-leccion-trabajar-ordenado-por-partes]] |
| 2026-03-25 | cierre-sesion-archivar-proyecto | operaciones | #sistema #web | [[learning-platform]] | session-archive-for-retake | Cierre completo: 20+ learnings archivados, hub actualizado, roadmap FASE 3 listo, sandbox archivado, instrucciones retomar | Al cerrar sesión de trabajo — archivar para retomar sin perder contexto | lento | [[2026-03-25-cierre-sesion-archivar-proyecto]] |
| 2026-03-26 | migracion-v3-multi-agente-simplificacion | conocimiento | #sistema | — | layer-separation-no-duplication | Sistema multi-agente con dos capas (documental + ejecutable): separar responsabilidades sin duplicar contenido entre capas | Solo si la tarea es evolución del sistema de agentes o arquitectura multi-capa | permanente | [[2026-03-26-migracion-v3-multi-agente-simplificacion]] |
| 2026-03-26 | github-repo-usar-carpeta-existente | operaciones | #github #sistema | [[learning-platform]] | use-existing-project-structure | Crear un nuevo repositorio o proyecto que necesita carpeta local | Solo si la tarea es crear un repositorio o proyecto nuevo | lento | [[2026-03-26-github-repo-usar-carpeta-existente]] |
| 2026-03-26 | readme-espanol-prioritario | operaciones | #sistema #github | [[learning-platform]] | readme-native-language-first | Crear cualquier repositorio o documentación pública para el sistema Ntizar | Siempre al crear repos o documentación pública Ntizar | permanente | [[2026-03-26-readme-espanol-prioritario]] |
| 2026-03-26 | github-repo-v3-completo | conocimiento | #github #sistema | [[learning-platform]] | repo-as-documentation-product | Crear repositorio público que sirva como producto de documentación y marketing | Solo si la tarea es crear o mejorar un repo público | lento | [[2026-03-26-github-repo-v3-completo]] |
| 2026-03-26 | svg-banner-desde-design-system | software | #web #sistema | [[learning-platform]] | svg-banner-from-css-variables | Necesitar banner o asset visual para README que sea coherente con el design system | Si la tarea necesita banner/asset visual para repo o web | normal | [[2026-03-26-svg-banner-desde-design-system]] |
| 2026-03-26 | windows-bash-path-copy-pattern | software | #sistema #github | — | windows-bash-forward-slash-copy | Copiar archivos en entorno bash-on-Windows (OpenCode, Git Bash, WSL) | Siempre que se copien archivos en bash sobre Windows | normal | [[2026-03-26-windows-bash-path-copy-pattern]] |
| 2026-03-26 | git-nested-cleanup-agents-md | operaciones | #github #sistema | — | clean-nested-git-before-repo-init | Crear repositorio nuevo a partir de archivos existentes de un vault Obsidian o proyecto | Solo si se crea repo nuevo desde archivos existentes | normal | [[2026-03-26-git-nested-cleanup-agents-md]] |
| 2026-03-26 | design-system-documentar-en-readme | conocimiento | #web #sistema | [[learning-platform]] | design-system-visibility-in-repo | Proyecto con design system propio que necesita visibilidad en el README | Si el proyecto tiene design system y se está creando/mejorando README | lento | [[2026-03-26-design-system-documentar-en-readme]] |

---

## Learnings de alta prioridad (cargar siempre — decay permanente)

Estos learnings tienen decay `permanente` (R=1.0 siempre) y `cuando_cargar: Siempre`:
- [[2026-03-20-montecarlo-deploy-sin-verificar]] — verify-before-deliver → en cualquier deploy
- [[2026-03-25-learning-platform-v2-planificacion-ordenada]] — iterative-development → en proyectos grandes
- [[2026-03-25-leccion-trabajar-ordenado-por-partes]] — iterative-development → SIEMPRE en proyectos complejos
- [[2026-03-24-sistema-v2-index-inteligente]] — on-demand-context-loading → en mantenimiento del sistema
- [[2026-03-26-migracion-v3-multi-agente-simplificacion]] — layer-separation-no-duplication → en evolución del sistema
- [[2026-03-26-readme-espanol-prioritario]] — readme-native-language-first → en cualquier repo/doc pública Ntizar

## Learnings de alta prioridad por dominio (cargar cuando la señal coincida)

**Deploy:**
- [[2026-03-20-montecarlo-deploy-sin-verificar]] — verify-before-deliver

**CORS / API externa:**
- [[2026-03-19-nap-dashboard-ciclo5]] — api-proxy-with-client-key
- [[2026-03-19-nap-dashboard-ciclo6]] — dual-proxy-cors-pattern

---

## Regla de carga con decay (v3)

El orchestrator calcula R(t) para cada learning al leer este índice:

1. **Filtro por señal**: solo considerar learnings donde `señal_de_relevancia` coincide con la tarea
2. **Filtro por decay**: solo cargar si R(t) > 0.3 (o > 0.5 bajo presión de tokens)
3. **Excepción permanente**: learnings con decay `permanente` siempre tienen R=1.0
4. **Excepción "Siempre"**: learnings con `cuando_cargar: Siempre` se cargan si R(t) > 0.3
5. **Archivado**: learnings con R(t) < 0.2 durante 60+ días → el librarian propone mover a `learnings/archive/`

En sesiones con presión de tokens, el orchestrator puede:
- Subir umbral de carga a R(t) > 0.5
- Omitir learnings de tipo `conocimiento` si la tarea no es de mantenimiento del sistema
- Priorizar learnings con decay `permanente` y `lento` sobre `normal` y `rápido`
