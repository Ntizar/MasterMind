---
name: geospatial-ai-agents
description: "Agentes geoespaciales con STAC y raster satelital."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [stac, planetary-computer, satelite, raster, agentes, mcp, geoint]
    related_skills: [satellite-gis-patterns, rs-change-detection-satellite, aws-dem-terrain-tiles]
---

# Agentes geoespaciales (STAC + Planetary Computer)

Patrón de arquitectura (Microsoft, MIT) para **asistentes geoespaciales multi-agente**: la pregunta va en lenguaje natural → un agente STAC elige la colección → se renderiza en el mapa → un agente de visión razona sobre el raster.

## When to Use (cuándo usarlo)

- Quieres **datos satelitales gratis y sin suscripción** (Planetary Computer / NASA VEDA).
- Diseñas un asistente que responde preguntas de terreno, inundación, comparación temporal o daño en edificios.
- Necesitas exponer herramientas geoespaciales como **servidores MCP**.

## Fuentes de datos aprovechables sin Azure

- **Microsoft Planetary Computer STAC API** — 130+ colecciones públicas.
- **NASA VEDA STAC API** — colecciones públicas equivalentes.
- Solo las colecciones privadas requieren MPC Pro / GeoCatalog en tu tenant.

## Módulos GEOINT (como herramientas de agente)

STAC (chat-to-map) · Clarifier · Load · **Raster Sampling** (valor del raster en un punto) · Contextual · Vision · **Terrain** (pendiente, riesgo de inundación, línea de visión: `elevation, slope and line-of-sight at 38.9N, 77.0W`) · Mobility · Comparison · Building Damage · Extreme Weather · Forecast.

## Patrón "un backend, varias superficies"

El mismo backend sirve: app React con mapa, bot de Teams y agente declarativo de M365 Copilot — y cada agente se expone como **servidor MCP** para VS Code / Claude Desktop. Es el patrón a copiar para llevar un motor geoespacial propio a varios clientes.

## Despliegue (solo si hay Azure)

```powershell
az login
./deploy-infrastructure.ps1     # preflight: AOAI gpt-4o, Container Apps, ACR
```

Toggles por entorno: `MPC_PRO`, `PRIVATE`, `FABRIC`, `WEATHER_MODELS`, `LOCATION` (todos OFF por defecto). Alternativa: GitHub Actions con OIDC y secrets `AZURE_CLIENT_ID`/`AZURE_TENANT_ID`/`AZURE_SUBSCRIPTION_ID` (RG por defecto `rg-planetaryexplorer`).

## Pitfalls

- La pila completa es **Azure de pago** (AI Foundry, Agent Service, Azure Maps, AI Search, Container Apps, Key Vault) — el valor gratis está en las **APIs STAC**, no en el despliegue.
- El README avisa: **no es un producto soportado** por Microsoft, es un patrón de referencia.
- El frontend autorizado es Esri ArcGIS (opcional).

## Referencia

- Repo: `microsoft/Planetary-Explorer` (~198 ⭐, Python, consultado 2026-09-15).
