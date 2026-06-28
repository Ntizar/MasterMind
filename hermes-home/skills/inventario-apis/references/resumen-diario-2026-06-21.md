# Resumen diario del inventario de APIs — Patrones y lecciones (junio 2026)

## Sesión del 21 de junio de 2026

### Hallazgos clave

1. **Dual-repo divergence crítica**: `/tmp/inventario-apis/` y `/opt/hermes-work/inventario-apis/` son dos repos git separados con estados muy diferentes:
   - `/tmp/`: 285 "procesadas" en estado.json, pero 4048 directorios reales
   - `/opt/hermes-work/`: 3648 "procesadas", 3611 directorios reales
   - Remote GitHub (origin/main): 285 procesadas (refleja `/tmp/`)

2. **`estado.json` tiene `categorias: {}` vacío**: El script dejó de llenar el campo `categorias` en junio 2026. Las métricas globales siguen siendo válidas pero el desglose por categoría está perdido.

3. **45 APIs nuevas hoy (21/06)**: Todas en categoría Agentes IA. Principalmente scrapers (27), herramientas IA (7), integraciones varias.

4. **4003 APIs añadidas ayer (20/06)**: También mayoritariamente en Agentes IA.

5. **Último commit real**: 17 de junio de 2026 — 4 días sin commits en el repo `/opt/hermes-work/`.

### Patrón de conteo fiable

Para generar un resumen diario fiable:
1. Contar directorios reales en ambas ubicaciones (`/tmp/` y `/opt/hermes-work/`)
2. Comparar con `estado.json` en ambas ubicaciones
3. Verificar modificación time de cada directorio para detectar APIs nuevas hoy
4. Usar directorios reales como fuente de verdad primaria (no estado.json)

### Distribución por categoría (real, junio 21)

| Categoría | Directorios | % del total |
|---|---|---|
| Automatización | 2485 | 61,4% |
| IA | 816 | 20,2% |
| Agentes IA | 747 | 18,5% |

### Temas de las APIs nuevas hoy

- 🕷️ Scrapers: 27 (45%) — la mayoría
- 🤖 IA / Asistentes: 7 (16%)
- 📦 Otros: 3
- 📧 Email / Social: 2
- 📅 Google Tools: 2
- 🏠 Inmobiliarias: 1
- 💰 Finanzas: 1
- 🛒 E-commerce: 1
- 🔍 SEO: 1
