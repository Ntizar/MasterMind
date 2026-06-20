---
name: skill-scientific-method
version: 1.0.0
category: STEM/Metodología Científica
description: "Método científico, diseño experimental, análisis de datos y comunicación científica — Observación, hipótesis, experimentación, conclusión, variables, controles, muestreo, aleatorización, estadística descriptiva, gráficos, significación estadística, informes, papers, revisión por pares."
tags: [método científico, hipótesis, experimentación, variables, controles, muestreo, aleatorización, estadística descriptiva, gráficos, significación estadística, informes, revisión por pares, diseño experimental]
author: Mastermind STEM
---

# skill-scientific-method — Método Científico, Diseño Experimental, Análisis de Datos y Comunicación Científica

## Descripción

Este skill proporciona al agente las capacidades para guiar a usuarios en el **método científico**, el **diseño experimental**, el **análisis de datos** y la **comunicación científica**. Es el skill especializado del ecosistema STEM de Mastermind para la metodología de la ciencia.

Este skill es **autocontenido**: el agente puede ejecutarlo sin consultar otros documentos. Sin embargo, hace referencia a skills STEM existentes para profundización en temas específicos.

## Temas Cubiertos

### 1. Método Científico

#### Etapas del método científico
El método científico es un conjunto de pasos sistemáticos para adquirir conocimiento válido y fiable:

1. **Observación**: detectar un fenómeno o problema mediante los sentidos o instrumentos. Plantear preguntas.
   - **Observación cualitativa**: descripción sin números (ej. "la planta creció más").
   - **Observación cuantitativa**: descripción con números (ej. "la planta creció 5 cm").
2. **Planteamiento del problema**: formular una pregunta clara y específica sobre el fenómeno observado.
   - Buena pregunta: "¿Cómo afecta la concentración de fertilizante NPK al crecimiento de Phaseolus vulgaris?"
   - Mala pregunta: "¿Por qué crecen las plantas?" (demasiado vaga).
3. **Investigación previa**: revisar la literatura existente para no repetir conocimientos ya establecidos.
4. **Formulación de la hipótesis**: propuesta tentativa y comprobable que responde a la pregunta.
   - **Hipótesis nula (H₀)**: no hay efecto/diferencia. "La concentración de fertilizante NO afecta el crecimiento."
   - **Hipótesis alternativa (H₁)**: hay efecto/diferencia. "La concentración de fertilizante SÍ afecta el crecimiento."
   - **Hipótesis de trabajo**: versión específica y direccional de H₁. "A mayor concentración de NPK, mayor crecimiento."
5. **Experimentación**: diseñar y realizar un experimento para probar la hipótesis.
   - Manipular la **variable independiente**.
   - Medir la **variable dependiente**.
   - Controlar las **variables extrañas/confundidoras**.
6. **Análisis de datos**: procesar los datos obtenidos (estadística descriptiva e inferencial).
7. **Conclusiones**: interpretar los resultados en relación con la hipótesis.
   - **Aceptar H₀** (no rechazar): los datos no muestran evidencia de efecto.
   - **Rechazar H₀** (aceptar H₁): los datos muestran evidencia estadística de efecto.
   - Las conclusiones deben ser **cautelosas**: la ciencia no "prueba" hipótesis, las respalda o las refuta con evidencia.
8. **Comunicación de resultados**: publicar los hallazgos para que la comunidad científica los revise y replique.

#### Características del método científico
- **Empírico**: se basa en observación y experimentación.
- **Objetivo**: minimiza la subjetividad.
- **Reproducible**: otros investigadores deben poder replicar el experimento.
- **Falsable** (Popper): la hipótesis debe poder ser refutada potencialmente.
- **Provisional**: las conclusiones son tentativas y se revisan con nueva evidencia.
- **Sistemático**: sigue un procedimiento ordenado y documentado.

#### Tipos de investigación
- **Experimental**: el investigador manipula activamente variables (laboratorio, campo controlado).
- **Observacional**: el investigador observa sin manipular (ecología, astronomía, epidemiología).
- **Descriptiva**: describe características de un fenómeno (inventarios, censos).
- **Correlacional**: estudia la relación entre variables sin establecer causalidad.
- **Explicativa**: busca las causas de un fenómeno (causalidad).

### 2. Diseño Experimental

#### Variables
- **Variable independiente (VI)**: la que el investigador manipula o selecciona. Es la "causa" hipotética.
  - Ej.: concentración de fertilizante, temperatura, dosis de medicamento.
- **Variable dependiente (VD)**: la que se mide como respuesta. Es el "efecto" hipotético.
  - Ej.: altura de la planta, tasa de reacción, presión arterial.
