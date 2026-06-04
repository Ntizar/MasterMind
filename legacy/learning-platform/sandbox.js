/* ============================================================
   SANDBOX — Simulador de OpenCode
   Respuestas predefinidas para tareas comunes
   ============================================================ */

const SANDBOX_RESPONSES = {
  // Escritura / SOPs
  'sop': {
    keywords: ['sop', 'procedimiento', 'proceso', 'instrucciones'],
    response: `
<strong>📋 SOP Generado</strong><br><br>
He creado un SOP completo para tu proceso. Aquí está la estructura:<br><br>
<div class="agent-flow">
  <div class="agent-step">🔀 DELEGANDO A: classifier → Tipo: escritura + operaciones</div>
  <div class="agent-step">🔀 DELEGANDO A: explorer → Leyendo vault en busca de SOPs existentes</div>
  <div class="agent-step">🔀 DELEGANDO A: planner → Diseñando estructura (objetivo, alcance, pasos, responsables)</div>
  <div class="agent-step">🔀 DELEGANDO A: spec-writer → Generando spec con criterios de aceptación</div>
  <div class="agent-step">✅ SPEC aprobada por usuario</div>
  <div class="agent-step">🔀 DELEGANDO A: implementer → Escribiendo SOP en Markdown</div>
  <div class="agent-step">🔀 DELEGANDO A: reviewer → Validando estructura y completitud</div>
  <div class="agent-step">✅ Reviewer PASS — Todos los criterios cumplidos</div>
  <div class="agent-step">🔀 DELEGANDO A: synthesizer → Resumiendo resultado</div>
  <div class="agent-step">🔀 DELEGANDO A: archiver → Guardando learning</div>
</div>
<br>
<strong>Output:</strong> SOP creado en <code>agents/sops/onboarding-clientes.md</code><br>
<strong>Learning:</strong> <code>agents/learnings/2026-03-25-sop-onboarding.md</code><br><br>
<small>💡 Para usar esto en tu vault: Abre OpenCode y pega la misma tarea</small>
    `,
    delay: 3000
  },
  
  // Análisis de datos / CSV
  'csv': {
    keywords: ['csv', 'datos', 'analizar', 'ventas', 'excel', 'dashboard'],
    response: `
<strong>📊 Análisis de Datos Completado</strong><br><br>
He analizado tus datos y generado insights. Flujo ejecutado:<br><br>
<div class="agent-flow">
  <div class="agent-step">🔀 DELEGANDO A: classifier → Tipo: análisis de datos</div>
  <div class="agent-step">🔀 DELEGANDO A: explorer → Leyendo CSV y detectando columnas</div>
  <div class="agent-step">🔀 DELEGANDO A: planner → Diseñando análisis (top productos, tendencias, anomalías)</div>
  <div class="agent-step">🔀 DELEGANDO A: implementer → Ejecutando análisis + creando visualizaciones</div>
  <div class="agent-step">🔀 DELEGANDO A: critic → Validando conclusiones</div>
  <div class="agent-step">✅ Critic PASS — Insights validados</div>
  <div class="agent-step">🔀 DELEGANDO A: synthesizer → Creando resumen ejecutivo</div>
  <div class="agent-step">🔀 DELEGANDO A: archiver → Guardando learning</div>
</div>
<br>
<strong>Output:</strong><br>
• Resumen ejecutivo (1 página)<br>
• Top 5 productos por ingresos<br>
• Gráfico de tendencia mensual<br>
• 3 insights accionables<br><br>
<strong>Archivos:</strong> <code>analisis-ventas-2026-03.md</code>, <code>dashboard.html</code>
    `,
    delay: 3500
  },
  
  // Desarrollo / Landing page
  'landing': {
    keywords: ['landing', 'página', 'web', 'html', 'css', 'responsive'],
    response: `
<strong>💻 Landing Page Creada</strong><br><br>
He generado una landing page completa. Flujo:<br><br>
<div class="agent-flow">
  <div class="agent-step">🔀 DELEGANDO A: classifier → Tipo: software + web</div>
  <div class="agent-step">🔀 DELEGANDO A: explorer → Buscando referencias de diseño</div>
  <div class="agent-step">🔀 DELEGANDO A: planner → Estructura: hero, features, testimonios, pricing, FAQ</div>
  <div class="agent-step">🔀 DELEGANDO A: spec-writer → Spec con requisitos técnicos</div>
  <div class="agent-step">✅ SPEC aprobada</div>
  <div class="agent-step">🔀 DELEGANDO A: implementer → Código HTML+CSS+JS</div>
  <div class="agent-step">🔀 DELEGANDO A: reviewer → Validando responsive, accesibilidad</div>
  <div class="agent-step">✅ Reviewer PASS</div>
  <div class="agent-step">🔀 DELEGANDO A: synthesizer → Instrucciones de deploy</div>
  <div class="agent-step">🔀 DELEGANDO A: archiver → Guardando learning</div>
</div>
<br>
<strong>Output:</strong><br>
• <code>index.html</code> (estructura)<br>
• <code>styles.css</code> (dark mode + responsive)<br>
• <code>script.js</code> (formulario newsletter)<br>
• <code>README.md</code> (instrucciones deploy Netlify)<br><br>
<small>🚀 Deploy: Arrastra la carpeta a Netlify Drop</small>
    `,
    delay: 4000
  },
  
  // Onboarding / Equipos
  'onboarding': {
    keywords: ['onboarding', 'nuevo', 'empleado', 'miembro', 'equipo'],
    response: `
<strong>👥 Plan de Onboarding Generado</strong><br><br>
He creado un plan de onboarding de 2 semanas:<br><br>
<div class="agent-flow">
  <div class="agent-step">🔀 DELEGANDO A: classifier → Tipo: operaciones + gestión de equipos</div>
  <div class="agent-step">🔀 DELEGANDO A: explorer → Leyendo docs existentes del equipo</div>
  <div class="agent-step">🔀 DELEGANDO A: planner → Timeline: día 1, semana 1, semana 2</div>
  <div class="agent-step">🔀 DELEGANDO A: spec-writer → Checklist detallado</div>
  <div class="agent-step">✅ SPEC aprobada</div>
  <div class="agent-step">🔀 DELEGANDO A: implementer → Escribiendo plan completo</div>
  <div class="agent-step">🔀 DELEGANDO A: reviewer → Validando completitud</div>
  <div class="agent-step">✅ Reviewer PASS</div>
  <div class="agent-step">🔀 DELEGANDO A: synthesizer → Resumiendo</div>
  <div class="agent-step">🔀 DELEGANDO A: archiver → Guardando learning</div>
</div>
<br>
<strong>Output:</strong> Plan con:<br>
• Día 1: Setup herramientas (checklist 10 items)<br>
• Semana 1: Reuniones 1:1 (5 reuniones agendadas)<br>
• Semana 2: Primer proyecto pequeño<br>
• Recursos: links a docs, templates, contactos<br><br>
<strong>Archivo:</strong> <code>onboarding-plan.md</code>
    `,
    delay: 3500
  },
  
  // Debuggear código
  'debug': {
    keywords: ['debug', 'error', 'bug', 'falla', 'no funciona'],
    response: `
<strong>🐛 Debugging Completado</strong><br><br>
He identificado y solucionado el error:<br><br>
<div class="agent-flow">
  <div class="agent-step">🔀 DELEGANDO A: classifier → Tipo: software + debugging</div>
  <div class="agent-step">🔀 DELEGANDO A: explorer → Analizando código y logs de error</div>
  <div class="agent-step">🔀 DELEGANDO A: critic → Identificando causa raíz</div>
  <div class="agent-step">🔀 DELEGANDO A: planner → Diseñando fix + tests</div>
  <div class="agent-step">🔀 DELEGANDO A: implementer → Aplicando solución</div>
  <div class="agent-step">🔀 DELEGANDO A: reviewer → Validando fix</div>
  <div class="agent-step">✅ Reviewer PASS — Error solucionado</div>
  <div class="agent-step">🔀 DELEGANDO A: synthesizer → Explicando causa y prevención</div>
</div>
<br>
<strong>Causa raíz:</strong> [Depende del código]<br>
<strong>Solución:</strong> [Fix aplicado]<br>
<strong>Prevención:</strong> Añadir test unitario para este caso<br><br>
<small>💡 Para debuggear código real: pega el código + error en OpenCode</small>
    `,
    delay: 3000
  },
  
  // Escritura / Artículos
  'articulo': {
    keywords: ['artículo', 'blog', 'escribir', 'contenido', 'post'],
    response: `
<strong>✍️ Artículo Generado</strong><br><br>
He escrito un artículo completo:<br><br>
<div class="agent-flow">
  <div class="agent-step">🔀 DELEGANDO A: classifier → Tipo: escritura + contenido</div>
  <div class="agent-step">🔀 DELEGANDO A: explorer → Investigando el tema</div>
  <div class="agent-step">🔀 DELEGANDO A: planner → Estructura: intro, 5 puntos, conclusión</div>
  <div class="agent-step">🔀 DELEGANDO A: implementer → Escribiendo 800 palabras</div>
  <div class="agent-step">🔀 DELEGANDO A: reviewer → Validando tono y claridad</div>
  <div class="agent-step">✅ Reviewer PASS</div>
  <div class="agent-step">🔀 DELEGANDO A: critic → Sugiriendo mejoras</div>
  <div class="agent-step">🔀 DELEGANDO A: synthesizer → Creando título y meta description</div>
</div>
<br>
<strong>Output:</strong><br>
• Artículo completo (800 palabras)<br>
• 3 opciones de título<br>
• Meta description para SEO<br>
• Sugerencias de imágenes<br><br>
<strong>Archivo:</strong> <code>articulo-blog.md</code>
    `,
    delay: 3000
  },
  
  // Default / genérico
  'default': {
    keywords: [],
    response: `
<strong>🔄 Tarea Procesada</strong><br><br>
He procesado tu tarea con el flujo estándar:<br><br>
<div class="agent-flow">
  <div class="agent-step">🔀 DELEGANDO A: classifier → Analizando tipo de tarea</div>
  <div class="agent-step">🔀 DELEGANDO A: explorer → Contexto relevante</div>
  <div class="agent-step">🔀 DELEGANDO A: planner → Diseñando enfoque</div>
  <div class="agent-step">🔀 DELEGANDO A: implementer → Ejecutando</div>
  <div class="agent-step">🔀 DELEGANDO A: reviewer → Validando</div>
  <div class="agent-step">✅ Output generado</div>
</div>
<br>
<strong>💡 Consejo:</strong> Para resultados más precisos, sé específico:<br>
• Tipo de tarea (escritura, código, análisis, etc.)<br>
• Formato esperado (SOP, artículo, dashboard, etc.)<br>
• Restricciones (tiempo, longitud, herramientas)<br><br>
<small>📚 Revisa M7 para ejemplos de tu perfil</small>
    `,
    delay: 2500
  }
};

