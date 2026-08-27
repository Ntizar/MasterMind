---
name: stem-basics
version: "2.0.0"
description: "Ecosistema de ciencias básicas: navegación por los 40+ skills granulares de la clase stem/. Incluye matemáticas, física, química, biología, ciencias de la Tierra, dibujo técnico y metodología científica."
category: "stem"
tags: [stem, math, physics, chemistry, biology, earth-science, technical-drawing, scientific-method]
---

# Ciencias Básicas (STEM) — Umbrella

## Resumen

Navegación y orquestación de los **40+ skills granulares** de la clase `stem/`. Organizados por disciplina, cada skill es autocontenido con instrucciones, fórmulas, ejemplos y referencias.

## Estructura del ecosistema

### Matemáticas (`stem/math`)

| Skill | Contenido |
|-------|-----------|
| `math-numeros-algebra` | Números reales, potencias, raíces, factorización, MCD/MCM, conjuntos |
| `math-ecuaciones` | Ecuaciones 1º/2º grado, sistemas, inecuaciones, valor absoluto, irracionales |
| `math-funciones` | Dominio, rango, tipos (lineal, cuadrática, polinómica, racional, exp, log), composición |
| `math-logaritmos-exponenciales` | Funciones exp/log, propiedades, ecuaciones, crecimiento/decaimiento |
| `math-sucesiones-series` | Sucesiones (aritméticas, geométricas), series, sumatorios, convergencia |
| `math-trigonometria` | Razones trigonométricas, identidades, ecuaciones, teorema del seno/coseno |
| `math-vectores-matrices` | Vectores R2/R3, matrices, determinantes, autovalores, autovectores, diagonalización, SVD |
| `math-calculo-diferencial` | Límites, continuidad, derivadas, regla de cadena, optimización, Taylor/Maclaurin |
| `math-calculo-integral` | Integrales definidas/indefinidas, técnicas (sustitución, partes, fracciones parciales), áreas, volúmenes |
| `math-estadistica-probabilidad` | Estadística descriptiva/inferencial, distribución normal, intervalos, tests, Bayes, regresión |

### Física (`stem/physics`)

| Skill | Contenido |
|-------|-----------|
| `physics-cinematica` | MRU, MRUA, MCU, caída libre, tiro parabólico, composición de movimientos, relativo |
| `physics-dinamica` | 3 leyes Newton, fuerzas, rozamiento, tensión, planos inclinados, centro de masas, cantidad de movimiento |
| `physics-energia-trabajo` | Trabajo, energía cinética/potencial, conservación, potencia, fuerzas conservativas |
| `physics-fluidos` | Hidrostática, presión, Arquímedes, Bernoulli, caudal, viscosidad, tensión superficial |
| `physics-electrostatica` | Ley Coulomb, campo eléctrico, potencial, Gauss, capacitancia, dieléctricos |
| `physics-electrodinamica` | Corriente, Ley Ohm, resistencias, circuitos, potencia, Kirchhoff, circuitos RC |
| `physics-magnetismo` | Campo magnético, Ampere, Lorentz, Faraday, Lenz, autoinducción, materiales |
| `physics-ondas-sonido` | MHS, ondas mecánicas, sonido, Doppler, interferencia, ondas estacionarias |
| `physics-optica` | Reflexión, refracción, Snell, lentes, espejos, instrumentos, interferencia, difracción, polarización |
| `physics-termodinamica` | Leyes, gases ideales, ciclos, entropía, trabajo, calor, temperatura |
| `physics-expert` | Teoría cuántica de campos, partículas, cosmología, plasmas |

### Ingeniería (`stem/engineering`)

| Skill | Contenido |
|-------|-----------|
| `stem-mecanica-solidos` | Esfuerzos/deformaciones, Mohr, vigas, columnas, torsión, elasticidad |
| `stem-hidraulica` | Bernoulli, Darcy-Weisbach, Moody, bombas, caudal, redes de tuberías |
| `stem-transferencia` | Conducción, convección, radiación, intercambiadores, coeficientes |
| `stem-materiales` | Cristales, diagramas fase, ensayos mecánicos, fractura, tratamientos térmicos |
| `stem-control` | Dominio tiempo/frecuencia, función transferencia, estabilidad (Routh/Nyquist/Bode), PID |
| `stem-electronica` | Diodos, transistores BJT/FET, op-amps, filtros, lógica booleana, A/D |
| `stem-physics-engineering` | Ondas EM, circuitos CA/RLC, termodinámica avanzada, mecánica fluidos, electricidad |
| `stem-math-engineering` | Fourier, Laplace, EDOs 2º orden, cálculo multivariable, integrales múltiples, Green/Stokes/Gauss |
| `stem-probabilidad-estadistica-eng` | Variables aleatorias, distribuciones, inferencia, regresión, confiabilidad, colas |