- **Variables extrañas/confundidoras**: factores que pueden afectar la VD pero no se están estudiando. Deben controlarse.
  - Ej.: luz, humedad, tipo de suelo (en el experimento de fertilizante).
- **Variables de control**: variables que se mantienen constantes durante todo el experimento.
- **Variables intervinientes**: variables que median la relación VI→VD.
- **Variables moderadoras**: variables que modifican la intensidad de la relación VI→VD.

#### Controles
- **Grupo control (testigo)**: grupo que NO recibe el tratamiento experimental. Sirve como referencia.
  - **Control negativo**: no recibe ningún tratamiento (ej. agua sin fertilizante).
  - **Control positivo**: recibe un tratamiento conocido para producir un efecto (ej. fertilizante comercial estándar).
- **Control interno**: medidas tomadas para asegurar que los cambios observados se deben a la VI y no a factores externos.
- **Control externo**: medidas para asegurar que los resultados son generalizables.

#### Muestreo
- **Muestra**: subconjunto de la población estudiada.
- **Población**: conjunto total de individuos o elementos de interés.
- **Muestreo probabilístico** (cada elemento tiene probabilidad conocida de ser seleccionado):
  - **Aleatorio simple**: todos tienen igual probabilidad (sorteo, tabla de números aleatorios).
  - **Estratificado**: se divide en estratos (ej. por edad) y se muestrea dentro de cada estrato.
  - **Por conglomerados**: se seleccionan grupos enteros (ej. escuelas, barrios).
  - **Sistemático**: cada k-ésimo elemento (ej. cada 10ª persona).
- **Muestreo no probabilístico** (probabilidad desconocida):
  - **Conveniencia**: se seleccionan los más accesibles.
  - **Intencional/por juicio**: el investigador selecciona según criterio.
  - **Balde de bola de nieve**: los participantes reclutan a otros.
- **Tamaño de muestra**:
  - **Ley de los grandes números**: a mayor n, los resultados son más estables.
  - **Análisis de potencia**: calcula el tamaño mínimo necesario para detectar un efecto real.
  - **Regla práctica**: n ≥ 30 para aproximación normal (teorema central del límite).

#### Aleatorización
- **Asignación aleatoria**: los sujetos se asignan aleatoriamente a grupos (experimental y control).
  - Elimina sesgos de selección.
  - Distribuye las variables extrañas de forma equilibrada entre grupos.
- **Orden aleatorio**: en experimentos con tratamientos múltiples, el orden de aplicación se aleatoriza.
  - Evita efectos de fatiga, aprendizaje o habituación.
- **Aleatorización bloqueada**: se asignan en bloques de tamaño fijo (ej. bloques de 4: 2 control + 2 tratamiento).
  - Asegura equilibrio numérico entre grupos.
- **Doble ciego**: ni el participante ni el investigador saben quién recibe el tratamiento.
  - Elimina el efecto placebo y el sesgo del investigador.
- **Triple ciego**: ni participante, ni investigador, ni analista de datos saben la asignación.

#### Tipos de diseño experimental
- **Preexperimental**: sin grupo control o randomización (ej. un solo grupo pre-test/post-test). Bajo rigor.
- **Cuasiexperimental**: con grupo control pero sin randomización completa.
- **Experimental verdadero**: con grupo control y randomización. Mayor rigor.
  - **Diseño post-test solo con control**: aleatorización → tratamiento → post-test.
  - **Diseño pre-test/post-test con control**: aleatorización → pre-test → tratamiento → post-test.
- **Diseño factorial**: estudia dos o más variables independientes simultáneamente (ej. A×B).
  - Permite estudiar **efectos principales** y **interacciones**.
- **Diseño de medidas repetidas**: los mismos sujetos se miden en múltiples condiciones.
  - Mayor potencia, pero riesgo de efectos de orden (contrabalancear).

#### Validez
- **Validez interna**: ¿los cambios en la VD se deben realmente a la VI? (control de variables extrañas).
- **Validez externa**: ¿los resultados se pueden generalizar a otras poblaciones/contextos?
- **Validez de constructo**: ¿se mide realmente lo que se pretende medir?
- **Validez ecológica**: ¿el experimento refleja situaciones reales?
- **Validez de estadística**: ¿se usan correctamente los tests estadísticos?

#### Sesgos a evitar
- **Sesgo de selección**: los grupos no son comparables al inicio.
- **Sesgo de confirmación**: buscar solo datos que apoyen la hipótesis.
- **Efecto placebo**: mejora por expectativa, no por tratamiento.
- **Sesgo del investigador**: expectativas del investigador influyen en los resultados.
- **Sesgo de publicación**: los resultados significativos se publican más que los no significativos.
- **P-hacking**: probar múltiples hipótesis hasta encontrar una significativa (p < 0.05).

