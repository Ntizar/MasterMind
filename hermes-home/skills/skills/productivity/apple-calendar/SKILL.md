---
name: apple-calendar
description: "Acceder, leer, crear, editar y eliminar eventos del calendario de Apple (iCloud CalDAV) de David Antizar. Usar para ver eventos próximos, organizar agenda, crear citas, editar o cancelar eventos."
version: 1.0.0
author: Mastermind
tags: [productivity, calendar, icloud, caldav]

---

# Apple Calendar (iCloud CalDAV)

Acceder y gestionar el calendario de iCloud de David Antizar.

## Credenciales

- **Username:** `dantizar@gmail.com`
- **Password de app:** `jxvr-knqs-hzsx-qcyc`
- **URL CalDAV:** `https://caldav.icloud.com`
- **TZ:** `Europe/Madrid`
- **Paquete:** `caldav` (pip install caldav) + `vobject` (pip install vobject)

## Calendarios disponibles

1. **Nosotros 🥰** (id: `8271049C-D351-4E88-A298-13CB3D7C0FE1`) - Eventos personales/pareja. **NUNCA usar para eventos del agente.**
2. **Oposición** (id: `895E66F3-9569-49E7-A46B-C925378F773B`) - Estudio oposición. Tiene espacio al final en el nombre: `"Oposición "`
3. **Casa** (id: `home`) - Eventos del hogar
4. **Recordatorios** (id: `tasks`) - Tareas/recordatorios
5. **Trabajo** (id: `work`) - Eventos laborales
6. **Mastermind Bot** (id: `fcb7cfb7-59ac-44a6-a920-c3b26fa6a1ee`) - Calendario automático del agente. Buscar por `"Mastermind Bot"` en display name.

## iCloud CalDAV Bug (CRÍTICO)

**Write-reliable, read-broken.** `cal.save()` siempre funciona (devuelve UID), pero `cal.events()`, `cal.date_search()`, `cal.search()` NUNCA devuelven eventos recién creados. Error `412 Precondition Failed` con `search(expand=True)`.

**Regla:** nunca confiar en caldav para lectura de eventos creados por caldav. La fuente de verdad es SIEMPRE la app iOS/Calendar.app. Si un evento se crea sin error HTTP → existe. Si caldav no lo devuelve → bug de iCloud, no problema de código.

**Workaround para lectura:** si necesitas leer eventos creados por el agente, verificar directamente en la app iOS. Para lectura programática, usar Google Calendar API o iCloud Calendar REST API (no CalDAV).

## Pasos

### 1. Leer eventos próximos

```python
python3 << 'PYEOF'
import caldav, vobject
from datetime import datetime, timedelta

client = caldav.DAVClient(
    url="https://caldav.icloud.com",
    username="dantizar@gmail.com",
    password="jxvr-knqs-hzsx-qcyc"
)
principal = client.principal()
calendars = principal.calendars()

now = datetime.now()
end = now + timedelta(days=N)  # N = días a buscar

for cal in calendars:
    name = cal.get_display_name()
    events = cal.events()
    for ev in events:
        ev.load()
        data = ev.get_data()
        vobj = vobject.readOne(data)
        for comp in vobj.components():
            if comp.name == "VEVENT":
                dtstart = comp.dtstart.value
                if hasattr(dtstart, 'date') and dtstart.date() >= now.date() and dtstart.date() <= end.date():
                    summary = str(comp.summary.value)
                    dtend = comp.dtend.value if comp.dtend else None
                    location = str(comp.location.value) if hasattr(comp, 'location') and comp.location else ''
                    print(f"  📌 {summary} | 🕐 {dtstart.strftime('%d/%m %H:%M')} - {dtend.strftime('%H:%M') if dtend else '?'} | 📍 {location}")
PYEOF
```

### 2. Crear un evento

```python
python3 << 'PYEOF'
import caldav
from datetime import datetime
import uuid

client = caldav.DAVClient(
    url="https://caldav.icloud.com",
    username="dantizar@gmail.com",
    password="jxvr-knqs-hzsx-qcyc"
)
principal = client.principal()
calendars = principal.calendars()

# Seleccionar calendario (por nombre)
cal = [c for c in calendars if c.get_display_name() == CALENDAR_NAME][0]

ical = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Mastermind//ES
BEGIN:VEVENT
DTSTART;TZID=Europe/Madrid:{start_str}
DTEND;TZID=Europe/Madrid:{end_str}
SUMMARY:{summary}
DESCRIPTION:{notes}
LOCATION:{location}
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:{uuid.uuid4()}
END:VEVENT
END:VCALENDAR"""

event = cal.save(ical)
print(f"Creado: {event.id}")
PYEOF
```

