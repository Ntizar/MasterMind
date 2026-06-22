---
name: STEM-INDEX
version: "1.0.0"
---

# 📚 Índice de Skills STEM — Ciencias Básicas

**Ecosistema completo de 10 skills** para enseñar y resolver problemas de ciencias básicas.
Organizado en 3 bloques temáticos, cubriendo desde fundamentos hasta aplicaciones avanzadas.

---

## Bloque 1 — Matemáticas (4 skills)

| # | Skill | Descripción |
|---|-------|-------------|
| 1 | `skill-math-foundations` | Álgebra, geometría, trigonometría y cálculo diferencial básico |
| 2 | `skill-math-statistics` | Estadística descriptiva, probabilidad, distribuciones e inferencia |
| 3 | `skill-math-linear-algebra` | Vectores, matrices, espacios vectoriales, autovalores y diagonalización |
| 4 | `skill-math-calculus` | Derivadas, integrales, EDOs y optimización |

## Bloque 2 — Física y Química (3 skills)

| # | Skill | Descripción |
|---|-------|-------------|
| 5 | `skill-physics-mechanics` | Mecánica clásica, cinemática, dinámica, energía y termodinámica |
| 6 | `skill-physics-electromagnetism` | Electrostática, magnetismo, circuitos, inducción y ondas EM |
| 7 | `skill-chemistry-basics` | Tabla periódica, enlaces, estequiometría, reacciones y soluciones |

## Bloque 3 — Biología y Ciencias de la Tierra (3 skills)

| # | Skill | Descripción |
|---|-------|-------------|
| 8 | `skill-biology-cell` | Biología celular, genética, evolución y ecología |
| 9 | `skill-earth-sciences` | Geología, meteorología, oceanografía y climatología |
| 10 | `skill-scientific-method` | Método científico, diseño experimental y análisis de datos |

---

## Estadísticas

- **Total de skills**: 10
- **Tamaño total**: ~39.0 KB
- **Bloques**: 3
- **Skills por bloque**: 4 / 3 / 3
- **Rango educativo**: ESO → Bachillerato → Universidad

## Archivos

Todos los archivos están en `/hermes-home/skills/`:

```
skill-math-foundations.md      (3,037 bytes)
skill-math-statistics.md       (3,181 bytes)
skill-math-linear-algebra.md   (3,204 bytes)
skill-math-calculus.md         (3,686 bytes)
skill-physics-mechanics.md     (3,726 bytes)
skill-physics-electromagnetism.md (3,584 bytes)
skill-chemistry-basics.md      (3,510 bytes)
skill-biology-cell.md          (3,871 bytes)
skill-earth-sciences.md        (4,188 bytes)
skill-scientific-method.md     (5,036 bytes)
```

## Estructura de cada skill

Cada skill incluye:
- **Descripción** general del área temática
- **Instrucciones** paso a paso para el agente
- **Subtemas** identificados y clasificados
- **Formato de respuesta** recomendado
- **Niveles de profundidad** (básico/intermedio/avanzado)
- **Ejemplos de uso** con resolución completa
- **Referencias útiles** (Khan Academy, libros, herramientas)
- **Pitfalls críticos** (errores comunes a evitar)

## Uso

Cargar un skill específico con:
```
skill_view(name='skill-math-foundations')
```

El agente cargará el skill automáticamente cuando detecte una petición relevante en el dominio correspondiente.

---

*Creado: 2026-06-22 | Ecosistema STEM completo: 10 skills, 3 bloques*
