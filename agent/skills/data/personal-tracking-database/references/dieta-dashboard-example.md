# Ejemplo real: MastermindFit (dieta + deporte + pasos)

## Estructura de database.json real

```json
{
  "meta": {
    "nombre": "David Antizar",
    "altura_cm": 174,
    "peso_inicial_kg": 98.6,
    "peso_objetivo_kg": 88,
    "fecha_inicio": "2026-06-03",
    "version": "2.1.0"
  },
  "peso": [
    {"fecha": "YYYY-MM-DD", "hora": "mañana|tarde", "peso_kg": 0, "notas": ""}
  ],
  "comidas": [
    {"fecha": "YYYY-MM-DD", "hora": "HH:MM", "tipo": "desayuno|almuerzo|comida|merienda|cena|postre|bebida|post-entreno", "descripcion": "", "kcal": 0, "proteinas_g": 0, "hidratos_g": 0, "grasas_g": 0, "notas": ""}
  ],
  "deporte": [
    {"fecha": "YYYY-MM-DD", "hora": "HH:MM", "tipo": "gimnasio|cardio|carrera|ciclismo|otro", "descripcion": "", "duracion_min": 0, "intensidad": "baja|media|alta", "kcal_estimadas": 0, "notas": ""}
  ],
  "pasos": [
    {"fecha": "YYYY-MM-DD", "pasos": 0, "notas": ""}
  ]
}
```

## Reglas de tipos de comida
- `desayuno`: antes de las 10:00
- `almuerzo`: media mañana (10:00-12:00)
- `comida`: mediodía (12:00-15:00)
- `merienda`: tarde (15:00-18:00)
- `cena`: noche (18:00-23:00)
- `postre`: después de comida/cena
- `bebida`: café, zumo, alcohol, etc.
- `post-entreno`: después del ejercicio

## Dashboard sections
- KPIs: peso actual, perdido, calorías día, pasos día
- Gráfico evolución peso (línea temporal)
- Gráfico calorías/desglose macros (barras agrupadas)
- Gráfico pasos diario (barras)
- Proyección peso objetivo (3 escenarios)
- Timeline comidas del día
- Timeline deporte

## Deploy
- URL: `https://dieta-ntizar-ntizar.apps.nan.builders/`
- Puerto: 5050
- Auto-redeploy: cada push a main en `/root/workspace/dieta`
