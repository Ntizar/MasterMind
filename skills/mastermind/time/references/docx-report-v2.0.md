# DOCX Report v2.0 — Arquitectura de Secciones

**Archivo:** `js/docx-report.js`

## Secciones (14-15 en v5.0)

1. Portada — Título, dirección, fecha, modos, rangos
2. Resumen Ejecutivo — KPIs + tabla principal
3. Mapa de Isocronas — Descripción visual
4. Datos Demográficos — CPs, salarios, vivienda
5. Transporte Público — Paradas y rutas GTFS (condicional)
6. Bicicletas — CityBikes/GBFS estaciones
7. Comparativa por Modo — Coche, Bus, Bici, Andando
8. Ranking CPs — Score compuesto (accesibilidad + coste)
9. Alertas — Ratio salario/precio favorable
10. Rutas Recomendadas — Ranking por modo
11. Multi-Ciudad — Comparativa entre ciudades (condicional)
12. Recomendaciones — Ayudas TP, parking bici, carpooling
13. Notas Técnicas — Metodología + fuentes
14. Créditos — "Hecho con ❤️ por David Antizar"

## Score de accesibilidad
```
score = (distancia × 0.35) + (coste × 0.25) + (vivienda × 0.25) + (salario × 0.15)
```

## Colores Kaizen v5.0
- Azul principal: `#1A4488` (cabeceras, títulos)
- Rojo: `#CB1823` (subtítulos, acentos)
- Filas alternadas: `#f1f5f9`

## API
```javascript
import { generarDOCX } from './docx-report.js';
await generarDOCX(resultados, punto, modosActivos, tiempos, gtfsData, transporteCercano, extras);
```

## Pitfalls
- `docx.js` es UMD global (`window.docx`), NO ESM
- `docx.Packer.toBlob()` requiere `await`
- Tablas: `Table → TableRow → TableCell`
- `shading: {fill: "1A4488", val: "clear"}` en TableCell properties (Kaizen blue)
