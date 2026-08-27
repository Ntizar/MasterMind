---
name: street-complete
description: StreetComplete — editor de OpenStreetMap para Android fácil de usar. Añadir datos al mapa respondiendo preguntas.
---

# StreetComplete — Editor OSM para Android

## Qué hace

[StreetComplete](https://github.com/streetcomplete/StreetComplete) es un editor de OpenStreetMap para Android que permite contribuir al mapa respondiendo preguntas simples. Ideal para proyectos que necesitan enriquecer datos OSM con información local (nombres de calles, tipos de acera, accesibilidad, etc.).

## Instalación

```bash
# APK desde F-Droid (recomendado)
# https://f-droid.org/packages/de.blau.android/

# O desde GitHub Releases
curl -LO https://github.com/streetcomplete/StreetComplete/releases/latest/download/StreetComplete-*-app-release.apk

# Para desarrollo
git clone https://github.com/streetcomplete/StreetComplete.git
cd StreetComplete
./gradlew assembleDebug
```

## Uso

```
# En el dispositivo Android:
# 1. Instalar StreetComplete
# 2. Abrir y navegar a un área
# 3. Las preguntas aparecen como pins en el mapa
# 4. Responder preguntas para contribuir a OSM

# Ejemplos de preguntas:
# - ¿Esta calle tiene acera?
# - ¿Cuál es el límite de velocidad aquí?
# - ¿Este bus stop tiene refugio?
# - ¿Esta vía es de un solo sentido?
```

## Integración con proyectos de datos

```python
# Ejemplo: descargar datos OSM enriquecidos por StreetComplete
# Usar Overpass API para extraer datos actualizados
import requests

query = """
[out:json];
area["name"="Madrid"]->.searchArea;
(
  node["highway"="stop"](area.searchArea);
  way["highway"="stop"](area.searchArea);
);
out body;
>;
out skel qt;
"""

response = requests.post(
    'https://overpass-api.de/api/interpreter',
    data={'data': query}
)
data = response.json()
```

## Pitfalls

- Solo funciona en Android (no iOS)
- Los datos enriquecidos están en OSM — usar Overpass API para extraerlos
- No es un editor completo — solo para preguntas específicas
- La cobertura depende de la actividad de la comunidad local

## Referencias

- Repo: https://github.com/streetcomplete/StreetComplete
- Relacionado: `osm-infrastructure-mapping`, `visir-hermes-fomento`, `catastro-api`