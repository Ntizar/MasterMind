#!/usr/bin/env python3
"""
Script para geocodificar estaciones de informes CIAF con Nominatim.
Actualiza archivos .md con coordenadas reales.

Uso:
  python3 geo-fix.py <archivo.md> [<lat> <lng>]
  python3 geo-fix.py --batch <database/estaciones.json>
  python3 geo-fix.py --all <directorio_informes>

La geocodificación usa Nominatim con URL encoding correcto.
"""
import sys
import os
import re
import json
import subprocess
from urllib.parse import quote

def geocode(station, province=None):
    """Geocodificar estación con Nominatim y URL encoding."""
    if station in ('Desconocida', 'Desconocido', ''):
        return None, None
    
    query = f"{station} {province or ''} Spain"
    encoded = quote(query)
    url = f'https://nominatim.openstreetmap.org/search?format=json&q={encoded}&limit=1'
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', url, '-H', 'User-Agent: CIAF-Data/1.0'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return None, None

def update_file(filepath, lat, lng):
    """Actualizar coordenadas en un archivo .md."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Actualizar coordenadas en bloque ubicacion
    content = re.sub(
        r'(\s+coordenadas:\s*)\[null,\s*null\]',
        rf'\1[{lat}, {lng}]',
        content
    )
    # Actualizar geolocalizacion.lat
    content = re.sub(
        r'(^\s+lat:\s*)(?:null|\d+\.\d+)',
        rf'\1{lat}',
        content,
        flags=re.MULTILINE
    )
    # Actualizar geolocalizacion.lng
    content = re.sub(
        r'(^\s+lng:\s*)(?:null|\d+\.\d+)',
        rf'\1{lng}',
        content,
        flags=re.MULTILINE
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python3 geo-fix.py <archivo.md> [<lat> <lng>]")
        print("     python3 geo-fix.py --batch <estaciones.json>")
        print("     python3 geo-fix.py --all <directorio>")
        sys.exit(1)
    
    if sys.argv[1] == '--batch' and len(sys.argv) >= 3:
        # Modo batch: leer estaciones.json
        with open(sys.argv[2], 'r') as f:
            stations = json.load(f)
        
        for station, coords in stations.items():
            if station == 'Desconocida':
                continue
            lat, lng = geocode(station)
            if lat:
                print(f"✅ {station}: {lat}, {lng}")
            else:
                print(f"❌ {station}: no encontrado")
    
    elif sys.argv[1] == '--all' and len(sys.argv) >= 3:
        # Modo all: procesar todos los .md de un directorio
        dirpath = sys.argv[2]
        for year_dir in os.listdir(dirpath):
            year_path = os.path.join(dirpath, year_dir)
            if not os.path.isdir(year_path):
                continue
            for md_file in os.listdir(year_path):
                if not md_file.endswith('.md'):
                    continue
                filepath = os.path.join(year_path, md_file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read(2000)
                
                est_match = re.search(r'estacion:\s*"([^"]+)"', content)
                if est_match:
                    station = est_match.group(1)
                    lat, lng = geocode(station)
                    if lat:
                        update_file(filepath, lat, lng)
                        print(f"✅ {md_file}: {lat}, {lng}")
    
    elif len(sys.argv) >= 3:
        # Modo single: actualizar un archivo con coordenadas dadas
        filepath = sys.argv[1]
        lat, lng = float(sys.argv[2]), float(sys.argv[3])
        update_file(filepath, lat, lng)
        print(f"✅ {filepath}: {lat}, {lng}")
