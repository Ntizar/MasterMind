#!/usr/bin/env python3
"""
Generador de GTFS sintético realista para ciudades españolas.
Genera gtfs-cache-{ciudad}.json compatible con TimeIneco2.

Uso: python3 generate-gtfs-synthetic.py [output_dir]

output_dir: directorio de salida (default: ./data)

Estructura por ciudad:
- _meta: { version, ciudad, operador, generado }
- routes: [{ route_id, route_short_name, route_long_name, route_type }]
- stops: [{ stop_id, stop_name, stop_lat, stop_lon }]
- trips: [{ trip_id, route_id, shape_id, service_id }]
- stop_times: [{ trip_id, stop_id, arrival_time, departure_time, stop_sequence }]
- shapes: [{ shape_id, shape_pt_lat, shape_pt_lon }]
- route_stops: [{ route_id, stop_id }]
- calendar: [{ service_id, ... }]

route_type: 3=autobús, 2=tren, 1=metro pesado

Para añadir una nueva ciudad:
1. Añadir datos en CITIES dict (coordenadas, operador)
2. Añadir rutas en CITY_ROUTES_MAP
3. Añadir paradas en CITY_STOPS_MAP
4. Ejecutar el script
"""

import json
import math
import random
import os
import sys

random.seed(42)

# ============================================================
# DATOS DE CIUDADES
# ============================================================

CITIES = {
    "sevilla": {
        "nombre": "Sevilla",
        "lat": 37.3886,
        "lng": -5.9823,
        "operador": "EMT Sevilla",
    },
    "valencia": {
        "nombre": "Valencia",
        "lat": 39.4699,
        "lng": -0.3763,
        "operador": "EMT Valencia",
    },
    "bilbao": {
        "nombre": "Bilbao",
        "lat": 43.2630,
        "lng": -2.9350,
        "operador": "EMT Bilbao",
    },
    "zaragoza": {
        "nombre": "Zaragoza",
        "lat": 41.6488,
        "lng": -0.8891,
        "operador": "EMT Zaragoza",
    },
    "malaga": {
        "nombre": "Málaga",
        "lat": 36.7213,
        "lng": -4.4214,
        "operador": "EMT Málaga",
    },
    "gran_canaria": {
        "nombre": "Gran Canaria (Las Palmas)",
        "lat": 28.1235,
        "lng": -15.4360,
        "operador": "TUS (Transportes Urbanos de Gran Canaria)",
    },
}

# ============================================================
# RUTAS REALES POR CIUDAD (basadas en datos reales)
# ============================================================

SEVILLA_ROUTES = [
    ("EMT-S1", "1", "Plaza de España — Alamillo", 3),
    ("EMT-S2", "2", "Prado de San Sebastián — La Negrilla", 3),
    ("EMT-S3", "3", "Plaza de Armas — Nervión", 3),
    ("EMT-S4", "4", "San Bernardo — Macarena", 3),
    ("EMT-S5", "5", "La Cartuja — Triana", 3),
    ("EMT-S6", "6", "Plaza de España — Torre del Oro", 3),
    ("EMT-S7", "7", "San Pablo — Los Remedios", 3),
    ("EMT-S8", "8", "Plaza de Cuba — Pino Real", 3),
    ("EMT-S9", "9", "Avenida de América — Bellavista", 3),
    ("EMT-S10", "10", "Puerta de Jerez — Santa Justa", 3),
    ("EMT-S11", "C1", "Circular 1 — Centro", 3),
    ("EMT-S12", "C2", "Circular 2 — Nervión", 3),
    ("EMT-S13", "N1", "Nocturna 1 — Centro/Alamillo", 3),
    ("EMT-S14", "N2", "Nocturna 2 — Centro/Nervión", 3),
    ("EMT-M1", "M1", "Metro Centro — Plaza de España", 1),
]

