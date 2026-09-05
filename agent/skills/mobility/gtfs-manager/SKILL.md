---
name: gtfs-manager
description: "Usa a editar y validar feeds GTFS con GTFS Manager."
version: "2.0.0"
tags: [gtfs, manager, gui, editor, validacion, web]
related_skills: [gtfs-manager, gtfs-tidy, gtfs-to-html-timetables, transit-data-pipelines]
---

# GTFS Manager — gestor gráfico de feeds GTFS (GUI)

> ⚠️ Corrección 2026-09-05 (auditoría): **NO** es una librería Python (`from gtfs_manager import GTFSManager`). Es una **app web GUI** que se ejecuta con `GTFSManager.exe` o Docker; licencia **GPL-3.0** (no Apache 2.0).

**Repo:** `https://github.com/WRI-Cities/static-GTFS-manager` (JavaScript/GUI, ~159⭐). Licencia: **GPL-3.0**.

## When to Use

- Cuando pidas **crear/editar y validar feeds GTFS** desde una interfaz gráfica (subir, editar agencias/rutas/paradas, validar), sin tocar el JSON/SQLite a mano.

## Qué es

Editor gráfico web (GUI) para feeds GTFS estáticos. Modelo de datos basado en **gtfs-validator** y el esquema oficial.

## Uso

```bash
# App de escritorio (Windows): ejecutar GTFSManager.exe
# o Docker:
docker run -p 8080:8080 gtfsmanager
# (abrir la UI web y cargar un feed .zip)
```

## Pitfalls

- **No** `from gtfs_manager import GTFSManager` — es GUI, no librería Python.
- Licencia: **GPL-3.0**.

## Verificación

- Abrir la UI, cargar un feed y validarlo; comprobar que reporta errores del feed.
