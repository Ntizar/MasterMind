# Web App Integration Testing — Patrón de auditoría para apps con APIs externas

Cuando se audita una aplicación web que depende de APIs externas (ORS, Nominatim, GTFS, Idealista, etc.), NO basta con leer el código — hay que **ejecutar la app y testear cada integración**.

## Flujo de verificación (4 pasos)

### Paso 1: Levantar el servidor y verificar health

```bash
# Arrancar en background
node server.mjs &
sleep 2
curl -s http://localhost:4000/healthz | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'Status: {d[\"status\"]}')
print(f'ORS API: {d[\"checks\"][\"ors_api\"]}')
"
```

**Qué buscar:** El healthcheck debe reportar qué APIs están configuradas. Si dice `ors_api: true` pero las requests fallan → key revocada/expirada.

### Paso 2: Testear API key directamente vs. vía proxy

```bash
# Test directo a la API externa (sin proxy)
ORS_KEY=$(grep ORS_API_KEY .env | cut -d= -f2)
curl -s -o /dev/null -w "%{http_code}" \
  -X POST "https://api.openrouteservice.org/v2/isochrones/driving-car" \
  -H "Authorization: $ORS_KEY" \
  -H "Content-Type: application/json" \
  -d '{"locations":[[-3.7038,40.4167]],"range":[1800],"range_type":"time"}'

# Test vía proxy local
curl -s -X POST http://localhost:4000/isochrone \
  -H 'Content-Type: application/json' \
  -d '{"profile":"driving-car","locations":[[-3.7038,40.4167]],"range":[1800],"range_type":"time"}'
```

**Diagnóstico:**
| Directo | Proxy | Diagnóstico |
|---------|-------|-------------|
| 200 OK | 200 OK | ✅ Todo funciona |
| 403 Forbidden | Error/Fallback | 🔴 Key revocada o expirada |
| 401 Unauthorized | Error/Fallback | 🔴 Key inválida |
| 200 OK | Error | 🟠 Bug en el proxy (bad request forwarding) |
| Timeout | Timeout | 🟠 API caída o red bloqueada |

### Paso 3: Verificar calidad de datos cacheados/semilla

```bash
# Para GTFS cache u otros datasets semilla
python3 -c "
import json
with open('data/gtfs-cache.json') as f:
    data = json.load(f)
print(f'Routes: {len(data.get(\"routes\",[]))}')
print(f'Stops: {len(data.get(\"stops\",[]))}')
print(f'Trips: {len(data.get(\"trips\",[]))}')    # 0 = sin datos reales
print(f'Stop_times: {len(data.get(\"stop_times\",[]))}')  # 0 = sin horarios
print(f'Shapes: {len(data.get(\"shapes\",[]))}')   # 0 = sin geometrías
"
```

**Criterio de calidad GTFS:**
- `trips > 0` AND `stop_times > 0` → ✅ Datos reales o semi-reales
- `trips == 0` AND `stop_times == 0` → 🔴 Datos ficticios (solo estructura, sin contenido)
- `routes > 0` pero con nombres "1", "2", "3" → 🔴 Nombres genéricos, no reales

### Paso 4: Test de geocoding

```bash
curl -s "http://localhost:4000/geocode?q=Plaza+Mayor+Madrid" | python3 -c "
import json,sys
d=json.load(sys.stdin)
if d:
    print(f'✅ Geocode: {d[0].get(\"display_name\",\"?\")[:60]}')
else:
    print('❌ Sin resultados')
"
```

## Patrón de detección: "Simulado vs. Real"

En很多 aplicaciones, el frontend muestra si los datos son "reales" o "simulados". Buscar en el código:

```bash
# Buscar indicadores de modo simulado
grep -rn "simulado\|simulación\|fallback\|ORS.*no\|sin.*key" js/
grep -rn "real.*ORS\|ORS.*real\|📡\|💠" js/
```

**En el informe/DOCX:** Si el informe dice "ORS" o "Simulado", verificar que el "ORS" es real (paso 2 confirmado) y no solo una etiqueta en el código.

## Patrón: "GTFS sin datos reales = transporte público decorativo"

Cuando el GTFS cache tiene 0 trips/stop_times pero la app muestra "46 rutas disponibles":
1. El sistema de matcheo por nombre (fallback) genera resultados falsos
2. Las "paradas cercanas" son por distancia geográfica, no por rutas reales
3. El informe incluye secciones de "transporte público" que no aportan información útil
4. **Conclusión para el usuario:** "El transporte público en el informe es decorativo — no hay datos reales de horarios ni rutas"

## Pitfalls

- **No asumir que la API funciona porque el healthcheck dice OK** — El healthcheck solo verifica que la variable de entorno existe, no que la key sea válida. Siempre hacer el request real.
- **El proxy puede enmascarar errores** — Si el proxy retorna 200 con un body de error de la API externa, el frontend puede confundirse. Verificar el HTTP status Y el body.
- **Datos cacheados en localStorage del navegador** — El usuario puede tener datos viejos cacheados. Pedir que limpie localStorage o probar en modo incógnito.
- **Simulación puede ser más pequeña que la realidad** — Las isocronas simuladas sin red viaria real suelen subestimar áreas peatonales y sobreestimar áreas de coche.