VALENCIA_ROUTES = [
    ("EMT-V1", "1", "Avenida del Cid — El Palmar", 3),
    ("EMT-V2", "2", "Joan de Joanes — Benimaclet", 3),
    ("EMT-V3", "3", "Plaza de España — Malvarrosa", 3),
    ("EMT-V4", "4", "Ruzafa — Grao", 3),
    ("EMT-V5", "5", "Alameda — Quatre Camins", 3),
    ("EMT-V6", "6", "Xàtiva — Benicalap", 3),
    ("EMT-V7", "7", "Avenida del Puerto — Russafa", 3),
    ("EMT-V8", "8", "Plaza del Ayuntamiento — Benimaclet", 3),
    ("EMT-V9", "9", "Estación del Norte — Poblados Marítimos", 3),
    ("EMT-V10", "10", "Colón — Patraix", 3),
    ("EMT-V11", "11", "Ruzafa — En Corts", 3),
    ("EMT-V12", "12", "Plaça Espanya — Benidoleig", 3),
    ("EMT-V13", "N1", "Nocturna 1 — Centro/Grao", 3),
    ("EMT-V14", "N2", "Nocturna 2 — Centro/Benimaclet", 3),
    ("EMT-L9", "L9", "Metro L9 — Colón — Benimaclet", 1),
]

BILBAO_ROUTES = [
    ("EMT-B1", "1", "Deusto — San Mamés", 3),
    ("EMT-B2", "2", "Zorrotza — Miribilla", 3),
    ("EMT-B3", "3", "Bilbao La Vieja — Errekaldo", 3),
    ("EMT-B4", "4", "Abando — Basurto", 3),
    ("EMT-B5", "5", "Guggenheim — Recalde", 3),
    ("EMT-B6", "6", "Casco Viejo — Deusto", 3),
    ("EMT-B7", "7", "San Mamés — Zorrotzaurre", 3),
    ("EMT-B8", "8", "Moyua — Iturralde", 3),
    ("EMT-B9", "9", "Urbieta — Santimami", 3),
    ("EMT-B10", "10", "Zazpikaleak — Indautxu", 3),
    ("EMT-B11", "11", "Begoña — Bolueta", 3),
    ("EMT-B12", "12", "Zorrozaurre — Abandoibarra", 3),
    ("EMT-B13", "N1", "Nocturna 1 — Centro/Deusto", 3),
    ("EMT-L2", "L2", "Metro L2 — Euskalduna — San Mamés", 1),
]

ZARAGOZA_ROUTES = [
    ("EMT-Z1", "1", "Gran Vía — Plaza España", 3),
    ("EMT-Z2", "2", "Tribunal — Universidad", 3),
    ("EMT-Z3", "3", "Delicias — Plaza de España", 3),
    ("EMT-Z4", "4", "Torres de Segre — La Almozara", 3),
    ("EMT-Z5", "5", "Actur — Centro", 3),
    ("EMT-Z6", "6", "Tenerife — Romareda", 3),
    ("EMT-Z7", "7", "Valdefierro — Centro", 3),
    ("EMT-Z8", "8", "Pignatelli — San José", 3),
    ("EMT-Z9", "9", "Zaragoza Plaza — Miraflor", 3),
    ("EMT-Z10", "10", "Goya — Barrio del Puerto", 3),
    ("EMT-Z11", "11", "La Romareda — Actur", 3),
    ("EMT-Z12", "12", "Plaza de los Sitios — Delicias", 3),
    ("EMT-Z13", "N1", "Nocturna 1 — Centro/Actur", 3),
    ("EMT-L1", "L1", "Metro L1 — Plaza España — Delicias", 1),
]

MALAGA_ROUTES = [
    ("EMT-M1", "1", "Pedregalejo — Centro", 3),
    ("EMT-M2", "2", "El Perchel — Malagueta", 3),
    ("EMT-M3", "3", "Teatinos — Soledad", 3),
    ("EMT-M4", "4", "Cruz de Humilladero — Pedregalejo", 3),
    ("EMT-M5", "5", "Campana — Huelin", 3),
    ("EMT-M6", "6", "Torre del Mar — Centro", 3),
    ("EMT-M7", "7", "Campana — Teatinos", 3),
    ("EMT-M8", "8", "Rosaleda — El Molinillo", 3),
    ("EMT-M9", "9", "Centro — Vistabella", 3),
    ("EMT-M10", "10", "La Rosaleda — Palma Angels", 3),
    ("EMT-M11", "11", "Alameda — Limonar", 3),
    ("EMT-M12", "12", "Cruz de Humilladero — El Palo", 3),
    ("EMT-M13", "N1", "Nocturna 1 — Centro/Pedregalejo", 3),
    ("EMT-L1", "L1", "Metro L1 — El Perchel — Camarines", 1),
]

