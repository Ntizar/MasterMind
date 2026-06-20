# 🧪 Índice STEM — Ecosistema de Skills de Ciencias Básicas

> **Mastermind** — Ecosistema completo de 10 skills STEM para el agente Hermes.
> Todos los skills son autocontenidos, ejecutables y están en español.

## Bloque 1 — Matemáticas (4 skills)

| # | Skill | Archivo | Tamaño | Líneas | Descripción |
|---|-------|---------|--------|--------|-------------|
| 1 | **Math Foundations** | `skill-math-foundations/SKILL.md` | 15 KB | 233 | Álgebra, geometría euclidiana, trigonometría, cálculo diferencial básico |
| 2 | **Math Statistics** | `skill-math-statistics/SKILL.md` | 16 KB | 264 | Estadística descriptiva, probabilidad, distribuciones, inferencia |
| 3 | **Math Linear Algebra** | `skill-math-linear-algebra/SKILL.md` | 18 KB | 307 | Vectores, matrices, espacios vectoriales, autovalores, sistemas lineales |
| 4 | **Math Calculus** | `skill-math-calculus/SKILL.md` | 21 KB | 345 | Derivadas avanzadas, integrales, EDOs, optimización, series/Taylor |

## Bloque 2 — Física y Química (3 skills)

| # | Skill | Archivo | Tamaño | Líneas | Descripción |
|---|-------|---------|--------|--------|-------------|
| 5 | **Physics Mechanics** | `skill-physics-mechanics/SKILL.md` | 11 KB | 318 | Cinemática, dinámica, termodinámica, trabajo y energía |
| 6 | **Physics Electromagnetism** | `skill-physics-electromagnetism/SKILL.md` | 13 KB | 407 | Electrostática, magnetismo, circuitos, ondas EM |
| 7 | **Chemistry Basics** | `skill-chemistry-basics/SKILL.md` | 18 KB | 494 | Estructura atómica, tabla periódica, enlaces, estequiometría, reacciones |

## Bloque 3 — Biología y Ciencias de la Tierra (3 skills)

| # | Skill | Archivo | Tamaño | Líneas | Descripción |
|---|-------|---------|--------|--------|-------------|
| 8 | **Biology Cell** | `skill-biology-cell/SKILL.md` | 32 KB | 467 | Biología celular, genética, evolución, ecología |
| 9 | **Earth Sciences** | `skill-earth-sciences/SKILL.md` | 44 KB | 635 | Geología, meteorología, oceanografía, climatología |
| 10 | **Scientific Method** | `skill-scientific-method/SKILL.md` | 35 KB | 535 | Método científico, diseño experimental, análisis de datos, comunicación |

## Resumen

- **Total:** 10 skills
- **Tamaño total:** ~223 KB
- **Total líneas:** ~4.325
- **Bloques:** 3 (Matemáticas, Física/Química, Biología/Tierra)
- **Idioma:** Español
- **Estado:** ✅ Todos verificados y funcionales

## Referencias cruzadas con skills STEM existentes

Los nuevos skills referencian los skills STEM ya existentes en `/hermes-home/skills/stem/`:

- **Math:** `math-calculo-diferencial`, `math-calculo-integral`, `math-ecuaciones`, `math-funciones`, `math-logaritmos-exponenciales`, `math-numeros-algebra`, `math-sucesiones-series`, `math-trigonometria`, `math-vectores-matrices`, `math-estadistica-probabilidad`, `math-estadistica-probabilidad-eng`
- **Physics:** `physics-cinematica`, `physics-dinamica`, `physics-energia-trabajo`, `physics-fluidos`, `physics-termodinamica`, `physics-electrodinamica`, `physics-electrostatica`, `physics-magnetismo`, `physics-ondas-sonido`, `physics-expert`
- **Chemistry:** Referencias a química general (sin skill específico existente)
- **Biology:** Referencias a biología general (sin skills específicos existentes)
- **Earth:** Referencias a ciencias de la tierra (sin skills específicos existentes)
- **Scientific Method:** Referencias a `math-estadistica-probabilidad`, `math-estadistica-probabilidad-eng`

## Estructura común de cada skill

Cada SKILL.md contiene:
- YAML frontmatter (`name`, `version`, `category`, `description`, `tags`, `author`)
- Descripción clara del alcance
- Temas cubiertos detallados con subtemas y fórmulas
- Instrucciones paso a paso para el agente
- Ejemplos de prompts (4-10 por skill)
- Referencias cruzadas a otros skills
- Sección "Pitfalls" con errores comunes
- Sección "Cuándo usar este skill"
