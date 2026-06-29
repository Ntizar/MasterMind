---
name: spanish-open-data-collection
description: "Patrones para recolectar datos abiertos españoles cuando las fuentes oficiales (INE, datos.gob.es, Portal de Vivienda) bloquean acceso API desde servidores. Incluye técnicas de estimación por provincia con multiplicadores intra-provincia."
version: "1.0.0"
tags: [data, spain, open-data, government, blocked, estimation, housing, ine]
---

# Spanish Open Data Collection — Patrones de recolección cuando fuentes oficiales bloquean

## Cuándo usar

- Se necesita datos abiertos españoles (precios vivienda, demografía, economía) desde un entorno servidor (VM, container, cron job)
- Las fuentes oficiales bloquean acceso API/curl desde IPs de servidor
- Se necesita cobertura a nivel de código postal (CP) pero solo hay datos a nivel provincial/municipal

## Fuentes que bloquean desde servidor

Las siguientes fuentes españolas **bloquean sistemáticamente** el acceso desde curl/headless:

| Fuente | Bloqueo | Detalle |
|--------|---------|---------|
| **INE (ine.es)** | ⚠️ Parcial | El sistema Jaxi (rendered JS) bloquea curl. **PERO la API REST SÍ funciona:** `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{id}?tip=AM&nult=1` retorna JSON directo. Tablas conocidas: 28201 (salarios), 2852 (población). Sin key, sin CAPTCHA. |
| **datos.gob.es** | 403 con CAPTCHA | Devuelve página HTML con "Error 403 - Acceso denegado" independientemente de User-Agent. Bloqueo por IP de servidor. |
| **Idealista** | 404 API + CAPTCHA web | API devuelve `{"message":"not found"}`. Web devuelve CAPTCHA de Cloudflare. |
| **Fotocasa** | JS-rendered | Devuelve HTML mínimo con script de CAPTCHA. Todo el contenido es JS. |
| **Portal de Vivienda (vivienda.gob.es)** | No reachable | No responde o redirige. |
| **Sede MINECO** | SharePoint | Devuelve página SharePoint (no datos). |
| **Registro de la Propiedad** | JS-rendered | Devuelve HTML pero sin datos accesibles vía curl. |

### Patrón de detección de bloqueo

```bash
# Si la respuesta tiene alguna de estas señales, está bloqueado:
# - HTML con "403" o "Acceso denegado"
# - HTML con "CAPTCHA" o "captcha-delivery"
# - JSON {"message":"not found"}
# - 404 en endpoints de API que deberían existir
# - HTML mínimo con <script> de captcha
```

### Headers que NO funcionan

Ninguno de estos headers supera el bloqueo de fuentes españolas desde servidor:
- `User-Agent: Mozilla/5.0 ... Chrome/120.0.0.0`
- `Accept: application/json`
- `Accept-Language: es-ES,es;q=0.9`
- `Referer: https://www.ine.es/`
- `Sec-Fetch-*` headers completos

**Conclusión:** No pierdas tiempo probando headers diferentes con estas fuentes. Si curl falla una vez, la fuente está bloqueada.

## Alternativas: Estimación por provincia con multiplicadores

Cuando las fuentes oficiales bloquean, usar **precios base por provincia** + **multiplicadores intra-provincia**.

### Paso 1: Obtener precios base por provincia

Usar fuentes alternativas que SÍ funcionan:
- Informes públicos de Idealista/Fotocasa (Q1-Q4 2024) — disponibles en sus blogs/web
- Prensa económica (El País, expansion.com) — artículos con datos agregados
- Informes del Banco de España — datos de vivienda
- **Browser tool** — navegar a la página y extraer datos con `browser_console`

### Paso 2: Definir multiplicadores intra-provincia

Los multiplicadores ajustan el precio base de provincia según:
- **Distrito/municipio específico** — capitales vs suburbios vs pueblos
- **Densidad de población** — áreas densas (+5%), áreas rurales (-10%)
- **Tipo de zona** — turística (+15%), industrial (-5%), residencial (+0%)

