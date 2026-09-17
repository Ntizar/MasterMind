---
name: jev-ultrafast-browser-agent
description: "Usa al crear agentes de navegador de acciones indexadas."
version: "1.0.0"
author: Mastermind (stars-explorer)
license: MIT
metadata:
  hermes:
    tags: [browser-agent, action-space, typesafe, speculative-fanout, browser-use, dom-snapshot, latencia, uv]
    related_skills: [browser-use-ai, agent-browser, page-agent-browser-automation, computer-use]
---

# Jev Ultrafast — Agente de navegador con espacio de acciones indexado dinámico

**Repo:** https://github.com/browser-use/jev-ultrafast (1.334⭐, Python ≥3.12, MIT, v0.1.0, creado 2026-09-16 por el equipo de Browser Use; verificado 2026-09-17 contra README + `docs/design.md` + `pyproject.toml` + `agent.py` reales).

**Lema del proyecto:** *"A browser agent that chooses instead of generating"* — el modelo **elige** entre acciones candidatas generadas por código; nunca emite selectores, coordenadas, comandos shell ni JavaScript ejecutable.

**Cuándo usar este patrón:** cuando la latencia o el coste del bucle agente-navegador es el problema (browser-use-ai/agent-browser gastan un LLM grande por paso con TODO el contexto, incluido screenshot/DOM), y se quiere un diseño donde cada decisión cuesta **una sola round-trip** y el texto lo escribe un LLM pequeño solo cuando hace falta.

## Los 4 patrones arquitectónicos reutilizables

### 1. Espacio de acciones indexado dinámico (no generado por el LLM)
Cada observación produce una **tabla de elementos con índice** construida por código:
```text
[1] button    Change ticket type · Round trip
[2] combobox  Where from?        · San Francisco
[3] combobox  Where to?          · empty
```
Operaciones disponibles: `CLICK`, `TYPE_TEXT`, `SELECT`, `SCROLL_UP`, `SCROLL_DOWN`, `WAIT`, `DONE`, `BLOCKED`. Solo se ofrecen operaciones compatibles con cada elemento (un checkbox no ofrece `TYPE_TEXT` — los roles editables controlan esa disponibilidad). El snapshot DOM es **atómico**: una sola llamada al navegador lee controles visibles, nombres, valores y texto, manteniendo referencias reales a nodos DOM vía WeakMap (identidad propia, no CDP backendNodeIds).

### 2. Fan-out especulativo operación+objetivo (TypeSafe)
Una ÚNICA petición pregunta «¿qué operación?» y «¿qué objetivo para CADA operación?». El ejecutor consume solo la cabeza correspondiente a la operación elegida → dos decisiones, una round-trip. Las cabezas de objetivo solo contienen elementos compatibles. Cada pregunta de objetivo nombra explícitamente la operación que asume (no pueden leerse entre sí).

### 3. LLM pequeño solo para escribir texto
`TYPE_TEXT` envía goal + campo seleccionado + contexto visible + acciones recientes a un LLM barato (el demo usa `inception/mercury-2.5` vía OpenRouter con reasoning desactivado; Gemini/GLM/DeepSeek valen por helper OpenAI-compatible). Su salida debe parsear como JSON con exactamente un campo `text` válido. Un valor generado sobrevive a un retry de página obsoleta solo si la entrada del helper es idéntica; se descarta tras mutación exitosa.

### 4. Guards de frescura semántica (no conteo de mutaciones)
Antes de clic/selección se comparan: documento, URL completa, viewport, valores/estados de formularios, objetivo seleccionado y contexto cercano de fila/diálogo. La geometría se relee SIEMPRE justo antes de input y se rechazan controles ocluidos. Tras interactuar se espera estado útil: combobox ARIA espera sugerencias visibles (máx 200 ms); resto ≤2 animation frames o 50 ms. Emulación de foco mantiene renderizando pestañas en segundo plano sin cambiar la pestaña visible de Chrome.

**Sin screenshots en el bucle por defecto:** el agente consume estado estructurado; solo ve **texto visible** (nada de cuerpos offscreen rellenando contexto). El inspector y el vídeo usan screencast aparte.

## Resultados medidos (para dimensionar la idea)

| Métrica | Preparado (v1) | Jev Ultrafast | Δ |
|---|---|---|---|
| Tarea Google Flights (mediana) | 9.450 s | 7.092 s | −25% |
| Llamadas al protocolo navegador | 1.092 | 101 | −10× |
| Wikipedia abrir artículo | — | 2.798 s | — |

3/3 passes en tareas alternas (nota del propio repo: 3 repeticiones de UNA tarea, NO benchmark de fiabilidad general).

