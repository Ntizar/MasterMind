---
name: perma-archiving
description: Archivado web permanente de URLs — preservar contenido web para research y referencias académicas.
version: "1.0.0"
tags: [archiving, web, preservation, research, reference, permanent]
---

# Perma — Archivado Web Permanente

## Resumen

Servicio de archivado web permanente para preservar contenido web. 516⭐.

## Repo de referencia

- **GitHub:** `github.com/harvard-lil/perma`
- **Lenguaje:** Ruby on Rails
- **Licencia:** AGPL-3.0
- **Mantenedor:** Harvard Law Library

## Instalación

```bash
# Clonar y configurar
git clone https://github.com/harvard-lil/perma.git
cd perma
bundle install
# Configurar database y variables de entorno
```

## Uso Básico

```python
# Usar la API de Perma
import requests

# Archivar una URL
response = requests.post(
    "https://api.perma.archives/",
    json={"url": "https://ejemplo.com/articulo"},
    headers={"Authorization": "Bearer TU_API_KEY"}
)

archived_url = response.json()["archived_url"]
# https://perma.archives/XXXX-XXXX
```

## Funcionalidades

1. **Archivado permanente:** URLs que no se rompen nunca
2. **Captura completa:** HTML, CSS, JS, imágenes
3. **Citation:** URLs estables para referencias académicas
4. **API:** Integración programática
5. **Bulk:** Archivar múltiples URLs a la vez

## Integración con Mastermind

- Útil para `research-paper-writing` — preservar fuentes
- Complementa `harvard-lil/perma` — archivado de referencias
- Ideal para `prisma-systematic-review` — preservar evidencia
- Reemplaza screenshots para referencias permanentes

## Pitfalls

- **Servicio:** Requiere usar el servicio (no solo código local)
- **Rate limit:** Límite de archivados por día
- **Coste:** Uso comercial puede requerir licencia
- **Formato:** No todo el contenido se archiva igual (JS heavy)

## Referencias

- [GitHub: harvard-lil/perma](https://github.com/harvard-lil/perma)