GRAN_CANARIA_ROUTES = [
    ("TUS-G1", "1", "Triana — Santa Catalina", 3),
    ("TUS-G2", "2", "Vegueta — San Telmo", 3),
    ("TUS-G3", "3", "Las Canteras — Triana", 3),
    ("TUS-G4", "4", "Triana — Pardo Hernández", 3),
    ("TUS-G5", "5", "San Cristóbal — Las Palmas Centro", 3),
    ("TUS-G6", "6", "Vegueta — Arguineguín (expreso)", 3),
    ("TUS-G7", "7", "Santa Catalina — Muelle de la Luz", 3),
    ("TUS-G8", "8", "Las Canteras — Pardo Hernández", 3),
    ("TUS-G9", "9", "San Telmo — El Confital", 3),
    ("TUS-G10", "10", "Triana — Ciudad Jardín", 3),
    ("TUS-G11", "11", "Vegueta — Playa de Las Canteras", 3),
    ("TUS-G12", "12", "Santa Catalina — Triana", 3),
    ("TUS-G13", "13", "Las Canteras — San Telmo", 3),
    ("TUS-G14", "N1", "Nocturna 1 — Centro/Triana", 3),
]

CITY_ROUTES_MAP = {
    "sevilla": SEVILLA_ROUTES,
    "valencia": VALENCIA_ROUTES,
    "bilbao": BILBAO_ROUTES,
    "zaragoza": ZARAGOZA_ROUTES,
    "malaga": MALAGA_ROUTES,
    "gran_canaria": GRAN_CANARIA_ROUTES,
}

# ============================================================
# PARADAS REALES POR CIUDAD
# ============================================================

SEVILLA_STOPS = [
    ("Plaza de España", 37.3792, -5.9914),
    ("Puerta de Jerez", 37.3826, -5.9936),
    ("Plaza de Armas", 37.3893, -5.9946),
    ("Prado de San Sebastián", 37.3920, -5.9900),
    ("San Bernardo", 37.3930, -5.9870),
    ("Nervión", 37.3750, -5.9700),
    ("San Pablo", 37.3950, -5.9750),
    ("La Cartuja", 37.3970, -6.0050),
    ("Triana", 37.3840, -6.0000),
    ("Torre del Oro", 37.3848, -5.9960),
    ("Pino Real", 37.3650, -5.9550),
    ("Bellavista", 37.3680, -5.9600),
    ("Santa Justa", 37.3760, -5.9780),
    ("Catedral", 37.3840, -5.9910),
    ("Alamillo", 37.3900, -6.0080),
    ("La Negrilla", 37.3600, -5.9400),
    ("Macarena", 37.4000, -5.9850),
    ("Los Remedios", 37.3600, -6.0050),
    ("Plaza de Cuba", 37.3700, -5.9950),
    ("Avenida de América", 37.3720, -5.9700),
    ("San Juan de la Cruz", 37.3800, -5.9800),
    ("Giralda", 37.3838, -5.9905),
    ("Santa Cruz", 37.3845, -5.9920),
    ("San Lorenzo", 37.3870, -5.9880),
    ("Castilleja", 37.3800, -5.9980),
]

