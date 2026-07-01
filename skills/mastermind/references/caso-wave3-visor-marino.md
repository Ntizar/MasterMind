# Caso: WaveThree — Visor marino 3D

**Fecha:** 2026-06-17
**Proyecto:** Visor marino 3D con Three.js, WebGPU y datos oceanográficos
**Repo:** github.com/Ntizar/WaveThree (privado)
**Deploy:** GitHub Pages vía GH Actions
**Estrategia:** Greenfield + crons one-shot (9 crons, 1h spacing)

## Señal de aprendizaje

Cuando el agente dijo "¿Qué tal si mañana elegimos la zona piloto?", David respondió: **"¿Cómo que mañana? Deepseek te necesito."** — frustración clara por la sugerencia de esperar.

**Lección:** La Fase 0 se hace AHORA. Los crons se programan AHORA.

## Secuencia ejecutada

```
16:18 — AGENTE PRINCIPAL: Fase 0 completa
         - Crear repo privado Ntizar/WaveThree
         - Scaffold: README, ARCHITECTURE.md, ADR-001, package.json, .gitignore
         - MVP visual: escena Three.js, ondas Gerstner con vertex shader, panel de parámetros
         - GH Actions workflow (deploy-gh-pages.yml)
         - Investigación: zona piloto Gijón (Cantábrico), mapa de fuentes, pipeline de datos
         - docs/sources/FASE-0-investigacion.md
         - Commit + push inicial

         → 9 crons one-shot programados espaciados 1h:

17:18 — F1.1: Mejora MVP visual (shader + espuma + UI glass)
18:18 — F1.2: UI avanzada (panel, selector escenarios, FPS)
19:18 — F1.3: Pipeline datos reales GEBCO (scripts Node.js)
20:18 — F2.1: Batimetría 3D (heightmap en escena, demo sintética)
21:18 — F2.2: Escenarios reales (4 escenarios, selector funcional)
22:18 — F3: Océano espectral (JONSWAP + iFFT, toggle Gerstner/espectral)
23:18 — F4: Estructuras costeras (dique, espuma, spray)
00:18 — F5: Producto técnico (comparador, exportación, docs)
01:18 — Auditoría final (bugs, CHANGELOG, calidad)
```

## Stack técnico

| Capa | Tecnología |
|------|-----------|
| Render 3D | Three.js (WebGPU con fallback WebGL) |
| MVP olas | Gerstner waves con vertex shader personalizado |
| Océano espectral | JONSWAP spectrum + iFFT 2D en CPU |
| Batimetría | GEBCO global grid (NetCDF → Float32 binary) |
| UI | Glassmorphism, panel colapsable, selector escenarios |
| Deploy | GH Actions → peaceiris/actions-gh-pages → gh-pages branch |
| Preproceso | Node.js scripts (netcdfjs, commander) |

## Archivos creados en Fase 0 (por el agente principal)

```
WaveThree/
├── .github/workflows/deploy-gh-pages.yml
├── README.md
├── package.json (workspace root)
├── apps/web-viewer/
│   ├── index.html (UI overlay glassmorphism)
│   ├── package.json
│   ├── vite.config.js
│   └── src/main.js (orquestador)
├── src/
│   ├── scene/setup.js (cámara, luces, renderizador, WebGPU/GL fallback)
│   ├── ocean/gerstner.js (6 ondas, vertex shader, espuma, fresnel)
│   ├── bathymetry/index.js (placeholder)
│   ├── structures/index.js (placeholder)
│   ├── loaders/index.js (scenario loader)
│   └── ui/panel.js (ControlPanel)
├── data/scenarios/temporal_2026_01_17_1200.json
├── docs/
│   ├── architecture/ARCHITECTURE.md
│   ├── decisions/ADR-001-estrategia-arquitectura.md
│   └── sources/FASE-0-investigacion.md
└── (crons generan el resto)
```

## Crons one-shot: estructura del prompt

Cada cron recibió un prompt autocontenido con:
1. **Proyecto y repo** (contexto completo)
2. **Qué hacer** (tarea específica de la fase)
3. **Archivos a modificar** (rutas exactas)
4. **Qué verificar** (criterios de aceptación)
5. **Instrucción de commit + push** (GITHUB_TOKEN del .env)

## Patrón de prompt

```
Eres un agente de desarrollo para WaveThree (repo: Ntizar/WaveThree, privado).

Tu tarea: **[Nombre de fase]**

Trabaja en /root/workspace/WaveThree/

## Qué hacer:
[lista de tareas numeradas con rutas de archivo]

## Verificar:
[criterios de aceptación]

## Haz commit y push con mensaje: "[mensaje]"

Usa GITHUB_TOKEN del .env.
```

## Lecciones

- GH Actions workflow debe crearse en el commit de creación del repo, no en un cron posterior
- La Fase 0 (investigación) la hace el agente principal — requiere síntesis, no ejecución mecánica
- Crons one-shot sin solapamiento: usar timestamps ISO con 1h de diferencia
- Cada cron termina con commit+push — GH Actions despliega automáticamente
- La auditoría es un cron separado al final, no parte de F5
- El MVP visual (Gerstner) se creó en Fase 0 para que el primer cron (F1.1) tenga algo que mejorar, no que crear desde cero