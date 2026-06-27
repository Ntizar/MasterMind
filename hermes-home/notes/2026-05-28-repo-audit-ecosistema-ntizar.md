# Auditoría del Ecosistema Ntizar - 28/05/2026

## Resumen

Exploración completa de los 26 repositorios del usuario Ntizar en GitHub. Se identificaron patrones de desarrollo, tecnologías recurrentes y oportunidades de aprendizaje.

## Ecosistema General

- **Total repos**: 26
- **Lenguajes principales**: TypeScript, Python, JavaScript, HTML, CSS
- **Hosting**: GitHub Pages (mayoría), Vercel, NaN.builders
- **Design System**: Ntizar Aurora v5.1 (CSS puro, Liquid Glass, CDN público)
- **Arquitectura multi-agente**: Ntizar Mastermind v3 (11 agentes, Ebbinghaus)

## Categorías de Proyectos

### 1. Infraestructura del Agente (3)
| Repo | Descripción |
|------|-------------|
| mastermind | Knowledge repository - aprendizaje y skills extraction |
| inicio-en-nan | Guía paso a paso NaN.builders |
| NtizarBrainMasterMind | Framework multi-agente (11 agentes, Obsidian+OpenCode) |

### 2. Datos y Monitoreo (4)
| Repo | Descripción |
|------|-------------|
| datos-gob-watch | Radar semanal de datasets de datos.gob.es |
| IRPFdibujitos | Calculadora IRPF España 2012-2026 con gráficas |
| Accidentes2024 | Megadashboard de accidentes con víctimas en España |
| hackaton1 | TrEnergIA - gemelo energético ferroviario |

### 3. Energía y Medio Ambiente (3)
| Repo | Descripción |
|------|-------------|
| SistemaElectricoFuturo | Simulador sistema eléctrico español 2026-2035 (17 escenarios) |
| rail-lidar-qa-mvp | Validación LiDAR ferroviaria con nubes de puntos 3D |
| Voynich_Solving | Descifrado estructural del Manuscrito Voynich |

### 4. Geoespacial y Maps (5)
| Repo | Descripción |
|------|-------------|
| solmad | Buscador 3D de terrazas con sol en Madrid (6.200+ terrazas) |
| farosspain | Mapa interactivo de faros de España |
| OrbitMixer | Comparador de imágenes satelitales Sentinel-2 |
| MonteCarloInversion | Simulador Monte Carlo de riesgos bursátiles |
| PacManMadrid | Visualización tráfico EMT Madrid estilo Pacman |

### 5. Productividad y Utilidades (4)
| Repo | Descripción |
|------|-------------|
| weekPlan | Planificador semanal con export Excel/ICS/CSV |
| FamilyTree | Editor visual de árboles genealógicos |
| Rumby | Plataforma multimodal de movilidad (Madrid → replicable) |
| nap-dashboard | Dashboard React+Vite para datos NAP |

### 6. Accesibilidad y Hands-Free (1)
| Repo | Descripción |
|------|-------------|
| FreeHands | Control PC sin manos: gaze + gestures + voice |

### 7. Design System (2)
| Repo | Descripción |
|------|-------------|
| Ntizar-Aurora | Design System Liquid Glass v5.1 (CSS puro, 6 skins, CDN) |
| MetalHoverLab | Playground de relieves metalizados con cursor |

### 8. Experimentos y Misceláneos (4)
| Repo | Descripción |
|------|-------------|
| OrbitMixer | Comparador satelital con gestos |
| empleady | (sin README, CSS) |
| lopezaesthetics | (sin README, solo index.html) |
| weekPlan | Planificador semanal |

## Patrones Detectados

### 1. Filosofía "Zero Build"
La mayoría de proyectos usan HTML/CSS/JS vanilla sin npm, sin bundler, sin build step. Solo proyectos complejos (solmad, Rumby, PacManMadrid) usan Vite/React/Next.js.

### 2. GitHub Pages como Hosting Principal
Prácticamente todos los proyectos se deployan en GitHub Pages con workflows automáticos. Excepciones: solmad (Vercel), Nap Dashboard (Vercel).

### 3. Ntizar Aurora como Design System Unificado
Todos los proyectos visuales usan Aurora v5.1 con CDN público. Paleta: azul #2563eb + naranja #f97316. Efecto Liquid Glass como lenguaje visual consistente.

### 4. Data Pipeline Pattern
Patrón recurrente: API externa → script Node.js/Python → JSON estático → frontend lee JSON → deploy estático.

### 5. Web Workers para Cálculos Pesados
Usado en solmad (sombras) y MonteCarloInversion (5 modelos estocásticos en paralelo).