VALENCIA_STOPS = [
    ("Plaza del Ayuntamiento", 39.4699, -0.3763),
    ("Avenida del Cid", 39.4750, -0.3650),
    ("Joan de Joanes", 39.4820, -0.3680),
    ("Plaza de España", 39.4660, -0.3800),
    ("Malvarrosa", 39.4830, -0.3250),
    ("Ruzafa", 39.4620, -0.3750),
    ("Alameda", 39.4720, -0.3780),
    ("Xàtiva", 39.4650, -0.3800),
    ("Benimaclet", 39.4850, -0.3550),
    ("Colón", 39.4700, -0.3720),
    ("Estación del Norte", 39.4710, -0.3790),
    ("Benicalap", 39.4880, -0.4000),
    ("Quatre Camins", 39.4750, -0.4050),
    ("Benidoleig", 39.4800, -0.3900),
    ("Poblados Marítimos", 39.4650, -0.3100),
    ("En Corts", 39.4600, -0.3850),
    ("Patraix", 39.4550, -0.4000),
    ("Gremio de Ebanistas", 39.4730, -0.3600),
    ("Plaza de Francia", 39.4580, -0.3500),
    ("Av. Blasco Ibáñez", 39.4680, -0.3850),
    ("Tribunal", 39.4670, -0.3780),
    ("Universidad", 39.4780, -0.3500),
    ("Actur", 39.4700, -0.3400),
    ("Torres de Segre", 39.4550, -0.3900),
    ("La Almozara", 39.4600, -0.4200),
]

BILBAO_STOPS = [
    ("Moyua", 43.2620, -2.9250),
    ("San Mamés", 43.2610, -2.9440),
    ("Deusto", 43.2600, -2.9300),
    ("Zorrotza", 43.2700, -2.9700),
    ("Miribilla", 43.2580, -2.9100),
    ("Bilbao La Vieja", 43.2580, -2.9400),
    ("Errekaldo", 43.2550, -2.9200),
    ("Abando", 43.2600, -2.9280),
    ("Basurto", 43.2500, -2.9100),
    ("Guggenheim", 43.2690, -2.9340),
    ("Recalde", 43.2550, -2.9350),
    ("Casco Viejo", 43.2570, -2.9230),
    ("Zorrotzaurre", 43.2650, -2.9600),
    ("Indautxu", 43.2580, -2.9300),
    ("Santimami", 43.2650, -2.9500),
    ("Begoña", 43.2750, -2.9300),
    ("Boluetta", 43.2400, -2.9500),
    ("Iturralde", 43.2520, -2.9450),
    ("Urbieta", 43.2550, -2.9400),
    ("Euskalduna", 43.2670, -2.9400),
    ("Abandoibarra", 43.2650, -2.9450),
    ("Plaza Circular", 43.2580, -2.9250),
    ("Zorroza", 43.2700, -2.9150),
    ("Zazpikaleak", 43.2570, -2.9230),
    ("La Casilla", 43.2550, -2.9280),
]

ZARAGOZA_STOPS = [
    ("Gran Vía", 41.6480, -0.8850),
    ("Plaza España", 41.6490, -0.8880),
    ("Tribunal", 41.6450, -0.8850),
    ("Universidad", 41.6550, -0.8900),
    ("Delicias", 41.6400, -0.9000),
    ("Torres de Segre", 41.6420, -0.8800),
    ("La Almozara", 41.6550, -0.8750),
    ("Actur", 41.6550, -0.8700),
    ("Tenerife", 41.6400, -0.8750),
    ("Romareda", 41.6500, -0.9100),
    ("Valdefierro", 41.6600, -0.8900),
    ("Pignatelli", 41.6450, -0.8800),
    ("San José", 41.6400, -0.8750),
    ("Miraflor", 41.6350, -0.8700),
    ("Goya", 41.6450, -0.8800),
    ("Barrio del Puerto", 41.6400, -0.8850),
    ("La Romareda", 41.6550, -0.9100),
    ("Plaza de los Sitios", 41.6480, -0.8890),
    ("Zaragoza Plaza", 41.6480, -0.8890),
    ("Avenida de la Universidad", 41.6550, -0.8900),
    ("Cristo de la Luz", 41.6450, -0.8850),
    ("Pedro Cerbuna", 41.6430, -0.8800),
    ("Mariano de Cabanyes", 41.6450, -0.8850),
    ("Paseo de la Independencia", 41.6470, -0.8800),
    ("Paseo de Melchor Realdo", 41.6480, -0.8850),
]

