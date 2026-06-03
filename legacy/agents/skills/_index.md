# Skills Registry

## Skills de dominio (ejecutables por agentes)

| Nombre | Archivo | Aplica a | Añadido |
|--------|---------|----------|---------|
| Software Development Universal | software-dev.md | Cualquier tarea de tipo software | 2026-03-19 |
| Dashboard Development Universal | dashboard-dev.md | Dashboards y visualización desde datos sucios | 2026-03-19 |
| Web Deploy — Shared Hosting | web-deploy.md | Deploy/migración de sitios en Apache shared hosting | 2026-03-19 |
| PWA → APK Android | pwa-android.md | Apps móviles Android desde HTML+JS vanilla, sin frameworks ni Play Store | 2026-03-20 |

## Skills del ecosistema (documentados en skills/)

| Nombre | Archivo | Categoría | Descripción |
|--------|---------|-----------|-------------|
| Multi-Agent Orchestration | `skills/multi-agent-orchestration.md` | Core | Orquestación con 11 agentes, 3 flujos adaptativos, delegación y checkpoints |
| Two-Layer Architecture | `skills/two-layer-architecture.md` | Core | Arquitectura documental/ejecutable con cero duplicación y 42% menos tokens |
| Ebbinghaus Memory System | `skills/ebbinghaus-memory-system.md` | Core | Memoria con curva de olvido, índice inteligente y carga bajo demanda |
| Adversarial Critic | `skills/adversarial-critic.md` | Core | Agente crítico con 6 criterios objetivos de activación automática |
| System Verification & Portability | `skills/system-verification-portability.md` | Core | Verificación cross-platform, .gitignore, reglas de portabilidad |
| Adaptive Flow Selection | `skills/adaptive-flow-selection.md` | Flujo | Selección de flujo corto/medio/largo por nivel de complejidad |
| Structured Report Protocol | `skills/structured-report-protocol.md` | Flujo | Reportes estructurados entre agentes con formatos obligatorios |
| Collaborative Decision Protocol | `skills/collaborative-decision-protocol.md` | Flujo | Protocolo de decisión colaborativa entre IA y humano |
| Intelligent Index Loading | `skills/intelligent-index-loading.md` | Flujo | Índice con señales de relevancia, decay y umbrales de carga |
| Skill Maintenance Protocol | `skills/skill-maintenance-protocol.md` | Flujo | Reaprendizaje activo y auditoría del Librarian |
| Spec Template Pattern | `skills/spec-template-pattern.md` | Template | Specs verificables con verbos prohibidos y límite de 700 tokens |
| Learning Template Pattern | `skills/learning-template-pattern.md` | Template | Destilación de aprendizaje con clusters, decay y conexiones |
| Review Template Pattern | `skills/review-template-pattern.md` | Template | Validación PASS/FAIL con hallazgos categorizados |
| nan.builders Deploy | `skills/nan-builders-deploy.md` | Deploy | Deploy estático para nan.builders + GitHub Pages |
| Dynamic Clusters Pattern | `skills/dynamic-clusters-pattern.md` | Clusters | Clusters dinámicos y red de conocimiento entre learnings |

## Cómo añadir un skill
1. Copia template-skill.md de agents/skills/
2. Renómbralo: [dominio]-[nombre].md
3. Rellénalo con: descripción, dominio, fases, matriz de decisiones, reglas, patrones, anti-patrones
4. Añade fila a la tabla de "Skills de dominio" o "Skills del ecosistema" según corresponda
5. Notifica al librarian