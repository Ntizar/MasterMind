# Ranking de spots de surf y tests reales (fase "mejores olas")

## Arquitectura de la app de "mejores olas" (prototipo en tests/)

- `tests/ranking-spots.mjs` — motor: para cada spot (lista de coords: rompiente + punto offshore + orientación + tipo):
  1. Batimetría real: 5 puntos offshore→rompiente vía EMODnet depth_sample
  2. Pronóstico horario real de 7 días: Open-Meteo Marine (`marine-api.open-meteo.com/v1/marine?latitude=..&longitude=..&hourly=wave_height,wave_period,wave_direction`)
  3. Física de la biblia (estudioTransecto 1D) hora a hora → Hs en la rompiente
  4. Score de surf: cercanía al ideal del spot (beach break 1.5 m, rivermouth 2.2 m), bonus T≥9s, penalización por exceso (>2× ideal). Horas buenas = score ≥7.
- Resultados en `tests/ranking-spots.json`; informe en `tests/informe-pdf.mjs` → HTML → PDF.
- **Multi-zona validada** (`tests/test-zona-med.mjs` → `ranking-spots-med.json`): segunda costa (Mediterráneo Valencia–Alicante) con el MISMO motor sin ajustes. Resultado: scores med. 5.4–5.7 vs Cantábrico 6.2–6.8 — físicamente correcto (mar de fondo atlántico T 8–12 s vs wind swell local med. T 4–7 s que se disipa antes). Solo los ideales del score se calibran por tipo de spot; las fórmulas son universales. Validar siempre una 2ª zona/costa antes de declarar el motor general.
- Resultado del test (agosto 2026, verano suave Hs 0.44–1.84): ganó El Brusco 6.8, Somo 6.5, Los Locos 6.5; Mundaka última (3.1) con agosto seco — coherente con la realidad (su barra de ría necesita descarga del Oka + swell NW largo).

## Fuente de oleaje: Open-Meteo Marine API (respaldo de Puertos del Estado)

- `https://marine-api.open-meteo.com/v1/marine?latitude=..&longitude=..&hourly=wave_height,wave_period,wave_direction&start_date=AAAA-MM-DD&end_date=AAAA-MM-DD`
- Sin clave, CORS abierto, rápida. Devuelve series horarias (Hs, T, dirección).
- **Cuándo usarla**: Puertos del Estado cae con frecuencia (503 "maintenance" en poem.puertos.es y portus.puertos.es). Open-Meteo Marine es el respaldo fiable. La boya oficial sigue siendo la validación de referencia cuando esté arriba.

## EMODnet: rate-limiting (lección de la ejecución real)

- Llamadas rápidas en ráfaga devuelven **HTML de error** (no JSON) → falla `r.json()` con "Unexpected token '<'".
- Fix validado: reintentos con backoff (3 intentos, 1.5s·n) + pausa de ~800 ms entre spots. Con eso 8/8 spots OK.

## PDF real con puppeteer (Chrome headless)

- Generar HTML del informe → PDF vectorial real (269 KB) con el puppeteer ya instalado:
  ```js
  await page.goto('file:///ruta/informe.html', { waitUntil: 'networkidle0' });
  await p.pdf({ path: '...pdf', format: 'A4', margin: { top: '15mm', ... }, printBackground: true });
  ```
- El informe profesional incluye siempre: condiciones con fuente, física con su test avalador, sección "Procedimiento de validación para el revisor" con URLs exactas de EMODnet/StationData, y pie "Hecho con ❤️ por David Antizar".

## Mapa de puntos críticos en el informe (Leaflet headless → PNG incrustado)

- Patrón validado (`tests/mapa-criticos.mjs`): HTML con Leaflet de CDN → puppeteer headless espera `networkidle0` → captura `page.screenshot()` → PNG incrustado en el informe (ruta relativa `<img src="mapa-criticos.png">`).
- **Bug típico**: los overlays hacían `.addTo(m)` donde `m` era el **id del div**, no la variable del mapa (`mapa`) → error `t.addLayer is not a function` y marcadores invisibles. Nombrar distinto el div y la variable.
- Etiquetas permanentes: `L.tooltip({ permanent: true, direction: 'top' }).setLatLng(..).setContent(..).addTo(mapa)` — los tooltips no permanentes NO se ven en capturas headless.
- Debug: contar `Object.keys(mapa._layers).length` y escuchar `pageerror` antes de asumir que el tile/datos fallan; verificar el PNG con visión antes de entregarlo.

## Test real de Somo (patrón de validación con valor)

Preguntar "¿de verdad sirve?" → ejecutar caso real completo: transecto real de EMODnet (12 pts), serie horaria real de 14 días (360 registros), física aplicada hora a hora → ranking de días surfables (0.6–2.5 m + T≥8 s), primera rotura por escenario (swell/temporal/tormenta), y equivalencia de transporte de sedimento en "horas de temporal" (Q∝Hs^5). Resultado del test: la costa la esculpen los temporales invernales (2 semanas de verano ≈ 3.7 h de temporal de 3 m). Los datos están en `tests/test-somo.mjs` del repo (re-ejecutable).
