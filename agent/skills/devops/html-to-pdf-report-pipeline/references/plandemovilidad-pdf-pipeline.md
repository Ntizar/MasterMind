# PLANDEMOVILIDAD — Casos reales de PDF generation

## Métricas del proyecto

| Métrica | Valor |
|---------|-------|
| Líneas de código | ~22K |
| Módulos JS | 32 |
| Capítulos del informe | 22 |
| Páginas del PDF | 73 |
| Tamaño del PDF | 754KB |
| report.js (generación) | 3938 líneas, 216KB |
| Generación HTML | `generarInformeCompleto()` en browser |
| Rasterización | canvas.toDataURL() + html2canvas |
| Conversión | weasyprint input.html output.pdf |
| Attribution | "Hecho con ❤️ por David Antizar" |

## Arquitectura del pipeline PDF

```
Browser (generarInformeCompleto)
    │
    ├── 22 capítulos HTML generados dinámicamente
    ├── Canvas charts → toDataURL() → <img> embebido
    ├── Leaflet maps → html2canvas → <img> embebido
    └── HTML final ~164KB
           │
           ├── [Opción] base64 chunked transfer
           └── weasyprint input.html output.pdf
                  │
                  ▼
            PDF 73 páginas, 754KB
```

## Casos de estudio: report.js vs ia-generativa.js

### report.js (funcional)
- **Tamaño:** 3938 líneas, 216KB
- **Función:** `generarInformeCompleto(appState)` → HTML string
- **Problema:** Monolítico, difícil de mantener, referencia directa IDs de HTML

### ia-generativa.js (roto)
- **Función:** Genera textos con IA vía API
- **Problema:** `report.js` NUNCA lee los textos generados por la IA
- **Estado:** Desconectado — la IA se ejecuta pero el informe usa texto hardcodeado
- **Lección:** Generar IA sin consumir su output = código muerto

## Seguridad: remover API proxy de repos públicos

**Caso:** `server.mjs` (Node.js proxy) exponía `api.nan.builders/v1` en repo público.

**Problema detectado:**
- El proxy era accesible públicamente vía curl
- Exponía infraestructura interna en el código fuente

**Solución aplicada:**
1. Borrar `server.mjs` del repo
2. En `js/config.js`: eliminar `endpoint: '/api/ai/generate'`
3. En `js/informe.js`: eliminar fetch al proxy, retornar fallback estático
4. En `deploy.sh` y `execute-all-fases.sh`: eliminar referencias a `server.mjs`

**Patrón recomendado:**
- Repo público → sin backend en el código
- API keys → solo en `localStorage` del usuario
- Si necesitas proxy: configurar en CI/CD, NO en el repo

## Rasterización específica de PLANDEMOVILIDAD

### Charts (Chart.js)
- 9+ tipos: doughnut, bar, line, horizontal, polar, scatter, pie
- IDs de canvas referenciados en `graficas.js`
- Rasterización: `canvas.toDataURL('image/png')`
- Importante: ejecutar ANTES de generar el HTML final

### Mapas (Leaflet)
- Isocronas OpenRouteService
- Capas NAP DGT, Overpass, GBFS
- Rasterización: `html2canvas(mapContainer)`
- Importante: mapa debe estar renderizado y visible

### CSS para weasyprint
```css
@page {
    size: A4;
    margin: 25mm 20mm 30mm 20mm;
    @bottom-center {
        content: "PLAN DE MOVILIDAD — Hecho con ❤️ por David Antizar";
        font-size: 8pt;
        color: #666;
    }
    @bottom-right {
        content: counter(page);
        font-size: 8pt;
        color: #666;
    }
}

@media print {
    body { margin: 0; padding: 0; }
    .no-print { display: none !important; }
    .page-break { page-break-before: always; }
    h1, h2, h3, h4 { page-break-after: avoid; }
    table, figure { page-break-inside: avoid; }
}
```

## Verificación post-export

```bash
# Tamaño esperado: >500KB para 60+ págs con imágenes
ls -la output.pdf

# Conteo de páginas
python3 -c "import fitz; print(fitz.open('output.pdf').page_count)"

# Verificar contenido
python3 -c "
import fitz
doc = fitz.open('output.pdf')
for i in range(min(3, doc.page_count)):
    text = doc[i].get_text()[:200]
    print(f'Pág {i+1}: {text[:100]}...')
"
```
