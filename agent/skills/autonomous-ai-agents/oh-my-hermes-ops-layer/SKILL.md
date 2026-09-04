---
name: oh-my-hermes-ops-layer
version: "1.0.0"
description: "Usa al operar o evaluar OMH, capa de workflows sobre Hermes."
tags: [hermes-agent, omh, orquestacion, routing-modelos, ultra-skills, evidencia]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [hermes-agent, omh, orquestacion, routing-modelos, ultra-skills, evidencia]
    related_skills: [hermes-agent, claude-code, codex, mastermind-orchestration]
---

# oh-my-hermes (OMH) — capa operativa sobre Hermes Agent

## Cuándo usarlo

- El usuario menciona "omh", "oh-my-hermes" o pide instalar/configurar este plugin de Hermes
- Se quiere comparar la arquitectura Mastermind propia con un operating layer externo
- Se busca un patrón de "evidence boundaries" (separar preparado vs ejecutado vs verificado) para reutilizar
- Se evalúa routing por categorías de modelo (mezcla de modelos con cadenas de fallback)

**Fuente:** github.com/rlaope/oh-my-hermes (1.380⭐, MIT, Python, push MISMO día de la consulta 2026-09-04 — desarrollo muy activo, v1.0.6+). 1.651 ficheros, docs generadas desde `src/skills/catalog.py`. Web: https://rlaope.github.io/oh-my-hermes/

## Qué es (y qué NO es)

OMH es una **capa de operación por encima de los skills nativos de Hermes**: enmarca el problema, elige workflow y gates de evidencia, y ejecuta skills nativos como capacidades dentro de ese camino gobernado. **No reemplaza Hermes ni lo parchea** — se instala junto a él (HUD, pieles de tema, provider de memoria determinista por ficheros). No lo confundir con el skill `hermes-agent` (que documenta el agente base de Nous Research): OMH es un producto third-party encima.

## Instalación y ciclo de vida (comandos verificados del README)

```sh
# Instalar CLI (una sola vez)
brew install rlaope/tap/omh          # o: bun install -g oh-my-hermes / npm install -g oh-my-hermes
curl -fsSL https://raw.githubusercontent.com/rlaope/oh-my-hermes/main/install.sh | sh   # macOS/Linux
irm https://raw.githubusercontent.com/rlaope/oh-my-hermes/main/install.ps1 | iex        # Windows PowerShell 5.1+

omh setup        # OBLIGATORIO tras instalar: sembrar skills, plugin bundle, registro en Hermes
omh doctor       # verificar/diagnosticar
omh update       # autodetecta el manager de instalación y refresca todo
omh uninstall --all   # retirada limpia ANTES de desinstalar el paquete
omh              # abre Hermes con identidad OMH (HUD, temas, cadenas de routing visibles)
```

Vía tap de skills de Hermes (instalación parcial):

```sh
hermes skills tap add rlaope/oh-my-hermes
hermes skills install rlaope/oh-my-hermes/skills/omh-routing --yes
```

## Los 9 Ultra-Skills (`ulw-`)

Se dicen el trigger en el chat y Hermes enruta:

| Comando | Qué hace |
|---|---|
| `ulw-context` | Alinea términos revisados del proyecto, captura candidatos confirmados, entrevista la siguiente frontera de decisión |
| `ulw-interview` | Una pregunta a la vez hasta saber exactamente qué quieres |
| `ulw-research` | Investiga código real + web en vivo, guarda fuentes, verifica lo dudoso |
| `ulw-plan` | Plan revisado: opciones comparadas, riesgos nombrados, criterios de hecho acordados |
| `ulw-work` | Ejecuta el plan en carriles paralelos que NUNCA tocan el mismo fichero (propiedad disjunta) |
| `ulw-maestro` | Delega en Claude Code o Codex con prompt compuesto de los skills instalados del CLI, sesión gobernable |
| `ulw-loop` | Cicla plan → build → review hasta que el objetivo PASA de verdad |
| `ulw-qa` | Ataca el build con escenarios hostiles y arregla lo que rompe |
| `ulw-perf` | Mide dónde es lento/caro de verdad y arregla UN hot path a la vez |