Donde:
- `CALENDAR_NAME` = nombre del calendario (ej: "Nosotros 🥰", "Trabajo")
- `start_str` = `YYYYMMDDTHHMMSS` (ej: `20260528T100000`)
- `end_str` = igual formato
- `summary` = título del evento
- `notes` = descripción (sin saltos de línea)
- `location` = ubicación
- `uid` = UID único (usar UUID)

### 3. Editar un evento

```python
python3 << 'PYEOF'
import caldav, vobject, uuid

client = caldav.DAVClient(
    url="https://caldav.icloud.com",
    username="dantizar@gmail.com",
    password="jxvr-knqs-hzsx-qcyc"
)
principal = client.principal()
calendars = principal.calendars()

# Encontrar evento
cal = [c for c in calendars if c.get_display_name() == CALENDAR_NAME][0]
events = cal.events()
target = None
for ev in events:
    ev.load()
    data = ev.get_data()
    vobj = vobject.readOne(data)
    for comp in vobj.components():
        if comp.name == "VEVENT" and str(comp.summary.value) == OLD_SUMMARY:
            target = ev
            break

if target:
    target.edit_icalendar_component('VEVENT', {
        'summary': NEW_SUMMARY,
        'dtstart': new_start,
        'dtend': new_end,
    })
    print(f"Editado: {target.id}")
PYEOF
```

### 4. Eliminar un evento

```python
python3 << 'PYEOF'
import caldav

client = caldav.DAVClient(
    url="https://caldav.icloud.com",
    username="dantizar@gmail.com",
    password="jxvr-knqs-hzsx-qcyc"
)
principal = client.principal()
calendars = principal.calendars()

cal = [c for c in calendars if c.get_display_name() == CALENDAR_NAME][0]
events = cal.events()
for ev in events:
    ev.load()
    data = ev.get_data()
    if OLD_SUMMARY in data:
        ev.delete()
        print(f"Eliminado: {ev.id}")
        break
PYEOF
```

## Fallback: Google Calendar API

Si iCloud CalDAV no responde (timeout, 412, eventos vacíos), usar Google Calendar API vía `google-workspace` skill. Es más rápido y fiable para lectura de eventos.

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
$GAPI calendar list --start 2026-05-26T00:00:00+02:00 --end 2026-05-26T23:59:59+02:00
```

Nota: los calendarios iCloud y Google pueden no estar sincronizados. Para eventos del agente (Mastermind Bot), verificar siempre en la app iOS como fuente de verdad.

## Pitfalls

- **NUNCA** hardcodear credenciales en el chat — siempre usar el script directo
- Los eventos sin hora específica (todo el día) tienen `DTSTART` sin `T`
- Para crear eventos con `delegate_task` o cron, pasar las credenciales como env vars
- Si hay error de conexión, verificar que el servidor tenga acceso a `caldav.icloud.com`
- **vobject** es requerido por `caldav` para parsear los datos ICS — instalar con `pip install vobject`
- Para acceder a valores vobject: usar `.value` (no `.get()`) — ej: `comp.summary.value`, `comp.dtstart.value`
- **caldav + iCloud bug:** `cal.events()` y `cal.search()` pueden devolver 0 eventos aunque los eventos se crearon correctamente (sin error). Los eventos pueden existir en iCloud pero la API de caldav no los lista. Verificar en la app de iOS/Calendar.app como fuente de verdad.
- **caldav + iCloud bug workaround:** si `cal.events()` devuelve 0 pero los eventos se crearon, usar `cal.date_search()` con un rango amplio (años) en lugar de `cal.search()`. Si tampoco funciona, los eventos probablemente están en el calendario pero caldav no los puede listar.
- **Script de sincronización BiciMad:** `/hermes-home/scripts/bicimad-calendar-sync.py` crea 10 eventos diarios en el calendario "Mastermind Bot". Se ejecuta con `no_agent=true` y hardcodea las credenciales como fallback de `ICLOUD_APP` env var. Busca calendario con `"Mastermind Bot"` en el display name.
- **NUNCA usar calendario "Nosotros 🥰" para eventos del agente** — es de la pareja.
- **Cron para calendar sync:** job_id `d689240b09b5`, cron `1 0 * * *` (00:01 Madrid), no_agent=true, script `hermes-home/scripts/bicimad-calendar-sync.py`.
- **ICLOUD_APP en Hermes:** variable añadida a `/opt/hermes/.env` para que los crons puedan usarla.
