---
name: agent-graph-architecture
description: "Usa al diseñar y presupuestar grafos de IA agéntica."
version: "1.0.0"
author: "David Antizar (Mastermind)"
license: "MIT"
tags: [agentic-ai, architecture, token-budgeting, graph-editor, browser-tools, ai-systems-design]
related_skills: [agent-canvas-visualization, layered-agent-architecture, browser-local-tools, token-tracking, mastermind-orchestration]
source_repo: https://github.com/gcjordi/aigraphstudio
demo: https://aigraphstudio.jordigarcia.eu/
metadata:
  hermes:
    tags: [agentic-ai, architecture, token-budgeting, graph-editor, browser-tools, ai-systems-design]
    related_skills: [agent-canvas-visualization, layered-agent-architecture, browser-local-tools, token-tracking, mastermind-orchestration]
---

# Agent Graph Architecture — diseño y presupuesto de sistemas agénticos

## When to Use

- Al **planificar una delegación multi-agente (Nivel 3-4)** y querer estimar llamadas, tokens
  y coste del flujo antes de lanzarlo.
- Al **auditar un pipeline agéntico existente** (loops sin cota, evaluator ausente, sobreuso de
  modelo frontier, caminos que saltan guardrails).
- Al **construir una tool HTML browser-first** que necesite persistencia local, schema versionado
  y exportaciones (patrón buildless de referencia).
- Cuando el usuario mencione "diseñar el grafo/flujo del agente", "cuánto costará esta
  arquitectura" o "presupuesto de tokens de un workflow".

Patrón extraído de `gcjordi/aigraphstudio` (MIT, JavaScript, 2026-09-07): herramienta web
buildless para **diseñar, analizar, simular y presupuestar workflows de IA agéntica** antes
de construirlos. No ejecuta modelos: es una capa de ingeniería de arquitectura.

## Principio rector

> **Usar la mínima inteligencia computacional necesaria para completar la tarea correctamente.**

Progresión conceptual: `Prompt → Agent → Loop → Graph → AI System`. Un nodo LLM por nodo es
antipatrón: muchas operaciones van en código determinista, reglas, esquemas, validadores,
APIs tradicionales, retrieval o aprobación humana.

## Vocabulario de 18 tipos de nodo

Start · Input · Prompt · LLM · Agent · Router/Decision · Tool/API · Code/Deterministic ·
RAG/Knowledge · Memory/State · Parallel Split · Merge · Evaluator · Guardrail ·
Human Approval · Loop · Retry · Output

Cada tipo lleva 6 campos educativos: qué representa, cuándo usarlo, cuándo NO usarlo,
buenas prácticas, errores comunes. **Usar este vocabulario al planificar delegaciones
(Nivel 3-4 Mastermind)**: si un plan no puede expresarse con estos nodos, probablemente
está mal diseñado.

## Modelo de presupuesto de tokens (el patrón estrella)

El estimador es **conservador**: suma TODOS los nodos y ramas (incluidas alternativas no
tomadas), sin inferir probabilidades de rama.

1. **Tarjan SCC** sobre el grafo (O(V+E)) → los ciclos son componentes fuertemente conectados.
2. Por SCC: sin controlador → multiplicador 1; `Loop/Retry` → esperado `max(1, estimatedIterations)`;
   acotado → peor caso `max(1, maxIterations, estimatedIterations)`.
3. Múltiples controladores en el mismo SCC → los límites se MULTIPLICAN (bucles anidados
   conservadores) + aviso de ambigüedad. SCC cíclico sin controlador = **peor caso ilimitado**
   (flaggear siempre).
4. Por nodo con modelo: `calls = ejecuciones_base × multiplicador_ESPERADO(scc)`; total
   input/output = tokens por llamada × calls. El peor caso usa el multiplicador de peor caso.
5. `coste = (tokens_in × precio_in + tokens_out × precio_out) / 1e6`. Precios NUNCA
   hardcodeados como hechos permanentes: catálogo editable por provider/model; precio
   cero → aviso explícito "precio no configurado".

## Heurísticas del analizador (fórmulas transparentes)

- Efficiency = max(0, 100 − 6·hallazgos_optimización − 15·hallazgos_controlador_ilimitado)
- Reliability = max(0, 100 − 20·críticos − 7·avisos)
- Complexity = min(100, round(nodos + 0.5·aristas + 3·ciclos/controladores + profundidad))
- Dependencia LLM/humana/frontier = nodos de ese tipo / nodos significativos
- Cobertura de Evaluator/Guardrail: se comprueba buscando un **camino que BYPASEA el control**
  (no basta con que exista en una rama no relacionada) — regla fina que conviene copiar.
