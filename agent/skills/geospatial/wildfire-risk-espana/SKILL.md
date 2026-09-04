---
name: wildfire-risk-espana
version: "1.0.0"
description: "Usa para predecir ventanas de quema prescrita en España."
tags: [wildfire, espana, fwi, machine-learning, quema]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [wildfire, espana, fwi, machine-learning, quema]
    related_skills: [aemet-llm-report-pipeline, firecrawl-web-scraping]
---
# IgniWise — Predicción de ventanas de quema prescrita

## Resumen
`IgniWise` combina Machine Learning con el Sistema Canadiense FWI para predecir ventanas temporales seguras para quemas prescritas en España (prevención de megaincendios). Random Forest calibrado con datos de incendios históricos (MITECO, 1983–2015), FWI integrado (Van Wagner, 1987), cobertura nacional de 48 provincias peninsulares. Datos reales: topografía (Copernicus DEM GLO-30), NDVI (Sentinel-2 / GEE), cobertura forestal (CORINE Land Cover 2018). Predicciones cada 6 horas. Código de colores: 🟢 seguro / 🟡 precaución / 🔴 peligroso.

## Uso (comandos reales del README)

Opción A — Web (recomendado): visitar **igniwise.com**.

Opción B — Desarrollo local:
```bash
git clone https://github.com/TrueRomanZe/igniwise.git
cd igniwise
python -m venv venv
source venv/bin/activate
```

## Patrones / Arquitectura
- ML: Random Forest calibrado con incendios históricos (MITECO, 1983–2015).
- FWI: Sistema Canadiense de Índice de Peligro de Incendio (Van Wagner, 1987), estándar internacional validado en 60+ países.
- Cobertura: 48 provincias de España peninsular.
- Entradas geoespaciales: Copernicus DEM GLO-30, NDVI Sentinel-2/GEE, CORINE Land Cover 2018.
- Totalmente automatizado: predicciones cada 6 horas sin intervención manual.

## Pitfalls
- Solo cubre España peninsular (48 provincias); no incluye islas.
- El modelo se calibra con datos MITECO 1983–2015; no asumir cobertura fuera de ese rango.
- Requiere Python 3.11+; datos y dataset con DOI 10.5281/zenodo.19144668.

## Verificación
- Comparar la predicción de la web (igniwise.com) con el código de color (🟢/🟡/🔴).
- Ejecutar localmente y verificar que las predicciones se actualicen cada 6 horas.

## Referencia
README de https://github.com/TrueRomanZe/IgniWise (MIT, Python 3.11+). Web: igniwise.com. Dataset DOI 10.5281/zenodo.19144668.