Estructura de multiplicadores:
```json
{
  "provincia": {
    "cp": {"rent_mult": 1.15, "sale_mult": 1.10}
  }
}
```

### Paso 3: Calcular precios por CP

```python
rent = base_rent * rent_mult * density_multiplier
sale = base_sale * sale_mult * density_multiplier
ratio = sale / (rent * 12)  # meses para comprar
```

### Ejemplo: Precios base por provincia (2024)

| Provincia | Alquiler (€/m²/mes) | Compra (€/m²) | Tendencia |
|-----------|---------------------|---------------|-----------|
| Madrid | 15.5 | 4500 | subida |
| Barcelona | 14.0 | 4200 | subida |
| Baleares | 13.0 | 3500 | subida |
| Guipúzcoa | 11.0 | 2900 | estable |
| Vizcaya | 11.0 | 2800 | subida |
| Málaga | 9.5 | 2600 | subida |
| Valencia | 10.0 | 2400 | subida |
| Sevilla | 8.5 | 1900 | subida |
| Zaragoza | 8.0 | 1600 | estable |
| Asturias | 7.0 | 1300 | bajada |
| Córdoba | 6.5 | 1100 | bajada |

### Multiplicadores de densidad

```python
def density_multiplier(density):
    if density > 50000: return 1.05
    elif density > 20000: return 1.02
    elif density > 10000: return 1.0
    elif density > 5000: return 0.97
    elif density > 2000: return 0.95
    else: return 0.90
```

## Cuándo NO usar

- Cuando se accede desde un entorno con navegador (no servidor) → usar `browser_navigate` + `browser_console`
- Cuando la fuente es un archivo local o base de datos interna
- Cuando se necesita datos en tiempo real → la estimación es un snapshot

## Fuentes que SÍ funcionan desde servidor

| Fuente | Tipo | Notas |
|--------|------|-------|
| **ADIF (WMS/FeatureServer)** | GIS/WFS | WMS Tramificación muy detallado. FeatureServer LTV con coords en geometry (no attributes). Ver `references/adif-railway-data-sources.md` |
| **IGN (WMTS)** | Tiles | Mapas base y red ferroviaria. Ver skill `ign-wmts-tiles` |
| **Nominatim** | Geocoding | Gratis, 1 req/s. Ver skill `nominatim-geocoding` |
| **Open-Meteo** | Clima | Gratis, sin API key. Ver skill `esios-complete` |

### ArcGIS FeatureServer — Pitfall de coordenadas

Cuando se consulta un FeatureServer de ArcGIS con `outSR=4326`, las coordenadas en los **atributos** (`X`, `Y`) pueden venir **NULL**, pero la **geometría** (`f.geometry.x`, `f.geometry.y`) sí tiene los valores correctos. Siempre usar `f.geometry.x/y` y añadir `returnGeometry=true` al query.

```javascript
// ❌ MAL — attributes X/Y vienen NULL con outSR=4326
const a = f.attributes;
L.marker([a.Y, a.X]);

// ✅ BIEN — geometry siempre tiene las coordenadas
L.marker([f.geometry.y, f.geometry.x]);
```

## Pitfalls

- **No confundir nombre de provincia con código postal** — "Guipúzcoa" ≠ "20xxx", "Vizcaya" ≠ "48xxx"
- **Los multiplicadores son aproximaciones** — no reemplazan datos reales. Marcar siempre como "estimada"
- **Las tendencias cambian** — "subida"/"bajada"/"estable" debe actualizarse periódicamente
- **Cobertura incompleta** — algunos CPs pequeños pueden no tener multiplicadores específicos. Usar 1.0 como fallback
- **Fuente de precios base** — documentar siempre de dónde vienen los precios base (Idealista Q1 2024, etc.)

## Referencias

- `references/spanish-housing-province-prices-2024.md` — Tabla completa de precios base por provincia con fuentes y ratios
- `references/blocked-sources-checklist.md` — Lista detallada de fuentes españolas que bloquean acceso servidor + patrón de detección
- `references/ine-rest-api-working.md` — INE REST API que SÍ funciona (salarios, población) — correción al bloqueo INE