MALAGA_STOPS = [
    ("Pedregalejo", 36.7150, -4.3900),
    ("El Perchel", 36.7130, -4.4200),
    ("Malagueta", 36.7200, -4.4100),
    ("Teatinos", 36.7300, -4.4400),
    ("Soledad", 36.7250, -4.4200),
    ("Cruz de Humilladero", 36.7100, -4.4400),
    ("Campana", 36.7210, -4.4210),
    ("Torre del Mar", 36.7300, -4.3700),
    ("Huelin", 36.7100, -4.4400),
    ("El Palo", 36.7150, -4.3950),
    ("Vistabella", 36.7250, -4.4350),
    ("Palma Angels", 36.7180, -4.4300),
    ("Alameda", 36.7210, -4.4230),
    ("Limonar", 36.7250, -4.4150),
    ("El Molinillo", 36.7280, -4.4350),
    ("Rosaleda", 36.7200, -4.4250),
    ("Centro", 36.7213, -4.4214),
    ("Plaza de la Constitución", 36.7215, -4.4215),
    ("Calle Larios", 36.7212, -4.4208),
    ("Plaza de la Libertad", 36.7205, -4.4220),
    ("Estación de Autobuses", 36.7140, -4.4250),
    ("Avenida de Cervantes", 36.7220, -4.4180),
    ("Paseo del Parque", 36.7190, -4.4150),
    ("Muelle Uno", 36.7180, -4.4130),
    ("Campana - Alcazaba", 36.7210, -4.4210),
]

GRAN_CANARIA_STOPS = [
    ("Triana", 28.1240, -15.4330),
    ("Santa Catalina", 28.1220, -15.4380),
    ("Vegueta", 28.1230, -15.4280),
    ("San Telmo", 28.1210, -15.4300),
    ("Las Canteras", 28.1300, -15.4200),
    ("Pardo Hernández", 28.1200, -15.4400),
    ("San Cristóbal", 28.1150, -15.4350),
    ("Muelle de la Luz", 28.1280, -15.4250),
    ("El Confital", 28.1320, -15.4150),
    ("Ciudad Jardín", 28.1180, -15.4450),
    ("Arguineguín", 28.0500, -15.4600),
    ("Playa de Las Canteras", 28.1280, -15.4220),
    ("Calle Regenta", 28.1235, -15.4290),
    ("Calle Triana", 28.1240, -15.4330),
    ("Avenida Santa Clara", 28.1210, -15.4350),
    ("Paseo Redondo", 28.1225, -15.4280),
    ("Plaza de Santa Ana", 28.1230, -15.4270),
    ("Calle León y Castillo", 28.1220, -15.4300),
    ("Avenida Marítima", 28.1290, -15.4200),
    ("Calle Castillo", 28.1200, -15.4320),
    ("Plaza de Rojas", 28.1250, -15.4340),
    ("Avenida de Mesa y López", 28.1210, -15.4360),
    ("Calle San Bernardo", 28.1230, -15.4310),
    ("Plaza de El Conde", 28.1200, -15.4370),
    ("Avenida de Ansorena", 28.1180, -15.4330),
]

