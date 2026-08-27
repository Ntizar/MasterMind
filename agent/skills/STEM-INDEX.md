---
name: stem-basics
description: Ecosistema completo de ciencias básicas: 10 skills en 3 bloques (Matemáticas, Física/Química, Biología/Ciencias de la Tierra). 40+ áreas de conocimiento.
version: "1.0.0"
---

# 🧪 Ecosistema STEM — Índice General

Ecosistema completo de skills de ciencias básicas para Mastermind. **10 skills organizados en 3 bloques**, cubriendo 40+ áreas de conocimiento.

> Todo el contenido es autocontenido, en español, y ejecutable directamente por el agente.

---

## 📐 Bloque 1 — Matemáticas (4 skills)

| # | Skill | Archivo | Contenido principal | Palabras |
|---|-------|---------|-------------------|----------|
| 1 | **Fundamentos Matemáticos** | `skill-math-foundations/skill.md` | Álgebra (ecuaciones, polinomios, factorización), Geometría (euclidiana, coordenada), Trigonometría (funciones, identidades), Cálculo diferencial básico (límites, continuidad) | ~1,142 |
| 2 | **Estadística y Probabilidad** | `skill-math-statistics/skill.md` | Estadística descriptiva, Probabilidad (axiomas, Bayes), Distribuciones (binomial, Poisson, normal), Inferencia básica (intervalos, contraste) | ~1,251 |
| 3 | **Álgebra Lineal** | `skill-math-linear-algebra/skill.md` | Vectores en R²/R³, Matrices (determinante, inversa), Espacios vectoriales (base, dimensión), Autovalores y diagonalización | ~1,372 |
| 4 | **Cálculo** | `skill-math-calculus/skill.md` | Derivadas (reglas, optimización), Integrales (definida, indefinida, técnicas), EDOs, Series y sucesiones, Optimización multivariable | ~1,537 |

**Niveles:** Secundaria → Bachillerato → 1º-2º universidad

---

## ⚡ Bloque 2 — Física y Química (3 skills)

| # | Skill | Archivo | Contenido principal | Palabras |
|---|-------|---------|-------------------|----------|
| 5 | **Mecánica Clásica** | `skill-physics-mechanics/skill.md` | Cinemática (MRU, MRUA, MCU, tiro parabólico), Dinámica (3 leyes de Newton), Trabajo y energía, Termodinámica (leyes, gases ideales, entropía) | ~711 |
| 6 | **Electromagnetismo** | `skill-physics-electromagnetism/skill.md` | Electrostática (Coulomb, campo eléctrico), Magnetismo (Ampère, Faraday), Circuitos (Ohm, Kirchhoff, RC/RL/RLC), Ondas EM | ~848 |
| 7 | **Química Básica** | `skill-chemistry-basics/skill.md` | Estructura atómica, Tabla periódica, Enlaces químicos (iónico, covalente, metálico), Estequiometría, Reacciones químicas (cinética, equilibrio) | ~1,054 |

**Niveles:** Secundaria → Bachillerato → 1º-2º universidad

---

## 🧬 Bloque 3 — Biología y Ciencias de la Tierra (3 skills)

| # | Skill | Archivo | Contenido principal | Palabras |
|---|-------|---------|-------------------|----------|
| 8 | **Biología Celular** | `skill-biology-cell/skill.md` | Estructura celular (procariota/eucariota), Genética molecular (ADN/ARN), Evolución (selección natural), Ecología, División celular (mitosis, meiosis) | ~794 |
| 9 | **Ciencias de la Tierra** | `skill-earth-sciences/skill.md` | Geología (tectónica de placas, volcanes), Meteorología (presión, vientos, nubosidad), Oceanografía (corrientes, mareas), Climatología (cambio climático) | ~914 |
| 10 | **Método Científico** | `skill-scientific-method/skill.md` | Método científico completo, Diseño experimental (variables, controles), Análisis de datos, Errores experimentales, Comunicación científica, Pensamiento crítico | ~1,065 |

**Niveles:** Secundaria → Bachillerato → 1º universidad

---

## 📊 Resumen del ecosistema

- **Total de skills:** 10
- **Total de palabras:** ~10,688
- **Áreas de conocimiento:** 40+
- **Todos en español** ✅
- **Formato:** YAML frontmatter + markdown
- **Ubicación:** `agent/skills/`

---

## 🔍 Cómo usar

1. Cargar un skill específico con `skill_view(name='skill-math-foundations')`
2. Cada skill contiene instrucciones detalladas para el agente
3. Los ejemplos de uso muestran prompts reales que el usuario podría dar
4. Las referencias apuntan a libros y recursos académicos de confianza

---

## 📁 Estructura de directorios

```
agent/skills/
├── STEM-INDEX.md                    ← Este archivo
├── skill-math-foundations/
│   └── skill.md
├── skill-math-statistics/
│   └── skill.md
├── skill-math-linear-algebra/
│   └── skill.md
├── skill-math-calculus/
│   └── skill.md
├── skill-physics-mechanics/
│   └── skill.md
├── skill-physics-electromagnetism/
│   └── skill.md
├── skill-chemistry-basics/
│   └── skill.md
├── skill-biology-cell/
│   └── skill.md
├── skill-earth-sciences/
│   └── skill.md
└── skill-scientific-method/
    └── skill.md
```

---

*Creado: 2026-06-24 | 10 skills | 10,688 palabras | Hecho con (L) por David Antizar*
