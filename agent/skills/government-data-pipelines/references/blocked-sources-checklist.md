# Fuentes Españolas que Bloquean Acceso desde Servidor

## Contexto
Cuando se ejecuta desde un entorno servidor (VM, container, cron job), las principales fuentes de datos abiertos españoles bloquean el acceso. Esto es un patrón persistente, no un fallo puntual.

## Lista de Fuentes Bloqueadas

### INE (ine.es)
- **Patrón de bloqueo:** 404 en TODOS los endpoints API
- **Endpoints probados:**
  - `/jaxi/api/datatable/{id}` → 404
  - `/jaxi/export/{id}/csv` → 404
  - `/jaxi/export/{id}/json` → 404
  - `/menus/jaxi/api/TablaServlet` → 404
  - `/jaxiT3/DetalleServlet` → 404
- **Causa:** Sistema Jaxi es JS-rendered, los datos se cargan vía JavaScript
- **Conclusión:** IMPOSIBLE acceder vía curl. No intentar.

### datos.gob.es
- **Patrón de bloqueo:** 403 "Acceso denegado" con página HTML de CAPTCHA
- **Headers probados:** User-Agent, Accept-Language, Referer, Sec-Fetch-*
- **Conclusión:** Bloqueo por IP de servidor. No hay workaround con headers.

### Idealista
- **API:** Devuelve `{"message":"not found"}` para endpoints de estadísticas
- **Web:** CAPTCHA de Cloudflare en todas las páginas
- **Conclusión:** No accesible desde servidor

### Fotocasa
- **Patrón:** HTML mínimo con script de CAPTCHA (12KB)
- **Contenido:** Todo renderizado por JavaScript
- **Conclusión:** No accesible vía curl

### Portal de Vivienda (vivienda.gob.es / pvp.inmobiliaria.gob.es)
- **Patrón:** No reachable / conexión rechazada
- **Conclusión:** No accesible

### Sede MINECO
- **Patrón:** Devuelve página SharePoint (no datos)
- **Conclusión:** No es una fuente de datos accesible vía curl

### Registro de la Propiedad
- **Patrón:** HTML pero sin datos accesibles vía curl
- **Conclusión:** JS-rendered, no accesible

## Fuentes que SÍ Funcionan desde Servidor

### Wikipedia/Wikidata APIs
- `https://es.wikipedia.org/w/api.php` → JSON estructurado
- `https://www.wikidata.org/w/api.php` → datos estructurados

### RSS Feeds
- Muchos blogs y portales exponen RSS/Atom
- Parsear XML con Python es fiable

### Páginas con contenido estático
- Algunas páginas gubernamentales tienen secciones con HTML estático
- Verificar caso por caso

### Browser Tool
- `browser_navigate` + `browser_console` puede extraer contenido JS-rendered
- **Pitfall:** No funciona en subdominios NaN (`*.apps.nan.builders`)

## Patrón de Detección

```bash
# Si la respuesta tiene cualquiera de estas señales, está bloqueado:
# - HTML con "403" o "Acceso denegado"
# - HTML con "CAPTCHA" o "captcha-delivery"  
# - JSON {"message":"not found"}
# - 404 en endpoints API que deberían existir
# - HTML mínimo con <script> de captcha
# - Tamaño de respuesta < 1KB (probablemente CAPTCHA)
```
