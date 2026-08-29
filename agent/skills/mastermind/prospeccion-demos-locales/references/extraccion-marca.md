# Extracción de marca de la web actual del negocio

Recetas verificadas en sesión (agosto 2026, 3 negocios reales de Madrid) para extraer todo lo
necesario antes de construir una demo.

## Contactos (solo lo publicado por el propio negocio)

```python
# regex probadas sobre el HTML descargado con urllib
import re
tel_links   = set(re.findall(r'href=["\']tel:([^"\']+)', html))
whatsapp    = set(re.findall(r'(?:wa\.me/|api\.whatsapp\.com/[^"\']*?phone=|whatsapp://send\?phone=)(\d{9,15})', html))
emails      = set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.]{2,10}', html))   # ojo: filtra emails de plugins (hello@quadlayers.com era de un plugin WP)
direcciones = re.findall(r'(C/[^<",]{5,50}|Avda[^<",]{5,50}|Calle [^<",]{5,50})', html)
```

- Revisar también la página de contacto interna (el teléfono a veces solo está ahí — fue el caso
  de pocerialacanada.com: 3 teléfonos distintos, uno por servicio).
- **Bug frecuente**: números con dígitos de más (saneamientosaluche.com tenía `3467684946688`,
  13 dígitos, y por eso su `tel:` fallaba). Si el número no pasa una validación de 9/11-12
  dígitos razonable → "(a confirmar con el negocio)", nunca publicar un número roto.

## Colores de marca reales

1. Los hex del HTML principal suelen ser la paleta **por defecto del CMS** (Gutenberg de
   WordPress suelta siempre los mismos 20 colores). NO usarlos.
2. Identificar el tema (`/wp-content/themes/<tema>/`) y descargar su `style.css` + el CSS del
   child si existe.
3. El método fiable: descargar el **logo** y pasarlo a `vision_analyze` pidiendo hex aproximados
   por elemento. Probado con logo JPG de 26 KB → paleta completa (navy #1B3A5C, naranja #E87722,
   azules del degradado del texto).
4. Comprobar contra los colores más frecuentes de la página; el de marca suele repetir
   (La Cañada: rojo #9E292B x32).

## Fotos

- Coger las de su web actual (galería, slider, "sobre nosotros"). Son suyas y venden más que
  cualquier stock.
- Descargar con UA de navegador, reintentar si el archivo queda truncado
  (error de PIL: `OSError: image file is truncated` → re-descarga completa o
  `PIL.ImageFile.LOAD_TRUNCATED_IMAGES = True`).
- Optimizar con PIL: ancho máx 1600 px, JPEG quality 76-78 → de 5,7 MB a ~230 KB.
- Guardar en `demos/<slug>/img/` con nombres semánticos (equipo-1.jpg, camion.jpg, trabajo-1.jpg).

## Contenido que hay que leer de su web

- Menú completo (las categorías del catálogo/tipos de servicio = secciones de la demo).
- Texto del "Sobre nosotros"/historia (años de fundación, cobertura, comunidad de fincas...).
- Diferenciadores: servicios que NO ofrece la competencia típica (ej: trasteros de obra en La
  Cañada, showroom desde 1968 en Aluche). Estos protagonizan una sección propia.
- Torpezas de su web actual (slider con imágenes de ejemplo de WordPress, banner de navidad en
  agosto, teléfono roto): son argumentos de venta para el email, no para la demo.
