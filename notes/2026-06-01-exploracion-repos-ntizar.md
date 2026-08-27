# Exploración Autónoma de Repositorios Ntizar — 2026-06-01

## Resumen

Exploración autónoma de los 26 repositorios del usuario Ntizar en GitHub. Se han analizado en profundidad 19 repos con README, identificando patrones reutilizables, arquitecturas destacadas y conocimiento valioso para el sistema Mastermind.

## Repositorios Analizados (26 total)

### Multi-Agent / IA
| Repo | Estrellas | Lenguaje | Descripción |
|------|-----------|----------|-------------|
| NtizarBrainMasterMind | 2 | CSS | Framework multi-agente OpenCode + Obsidian, 11 agentes, memoria Ebbinghaus |
| FreeHands | 0 | Python | Control PC sin manos: gaze + gestos + voz, MediaPipe + PyAutoGUI |

### Data Science / Simulación
| Repo | Estrellas | Lenguaje | Descripción |
|------|-----------|----------|-------------|
| SistemaElectricoFuturo | 1 | JavaScript | Simulador sistema eléctrico español 2026-2035, 17 escenarios, 8.760 horas |
| MonteCarloInversion | 0 | JavaScript | Simulación Monte Carlo bursátil, 5 modelos estocásticos, 9 fuentes de datos |
| rail-lidar-qa-mvp | 0 | Python | Validación calidad LiDAR ferroviario, nubes de puntos .laz, QA visual |
| Voynich_Solving | 0 | Python | Desciframiento manuscrito Voynich como base de datos farmacéutica medieval |
| hackaton1 (TrEnergIA) | 0 | Python | Gemelo energético ferroviario, optimización consumo trenes vs ESIOS |

### Frontend / Dashboards
| Repo | Estrellas | Lenguaje | Descripción |
|------|-----------|----------|-------------|
| Ntizar-Aurora | 0 | CSS | Design System Aurora v5.1, CSS puro, 11 packs opt-in, CDN público |
| solmad | 3 | TypeScript | Madrid Solea: buscador 3D terrazas con sol, Web Workers + SunCalc |
| nap-dashboard | 1 | TypeScript | Dashboard transporte España, parser GTFS en navegador, React + Vite |
| FamilyTree | 0 | JavaScript | Editor visual árbol genealógico, vanilla JS, export JSON/Excel |
| Accidentes2024 | 0 | JavaScript | Megadashboard visual accidentes con víctimas en España 2024 |
| XVLegislatura | 0 | JavaScript | Atlas orgánico Gobierno España, D3.js, 22 ministerios, 300+ órganos |
| OrbitMixer | 1 | JavaScript | Playground visual de mezclas orbitales |
| MetalHoverLab | 0 | JavaScript | Exportable metal hover playground para figuras enmascaradas |
| PacManMadrid | 0 | JavaScript | Pacman temático Madrid |

### Datos Públicos / Divulgación
| Repo | Estrellas | Lenguaje | Descripción |
|------|-----------|----------|-------------|
| datos-gob-watch | 0 | CSS | Radar semanal datasets datos.gob.es, digest estático GitHub Pages |
| IRPFdibujitos | 1 | Python | Calculadora IRPF 2012-2026, motor Python, web vanilla, datos CC0 |
| YoloConteo | 0 | Python | Contador personas/vehículos, YOLOv8n ONNX/WebGPU, 100% navegador |

### Otros
| Repo | Estrellas | Lenguaje | Descripción |
|------|-----------|----------|-------------|
| mastermind | 0 | TeX | Knowledge repository - AI learning and skills extraction |
| inicio-en-nan | 0 | N/A | Guía paso a paso: desde que pagas NaN.builders hasta tener agente IA |
| farosspain | 0 | HTML | Proyecto faros |
| llopezaesthetics | 0 | HTML | Proyecto estético |
| empleady | 0 | CSS | Design system empleady |
| Rumby | 0 | TypeScript | Proyecto Rumby |
| weekPlan | 0 | JavaScript | Planificador semanal |

## Patrones Identificados

### 1. Design System Ntizar (Aurora)
- CSS puro sin dependencias
- Namespaced bajo `.nz`
- 11 packs opt-in (core + 10 dominios)
- 5 skins de marca
- CDN público jsDelivr
- Agent-ready con AGENTS.md
- OKLCH, multi-axis theming, liquid glass real

### 2. Arquitectura Multi-Agente
- 10-11 agentes especializados
- Dos capas: Obsidian (docs) + OpenCode (ejecución)
- Memoria con decaimiento Ebbinghaus
- Asignación multi-modelo por agente
- 40-60% ahorro en tokens vs prompting tradicional
- 12 reglas derivadas de 13 ciclos de uso real

### 3. 100% Frontend / Sin Backend
- Web Workers para cálculos pesados
- IndexedDB cache con TTL diferenciado
- GitHub Pages para deploy
- Vanilla JS / TypeScript, cero npm
- CSP estricta
- CORS proxy chain para APIs sin CORS

### 4. Datos Públicos Españoles
- ESIOS/REE para datos energéticos
- NAP transporte para datos movilidad
- datos.gob.es para datasets abiertos
- BOE para datos normativos
- PNOA LiDAR para datos geoespaciales

### 5. Divulgación Transparente
- Código MIT + datos CC0
- Auditoria abierta por expertos
- Tests pytest para validación
- Manual divulgativo
- Changelog detallado

## Skills Creados (7 nuevos)

1. **multi-agent-orchestration** — Patrón de orquestación multi-agente con 11 agentes
2. **monte-carlo-simulation** — Simulación Monte Carlo bursátil frontend
3. **aurora-design-system** — Design System Ntizar Aurora v5.1
4. **static-digest-pipeline** — Pipeline de digest estático semanal
5. **gtfs-browser-parser** — Parser GTFS completo en navegador
6. **solar-shadow-computation** — Cálculo de sombras solares con Web Workers
7. **sistema-electrico-simulador** — Simulador sistema eléctrico español
8. **onnx-webgpu-inference** — Detección YOLO ONNX en navegador
9. **freehands-multimodal-control** — Control PC sin manos multimodal
10. **irpf-calculator** — Calculadora fiscal IRPF divulgativa

## Aprendizajes Clave

- Ntizar prioriza **transparencia total**: código abierto, datos CC0, auditoría pública
- El **Design System Aurora** se ha convertido en un producto reutilizable con CDN público
- La arquitectura **multi-agente** (Mastermind) es el núcleo de su flujo de trabajo
- **Cero dependencias de build** en la mayoría de proyectos: vanilla JS, CSS puro
- **GitHub Pages** es la plataforma de deploy preferida para proyectos frontend
- **Web Workers** para cálculos pesados sin bloquear UI es un patrón recurrente
- **IndexedDB con TTL** diferenciado para cache de datos financieros
- **Cadena de proxies CORS** como solución a APIs sin CORS
