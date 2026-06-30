# iCloud CalDAV Bug - caldav library

## Problema

iCloud CalDAV es **write-reliable, read-broken** con la librería `caldav` Python.

### Síntomas

- `cal.events()` devuelve 0 eventos aunque los eventos existen en iCloud
- `cal.search(summary=..., start=..., end=...)` devuelve error `412 Precondition Failed`
- `cal.date_search()` devuelve 0 eventos
- `cal.save(ical)` funciona perfectamente y devuelve UID

### Causa

iCloud CalDAV no soporta correctamente las queries CalDAV REPORT. Los eventos se crean y sincronizan en iCloud, pero las consultas CalDAV no los devuelven.

### Workaround

1. **Crear/editar/eliminar:** caldav funciona perfectamente. `cal.save()` devuelve UID válido.
2. **Leer/verificar:** NO usar caldav. Verificar directamente en la app de iOS/Calendar.app.
3. **Verificación programática:** si necesitas verificar que un evento existe, crearlo y confiar en el UID devuelto. No hay forma confiable de leerlo vía caldav.

### Calendarios disponibles (David Antizar)

| Calendario | ID | Uso |
|-----------|-----|-----|
| Nosotros 🥰 | `8271049C-D351-4E88-A298-13CB3D7C0FE1` | Pareja - NO usar para eventos del agente |
| Oposición | `895E66F3-9569-49E7-A46B-C925378F773B` | Estudio oposición |
| Mastermind Bot | `fcb7cfb7-59ac-44a6-a920-c3b26fa6a1ee` | Eventos automáticos del agente |
| Casa | `home` | Hogar |
| Recordatorios | `tasks` | Tareas |
| Trabajo | `work` | Laboral |

### Historial

- **2026-05-26:** Calendario "Mastermind 🤖" creado, pero caldav no podía leer sus eventos. Borrado y reemplazado por "Mastermind Bot".
- **2026-05-26:** 10 eventos BiciMad creados en "Mastermind Bot" para mañana 27/05.
