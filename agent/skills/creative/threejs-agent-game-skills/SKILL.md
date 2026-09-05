---
name: threejs-agent-game-skills
description: "Usa al construir juegos three.js con skills de agente y QA."
version: "1.0.0"
author: "Skill reportado de majidmanzarpour/threejs-game-skills"
license: "MIT"
tags: [threejs, juegos, agent-skills, qa, playwright, verificacion, creative]
related_skills: [webgl-scene-wow, ecctrl, threejs-webgpu-relighting, webgpu-engine-architecture, threejs-awesome-graphics-agent-skills, skillopt]
---

# Three.js Game Skills — paquete de agent skills para juegos pulidos

## Qué es

Un **paquete autocontenido de skills para agentes** (Codex / Claude Code, y por extensión Hermes) cuyo objetivo es construir **juegos three.js jugables y pulidos**: gameplay, gráficos AAA, UI, assets generados por IA (3D/imagen/audio), depuración y verificación de release.

- **Repo original:** `https://github.com/majidmanzarpour/threejs-game-skills` (1.4K⭐) · Creado por [Majid Manzarpour](https://x.com/majidmanzarpour).
- **Estructura:** ~9 skills especializadas + un **skill "director"** (`threejs-game-director`) que **enruta el trabajo** sin que el usuario tenga que elegir cada especialista a mano.
- **Scaffold incluido:** Vite + TypeScript + Three.js dentro de los propios skill folders.

## El patrón valioso (lo que aporta a Mastermind)

1. **Skill director que enruta** (gameplay, graphics, UI, asset-gen, audio, debugging, release): un solo punto de entrada que despacha a los especialistas. Encaja con el patrón `layered-agent-architecture` / orquestación de Mastermind.
2. **Verificación del propio trabajo, end-to-end**: hooks de test deterministas, **RNG con semilla fija**, plantillas **Playwright** para smoke tests, *visual-regression baselines* y *bot playtests*. El agente puede **comprobar su propio output**, no solo escribirlo — conecta con `dogfood` / `requesting-code-review`.
3. **Escalado de la verificación al cambio**: un juego entero recibe "production pass"; un fix pequeño de HUD sigue siendo un fix pequeño (scope-aware QA).
4. **Sin modelo ni API key de pago obligatorios** — el paquete no depende de un proveedor concreto.

## Instalación (si se va a usar directamente)

```bash
# Codex
npx skills add majidmanzarpour/threejs-game-skills --skill '*' -a codex -g -y
# Claude Code
npx skills add majidmanzarpour/threejs-game-skills --skill '*' -a claude-code -g -y
# O desde checkout clonado: ./install.sh --codex / --claude / --all
```

## Integración con Mastermind

- **Adoptar el patrón "director + verificación end-to-end"** al construir juegos/demos three.js para David: usar un skill director que rute especialistas y colar **QA con RNG sembrado + Playwright** en cualquier juego que haya que dejar "funcionando de verdad" (no solo bonito).
- Encaja con los skills three.js ya existentes (`webgl-scene-wow`, `ecctrl`, `threejs-webgpu-relighting`): este paquete aporta la **capa de proceso** (orquestación + verificación), los otros aportan la **capa técnica** (escenas, controles, relighting).

## Pitfalls

- Los `npx skills add` van a `codex`/`claude-code`, NO a la instalación de Hermes: para adoptarlo en Mastermind hay que **portar el patrón** (copiar la lógica de director + QA) a skills nativos de `%LOCALAPPDATA%\hermes\skills\`, no ejecutar el `npx` y asumir que queda integrado.
- 1.4K⭐ es más bajo que los veteranos del dominio (three.js está cubierto por skills más grandes) → tratar como **referencia de proceso**, no como la fuente única de verdad técnica.
- Los hooks deterministas (RNG sembrado) son un requisito para que los tests no fallen por azar: si se portan, mantener la semilla en cada test.

## Verificación

- Si David pide un juego three.js jugable: adoptar el flujo director → especialistas → **smoke test Playwright + captura visual + bot playtest** antes de dar por bueno el resultado. El test de humo es que el juego cargue, tenga input funcional y una captura de regresión estable.
