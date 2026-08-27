---
name: gtfs-to-html-timetables
version: "1.0.0"
description: "Generar horarios de tránsito legibles como HTML o PDF desde datos GTFS estáticos. Inspirado en BlinkTagInc/gtfs-to-html (⭐226)."
tags: [gtfs, html, timetable, transit, pdf, schedule]
---

# GTFS a Horarios HTML

## Resumen

Convierte feeds GTFS estáticos en horarios legibles para humanos en formato HTML o PDF. Genera tablas de horarios por ruta, parada y día de la semana.

## Cuándo usar

- Generar horarios imprimibles desde GTFS
- Mostrar tablas de horarios en web de transporte
- Exportar PDF de horarios para impresión

## Patrón de uso

```bash
# Instalar
npm install gtfs-to-html

# Configurar
echo '{"sqlitePath": "/tmp/gtfs.db", "agency": "metro-madrid"}' > config.json

# Importar GTFS y generar HTML
gtfs-to-html --config config.json
```

```javascript
// Generar horario para una ruta específica
const gtfsToHtml = require('gtfs-to-html');

await gtfsToHtml({
  sqlitePath: '/tmp/gtfs.db',
  agency: 'metro-madrid',
  routes: ['1'], // Línea 1
  output: './horarios/',
  format: 'html' // o 'pdf'
});
```

## Estructura de salida

```
horarios/
├── index.html          # Listado de todas las rutas
├── route-1/
│   ├── timetable.html   # Tabla de horarios
│   ├── schedule.html    # Horario por parada
│   └── map.html         # Mapa de la ruta
└── route-2/
    └── ...
```

## Pitfalls

- **SQLite:** La herramienta importa GTFS a SQLite primero. Asegurar que hay espacio.
- **Frequencies.txt:** Si el feed usa frequencies (headway) en vez de stop_times exactos, la tabla se genera diferente.
- **Time format:** GTFS usa HH:MM:SS. Formatear a HH:MM para display.
- **Multi-agency:** Si el feed tiene múltiples agencias, especificar cuál generar.
- **PDF:** Requiere wkhtmltopdf o Chromium para generar PDF.

## Referencias

- gtfs-to-html: https://github.com/BlinkTagInc/gtfs-to-html
- GTFS Schedule spec: https://gtfs.org/schedule/

---

**Hecho con ❤️ por David Antizar**