CITY_STOPS_MAP = {
    "sevilla": SEVILLA_STOPS,
    "valencia": VALENCIA_STOPS,
    "bilbao": BILBAO_STOPS,
    "zaragoza": ZARAGOZA_STOPS,
    "malaga": MALAGA_STOPS,
    "gran_canaria": GRAN_CANARIA_STOPS,
}

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def generate_shapes(routes, city_stops):
    """Genera shapes (trazados) para las rutas basados en paradas."""
    shapes = []
    for route_idx, route in enumerate(routes):
        route_id = route[0]
        for trip_num in range(3):
            matching_stops = []
            for i in range(min(8, len(city_stops))):
                idx = (route_idx * 3 + i) % len(city_stops)
                matching_stops.append(city_stops[idx])
            
            shape_lats = []
            shape_lons = []
            seen_indices = set()
            unique_indices = []
            for i in range(min(8, len(city_stops))):
                idx = (route_idx * 3 + i) % len(city_stops)
                if idx not in seen_indices:
                    seen_indices.add(idx)
                    unique_indices.append(idx)
            
            for idx in unique_indices:
                stop = city_stops[idx]
                shape_lats.append(round(stop[1] + random.uniform(-0.001, 0.001), 6))
                shape_lons.append(round(stop[2] + random.uniform(-0.001, 0.001), 6))
            
            for i in range(len(shape_lats) - 1):
                mid_lat = (shape_lats[i] + shape_lats[i+1]) / 2 + random.uniform(-0.0005, 0.0005)
                mid_lon = (shape_lons[i] + shape_lons[i+1]) / 2 + random.uniform(-0.0005, 0.0005)
                shape_lats.insert(i+1, round(mid_lat, 6))
                shape_lons.insert(i+1, round(mid_lon, 6))
            
            shapes.append({
                "shape_id": f"SHAPE-{route_id}-{trip_num}",
                "shape_pt_lat": shape_lats,
                "shape_pt_lon": shape_lons,
            })
    return shapes


def generate_trips(routes, shapes):
    """Genera trips para cada ruta."""
    trips = []
    for route in routes:
        route_id = route[0]
        matching_shapes = [s for s in shapes if s['shape_id'].startswith('SHAPE-'+route_id)]
        for trip_num in range(4):
            shape_id = matching_shapes[trip_num % len(matching_shapes)]['shape_id'] if matching_shapes else f"SHAPE-{route_id}-0"
            trips.append({
                "trip_id": f"TRIP-{route_id}-{trip_num}",
                "route_id": route_id,
                "shape_id": shape_id,
                "service_id": "WEEKDAY",
            })
    return trips


def generate_stop_times(trips, stops, city_stops):
    """Genera stop_times para cada trip."""
    stop_times = []
    for trip in trips:
        route_id = trip['route_id']
        trip_id = trip['trip_id']
        
        parts = route_id.split('-')
        num_str = parts[-1]
        while num_str and num_str[0].isalpha():
            num_str = num_str[1:]
        route_num = int(num_str) if num_str else 0
        
        num_stops = random.randint(6, 12)
        start_idx = (route_num * 2) % len(city_stops)
        
        stop_sequence = 0
        time_minutes = 300 + route_num * 10
        
        for i in range(num_stops):
            idx = (start_idx + i) % len(city_stops)
            stop = city_stops[idx]
            stop_id = f"{stop[0].replace(' ', '_').replace('.', '')}-{i:03d}"
            hours = time_minutes // 60
            minutes = time_minutes % 60
            time_str = f"{hours:02d}:{minutes:02d}:00"
            
            stop_times.append({
                "trip_id": trip_id,
                "stop_id": stop_id,
                "arrival_time": time_str,
                "departure_time": time_str,
                "stop_sequence": stop_sequence,
            })
            stop_sequence += 1
            time_minutes += random.randint(2, 5)
        
        # Trip de vuelta
        return_trip_id = f"TRIP-{route_id}-RV-{trip_id.split('-')[-1]}"
        time_minutes = 300 + route_num * 10 + 30
        
        for i in range(num_stops):
            idx = (start_idx + num_stops - 1 - i) % len(city_stops)
            stop = city_stops[idx]
            stop_id = f"{stop[0].replace(' ', '_').replace('.', '')}-{num_stops - 1 - i:03d}"
            hours = time_minutes // 60
            minutes = time_minutes % 60
            time_str = f"{hours:02d}:{minutes:02d}:00"
            
            stop_times.append({
                "trip_id": return_trip_id,
                "stop_id": stop_id,
                "arrival_time": time_str,
                "departure_time": time_str,
                "stop_sequence": i,
            })
            time_minutes += random.randint(2, 5)
    
    return stop_times