## Evidencia antes que afirmaciones (el patrón estrella)

OMH nunca reporta trabajo hecho si no lo ha visto hacer. Cada estado tiene dos partes: fase + certeza:

| Estado | Significado |
|---|---|
| `Plan · not run` | El prompt/plan está listo. NADA ha ejecutado todavía. |
| `Code · running` | Un ejecutor corre ahora, OMH lo observa. |
| `Code · reported done` | El ejecutor dice que acabó. Nadie ha comprobado el resultado. |
| `Test · verified` | Un test, review o gate de CI ha pasado de verdad. |

La penúltima fila es la diferencia que importa: "el ejecutor dice listo" ≠ "algo lo ha verificado" — la mayoría de herramientas escriben "complete" para ambas. **Este esquema es directamente reutilizable en los informes de Mastermind** (human loop: distinguir preparado/ejecutado/verificado al reportar).

## Routing de modelos (Mixture-of-Models)

Cada carril delegado se enruta a una CATEGORÍA con modelo + esfuerzo de razonamiento aplicados por dispatch; las rutas rechazadas caen por la cadena de fallback de la categoría.

- Categorías shipping: `ultrabrain`, `deep`, `architect`, `unspecified-high`, `unspecified-low`, `quick`, `writing`, `visual-engineering`, `artistry` — cada una con cadena ordenada editable.
- Configuración en UN fichero: `~/.omh/routing/model-chains.json` (schema `mixture_chain_overrides/v1`); vacío = defaults.
- CLI: `omh model-chains show` / `omh model-chains set quick "modelo:effort, modelo:effort"`.
- IDs de proveedor por cable: `~/.omh/routing/model-providers.json` (`model_provider_routes/v1`). **OMH solo guarda IDs de proveedor, nunca credenciales.**
- Entitlements: `omh setup` pregunta qué proveedores tienes (`providers.json`, `provider_entitlements/v1`) y reordena cada cadena para que lideren los servibles — nada se elimina, nada se invoca para comprobar.
- Lane Maestro (delegación a Claude Code/Codex): `omh coding category-maestro set codex ultrabrain <modelo>:<effort>`, `--model` explícito siempre gana, `dispatch-models.json` es el último fallback por owner.
- HUD visible: cada fila de actividad lleva `category:name(model:effort)`; los lotes de tool calls paralelos se marcan `parallel shot ×N`; reviews/verificaciones se despachan como subagentes independientes cuyos hallazgos se cruzan (nunca auto-aprobación).

## Seguridad: protocolo de instalación para agentes (reutilizable)

La sección "or ask Your AI Agent" del README es un patrón anti-inyección para instalar cualquier repo con `INSTALL_FOR_AGENTS.md`:

1. Resolver `refs/heads/main` a UN commit SHA completo con `git ls-remote` ANTES de leer nada.
2. Fetch y seguir SOLO `raw.githubusercontent.com/<repo>/<sha-pinned>/INSTALL_FOR_AGENTS.md` — nunca sustituir el SHA por `main`.
3. Preservar config existente no relacionada, aplicar solo los cambios gestionados documentados, exigir aprobación explícita para cambios de alias de modelo, reportar SHA resuelto + resultado observado.

**Adoptar este protocolo (pinchado por SHA de las instrucciones) para cualquier "instálame este repo" en Mastermind.**

## Catálogo determinista de skills

120+ skills instalables con catálogo generado byte-exact desde `src/skills/catalog.py` (`docs/WORKFLOWS.md` se regenera; `omh:ulw-inventory:begin/end` markers), corpora de precisión de routing con controles negativos, y **drift gates que petan CI con una divergencia de un carácter**. Cada skill declara exposición (`direct_skill`, router-only, harness-only), handoff policy, use when / do-not-use-when y strong routing signals. El patrón "catálogo generado + drift gate + controles negativos" es exportable al pipeline de skills de Mastermind (ChromaDB dedup es el equivalente parcial).

