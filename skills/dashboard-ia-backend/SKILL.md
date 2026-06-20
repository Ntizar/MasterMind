---
name: dashboard-ia-backend
version: "1.0.0"
description: "Patrón completo para construir dashboards interactivos con backend Express + frontend vanilla JS + asistente IA que lee datos locales. Base: dieta-nan."
tags: [dashboard, backend, express, vanilla-js, ia, chat, api-rest, chartjs]
---

# Dashboard con Backend + IA Interactiva

Patrón para construir productos web con:
- **Backend Express** que lee datos locales (JSON, filesystem) y expone APIs REST
- **Frontend vanilla JS** con Chart.js para gráficos y diseño moderno
- **Asistente IA** que consulta la API de LLM con contexto completo de los datos del usuario

## Arquitectura

```
project/
├── server.js              ← Express backend
├── package.json
├── .gitignore
└── public/
    └── index.html         ← Dashboard autocontenido
```

## Pasos

1. **Crear estructura:** `mkdir -p project/public && cd project && npm init -y`
2. **Instalar deps:** `npm install express cors`
3. **Crear server.js** con:
   - `express.static('public')` para servir frontend
   - APIs REST que leen datos locales
   - Endpoint IA que construye prompt con contexto + llama a LLM
4. **Crear index.html** con:
   - Chart.js desde CDN para gráficos
   - Aurora design system (CDN)
   - Fetch a las APIs del backend
   - Chat IA con burbujas de mensaje
5. **Deploy en NaN Builders:**
   - `npm install`
   - `node server.js`
   - Configurar variable de entorno `NAN_API`

## Patrón de endpoint IA

```javascript
app.post('/api/ia/consejo', async (req, res) => {
  const { mensaje } = req.body;
  
  // 1. Construir contexto del usuario (leer datos locales)
  const db = loadDB();
  const contexto = `
    Usuario: ${db.meta.nombre}, ${db.meta.peso_inicial_kg}kg → ${ultimoPeso.peso_kg}kg
    Objetivo: ${db.meta.peso_objetivo_kg}kg
    TMB: ~${tmb} kcal, TDEE: ~${tdee} kcal
    
    Comidas de hoy:
    ${comidasHoy.map(c => `- ${c.hora}: ${c.descripcion} (${c.kcal} kcal)`).join('\n')}
    
    Pregunta: ${mensaje}
  `;

  // 2. Llamar a API de LLM
  const response = await fetch('https://api.nan.builders/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.NAN_API}`
    },
    body: JSON.stringify({
      model: 'qwen3.6',
      messages: [
        {
          role: 'system',
          content: 'Eres un experto en [tema] con tono cercano e informal. Das consejos prácticos basados en datos reales.'
        },
        { role: 'user', content: contexto }
      ],
      max_tokens: 500,
      temperature: 0.7
    })
  });

  const data = await response.json();
  res.json({ consejo: data.choices?.[0]?.message?.content || 'Error' });
});
```

## Frontend: IA Chat

HTML mínimo para chat:

```html
<div class="ia-chat" id="ia-chat"></div>
<div class="ia-input-row">
  <input type="text" id="ia-input" placeholder="Pregunta..."
         onkeypress="if(event.key==='Enter')sendIA()">
  <button onclick="sendIA()">Enviar</button>
</div>

<script>
function addChatMsg(text, type) {
  const chat = document.getElementById('ia-chat');
  const div = document.createElement('div');
  div.className = 'ia-msg ' + type;
  div.innerHTML = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function sendIA() {
  const input = document.getElementById('ia-input');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';
  
  addChatMsg(msg, 'user');
  addChatMsg('<span class="loading"></span> Pensando...', 'ai');
  
  const res = await fetch('/api/ia/consejo', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mensaje: msg })
  });
  const data = await res.json();
  const msgs = document.querySelectorAll('.ia-msg');
  msgs[msgs.length-1].innerHTML = formatIA(data.consejo);
}

