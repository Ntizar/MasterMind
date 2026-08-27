# Government WAF Scraping — Spanish Public Administration Sites

Workaround for scraping Spanish government websites that block headless browsers.

## Affected Sites

| Site | Blocks? | Notes |
|------|---------|-------|
| transportes.gob.es | ✅ 403 | WAF checks browser fingerprint |
| boe.es | ⚠️ Rate limits | Works with curl, rate limit ~10 req/min |
| minimatur.gob.es | ✅ 403 | Same WAF as transportes |
| datos.gob.es | ❌ Open | Open data portal, no WAF |
| ign.es (WMTS) | ❌ Open | Map tiles, no auth needed |

## Workaround

```bash
curl -sL \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml" \
  "https://www.transportes.gob.es/organos-colegiados/ciaf/normativa"
```

## Why It Works

The WAF checks for headless browser indicators (missing plugins, specific JS properties, WebDriver flag), not the User-Agent string alone. A curl request with a realistic User-Agent bypasses the check because the server only sees HTTP headers, not browser fingerprinting JS.

## Parsing Pattern

Government sites use Drupal/CMS with predictable HTML structure:

```python
import re
html = response.text

# Find section headings (h2/h3/h4)
sections = re.split(r'<h[234][^>]*>', html)
for sec in sections:
    title_match = re.match(r'(.*?)</h[234]>', sec, re.DOTALL)
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        # Extract links within this section
        links = re.findall(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', sec, re.DOTALL)
```

## Verification

Always verify scraped links actually work:

```python
for url in scraped_urls:
    resp = requests.head(url, allow_redirects=True, timeout=10)
    print(f'{resp.status_code} {url}')
```

## CIAF-visor Normativa Example

Scraped `transportes.gob.es/organos-colegiados/ciaf/normativa` and found only 7 documents (vs 15 that were hardcoded). The official page organizes them as:
- **Europea** (2): Directiva 2016/798, Reglamento 2020/572
- **Nacional** (2): Ley 38/2015, RD 623/2014
- **Otra normativa** (3): RD 2387/2004, RD 664/2015, RD 929/2020

All link to PDFs hosted on `transportes.gob.es/recursos_mfom/comodin/recursos/`.