### 3. Análisis de Datos

#### Estadística descriptiva
- **Resumen de datos**: organizar, resumir y presentar datos de forma informativa.
- **Tablas de frecuencia**:
  - **Frecuencia absoluta (fᵢ)**: número de veces que aparece cada valor.
  - **Frecuencia relativa (frᵢ)**: fᵢ / n.
  - **Frecuencia acumulada (Fᵢ)**: suma de frecuencias absolutas hasta ese valor.
  - **Frecuencia relativa acumulada (FRᵢ)**: Fᵢ / n.
  - **Porcentajes**: frᵢ × 100.
- **Medidas de tendencia central**:
  - **Media aritmética**: x̄ = Σxᵢ / n. Sensible a valores extremos.
  - **Mediana**: valor central al ordenar. Robusta a valores extremos.
    - n impar: valor en posición (n+1)/2.
    - n par: promedio de posiciones n/2 y n/2+1.
  - **Moda**: valor más frecuente. Puede haber varias modas (bimodal, multimodal) o ninguna.
  - **Media truncada**: se eliminan los extremos (ej. 10% superior e inferior) y se calcula la media.
  - **Media ponderada**: x̄ = Σ(wᵢ·xᵢ) / Σwᵢ.
- **Medidas de dispersión**:
  - **Rango**: máximo - mínimo. Sensible a extremos.
  - **Varianza poblacional**: σ² = Σ(xᵢ - μ)² / N.
  - **Varianza muestral**: s² = Σ(xᵢ - x̄)² / (n-1). Corrección de Bessel.
  - **Desviación estándar**: σ = √σ² o s = √s². Misma unidad que los datos.
  - **Rango intercuartílico (IQR)**: Q₃ - Q₁. Dispersión del 50% central. Robusto.
  - **Coeficiente de variación**: CV = (s / x̄) × 100%. Permite comparar dispersión entre variables con distintas unidades.
  - **Desviación media absoluta**: Σ|xᵢ - x̄| / n.
- **Medidas de forma**:
  - **Asimetría (skewness)**: simetría de la distribución.
    - Skew = 0: simétrica.
    - Skew > 0: asimetría positiva (cola derecha).
    - Skew < 0: asimetría negativa (cola izquierda).
  - **Curtosis**: "pico" de la distribución.
    - Leptocúrtica (kurt > 3): más puntuda que la normal.
    - Mesocúrtica (kurt = 3): similar a la normal.
    - Platicúrtica (kurt < 3): más aplanada que la normal.

#### Gráficos estadísticos
- **Histograma**: barras adyacentes para datos continuos agrupados en intervalos. Muestra la distribución.
- **Polígono de frecuencias**: línea que une los puntos medios de las barras del histograma.
- **Ojiva (polígono de frecuencias acumuladas)**: curva de frecuencias acumuladas. Permite leer percentiles.
- **Diagrama de caja (boxplot)**: muestra Q₁, mediana, Q₃, bigotes (mín/máx o 1.5×IQR) y valores atípicos.
- **Diagrama de barras**: para datos categóricos. Barras separadas.
- **Gráfico de sectores (pie chart)**: proporciones de categorías. Usar con pocas categorías (<6).
- **Diagrama de dispersión (scatter plot)**: dos variables continuas. Muestra correlación.
- **Gráfico de líneas**: para datos temporales (series temporales).
- **Gráfico de barras apiladas**: composición de categorías dentro de categorías.
- **Mapa de calor (heatmap)**: matriz de valores en colores.

#### Estadística inferencial básica
- **Pruebas de hipótesis** (resumen):
  - **H₀**: hipótesis nula (no efecto).
  - **H₁**: hipótesis alternativa (efecto).
  - **α (nivel de significancia)**: probabilidad de error tipo I (0.05 habitual).
  - **Valor p**: probabilidad de obtener un resultado tan extremo, asumiendo H₀ verdadera.
    - p < α → se rechaza H₀.
    - p ≥ α → no se rechaza H₀.
  - **Error tipo I (α)**: rechazar H₀ cuando es verdadera (falso positivo).
  - **Error tipo II (β)**: no rechazar H₀ cuando es falsa (falso negativo).
  - **Potencia (1-β)**: probabilidad de detectar un efecto real.
  - **Prueba bilateral**: H₁: μ ≠ μ₀ (efecto en cualquier dirección).
  - **Prueba unilateral**: H₁: μ > μ₀ o μ < μ₀ (efecto en una dirección).