function formatIA(text) {
  return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
             .replace(/\*(.*?)\*/g, '<em>$1</em>')
             .replace(/\n/g, '<br>');
}
</script>
```

## Pitfalls

- **NAN_API como variable de entorno** — no hardcodear la key en el código
- **Contexto del prompt** — incluir TODOS los datos relevantes para que la IA tenga contexto completo
- **Error handling** — siempre tener fallback si la API de LLM falla (mensaje de error claro)
- **Auto-refresh** — usar `setInterval` para refrescar datos cada 60s en dashboards en vivo
- **Comparación visual** — mostrar ✅/❌ cuando se compara contra objetivos (macros, peso, etc.)
- **NUNCA hardcodear datos del usuario en prompts IA** — usar helpers tipo `perfilUsuario(db)` que lean perfil y peso actual de la DB. El peso cambia diario.
- **Chat history keys** — si la BD almacena en español (`rol`, `contenido`) pero el frontend espera inglés (`role`, `content`), hacer alias en el SELECT: `SELECT rol AS role, contenido AS content`. Alternativa: usar siempre el mismo idioma en todo el stack.
- **Chat messages XSS** — al renderizar mensajes del assistant, SIEMPRE aplicar `escapeHtml()` ANTES de `formatMarkdown()`. El LLM puede generar HTML malicioso o el usuario puede inyectar `<script>` en su propio chat.

## Estimación IA automática (patrón reutilizable)

Además del chat IA, se puede usar el LLM para **estimar datos** a partir de descripciones libres. Patrón:

### Flujo
1. Usuario escribe descripción en campo de texto
2. Al `blur` (salir del campo), frontend llama a `/api/estimar-X`
3. Backend lee perfil dinámico de DB → construye prompt con contexto → llama LLM
4. LLM responde JSON estructurado → backend reenvía al frontend
5. Frontend rellena campos automáticamente + badge visual

### Backend (endpoint de estimación)

```javascript
app.post('/api/estimar-comida', async (req, res) => {
  const { descripcion, tipo } = req.body;
  const db = readDB();
  const response = await fetch('https://api.nan.builders/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
    body: JSON.stringify({
      model: 'qwen3.6',
      messages: [
        { role: 'system', content: 'Eres experto. Responde SOLO JSON válido: {"kcal":N,"proteinas_g":N,...}' },
        { role: 'user', content: `PERFIL: ${contextoPerfil(db)}\nDescripción: ${descripcion}` }
      ],
      max_tokens: 100, temperature: 0.3
    })
  });
  const data = await response.json();
  const clean = data.choices[0].message.content.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
  res.json({ estimado: true, ...JSON.parse(clean) });
});
```

**Claves:** temperature baja (0.3), max_tokens corto, JSON estricto, limpiar `<think>` tags de qwen3.

### Frontend (auto-estimación)

```javascript
var _estimando = false;
function estimarComida() {
  var desc = document.getElementById('comidaDesc').value.trim();
  var kcal = parseInt(document.getElementById('comidaKcal').value) || 0;
  if (!desc || desc.length < 3 || _estimando || kcal > 0) return; // skip si manual
  _estimando = true;
  badge.innerHTML = '<span class="ia-badge">🤖 Estimando...</span>';
  fetch('/api/estimar-comida', { method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({descripcion: desc, tipo: document.getElementById('comidaTipo').value}) })
  .then(r => r.json()).then(d => {
    if (d.estimado) {
      document.getElementById('comidaKcal').value = d.kcal;
      document.getElementById('comidaProt').value = d.proteinas_g;
      // ... rellenar más campos
      badge.innerHTML = '<span class="ia-badge ia-badge--ok">✅ IA: ' + d.kcal + ' kcal</span>';
      setTimeout(() => badge.innerHTML = '', 5000);
    }
  }).finally(() => _estimando = false);
}
```

### CSS del badge

```css
.ia-badge { display:inline-flex; align-items:center; gap:4px; font-size:0.7rem;
  padding:2px 8px; border-radius:99px; background:linear-gradient(135deg,#2563eb,#7c3aed);
  color:#fff; font-weight:600; animation:iaPulse 1.5s ease-in-out infinite; }
.ia-badge--ok { background:linear-gradient(135deg,#22c55e,#16a34a); animation:none; }
@keyframes iaPulse { 0%,100%{opacity:1} 50%{opacity:0.6} }
```

## Ejemplos

- `dieta-masterfit` — Dashboard de dieta con IA + estimación automática de kcal
