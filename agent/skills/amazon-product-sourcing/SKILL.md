---
name: amazon-product-sourcing
description: Use al buscar productos en Amazon para afiliación y enlaces.
---

# Búsqueda de productos Amazon.es para afiliación

Flujo validado en Kit72h (85 productos → URLs verificadas). Castellano siempre, atribución a David Antizar.

## Flujo

1. Extraer lista de productos desde la fuente (ej. `data/kits.json`) a un archivo de texto plano `num|producto|precio_aprox` — más fácil de delegar que JSON.
2. Delegar búsqueda por lotes (~17 productos/lote) con `delegate_task` en paralelo.
3. Cada lote escribe su resultado en un `.txt` propio (formato: `num | producto | URL | precio | verificada: extraccion|busqueda|no`).
4. Verificar que todos los ficheros existen y tienen las líneas esperadas (los subagentes pueden fallar en silencio: rate limit, cap de iteraciones). Relanzar solo los lotes incompletos.
5. Generar Excel con openpyxl (2 columnas de URL: la de Mastermind y la del usuario con su tag) y pasarlo al usuario.
6. Cuando el usuario devuelve el Excel con sus URLs de afiliado, inyectarlas en la fuente (`kits.json`) y verificar la web.

## Método probado para scrapear Amazon.es (curl con cookies)

- `curl -s -L -c cookies -b cookies -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36' 'https://www.amazon.es/s?k=PRODUCTO+URL'`
- curl directo SIN cookies → 503. Con cookie jar de sesión funciona.
- Si 503 persiste: nueva cookie jar o `web_search 'site:amazon.es <producto>'`.
- Extraer ASIN (`dp/XXXXXXXXXX`), título, precio, valoración. Filtrar: precio en rango, ≥4★, buybox activo.
- Verificación final: fetch directo de la ficha (HTTP 200) → marcar `extraccion`; si solo vino de búsqueda → `busqueda` (revisable).

## Pitfalls

- **Rate limit del proveedor con subagentes paralelos**: 5 delegaciones simultáneas pueden agotar tokens/min (HTTP 429) y cortar lotes a mitad. Los lotes que fallen deben relanzarse tras leer su `.txt` — nunca asumir completado por el resumen del subagente.
- **Subagentes con cap de iteraciones**: su resumen puede llegar truncado; el fichero en disco es la verdad, no el summary.
- **Productos sin sentido en Amazon** (efectivo, mapas locales genéricos): marcar `N/A — no aplica` y proponer bloque de texto en la web en vez de enlace.
- **NO inventar URLs nunca** — cada ASIN debe venir de una búsqueda o fetch real.
- openpyxl no está en el venv de Hermes: usar el Python del sistema `C:/Users/d_ant/AppData/Local/Programs/Python/Python312/python.exe`.
- Límites de Amazon Afiliados: URLs requieren aprobación humana; mantener el flujo Excel → revisión usuario → inyección en la web.

## Tag de afiliado (atajo sin Excel)

Cuando el usuario ya tiene su tag (Kit72h: `nti0c8-21`), NO hace falta el flujo Excel: inyectarlo directamente en las URLs verificadas con `url.split('?')[0] + '?tag=nti0c8-21'`.

**Pitfall del placeholder compartido**: si dos productos apuntan al mismo placeholder (ej. `AMAZON-URL-FAJA` usado por "faja portadocumentos" y por "efectivo en billetes"), el N/A de uno deja el otro sin enlace. Tras la inyección, auditar SIEMPRE todos los items `afiliado==''` y recuperar los que sí son vendibles buscando su ASIN de nuevo.

## Control de estado de enlaces (detección de roturas)

- Script `scripts/comprobar-urls.py` en el repo: lee `data/kits.json`, comprueba cada ficha con curl+cookie jar (200 + `productTitle` en HTML), y genera `data/estado.json` con `ok` / `posible_rotura` + búsqueda de alternativa.
- La web (js/estado.js) muestra badges ✅ disponible / ⚠️ posible rotura con enlace a búsqueda Amazon.
- Reintentos anti-503: dormir 3-6 s y repetir; 404 directo = rotura. Pausa de 1,5 s entre fichas.
- Programar revisión periódica con cronjob mensual que ejecuta el script y hace commit/push de `estado.json`.
- Ojo con URLs duplicadas entre kits: `estado.json` se indexa por URL única — al añadir productos nuevos, relanzar el script o rellenar sus entradas (verifica que `total` de estado.json == URLs únicas de kits.json).

## Contenido adyacente de alto valor

Las webs de afiliación mejoran mucho con: sección de guías temáticas (huerto, autosuficiencia...) con productos propios buscados y verificados igual que el resto, y blog con 3-4 entradas SEO que enlazan a los kits. Para libros, comprobar si existe edición en castellano antes de enlazar la original.

## Verificación

- Contar líneas de todos los `.txt` de lotes vs total de productos antes de generar el Excel.
- Comprobar que cada URL responde 200 y sigue patrón `amazon.es/dp/ASIN` (o slug largo con `/dp/` al final).
- Tras inyectar el tag: contar items con `tag=<usuario>` vs total, y verificar el sitio en local (http.server + comprobaciones JS del DOM: badges, botones con tag, entradas de blog).