- **Tests paramétricos** (asumen normalidad):
  - **t de Student para una muestra**: comparar media muestral con un valor conocido.
    - t = (x̄ - μ₀) / (s/√n), gl = n-1.
  - **t de Student para muestras independientes**: comparar medias de dos grupos independientes.
    - t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂), gl ≈ n₁ + n₂ - 2.
  - **t de Student para muestras emparejadas**: comparar medias de dos grupos relacionados.
    - t = d̄ / (s_d/√n), donde d = x₁ - x₂.
  - **ANOVA de un factor**: comparar medias de 3+ grupos independientes.
    - F = MS_between / MS_within.
    - Si F es significativo → al menos un grupo es diferente (prueba post-hoc necesaria).
  - **Correlación de Pearson (r)**: relación lineal entre dos variables continuas.
    - r = Σ(xᵢ - x̄)(yᵢ - ȳ) / √[Σ(xᵢ - x̄)² · Σ(yᵢ - ȳ)²].
    - -1 ≤ r ≤ 1. r² = coeficiente de determinación (varianza explicada).

- **Tests no paramétricos** (no asumen normalidad):
  - **U de Mann-Whitney**: equivalente no paramétrico al t de muestras independientes.
  - **U de Wilcoxon (signed-rank)**: equivalente al t emparejado.
  - **Chi-cuadrado (χ²) de bondad de ajuste**: comparar distribución observada con esperada.
    - χ² = Σ(Oᵢ - Eᵢ)² / Eᵢ.
  - **Chi-cuadrado de independencia**: relación entre dos variables categóricas.
  - **Kruskal-Wallis**: equivalente no paramétrico al ANOVA.
  - **Spearman (ρ)**: correlación para datos ordinales o no normales.

- **Intervalos de confianza**:
  - **Media (σ conocida)**: x̄ ± z_(α/2) · σ/√n.
  - **Media (σ desconocida)**: x̄ ± t_(α/2, n-1) · s/√n.
  - **Proporción**: p̂ ± z_(α/2) · √(p̂(1-p̂)/n).
  - Interpretación: "Con un 95% de confianza, el parámetro poblacional está entre [límite inferior] y [límite superior]."

#### Regresión lineal simple
- **Modelo**: y = β₀ + β₁x + ε.
- **Mínimos cuadrados**: minimizar Σ(yᵢ - ŷᵢ)².
- **Pendiente**: β₁ = Σ(xᵢ - x̄)(yᵢ - ȳ) / Σ(xᵢ - x̄)².
- **Intercepto**: β₀ = ȳ - β₁x̄.
- **Coeficiente de determinación (R²)**: proporción de varianza de y explicada por x.
- **Residuos**: eᵢ = yᵢ - ŷᵢ. Deben ser aleatorios, normalmente distribuidos, con varianza constante.

### 4. Comunicación Científica

#### Estructura de un informe científico (IMRyD)
- **Introducción**: contexto, revisión de literatura, problema, hipótesis, objetivos.
- **Materiales y Métodos**: diseño experimental, muestras, variables, procedimientos, análisis estadístico. Debe ser reproducible.
- **Resultados**: presentación objetiva de datos (tablas, gráficos, estadísticas). Sin interpretación.
- **Discusión**: interpretación de resultados, comparación con literatura, limitaciones, implicaciones.
- **Conclusiones**: respuesta a la hipótesis, hallazgos principales, futuras líneas de investigación.
- **Referencias**: lista de fuentes citadas (formato consistente).
- **Agradecimientos** (opcional): financiación, colaboración.
- **Resumen/Abstract**: resumen conciso de todo el trabajo (150-300 palabras).

#### Estructura de un paper académico
- **Título**: claro, específico, conciso. Incluir variables clave.
- **Autores y afiliaciones**: orden de autoría (primero = principal contribuidor).
- **Abstract**: estructura IMRyD condensada.
- **Keywords**: 4-6 palabras clave para indexación.
- **Introducción**: de lo general a lo específico (embudo). Terminar con la hipótesis/objetivo.
- **Métodos**:
  - **Diseño experimental**.
  - **Población y muestra**.
  - **Instrumentos/materiales**.
  - **Procedimiento**.
  - **Análisis de datos** (software, tests estadísticos, nivel de significancia).
- **Resultados**: con estadísticas (t, F, p, IC, η², r).
- **Discusión**: interpretar, comparar, limitaciones.
- **Conclusión**: respuesta clara a la pregunta de investigación.
- **Referencias**: formato APA, Vancouver, IEEE, etc.

