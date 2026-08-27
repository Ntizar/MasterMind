# Ecosistema STEM — Limpieza y Consolidación

## Contexto

El cronjob `STEM skills ecosystem` (b1402bbcdf71) creó un conjunto de skills STEM pero dejó el sistema en un estado caótico: duplicación masiva entre skills granulares dentro de `stem/` y skills "agregados" sueltos en `agent/skills/`.

## Problema detectado

- **43 skills granulares** en `agent/skills/stem/` (bien organizados por subtema)
- **7+ skills agregados** sueltos en `agent/skills/` que duplicaban contenido de los anteriores
- Cronjob diario (`repeat: "forever"`) sin criterio de "nuevo vs existente"

## Skills eliminados (duplicados)

1. `skill-math-foundations` → duplicaba math-numeros-algebra + math-funciones + math-trigonometria + math-ecuaciones
2. `skill-math-calculus` → duplicaba math-calculo-diferencial + math-calculo-integral
3. `skill-math-statistics` → duplicaba math-estadistica-probabilidad
4. `skill-math-linear-algebra` → duplicaba math-vectores-matrices
5. `skill-physics-mechanics` → duplicaba physics-cinematica + physics-dinamica + physics-energia-trabajo + physics-termodinamica
6. `skill-physics-electromagnetism` → duplicaba physics-electrostatica + physics-electrodinamica + physics-magnetismo
7. `skill-scientific-method` → duplicaba contenido existente en otras skills

## Estructura final del ecosistema STEM (43 skills)

### 📐 Matemáticas (10)
- math-numeros-algebra — Números reales, álgebra elemental, factorización
- math-ecuaciones — Ecuaciones lineales, cuadráticas, sistemas
- math-funciones — Tipos de funciones, composición, inversión
- math-logaritmos-exponenciales — Exponenciales, logaritmos
- math-trigonometria — Razones trigonométricas, identidades
- math-sucesiones-series — Sucesiones, series, convergencia
- math-calculo-diferencial — Límites, derivadas, optimización
- math-calculo-integral — Integrales, técnicas de integración
- math-vectores-matrices — Vectores, matrices, autovalores
- math-estadistica-probabilidad — Estadística, probabilidad, Bayes

### ⚛️ Física (11)
- physics-cinematica — MRU, MRUA, MCU, tiro parabólico
- physics-dinamica — Leyes de Newton, fuerzas, rozamiento
- physics-energia-trabajo — Trabajo, energía, conservación
- physics-termodinamica — Gases ideales, ciclos, entropía
- physics-fluidos — Hidrostática, Bernoulli, Arquímedes
- physics-electrostatica — Coulomb, campo eléctrico, Gauss
- physics-electrodinamica — Ohm, Kirchhoff, circuitos RC/RLC
- physics-magnetismo — Ampere, Lorentz, Faraday, Lenz
- physics-ondas-sonido — Onda armónica, Doppler, interferencia
- physics-optica — Refracción, lentes, espejos, difracción
- physics-expert — Teoría cuántica, partículas, cosmología

### 🔧 Ingeniería (7)
- stem-mecanica-solidos — Esfuerzos, Mohr, vigas, torsión
- stem-electronica — Transistores, op-amps, lógica digital
- stem-control — PID, Nyquist, Bode, estabilidad
- stem-materiales — Diagramas de fase, ensayos, tratamientos
- stem-hidraulica — Bernoulli, Darcy-Weisbach, bombas
- stem-transferencia — Conducción, convección, radiación
- stem-physics-engineering — Ondas EM, circuitos CA, termodinámica avanzada

### 📐🔬 Matemáticas Ingeniería (1)
- stem-math-engineering — Fourier, Laplace, cálculo multivariable

### 📏 Dibujo Técnico (11)
- td-basics — Normalización ISO, sistemas básicos
- td-proyecciones — Vistas principales, ortogonal
- td-diedrico-punto-recta-plano — Sistema diédrico
- td-abatimientos-giros — Verdaderas magnitudes
- td-cortes-secciones — Cortes, secciones, roturas
- td-intersecciones-vm — Intersecciones, VM
- td-perspectivas — Isométrica, caballera, dimétrica
- td-planos-conjunto — Despiece, listas, montaje
- td-acotacion — Acotación ISO 129
- td-tolerancias — Tolerancias ISO 286/1101
- td-advanced — Normalización avanzada, GPS

## Lecciones aprendidas

1. **Los cronjobs sin memoria repiten trabajo** — Sin `context_from` ni criterio de "qué ya existe", un cronjob diario va a hacer bucle infinito de lo mismo
2. **Skills granulares > skills agregados** — Para ChromaDB es mejor tener 43 skills específicos que 7 agregados. La búsqueda semántica encuentra justo lo que necesitas
3. **La acumulación sin limpieza es deuda técnica** — Cada skill duplicado es ruido en ChromaDB y confusión en la búsqueda
4. **Los cronjobs deben ser on-demand o tener criterio** — O bien hacer un cronjob que compare estado actual vs objetivo, o bien eliminarlo cuando ya cumplió su función

## Cronjob eliminado

- `STEM skills ecosystem` (b1402bbcdf71) — borrado por ser redundante y repetitivo
- No se reprogramará — la consolidación STEM está completa