- Checks automáticos: ¿nodo LLM innecesario? ¿frontier donde basta modelo barato? ¿bucle sin
  condición de salida? ¿falta evaluator antes de Output? ¿nodos desconectados? ¿falta Start/Output?

## Simulación estructural (sin ejecutar nada)

Recorrido determinista por rondas de tokens: Start siembra la cola; Router/Guardrail/Human
multi-salida eligen la etiqueta exacta configurada (o primera si vacía); Evaluator sigue FAIL
sus primeras `failures` y luego PASS; Loop/Retry repite con etiquetas REPEAT/FAIL/TRUE/YES
hasta el conteo esperado y sale por EXIT/PASS/FALSE/NO; Merge espera mientras otro token vivo
pueda alcanzarlo; tope global 10 000 pasos. Camino sin Output = **incompleto**, no éxito.

## Arquitectura de la app (patrón browser-local-tools de referencia)

App estática **sin build, sin dependencias, sin CDN, sin backend**: source = deployment.
15 módulos ES: `model.js` (CONFIG central, fábricas, validación, precios), `nodes.js`,
`i18n.js` (diccionario CA/ES/EN), `templates.js` (14 grafos de ejemplo), `canvas.js` (SVG,
pan/zoom, pointer events), `app.js` (UI + undo/redo ≤60 snapshots), `storage.js` (IndexedDB),
`rules.js`, `analyzer.js`, `simulator.js`, `exporters.js`, `dom.js` (creación con text nodes
y escaping seguro).

- **Schema versionado** (`schemaVersion: 1`): imports pasan reconstrucción por allowlist —
  campos desconocidos se descartan, majors no soportados se rechazan; el import recibe ID de
  proyecto nuevo (evita sobrescribir en silencio), los nodos conservan ID (aristas estables).
- **Límites explícitos**: 500 nodos, 2000 aristas, 5 MiB serializado, coords ±100k, PNG ≤8192px/lado.
- **Guardrails XSS**: sin `innerHTML` con datos de usuario — text nodes + escaping; etiquetas
  de aristas sanitizadas para Mermaid.
- `registerExporter(id, label, run)` = registro central de exportadores (JSON autoritativo;
  SVG, PNG, Mermaid topológico, Markdown con informe del analizador, HTML imprimible).
- Guardar = commit validado explícito; si falla, los edits sobreviven en memoria y pide export
  JSON — **nunca afirmar como éxito un write que falló**. Sin autosave ni sync multi-tab.
- `?qa=1` aísla la DB de tests de la DB de usuario.
- Exportadores "ejecutables" (LangGraph/n8n/Agents SDK): **rechazar patrones no soportados
  antes que generar código incompleto que parece ejecutable** — filosofía explícita del repo.

## Cómo lo usa Mastermind

1. **Antes de un Nivel 4**: dibujar el flujo con los 18 tipos, estimar tokens con el modelo
   SCC (multiplicadores × llamadas base × coste/1M) para decidir batch/paralelismo.
2. **Auditoría de pipelines propios**: pasar la checklist del analizador (evaluator antes de
   output, ciclos acotados, no-frontier donde basta, caminos que bypassan guardrails).
3. **Plantilla para tools HTML**: el patrón buildless + IndexedDB + schema-allowlist es
   directamente reutilizable en las herramientas de navegador de David (ver `browser-local-tools`).

## Pitfalls

- Las puntuaciones son **heurísticas transparentes, no medidas científicas** — no presentar
  el score como calidad objetiva.
- El estimador deliberadamente SUMA ramas alternativas → sobrestima a propósito; la
  simulación da totales por camino y suele dar menos. No mezclar ambos números.
- Latencia es metadata editable, no camino crítico medido. Coste excluye tools, hosting,
  caching, descuentos batch y trabajo humano.
- Mermaid exporta solo topología (nombres/estructura), no propiedades de nodo.
- Repo con 4⭐ recién creado (2026-09-07) — verificar en re-encuentros si el skill existente
  sigue siendo fiel (`gh api repos/gcjordi/aigraphstudio/readme`), no asumir.

## Verificación

- Demo live: https://aigraphstudio.jordigarcia.eu/ — cargar `examples/parallel.json` o
  `examples/optimizer.json` del repo y comprobar análisis + simulación.
- Árbol real del repo: `gh api repos/gcjordi/aigraphstudio/git/trees/HEAD?recursive=1`.
- ARCHITECTURE.md es la especificación completa del modelo de costes y simulación — leerlo
  antes de citar cifras.

---
*Basado en `gcjordi/aigraphstudio` v1.0.0 · README + ARCHITECTURE.md verificados 2026-09-07 ·
Hecho con ❤️ por David Antizar*
