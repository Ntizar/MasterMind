#!/usr/bin/env python3
"""Crea eventos diarios de BiciMad (estación 298) en el calendario Mastermind 🤖 de iCloud."""
import caldav
from datetime import datetime, timedelta
import uuid
import os

ICLOUD_USER = "dantizar@gmail.com"
ICLOUD_PASS = os.environ.get("ICLOUD_APP", "jxvr-knqs-hzsx-qcyc")
ICLOUD_URL = "https://caldav.icloud.com"

# Estaciones de BiciMad para la mañana
STATIONS = [
    ("45 5", "07:45", "07:48", "BiciMad 298 - Marques de Viana"),
    ("48 5", "07:48", "07:51", "BiciMad 298 - Marques de Viana"),
    ("51 5", "07:51", "07:54", "BiciMad 298 - Marques de Viana"),
    ("54 5", "07:54", "08:00", "BiciMad 298 - Marques de Viana"),
    ("0 6",  "08:00", "08:03", "BiciMad 298 - Marques de Viana"),
    ("3 6",  "08:03", "08:06", "BiciMad 298 - Marques de Viana"),
    ("6 6",  "08:06", "08:09", "BiciMad 298 - Marques de Viana"),
    ("9 6",  "08:09", "08:12", "BiciMad 298 - Marques de Viana"),
    ("12 6", "08:12", "08:15", "BiciMad 298 - Marques de Viana"),
    ("15 6", "08:15", "08:18", "BiciMad 298 - Marques de Viana"),
]

def main():
    if not ICLOUD_PASS:
        print("ERROR: ICLOUD_APP no está definida en el entorno")
        return

    client = caldav.DAVClient(
        url=ICLOUD_URL,
        username=ICLOUD_USER,
        password=ICLOUD_PASS
    )
    principal = client.principal()
    calendars = principal.calendars()

    # Buscar calendario Mastermind
    cal = None
    for c in calendars:
        name = c.get_display_name()
        if name == "Mastermind":
            cal = c
            print(f"Calendario encontrado: {name}")
            break

    if not cal:
        print("ERROR: Calendario 'Mastermind 🤖' no encontrado")
        print("Calendarios disponibles:", [c.get_display_name() for c in calendars])
        return

    today = datetime.now()
    today_str = today.strftime("%Y%m%d")

    created = 0
    skipped = 0

    for cron_expr, start_hm, end_hm, summary in STATIONS:
        # Parsear hora
        start_parts = start_hm.split(":")
        end_parts = end_hm.split(":")

        start_str = f"{today_str}T{start_hm}00"
        end_str = f"{today_str}T{end_hm}00"

        ical = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Mastermind//ES
BEGIN:VEVENT
DTSTART;TZID=Europe/Madrid:{start_str}
DTEND;TZID=Europe/Madrid:{end_str}
SUMMARY:{summary}
DESCRIPTION:Cron BiciMad ejecutándose cada 3 min\nCron: {cron_expr}
LOCATION:Marques de Viana (Estación 298)
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
UID:{uuid.uuid4()}
END:VEVENT
END:VCALENDAR"""

        # Verificar si ya existe
        events = cal.events()
        exists = False
        for ev in events:
            ev.load()
            data = ev.get_data()
            if summary in data and today_str in data:
                exists = True
                break

        if exists:
            skipped += 1
            print(f"  ⏭️  Saltado (ya existe): {summary} {start_hm}")
        else:
            event = cal.save(ical)
            created += 1
            print(f"  ✅ Creado: {summary} {start_hm}-{end_hm}")

    print(f"\nResumen: {created} creados, {skipped} saltados")

if __name__ == "__main__":
    main()
