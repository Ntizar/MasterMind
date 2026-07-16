# AI Prompt Template UI — Demo interactivo de generación IA

## El patrón

Prototipos HTML que muestran cómo un LLM generaría contenido para cada sección de un documento, con:
1. **Panel de datos** — qué datos alimentan el prompt
2. **Prompt box** — el prompt estructurado con syntax highlighting
3. **AI response** — el contenido generado como si el LLM lo hubiera producido

## Caso de uso

- Demostrar a stakeholders cómo funcionaría la generación IA antes de implementar
- Documentar los templates de prompt por capítulo/sección
- Validar que los datos de entrada son suficientes para generar contenido útil

## Arquitectura típica

```
ai-demo.html (autocontenido, ~1000-1200 líneas)
├── Sidebar con navegación por capítulo
├── Panel de arquitectura (flujo visual)
├── Por cada capítulo:
│   ├── Data section (cards con KPIs de ejemplo)
│   ├── Prompt box (dark bg, syntax highlighting)
│   └── AI response (green border, contenido renderizado)
└── Footer con atribución
```

## Prompt Box — syntax highlighting manual

```html
<div class="prompt-box">
<span class="comment">// System prompt para el Resumen Ejecutivo</span>

<span class="keyword">Eres</span> un consultor de movilidad sostenible redactando el Resumen Ejecutivo
de un PMST conforme a la <span class="section">Ley 8/2021 de Movilidad Sostenible</span>.

<span class="keyword">Datos del centro:</span>
- Nombre: <span class="var">{centro.nombre}</span>
- Plantilla: <span class="var">{centro.plantilla}</span> trabajadores

<span class="keyword">Instrucciones:</span>
1. Redacta un resumen de 400-600 palabras
2. Incluye 4-5 KPIs destacados en formato visual
3. Tono: profesional pero accesible para dirección general
</div>
```

```css
.prompt-box {
    background: #111827; color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem; line-height: 1.7;
    position: relative;
}
.prompt-box::before {
    content: 'PROMPT → LLM';
    position: absolute; top: 0; right: 0;
    background: #7c3aed; color: white;
    padding: 4px 12px; font-size: 0.6rem;
}
.prompt-box .var { color: #f97316; font-weight: 600; }
.prompt-box .section { color: #2563eb; }
.prompt-box .comment { color: #6b7280; font-style: italic; }
.prompt-box .keyword { color: #a78bfa; }
```

## AI Response Box — contenido renderizado

```html
<div class="ai-response">
    <div class="ai-response-header">🤖 Respuesta generada por IA — [Nombre]</div>
    <div class="ai-response-body">
        <h4>Sección generada</h4>
        <p>Contenido con <span class="highlight">datos reales</span> insertados...</p>
        <table>...</table>
        <ul>...</ul>
    </div>
</div>
```

```css
.ai-response { border: 2px solid #16a34a; border-radius: 12px; }
.ai-response-header { background: #16a34a; color: white; padding: 10px 16px; }
.ai-response-body { background: white; padding: 20px; }
.ai-response-body .highlight {
    background: linear-gradient(transparent 60%, #fef08a 60%);
    font-weight: 600;
}
.ai-response-body .kpi-inline {
    display: inline-block; background: #dbeafe; color: #1e40af;
    padding: 2px 8px; border-radius: 4px; font-weight: 700;
}
```

## Arquitectura visual — flujo de datos

```html
<div class="arch-flow">
    <div class="arch-box data">📋 Encuestas<br><small>CSV/JSON</small></div>
    <span class="arch-arrow">→</span>
    <div class="arch-box data">🗺️ APIs<br><small>NAP, GBFS, ORS</small></div>
    <span class="arch-arrow">→</span>
    <div class="arch-box process">🔧 Normalización<br><small>appState</small></div>
    <span class="arch-arrow">→</span>
    <div class="arch-box ai">🤖 LLM<br><small>prompt</small></div>
    <span class="arch-arrow">→</span>
    <div class="arch-box output">📄 Capítulo HTML<br><small>22 secciones</small></div>
</div>
```

```css
.arch-box { padding: 14px 18px; border-radius: 10px; text-align: center; min-width: 120px; }
.arch-box.data { background: #dbeafe; border: 2px solid #2563eb; }
.arch-box.process { background: #fff7ed; border: 2px solid #f97316; }
.arch-box.ai { background: #f3e8ff; border: 2px solid #7c3aed; }
.arch-box.output { background: #dcfce7; border: 2px solid #16a34a; }
```

## Integración con plan de generación real

Cuando se implemente la generación IA real:
1. Cada prompt box se convierte en un template literal con `{}`
2. Se inyectan datos reales de `appState`
3. Se envía al LLM (NaN API, OpenAI, etc.)
4. La respuesta se renderiza en el AI response box
5. Se cachea para no regenerar innecesariamente

## Referencia de sesión

- Proyecto: PLANDEMOVILIDAD v2.0
- Archivo: `ai-demo.html` (1181 líneas, 8 capítulos de ejemplo)
- Capítulos demo: Resumen Ejecutivo, Entorno, Encuesta, Carbono, TP, DAFO, Medidas, Conclusiones
