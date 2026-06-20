---
name: nan-builder-ia-integration
category: devops
version: "1.3.0"
description: "Integrar un asistente IA con NaN Builders — patrón probado para apps que consumen la API de NaN (qwen3.6) desde un contenedor Node.js. Incluye manejo del token NAN_API, .env seguro, diseño de IA con personalidad, y errores comunes."
tags: [nan-builders, ia, api, token, docker, nodejs, chat, seguridad]
---

# nan-builder-ia-integration

Integrar un asistente IA con NaN Builders — patrón probado para apps que consumen la API de NaN (qwen3.6) desde un contenedor Node.js.

## Problema crítico

El token `NAN_API` está en el entorno de la sesión de Hermes, **NO** en el contenedor de NaN. El contenedor no hereda variables de entorno del host.

## Solución segura (v1.1 — token nunca en Git)

### 1. Crear `.env` con el token (SOLO LOCAL)

```bash
echo "NAN_API=$NAN_API" > /path/to/app/.env
```

### 2. `.gitignore` debe incluir `.env`

```
.env
```

### 3. Server.js — leer el token

Prioridad de lectura en `server.js`:

```javascript
function getNanToken() {
  // 1) Variable de entorno del dashboard NaN (si se configura)
  if (process.env.NAN_API) return process.env.NAN_API;
  // 2) .env local (copiado en el contenedor por Dockerfile COPY . .)
  try {
    const envPath = path.join(__dirname, '.env');
    const envContent = fs.readFileSync(envPath, 'utf8');
    const match = envContent.match(/^NAN_API=(.+)$/m);
    if (match) return match[1].trim();
  } catch (e) {}
  return '';
}
```

### 4. El `.env` se copia en el contenedor, NO en Git

El Dockerfile hace `COPY . .` — el `.env` se copia en el contenedor porque **no está en `.dockerignore`**. Pero está en `.gitignore`, así que nunca va a Git.

**Deploy:** solo commit del código (sin `.env`). El `.env` se mantiene local y se copia en el contenedor en cada build.

### 5. Llamada a la API de NaN

```javascript
const response = await fetch('https://api.nan.builders/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    model: 'qwen3.6',
    messages: [
      { role: 'system', content: 'Eres un experto en [dominio]...' },
      { role: 'user', content: contexto }
    ],
    max_tokens: 500,
    temperature: 0.7
  })
});
const data = await response.json();
```

### 6. Manejo de errores en frontend

Si la IA falla, mostrar mensaje amigable en vez de `Unexpected token '<'`:

```javascript
if (data.fallback) {
  lastMsg.innerHTML = '⚠️ Configuración IA: ' + data.consejo;
} else {
  lastMsg.innerHTML = formatIA(data.consejo);
}
```

## Checklist de deploy

- [ ] `.env` con `NAN_API=<token>` en el directorio del proyecto (LOCAL SOLO)
- [ ] `.gitignore` incluye `.env`
- [ ] `.dockerignore` NO incluye `.env` (se copia en el contenedor)
- [ ] Server.js lee el token desde `.env` o `process.env`
- [ ] Endpoint de IA con manejo de errores graceful
- [ ] Frontend muestra error amigable si falla la IA
- [ ] **NUNCA** hacer `git add .env` — el token no debe estar en Git

## Diseño de IA con Personalidad (Patrón Amadeo Llados)

Cuando la IA de una app necesita un personaje con reglas de comportamiento, el system prompt debe incluir:

1. **Identidad clara:** nombre, tono, estilo de comunicación
2. **Reglas comportamentales atadas a datos:** "si detectas X en los datos del usuario, responde con Y"
3. **Detección de patrones en los datos:** usar regex o filtros sobre las comidas/actividad para activar respuestas específicas
4. **Límite de tokens:** `max_tokens: 600` para respuestas concisas (no 500 que a veces se cortan)

```javascript
// Ejemplo: detección de alcohol en comidas
const alcoholHoy = comidasHoy.filter(c =>
  /volldamm|cerveza|vino|gintonic|gin|beer|alcohol|copa|botella/i.test(c.descripcion)
);
const kcalAlcohol = alcoholHoy.reduce((s, c) => s + (c.kcal || 0), 0);

// Inyectar en el contexto para que la IA reaccione
${kcalAlcohol > 0 ? `- ⚠️ ALCOHOL detectado: ${kcalAlcohol} kcal en ${alcoholHoy.length} tomas` : ''}
```

