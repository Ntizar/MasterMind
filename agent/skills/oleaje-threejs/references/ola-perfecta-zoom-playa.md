# Ola perfecta — zoom de playa: dónde rompe exactamente la ola (fase 3 de la app de mejores olas)

Módulo `tests/ola-perfecta.mjs` + `tests/mapa-ola-perfecta.mjs` (commit `d0acf17`). Pipeline:
ranking (qué playa) → **zoom (dónde exactamente en la playa)** → siguiente: cuándo (animación por horas + Telegram).

## Pipeline

1. **Rejilla batimétrica fina EMODnet**: 15×15 sondas en 1,4 km de lado (~86 m/punto, como Studio zoom≥14) centrada en la playa. Cada sonda con reintentos + backoff (algunas peticiones fallan con HTML/error del servicio; 4 intentos, pausa 1,5·i s).
2. **Posición EXACTA de la playa por Nominatim** (ver lección 1): `https://nominatim.openstreetmap.org/search?q=Playa+de+Somo+Cantabria&format=json&limit=1` con User-Agent propio → way 516058323, centro 43.4594/-3.7314 y boundingbox.
3. **Motor 2D de rayos** (reutilizar la física del Studio, no reescribir): 7 rayos desde el borde de mar de la rejilla, propagación con `dα/ds = -(1/c)·∂c/∂n` sobre gradiente de c interpolado bilinealmente, `c = sqrt(9.81·h)` shallow, paso 50 m. Hs local por shoaling puro `Ks = sqrt(cg(30)/cg(h))` (shallow: cg≈c/2). **Rotura**: primer punto con `HsLocal > 0.78·h` → el rayo TERMINA ahí (no sigue a tierra).
4. **Mapa Leaflet zoom playa** (`ola-perfecta.html`): rejilla como círculos translúcidos, rayos polyline azules, roturas como circleMarker rojo + **tooltip permanente** `L.tooltip({permanent:true, direction:'top'})` con `⭐ X.X m` (tooltips no permanentes no salen en screenshots headless).
5. **Verificación**: screenshot puppeteer headless (`--enable-unsafe-swiftshader`) + revisión con visión; comprobar que rayos/marcadores caen SOBRE el agua junto a la orilla.

## Resultados validados (3 playas, misma condición NW/NNW 1 m–1.2 m · T 9–10 s)

- **Somo** (barra recta): reparto parejo 0.7–2.1 m, máx en el extremo norte de la barra (Los Lloros/Hocico de la Peña) por convergencia de ortogonales.
- **Suances — Los Locos** (cabo convergente): La Roca Blanca concentra energía → **rompe más grande que el Hs offshore** (1.47 m vs 1.0 m); la zona central abrigada por el falso cabo del faro queda a 0.26–0.46 m. Firmas físicas de cabos: espirales de rayos rodeando la punta.
- **Liencres — Playa del Madero** (ría con canal): la boca del Pas disipa la ola (0.36 m); dos células separadas: sector oeste Canallave/Madero (1.4–1.7 m, abierta y regular) y esquina de Somocuevas (concentrada más chica).
- Cada playa tiene una "huella" distinta detectable en los puntos de rotura: barra recta = reparto parejo, cabo = pico > Hs offshore junto a la punta, ría = mínimo de energía en la boca. Comparar la huella del resultado con el tipo de spot como validación física.

## Replicar en una playa nueva (patrón barato, ~1 min + 45 s de sondas)

1. Coordenadas por Nominatim (`curl -A 'water3j/1.0' 'https://nominatim.openstreetmap.org/search?q=Playa+de+X&format=json&limit=1'`) — usar el centro del way `natural=beach`.
2. Copiar `tests/ola-suances.mjs` → `tests/ola-<playa>.mjs` cambiando `NOMBRE`, `C` y el spot del ranking que da la condición (si la playa no está en el ranking, usar la de la costa vecina — misma exposición).
3. Copiar `tests/mapa-suances.mjs` y `tests/shot-suances.mjs` cambiando nombres de fichero y título.
4. **Ojo con el título del mapa**: al copiar hay que reemplazar el nombre en el string del título también (Liencres salió con cabecera genérica correcta tras el replace, pero verificar con grep `grep -o 'Ola perfecta[^<]*'`).
5. Verificar con visión: roturas sobre el agua junto a la orilla, etiquetas `⭐ X.X m` con número.

