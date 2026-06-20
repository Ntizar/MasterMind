// Patrón reutilizable para IA Chat en dashboards
// Copiar en un archivo JS separado o inline en el HTML

const IA_CHAT_CONFIG = {
  endpoint: '/api/ia/consejo',
  systemPrompt: 'Eres un experto con tono cercano e informal. Das consejos prácticos basados en datos reales.',
  loadingText: '🤔 Pensando...',
};

function initIaChat(config = {}) {
  const cfg = { ...IA_CHAT_CONFIG, ...config };
  
  window.addChatMsg = function(text, type) {
    const chat = document.getElementById('ia-chat');
    if (!chat) return;
    const div = document.createElement('div');
    div.className = 'ia-msg ' + type;
    div.innerHTML = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
  };

  window.sendIaMessage = async function(inputId = 'ia-input') {
    const input = document.getElementById(inputId);
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';
    
    window.addChatMsg(msg, 'user');
    window.addChatMsg(cfg.loadingText, 'ai');
    
    try {
      const res = await fetch(cfg.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensaje: msg })
      });
      const data = await res.json();
      const msgs = document.querySelectorAll('.ia-msg');
      if (msgs.length > 0) {
        msgs[msgs.length - 1].innerHTML = formatIaMessage(data.consejo || data.error || 'Sin respuesta');
      }
    } catch (err) {
      const msgs = document.querySelectorAll('.ia-msg');
      if (msgs.length > 0) {
        msgs[msgs.length - 1].innerHTML = '⚠️ Error de conexión. Intenta de nuevo.';
      }
    }
    
    input.focus();
  };

  window.formatIaMessage = function(text) {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
  };
}

// Uso:
// <div class="ia-chat" id="ia-chat"></div>
// <input id="ia-input" onkeypress="if(event.key==='Enter')sendIaMessage()">
// <button onclick="sendIaMessage()">Enviar</button>
// <script>initIaChat({ endpoint: '/mi-endpoint-ia' });</script>
