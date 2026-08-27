# ERA — Scraping de Accident Investigation Reports

## Sitio

- **URL base:** `https://www.era.europa.eu`
- **Plataforma:** Drupal (server-side rendered — curl funciona sin JS)
- **Rate limiting:** Agresivo, 429 tras ~50 requests rápidas. Backoff: 30s, 60s, 90s...

## Estructura de navegación

```
era-folder/accident-investigation-reports  (índice de países)
  └── era-folder/investigations             (AT — sin prefijo de país en URL)
  └── era-folder/be-investigations           (BE)
  └── era-folder/bg-investigations           (BG)
  ...                                        (29 países total)
      └── era-folder/2024-13                 (año — sufijo numérico variable)
          └── tabla con enlaces a PDFs
```

### URLs de los 29 países

```python
PAISES_URLS = {
    "AT": f"{BASE_URL}/era-folder/investigations",      # AT sin prefijo
    "BE": f"{BASE_URL}/era-folder/be-investigations",
    "BG": f"{BASE_URL}/era-folder/bg-investigations",
    "CH": f"{BASE_URL}/era-folder/ch-investigations",
    "CZ": f"{BASE_URL}/era-folder/cz-investigations",
    "DE": f"{BASE_URL}/era-folder/de-investigations",
    "DK": f"{BASE_URL}/era-folder/dk-investigations",
    "EE": f"{BASE_URL}/era-folder/ee-investigations",
    "EL": f"{BASE_URL}/era-folder/el-investigations",
    "ES": f"{BASE_URL}/era-folder/es-investigations",
    "FI": f"{BASE_URL}/era-folder/fi-investigations",
    "FR": f"{BASE_URL}/era-folder/fr-investigations",
    "HR": f"{BASE_URL}/era-folder/hr-investigations",
    "HU": f"{BASE_URL}/era-folder/hu-investigations",
    "IE": f"{BASE_URL}/era-folder/ie-investigations",
    "IT": f"{BASE_URL}/era-folder/it-investigations",
    "LT": f"{BASE_URL}/era-folder/lt-investigations",
    "LU": f"{BASE_URL}/era-folder/lu-investigations",
    "LV": f"{BASE_URL}/era-folder/lv-investigations",
    "NL": f"{BASE_URL}/era-folder/nl-investigations",
    "NO": f"{BASE_URL}/era-folder/no-investigations",
    "PL": f"{BASE_URL}/era-folder/pl-investigations",
    "PT": f"{BASE_URL}/era-folder/pt-investigations",
    "RO": f"{BASE_URL}/era-folder/ro-investigations",
    "SE": f"{BASE_URL}/era-folder/se-investigations",
    "SI": f"{BASE_URL}/era-folder/si-investigations",
    "SK": f"{BASE_URL}/era-folder/sk-investigations",
    "Serbia": f"{BASE_URL}/era-folder/serbia-investigations",
    "UK": f"{BASE_URL}/era-folder/uk-investigations",
}
```

## Patrones de URL de PDFs (CRÍTICO)

ERA usa **dos rutas diferentes** para servir PDFs:

- `/sites/default/files/` — Drupal 8+ (PDFs más recientes)
- `/system/files/` — Drupal 7 y migrados (PDFs antiguos)

### Regex que captura AMBOS patrones

```python
# ❌ INCORRECTO — solo captura /sites/default/files/
pdf_links = re.findall(r'href="(/sites/default/files/[^"]*\.pdf)"', html)

# ✅ CORRECTO — captura cualquier path que termine en .pdf
pdf_links = re.findall(r'href="([^"]*\.pdf[^"]*)"', html, re.IGNORECASE)
```

Con el patrón amplio, AT pasó de 4 PDFs (solo recientes) a 185 PDFs (todos los años).

## Patrones de URL de años

Los años tienen sufijos numéricos variables que cambian entre países:

```
/era-folder/2005          (AT — sin sufijo)
/era-folder/2024-13      (AT — con sufijo)
/era-folder/2007-0       (BE — sufijo -0)
/era-folder/2023-2       (CZ — sufijo variable)
```

### Regex para extraer años

```python
year_links = re.findall(r'href="(/era-folder/\d{4}[-\d]*)"', html)
# Limpiar sufijo: "2024-13" → "2024"
año_clean = re.match(r'(\d{4})', año).group(1)
```

## Distribución de PDFs por país (2026-07-08)

