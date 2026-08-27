---
name: crawlee-web-scraping
version: "1.0.0"
description: "Crawlee — Librería de web scraping y browser automation de Apify. Soporta Puppeteer, Playwright, Cheerio, JSDOM, HTTP raw. Proxy rotation, anti-bot bypass."
tags: [web-scraping, crawler, crawling, puppeteer, playwright, automation, apify, nodejs, proxy]
---

# Crawlee — Web Scraping y Browser Automation

## Resumen

[Crawlee](https://github.com/apify/crawlee) (⭐25K) de Apify es la librería de web scraping y browser automation más popular para Node.js. Soporta Puppeteer, Playwright, Cheerio, JSDOM y HTTP raw. Proxy rotation y anti-bot bypass incluidos.

**Diferencia clave**: Cubre el scraping end-to-end — desde la request HTTP hasta la extracción de datos, con rotación de proxy y comportamiento human-like por defecto.

## Cuándo usar

- Scraping a gran escala de múltiples sitios
- Automatización de navegadores para sitios dinámicos
- Extracción de datos para AI/LLMs/RAG
- Scraping que requiere proxy rotation y anti-bot
- Descargar archivos (HTML, PDF, JPG, PNG) de sitios web

## Patrón de uso

```bash
npm install crawlee
```

```javascript
// Cheerio — scraping ligero (HTML estático)
import { CheerioCrawler } from 'crawlee';

const crawler = new CheerioCrawler({
  requestHandler: ({ request, $, enqueueLinks }) => {
    const title = $('h1').text();
    const paragraphs = $$('p').map(p => p.text());
    
    // Extraer más páginas
    await enqueueLinks({
      globs: ['https://example.com/*'],
      exclude: ['https://example.com/logout']
    });
    
    console.log(title, paragraphs.length, 'paragraphs');
  },
});

await crawler.run(['https://example.com']);
```

```javascript
// Playwright — scraping de sitios dinámicos (JS renderizado)
import { PlaywrightCrawler } from 'crawlee';

const crawler = new PlaywrightCrawler({
  maxRequestRetries: 3,
  requestHandler: ({ request, page }) => {
    // Esperar a que el JS renderice
    await page.waitForSelector('.dynamic-content');
    const data = await page.$$eval('.item', els => 
      els.map(el => el.textContent)
    );
  },
});

await crawler.run(['https://dynamic-site.com']);
```

```javascript
// Puppeteer — alternativa a Playwright
import { PuppeteerCrawler } from 'crawlee';

const crawler = new PuppeteerCrawler({
  launchOptions: { headless: true },
  requestHandler: async ({ page, request }) => {
    await page.waitForSelector('.content');
    const text = await page.$eval('.content', el => el.textContent);
  },
});
```

## Features clave

| Feature | Descripción |
|---------|-------------|
| Multi-engine | Cheerio, Playwright, Puppeteer, JSDOM, HTTP |
| Proxy rotation | Proxy rotation integrado |
| Human-like | Comportamiento humano por defecto |
| Auto-scaling | Escala automáticamente según recursos |
| Session management | Gestión de sesiones con rotación |
| Proxy config | Soporta proxies HTTP, HTTPS, SOCKS |
| Headful/Headless | Ambos modos soportados |

## Integración con otros skills

- **adaptive-web-scraping**: Alternativa Python (Scrapling) vs Crawlee (Node.js)
- **firecrawl-web-scraping**: Alternativa API-based para scraping
- **marker-pdf-conversion**: Crawlee descarga PDFs → Marker los convierte
- **static-digest-pipeline**: Pipeline de digest estático con Crawlee como fuente

## Pitfalls
- **Rate limiting**: Respetar rate limits. Crawlee no lo hace automáticamente
- **Legal**: Verificar ToS del sitio antes de scrapear
- **Memory**: Páginas grandes consumen memoria. Configurar `maxConcurrency` apropiadamente
- **Playwright vs Puppeteer**: Playwright es más moderno y rápido. Puppeteer solo funciona con Chrome/Chromium

## Referencias
- Docs: https://crawlee.dev
- npm: https://www.npmjs.com/package/@crawlee/core
- Discord: https://discord.gg/jyEM2PRvMU

---

**Hecho con ❤️ por David Antizar**