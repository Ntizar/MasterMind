# Patrón de debugging para round-trip NeTEx↔GTFS

## Sesión 15 Jul 2026: diagnóstico y fixes

### Problema original
Round-trip Ouigo: GTFS→NeTEx→GTFS perdía 100% de trips y stop_times.

### Diagnóstico paso a paso

1. **Verificar writer genera XML válido**: `gtfs-to-netex-es --input ouigo --output /tmp/out.xml`
   - Validar con validator: 0 errores, 3 warnings triviales
   
2. **Verificar reader lee el XML**: cargar XML en reader y verificar contadores
   ```python
   from netex_es_to_gtfs.netex_reader import NeTExReader
   r = NeTExReader('/tmp/out.xml')
   feed = r.read()
   print(f"Trips: {len(feed.trips)}, StopTimes: {len(feed.stop_times)}")
   ```

3. **Comparar estructura XML vs código reader**: buscar en XML qué elementos existen y qué busca el reader
   ```bash
   grep -o '<ServiceJourney[^>]*' file.xml  # Verificar nombre de elemento
   grep -o '<passingTimes>' file.xml        # Verificar passingTimes vs calls
   grep -o '<DayTypeRef\|dayTypes' file.xml  # Verificar dayTypes vs DayTypeRef
   ```

### Fixes aplicados

1. **ServiceJourney vs VehicleJourney**: reader buscaba `VehicleJourney`, writer genera `ServiceJourney` (NeTEx-CEN). Cambiar una línea en `_read_vehicle_journeys()`.

2. **passingTimes vs calls**: reader buscaba `<calls><Call>`, writer genera `<passingTimes><TimetablePassingTime>`. Soporte añadido en reader (línea 535-561).

3. **DayTypeRef vs dayTypes**: reader buscaba elemento `DayTypeRef`, writer genera atributo `dayTypes ref="..."`. Soporte añadido en `_read_vehicle_journeys()`.

4. **_extract_trip_id con sufijo _N**: writer añade sufijo counter (`TRIP001_1`). Reader debe limpiarlo con regex `re.sub(r'_\d+$', '', last)`.

5. **Normalización de DayType IDs**: IDs con case inconsistente se solapan al normalizarse. Usar `set` de fechas + deduplicate.

6. **Inferencia de calendars con 300+ fechas**: threshold de 300 fechas para saltar inferencia.

### Patrón de verificación post-fix
```python
# 1. Verificar reader lee el XML
r = NeTExReader('output.xml')
feed = r.read()
assert len(feed.trips) > 0, "Reader no lee trips"
assert len(feed.stop_times) > 0, "Reader no lee stop_times"

# 2. Verificar round-trip completo
reader_orig = GTFSReader('original-gtfs/')
feed_orig = reader_orig.read()
writer = NeTExWriter(feed_orig, Config())
writer.to_file('/tmp/rt.xml')
reader_rt = NeTExReader('/tmp/rt.xml')
feed_rt = reader_rt.read()

for entity in ['stops', 'routes', 'trips', 'stop_times']:
    orig_count = len(getattr(feed_orig, entity))
    rt_count = len(getattr(feed_rt, entity))
    assert orig_count == rt_count, f"{entity}: {orig_count} → {rt_count}"
```

### Herramientas útiles
```bash
# Verificar estructura XML
grep -o '<[^>]*>' file.xml | sort | uniq -c | sort -rn

# Contar elementos específicos
grep -c 'ServiceJourney' file.xml
grep -c 'TimetablePassingTime' file.xml
grep -c 'DayType id=' file.xml

# Normalizar IDs para debug
python3 -c "
import re
ids = ['ES:DAY_TYPE:MTM:MondayToFriday', 'ES:DayType:MondayToFriday']
for id in ids:
    last = id.split(':')[-1]
    snake = re.sub(r'(?<=[a-z])(?=[A-Z])', '_', last).upper()
    print(f'{id} → {snake}')
"
```