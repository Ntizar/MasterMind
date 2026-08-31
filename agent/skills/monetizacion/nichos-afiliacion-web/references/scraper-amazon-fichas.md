# Scraper de fichas Amazon.es — patrón reutilizable (validado en Kit72h, agosto 2026)

Extraído del flujo Kit72h (83/85 productos resueltos). Permite: buscar producto en
amazon.es, extraer ASIN/título/precio/valoración, filtrar por rango y ≥4★, y verificar
la ficha final con buybox.

## Claves del método

- `--compressed` es OBLIGATORIO: amazon.es responde gzip y curl sin esto devuelve bytes no parseables.
- Cookie jar persistente (`-c cookies.txt -b cookies.txt`): la primera request establece sesión; las siguientes pasan.
- 503 / captcha → pausa + jar nuevo, o cambiar la query (una query con "ración liofilizada" devolvió login; "comida deshidratada raciones camping" funcionó).
- Precio en resultados de búsqueda: elemento `a-offscreen`. Valoración: `starRating`/aria-label.
- ASIN: patrón `dp/([A-Z0-9]{10})`.
- Verificación final: GET a `https://www.amazon.es/dp/<ASIN>` → HTTP 200, título presente, buybox/`addToCart` presente, precio coincide.

## Ejemplo mínimo (bash)

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
curl -s --compressed -L -c cookies.txt -b cookies.txt -A "$UA" \
  'https://www.amazon.es/s?k=powerbank+20000mah' > s.html
grep -oE 'dp/[A-Z0-9]{10}' s.html | sort -u | head
# para cada ASIN candidato:
curl -s --compressed -L -b cookies.txt -A "$UA" 'https://www.amazon.es/dp/<ASIN>' > ficha.html
# comprobar: título, precio a-offscreen, addToCart / buybox
```

## Referencia del flujo real

El scraper completo usado en el proyecto está en el repo: `Ntizar/Kit72h`,
`busquedas/buscar3.py` (búsqueda) y `busquedas/fichas3.py` (verificación de fichas).
Copiar y adaptar por lote de productos. Resultados por lote: `busquedas/loteN.txt`
formato `NUM | producto | URL | precio | verificada: extraccion|busqueda|no`.