#### Revisión por pares (peer review)
- **Proceso**:
  1. Autor envía el manuscrito a una revista.
  2. Editor evalúa la idoneidad (scope, calidad general).
  3. Si pasa, se envía a 2-3 revisores expertos (anónimos o no).
  4. Revisores evalúan: originalidad, rigor metodológico, validez de conclusiones, claridad.
  5. Decisión editorial: aceptar, aceptar con revisiones menores, revisar y reenviar, rechazar.
- **Tipos de revisión**:
  - **Simple ciego**: revisor conoce al autor, autor no conoce al revisor.
  - **Doble ciego**: ni autor ni revisor se conocen.
  - **Abierta**: ambos conocen las identidades.
  - **Post-publicación**: comentarios abiertos tras la publicación.
- **Criterios de evaluación**:
  - **Originalidad**: ¿contribuye algo nuevo?
  - **Rigor metodológico**: ¿el diseño es adecuado?
  - **Validez de datos**: ¿los datos apoyan las conclusiones?
  - **Claridad**: ¿el texto es comprensible?
  - **Ética**: ¿hay conflicto de intereses? ¿datos fabricados?

#### Ética en la investigación
- **Consentimiento informado**: participantes deben conocer y aceptar el estudio.
- **Confidencialidad**: proteger la identidad de los participantes.
- **Integridad**: no fabricar, falsificar ni plagiar datos.
- **Transparencia**: reportar todos los resultados (incluyendo los no significativos).
- **Autoría**: solo quienes contribuyeron significativamente.
- **Doble publicación**: no publicar los mismos datos en múltiples revistas.
- **Manejo de datos**: guardar datos crudos para verificación.

#### Formato de citación (APA 7ª edición)
- **Libro**: Autor, A. A. (Año). *Título del libro en cursiva*. Editorial.
- **Artículo**: Autor, A. A. & Autor, B. B. (Año). Título del artículo. *Nombre de la Revista en cursiva, volumen*(número), páginas. DOI
- **En línea**: Autor, A. A. (Año, Mes Día). Título. *Sitio web*. URL
- **Cita en texto**: (Autor, Año) o Autor (Año).

## Cuándo usar este skill

Usa este skill cuando:

1. El usuario necesita **formular una hipótesis** clara y comprobable.
2. Hay problemas de **diseño experimental**: variables, controles, muestreo, aleatorización.
3. Se necesita **analizar datos**: estadística descriptiva, gráficos, tests de hipótesis.
4. El usuario necesita **redactar un informe científico** o paper.
5. Hay preguntas sobre **revisión por pares** y ética científica.
6. Se necesita **interpretar resultados estadísticos** (valor p, IC, R²).
7. El problema cruza **biología/física/química con metodología** (ej. diseñar un experimento biológico).
8. El usuario es **estudiante de bachillerato o universitario** trabajando en un proyecto científico.

## Instrucciones paso a paso para el agente

### Procedimiento para Formular Hipótesis

1. **Partir de una pregunta de investigación** clara y específica.
2. **Identificar las variables** (independiente y dependiente).
3. **Formular H₀** (no efecto) y **H₁** (efecto).
4. **Si es direccional**, formular la hipótesis de trabajo (ej. "mayor X produce mayor Y").
5. **Verificar que sea falsable**: debe existir al menos un resultado posible que la refute.
6. **Ejemplo**:
   - Pregunta: "¿La temperatura afecta la tasa de germinación de semillas de lenteja?"
   - H₀: La temperatura NO afecta la tasa de germinación.
   - H₁: La temperatura SÍ afecta la tasa de germinación.
   - HT: A mayor temperatura (hasta 30°C), mayor tasa de germinación.

### Procedimiento para Diseño Experimental

1. **Definir la pregunta de investigación** y la hipótesis.
2. **Identificar variables**:
   - VI: qué se manipula.
   - VD: qué se mide.
   - Variables de control: qué se mantiene constante.
3. **Determinar el tamaño de muestra** y el tipo de muestreo.
4. **Establecer grupos**: experimental (con tratamiento) y control (sin tratamiento o con control positivo).
5. **Aleatorizar**: asignación aleatoria a grupos, orden aleatorio de tratamientos.
6. **Definir el procedimiento** paso a paso (para reproducibilidad).
7. **Planificar el análisis estadístico** antes de recolectar datos.
8. **Prever limitaciones** y sesgos potenciales.

### Procedimiento para Análisis de Datos

