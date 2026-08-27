# API Mega List - Colección Masiva de APIs

- **URL**: https://github.com/cporter202/API-mega-list
- **Stars**: 5,483
- **Lenguaje**: JavaScript
- **Categoría**: Data / Colecciones / Referencia
- **¿Qué hace?**: La colección más completa de APIs en GitHub con 10,498 APIs listas para usar, organizadas en 18 categorías. Cada API incluye enlace directo a su implementación (principalmente Apify actors). Actualizado diariamente.

## Casos de uso
1. **Descubrir APIs** para cualquier necesidad (scraping, IA, automatización, redes sociales, etc.)
2. **Prototipado rápido** con APIs ya implementadas y listas para usar
3. **Investigación de mercado** para encontrar proveedores de servicios API
4. **Vibe coding** - encontrar APIs para proyectos de desarrollo rápido
5. **Referencia** como catálogo de APIs disponibles

## Categorías del repositorio (18 total)
| Categoría | APIs | Descripción |
|-----------|------|-------------|
| automation-apis | 4,825 | Automatización, scraping, webhooks |
| ai-apis | 1,208 | APIs de inteligencia artificial |
| social-media-apis | 3,268 | Redes sociales (Twitter, Instagram, LinkedIn...) |
| lead-generation-apis | 3,452 | Generación de leads |
| developer-tools-apis | 2,652 | Herramientas para desarrolladores |
| ecommerce-apis | 2,440 | E-commerce, pagos, catálogos |
| other-apis | 1,297 | Miscellaneous |
| real-estate-apis | 851 | Bienes raíces |
| integrations-apis | 890 | Integraciones |
| news-apis | 590 | Noticias y medios |
| seo-tools-apis | 710 | Herramientas SEO |
| jobs-apis | 848 | Empleo y trabajo |
| travel-apis | 397 | Viajes y transporte |
| business-apis | 2 | Negocios |
| mcp-servers-apis | 131 | Servidores MCP |
| agents-apis-697 | 697 | APIs para agentes IA |

## Patrones útiles

### Estructura del repositorio
```
API-mega-list/
├── README.md                    # Catálogo principal con stats
├── ai-apis-1208/
│   └── README.md                # 1,208 APIs de IA
├── automation-apis-4825/
│   └── README.md                # 4,825 APIs de automatización
├── social-media-apis-3268/
│   └── README.md                # 3,268 APIs de redes sociales
├── mcp-servers-apis-131/
│   └── README.md                # 131 servidores MCP
├── agents-apis-697/
│   └── README.md                # 697 APIs para agentes
└── ...                          # +11 categorías más
```

### Cada categoría tiene un README con tabla de APIs
```markdown
| API Name | Description |
|----------|-------------|
| [API Name](url) | Descripción de la API |
```

## Snippets reutilizables

### Buscar APIs específicas por categoría
```bash
# Clonar para referencia offline
git clone https://github.com/cporter202/API-mega-list.git

# Buscar APIs de IA
grep -i "openai\|anthropic\|llm" ai-apis-1208/README.md

# Buscar APIs de scraping
grep -i "scraper\|crawl\|extract" automation-apis-4825/README.md
```

### Integrar con Apify (mayoría de APIs son actors de Apify)
```bash
# Instalar CLI de Apify
npm install apify-client

# Ejecutar un actor de Apify desde código
const Apify = require('apify-client');
const client = new Apify.ApiifyClient({ token: 'YOUR_TOKEN' });

const run = await client.actor('damilo/google-images-scraper').call({
    searchTerm: 'machine learning',
    maxItems: 100
});

const items = await client.dataset(run.defaultDatasetId).listItems();
```

### Monitorear actualizaciones del repositorio
```bash
# Configurar watch para recibir notificaciones
# El repo se actualiza diariamente - verificar nuevas APIs

# O usar la API de GitHub
curl -s "https://api.github.com/repos/cporter202/API-mega-list/commits?per_page=1" | \
    jq '.[0].commit.message'
```

## Cómo integrarlo en proyectos

1. **Referencia rápida**: Guardar como bookmark en el navegador
2. **Clonar para offline**: `git clone` para tener catálogo local
3. **Integrar con scripts**: Usar los enlaces de Apify en scripts de automatización
4. **Descubrimiento**: Revisar semanalmente las nuevas APIs añadidas
5. **MCP Servers**: Revisar la categoría mcp-servers-apis-131 para servidores MCP listos

## Relevancia para Mastermind
- **Catálogo de APIs**: Referencia rápida para encontrar APIs en cualquier momento
- **MCP Servers**: La categoría de servidores MCP es directamente útil para Mastermind
- **Agent APIs**: 697 APIs diseñadas para agentes IA - muy relevante
- **Scraping**: Muchas APIs de scraping listas para usar en automatizaciones

## Notas
- La mayoría de APIs son **Apify actors** - requieren cuenta en Apify
- Algunos actors tienen modelo freemium, otros de pago
- El repo se actualiza diariamente con nuevas APIs
- No es un SDK, es un **catálogo de referencias** con enlaces

- **Fecha de aprendizaje**: 2026-05-26
