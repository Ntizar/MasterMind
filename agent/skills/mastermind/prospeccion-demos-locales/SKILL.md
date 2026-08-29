---
name: prospeccion-demos-locales
description: "Use when prospecting local businesses for web demo sales."
version: 1.0.0
author: Mastermind
license: MIT
metadata:
  hermes:
    tags: [prospeccion, ventas, demos, scraping, github-pages, web-design, diseno-web]
---

# Prospección de negocios locales con demos web personalizadas

Sistema para identificar negocios locales con web mejorable y generarles una **demo conceptual
personalizada** como pieza de venta (oferta: web 500 € + mantenimiento 50 €/año).
Proyecto activo: `~/Projects/prospeccion-mvp` (repo: Ntizar/prospeccion-mvp, Pages activo).
Documento maestro del cliente: `~/Projects/planning-tmp/planning.pdf`.

## Pipeline (nivel 2-3 de ejecución)

1. **Descubrir** — Overpass API (OpenStreetMap, licencia ODbL, sin problemas de términos como
   Google Maps). Query por `area["name"="Ciudad"]["admin_level"="8"]` + tags de negocio
   (`craft=plumber`, `shop=*`...). Filtrar solo los que tienen `website`. Dedupe por nombre
   normalizado (sin acentos/no alfanum). Script: `scripts/descubrir.py` del repo.
2. **Auditar** — urllib con `ssl` (CERT_NONE para OBSERVAR: cert roto = hallazgo, no bypass),
   comprobar: HTTPS, viewport, title/description, tiempo de carga, `tel:`/`wa.me`/`<form>`,
   peso HTML, generador antiguo. Score explicable por reglas. NO inventar problemas: una web
   decente saca score bajo y así se queda.
3. **Scrapear su identidad** (ver `references/extraccion-marca.md`):
   - Contactos reales: `tel:`, `wa.me/`, `api.whatsapp.com?phone=`, `mailto:`, direcciones.
     Solo datos publicados por el propio negocio. Nada inventado; lo no verificado → "(a confirmar)".
   - Logo → descargar → `vision_analyze` para extraer paleta REAL de marca (los colores del CSS
     suelen ser los defaults del CMS, p.ej. paleta Gutenberg de WordPress).
   - Fotos reales: descargar `img/` del lead, optimizar con PIL (max 1600px, quality 76-78,
     ~50-250 KB). Manejar imágenes truncadas (re-descargar / `LOAD_TRUNCATED_IMAGES=True`).
   - Contenido: servicios reales, historia, diferenciadores, textos del "Sobre nosotros".
4. **Construir la demo DESDE CERO** — nunca plantilla-rígida. Lección clave del cliente:
   *la plantilla "cierra demasiado" cómo debe ser la web; escribir cada HTML desde cero
   inspirándose en su web actual y modernizándola*. Dos demos de negocios distintos NUNCA
   comparten estructura. Reglas fijas y anti-slop en `references/guia-diseno.md`
   (espejo de `plantillas/GUIA-DISENO.md` del repo).
5. **Publicar** — GitHub Pages del repo `prospeccion-mvp`:
   ```bash
   gh api repos/Ntizar/prospeccion-mvp/pages -X POST -f build_type=legacy -f "source[branch]=main" -f "source[path]=/"   # solo primera vez
   git add -A && git commit && git push
   # Pages tarda: 404 inicial es normal, esperar ~30-60s y verificar:
   gh api repos/Ntizar/prospeccion-mvp/pages/builds/latest --jq '.status'
   curl -s -o /dev/null -w "%{http_code}" https://ntizar.github.io/prospeccion-mvp/demos/<slug>/index.html
   ```
6. **Contacto comercial** — SIEMPRE con aprobación humana (canal acordado: formulario de
   contacto del negocio). Los borradores salen de los hallazgos reales de la auditoría.

## Legales (innegociables)

- Demo con `<meta name="robots" content="noindex, nofollow">` + banner de disclosure
  ("Demo conceptual — propuesta no oficial para X. No es su web.").
- No scrapear Google Maps contra sus términos; fuente aprobada: OSM + la web pública del negocio.
- Sin datos personales, sin reseñas reproducidas, sin promesas de resultado.
- España: LSSI regula el correo comercial no invitado; el formulario de contacto propio del
  negocio es la vía segura para arrancar. Yo no soy abogado: derivar decisiones de canal a David.

## Pitfalls

- **Token de Telegram en el comando** → bloqueo de aprobación y timeout silencioso. Leerlo del
  `.env` dentro del script. Si un comando se BLOQUEA esperando consentimiento, NO reintentar
  variantes: parar y pedir al usuario.
- `curl` sin `timeout` puede colgar el pipeline entero: siempre `timeout=25` en urllib y
  reintentos con backoff.
- `execute_code` con User-Agent custom es obligatorio contra APIs exigentes (NaN 403 sin él).
- No usar `web_extract` para sitios que bloquean extractores: urllib directo funciona mejor.
- Pages no permite headers HTTP custom → el `noindex` va como meta tag en el HTML.
- Repos privados no tienen Pages gratis (plan público actual).

## Estado y siguientes pasos (recurrente)

- Canal de avisos pendiente de activar: bot Telegram @NtizarBot (token ya en `.env` del perfil
  hermes como `TELEGRAM_BOT_TOKEN`; falta `TELEGRAM_ALLOWED_USERS` con el ID numérico de David).
- Demos publicadas de referencia (verificar estructura variada): `demos/tenofransa` (industrial
  azul), `demos/poceria-la-canada` (rojo 24h, 3 teléfonos), `demos/saneamientos-aluche` (showroom).
