---
name: curl-impersonate
description: "Usa al hacer requests impersonando navegadores (curl)."
version: "2.0.0"
tags: [curl, impersonate, fingerprint, antiscraping, http, cli, browsing]
related_skills: [curl-impersonate, adaptive-web-scraping, browser-use-ai, firecrawl-web-scraping]
---

# curl-impersonate — requests que parecen de navegador real

> ⚠️ Corrección 2026-09-05 (auditoría stars-explorer): la v1 documentaba build con CMake (`mkdir build && cmake ..`). El repo usa **autotools** (`./configure` + `make chrome-build`/`firefox-build`), y es principalmente un build/fork de curl para **CLI** (no solo "librería").

**Repo:** `https://github.com/lwthiker/curl-impersonate` (fork de curl en C, ~7K⭐). Bindings Python: `lexiforest/curl_cffi` (targets válidos: `chrome120`, `safari15_5`).

## When to Use

- Cuando un sitio web **bloquee** requests por fingerprint de TLS/User-Agent y necesites que la petición parezca de un navegador real (Chrome, Edge, Safari, Firefox).
- Para scraping de webs con protecciones anti-bot que no caen con un curl normal.

## Qué es

Un **build especial de curl**: fork parcheado para imitar el fingerprint TLS/HTTP2 de navegadores reales. Se usa principalmente como **CLI** (wrappers `curl_chrome*` / `curl_ff*`) y opcionalmente como libcurl enlazable. Impersona **Chrome, Edge, Safari y Firefox**.

## Uso (build autotools)

```bash
./configure
make chrome-build          # (o make firefox-build)
sudo make chrome-install   # (o sudo make firefox-install)
# Tras instalar, el acceso es via binarios tipo curl_chrome116, curl_ff117...
```

*(NO usa CMake en la raíz — no hay CMakeLists.txt; el build es autotools, ver INSTALL.md.)*

## Python (recomendado, simple)

```bash
pip install curl_cffi
```

```python
from curl_cffi import requests as creq
r = creq.get('https://web.com', impersonate='chrome120')   # o chromium/safari...
```

## Pitfalls

- Build: `./configure` + `make chrome-build`/`firefox-build` + `install` — **no** `mkdir build && cmake ..`.
- Es fork/build de curl orientado a **CLI**; describirlo solo como "librería" omite el rol central.
- Cubre **Chrome, Edge, Safari y Firefox** (no solo los 3 de la v1).

## Verificación

- Build con autotools y hacer `curl_chrome116 https://ejemplo.com` (o `curl_cffi` con `impersonate='chrome120'`); comprobar que un WAF que bloquea curl normal deja pasar la petición.