## Uso práctico

```bash
git clone https://github.com/browser-use/jev-ultrafast.git && cd jev-ultrafast
uv sync                      # instala browser-harness==0.1.13 + httpx[http2]
cp .env.example .env         # TYPESAFE_API_KEY y TEXT_MODEL_API_KEY (OpenRouter)
uv run jev                   # inspector local → http://127.0.0.1:8766
```
Chrome se conecta vía [Browser Harness](https://github.com/browser-use/browser-harness); si falla, `uv run browser-harness --doctor` y permitir remote debugging en Chrome. El inspector muestra elementos numerados, probabilidades de operación/objetivo y acciones ejecutadas; **Choose next** pausa antes de ejecutar.

Como librería:
```python
from jev_ultrafast import Agent
with Agent(url, goal) as agent:            # Agent(url, goals, record_dir=None, screenshots=False)
    for state in agent.run():
        print(state["elapsed_ms"], state["status"])
```
Ejecutar con `uv run --env-file .env python tu_script.py`. CLI de ejemplo: `python examples/run.py --url … --goal '…'`; `examples/flights.py --keep-open` verifica ruta/fecha/resultados de forma independiente (no reserva vuelos).

## Estructura (pensada para leerse entera)

| Fichero | Misión |
|---|---|
| `jev_ultrafast/agent.py` | bucle completo y handoff al helper de texto |
| `jev_ultrafast/snapshot.js` | snapshot DOM atómico, controles indexados, guards de frescura |
| `jev_ultrafast/browser.py` | conexión a Chrome, geometría actual, ejecución |
| `jev_ultrafast/model.py` | cabezas dinámicas operación/objetivo + generación de texto |
| `jev_ultrafast/questions.py` | instrucciones del modelo |
| `jev_ultrafast/demo.py` | inspector local (entry point `jev`) |

Tests **offline**: `uv run pytest` (+ `ruff check .`, `node --check jev_ultrafast/snapshot.js`). `scripts/check_guards.py` prueba controles reales en navegador local sin llamadas a modelo. Grabación de demos: `scripts/record_flights.py <carpeta>` + `scripts/render_demo.py <carpeta>`.

## Pitfalls

- **Es un MVP de 0.1.0 (2026-09-16):** NO maneja shadow roots, iframes, canvas, uploads, pop-up tabs, scroll anidado ni widgets de teclado arbitrarios. Puede `BLOCKED` legítimamente en webs complejas.
- **`DONE` no es prueba de éxito:** el propio repo exige verificación independiente del resultado (el ejemplo de flights comprueba ruta/fecha/opciones visibles en el DOM). Nunca fiarse del auto-informe del modelo.
- **Límites duros por run:** 60 acciones de navegador, 120 peticiones de decisión, ≤250 candidatos de acción (los truncados no son seleccionables).
- **El servicio del inspector es loopback-only** con checks de Host/Origin + token local; credenciales quedan server-side. Las pestañas comparten el perfil Chrome existente.
- **Dependencias de pago:** TypeSafe API + API de texto (OpenRouter en el ejemplo). No es self-hosted out-of-the-box.
- **`skill_angles` del explorador decía `pattern-real-time`** — absurdo heurístico; el patrón real es *indexed action space + speculative fan-out* (confirmado leyendo README y design.md, regla del pipeline).

## Integración con Mastermind

- **Patrón a robar para nuestros pipelines:** cuando construyamos automatización de navegador propia (scraping de sigma.madrid.es, NAP DGT, portales BOE), la idea de «candidatos generados por código + modelo solo elige» reduce errores de alucinación de selectores y coste por paso.
- **Comparativa de herramientas browser-IA (consultado 2026-09-17):** `browser-use-ai` (101k⭐, LLM grande por paso, máximo alcance/capacidad) · `agent-browser` (CLI Rust, control manual scriptable) · `page-agent` (in-page JS, sin infraestructura externa) · **jev-ultrafast** (mínima latencia/peticiones, alcance MVP — el mejor para tareas de formulario corto y repetitivo en un site concreto).
- Si TypeSafe fuera un problema de licencias, el patrón de fan-out operación/objetivo es implementable a mano con cualquier LLM que soporte structured output: dos preguntas en un solo prompt con claves `operation`, `click_target`, `type_text_target`, `select_target`.

## Verificación

```bash
# Comprobar que el repo sigue vivo y la versión:
gh api repos/browser-use/jev-ultrafast --jq '{stars:.stargazers_count, pushed:.pushed_at, archived:.archived}'
gh api repos/browser-use/jev-ultrafast/contents/pyproject.toml --jq '.content' | base64 -d | grep version
```
