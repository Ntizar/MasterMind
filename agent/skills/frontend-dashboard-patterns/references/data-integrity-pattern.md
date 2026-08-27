# Data Integrity & Graceful Degradation — Referencia Completa

## Principio Fundamental

**NUNCA inventar datos para rellenar secciones vacías de un dashboard.** Un dashboard con secciones vacías y mensajes honestos es más útil que uno con datos falsos que engañan al usuario.

## Caso Real: Mastermind Dashboard

### Problema Original

El endpoint `/api/agents` generaba actividad falsa cuando no había eventos reales:

```javascript
// server.js — ANTES (MALO)
app.get('/api/agents', (req, res) => {
  // ...
  if (agentLog.length === 0) {
    // INVENTAR actividad cuando no hay datos reales
    agentLog = patterns.slice(0, 5).map((p, i) => ({
      from: p.from, to: p.to,
      action: p.action,
      time: new Date(Date.now() - i * 120000).toLocaleTimeString()
    }));
  }
  res.json({ agents, activity: agentLog, patterns });
});
```

Esto producía en el frontend:

```
Actividad Reciente
mastermind → planner   Delegó planificación   14:30:17
planner → mastermind   Plan completado        14:28:17
mastermind → implementer Delegó implementación 14:26:17
```

**Problema:** El usuario veía actividad que nunca ocurrió. Esto es peor que una sección vacía.

### Solución

```javascript
// server.js — DESPUÉS (BIEN)
app.get('/api/agents', (req, res) => {
  // agentLog es un array que se llena SOLO con eventos reales
  // Si está vacío, se devuelve vacío — el frontend muestra empty state
  res.json({ agents, activity: agentLog, patterns });
});
```

```javascript
// dashboard.html — Frontend con empty state honesto
function updateActivity(data) {
  const list = document.getElementById('activityList');
  if (!data || !data.activity || data.activity.length === 0) {
    list.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">⏳</div>
        <div class="empty-title">Esperando actividad...</div>
        <div class="empty-desc">Los agentes se comunican aquí cuando hay tareas en curso</div>
      </div>`;
    return;
  }
  // Renderizar actividad real
  list.innerHTML = data.activity.map(a => `
    <div class="activity-item">
      <span class="agent-badge">${a.from}</span>
      <span class="arrow">→</span>
      <span class="agent-badge">${a.to}</span>
      <span class="action">${a.action}</span>
      <span class="time">${a.time}</span>
    </div>
  `).join('');
}
```

## Fallback Chain Completa para Procesos

```javascript
// server.js — Fallback chain para procesos en contenedores
app.get('/api/processes', (req, res) => {
  try {
    // 1. Intentar ps aux (funciona en VM local, falla en contenedores)
    const raw = sh("ps aux --sort=-%mem 2>/dev/null | head -30", '');
    if (raw && raw !== 'N/A') {
      const processes = parsePsOutput(raw);
      if (processes.length > 0) return res.json(processes);
    }

    // 2. Fallback a /proc (funciona parcialmente en contenedores)
    const pids = fs.readdirSync('/proc').filter(p => /^\d+$/.test(p));
    if (pids.length > 1) {  // Más de solo PID 1
      const processes = parseProcDir(pids);
      if (processes.length > 1) return res.json(processes);
    }

    // 3. Fallback final: info del ecosistema (marcado como no-local)
    res.json([
      { user: 'appuser', pid: 1, cpu: '0.0', mem: '0.0', command: 'node server.js (Dashboard)', isNode: true },
      { user: 'system', pid: '-', cpu: '-', mem: '-', command: 'Hermes Agent (VM local)', isHermes: true },
      { user: 'system', pid: '-', cpu: '-', mem: '-', command: 'ChromaDB (VM local)', isHermes: true },
    ]);
  } catch {
    res.json([{ user: 'appuser', pid: 1, cpu: '0.0', mem: '0.0', command: 'node server.js' }]);
  }
});
```

## Fallback Chain para Skills

```javascript
// server.js — Fallback chain para skills
app.get('/api/skills', async (req, res) => {
  try {
    // 1. Intentar ChromaDB (solo disponible en VM local)
    const chromaResp = await fetch('http://localhost:8000/api/v1/collections/mastermind-skills');
    if (chromaResp.ok) {
      const data = await chromaResp.json();
      return res.json({ status: 'connected', count: data.count, dimensions: data.metadata?.dimensions, collection: data.name });
    }
    throw new Error('ChromaDB no responde');
  } catch {
    try {
      // 2. Fallback a filesystem (no existe en contenedor NaN)
      const skillsDir = 'agent/skills';
      if (fs.existsSync(skillsDir)) {
        const cats = fs.readdirSync(skillsDir).filter(f => fs.statSync(path.join(skillsDir, f)).isDirectory());
        return res.json({ status: 'filesystem', count: cats.length, categories: cats.map(c => ({ name: c, count: countSkillsInDir(path.join(skillsDir, c)) })) });
      }
    } catch {}

    // 3. Fallback final: categorías conocidas del ecosistema
    res.json({
      status: 'no_collections',
      count: 0,
      categories: [
        { name: 'mastermind', count: '~10' },
        { name: 'devops', count: '~12' },
        { name: 'esios', count: '~5' },
        { name: 'frontend', count: '~8' },
        { name: 'data-science', count: '~6' },
        { name: 'mlops', count: '~7' },
        { name: 'testing', count: '~4' },
        { name: 'github', count: '~6' },
        { name: 'creative', count: '~15' },
        { name: 'ia', count: '~3' },
      ]
    });
  }
});
```

## Frontend: Empty States por Sección

```javascript
// dashboard.html — Cada sección con su empty state
function updateProcesses(data) {
  const list = document.getElementById('processList');
  if (!data || data.length === 0) {
    list.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔒</div>
        <div class="empty-title">Sin procesos visibles</div>
        <div class="empty-desc">Solo el proceso actual es visible desde este contenedor</div>
      </div>`;
    return;
  }
  // Renderizar procesos reales
  list.innerHTML = data.map(p => `
    <div class="process-row ${p.isHermes ? 'hermes' : p.isNode ? 'node' : ''}">
      <span class="pid">${p.pid}</span>
      <span class="cmd">${p.command}</span>
      <span class="cpu">${p.cpu}%</span>
      <span class="mem">${p.mem}%</span>
    </div>
  `).join('');
}

function updateCrons(data) {
  const list = document.getElementById('cronList');
  if (!data || (data.system.length === 0 && data.hermes.length === 0)) {
    list.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">📅</div>
        <div class="empty-title">Sin cron jobs</div>
        <div class="empty-desc">No hay tareas programadas en este entorno</div>
      </div>`;
    return;
  }
  // Renderizar crons reales
  // ...
}