## Lecciones duras (cada una costó un ciclo de debug)

1. **Verificar coordenadas de la playa con Nominatim ANTES de descargar batimetría.** Los spots del ranking estaban desplazados ~3 km (caían tierra adentro). Síntoma: el mapa muestra barrios/valle, no mar. OSM way "natural=beach" da centro + bbox fiables. Nombres de spots de un ranking hecho a mano NO son coordenadas de playa.
2. **CONVENCIÓN DEL SIGNO DE EMODnet (T17, lección dura re-aprendida)**: EMODnet `avg` NO tiene signo inconsistente — tiene una convención fija: **negativo = agua (profundidad = -avg), positivo = tierra (elevación, sin profundidad válida → h=null)**. Prueba real: casco de Loredo `avg=+34.1`, mar abierto `avg=-2.35`. **NUNCA usar `Math.abs(j.avg)`**: convierte elevaciones terrestres en "profundidades" y produce OLAS DENTRO DE LA TIERRA (bug raíz cazado por David). Umbral conservador: solo `avg < 0` es agua; `avg >= 0` → tierra. Cubierto por T17 en `tests/tanda10.mjs` (7/7), incluida la invariante "ninguna rotura con h inválida" sobre los JSON reales.
3. **Los valores de EMODnet en tierra/marisma no valen cero**: con la convención T17 la máscara los excluye sola (`avg>=0` → tierra → h=null). Para la rejilla VISUAL filtrar a `h>2 m` (agua franca). El rayo muere en `h=null` (tierra) o en su rotura — nunca seguir tras romper. Si aún se ven rayos en tierra, sospechar convención del signo (lección 2) o abanico de partida demasiado ancho (multiplicador 1.1 sobre el semiancho, no 1.3–1.4, para no coger la marisma lateral).
4. **Geometría de propagación**: lat menor = mar al sur o norte según costa — decidir con el transecto ya validado (en Somo el mar está al NORTE del transecto antiguo: 43.398 → 79 m, 43.443 → costa). Azimut y convención sin(α)/cos(α) del avance: comprobar con el primer punto del rayo antes de 200 pasos.
5. **Interpolador bilineal**: rechaza bordes (`i>=14`) → arrancar el rayo 100 m DENTRO del borde, no exactamente en el borde (fy=14.0 → null → traza vacía).
6. **`.addTo(mapa)` vs div id**: en Leaflet, `L.map('m')` devuelve la variable; si los overlays usan otra (p.ej. `m` que es el id) sale `t.addLayer is not a function` y el mapa se ve vacío sin marcadores. Debug con `p.on('pageerror')`.
7. **Vision cache**: al re-capturar screenshots con el mismo nombre de archivo, usar nombre nuevo o query en la URL; el analizador de imagen puede devolver la captura vieja.
8. **Sondear 225 puntos tarda ~45 s** con cortesía entre llamadas: para varias playas, cachear la rejilla en IndexedDB (ya existe store de batimetría en el Studio) o batchear puntos por petición (EMODnet acepta MULTILINESTRING/WKT).
9. **Interpolación de variables en generadores HTML anidados**: al escribir el generador del mapa (Node) que produce HTML con template literals, distinguir `${var}` que Node interpola al generar de `${var}` que el navegador debe evaluar. Si queda literal (`setContent('${r.HsRompe} m')` visible en el tooltip), es que se escapó de más: interpolar SIEMPRE en Node con los datos del JSON (`'⭐ ${r.HsRompe} m'` dentro del template del generador). Verificar el HTML final con grep antes de capturar.
10. **Generar scripts de playa por clonación con replaces**: clonar `ola-suances.mjs` → `ola-<playa>.mjs` con `.replace()` es rápido, pero el `const NOMBRE = '...'` puede romperse si el replace sustituye `NOMBRE` por un literal con espacios (falla `const 'Suances (Los Locos)' = ...`). Reparar con un patch puntual y verificar con `node --check` implícito al ejecutar.
