#!/usr/bin/env python3
"""BiciMad multi-station alert - checks multiple stations and prints formatted message.
Hermes will deliver the output to Telegram automatically."""

import json
import urllib.request
from datetime import datetime, timezone, timedelta

# Station IDs (internal GBFS IDs)
STATIONS = [
    {"id": "2002", "label": "Bellver - Mq. de Viana"},   # display 298
    {"id": "1612", "label": "Metro Tetuán"},             # display 206
    {"id": "1540", "label": "María de Guzmán"},          # display 134
]

GBFS_URLS = {
    "info": "https://madrid.publicbikesystem.net/customer/gbfs/v2/en/station_information",
    "status": "https://madrid.publicbikesystem.net/customer/gbfs/v2/en/station_status",
}

def get_madrid_offset():
    now = datetime.now(timezone.utc)
    month = now.month
    if 3 <= month <= 10:
        return timedelta(hours=2)  # CEST
    return timedelta(hours=1)  # CET

def fetch_gbfs(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "BiciMad-Alert/1.0")
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode())

def format_station(station_name, bikes, docks, total):
    fill_pct = int((bikes / total) * 100) if total > 0 else 0
    
    if fill_pct < 20:
        fill_emoji, fill_text = "🔵", "Vacío"
    elif fill_pct < 40:
        fill_emoji, fill_text = "🟡", "Bajo"
    elif fill_pct < 60:
        fill_emoji, fill_text = "🟠", "Medio"
    elif fill_pct < 80:
        fill_emoji, fill_text = "🟠", "Alto"
    else:
        fill_emoji, fill_text = "🔴", "Lleno"
    
    if bikes == 0:
        bike_status = "❌ Sin bicis"
    elif bikes <= 3:
        bike_status = f"🚲 Solo {bikes} bici{'s' if bikes > 1 else ''}"
    else:
        bike_status = f"🚲 {bikes} bicis ✅"
    
    if docks == 0:
        dock_status = "❌ Sin plazas"
    elif docks <= 3:
        dock_status = f"🔌 Solo {docks} plazas"
    else:
        dock_status = f"🔌 {docks} plazas"
    
    return (
        f"{fill_emoji} *{station_name}*\n"
        f"  {bike_status} | {dock_status}\n"
        f"  Relleno: {fill_pct}% ({fill_text})"
    )

if __name__ == "__main__":
    madrid_offset = get_madrid_offset()
    madrid_now = datetime.now(timezone.utc) + madrid_offset
    time_str = madrid_now.strftime("%H:%M")
    
    # Fetch all GBFS data once
    info_data = fetch_gbfs(GBFS_URLS["info"])
    status_data = fetch_gbfs(GBFS_URLS["status"])
    
    # Build station info lookup
    info_map = {}
    for s in info_data.get("data", {}).get("stations", []):
        info_map[str(s["station_id"])] = s
    
    # Build station status lookup
    status_map = {}
    for s in status_data.get("data", {}).get("stations", []):
        status_map[str(s["station_id"])] = s
    
    results = []
    errors = []
    
    for station in STATIONS:
        sid = station["id"]
        info = info_map.get(sid, {})
        status = status_map.get(sid, {})
        
        name = info.get("name", station["label"])
        capacity = info.get("capacity", 0)
        bikes = status.get("num_bikes_available", None)
        docks = status.get("num_docks_available", None)
        
        if bikes is None or docks is None:
            errors.append(f"❌ {station['label']} no encontrada")
            continue
        
        results.append(format_station(name, bikes, docks, capacity))
    
    # Build output
    lines = [f"🚲 *BiciMad — Resumen* 🕐 {time_str} (Madrid)\n"]
    
    if errors:
        lines.extend(errors)
        lines.append("")
    
    if results:
        lines.append("📊 *Paradas:*\n")
        lines.append("\n".join(results))
    else:
        lines.append("❌ No se pudieron consultar las paradas")
    
    print("\n".join(lines))
