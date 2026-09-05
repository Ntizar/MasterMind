---
name: perma-archiving
description: "Usa a archivar webs permanentemente con Perma (Django)."
version: "2.0.0"
tags: [perma, archivado, archiving, django, python, web, preservacion]
related_skills: [perma-archiving, website-downloader, batch-file-download]
---

# Perma — archivado web permanente

> ⚠️ Corrección 2026-09-05 (auditoría): el stack es **Django/Python** (no Ruby on Rails); **no** `bundle install`; licencia MIT/GPL (no AGPL); la API real es **`api.perma.cc/v1`** (no `api.perma.archives`).

**Repo:** `https://github.com/permalink/perma` (Django/Python, ~2K⭐). Servicio de la Library of Congress / oficinas de archivo: crea enlaces permanentes a URLs.

## When to Use

- Cuando pidas **archivar una URL de forma permanente** (captura inmutable para citas/legal/periodismo) con Perma o self-host.

## Uso (API)

```bash
# API real: api.perma.cc/v1
curl -X POST https://api.perma.cc/v1/archives \
  -H "Authorization: Token <token>" \
  -d '{"url":"https://ejemplo.com"}'
```

Self-host en local: Django + Python (requisitos del repo).

## Pitfalls

- Stack: **Django/Python**, no Rails; instalación vía requirements de Python, no `bundle install`.
- Endpoint: **`api.perma.cc/v1`** (no `api.perma.archives`, que no existe/DNS).
- Licencia: MIT/GPL (no AGPL).

## Verificación

- Crear un archive vía la API y comprobar que devuelve el enlace permanente estable.
