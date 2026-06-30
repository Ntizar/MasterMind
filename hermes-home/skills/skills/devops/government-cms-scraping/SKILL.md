---
name: government-cms-scraping
description: Extraer datos de sitios web gubernamentales (principalmente Drupal) donde el contenido se carga dinámicamente vía AJAX — patrones de URL, cookies de sesión, manejo de Cloudflare, múltiples path patterns de recursos.
---

# Government CMS Data Scraping

Extraer datos de sitios web gubernamentales (principalmente Drupal) donde el contenido se carga dinámicamente vía AJAX.

## Patrones comunes

### 1. Drupal Views con AJAX (contenido dinámico)

**Síntoma:** `curl` obtiene el HTML pero sin el contenido real (solo menú de navegación). Los PDFs/enlaces están en JavaScript.

**Estrategia:**

1. **Buscar PDFs en meta description primero:**
   ```bash
   curl -s "$URL" | grep -oP '<meta[^>]+description[^>]+>[^<]+' | head -1
   ```
   Los CMS suelen meter enlaces en el meta description.

2. **Probar múltiples patrones de URL por año/rango:**
   ```
   /informes/AÑO        (ej: /2008, /2015)
   /informes/infofin-AÑO (ej: /infofin-2017)
   /infofin/2008/informes-accidentes-ferroviarios-2008  (subpáginas internas)
   ```

3. **Buscar todos los patrones de recursos en cada página:**
   ```bash
   # Patrón nuevo (paginabasica)
   grep -oP '/recursos_mfom/paginabasica/recursos/[^"<\s]+\.pdf'
   # Patrón medio (pdf/UUID/)
   grep -oP '/recursos_mfom/pdf/[^"]+\.pdf'
   # Patrón viejo (comodin/recursos/ o directo en /recursos_mfom/)
   grep -oP 'href="(/recursos_mfom/[^"]+\.pdf)"'
   ```

4. **Usar cookies de sesión:**
   ```bash
   # Paso 1: Obtener cookie
   curl -s -c /tmp/session.txt -b /tmp/session.txt "https://site.es/" -o /dev/null
   # Paso 2: Usar cookie en peticiones
   curl -s -b /tmp/session.txt "https://site.es/pagina"
   ```

### 2. Browser tool bloqueado por Cloudflare

**Síntoma:** 403 "PÁGINA WEB BLOQUEADA" en browser tool.

**Soluciones alternativas:**
- `curl` con User-Agent realista y Referer
- **Wayback Machine** (archive.org) como fallback para snapshots históricos
- Buscar endpoints API directos en el JS embebido (`Drupal.settings`)

### 3. Subpáginas internas con patrones específicos

**Síntoma:** La página principal del año no tiene PDFs, pero las subpáginas sí.

**Patrón descubierto (CIAF 2007-2014):**
```
# Página principal: solo menú, sin contenido
/informes-finales-de-sucesos-investigados/2008

# Subpágina con PDFs:
/informes-finales-de-sucesos-investigados/2008/informes-accidentes-ferroviarios-2008
```

**Estrategia:**
1. Probar `/{año}/informes-accidentes-ferroviarios-{año}` como subpágina
2. Si no funciona, probar `/{año}/` directamente (puede contener enlaces)
3. Buscar **todos** los patrones de PDFs posibles en cada subpágina
4. Combinar resultados de múltiples subpáginas por año

### 3. Endpoint AJAX de Drupal Views

Si el contenido se carga vía AJAX, buscar en `Drupal.settings`:
```bash
curl -s "$URL" | grep -oP 'Drupal\.settings[^;]+' | python3 -c "import sys,json; print(json.dumps(json.loads(sys.stdin.read().replace(\"Drupal.settings, \",\"\")), indent=2))"
```

Los endpoints AJAX suelen estar en `path` o `url` dentro de la configuración de la vista.

## Ejemplo: CIAF (Comisión de Investigación de Accidentes Ferroviarios)

**URL principal:** `https://www.transportes.gob.es/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados/`

**Patrón de URL (verificado 2026-06-26):**
- **2007-2016:** `/MFOM/LANG_CASTELLANO/ORGANOS_COLEGIADOS/CIAF/INFORMES/YYYY/` — HTML estático con PDFs
- **2017-2025:** `/informes-finales-de-sucesos-investigados/infofin-YYYY` — HTML estático con PDFs
- **NOTA:** Los patrones anteriores (`informes-accidentes-ferroviarios-YYYY`) NO funcionan. La URL real para 2007-2016 es la ruta `/MFOM/LANG_CASTELLANO/...`

**Patrones de PDFs (cambian según año):**
- Viejo (2009-2016): `/recursos_mfom/pdf/UUID/ID/FILENAME.pdf`
- Nuevo (2017-2025): `/recursos_mfom/paginabasica/recursos/FILENAME.pdf`

**Resultado:** 219 informes totales (2007-2025). 2007 y 2008 vacíos.

## Checklist de scraping

1. [ ] Probar curl con User-Agent realista y Referer
2. [ ] Buscar PDFs en meta description
3. [ ] Identificar patrón de URL (AÑO directo vs infofin-AÑO)
4. [ ] Probar múltiples patrones de path de recursos
5. [ ] Obtener cookies de sesión si es necesario
6. [ ] Buscar configuración AJAX en Drupal.settings
7. [ ] Wayback Machine como último recurso
8. [ ] Validar que los PDFs descargados no son páginas de error (Content-Type: text/html)

## Pitfalls

- **Cloudflare 403 en browser tools:** el navegador está bloqueado pero curl puede funcionar
- **Drupal Views AJAX:** el HTML descargado solo tiene el menú, no el contenido
- **Múltiples patrones de URL:** un mismo CMS cambia sus rutas entre versiones
- **PDFs que son HTML de error:** verificar Content-Type antes de guardar
- **Títulos con espacios en href:** los CMS Drupal suelen meter `title='Enlace a archivo...'` dentro del href. Usar `grep -oP "href=(['\"])(/recursos_mfom/pdf/[^'\"]+?\.pdf)\1"` en vez de `[^"<\s]` que se rompe con espacios
- **Subpáginas internas:** si la página principal de un año no tiene PDFs, probar `/{año}/informes-accidentes-ferroviarios-{año}` como subpágina alternativa
