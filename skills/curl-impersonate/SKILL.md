---
name: curl-impersonate
description: curl-impersonate — librería para hacer requests que impersonan browsers reales, evitando detección anti-bot.
category: data-pipeline
---

# curl-impersonate — Impersonar Browsers para Scraping

## Qué es

curl-impersonate es una librería que modifica curl para impersonar fingerprints de browsers reales:
- **TLS fingerprint** — TLS Client Hello idéntico a Chrome/Firefox/Safari
- **HTTP/2 settings** — SETTINGS frame idéntico a browser real
- **User-Agent spoofing** — headers completos de browser
- **Anti-bot** — evade detección de Cloudflare, DataDome, etc.

## Instalación

```bash
# Clonar y compilar
git clone https://github.com/lwthiker/curl-impersonate.git
cd curl-impersonate
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
make -j$(nproc)
sudo make install

# O usar la librería Python
pip install curl_cffi
```

## Uso básico

```python
from curl_cffi import requests

# Impersonar Chrome 120
response = requests.get(
    'https://httpbin.org/headers',
    impersonate='chrome120'
)
print(response.json())

# Impersonar Safari
response = requests.get(
    'https://httpbin.org/headers',
    impersonate='safari15_5'
)
```

## Casos de uso para David

- **Web scraping** — scrapear sites con anti-bot
- **API testing** — hacer requests que parecen de browser
- **Data collection** — recoger datos de sites protegidos
- **Integration** — usar con Crawlee/Firecrawl para scraping robusto

## Pitfalls

- Requiere compilar curl custom (o usar curl_cffi)
- Las fingerprints se actualizan con cada versión de browser
- No es 100% indetectable — sites muy protectados pueden detectar
- curl_cffi es la opción más fácil (no requiere compilar)

## Referencias

- Repo: `github.com/lwthiker/curl-impersonate` (6K⭐)
- curl_cffi: `https://github.com/lexiforest/curl_cffi`