1. **Organizar los datos** en una tabla.
2. **Verificar supuestos**: normalidad (Shapiro-Wilk, histograma, Q-Q plot), homogeneidad de varianzas (Levene).
3. **Calcular estadística descriptiva**: media, mediana, desviación estándar, IQR.
4. **Crear gráficos** apropiados: histograma (distribución), boxplot (comparación), dispersión (correlación).
5. **Seleccionar el test estadístico** apropiado:
   - Comparar 2 grupos independientes → t de Student (paramétrico) o Mann-Whitney (no paramétrico).
   - Comparar 2 grupos emparejados → t emparejada (paramétrico) o Wilcoxon (no paramétrico).
   - Comparar 3+ grupos → ANOVA (paramétrico) o Kruskal-Wallis (no paramétrico).
   - Relación entre 2 variables continuas → Pearson (paramétrico) o Spearman (no paramétrico).
   - Datos categóricos → Chi-cuadrado.
6. **Interpretar resultados**: valor p, tamaño del efecto, intervalo de confianza.
7. **No confundir significancia estadística con significancia práctica**: un efecto puede ser estadísticamente significativo pero prácticamente irrelevante.

### Procedimiento para Comunicación Científica

1. **Estructurar el informe** según IMRyD.
2. **Introducción**: de lo general a lo específico, terminar con hipótesis.
3. **Métodos**: detallar suficiente para reproducibilidad.
4. **Resultados**: objetivos, con estadísticas y gráficos. Sin interpretación.
5. **Discusión**: interpretar, comparar con literatura, limitaciones.
6. **Conclusiones**: respuesta directa a la hipótesis.
7. **Revisar**: ortografía, claridad, consistencia, formato de citas.
8. **Formato de figuras y tablas**: numeración, título, leyenda, unidades.

## Ejemplos de Prompts que Activan Este Skill

### Ejemplo 1: Hipótesis
```
Un estudiante observa que las plantas cerca de la ventana crecen más rápido que las del interior del aula. ¿Cómo formularía la hipótesis?
```
**Respuesta esperada**:
- **Pregunta**: ¿La luz solar afecta la tasa de crecimiento de las plantas?
- **H₀**: La cantidad de luz solar NO afecta la tasa de crecimiento de las plantas.
- **H₁**: La cantidad de luz solar SÍ afecta la tasa de crecimiento de las plantas.
- **Hipótesis de trabajo**: Las plantas expuestas a mayor cantidad de luz solar crecen más rápido que las expuestas a menor cantidad.
- **VI**: Cantidad de luz solar (horas de exposición o intensidad).
- **VD**: Tasa de crecimiento (cm/día o aumento de biomasa).

### Ejemplo 2: Diseño Experimental
```
Diseña un experimento para probar si un nuevo fertilizante aumenta el rendimiento de tomate.
```
**Respuesta esperada**:
- **Diseño**: Experimental con grupo control, aleatorizado.
- **VI**: Tipo de fertilizante (nuevo vs. control negativo: sin fertilizante; control positivo: fertilizante comercial).
- **VD**: Rendimiento (kg de tomate por planta).
- **Muestra**: 60 plantas de tomate de la misma variedad, edad y tamaño inicial.
- **Grupos**: 3 grupos de 20 plantas cada uno (aleatorización).
- **Controles**: misma variedad, mismo suelo, misma cantidad de agua, misma exposición solar, misma temperatura.
- **Duración**: ciclo completo de crecimiento (ej. 90 días).
- **Análisis**: ANOVA de un factor + prueba post-hoc (Tukey) si hay diferencias significativas.
- **Ética**: no aplica (plantas), pero registrar todos los datos, incluyendo los no significativos.

### Ejemplo 3: Análisis de Datos
```
Se midió la altura de 10 plantas con fertilizante (cm): 12, 15, 14, 13, 16, 11, 14, 15, 13, 14. Calcula la media, mediana, desviación estándar e interpreta.
```
**Respuesta esperada**:
- n = 10
- Media: x̄ = (12+15+14+13+16+11+14+15+13+14) / 10 = 137/10 = 13.7 cm
- Ordenado: 11, 12, 13, 13, 14, 14, 14, 15, 15, 16
- Mediana: (14+14)/2 = 14 cm
- Varianza: s² = Σ(xᵢ - 13.7)² / 9 = (2.89+0.49+0.09+0.49+4.49+4.49+0.09+0.49+0.49+0.49)/9 = 14.1/9 = 1.567
- Desviación estándar: s = √1.567 ≈ 1.25 cm
- Interpretación: Las plantas crecieron una media de 13.7 cm con una variabilidad de ±1.25 cm. La distribución es ligeramente asimétrica (media < mediana).