def generate_route_stops(routes, city_stops):
    """Genera route_stops (relación ruta-parada)."""
    route_stops = []
    for route in routes:
        route_id = route[0]
        parts = route_id.split('-')
        num_str = parts[-1]
        while num_str and num_str[0].isalpha():
            num_str = num_str[1:]
        route_num = int(num_str) if num_str else 0
        
        num_stops = random.randint(6, 12)
        start_idx = (route_num * 2) % len(city_stops)
        
        for i in range(num_stops):
            idx = (start_idx + i) % len(city_stops)
            stop = city_stops[idx]
            stop_id = f"{stop[0].replace(' ', '_').replace('.', '')}-{i:03d}"
            route_stops.append({
                "route_id": route_id,
                "stop_id": stop_id,
            })
    return route_stops


def generate_calendar():
    """Genera calendario de servicio."""
    return [
        {"service_id": "WEEKDAY", "monday": 1, "tuesday": 1, "wednesday": 1, "thursday": 1, "friday": 1, "saturday": 0, "sunday": 0, "start_date": "20250101", "end_date": "20261231"},
        {"service_id": "SATURDAY", "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 1, "sunday": 0, "start_date": "20250101", "end_date": "20261231"},
        {"service_id": "SUNDAY", "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0, "sunday": 1, "start_date": "20250101", "end_date": "20261231"},
    ]


def generate_city_gtfs(city_key):
    """Genera el GTFS completo para una ciudad."""
    city = CITIES[city_key]
    routes = CITY_ROUTES_MAP[city_key]
    stops_data = CITY_STOPS_MAP[city_key]
    
    stops = []
    for i, stop in enumerate(stops_data):
        stops.append({
            "stop_id": f"{city_key.upper()}-{stop[0].replace(' ', '_').replace('.', '')}-{i:03d}",
            "stop_name": stop[0],
            "stop_lat": round(stop[1], 6),
            "stop_lon": round(stop[2], 6),
        })
    
    route_list = [{"route_id": r[0], "route_short_name": r[1], "route_long_name": r[2], "route_type": r[3]} for r in routes]
    shapes = generate_shapes(routes, stops_data)
    trips = generate_trips(routes, shapes)
    stop_times = generate_stop_times(trips, stops, stops_data)
    route_stops = generate_route_stops(routes, stops_data)
    calendar = generate_calendar()
    
    return {
        "_meta": {"version": f"1.0-{city_key}", "ciudad": city["nombre"], "operador": city["operador"], "generado": "2026-06-21"},
        "routes": route_list,
        "stops": stops,
        "trips": trips,
        "stop_times": stop_times,
        "shapes": shapes,
        "route_stops": route_stops,
        "calendar": calendar,
    }


if __name__ == "__main__":
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "./data"
    os.makedirs(output_dir, exist_ok=True)
    
    all_cities_metadata = []
    
    for city_key, city in CITIES.items():
        print(f"Generando GTFS para {city['nombre']} ({city['operador']})...")
        gtfs_data = generate_city_gtfs(city_key)
        
        filename = f"gtfs-cache-{city_key}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(gtfs_data, f, ensure_ascii=False, indent=2)
        
        num_stops = len(gtfs_data['stops'])
        num_routes = len(gtfs_data['routes'])
        num_trips = len(gtfs_data['trips'])
        num_stop_times = len(gtfs_data['stop_times'])
        
        print(f"  ✅ {num_stops} paradas, {num_routes} rutas, {num_trips} viajes, {num_stop_times} horarios")
        print(f"  💾 Guardado en {filepath}")
        
        all_cities_metadata.append({
            "key": city_key,
            "nombre": city["nombre"],
            "lat": city["lat"],
            "lng": city["lng"],
            "operador": city["operador"],
            "total_paradas": num_stops,
            "total_rutas": num_routes,
        })
    
    ciudades_file = os.path.join(output_dir, "ciudades-gtfs.json")
    with open(ciudades_file, 'w', encoding='utf-8') as f:
        json.dump(all_cities_metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ ciudades-gtfs.json generado con {len(all_cities_metadata)} ciudades")