**Ver:** `references/ai-persona-pattern.md` para el system prompt completo de Amadeo Llados como ejemplo reutilizable.

## Extracción Estructurada de JSON con IA (Auto-fill de formularios)

Patrón para que la IA estime/rellene campos de un formulario a partir de una descripción libre. Ejemplo real: usuario escribe "pechuga pollo + arroz" → IA estima kcal, proteínas, hidratos, grasas.

### Backend — Endpoint de estimación

```javascript
app.post('/api/estimar-comida', async (req, res) => {
  const { descripcion, tipo } = req.body;
  if (!descripcion) return res.status(400).json({ error: 'Descripción requerida' });
  const token = getNanToken();
  if (!token) return res.json({ estimado: false, error: 'Token no configurado' });

  try {
    const response = await fetch('https://api.nan.builders/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({
        model: 'qwen3.6',
        messages: [
          {
            role: 'system',
            content: `Eres un nutricionista experto. Estima las calorías y macros de una comida.

REGLAS:
1. Responde SOLO con JSON válido, sin texto adicional, sin markdown, sin \`\`\`
2. Usa cantidades realistas para una persona de [perfil del usuario]
3. Si la descripción es vaga, asume porciones estándar
4. El tipo de comida ayuda a dimensionar
5. Siempre redondea a números enteros

Formato exacto:
{"kcal":450,"proteinas_g":35,"hidratos_g":45,"grasas_g":15}`
          },
          { role: 'user', content: `Tipo: ${tipo}\nDescripción: ${descripcion}\nEstima kcal y macros. Responde SOLO el JSON.` }
        ],
        max_tokens: 100,
        temperature: 0.3  // Bajo para consistencia en estimaciones numéricas
      })
    });
    const data = await response.json();
    const content = data.choices?.[0]?.message?.content || '';
    // ⚠️ CRÍTICO: qwen3 envuelve razonamiento en tags <think>...</think>
    const clean = content.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
    const estimado = JSON.parse(clean);
    res.json({ estimado: true, ...estimado });
  } catch (err) {
    res.json({ estimado: false, error: 'No pude estimar: ' + err.message });
  }
});
```

### Frontend — Trigger en blur + guard de override

```javascript
var _estimandoIA = false;
function estimarComida() {
  var desc = document.getElementById('comidaDesc').value.trim();
  var badge = document.getElementById('iaEstimarBadge');
  if (!desc || desc.length < 3 || _estimandoIA) return;

  // Guard: NO sobreescribir si el usuario ya puso valores manuales
  var kcal = parseInt(document.getElementById('comidaKcal').value) || 0;
  if (kcal > 0) return;

  _estimandoIA = true;
  badge.innerHTML = '<span class="ia-badge">🤖 Estimando...</span>';

  fetch('/api/estimar-comida', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ descripcion: desc, tipo: document.getElementById('comidaTipo').value })
  })
  .then(function(r){return r.json();})
  .then(function(d){
    if (d.estimado) {
      document.getElementById('comidaKcal').value = d.kcal || '';
      document.getElementById('comidaProt').value = d.proteinas_g || '';
      document.getElementById('comidaHidr').value = d.hidratos_g || '';
      document.getElementById('comidaGras').value = d.grasas_g || '';
      badge.innerHTML = '<span class="ia-badge ia-badge--ok">✅ IA: ' + d.kcal + ' kcal</span>';
      setTimeout(function(){ badge.innerHTML = ''; }, 5000);
    }
  })
  .finally(function(){ _estimandoIA = false; });
}
```

### Diferencias con el patrón de Chat/Consejo

| Aspecto | Chat/Consejo | Extracción JSON |
|---------|-------------|-----------------|
| `temperature` | 0.7-0.8 (creatividad) | 0.3 (consistencia) |
| `max_tokens` | 500-600 | 100 (respuesta corta) |
| Salida esperada | Texto libre markdown | JSON puro |
| Limpieza needed | Formateo markdown | `<think>` tags de qwen3 |
| Interacción | Click botón → respuesta | Blur/Enter → auto-fill |
| Guard | No aplica | No sobreescribir valores manuales |

### UX — Badge de estado

Badge animado junto al label del campo para feedback visual:
- **Estimando:** badge azul/púrpura con pulsación (`animation: iaPulse`)
- **Estimado:** badge verde "✅ IA: 450 kcal" (desaparece a los 5s)
- **Error:** badge naranja "⚠️ Sin estimación" (desaparece a los 3s)
- Botón "🤖 Estimar" para forzar re-estimación manual

## Pitfalls

- **🔴 qwen3 `<think>` tags en respuesta JSON:** qwen3.6 envuelve su razonamiento interno en tags `<think>...</think>` antes del JSON. Si no se limpian, `JSON.parse()` falla. **Siempre hacer:** `content.replace(/<think>[\s\S]*?<\/think>/g, '').trim()` antes de parsear.
- **🔴 Fechas hardcodeadas en contexto de IA (SILENT FAILURE):** El error más peligroso. Si el contexto de la IA contiene una fecha fija (ej: `c.fecha === '2026-06-10'`), la API responde OK pero con datos stale. El usuario pregunta "¿qué comí hoy?" y la IA responde con datos de hace semanas. **Siempre usar fecha dinámica:**
  ```javascript
  // ❌ FATAL — fecha hardcodeada
  const comidasHoy = db.comidas.filter(c => c.fecha === '2026-06-10');

  // ✅ CORRECTO — fecha dinámica por zona horaria
  function hoy() {
    return new Date().toLocaleDateString('sv-SE', { timeZone: 'Europe/Madrid' });
  }
  const comidasHoy = db.comidas.filter(c => c.fecha === hoy());
  ```
  **Detección:** buscar `=== '2026-` o `=== '2025-` en el código del endpoint de IA. Si hay alguna, es un bug.
- **Token truncado:** `echo "NAN_API=$NAN_API"` funciona, pero verificar longitud (debe ser ~25+ chars)
- **`Unexpected token '<'`:** significa que la API devuelve HTML (error 500) en vez de JSON — casi siempre token inválido o no configurado
- **❌ NUNCA usar `git add -f .env`:** esto pone el token en el historial de Git. Si ya lo hiciste, eliminar con `git filter-branch` o `git reset --soft HEAD~1` + force push (ver `references/token-cleanup.md`)
- **NaN no hereda env vars:** las variables del host NO están disponibles en el contenedor
- **Repo público = token visible:** si el repo es público y el `.env` está en Git, revocar el token inmediatamente
- **Contexto de IA sin fecha dinámica:** la IA responde como si siempre fuera el mismo día. Incluir `hoy()` en el system prompt o en el contexto del usuario.
- **🔴 `.env` literal `${VAR}` en vez del valor real:** al crear el `.env` con `echo "NAN_API=${NAN_API}" > .env`, si el shell no expande la variable (por comillas dobles incorrectas o variable no exportada), el archivo contiene el literal `${NAN_API}` en vez del token. **Siempre verificar:** `head -c 20 .env` — debe empezar con `NAN_API=sk-...`, NO con `NAN_API=${`. Si contiene el literal, regenerar con: `source /hermes-home/.env && echo "NAN_API=$NAN_API" > .env`.
- **🔴 `package.json` sin `"type": "module"` + server.js con `import` = crash silencioso:** Si el server.js usa ESM (`import`) pero `package.json` no tiene `"type": "module"`, Node ejecuta como CommonJS y crash al importar. **Siempre añadir `"type": "module"`** cuando el server usa ESM.
- **🔴 `pdf-parse` no tiene default export en ESM:** `import pdfParse from 'pdf-parse'` falla con `SyntaxError: The requested module 'pdf-parse' does not provide an export named 'default'`. **Fix:** usar `createRequire`: `import { createRequire } from 'module'; const require = createRequire(import.meta.url); const pdfParse = require('pdf-parse');`
- **🔴 Regex con `` (caracter especial) en template literal:** `new RegExp('<think>[\\s\\S]*?</think>', 'g')` dentro de un template literal puede causar `SyntaxError: Invalid regular expression flags`. **Fix:** definir el regex con `new RegExp()` fuera del template literal, escapando correctamente los caracteres especiales.

## Referencias

- `references/token-cleanup.md` — Cómo eliminar un token accidentalmente subido a Git
- `references/ai-persona-pattern.md` — System prompt completo de Amadeo Llados como ejemplo reutilizable de IA con personalidad + patrones de detección en datos de usuario
- `references/esm-nan-deploy-pitfalls.md` — Pitfalls ESM + NaN: type:module, regex especiales, pdf-parse, .env en .dockerignore
