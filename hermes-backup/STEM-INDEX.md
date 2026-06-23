# Índice de Skills STEM — Ciencias Básicas

> **Fecha de creación:** 2026-06-23
> **Total de skills:** 10
> **Bloques:** 3 (Matemáticas, Física/Química, Biología/Ciencias de la Tierra)

---

## 📐 BLOQUE 1 — Matemáticas (4 skills)

| # | Skill | Categoría | Descripción |
|---|-------|-----------|-------------|
| 1 | `skill-math-foundations` | stem/math | Álgebra, geometría, trigonometría, cálculo diferencial básico |
| 2 | `skill-math-statistics` | stem/math | Estadística descriptiva, probabilidad, distribuciones, inferencia |
| 3 | `skill-math-linear-algebra` | stem/math | Vectores, matrices, espacios vectoriales, transformaciones lineales, autovalores |
| 4 | `skill-math-calculus` | stem/math | Derivadas, integrales, EDOs, optimización, series, cálculo multivariable |

## ⚛️ BLOQUE 2 — Física y Química (3 skills)

| # | Skill | Categoría | Descripción |
|---|-------|-----------|-------------|
| 5 | `skill-physics-mechanics` | stem/physics | Mecánica clásica, cinemática, dinámica, trabajo y energía, termodinámica |
| 6 | `skill-physics-electromagnetism` | stem/physics | Electrostática, magnetismo, circuitos, ondas electromagnéticas, ecuaciones de Maxwell |
| 7 | `skill-chemistry-basics` | stem/chemistry | Estequiometría, enlaces, reacciones, tabla periódica, equilibrio, pH |

## 🧬 BLOQUE 3 — Biología y Ciencias de la Tierra (3 skills)

| # | Skill | Categoría | Descripción |
|---|-------|-----------|-------------|
| 8 | `skill-biology-cell` | stem/biology | Biología celular, bioquímica, genética, evolución, ecología |
| 9 | `skill-earth-sciences` | stem/earth-science | Geología, meteorología, oceanografía, climatología, astrogeología |
| 10 | `skill-scientific-method` | stem/research | Método científico, diseño experimental, análisis de datos, incertidumbre |

---

## Mapa de interconexiones

```
                    ┌─────────────────────┐
                    │  MATEMÁTICAS (4)     │
                    ├─────────────────────┤
                    │ foundations ────────┼──→ base para TODO
                    │ statistics ─────────┼──→ análisis de datos
                    │ linear-algebra ─────┼──→ vectores, campos
                    │ calculus ───────────┼──→ física, optimización
                    └─────────┬───────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │  FÍSICA (2)     │ │  QUÍMICA (1)    │ │  BIOLOGÍA (1)   │
    ├─────────────────┤ ├─────────────────┤ ├─────────────────┤
    │ mechanics ──────┼→│ chemistry ──────┼→│ biology ────────┤
    │ electromagnetism│ │                 │ │                 │
    └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
             │                   │                   │
             ▼                   ▼                   ▼
    ┌─────────────────────────────────────────────────────────┐
    │              CIENCIAS DE LA TIERRA (2)                   │
    ├─────────────────────────────────────────────────────────┤
    │ earth-sciences ←──→ ecosystems + ciclos biogeoquímicos  │
    │ scientific-method ←──→ methodology for ALL sciences     │
    └─────────────────────────────────────────────────────────┘
```

## Dependencias recomendadas (orden de estudio)

1. **skill-math-foundations** → base absoluta
2. **skill-math-statistics** → herramientas de análisis
3. **skill-math-linear-algebra** → vectores y matrices
4. **skill-math-calculus** → cálculo avanzado
5. **skill-physics-mechanics** → aplica matemáticas a fenómenos físicos
6. **skill-physics-electromagnetism** → física avanzada
7. **skill-chemistry-basics** → química fundamental
8. **skill-biology-cell** → biología celular
9. **skill-earth-sciences** → ciencias de la Tierra
10. **skill-scientific-method** → metodología transversal (puede usarse en paralelo)