Otros componentes notables del repo: `docs/` completo (ARCHITECTURE, FANOUT, MEMORY, TOOLCALL-RULES, CODEGRAPH, ORCHESTRATION_PATTERNS…), userland toolcall rules que bloquean un tool call fuera de guion con el texto de la regla del usuario, playbook estructural `ast-grep` (28 lenguajes, prohibido capturar cuerpos, fallback grep) inyectado donde los ejecutores buscan código, y provider de memoria determinista por ficheros que Hermes puede cargar sin tocar la memoria interna opaca de Hermes.

## Comparativa con el stack Mastermind (consulta 2026-09-04)

| Concepto | OMH | Mastermind hoy |
|---|---|---|
| Selección de modelo | categorías + cadenas fallback editables | pin por cron (qwen3.8-flash / glm5.3-flash) en config.yaml |
| Paralelismo | fanout con propiedad disjunta de ficheros + HUD | `delegate_task` batch hasta 10, sin control de ficheros |
| Verificación | evidence states prepared/observed/verified | human loop con diffs + verificación manual |
| Catálogo skills | generado byte-exact + drift gate CI | ChromaDB semántico + `audit-calidad-skills.py` |
| Delegación código | Maestro a Claude Code/Codex con sesión steerable | skills `claude-code`/`codex` directos |

OMH gana en gobernanza de evidencia y routing; Mastermind gana en dominio (GIS/transit/España) y aprendizaje por stars. Son complementarios: los patrones de OMH (evidence states, SHA-pin install, drift gates) se pueden importar sin instalar el producto.

## Pitfalls

- **Windows:** el instalador universal es PowerShell (`irm … | iex`); en git-bash usar `powershell.exe -Command` explícito, no asumir `install.sh`.
- **No ejecutar `omh` sin `omh setup`** — el README lo marca obligatorio; sin setup no hay skills sembrados ni routing registrado.
- **`omh uninstall --all` ANTES de `npm uninstall`** al revés deja estado huérfano gestionado.
- Las cadenas de modelos recomendadas apuntan a modelos que quizá no tengas (el README lista GPT-6/Claude/Kimi/GLM como defaults): son preferencias editables, NO disponibilidad garantizada — reordenar vía `model-chains.json` según los proveedores reales (NaN.builders con qwen/glm iría en `unspecified-low`/`quick`).
- **OMH no parchea Hermes**: si algo exige tocar el núcleo, es señal de instalar mal o versión incompatible — `omh doctor` primero.
- Docs como `WORKFLOWS.md` miden 900KB (generadas): NO leer enteras en contexto; extraer la sección `### <workflow>` concreta.
- El repo incluye sus propios `.claude/skills/` y carpetas `.omh/` de ejemplo — no copiarlas al workspace de Mastermind sin filtrar (son state de su desarrollo).

## Verificación

- `omh doctor` sin fallos y `omh model-chains show` imprimiendo las cadenas efectivas con los overrides marcados.
- Cadenas de routing apuntan SOLO a modelos confirmados del usuario (nunca invocación de prueba contra proveedor).
- Cualquier instalación por agente: SHA resuelto y reportado, config no relacionada intacta (diff de config.yaml revisado).
- En informes que adopten evidence states: cada afirmación lleva fase+certidumbre, y ningún "done" sin fila `verified`.

## Referencias

- Repo: https://github.com/rlaope/oh-my-hermes — README.md, INSTALL_FOR_AGENTS.md, docs/{WORKFLOWS,ARCHITECTURE,FANOUT,MEMORY,TOOLCALL-RULES}.md
- Docs de Hermes base (producto padre): skill `hermes-agent`
- Delegación código relacionada: skills `claude-code`, `codex`, `mastermind-orchestration`