### Dibujo Técnico (`stem/td`)

| Skill | Contenido |
|-------|-----------|
| `td-basics` | Normalización ISO, sistemas representación, acotación, escalas, rotulación |
| `td-proyecciones` | Proyección ortogonal, vistas principales, correspondencia, perspectivas |
| `td-diedrico-punto-recta-plano` | Sistema diédrico, pertenencia, incidencia, paralelismo, perpendicularidad |
| `td-abatimientos-giros` | Abatimiento, giros, cambio de plano, verdaderas magnitudes, distancias |
| `td-intermediate` | Geometría descriptiva, perspectivas axonométricas, intersecciones, superficies |
| `td-cortes-secciones` | Cortes totales/parciales/escalados, semicortes, secciones, roturas |
| `td-intersecciones-vm` | Recta-plano, plano-plano, recta-recta, verdaderas magnitudes |
| `td-planos-conjunto` | Despiece, lista piezas, marcas, vistas montaje/explosivas |
| `td-acotacion` | ISO 129, tipos de cota, funcionales, auxiliares, reglas |
| `td-tolerancias` | ISO 286/1101, GPS, ajustes agujero/eje, representación |
| `td-advanced` | Tolerancias geométricas avanzadas, piezas complejas, planos de conjunto |

## Cómo usar

### Flujo estándar

1. **Identificar la disciplina** del problema del usuario
2. **Cargar el skill granular** con `skill_view(name='stem/math/math-calculo-diferencial')`
3. **Seguir las instrucciones** del skill para resolver el problema
4. **Si el problema cruza disciplinas**, cargar múltiples skills

### Ejemplo

```
Usuario: "Resuelve esta integral por partes: ∫x·eˣdx"
Agente:
  1. Identifica: cálculo integral → skill 'math-calculo-integral'
  2. Carga: skill_view(name='math-calculo-integral')
  3. Sigue instrucciones del skill
```

### Si un skill granular no existe

Si la búsqueda semántica (ChromaDB) no encuentra un skill granular relevante:
1. Cargar `stem-basics` para ver la estructura completa
2. Verificar si el tema está cubierto por un skill más general
3. Si NO está cubierto: crear un nuevo skill granular siguiendo la convención `stem/<disciplina>/<tema-especifico>`

## Archivos de soporte

- `references/quick-reference.md` — Tabla rápida de fórmulas clave por disciplina
- `scripts/verify-stem-skills.py` — Script para verificar integridad de skills STEM

## Pitfalls

- **ChromaDB no detecta skills nuevos automáticamente** — después de crear/modificar cualquier skill STEM, ejecutar `bash scripts/indexar-skills.py` para re-indexar. Si ChromaDB no responde, arrancar antes: `bash scripts/start-chromadb.sh`.
- **Cargar el skill granular, no este umbrella** — este skill (`stem-basics`) es un índice de navegación. Para resolver problemas reales, cargar el skill específico con `skill_view(name='stem/math/math-calculo-diferencial')`.
- **No crear skills `skill-xxx` planos** — todos los skills STEM deben seguir la convención `stem/<disciplina>/<tema>` (ej: `stem/math/math-calculo-diferencial`). No crear como `skill-math-calculus` en la raíz de `agent/skills/`.
- **Subagentes pueden crear `skill.yaml`** — cuando se delega creación masiva, verificar que el archivo se llama `SKILL.md`. Si hay `skill.yaml`, renombrar.
- **ESIOS `time_trunc=hour` SUMA, no promedia** — si se usa en contextos STEM relacionados con energía, usar `convertEsiosValue()` de `esios-units.js`.

## Notas

- Los skills están en ChromaDB (colección `mastermind-skills`) para búsqueda semántica.
- Re-indexar después de crear/actualizar: `bash scripts/indexar-skills.py`
- Ver también: `chromadb-skills-vector-search` para el sistema de búsqueda semántica.