| País | PDFs | País | PDFs | País | PDFs |
|------|------|------|------|------|------|
| CZ | 601 | RO | 563 | HU | 508 |
| UK | 375 | DE | 407 | ES | 376 |
| FI | 314 | NO | 170 | AT | 185 |
| PL | 128 | DK | 149 | BE | 111 |
| HR | 111 | FR | 119 | IT | 101 |
| SE | 109 | PT | 61 | BG | 57 |
| IE | 53 | SK | 43 | LV | 24 |
| NL | 22 | EE | 19 | SI | 14 |
| Serbia | 65 | LT | 8 | LU | 5 |
| EL | 4 | CH | 13 | | |

**Total: 4.715 PDFs en 29 países, 429 carpetas de año (2002-2025)**

## Progreso de descarga (2026-07-10)

### Países completados (con marcador `.completado`) — 18 países, PDFs movidos a almacenamiento local

AT (185), BE (111), BG (57), CH (13), CZ (601), DE (407), DK (149), EE (19), EL (4), ES (376), FI (314), FR (119), HR (111), HU (508), IE (53), SE (104/109), SI (14/14), SK (37/43)

Cada país tiene un marcador `Data/PAIS/.completado` para que el script de progreso no los re-descargue.

### Descargados en disco (sin mover aún) — 2026-07-10

| País | Índice | Descargados | Fallidos | Estado |
|------|--------|-------------|----------|--------|
| IT | 101 | 101 | 0 | ✅ Completo |
| NL | 22 | 8 | 0 | ⚠️ Parcial |
| PT | 61 | 61 | 0 | ✅ Completo |
| RO | 563 | 182 | 0 | ⚠️ Parcial |
| SE | 109 | 104 | 5 | ✅ (5 fallidos 2025) |
| SI | 14 | 14 | 0 | ✅ Completo |
| SK | 43 | 37 | 6 | ✅ (6 fallidos) |
| Serbia | 65 | 57 | 8 | ✅ (8 fallidos) |
| UK | 375 | ~306 | ~69 | ⬇️ En curso |

### Pendientes (no iniciados)

LT (8), LU (5), LV (24), NO (170), PL (128)

### Fixes aplicados durante la sesión 2026-07-10

1. **URL de SK corregida:** estaba como `***` (placeholder roto) → cambiada a `sk-investigations`. El script fallaba silenciosamente al scrapear SK.
2. **Lock stale eliminado:** `Data/descarga_activa.lock` tenía PID de un proceso muerto. El script lo detecta pero a veces no limpia correctamente. Fix manual: `rm -f Data/descarga_activa.lock`.
3. **Disk space en `/root` (20G):** UK se paró a los 113 PDFs con `OSError: [Errno 28] No space left on device`. Fix: limpiar caches (`npm cache clean --force`, `rm -rf /root/.npm/_cacache /root/.cache/pip`) liberó 1.8G. Reanudado UK desde donde se quedó (script idempotente — salta PDFs ya descargados).

### Workflow de descarga por país (orden alfabético)

1. Lanzar descarga del país N en background: `python3 script.py --pais XX --delay=1.5 | tee log_XX.txt`
2. Al terminar, lanzar en paralelo:
   - Reintentos país N: `python3 script.py --pais XX --reintentar --delay=2 | tee log_XX_reintentos.txt`
   - Descarga país N+1: `python3 script.py --pais YY --delay=1.5 | tee log_YY.txt`
3. Monitorizar con: `find Data/XX -name "*.pdf" | wc -l` y `tail -15 log_XX.txt`
4. Al mover PDFs a almacenamiento local, crear `Data/PAIS/.completado` para que el cron no re-descargue
5. Repetir hasta completar los 29 países

### Workflow de descarga secuencial (5 países en un script bash)

Para descargar varios países seguidos sin intervención:

```bash
cd /root/workspace/ERAVisor
PAISES="SE SI SK Serbia UK"
for PAIS in $PAISES; do
    echo "🚆 Descargando: $PAIS"
    python3 scripts/descargar_todos_era.py --pais "$PAIS" --delay=1.5 2>&1
    PDFS=$(find "Data/$PAIS" -name '*.pdf' 2>/dev/null | wc -l)
    echo "📊 $PAIS: $PDFS PDFs descargados"
done
```

Lanzar en background con `notify_on_complete=true` para recibir aviso al terminar.

## Script de referencia

`/root/workspace/ERAVisor/scripts/descargar_todos_era.py`

Features:
- Scrapeo incremental con guardado tras cada país
- Resume desde índice previo (`indice_era.json`)
- Dry-run (`--dry-run`) para contar sin descargar
- Filtrar por país (`--pais AT`)
- Reintentar fallidos (`--reintentar`)
- Delay configurable (`--delay=1.5`)
- Estructura: `Data/PAIS/AÑO/archivo.pdf`
- `--reintentar` re-scrapea el país (necesario para refrescar índice tras 429s del scrapeo inicial) y luego solo descarga los archivos que faltan o fallaron
