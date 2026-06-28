---
name: satellite-traffic-detection
description: "DRISH-X/DRISH-ES — detección de tráfico de vehículos desde imágenes satelitales Sentinel-2. RGB offset 1.01s + Random Forest. Fork español en Ntizar/drish-es con autopistas españolas"
version: 1.0.0
author: Ntizar
tags: [vision, satellite, traffic, DRISH-X]

---

# DRISH-X — Satellite-Powered Freight Intelligence

## Descripción

Inteligencia automatizada de tráfico de vehículos desde imágenes satelitales Sentinel-2. Responde: "¿cuánto tráfico hay en esta carretera y cómo ha cambiado con el tiempo?"

## Repos

### Original (inglés)
- **Repo**: sparkyniner/DRISH-X-Satellite-powered-freight-intelligence- (233★)
- **URL**: https://github.com/sparkyniner/DRISH-X-Satellite-powered-freight-intelligence-
- **License**: MIT
- **Autor**: Sairaj Balaji
- **Sites preset**: Autopistas alemanas (A7 Braunschweig, A3 Frankfurt, A5 Karlsruhe)

### Fork español — DRISH-ES
- **Repo**: Ntizar/drish-es (público)
- **URL**: https://github.com/Ntizar/drish-es
- **Autor**: David Antizar (adaptación española)
- **Diferencias con el original**:
  - UI 100% traducida al español (HTML, JS, Python logs)
  - 8 sites predefinidos de autopistas españolas (M-30, A-1, A-2, A-4, A-5, A-6, AP-7, A-7)
  - Centro por defecto: Madrid (40.45, -3.69)
  - README completo en castellano
  - Motor de detección idéntico (mismo RF pickle, mismo pipeline)
- **Referencia de targets**: `references/spanish-motorway-targets.md`

## Tecnologías

- Python 3.11 (recomendado)
- FastAPI + uvicorn (API server)
- Sentinel-2 L2A / Copernicus Data Space (imágenes satelitales)
- scikit-learn Random Forest (clasificación, NO YOLO)
- OSMnx + Overpass API (red de carreteras)
- SentinelHub SDK (descarga de imágenes)
- Leaflet + Chart.js (frontend)

## Principio Científico

El sensor Sentinel-2 registra los canales rojo (B04), verde (B03) y azul (B02) con un desfase de **1.01 segundos**. Un vehículo a 80 km/h se desplaza ~22m en ese intervalo. A 10m/píxel, aparece en posiciones diferentes por canal → firma espectral "azul-verde-roja" de 3-5 píxeles.

## Arquitectura del Pipeline (código real)

```
Sentinel-2 L2A (10m, revisita 5 días)
  │
  ├─ Evalscript: B04(R), B03(G), B02(B), B08(NIR), CLM → array (H,W,5)
  │
  ├─ build_feature_stack() → 7 features por píxel:
  │   [0] varianza(R,G,B)
  │   [1] ratio_normalizado(R,B)
  │   [2] ratio_normalizado(G,B)
  │   [3] B04 - mean(B04)
  │   [4] B03 - mean(B03)
  │   [5] B02 - mean(B02)
  │   [6] B08 - mean(B08)
  │
  ├─ Clasificación: RandomForestClassifier (rf_model.pickle)
  │   → 4 clases: fondo, azul, verde, rojo
  │   → Post-proceso: suprimir fondo con prob < 0.75
  │   → Fallback: proxy_classify() si no hay modelo RF
  │
  ├─ ObjectExtractor (recursivo):
  │   Semilla: píxeles azules (clase 2)
  │   Crecimiento: azul → verde → rojo
  │   Validación: 3 colores presentes, 3-5 píxeles, score > 1.2
  │
  └─ Salida: lat, lon, rumbo, velocidad (~±15 km/h), confianza
```

## API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/analyze` | Análisis de zona (streaming NDJSON) |
| GET | `/api/roads` | Red de carreteras por bbox |
| GET | `/api/sites` | Sites predefinidos + historial |
| GET | `/api/feed` | Alertas de detección recientes |
| GET | `/api/analytics/trends` | Series temporales diarias |
| GET | `/api/detections/:id` | Detecciones de una misión |
| POST | `/api/auth` | Credenciales Copernicus (runtime) |

## Despliegue en NaN Builders (Python/FastAPI)

Dockerfile patrón para DRISH-ES en NaN:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PORT=4000

COPY DrishX/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY DrishX/ ./
RUN mkdir -p drishx_data/sentinel_data/detections drishx_data/osm_cache drishx_data/sh_cache

RUN groupadd -S appgroup && useradd -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:4000/api/sites')" || exit 1

EXPOSE 4000
CMD ["python", "drishx.py"]
```

**Pitfall NaN + .env:** El `.env` está en `.gitignore` → NO llega al repo → NO está en el contenedor NaN. Las credenciales Copernicus se configuran como **variables de entorno en el dashboard de NaN** (pestaña Env), no vía .env. El código lee `os.getenv("COPERNICUS_CLIENT_ID")` directamente.

**Puerto:** El `uvicorn.run()` debe usar `int(os.getenv("PORT", 4000))` para ser flexible entre local (4000) y NaN (PORT inyectado).

## Casos de Uso

- **Freight intelligence**: conteo y seguimiento de camiones en autopistas
- **Traffic analysis**: patrones de tráfico temporal
- **Infrastructure planning**: datos para planificación de infraestructura
- **Environmental monitoring**: impacto del tráfico en zonas sensibles

## Targets de Interés

- Autopistas principales
- Corredores de carga
- Fronteras y puntos de control
- Zonas industriales

## Patrón de Localización (fork a otro idioma)

Para crear una versión localizada (ej: DRISH-ES):

1. Clonar el repo original
2. **Backend (drishx.py):** Cambiar `FEATURED_SITES` con targets locales, traducir log messages y mensajes de error/estado del endpoint `/api/analyze`
3. **Frontend HTML:** Traducir todos los labels, placeholders, botones, títulos de sección
4. **Frontend JS:** Cambiar `testArea` (centro por defecto del mapa), traducir strings de notificación, mensajes de HUD, labels del panel de intel, textos de autenticación, instantiate la clase con nombre localizado
5. **CSS:** No necesita cambios (solo código, sin texto visible)
6. **README:** Reescribir completo en el idioma objetivo
7. **Crear repo** en GitHub y push

**Pitfall:** El modelo RF (`rf_model.pickle`) es binario y universal — no necesita cambios al localizar. El modelo fue entrenado en autopistas alemanas pero funciona razonablemente en autopistas europeas similares.

## Pitfalls

- Requiere acceso a Copernicus Data Space (gratuito pero con registro)
- La resolución de Sentinel-2 (10m/píxel) limita la detección en carreteras secundarias
- Las condiciones climáticas (nubes) afectan la disponibilidad de imágenes
- El desfase temporal de 1.01s requiere corrección de geometría
- **execute_code + patch con comillas escapadas:** Las comillas simples dentro de strings Python que usan comillas dobles causan SyntaxError en execute_code. Dividir en batches pequeños o usar write_file para archivos completos cuando hay muchas traducciones

## Herramientas Complementarias

- **Aouei/remote-sensing-satellite-downloader**: descarga de Sentinel-2/Landsat
- **orcunkok/AWS-Dem-Downloader**: descargas de DEM de elevación
- **c2g-dev/city2graph**: análisis de grafos sobre datos geoespaciales