### 6. Leaflet + Tiles Libres
Leaflet como librería de mapas estándar, con tiles de CARTO/OSM sin necesidad de API keys.

### 7. Contribuciones vía PRs
Solmad usa un sistema donde los usuarios aportan datos que van a una rama de review → PR → merge.

## Tecnologías Clave Identificadas

| Tecnología | Uso | Reutilizable |
|------------|-----|-------------|
| Ntizar Aurora CSS | Design system unificado | Sí - todos los proyectos |
| Leaflet + CARTO | Mapas interactivos | Sí - proyectos geoespaciales |
| SunCalc | Cálculo solar | Sí - solmad y derivados |
| Overpass API | Datos de edificios OSM | Sí - proyectos geoespaciales |
| Web Workers + Comlink | Cálculos sin bloquear UI | Sí - proyectos con cálculos pesados |
| MediaPipe | Hand/face/gesture recognition | Sí - FreeHands y derivados |
| WebGazer.js | Gaze tracking | Sí - accesibilidad |
| faster-whisper | STT local | Sí - proyectos con voz |
| PyAutoGUI | Control de OS | Sí - FreeHands |
| Earth Search STAC | Imágenes satelitales | Sí - OrbitMixer |
| TiTiler.xyz | COG→PNG render | Sí - proyectos satelitales |
| OpenTopoData | Elevation/DEM | Sí - proyectos geoespaciales |
| Nominatim | Reverse geocoding | Sí - proyectos geoespaciales |
| Next.js | Apps SSR/modulares | Sí - Rumby y similares |
| Zustand | Estado global React | Sí - proyectos React |
| Tailwind | Estilos utility-first | Sí - solmad |

## Aprendizajes Importantes

### 1. Arquitectura Mastermind v3
- Dos capas separadas: Obsidian (documentación) + OpenCode (ejecución)
- 11 agentes con responsabilidades únicas
- Asignación de modelos por rol (no usar el más caro para todo)
- Memoria con decaimiento Ebbinghaus (R(t) = a / (log(t+1))^b + c)
- 4 skills de dominio activos: software-dev, dashboard-dev, web-deploy, pwa-android

### 2. Aurora v5.1 - Agent-Ready
- AGENTS.md + INDEX.md (~5k tokens) en vez de 50k del CSS completo
- CDN público en jsdelivr
- 6 skins: aurora, sunset, midnight, ocean, citrus, contrast
- OKLCH para colores perceptualmente uniformes
- Namespaced: todo dentro de `.nz`

### 3. Solmad - Algoritmo de Sombras
- Overpass API por zona (no todo Madrid de golpe)
- Alturas estimadas: `building:levels * 3.2m` o fallback 10m
- Grid indexado en Web Worker para ray tracing solar
- Cache por terraza, día del año, franja 15 min

### 4. FreeHands - Pipeline Multimodal
- WebGazer (gaze) + MediaPipe (gestures) + faster-whisper (voice)
- Todo local, sin cloud
- Calibración por usuario
- Duck test para validación end-to-end

### 5. SistemaElectricoFuturo
- 17 escenarios realistas para España
- Simulación 8.760 horas/año + trayectoria 2026-2035
- Calendario nuclear real ENRESA
- Almacenamiento avanzado: degradación baterías, bombeo estacional, V2G
- Política energética: tope ibérico, CfDs, peajes dinámicos, PVPC

### 6. Voynich_Solving - Lecciones de Investigación
- Hipótesis estructural: defendible (notación farmaceutica medieval)
- Hipótesis semántica: no demostrada (18.7% cobertura)
- Benchmark: fixed-F1 ~41-60% vs baselines 64-87%
- Lección: separar estructura de semántica en investigación computacional

## Oportunidades Identificadas

1. **Unificar skills existentes** con los nuevos creados (8 skills nuevos)
2. **Explorar Rumby** más a fondo - arquitectura modular de conectores
3. **Aprender de MonteCarloInversion** - modelos estocásticos en browser
4. **Revisar TrEnergIA** - optimización de consumo energético ferroviario
5. **Conectar FreeHands con Hermes** - control por gestos del agente

## Skills Creados Esta Sesión

1. `ntizar-mastermind-architecture` - Arquitectura multi-agente v3
2. `solmad-solar-shadow` - Cálculo de sol y sombras
3. `ntizar-aurora-css` - Design System v5.1
4. `freehands-gesture-control` - Control sin manos
5. `ntizar-static-web-patterns` - Patrones web estáticos
6. `nan-deploy-guide` - Guía deploy NaN.builders
7. `orbitmixer-satellite-compare` - Comparador satelital
8. `datos-gob-watch` - Radar semanal de datasets

Total: 8 skills nuevos creados.
