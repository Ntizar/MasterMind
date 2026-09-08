# Imágenes de producto de Amazon por ASIN (receta verificada)

Objetivo: bajar la imagen principal de un producto de Amazon.es (m.media-amazon.com) a partir del **ASIN**, sin PA-API.

## PITFALL principal
- **La página de producto `https://www.amazon.es/dp/<ASIN>` devuelve VACÍO (size=0) a curl sin cookies** → bloqueo. No se puede extraer la imagen de ahí directamente.
- **La vía fiable es la BÚSQUEDA**: `https://www.amazon.es/s?k=<query>` con **cookie jar + User-Agent + --compressed** (el patrón de `kit72h/scripts/buscar-amazon.py`). Los resultados SÍ contienen la imagen del producto.

## Receta (Python, reutiliza el approach de buscar-amazon.py)

```python
import os, re, subprocess, time, random, urllib.parse
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126 Safari/537.36")
JAR = 'C:/Users/d_ant/Projects/kit72money/_cookies_amz.txt'   # cookie jar persistente

def curl_get(url, timeout=60):
    tmp = '_tmp.html'
    cmd = ['curl','-s','-L','-o',tmp,'-w','%{http_code}','-c',JAR,'-b',JAR,
           '-A',UA,'--compressed','--max-time',str(timeout),url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+15)
    code = r.stdout.strip() or '000'
    txt = open(tmp, encoding='utf-8', errors='ignore').read() if os.path.exists(tmp) else ''
    if os.path.exists(tmp): os.remove(tmp)
    return code, txt

def img_for_asin(txt, asin):
    parts = re.split(rf'data-asin="{asin}"', txt)          # bloque del resultado
    if len(parts) < 2: return None
    b = parts[1][:20000]
    m = re.search(r'(?:src|data-image|data-lazy-src)="(https://m\.media-amazon\.com/images/I/[^"]+)"', b)
    return m.group(1) if m else None

url = 'https://www.amazon.es/s?k=' + urllib.parse.quote_plus('linterna led pilas')
img = None
for intento in range(3):
    code, txt = curl_get(url)
    if code == '200' and 's-result' in txt and 'captcha' not in txt[:3000].lower():
        img = img_for_asin(txt, 'B07C2T6GX4')
        if img: break
    try: os.remove(JAR)
    except OSError: pass
    time.sleep(2 + random.random()*3)
```

## Resultados observados (2026-09-06)
- 6 productos: **4/6 imágenes obtenidas** (`potabilizadoras`, `conservas`, `linterna`, `barritas`). 
- **Fallaron** `agua` y `raciones` → el ASIN **no estaba en la 1ª página** de resultados de la query usada (no es bloqueo, es que el producto no salió en el top). Fix: query más específica / paginar / usar la PA-API.

## Retry/fallback (verificado en kit72h, 7 categorías)
- **El ASIN no siempre sale en la 1ª página** → probar **varias queries por producto** (sinónimos) y, si sigue sin salir, **probar ASINs alternativos del mismo ítem** (p. ej. el mismo kit tenía `raciones militares` y `barritas`; si uno no sale, el otro sí).
- **Subir resolución**: las URLs vienen `.../I/<id>._AC_UL320_.jpg`; reemplaza `_AC_UL320_` → `_AC_SL1500_` (y `_UL320_` → `_SL1500_`) para el alta calidad.
- **Fallback de tema**: para un producto que no sale, busca el **tema** (p. ej. `manta termica`) y toma la imagen del **primer resultado cuyo título contenga el tema** (`primera_imagen_de_tema(txt, "manta")`). Vale para vídeo genérico de explicación (no para ficha exacta).
- 7/7 conseguidas con esto (agua, comida, luz, info, docs, salud, abrigo). Verificar con un **contact-sheet** (Pillow) y `vision_analyze` antes de integrar.

## Notas
- Las imágenes `m.media-amazon.com` son hotlinkables y se usan para contenido de afiliado, pero exigen **disclosure** del enlace afiliado y seguir las guías de Associates.
- **PA-API** (`GetItems` → `Images.Primary.Large.URL`) es la vía 100% compliant y estable si se tienen las keys de Associates; elimina el scraping frágil.
- Recortar a 9:16 (1080×1920) con Pillow: `ImageOps.exif_transpose` + crop centrado + `Image.LANCZOS`.
