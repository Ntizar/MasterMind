# PMST Chapter Structure — 22 capítulos Ley 8/2021

## Estructura del informe PMST

El Plan de Movilidad Sostenible al Trabajo (PMST) conforme a la Ley 8/2021 tiene 22 capítulos:

1. **Portada** — Logo, nombre empresa, fecha, versión
2. **Índice** — Navegación por capítulos
3. **Resumen Ejecutivo** — Síntesis 1 página, KPIs clave
4. **Marco Legal** — Ley 8/2021, obligaciones, zonas BDE
5. **Metodología** — Fuentes datos, alcance, periodo
6. **Análisis del Entorno** — Municipio, transporte, infraestructuras
7. **Caracterización del Centro** — Dirección, accesibilidad, parking
8. **Caracterización de la Empresa** — Sector, plantilla, turnos
9. **Resultados de la Encuesta** — Tablas, gráficas, análisis cruzado
10. **Reparto Modal** — % por modo, comparativa nacional
11. **Distancias y Tiempos** — Media, mediana, distribución
12. **Huella de Carbono** — Factores MITECO 2024, toneladas CO₂e
13. **Aparcamiento** — Plazas, ocupación, ratios
14. **Transporte Público** — Paradas cercanas, frecuencias, cobertura
15. **Infraestructura Ciclista** — Bici compartida, carriles, aparcabicis
16. **DAFO** — Matriz 2×2 con factores reales
17. **Objetivos SMART** — 7+ objetivos específicos, medibles, alcanzables
18. **Plan de Medidas** — 15+ medidas priorizadas, impacto/coste/plazo
19. **Seguimiento** — KPIs multi-año, tabla de seguimiento
20. **Cronograma** — Timeline visual de implementación
21. **Presupuesto Estimado** — Inversión por medida, ROI
22. **Conclusiones** — Compromisos, hoja de ruta 2024-2028

## Datos de entrada por capítulo

| Capítulo | Datos necesarios de appState |
|----------|------------------------------|
| Resumen Ejecutivo | centro, diagnostico, comparativas, medidas |
| Análisis Entorno | centro (coords), transportePublico, isocronas |
| Resultados Encuesta | encuesta.respuestas, encuesta.agregados |
| Huella Carbono | diagnostico.co2e, factores MITECO |
| Transporte Público | transportePublico.paradas (NAP DGT) |
| Bicicleta | transportePublico.gbfs (GBFS) |
| DAFO | dafo (fortalezas, debilidades, oportunidades, amenazas) |
| Medidas | medidas[] (de DAFO derivation) |
| KPIs | kpiMatrix (multi-año) |

## CSS Print para informe A4

```css
@media print {
    @page { size: A4; margin: 2cm; }
    .chapter { page-break-before: always; }
    .chapter:first-child { page-break-before: avoid; }
    h2 { color: #1e40af; border-bottom: 2px solid #2563eb; }
    table { width: 100%; border-collapse: collapse; }
    th { background: #2563eb; color: white; padding: 10px; }
    td { padding: 8px 10px; border-bottom: 1px solid #e5e7eb; }
}
```

## Generación con LLM

Cada capítulo se genera con un prompt que incluye:
1. **Role**: "Eres un consultor de movilidad sostenible..."
2. **Context**: Tipo de capítulo, normativa aplicable
3. **Data**: JSON con datos reales de appState
4. **Constraints**: Extensión (400-800 palabras), tono profesional
5. **Output**: HTML con h3, tablas, listas, KPIs inline

## Test real
- 22 capítulos generados
- 164KB de HTML
- ~55-60 páginas impresas
- 31 tablas, 123 párrafos, 55 listas
- CSS print A4 con page-break por capítulo