// ── Chat Logic ───────────────────────────────────────────────

function useExample(text) {
  document.getElementById('chat-input').value = text;
  document.getElementById('chat-input').focus();
}

function sendMessage() {
  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('send-btn');
  const messageText = input.value.trim();
  
  if (!messageText) return;
  
  // Add user message
  addMessage(messageText, 'user');
  input.value = '';
  sendBtn.disabled = true;
  
  // Detect response type
  const responseType = detectResponseType(messageText);
  const response = SANDBOX_RESPONSES[responseType];
  
  // Show typing indicator
  showTypingIndicator();
  
  // Simulate delay
  setTimeout(() => {
    removeTypingIndicator();
    addMessage(response.response, 'system', true);
    sendBtn.disabled = false;
  }, response.delay);
}

function detectResponseType(message) {
  const lower = message.toLowerCase();
  
  for (const [type, data] of Object.entries(SANDBOX_RESPONSES)) {
    if (type === 'default') continue;
    
    if (data.keywords.some(keyword => lower.includes(keyword))) {
      return type;
    }
  }
  
  return 'default';
}

function addMessage(text, type, isHtml = false) {
  const messagesContainer = document.getElementById('chat-messages');
  const avatar = type === 'user' ? '👤' : '🤖';
  
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${type}`;
  messageDiv.innerHTML = `
    <div class="message-avatar">${avatar}</div>
    <div class="message-content">${isHtml ? text : escapeHtml(text)}</div>
  `;
  
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
  const messagesContainer = document.getElementById('chat-messages');
  
  const typingDiv = document.createElement('div');
  typingDiv.className = 'message system';
  typingDiv.id = 'typing-indicator';
  typingDiv.innerHTML = `
    <div class="message-avatar">🤖</div>
    <div class="message-content">
      <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
    </div>
  `;
  
  messagesContainer.appendChild(typingDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
  const typingIndicator = document.getElementById('typing-indicator');
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ── Enter key to send ────────────────────────────────────────

document.getElementById('chat-input').addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// ── Personalization ──────────────────────────────────────────

// Replace {{NAME}} with user's name from localStorage
const savedName = localStorage.getItem('brainacademy_name');
if (savedName) {
  document.title = `Sandbox — ${savedName} Brain`;
  document.querySelectorAll('.sandbox-title').forEach(el => {
    el.innerHTML = el.innerHTML.replace('{{NAME}}', savedName);
  });
}
