# Análisis de Datos Extraídos CIAF — Post-Extracción

## Contexto

Una vez extraídos los 270+ informes CIAF a JSON (vía `liteparse` o pipeline manual), el siguiente paso es **interpretar los datos como un humano** y producir un resumen ejecutivo accionable. Este reference documenta esa metodología.

## Metodología de análisis

### 1. Carga masiva y validación

```python
import json, os
from collections import defaultdict, Counter

data_dir = "data/individual"
reports = []
for filename in os.listdir(data_dir):
    if filename.endswith('.json'):
        with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
            reports.append(json.load(f))
```

**Validar:** Total de informes, años cubiertos, campos nulos, IDs duplicados.

### 2. Dimensiones de análisis

| Dimensión | Qué buscar | Herramienta |
|-----------|-----------|-------------|
| **Temporal** | Evolución de víctimas, fatalidades por año, tendencias | `defaultdict` + sorted |
| **Geográfica** | Provincias/estaciones más accidentadas | Counter por provincia |
| **Causas raíz** | Keywords en conclusiones (señal, maquinista, procedimiento) | Substring matching en `conclusiones[]` |
| **Grave vs menor** | Qué diferencia los accidentes graves de los menores | Filtrar por `gravedad` field |
| **Horaria** | Picos de incidentes por hora | Extraer de `hora` field |
| **Tipo de suceso** | Colisión vs descarrilamiento vs incidente | Counter por `tipo` |
| **Trenes** | Tipos de tren más afectados | Counter por `trenes[].tipo` |

### 3. Keywords de causas CIAF

Extraídas de análisis de 270 informes reales. Usar para substring matching en `conclusiones[]`:

| Keyword | Significado | Menciones típicas |
|---------|------------|-------------------|
| `señal` | Problemas de señalización (aspecto indebido, fallo ASFA) | ~138 |
| `maquinista` | Error humano del conductor (distraído, cansado, mal formado) | ~102 |
| `procedimiento` | Incumplimiento de protocolos de seguridad | ~30 |
| `formación` | Déficit de capacitación | ~28 |
| `comunicación` | Falta de comunicación entre CTC, RC y maquinista | ~11 |
| `velocidad` + `exces` | Exceso de velocidad | ~6 |
| `paso a nivel` | Invaders en pasos a nivel (vehículos, personas) | ~57 |
| `rocas` / `desprendimiento` | Obstáculos en vía | ~8 |
| `material rodante` / `material móvil` | Fallo mecánico del tren | ~36 |
| `infraestructura` | Problemas de vía, drenaje, muros | ~55 |

**Pitfall:** Las menciones NO son exclusivas. Un accidente puede tener "maquinista" + "señal" + "procedimiento". Usar Counter normalizado, no filtrar por top-1.

### 4. Producción del resumen ejecutivo

**Estructura recomendada:**
1. **Visión general** — Total informes, período, víctimas totales
2. **Top 10 peores accidentes** — Por víctimas, con resumen de cada uno
3. **Causas raíz más comunes** — Ranking con barra visual
4. **Hallazgos clave** — Letras A, B, C... con narrativa
5. **Evolución temporal** — ¿Hemos mejorado? Con matices
6. **Recomendaciones frecuentes** — Qué entidades receive qué types
7. **Acciones prioritarias** — 3-5 recomendaciones concretas

**Estilo:** Narrativo, como un humano que "entiende qué pasó", no como una tabla fría. Usar frases como "el patrón es claro", "la buena noticia es", "ojo con".

### 5. CIAF — Hallazgos del dataset completo (2007-2025)

**Los 5 peores:**
1. Santiago de Compostela (2013): 80 muertos — exceso velocidad + ASFA + maquinista
2. Estación de França, Barcelona (2017): 60 heridos — maquinista no frenó
3. Vacarisses, Barcelona (2018): 1 muerto, 52 heridos — rocas por muro colapsado
4. Arahal, Sevilla (2017): 31 heridos — inundaciones
5. Castellgalí, Barcelona (2019): 1 muerta, 108 heridos — contravía

**Patrón Barcelona:** 44 informes, provincia más accidentada. Rodalies concentra siniestralidad.

**Tendencia post-Santiago:** Fatalidades bajan drásticamente (39→0 fallecidos entre 2008→2022 en accidentes principales), pero cantidad de informes no baja.

**Picos horarios:** 09:00-12:00 y 19:00-21:00 — horas punta de frecuencia.

### 6. Pitfalls del análisis

- **Recomendaciones son `dict[]`, no `string[]`:** Formato `{'numero': '51/2016 - 1', 'destinatario': '...', 'texto': '...'}`. Acceder a `rec['texto']` no `rec.lower()`.
- **Campos nulos:** Muchos informes antiguos (2007-2010) tienen `null` en campos como `hora`, `comunidad`, `operador`. Usar `r.get('campo', default)`.
- **Encoding:** Tildes y ñ en títulos/resúmenes. Siempre `encoding='utf-8'`.
- **Tipo vs gravedad:** `tipo` es "accidente"/"incidente"/"descarrilamiento". `gravedad` es "grave"/"menor". Son independientes.
- **Años sin datos:** 2015 tiene 10 informes pero 0 víctimas — solo incidentes operacionales menores.
