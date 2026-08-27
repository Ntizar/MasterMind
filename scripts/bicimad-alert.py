#!/usr/bin/env python3
"""BiciMad morning alert - checks station 2002 (display 298) and prints formatted message.
Hermes will deliver the output to Telegram automatically."""

import json
import urllib.request
from datetime import datetime, timezone, timedelta

STATION_ID = "2002"  # Station display ID 298 (Marques de Viana - Bellver)

def get_madrid_offset():
    """Get current Madrid timezone offset."""
    now = datetime.now(timezone.utc)
    month = now.month
    if 3 <= month <= 10:
        return timedelta(hours=2)  # CEST
    return timedelta(hours=1)  # CET

def fetch_bicimad():
    """Fetch real-time data for station from Bicimad GBFS API."""
    # Get station info (includes capacity and name)
    url = "https://madrid.publicbikesystem.net/customer/gbfs/v2/en/station_information"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "BiciMad-Alert/1.0")
    
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode())
    
    # Get capacity from station info
    info_stations = data.get("data", {}).get("stations", [])
    capacity = 0
    name = "Unknown"
    for s in info_stations:
        if str(s.get("station_id")) == STATION_ID:
            capacity = s.get("capacity", 0)
            name = s.get("name", "Unknown")
            break
    
    # Get station status
    url = "https://madrid.publicbikesystem.net/customer/gbfs/v2/en/station_status"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "BiciMad-Alert/1.0")
    
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode())
    
    # Find station
    for station in data.get("data", {}).get("stations", []):
        if str(station.get("station_id")) == STATION_ID:
            return {
                "name": name,
                "bikes": station.get("num_bikes_available", 0),
                "docks": station.get("num_docks_available", 0),
                "total": capacity,
            }
    return None

def format_message(station):
    """Format a clean, emoji-rich message."""
    name = station["name"]
    bikes = station["bikes"]
    docks = station["docks"]
    total = station["total"]
    
    # Calculate fill percentage
    fill_pct = int((bikes / total) * 100) if total > 0 else 0
    
    # Fill level indicator
    if fill_pct < 20:
        fill_emoji = "🔵"
        fill_text = "Vacío"
    elif fill_pct < 40:
        fill_emoji = "🟡"
        fill_text = "Bajo"
    elif fill_pct < 60:
        fill_emoji = "🟠"
        fill_text = "Medio"
    elif fill_pct < 80:
        fill_emoji = "🟠"
        fill_text = "Alto"
    else:
        fill_emoji = "🔴"
        fill_text = "Lleno"
    
    # Bike availability
    if bikes == 0:
        bike_status = "❌ Sin bicis"
    elif bikes <= 3:
        bike_status = f"🚲 Solo {bikes} bici{'s' if bikes > 1 else ''}"
    elif bikes <= 8:
        bike_status = f"🚲 {bikes} bicis"
    else:
        bike_status = f"🚲 {bikes} bicis ✅"
    
    # Dock availability
    if docks == 0:
        dock_status = "❌ Sin plazas"
    elif docks <= 3:
        dock_status = f"🔌 Solo {docks} plazas"
    else:
        dock_status = f"🔌 {docks} plazas"
    
    # Time in Madrid
    madrid_offset = get_madrid_offset()
    madrid_now = datetime.now(timezone.utc) + madrid_offset
    time_str = madrid_now.strftime("%H:%M")
    
    # Return plain text (Telegram will auto-format)
    return (
        f"🚲 *BiciMad — Estación 298*\n"
        f"📍 {name}\n"
        f"📊 {bike_status} | {dock_status}\n"
        f"{fill_emoji} Relleno: {fill_pct}% ({fill_text})\n"
        f"🕐 {time_str} (Madrid)"
    )

if __name__ == "__main__":
    station = fetch_bicimad()
    if not station:
        print("❌ ERROR: Station 298 not found in Bicimad API")
        exit(1)
    
    message = format_message(station)
    print(message)
