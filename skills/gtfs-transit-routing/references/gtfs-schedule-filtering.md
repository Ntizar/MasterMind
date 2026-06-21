# Filtrado de Horarios GTFS

## calendar.txt

```
service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date
WEEKDAY,1,1,1,1,1,0,0,20240901,20250101
WEEKEND,0,0,0,0,0,1,1,20240901,20250101
```

**Uso:** Para filtrar por día laborable:
```javascript
function isWeekday(serviceId, calendar) {
  const service = calendar.find(c => c.service_id === serviceId);
  if (!service) return true; // fallback: incluir si no hay info
  const day = new Date().getDay(); // 0=domingo, 1=lunes...
  const col = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday'][day];
  return service[col] === '1';
}
```

## calendar_dates.txt

Algunos feeds usan solo `calendar_dates` para excepciones:
```
service_id,date,exception_type
WEEKDAY,20241225,2  // 2 = excluded (Navidad)
WEEKDAY,20241226,2  // 2 = excluded
WEEKDAY,20250101,2  // 2 = excluded (Año Nuevo)
```

**exception_type:** 1 = added, 2 = removed

**Lógica combinada:**
1. Si hay `calendar.txt`: usar como base
2. Si hay `calendar_dates.txt`: aplicar excepciones sobre la base
3. Si solo hay `calendar_dates.txt`: solo los service_ids con exception_type=1 son válidos

## Horarios Laborales para TimeIneco

| Tipo | Ventana | Uso |
|------|---------|-----|
| Mañana (ida) | 07:30 - 09:30 | Llegada al trabajo |
| Tarde (vuelta) | 16:30 - 18:30 | Salida del trabajo |

**Implementación:**
```javascript
function isLaboralHorario(timeStr) {
  const sec = parseTime(timeStr);
  const morningStart = parseTime("07:30:00");
  const morningEnd = parseTime("09:30:00");
  const eveningStart = parseTime("16:30:00");
  const eveningEnd = parseTime("18:30:00");
  return (sec >= morningStart && sec <= morningEnd) ||
         (sec >= eveningStart && sec <= eveningEnd);
}
```

## Pitfalls

- **Horarios 24h+:** Algunos trips empiezan a las 23:00 y terminan a las 01:00. `stop_sequence` indica orden, no hora.
- **Frecuencia vs horario:** Algunos buses (líneas nocturnas, frecuencia alta) no tienen `stop_times` detallados. En ese caso, usar frecuencia estimada (ej: cada 10 min).
- **Días festivos:** `calendar_dates` con `exception_type=2` puede excluir días que `calendar.txt` marca como laborables.
