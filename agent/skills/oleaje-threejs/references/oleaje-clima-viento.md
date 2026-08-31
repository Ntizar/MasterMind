# Oleaje completo: boyas desglosadas + viento + clima (módulo "entender el mar")

Módulo `tests/oleaje-completo.mjs` → `tests/oleaje-completo.json` (commit `27ef855`). Nace de la
petición de David: "hay que entender mejor el oleaje de esas boyas y cómo afecta el clima previsto".

## Qué añade sobre el pronóstico básico

Open-Meteo Marine da MÁS que `wave_height/wave_period/wave_direction`. Campos que el módulo usa:

- **Desglose de componentes**: `swell_wave_height/period/direction` (mar de fondo) vs
  `wind_wave_height/direction` (mar de viento). La fracción de swell (`fracSwell = swellH/Hs`)
  distingue "mar limpio de fondo" de "chapoteo local" — clave para calidad de surf.
- **Viento** (`api.open-meteo.com/v1/forecast`, no el marine): `wind_speed_10m`,
  `wind_direction_10m` + `precipitation`, `cloud_cover`. Hay que pedirlo de un endpoint aparte.
- **Calidad de viento vs orientación de la playa**: delta angular entre dirección de viento y la
  orientación de la playa (a qué rumbo mira la arena). Tabla: >140° offshore (nota 1.0), >100°
  cruzado-tierra (0.9), >60° cruzado (0.7), >30° cruzado-mar (0.45), resto onshore (0.2).
  "Hay ola" ≠ "hay BUENA ola": el viento onshore fuerte (>15 km/h) revuelve el mar.
- **Resumen diario**: HsMax, swell dominante (máx swellH del día), fracSwell medio, viento medio,
  horas offshore útiles, horas de onshore fuerte, lluvia total (mm).

## Hallazgo real (ago-sep 2026, Cantábrico)

Semana con oleaje 93-100% swell de fondo NW (T 6-7.5 s). El día 30: Suances y Liencres comen
13-14 h de onshore con 3-4 mm de lluvia mientras Somo aguanta — el ENE entra más fuerte en la
costa oeste de la bahía. Este tipo de diferencia entre spots a 20 km SOLO sale con el viento
integrado por spot; el Hs de la boya es el mismo para todos.

## Pendiente acordada

Integrar la nota de viento en el score del ranking (penalizar onshore fuerte >15 km/h, premiar
ventanas offshore) y en el informe PDF (columna de viento + clima por día). El módulo ya produce
los datos; falta el wiring en `ranking-spots.mjs` y `informe-pdf.mjs`.

## Lecciones

1. El pronóstico de viento vive en el endpoint forecast, NO en marine-api — dos fetch por spot.
2. La orientación de la playa (`orient` en el ranking, p.ej. 'NW') es un dato a mano de cada spot:
   sin ella no hay offshore/onshore. Añadirla al alta de spots nuevos.
3. `wind_wave_height` puede ser 0 en calma total: usar `swellH/Hs` con guard `Hs > 0`.
