# CIAF — Arquitectura de Datos (2026-06-26)

## Inventario verificado

| Tipo | Cantidad | Ubicación |
|------|----------|-----------|
| Informes | 277 | `/root/workspace/CIAF/YYYY/*.pdf` |
| Memorias | 17 | `/root/workspace/CIAF/memorias/` |
| Normativa | 7 | `/root/workspace/CIAF/normativa/` |
| **Total** | **301** | |

### Distribución por año (informes)
2007:4, 2008:53, 2009:43, 2010:28, 2011:24, 2012:22, 2013:23, 2014:14, 2015:10, 2016:11, 2017:12, 2018:2, 2019:3, 2020:3, 2021:6, 2022:5, 2023:3, 2024:3, 2025:1

## Tres eras de formato

### Era 1: Pre-RD 810/2007 (2007-2008)
- **Normativa:** Sin formato estandarizado
- **Secciones:** Variables (Antecedentes, Hechos, Análisis)
- **Características:** Formato libre, más narrativo
- **Parser:** Difícil — requiere detección por contenido

### Era 2: RD 810/2007 (2009-2013)
- **Normativa:** Real Decreto 810/2007
- **Secciones:** 1-5 (Resumen, Descripción del accidente, Análisis, Conclusiones, Recomendaciones)
- **Características:** Estructura más definida pero menos rigidizada

### Era 3: RD 623/2014 (2014-2025)
- **Normativa:** Real Decreto 623/2014 (Art. 15)
- **Secciones:** 0-6 (Abreviaturas, Resumen del accidente, Descripción, Análisis, Conclusiones, Recomendaciones, Anexos)
- **Características:** Estructura más detallada, incluye abreviaturas y anexos

## Arquitectura propuesta (David Antizar)

### Fuente de verdad: JSON particionado
```
ciaf-web/
├── data/
│   ├── index.json              ← ~50KB, todos los IDs + metadatos mínimos
│   ├── reports/
│   │   ├── 2007.json
│   │   ├── ...
│   │   └── 2025.json
│   ├── relations.json          ← entidades × informes × recomendaciones
│   ├── memorias.json           ← resúmenes anuales
│   └── normativa.json          ← referencias normativas
├── images/
│   ├── 2007/
│   │   └── IF-01-2007-fig01.png
│   └── ...
├── scripts/
│   ├── parser-v4.py            ← parser multi-formato
│   ├── sync.py                 ← auto-import desde web
│   └── coherence-check.py      ← verificar consistencia memorias↔informes
└── index.html                  ← dashboard principal
```

### Relaciones entre entidades
- **Empresas:** Renfe, Adif, operadores, fabricantes
- **Causas:** Señalización, error humano, vía, material rodante
- **Recomendaciones:** A quién, qué se recomienda, estado de implementación
- **Ubicaciones:** Estaciones, líneas, pk (punto kilométrico)

### Características del visor
- **Mapa:** Leaflet con todas las líneas férreas + markers de informes
- **Dashboard:** Filtros multi-selección (año, empresa, causa, gravedad)
- **Resumen ejecutivo:** KPIs, gráficos Chart.js de evolución temporal
- **Memorias:** Sección dedicada para comparar año a año
- **Coherencia:** Warning cuando memorias e informes no coinciden
- **Auto-import:** `sync.py` descarga nuevos PDFs y los procesa

## Fuentes de datos verificadas

| Fuente | Patrón URL | Estado |
|--------|------------|--------|
| Informes 2017-2025 | `infofin-YYYY` | ✅ Verificado |
| Informes 2009-2016 | `/MFOM/.../YYYY/` | ✅ Verificado |
| Memorias | `memoriasanuales` | ✅ Verificado |
| Normativa | `comodin/recursos/` | ✅ Verificado |
