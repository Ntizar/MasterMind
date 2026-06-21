---
name: STEM-INDEX
version: "1.0.0"
description: Índice maestro de todos los skills STEM del ecosistema Mastermind.
---

# Índice de Skills STEM

## Ecosistema completo — 10 skills en 3 bloques

---

### BLOQUE 1 — Matemáticas (4 skills)

| # | Skill | Descripción |
|---|-------|-------------|
| 1 | `skill-math-foundations` | Álgebra, geometría euclidiana, trigonometría, números reales, potencias y raíces |
| 2 | `skill-math-statistics` | Estadística descriptiva, probabilidad, distribuciones (Binomial, Normal, Poisson), inferencia |
| 3 | `skill-math-linear-algebra` | Vectores, matrices, espacios vectoriales, transformaciones lineales, autovalores |
| 4 | `skill-math-calculus` | Derivadas, integrales, EDOs, optimización, series de Taylor |

---

### BLOQUE 2 — Física y Química (3 skills)

| # | Skill | Descripción |
|---|-------|-------------|
| 5 | `skill-physics-mechanics` | Cinemática, dinámica, trabajo y energía, rotación, gravitación, termodinámica |
| 6 | `skill-physics-electromagnetism` | Electrostática, circuitos, magnetismo, inducción, ondas electromagnéticas |
| 7 | `skill-chemistry-basics` | Estequiometría, enlaces, reacciones, tabla periódica, ácidos y bases, equilibrio |

---

### BLOQUE 3 — Biología y Ciencias de la Tierra (3 skills)

| # | Skill | Descripción |
|---|-------|-------------|
| 8 | `skill-biology-cell` | Biología celular, bioquímica, genética, evolución, ecología |
| 9 | `skill-earth-sciences` | Geología, meteorología, climatología, oceanografía, hidrología |
| 10 | `skill-scientific-method` | Método científico, diseño experimental, análisis de datos, incertidumbre |

---

## Estructura de directorios

```
/hermes-home/skills/
├── skill-math-foundations/
│   └── SKILL.md
├── skill-math-statistics/
│   └── SKILL.md
├── skill-math-linear-algebra/
│   └── SKILL.md
├── skill-math-calculus/
│   └── SKILL.md
├── skill-physics-mechanics/
│   └── SKILL.md
├── skill-physics-electromagnetism/
│   └── SKILL.md
├── skill-chemistry-basics/
│   └── SKILL.md
├── skill-biology-cell/
│   └── SKILL.md
├── skill-earth-sciences/
│   └── SKILL.md
├── skill-scientific-method/
│   └── SKILL.md
└── STEM-INDEX.md  ← este archivo
```

## Resumen

- **Total de skills:** 10
- **Total de bloques:** 3
- **Categorías:** math (4), physics (2), chemistry (1), biology (1), earth-science (1), research (1)
- **Estado:** ✅ Todos creados y verificados

## Notas de uso

- Cada skill es **autocontenido** y puede cargarse independientemente
- Los skills siguen el formato estándar: YAML frontmatter + markdown
- Cada uno incluye: descripción, instrucciones, ejemplos de uso, referencias, pitfalls
- Cargar con `skill_view(name='skill-math-foundations')` (o el nombre correspondiente)

---

*Generado el 2026-06-21 — 10 skills STEM completos*
