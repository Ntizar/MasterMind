---
name: drish-x
---

# DRISH-X

- **URL:** https://github.com/sparkyniner/DRISH-X-Satellite-powered-freight-intelligence-
- **Categoría:** GIS / Inteligencia de tráfico satelital
- **¿Qué hace?:**
DrishX es un sistema de inteligencia de tráfico vehicular automatizado a partir de imágenes satelitales Sentinel-2. Detecta vehículos grandes (camiones, autobuses) en carreteras de cualquier lugar del planeta analizando el "motion smear" espectral — un artefacto físico causado por el sensor Sentinel-2 que captura bandas RGB con 1.01 segundos de diferencia. Los vehículos en movimiento aparecen desplazados entre bandas, creando un patrón azul-verde-rojo que un Random Forest está entrenado para detectar.

- **Casos de uso:**
  - **Inteligencia económica:** Monitorear tráfico de camiones en puertos y corredores comerciales como proxy de actividad económica
  - **Supply chain y logística:** Validar proyecciones de tráfico para nuevos sitios, benchmarkear patrones estacionales
  - **Monitoreo de sanciones:** Detectar cambios en rutas comerciales cuando entran en vigor sanciones o aranceles
  - **Inteligencia de seguridad:** Monitorear cambios en volumen vehicular cerca de instalaciones sensibles, fronteras, bases militares
  - **Respuesta a desastres:** Identificar carreteras operativas vs bloqueadas después de terremotos/inundaciones
  - **Periodismo investigativo:** Verificar afirmaciones sobre corredores comerciales con datos satelitales independientes

- **Snippets/Conceptos clave:**
  - **Física del motion smear:** Sentinel-2 captura B02 (blue) y B04 (red) con ~1.01s de desfase. Un vehículo a 80 km/h se mueve ~22m en ese intervalo. A 10m/pixel, aparece en posiciones diferentes en cada banda.
  - **Pipeline de detección:**
    ```
    1. Feature Stack (7 features por pixel):
       - Variance of RGB, Normalized ratio R/B, Normalized ratio G/B,
       - Mean-centered B04, B03, B02, B08
    2. Random Forest Classification:
       - Cada pixel → background, blue, green, o red
       - Post-process: threshold background confidence > 0.75
    3. Recursive Object Extraction:
       - Start en blue → crecer por green → red
       - Validar: 3 colores presentes, 3-5 pixel extent
       - Score: mean_max_prob + mean_prob > 1.2
    4. Output por detección:
       - Lat/lon, heading, speed estimate, confidence score
    ```
  - **Capacidades:**
    - Detectar vehículos grandes (70-80% en autopistas europeas)
    - Estimación de velocidad (±15 km/h) y dirección (±22.5°)
    - Cobertura global con Sentinel-2 (revisita cada 5 días)
    - Procesar archivos multi-mes en minutos con análisis paralelo
  - **Limitaciones:**
    - No detecta autos (sub-pixel a 10m)
    - No distingue tipos de vehículo
    - No ve a través de nubes (limitación óptica)
    - No es monitoreo en tiempo real (delay + 5 días revisita)
    - Mejor en asfalto oscuro, condiciones despejadas
  - **Requisitos:** Python 3.11, cuenta gratuita Copernicus Data Space, modelo RF entrenado (`rf_model.pickle`)
  - **Variables de entorno:**
    ```bash
    COPERNICUS_CLIENT_ID=...        # OAuth client ID
    COPERNICUS_CLIENT_SECRET=...    # OAuth client secret
    RF_MODEL_PATH=./rf_model.pickle # Modelo Random Forest
    DRISHX_DATA_DIR=./drishx_data   # Directorio de datos
    ```
  - **API Endpoints (FastAPI, puerto 8000):**
    ```
    POST /api/analyze     — Ejecutar detección en un AOI (streaming)
    GET  /api/roads       — Red de carreteras para un bbox
    GET  /api/sites       — Sitios preconfigurados
    GET  /api/feed        — Alertas de detección recientes
    GET  /api/analytics/trends — Series temporales agregadas
    GET  /api/detections/:id — Detecciones de una misión
    ```
  - **Sitios de validación preconfigurados:**
    - Braunschweig A7 (52.25, 10.45, 52.32, 10.55) — Validación research-grade
    - Frankfurt A3 (50.05, 8.55, 50.12, 8.65) — Corredor de alta densidad
    - Karlsruhe A5 (48.95, 8.35, 49.05, 8.45) — Benchmark estándar
  - **Corredores recomendados:** Shahid Rajaee Highway (Irán), Rotterdam A15, Laredo I-35, Mombasa-Nairobi A109

- **Cómo integrarlo en proyectos:**
  1. **Instalación:** Clonar repo, crear venv con Python 3.11, `pip install -r requirements.txt`, `python drishx.py`.
  2. **Configurar Copernicus:** Crear cuenta gratuita en dataspace.copernicus.eu, obtener Client ID/Secret.
  3. **Seleccionar AOI:** Usar la interfaz web (localhost:8000) → Draw AOI → definir región → análisis automático.
  4. **Programático:** Llamar `/api/analyze` con un bbox para análisis desde scripts.
  5. **Integrar con dashboards:** Consumir `/api/analytics/trends` para series temporales de tráfico en paneles.
  6. **Para mayor resolución:** Considerar PlanetScope (3.7m) si necesitas detectar vehículos más pequeños — misma física espectral.
  7. **Modelo RF:** El archivo `rf_model.pickle` debe estar disponible. Si se necesita reentrenar, basarse en Fisser et al. (2022) "Detecting Moving Trucks on Roads Using Sentinel-2 Data".

- **Fecha de aprendizaje:** 2026-05-26