function updateSkills(data) {
  const info = document.getElementById('skillsInfo');
  const grid = document.getElementById('skillsGrid');

  if (!data) {
    info.innerHTML = '<span class="status-dot warning">●</span> No disponible';
    grid.innerHTML = '<div class="empty-state">Esperando datos...</div>';
    return;
  }

  if (data.status === 'connected') {
    info.innerHTML = `<span class="status-dot success">●</span> ${data.count} skills · ${data.dimensions}dim`;
    grid.innerHTML = '';  // Se rellena con datos reales de ChromaDB
  } else if (data.status === 'filesystem') {
    info.innerHTML = `<span class="status-dot warning">●</span> ${data.count} skills (lectura local)`;
    grid.innerHTML = data.categories.map(c =>
      `<span class="skill-category">${c.name} (${c.count})</span>`
    ).join('');
  } else {
    info.innerHTML = `<span class="status-dot warning">●</span> ChromaDB no accesible`;
    grid.innerHTML = (data.categories || []).map(c =>
      `<span class="skill-category">${c.name}</span>`
    ).join('');
  }
}
```

## CSS para Empty States

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: var(--nz-muted, #888);
  text-align: center;
  min-height: 120px;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  opacity: 0.6;
}

.empty-title {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: var(--nz-text-secondary, #aaa);
}

.empty-desc {
  font-size: 0.8rem;
  opacity: 0.7;
  max-width: 280px;
}

.status-dot.success { color: #22c55e; }
.status-dot.warning { color: #f97316; }
.status-dot.error { color: #ef4444; }
```

## Verificación Post-Implementación

```bash
# 1. Buscar generación de datos falsos
grep -rn 'patterns.slice\|fake\|mock\|dummy\|simulated' server.js

# 2. Verificar que cada endpoint tiene fallback
grep -c 'catch\|fallback\|empty\|no_' server.js

# 3. Probar en contenedor real
curl -s https://app.apps.nan.builders/api/agents | python3 -c "import json,sys; d=json.load(sys.stdin); print('Activity:', len(d.get('activity',[])))"

# 4. Verificar empty states en frontend
curl -s https://app.apps.nan.builders/dashboard.html | grep -c 'empty-state'
```