# Pipeline de depuración validador español — Sesión Ouigo (2026-07-15)

## Progreso: 2.908 → 0 errores 🎉

| Categoría | Antes | Después | Técnica |
|-----------|-------|---------|---------|
| ES_ID_FORMAT | 460 | 0 | `_make_id()` centralizado + UPPER_SNAKE_CASE |
| NETEX_ID_5 | 2.662 | 0 | Unificar IDs (definición = referencia) |
| SERVICE_JOURNEY_3 | 68 | 0 | `passingTimes` + `TimetablePassingTime` |
| SERVICE_JOURNEY_15 | 68 | 0 | `ArrivalTime`/`DepartureTime` texto directo |
| LINE_4 | 11 | 0 | `TransportMode` con mayúscula |
| ROUTE_3 | 11 | 0 | `lineRef` en cada Route |
| JOURNEY_PATTERN_2 | 11 | 0 | `journeyPatternElements` wrapper |
| ROUTE_4 | 11 | 0 | `pointsInSequence` (no `routeElements`) |
| XPATH_1 | 3 | 0 | `./*` → `/*` en XPath (context node) |
| COMPOSITE_FRAME_1/3 | 2 | 0 | `validityConditions` wrapper + validador busca dentro |
| COMPOSITE_FRAME_6 | 1 | 1 (WARN) | AvailabilityCondition — no crítico |
| **Total errores** | **2.908** | **0** | ✅ |

## Flujo de depuración

1. **Generar XML** con feed real (Ouigo)
2. **Validar** con `netex-es-validator --verbose`
3. **Agrupar errores**: `grep ERROR | sed ... | sort | uniq -c | sort -rn`
4. **Analizar el error más numeroso** y atacarlo primero
5. **Arreglar** en el generador (prioridad) o en el validador (cuando el validador tiene bugs)
6. **Regenerar** y volver al paso 2

## Arreglos en el generador

### 1. ID centralizado (`_make_id`)
```python
def _make_id(self, tipo: str, secuencia: str) -> str:
    import re
    # CamelCase → UPPER_SNAKE_CASE
    tipo_up = re.sub(r'(?<=[a-z])(?=[A-Z])', '_', tipo).upper()
    # Sanitizar : en secuencia
    seq_clean = secuencia.replace(':', '_').upper()
    op = self._get_operator_code()
    return f"{self.config.frame_id_prefix}:{tipo_up}:{op}:{seq_clean}"
```

### 2. Elementos de paso (TimetablePassingTime)
```python
# WRONG:
el("calls")
el("Call", {...})
el("Arrival")
arr.append(time_element(time))

# RIGHT:
el("passingTimes")
el("TimetablePassingTime", {...})
child(tpt, "ArrivalTime", time_str)  # "17:02:00" directo
child(tpt, "DepartureTime", time_str)
```

### 3. ValidityConditions en CompositeFrame
```python
vb = el("ValidBetween", {"version": "1"})
# ... FromDate/ToDate ...
vc = el("validityConditions")
vc.append(vb)
frame.append(vc)
# NOT: frame.append(vb)  ← sin wrapper
```

### 4. JourneyPattern → journeyPatternElements
```python
jpe = el("journeyPatternElements")
# ... StopPointInJourneyPattern ...
jp.append(jpe)
# NOT: el("pointsInSequence")  ← eso es para Route
```

### 5. Route → lineRef
```python
ref(route_elem, "lineRef", writer._make_id("Line", route.route_id))
```

### 6. Filtrar viajes sin stop_times
```python
# En create_vehicle_journeys:
trip_stop_times = [st for st in (writer.feed.stop_times or [])
                  if st.trip_id == trip.trip_id]
if not trip_stop_times:
    continue  # Saltar — SERVICE_JOURNEY_3
```

## Arreglos en el validador

### Regla LINE_4 — Case del elemento
```python
# ANTES (no encuentra):
tm = line.find("netex:transportMode", self.NS)
# DESPUÉS:
tm = line.find("netex:TransportMode", self.NS)
```

### Regla ROUTE_4 — Nombre del elemento
```python
# ANTES (no encuentra):
r_elems = route.find("netex:routeElements", self.NS)
# DESPUÉS:
r_elems = route.find("netex:pointsInSequence", self.NS)
```

### Regla SERVICE_JOURNEY_15 — ArrivalTime anidado
```python
# ANTES (busca directo en passingTimes, no encuentra):
pt_elem.findall("netex:arrival", self.NS)
# DESPUÉS (busca dentro de TimetablePassingTime):
pt_elem.findall(".//netex:ArrivalTime", self.NS)
```

### Regla XPATH_1 — Contexto del XPath
```python
# ANTES (aplica a children del root element, encuentra falsos positivos):
xpath="./*[not(self::netex:PublicationDelivery)]"
# DESPUÉS (aplica al documento raíz, solo busca si el root no es PublicationDelivery):
xpath="/*[not(self::netex:PublicationDelivery)]"
# El error era que `./*` buscaba dentro de PublicationDelivery, no en el documento.
```

### Regla COMPOSITE_FRAME_3 — Ubicación de ValidBetween
```python
# ANTES (busca directo en CompositeFrame, no encuentra):
vb = cf.find("netex:validBetween", self.NS)
# DESPUÉS (busca dentro de validityConditions, con PascalCase):
vc = cf.find("netex:validityConditions", self.NS)
vb = vc.find("netex:ValidBetween", self.NS) if vc is not None else None
```

## Trampas del `patch` tool

⚠️ **El `patch` tool elimina la indentación de la primera línea** cuando se reemplazan bloques multilínea. Tras cada patch, verificar con `read_file` que la indentación sea correcta. El patrón clásico de error:

```
# Antes del patch (correcto):
        vb = el("ValidBetween", {"version": "1"})
        fb = el("FromDate")

# Después del patch (indentación perdida en línea 1):
vb = el("ValidBetween", {"version": "1"})
        fb = el("FromDate")
```

**Solución:** Tras un patch multilínea, compilar con Python y arreglar indentaciones con `patch` de una línea.

## Reglas de oro

1. **Nunca concatenar IDs manualmente** — siempre usar `_make_id()`
2. **El validador español es la fuente de verdad** para el perfil ES, pero tiene bugs (element naming, XPath)
3. **SERVICE_JOURNEY_3** es un error real (viaje sin stop_times) — filtrar en generación
4. **ES_ID_FORMAT** se arregla con un solo helper centralizado + UPPER_SNAKE_CASE
5. **NETEX_ID_5** se arregla asegurando que definición y referencia usen el mismo generador de IDs
6. **Los elementos de NeTEx son PascalCase** (TransportMode, ArrivalTime, DepartureTime, ValidBetween, etc.) — SIEMPRE
7. **El XSD oficial y el validador español pueden diferir** en nombres de elementos — arreglar el que tenga el bug