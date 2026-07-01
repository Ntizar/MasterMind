# CIAF — Scraping y análisis de estructuras de informes

## Web de la CIAF
- URL base: `https://www.transportes.gob.es/organos-colegiados/ciaf`
- Sección de informes: `https://www.transportes.gob.es/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados`
- URLs por año: `/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados/infofin-{year}` (2017-2025)

## Patrón de URLs de PDFs
```
https://www.transportes.gob.es/recursos_mfom/paginabasica/recursos/{filename}.pdf
```
Ejemplo: `recursos_mfom/paginabasica/recursos/2025-41-0522-if.pdf`

## Pitfalls de scraping
- **Browser tool bloquea con 403** — usar siempre curl con User-Agent
- **Headers necesarios:**
  ```bash
  curl -sL -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
    -H 'Accept: application/pdf,*/*' \
    -H 'Referer: https://www.transportes.gob.es/' \
    URL_PDF
  ```
- **Extracción de enlaces:** `grep -oP 'href="[^"]*\.pdf"'` en la página HTML

## Estructura de informes por año

| Año | Tipo | Secciones | Líneas | Notas |
|-----|------|-----------|--------|-------|
| 2017 | Accidente | 6 secciones simples | ~1,200 | Más conciso |
| 2020 | Accidente | 6 secciones detalladas | ~2,000 | Más granular |
| 2025 | Incidente | 6 secciones + abreviaturas + append inglés | ~950 | Estructura más reciente |

### Secciones core (siempre presentes, 6):
1. **Resumen / Hechos** → qué pasó
2. **Investigación y Contexto** → cómo se investigó
3. **Descripción del Suceso** → detalles técnicos
4. **Análisis** → causas y factores
5. **Conclusiones** → hallazgos
6. **Recomendaciones / Medidas** → acciones preventivas

### Evolución de la estructura:
- **2017:** Secciones simples, menos subsecciones
- **2020+:** Secciones más detalladas, subsecciones numeradas (2.1, 2.2...)
- **2025+:** Incluye lista de abreviaturas y append en inglés

## Geocodificación de ubicaciones
- Las estaciones se pueden geocodificar con Nominatim (OpenStreetMap)
- Patrón: "estación de {nombre}" → buscar en Nominatim → extraer lat/lng
- Algunos informes incluyen coordenadas explícitas en el texto

## Total de informes disponibles
- **35 PDFs** desde 2017 hasta 2025
- Distribución por año:
  - 2017: 12 informes
  - 2018: 2 informes
  - 2019: 3 informes
  - 2020: 3 informes
  - 2021: 6 informes
  - 2022: 5 informes
  - 2023: 3 informes
  - 2024: 3 informes
  - 2025: 1 informe