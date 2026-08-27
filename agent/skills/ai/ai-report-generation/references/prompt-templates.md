# Prompt Templates — AI Report Generation

## Plantilla Base (todas las secciones)

```
Eres un consultor de movilidad sostenible redactando el capítulo "{CHAPTER_NAME}"
de un Plan de Movilidad Sostenible al Trabajo (PMST) conforme a la
Ley 8/2021 de Movilidad Sostenible y la Ley 6/2018 de PGE.

CONTEXTO:
- Documento: PMST de {CENTRO_NOMBRE}
- Ubicación: {CENTRO_DIRECCION} ({CENTRO_LAT}, {CENTRO_LON})
- Plantilla: {PLANTILLA} trabajadores
- Periodo: {PERIODO}

DATOS RELEVANTES:
{JSON_DATA}

INSTRUCCIONES:
1. Redacta entre {MIN_WORDS}-{MAX_WORDS} palabras
2. Usa datos reales del centro, NO textos genéricos
3. Incluye tablas con cifras específicas cuando sea posible
4. Menciona la normativa aplicable (Ley 8/2021)
5. Tono: profesional pero accesible para dirección general
6. NO uses jerga técnica sin explicarla
7. Formato de salida: HTML puro (h3, p, table, ul, strong)
   - NO uses markdown (##, **, -)
   - NO uses code fences
   - SÍ usa <table>, <tr>, <td>, <strong>, <em>
```

## Capítulo 2: Resumen Ejecutivo

```
{BASE_PROMPT}

DATOS ESPECÍFICOS:
- Reparto modal: {SOSTENIBLE}% sostenible, {MOTORIZADO}% motorizado
- Huella CO₂e: {CO2_TOTAL} toneladas/año ({CO2_POR_EMPLEADO} kg/empleado)
- Comparativa nacional: coche {DIFF_COCHE}%, TP {DIFF_TP}%
- Medidas propuestas: {NUM_MEDIDAS}

INSTRUCCIONES ADICIONALES:
1. Empieza con la obligación legal (Ley 8/2021, >100 empleados)
2. Incluye 4-5 KPIs destacados en formato visual (tabla o cards)
3. Identifica las 3 prioridades más urgentes
4. Cierra con la hoja de ruta resumida
5. Extensión: 400-600 palabras
```

## Capítulo 5: Análisis del Entorno

```
{BASE_PROMPT}

DATOS GEOGRÁFICOS:
- Isochronas ORS: {ISOCRONE_DATA}
- Estaciones transporte público (NAP DGT): {ESTACIONES_DATA}
- Puntos interés cercanos: {POI_DATA}
- Climatología: {CLIMA_DATA}

INSTRUCCIONES ADICIONALES:
1. Describe el entorno urbano del centro (zona, densidad, uso del suelo)
2. Analiza accesibilidad según isocronas por modo
3. Evalúa cobertura de TP (paradas en radio 500m/1km/2km)
4. Identifica barreras geográficas
5. Menciona climatología y su impacto en movilidad sostenible
6. Incluye tabla de isochronas
7. Extensión: 600-800 palabras
```

## Capítulo 8: Resultados de la Encuesta

```
{BASE_PROMPT}

DATOS DE ENCUESTA:
- Total encuestados: {TOTAL} / {PLANTILLA} (tasa: {TASA_RESPUESTA}%)
- Por departamento: {DEPTO_DATA}
- Reparto modal: {MODAL_DATA}
- Distribución distancias: {DIST_DATA}
- Distribución tiempos: {TIEMPO_DATA}
- Cross-analysis modo×distancia: {CROSS_DATA}

INSTRUCCIONES ADICIONALES:
1. Evalúa representatividad de la muestra
2. Analiza reparto modal global y por departamento
3. Identifica patrones de distancia (¿qué % vive a <5km?)
4. Analiza tiempos de viaje (>45 min = problema)
5. Cross-analysis: qué modos dominan por tramo
6. Detecta anomalías o departamentos destacados
7. Extensión: 600-1000 palabras
```

## Capítulo 11: Huella de Carbono

```
{BASE_PROMPT}

DATOS DE CÁLCULO:
- Factores MITECO 2024: {FACTORES_CO2}
- Desglose por modo: {DESGLOSE_CO2}
- Total: {CO2_TOTAL} toneladas CO₂e/año
- Por empleado: {CO2_POR_EMPLEADO} kg CO₂e/año

INSTRUCCIONES ADICIONALES:
1. Presenta desglose total con tabla por modo
2. Calcula equivalencias comprensibles (árboles, vuelos, hogares)
3. Compara con media del sector si hay datos
4. Proporciona escenarios de reducción (-10%, -20%, -30%)
5. Identifica qué medidas tienen mayor impacto
6. Incluye coste económico (€/tonelada ETS)
7. Extensión: 500-700 palabras
```

## Capítulo 15: Análisis DAFO

```
{BASE_PROMPT}

DATOS DAFO:
- Fortalezas: {FORTALEZAS}
- Debilidades: {DEBILIDADES}
- Oportunidades: {OPORTUNIDADES}
- Amenazas: {AMENAZAS}

INSTRUCCIONES ADICIONALES:
1. Presenta la matriz DAFO 2×2
2. Deriva 3-4 estrategias por combinación (FO, DO, FA, DA)
3. Prioriza las estrategias por impacto
4. Conecta con las medidas del plan
5. Extensión: 400-600 palabras
```

## Capítulo 17: Plan de Medidas

```
{BASE_PROMPT}

MEDIDAS PROPUESTAS:
{MEDIDAS_DATA}

INSTRUCCIONES ADICIONALES:
1. Ordena por relación impacto/coste
2. Para cada medida: categoría, impacto, coste estimado, plazo, responsable
3. Incluye inversión total y ROI estimado
4. Agrupa por tipo: infraestructura, incentivos, organización, comunicación
5. Extensión: 500-800 palabras
```

## Capítulo 21: Conclusiones

```
{BASE_PROMPT}

SÍNTESIS DE TODOS LOS CAPÍTULOS:
- Diagnóstico: {RESUMEN_DIAGNOSTICO}
- DAFO: {RESUMEN_DAFO}
- Medidas: {RESUMEN_MEDIDAS}
- KPIs: {KPI_ACTUAL}

INSTRUCCIONES ADICIONALES:
1. Sintetiza hallazgos principales (3-5 bullets)
2. Lista compromisos de la dirección (verbos de acción)
3. Hoja de ruta por fases (preparación, implementación, consolidación)
4. Cierra con frase motivacional
5. Extensión: 300-500 palabras
```
