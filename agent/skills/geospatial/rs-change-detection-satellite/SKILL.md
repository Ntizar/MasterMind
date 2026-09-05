---
name: rs-change-detection-satellite
description: "Usa a detectar cambios satelitales con earthchange."
version: "2.0.0"
tags: [change-detection, satelite, remote-sensing, earthchange, cli, stac]
related_skills: [rs-change-detection-satellite, satellite-ai-vision, geodeep]
---

# Change Detection satelital — `earthchange`

> ⚠️ Corrección 2026-09-05 (auditoría): el paquete PyPI se llama **`earthchange`** (`pip install earthchange[all]`) y su interfaz principal es la **CLI** (`earthchange -s ... --map`), no solo snippets de índices/STAC.

**Repo:** `https://github.com/firmanhadi21/rs-change-detection` (Python, ~4⭐).

## When to Use

- Cuando pidas **detectar cambios satelitales** entre dos fechas (índices, STAC, mapas de diferencia) con `earthchange`.

## Uso (CLI real)

```bash
pip install "earthchange[all]"
earthchange -s <start_date> --map   # comprobar flags en el README
```

## Pitfalls

- Paquete: **`earthchange`** (no otro nombre).
- Interfaz principal es la **CLI**; verificar flags en el README.

## Verificación

- `earthchange` sobre dos fechas de una zona y comprobar que produce un mapa de cambio.