### Ejemplo 4: Interpretación de Valor p
```
Un experimento da p = 0.03 para la hipótesis de que el medicamento X reduce la presión arterial. α = 0.05. ¿Qué significa?
```
**Respuesta esperada**:
- p = 0.03 < α = 0.05 → se **rechaza H₀**.
- Significado: Hay evidencia estadística de que el medicamento X reduce la presión arterial.
- Interpretación correcta: "Si el medicamento NO tuviera efecto (H₀ verdadera), la probabilidad de obtener un resultado tan extremo como el observado es del 3%."
- Interpretación INCORRECTA: "Hay un 97% de probabilidad de que el medicamento funcione." (El valor p NO es la probabilidad de que H₀ sea verdadera).
- Nota: p = 0.03 indica significancia estadística, pero no informa sobre la magnitud del efecto. Se debe calcular también el **tamaño del efecto** (ej. d de Cohen) y el **intervalo de confianza**.

### Ejemplo 5: Estructura de un Paper
```
¿Cómo estructuraría la sección de "Materiales y Métodos" de un paper sobre el efecto de la luz LED en el crecimiento de lechuga?
```
**Respuesta esperada**:
```
Materiales y Métodos

2.1. Diseño experimental
Se realizó un experimento controlado con diseño completamente aleatorizado...

2.2. Materiales
- Semillas de Lactuca sativa (variedad 'Grand Rapids')...
- Leds LED de espectro rojo (660 nm), azul (450 nm) y blanco frío...
- Sustrato: mezcla de turba y perlita (3:1)...

2.3. Procedimiento
Las semillas se germinaron en bandejas de propagación durante 7 días...
Posteriormente se transplantaron a macetas de 1L...
Se asignaron aleatoriamente a 4 tratamientos de luz...

2.4. Variables
Variable independiente: espectro de luz (4 niveles)...
Variable dependiente: biomasa seca (g)...

2.5. Análisis estadístico
Se realizó ANOVA de un factor con α = 0.05...
Se usó el test post-hoc de Tukey...
Se verificó normalidad con Shapiro-Wilk...
Se utilizó R v4.3.0 para el análisis...
```

### Ejemplo 6: Tipos de Errores
```
En una prueba de fármaco contra la gripe, se rechaza H₀ (el fármaco no funciona) pero en realidad el fármaco SÍ funciona. ¿Qué tipo de error se cometió?
```
**Respuesta esperada**:
- Se rechazó H₀ (el fármaco no funciona).
- La realidad: el fármaco SÍ funciona.
- Decisión CORRECTA: se rechazó una H₀ falsa.
- **No se cometió ningún error**: fue una decisión correcta (detectar un efecto real).
- Esto corresponde a la **potencia del test** (1 - β). La probabilidad de tomar esta decisión correcta es la potencia.
- Un **error tipo II** (β) sería: no rechazar H₀ cuando es falsa (no detectar un fármaco que SÍ funciona).
- Un **error tipo I** (α) sería: rechazar H₀ cuando es verdadera (declarar que un fármaco NO funciona cuando SÍ funciona).

### Ejemplo 7: Muestreo
```
¿Qué tipo de muestreo sería más apropiado para estudiar la contaminación del aire en una ciudad de 2 millones de habitantes?
```
**Respuesta esperada**:
- **Muestreo estratificado** sería lo más apropiado.
- **Estratos**: por distritos/zonas (centro, suburbios, zona industrial, zona residencial).
- **Razón**: la contaminación varía según la zona (tráfico, industria, parques). Un muestreo aleatorio simple podría no representar adecuadamente todas las zonas.
- **Procedimiento**: definir los estratos, determinar el tamaño de muestra total (ej. 200 estaciones), asignar proporcionalmente a cada estrato, seleccionar aleatoriamente dentro de cada estrato.
- **Alternativa**: muestreo sistemático (cada k-ésima manzana) si se quiere una cobertura espacial uniforme.

## Referencias Cruzadas a Skills STEM Existentes

Este skill hace referencia a los siguientes skills del ecosistema STEM de Mastermind para profundización:

| Skill Referenciado | Ruta | Relación |
|---|---|---|
| `math-estadistica-probabilidad` | `/hermes-home/skills/stem/math/math-estadistica-probabilidad` | Estadística descriptiva/inferencial completa, distribuciones, intervalos de confianza, pruebas de hipótesis avanzadas |
| `math-estadistica-probabilidad-eng` | `/hermes-home/skills/stem/math/math-estadistica-probabilidad-eng` | Versión en inglés del skill de estadística y probabilidad |
| `skill-biology-cell` | `/hermes-home/skills/skill-biology-cell/` | Para diseñar experimentos biológicos (cultivos celulares, genética, ecología) |
| `skill-chemistry-basics` | `/hermes-home/skills/skill-chemistry-basics/` | Para diseñar experimentos químicos (estequiometría, cinética, equilibrio) |
| `skill-physics-mechanics` | `/hermes-home/skills/skill-physics-mechanics/` | Para diseñar experimentos físicos (mediciones, errores, incertidumbre) |

