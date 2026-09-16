# 2026-09-16 — SunCalc v2: migración pendiente en SolMAD y sombras solares

Hallazgo del batch de stars de hoy (mourner/suncalc, 3.471⭐). **SolMAD (y cualquier proyecto de sombras propio) está pinneado a `suncalc@^1.9.0`** y SunCalc 2.0.2 (2026-09-02) es una reescritura con ruptura de convenciones:

| | v1 (actual) | v2 |
|---|---|---|
| Ángulos | radianes | **grados** |
| Azimut | 0 = SUR | **0 = NORTE, CW** |
| Import | default CJS | ESM-first (`import * as SunCalc`) |
| Altitud | geométrica | aparente (refracción) |
| Evento inexistente | `Invalid Date` | `null` + `alwaysUp/alwaysDown` |
| Precisión sol | ~0.43° / ~75s | ~0.08° / ~15s |

**Trampa específica para SolMAD:** nuestro patrón convierte el azimut v1 con `(azFromSouth + 180 + 360) % 360` (`src/lib/sun.ts`). Con v2 eso suma 180° de más → las sombras se trazarían en dirección opuesta sin ningún error visible. La migración exige borrar la conversión, pasar los inputs angulares a grados y cambiar las comprobaciones de fecha a `=== null`.

**Ganancia si se migra:** ±15s en salidas/puestas y altitud aparente refractada → la hora en que una terraza "pierde el sol" por el raytraceo deja de bailarle 1-3 minutos respecto a lo observable; relevante para el caché por franjas de 15 min (v1 podía desfasar una franja entera en el crepúsculo).

**Decisión del batch:** skill propio NO (ChromaDB dedup 0.63 contra `solar-shadow-computation`; SunCalc ya está citado en 3 skills solares) → UPGRADE de `solar-shadows-web-workers` a v1.1.0 con la sección "SunCalc v2" + pitfall versión-dependiente. La migración real de SolMAD queda pendiente de ventana de QA (no es urgente: v1 sigue funcionando, solo es menos preciso).

Ref: release notes v2.0.0 (gh api), README actualizado 2026-09-16.
