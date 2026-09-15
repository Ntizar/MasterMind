---
name: fleetbase-logistics-os
description: "SO logístico self-hosted con flota, pedidos y OSRM."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [logistica, flota, osrm, self-host, laravel, tracking, movilidad]
    related_skills: [routing-isochrones, transit-data-pipelines, postgres-mcp]
---

# Fleetbase — sistema operativo logístico self-hosted

Back-office completo de operaciones logísticas (AGPL-3.0): pedidos, conductores, zonas de servicio, tracking en vivo y routing — pensado como **framework extensible**, no como app cerrada.

## When to Use (cuándo usarlo)

- Necesitas un **back-office de flota/entregas** self-hosted para una demo o producto de movilidad.
- Quieres tracking en vivo sobre mapa + API REST para conectar tus propios frontends vanilla JS.
- Buscas un caso de estudio de arquitectura Laravel + Ember + Docker modular.

## Instalación verificada

```bash
npm install -g @fleetbase/cli
flb install-fleetbase                    # instalador interactivo (orquesta Docker)

# alternativa manual
git clone git@github.com:fleetbase/fleetbase.git && cd fleetbase && ./scripts/docker-install.sh
```

Requisitos: Node 22, Docker + Compose, Git. Consola en `http://localhost:4200`, API REST en `http://localhost:8000`.
Si falta la app key: `docker compose exec application bash -c "php artisan key:generate --show"` → pegar en `APP_KEY`. CORS con `CONSOLE_HOST` y `FRONTEND_HOSTS` (lista separada por comas).

## Piezas reutilizables para dashboards de movilidad

- **Order Board** estilo kanban y **Order Config** con reglas, flujos y campos personalizados.
- **Tracking de pedido en mapa**, **live fleet map**, **service zones** y telemetría de dispositivos.
- API REST + **sockets** + webhooks → integrable con frontends propios.
- **Routing OSRM integrado**: por defecto `router.project-osrm.org`; se apunta a un OSRM propio con `OSRM_HOST` en el `.env` del entorno correspondiente dentro de `console/environments/`.

## Comparativa con el stack actual

Frente a los pipelines GTFS/GBFS + visores propios, Fleetbase aporta el **back-office de operaciones** (pedidos, conductores, zonas, despacho) pero **no datos de transporte público**. Integración natural: OSRM self-hosted + la capa de isócronas del skill `routing-isochrones`.

## Pitfalls

- AGPL-3.0: si se expone como servicio, obliga a publicar modificaciones.
- El instalador es interactivo; en automatización conviene la vía `scripts/docker-install.sh` + `.env` explícito.
- PHP/Laravel + Ember: no es stack habitual del resto de proyectos — valorar coste de mantenimiento antes de adoptarlo.

## Referencia

- Repo: `fleetbase/fleetbase` (~3.302 ⭐, JavaScript/PHP, consultado 2026-09-15).
