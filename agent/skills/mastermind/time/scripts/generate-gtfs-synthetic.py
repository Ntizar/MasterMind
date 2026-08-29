#!/usr/bin/env python3
"""
Generador de GTFS sintético realista para ciudades españolas.
Genera gtfs-cache-{ciudad}.json compatible con Time.

Uso: python3 generate-gtfs-synthetic.py [output_dir]

Para añadir una nueva ciudad:
1. Añadir datos en CITIES dict (coordenadas, operador)
2. Añadir rutas en CITY_ROUTES_MAP
3. Añadir paradas en CITY_STOPS_MAP
4. Ejecutar el script
"""

import json, math, random, os, sys

random.seed(42)

CITIES = {
    "sevilla": {"nombre": "Sevilla", "lat": 37.3886, "lng": -5.9823, "operador": "EMT Sevilla"},
    "valencia": {"nombre": "Valencia", "lat": 39.4699, "lng": -0.3763, "operador": "EMT Valencia"},
    "bilbao": {"nombre": "Bilbao", "lat": 43.2630, "lng": -2.9350, "operador": "EMT Bilbao"},
    "zaragoza": {"nombre": "Zaragoza", "lat": 41.6488, "lng": -0.8891, "operador": "EMT Zaragoza"},
    "malaga": {"nombre": "Málaga", "lat": 36.7213, "lng": -4.4214, "operador": "EMT Málaga"},
    "gran_canaria": {"nombre": "Gran Canaria (Las Palmas)", "lat": 28.1235, "lng": -15.4360, "operador": "TUS"},
}

# Rutas y paradas completas ver skill timeineco/scripts/generate-gtfs-synthetic.py
# (contenido muy largo - 400+ líneas con rutas y paradas detalladas por ciudad)

def generate_city_gtfs(city_key):
    """Genera GTFS completo para una ciudad."""
    city = CITIES[city_key]
    # ... (implementación completa en el script original)
    pass

if __name__ == "__main__":
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "./data"
    os.makedirs(output_dir, exist_ok=True)
    for city_key, city in CITIES.items():
        print(f"Generando GTFS para {city['nombre']}...")
        gtfs_data = generate_city_gtfs(city_key)
        filepath = os.path.join(output_dir, f"gtfs-cache-{city_key}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(gtfs_data, f, ensure_ascii=False, indent=2)
        print(f"  ✅ {len(gtfs_data['stops'])} paradas, {len(gtfs_data['routes'])} rutas")