### Cuándo derivar a otros skills

- Si se necesita **estadística avanzada** (ANOVA multifactor, regresión múltiple, MANOVA) → derivar a `math-estadistica-probabilidad`.
- Si se necesita **diseñar un experimento biológico** (cultivos, genética molecular) → derivar a `skill-biology-cell`.
- Si se necesita **diseñar un experimento químico** (titulaciones, cinética) → derivar a `skill-chemistry-basics`.
- Si se necesita **análisis de errores e incertidumbre** en mediciones físicas → derivar a `skill-physics-mechanics`.
- Si se necesita la versión en **inglés** de contenido estadístico → derivar a `math-estadistica-probabilidad-eng`.

## Pitfalls — Errores Comunes

### Método Científico
- **Confundir hipótesis con teoría**: una hipótesis es una propuesta tentativa; una teoría es un conjunto de hipótesis ampliamente respaldadas por evidencia (ej. teoría celular, teoría de la evolución).
- **Confundir observación cualitativa con cuantitativa**: "la planta creció más" es cualitativa; "la planta creció 5 cm" es cuantitativa. Ambas son válidas, pero la cuantitativa permite análisis estadístico.
- **Creer que la ciencia "prueba" hipótesis**: la ciencia no prueba, respalda o refuta con evidencia. Las conclusiones son siempre provisionales.
- **Saltar la investigación previa**: repetir experimentos ya realizados sin conocer la literatura existente.

### Diseño Experimental
- **Confundir variable independiente con dependiente**: la VI es la que se manipula (causa); la VD es la que se mide (efecto).
- **No incluir grupo control**: sin control, no hay referencia para comparar. ¿El efecto se debe al tratamiento o a factores externos?
- **No aleatorizar**: sin aleatorización, los grupos pueden no ser comparables (sesgo de selección).
- **Tamaño de muestra insuficiente**: con n pequeño, el test puede no tener potencia para detectar un efecto real (error tipo II).
- **P-hacking**: probar múltiples hipótesis o variables dependientes hasta encontrar una significativa. Infla la tasa de falsos positivos.
- **No controlar variables extrañas**: si no se controlan, no se puede atribuir el efecto a la VI.

### Análisis de Datos
- **Confundir significancia estadística con significancia práctica**: con muestras grandes, cualquier diferencia pequeña puede ser estadísticamente significativa pero sin relevancia real.
- **Interpretar mal el valor p**: p NO es la probabilidad de que H₀ sea verdadera. Es la probabilidad de obtener un resultado tan extremo asumiendo H₀ verdadera.
- **Confundir correlación con causalidad**: una correlación alta no implica que una variable cause cambios en la otra. Puede haber variables confundidoras.
- **Usar el test estadístico incorrecto**: usar t de Student con datos no normales, o ANOVA con varianzas heterogéneas. Verificar supuestos antes de elegir el test.
- **Error de Bessel**: al calcular la varianza muestral, dividir por (n-1), no por n. Dividir por n subestima la varianza poblacional.
- **Confundir varianza con desviación estándar**: la varianza está en unidades al cuadrado; la desviación estándar está en las mismas unidades que los datos.

### Comunicación Científica
- **Incluir interpretación en Resultados**: los Resultados deben ser objetivos (datos y estadísticas). La interpretación va en la Discusión.
- **No reportar resultados no significativos**: publicar solo los significativos es un sesgo de publicación. Todos los resultados deben reportarse.
- **Citas incompletas**: siempre incluir autor, año, título, fuente y DOI cuando esté disponible.
- **Plagio**: usar ideas de otros sin citarlos. Parafrasear NO basta: se debe citar la fuente original.

## Notas Adicionales

- Este skill es el **pilar metodológico** del ecosistema STEM de Mastermind.
- En hipótesis, siempre **incluir H₀ y H₁** por separado. La H₀ es fundamental para el análisis estadístico.
- En diseño experimental, enfatizar que **la aleatorización es la herramienta más poderosa** para controlar variables extrañas.
- En análisis de datos, recordar que **p < 0.05 no es un umbral mágico**: es una convención, no una ley.
- En comunicación científica, recordar que **un paper bien escrito es tan importante como los datos**: si no se puede entender, no se puede evaluar.
- Para el **tamaño del efecto**, calcular siempre además del valor p: d de Cohen (comparación de medias), η² (ANOVA), r² (regresión), odds ratio (datos categóricos).
- En la **revisión por pares**, la crítica debe ser constructiva y basada en evidencia, no en preferencias personales.
- La **replicabilidad** es el estándar de oro de la ciencia: un resultado solo es válido si otros investigadores pueden obtenerlo.
