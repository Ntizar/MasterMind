/* ============================================================
   BRAIN ACADEMY — Platform Engine v3.0
   Disruptive, gamified, premium learning experience
   ============================================================ */

(function () {
  'use strict';

  const STATE = {
    userName: '',
    userProfile: null,
    profileId: null,
    currentModule: 0,
    totalModules: 6,
    completedModules: new Set(),
    quizAnswers: {},
    quizResults: {},
    totalQuestions: 0,
    correctAnswers: 0,
    timerSeconds: 5400,
    timerInterval: null,
    modules: null,
    profiles: null,
    xp: 0,
    level: 1,
    badges: [],
    startTime: null,
  };

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => document.querySelectorAll(sel);

  // Configure mermaid if loaded
  if (window.mermaid) {
    mermaid.initialize({ startOnLoad: false, theme: 'dark', themeVariables: { primaryColor: '#3b82f6', secondaryColor: '#f97316' } });
  }

  // ── Init ───────────────────────────────────────────────────
  async function init() {
    console.log('%c Brain Academy v3.0 ', 'background:#3b82f6;color:#fff;padding:4px 8px;border-radius:4px;font-weight:bold;');

    // Clear old v1/v2 state
    if (localStorage.getItem('brainacademy_state')) {
      localStorage.removeItem('brainacademy_state');
    }

    initFinishModal();

    // Try to restore a saved session
    const restored = await loadState();
    if (restored) return;

    // No saved state — show onboarding
    const onbName = $('#onb-name');
    const onbStart = $('#onb-start');
    if (!onbName || !onbStart) return;

    const savedName = localStorage.getItem('brainacademy_name');
    if (savedName) {
      onbName.value = savedName;
      onbStart.disabled = false;
    }

    onbName.addEventListener('input', () => {
      onbStart.disabled = onbName.value.trim().length === 0;
    });

    onbStart.addEventListener('click', () => {
      const name = onbName.value.trim();
      if (!name) return;
      STATE.userName = name;
      localStorage.setItem('brainacademy_name', name);
      showProfileSelection();
    });

    onbName.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !onbStart.disabled) onbStart.click();
    });
  }

  // ── Profile Selection ──────────────────────────────────────
  async function showProfileSelection() {
    try {
      const resp = await fetch('profiles.json');
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      STATE.profiles = await resp.json();
    } catch (err) {
      console.error('Error loading profiles:', err);
      return;
    }

    const container = $('#screen-onboarding .container');
    if (!container) return;

    container.innerHTML = `
      <div class="text-center animate-fade-up">
        <div class="navbar-brand-dot" style="width:14px;height:14px;margin:0 auto 1.5rem;"></div>
        <h1 class="hero-title">
          <span class="text-gradient">Hola, ${esc(STATE.userName)}</span>
        </h1>
        <p style="color:var(--text-secondary);font-size:var(--text-lg);margin-top:1rem;max-width:560px;margin-left:auto;margin-right:auto;">
          Elige como quieres hacer el recorrido. El contenido se adapta a tu nivel.
        </p>
      </div>

      <div class="profile-grid">
        ${renderProfiles()}
      </div>
    `;
  }

  function renderProfiles() {
    if (!STATE.profiles || !STATE.profiles.profiles) return '';

    return Object.values(STATE.profiles.profiles).map(profile => {
      const color = profile.color || 'blue';
      const iconMap = { terminal: '>&_', rocket: '>>>' };
      const icon = iconMap[profile.icono] || profile.icono;

      return `
        <div class="profile-card ${color} animate-fade-up" onclick="selectProfile('${profile.id}')">
          <div class="profile-icon-wrap">${icon}</div>
          <h3>${profile.nombre}</h3>
          <div class="profile-subtitle">${profile.subtitulo || ''}</div>
          <p class="profile-desc">${profile.descripcion}</p>
          <div class="profile-duration">${profile.duracion_total}</div>
        </div>
      `;
    }).join('');
  }

  window.selectProfile = function(profileId) {
    STATE.userProfile = STATE.profiles.profiles[profileId];
    STATE.profileId = profileId;
    STATE.timerSeconds = STATE.userProfile.timer_seconds || 5400;
    STATE.startTime = Date.now();
    localStorage.setItem('brainacademy_profile', profileId);

    $$('.screen').forEach(s => s.classList.remove('active'));
    $('#screen-learning').classList.add('active');

    loadModules();
  };

  // ── Module loading ─────────────────────────────────────────
  async function loadModules() {
    try {
      const resp = await fetch('modules-v2.json');
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      STATE.modules = await resp.json();
      initLearningScreen();
    } catch (err) {
      console.error('Error loading modules:', err);
      $('#module-content').innerHTML = '<div class="lesson"><h3>Error</h3><p>' + err.message + '</p></div>';
    }
  }

  function initLearningScreen() {
    $('#nav-system-name').textContent = STATE.userName + ' Academy';
    initTabs();
    startTimer();
    navigateToModule(STATE.currentModule || 0);
    updateProgress();
  }

  // ── Tabs ───────────────────────────────────────────────────
  function initTabs() {
    $('#module-tabs').addEventListener('click', (e) => {
      const tab = e.target.closest('.mtab');
      if (!tab) return;
      navigateToModule(parseInt(tab.dataset.mod, 10));
    });
  }

  function updateTabStates() {
    $$('.mtab').forEach(tab => {
      const mod = parseInt(tab.dataset.mod, 10);
      tab.classList.toggle('active', mod === STATE.currentModule);
      tab.classList.toggle('completed', STATE.completedModules.has(mod));
    });
  }

  // ── Module rendering ───────────────────────────────────────
  function navigateToModule(modIndex) {
    STATE.currentModule = modIndex;
    const modData = STATE.modules['mod' + modIndex];

    if (!modData) {
      $('#module-content').innerHTML = '<div class="lesson"><h3>Modulo no encontrado</h3></div>';
      return;
    }

    let html = personalize(modData.content);

    // Add quiz if exists
    if (modData.quiz && modData.quiz.questions) {
      html += renderQuiz(modData.quiz, modIndex);
    }

    $('#module-content').innerHTML = html;

    // Smooth scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    bindNavButtons();
    bindQuizInteractions();
    restoreQuizState(modIndex);
    updateTabStates();
    updateProgress();
    saveState();

    // Initialize mermaid diagrams if any exist in this module
    if (window.mermaid && document.querySelector('.mermaid')) {
      try { mermaid.run({ querySelector: '.mermaid' }); } catch (e) { /* ignore */ }
    }
  }

  // ── Quiz rendering ─────────────────────────────────────────
  function renderQuiz(quiz, modIndex) {
    let html = `<div class="quiz-block"><h4>Quiz — Modulo ${modIndex}</h4>`;

    quiz.questions.forEach((q, qi) => {
      html += `<div class="quiz-question" data-qid="${q.id}">
        <p>${qi + 1}. ${q.text}</p>`;

      q.options.forEach(opt => {
        html += `<label class="quiz-option" data-qid="${q.id}" data-value="${opt.value}">
          <input type="radio" name="${q.id}" value="${opt.value}">
          <span>${opt.text}</span>
        </label>`;
      });

      html += `<div class="quiz-feedback" id="feedback-${q.id}"></div></div>`;
    });

    html += `<button class="btn btn-accent btn-lg" id="quiz-submit-${modIndex}" style="margin-top:1rem;width:100%;">
      Comprobar respuestas
    </button></div>`;

    return html;
  }

  function bindQuizInteractions() {
    // Option selection
    $$('.quiz-option').forEach(opt => {
      opt.addEventListener('click', () => {
        const qid = opt.dataset.qid;
        const value = opt.dataset.value;

        // If already answered, skip
        if (STATE.quizResults[qid] !== undefined) return;

        // Store answer
        STATE.quizAnswers[qid] = value;

        // Visual selection
        $$(`.quiz-option[data-qid="${qid}"]`).forEach(o => {
          o.classList.remove('selected');
          o.style.borderColor = '';
        });
        opt.classList.add('selected');
        opt.style.borderColor = 'rgba(59,130,246,0.5)';
      });
    });

    // Submit buttons
    const modIndex = STATE.currentModule;
    const submitBtn = $(`#quiz-submit-${modIndex}`);
    if (submitBtn) {
      submitBtn.addEventListener('click', () => submitQuiz(modIndex));
    }
  }

  function submitQuiz(modIndex) {
    const modData = STATE.modules['mod' + modIndex];
    if (!modData || !modData.quiz) return;

    let newCorrect = 0;
    let newTotal = 0;

    modData.quiz.questions.forEach(q => {
      // Skip already graded
      if (STATE.quizResults[q.id] !== undefined) return;

      const answer = STATE.quizAnswers[q.id];
      if (!answer) return;

      newTotal++;
      const isCorrect = answer === q.correct;
      STATE.quizResults[q.id] = isCorrect;

      if (isCorrect) {
        newCorrect++;
        awardXP(25);
      }

      // Visual feedback
      $$(`.quiz-option[data-qid="${q.id}"]`).forEach(opt => {
        opt.classList.add('disabled');
        if (opt.dataset.value === q.correct) {
          opt.classList.add('correct');
        } else if (opt.dataset.value === answer && !isCorrect) {
          opt.classList.add('incorrect');
        }
      });

      // Feedback text
      const fb = $(`#feedback-${q.id}`);
      if (fb) {
        fb.className = 'quiz-feedback show ' + (isCorrect ? 'correct' : 'incorrect');
        fb.textContent = isCorrect ? q.feedback : 'Incorrecto. ' + q.feedback;
      }
    });

    STATE.totalQuestions += newTotal;
    STATE.correctAnswers += newCorrect;

    // Update nav score
    const navScore = $('#nav-score');
    if (navScore) navScore.textContent = STATE.correctAnswers + '/' + STATE.totalQuestions;

    // Disable submit
    const btn = $(`#quiz-submit-${modIndex}`);
    if (btn) {
      btn.disabled = true;
      btn.textContent = newCorrect + '/' + newTotal + ' correctas';
      btn.style.opacity = '0.6';
    }

    saveState();
    checkBadges();
  }

  function restoreQuizState(modIndex) {
    const modData = STATE.modules['mod' + modIndex];
    if (!modData || !modData.quiz) return;

    modData.quiz.questions.forEach(q => {
      if (STATE.quizResults[q.id] !== undefined) {
        const answer = STATE.quizAnswers[q.id];
        const isCorrect = STATE.quizResults[q.id];

        $$(`.quiz-option[data-qid="${q.id}"]`).forEach(opt => {
          opt.classList.add('disabled');
          if (opt.dataset.value === q.correct) opt.classList.add('correct');
          else if (opt.dataset.value === answer && !isCorrect) opt.classList.add('incorrect');
        });

        const fb = $(`#feedback-${q.id}`);
        if (fb) {
          fb.className = 'quiz-feedback show ' + (isCorrect ? 'correct' : 'incorrect');
          fb.textContent = isCorrect ? q.feedback : 'Incorrecto. ' + q.feedback;
        }
      }
    });
  }

  // ── Personalization ────────────────────────────────────────
  function personalize(html) {
    const name = STATE.userName || 'Usuario';
    const profile = STATE.userProfile || {
      nombre: 'Usuario',
      descripcion: '',
      duracion_total: '~2h',
      duracion_modulos: {},
      ejemplos_dominio: [],
      casos_uso: []
    };

    const r = (ph, val) => {
      if (val === undefined || val === null) return;
      html = html.split(ph).join(val);
    };

    r('{{NAME}}', '<span class="user-name">' + esc(name) + '</span>');
    r('{{DURACION_TOTAL}}', profile.duracion_total || '~2h');

    const d = profile.duracion_modulos || {};
    r('{{DURACION_M1}}', d.M1 || '~20 min');
    r('{{DURACION_M2}}', d.M2 || '~25 min');
    r('{{DURACION_M3}}', d.M3 || '~20 min');
    r('{{DURACION_M4}}', d.M4 || '~25 min');
    r('{{DURACION_M5}}', d.M5 || '~25 min');

    r('{{PERFIL_NOMBRE}}', profile.nombre || 'Usuario');
    r('{{PERFIL_DESCRIPCION}}', profile.descripcion || '');

    if (profile.ejemplos_dominio) {
      r('{{EJEMPLOS_DOMINIO}}', profile.ejemplos_dominio.slice(0, 3).map(cap).join(', '));
      r('{{EJEMPLO_RELEVANTE_1}}', cap(profile.ejemplos_dominio[0] || 'un dashboard'));
      r('{{EJEMPLO_RELEVANTE_2}}', cap(profile.ejemplos_dominio[1] || 'un documento'));
      r('{{EJEMPLO_RELEVANTE_3}}', cap(profile.ejemplos_dominio[2] || 'un plan'));
    }

    if (profile.casos_uso) {
      r('{{CASOS_USO}}', profile.casos_uso.slice(0, 3).join(', '));
      r('{{CASOS_USO_LIST}}', profile.casos_uso.slice(0, 4).map(c => '<li>' + c + '</li>').join(''));
      r('{{EJEMPLO_TAREA_PERFIL}}', profile.casos_uso[0] || 'una tarea de ejemplo');
    }

    return html;
  }

  function esc(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function cap(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  // ── Navigation ─────────────────────────────────────────────
  function bindNavButtons() {
    $$('#module-content [data-next]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const nextIndex = parseInt(btn.dataset.next.replace('mod', ''), 10);
        STATE.completedModules.add(STATE.currentModule);
        awardXP(50);
        navigateToModule(nextIndex);
      });
    });

    $$('#module-content [data-prev]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const prevIndex = parseInt(btn.dataset.prev.replace('mod', ''), 10);
        navigateToModule(prevIndex);
      });
    });

    const finishBtn = $('#module-content #finish-btn');
    if (finishBtn) {
      finishBtn.addEventListener('click', (e) => {
        e.preventDefault();
        STATE.completedModules.add(STATE.currentModule);
        awardXP(200);
        updateProgress();
        showFinishModal();
        launchConfetti();
      });
    }
  }

  // ── Progress ───────────────────────────────────────────────
  function updateProgress() {
    const completed = STATE.completedModules.size;
    const total = STATE.totalModules;
    const pct = Math.round((completed / total) * 100);

    const bar = $('#progress-bar');
    const label = $('#progress-label-text');
    const pctLabel = $('#progress-label-pct');
    const navProg = $('#nav-progress');
    const navScore = $('#nav-score');

    if (bar) bar.style.width = pct + '%';
    if (label) label.textContent = 'Modulo ' + STATE.currentModule + ' de ' + (total - 1);
    if (pctLabel) pctLabel.textContent = pct + '%';
    if (navProg) navProg.textContent = pct + '%';
    if (navScore) navScore.textContent = STATE.correctAnswers + '/' + STATE.totalQuestions;
  }

  // ── Timer ──────────────────────────────────────────────────
  function startTimer() {
    const timerEl = $('#nav-timer');
    if (!timerEl) return;

    const update = () => {
      const h = Math.floor(STATE.timerSeconds / 3600);
      const m = Math.floor((STATE.timerSeconds % 3600) / 60);
      const s = STATE.timerSeconds % 60;
      timerEl.textContent = pad(h) + ':' + pad(m) + ':' + pad(s);
    };

    update();
    STATE.timerInterval = setInterval(() => {
      if (STATE.timerSeconds > 0) {
        STATE.timerSeconds--;
        update();
      } else {
        clearInterval(STATE.timerInterval);
      }
    }, 1000);
  }

  function pad(n) { return String(n).padStart(2, '0'); }

  // ── Gamification ───────────────────────────────────────────
  const BADGES = [
    { id: 'first_module', name: 'Primera Mision', icon: '\u{1F3C1}', desc: 'Completar M0', check: (s) => s.completedModules.has(0) },
    { id: 'architect', name: 'Arquitecto', icon: '\u{1F3D7}\uFE0F', desc: 'Completar M1', check: (s) => s.completedModules.has(1) },
    { id: 'agent_tamer', name: 'Domador de Agentes', icon: '\u{1F916}', desc: 'Completar M2', check: (s) => s.completedModules.has(2) },
    { id: 'memory_master', name: 'Maestro de Memoria', icon: '\u{1F9E0}', desc: 'Completar M3', check: (s) => s.completedModules.has(3) },
    { id: 'installer', name: 'Setup Completo', icon: '\u{1F527}', desc: 'Completar M4', check: (s) => s.completedModules.has(4) },
    { id: 'sharpshooter', name: 'Francotirador', icon: '\u{1F3AF}', desc: '80%+ en quizzes', check: (s) => s.totalQuestions >= 5 && (s.correctAnswers / s.totalQuestions) >= 0.8 },
    { id: 'fast_learner', name: 'Rapido y Furioso', icon: '\u26A1', desc: 'Completar en <60% del tiempo', check: (s) => {
      if (s.completedModules.size < 6 || !s.startTime) return false;
      const elapsed = (Date.now() - s.startTime) / 1000;
      const totalTime = s.userProfile?.timer_seconds || 5400;
      return elapsed < totalTime * 0.6;
    }},
    { id: 'graduate', name: 'Graduado', icon: '\u{1F393}', desc: 'Completar todos los modulos', check: (s) => s.completedModules.size >= 6 },
    { id: 'perfectionist', name: 'Perfeccionista', icon: '\u{1F48E}', desc: '100% en quizzes', check: (s) => s.totalQuestions >= 10 && s.correctAnswers === s.totalQuestions },
  ];

  function awardXP(amount) {
    STATE.xp += amount;
    const oldLevel = STATE.level;
    STATE.level = Math.floor(STATE.xp / 200) + 1;

    showXPNotification('+' + amount + ' XP');

    if (STATE.level > oldLevel) {
      setTimeout(() => showXPNotification('Nivel ' + STATE.level + '!'), 800);
    }

    checkBadges();
    saveState();
  }

  function showXPNotification(text) {
    const notif = document.createElement('div');
    notif.className = 'xp-notification';
    notif.textContent = text;
    document.body.appendChild(notif);
    setTimeout(() => notif.remove(), 2200);
  }

  function checkBadges() {
    if (!STATE.badges) STATE.badges = [];

    BADGES.forEach(badge => {
      if (!STATE.badges.includes(badge.id) && badge.check(STATE)) {
        STATE.badges.push(badge.id);
        showBadgeNotification(badge);
      }
    });
  }

  function showBadgeNotification(badge) {
    const notif = document.createElement('div');
    notif.className = 'badge-notification';
    notif.innerHTML = `
      <div class="badge-notification-icon">${badge.icon}</div>
      <div class="badge-notification-title">${badge.name}</div>
      <div class="badge-notification-desc">${badge.desc}</div>
    `;
    document.body.appendChild(notif);
    setTimeout(() => notif.remove(), 3200);
  }

  // ── Confetti ───────────────────────────────────────────────
  function launchConfetti() {
    const container = document.createElement('div');
    container.className = 'confetti-container';
    document.body.appendChild(container);

    const colors = ['#3b82f6', '#f97316', '#22c55e', '#a855f7', '#eab308', '#ec4899'];

    for (let i = 0; i < 80; i++) {
      const piece = document.createElement('div');
      piece.className = 'confetti-piece';
      piece.style.left = Math.random() * 100 + '%';
      piece.style.background = colors[Math.floor(Math.random() * colors.length)];
      piece.style.width = (Math.random() * 8 + 4) + 'px';
      piece.style.height = (Math.random() * 8 + 4) + 'px';
      piece.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
      piece.style.animationDuration = (Math.random() * 2 + 2) + 's';
      piece.style.animationDelay = (Math.random() * 0.5) + 's';
      container.appendChild(piece);
    }

    setTimeout(() => container.remove(), 4000);
  }

  // ── Finish Modal ───────────────────────────────────────────
  function showFinishModal() {
    const completed = STATE.completedModules.size;
    const total = STATE.totalModules;
    const elapsed = STATE.startTime ? Math.floor((Date.now() - STATE.startTime) / 60000) : 0;
    const badges = STATE.badges || [];

    $('#finish-title').textContent = 'Felicidades, ' + STATE.userName + '!';

    let badgesHtml = '';
    if (badges.length > 0) {
      badgesHtml = `<div style="margin:1.25rem 0;padding:1.25rem;background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.2);border-radius:16px;">
        <h4 style="margin-bottom:0.75rem;font-size:var(--text-sm);color:var(--blue-300);">Badges (${badges.length}/${BADGES.length})</h4>
        <div style="display:flex;flex-wrap:wrap;gap:1rem;">
          ${badges.map(id => {
            const b = BADGES.find(x => x.id === id);
            return b ? `<div style="text-align:center;" title="${b.name}: ${b.desc}">
              <span style="font-size:2rem;display:block;">${b.icon}</span>
              <small style="color:var(--text-muted);font-size:0.65rem;">${b.name}</small>
            </div>` : '';
          }).join('')}
        </div>
      </div>`;
    }

    const stats = [
      { value: STATE.correctAnswers + '/' + STATE.totalQuestions, label: 'Aciertos', color: 'var(--blue-400)' },
      { value: Math.round((completed / total) * 100) + '%', label: 'Progreso', color: 'var(--orange-400)' },
      { value: STATE.xp, label: 'XP', color: '#86efac' },
      { value: 'N' + STATE.level, label: 'Nivel', color: '#c4b5fd' },
    ];

    $('#finish-body').innerHTML = `
      <div style="text-align:center;margin-bottom:1.5rem;">
        <div style="font-size:3rem;margin-bottom:0.75rem;">&#x1F389;</div>
        <p style="font-size:var(--text-xl);color:var(--text-primary);margin-bottom:0.5rem;">
          <strong>${completed}/${total} modulos</strong> completados
        </p>
        <p style="color:var(--text-secondary);font-size:var(--text-sm);">en <strong>${elapsed} minutos</strong></p>
        <p style="color:var(--blue-300);font-size:var(--text-xs);margin-top:0.5rem;">Perfil: ${STATE.userProfile?.nombre || 'No seleccionado'}</p>
      </div>
      ${badgesHtml}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;margin-bottom:1rem;">
        ${stats.map(s => `
          <div style="padding:1rem;text-align:center;background:var(--glass-bg-subtle);border:1px solid var(--border-subtle);border-radius:12px;">
            <div style="font-size:var(--text-2xl);font-weight:900;color:${s.color};margin-bottom:0.25rem;">${s.value}</div>
            <small style="color:var(--text-muted);font-size:var(--text-xs);text-transform:uppercase;letter-spacing:0.5px;">${s.label}</small>
          </div>
        `).join('')}
      </div>
    `;

    $('#finish-overlay').style.display = 'flex';
  }

  function initFinishModal() {
    const overlay = $('#finish-overlay');
    const close = $('#finish-close');
    const restart = $('#finish-restart');
    const exportBtn = $('#finish-export');

    if (close) close.addEventListener('click', () => overlay.style.display = 'none');
    if (overlay) overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.style.display = 'none'; });

    if (restart) restart.addEventListener('click', () => {
      STATE.completedModules.clear();
      STATE.quizAnswers = {};
      STATE.quizResults = {};
      STATE.correctAnswers = 0;
      STATE.totalQuestions = 0;
      STATE.currentModule = 0;
      STATE.xp = 0;
      STATE.level = 1;
      STATE.badges = [];
      STATE.startTime = Date.now();
      STATE.timerSeconds = STATE.userProfile?.timer_seconds || 5400;
      localStorage.removeItem('brainacademy_state_v3');
      overlay.style.display = 'none';
      navigateToModule(0);
      startTimer();
    });

    if (exportBtn) exportBtn.addEventListener('click', generatePDF);
  }

  // ── PDF Generation (Ntizar Design) ────────────────────────
  function generatePDF() {
    if (!window.jspdf) {
      showXPNotification('Cargando PDF...');
      setTimeout(generatePDF, 1500);
      return;
    }

    try {
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();

      const name = STATE.userName || 'Usuario';
      const profile = STATE.userProfile?.nombre || 'No seleccionado';
      const date = new Date().toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });
      const elapsed = STATE.startTime ? Math.floor((Date.now() - STATE.startTime) / 60000) : 0;

      // ─── Page 1: Cover ───
      // Background
      doc.setFillColor(7, 11, 18);
      doc.rect(0, 0, 210, 297, 'F');

      // Blue gradient accent bar
      doc.setFillColor(59, 130, 246);
      doc.rect(0, 0, 210, 4, 'F');

      // Decorative circles
      doc.setFillColor(59, 130, 246);
      doc.setGState(new doc.GState({ opacity: 0.08 }));
      doc.circle(30, 60, 80, 'F');
      doc.setFillColor(249, 115, 22);
      doc.circle(180, 220, 60, 'F');
      doc.setGState(new doc.GState({ opacity: 1 }));

      // Small brand dot
      doc.setFillColor(59, 130, 246);
      doc.circle(105, 55, 4, 'F');
      doc.setFillColor(249, 115, 22);
      doc.circle(107, 55, 4, 'F');

      // Title
      doc.setTextColor(240, 244, 255);
      doc.setFontSize(36);
      doc.setFont('helvetica', 'bold');
      doc.text(name, 105, 85, { align: 'center' });

      doc.setFontSize(16);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(148, 163, 184);
      doc.text('Brain', 105, 96, { align: 'center' });

      // Subtitle line
      doc.setDrawColor(59, 130, 246);
      doc.setLineWidth(0.5);
      doc.line(60, 108, 150, 108);

      doc.setFontSize(11);
      doc.setTextColor(148, 163, 184);
      doc.text('Guia Personalizada del Sistema de Agentes IA', 105, 118, { align: 'center' });

      // Stats box
      doc.setFillColor(13, 17, 23);
      doc.roundedRect(35, 135, 140, 35, 4, 4, 'F');
      doc.setDrawColor(59, 130, 246);
      doc.setLineWidth(0.3);
      doc.roundedRect(35, 135, 140, 35, 4, 4, 'S');

      doc.setFontSize(9);
      doc.setTextColor(96, 165, 250);
      doc.text('Perfil:', 45, 148);
      doc.text('Completado:', 45, 157);
      doc.text('Fecha:', 45, 166);

      doc.setTextColor(240, 244, 255);
      doc.text(profile, 80, 148);
      doc.text(STATE.completedModules.size + '/6 modulos en ' + elapsed + ' min', 80, 157);
      doc.text(date, 80, 166);

      // Footer
      doc.setFontSize(8);
      doc.setTextColor(75, 85, 99);
      doc.text('Brain Academy v3.0 — Sistema de Agentes Inteligentes sobre Obsidian', 105, 280, { align: 'center' });

      // ─── Page 2: Quick Setup ───
      doc.addPage();
      doc.setFillColor(7, 11, 18);
      doc.rect(0, 0, 210, 297, 'F');

      // Header bar
      doc.setFillColor(59, 130, 246);
      doc.rect(0, 0, 210, 3, 'F');

      doc.setFontSize(20);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(240, 244, 255);
      doc.text('Setup Rapido', 20, 25);

      doc.setFontSize(9);
      doc.setTextColor(148, 163, 184);
      doc.text('Necesitas 3 herramientas gratuitas. 10 minutos de instalacion.', 20, 34);

      // Steps
      const steps = [
        {
          num: '01',
          title: 'Instalar Obsidian',
          desc: 'Descarga desde obsidian.md/download (~100MB).\nCrea un vault llamado "' + name + ' Brain".',
          color: [59, 130, 246]
        },
        {
          num: '02',
          title: 'Copiar MASTERTMIND',
          desc: 'Copia toda la carpeta MASTERTMIND/ dentro de tu vault.\nContiene los 10 agentes, skills, learnings y configuracion.',
          color: [59, 130, 246]
        },
        {
          num: '03',
          title: 'Personalizar',
          desc: 'Abre agents/state/_system-config.md.\nCambia system_name y owner a "' + name + '".',
          color: [249, 115, 22]
        },
        {
          num: '04',
          title: 'Activar el Sistema',
          desc: 'Abre OpenCode en tu vault.\nPega el contenido de session-prompt.md.\nEl sistema responde con SISTEMA ACTIVO.',
          color: [249, 115, 22]
        }
      ];

      let stepY = 50;
      steps.forEach(step => {
        // Number circle
        doc.setFillColor(...step.color);
        doc.setGState(new doc.GState({ opacity: 0.15 }));
        doc.circle(30, stepY + 6, 10, 'F');
        doc.setGState(new doc.GState({ opacity: 1 }));

        doc.setFontSize(14);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(...step.color);
        doc.text(step.num, 26, stepY + 9);

        // Title
        doc.setFontSize(12);
        doc.setTextColor(240, 244, 255);
        doc.text(step.title, 48, stepY + 6);

        // Desc
        doc.setFontSize(9);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(148, 163, 184);
        const lines = doc.splitTextToSize(step.desc, 140);
        doc.text(lines, 48, stepY + 14);

        stepY += 12 + (lines.length * 5) + 10;
      });

      // Session prompt box
      doc.setFillColor(13, 17, 23);
      doc.roundedRect(20, stepY + 5, 170, 55, 4, 4, 'F');
      doc.setDrawColor(34, 197, 94);
      doc.setLineWidth(0.3);
      doc.roundedRect(20, stepY + 5, 170, 55, 4, 4, 'S');

      doc.setFontSize(8);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(134, 239, 172);
      doc.text('session-prompt.md', 28, stepY + 14);

      doc.setFont('courier', 'normal');
      doc.setFontSize(7);
      doc.setTextColor(148, 163, 184);
      const promptLines = [
        'Lee los siguientes archivos en este orden exacto:',
        '1. AGENTS.md',
        '2. agents/00-orchestrator.md',
        '3. agents/state/_system-config.md',
        '4. agents/state/_session-state.md',
        '5. agents/skills/_index.md',
        '6. agents/learnings/_index.md',
        '7. agents/projects/_clusters.md'
      ];
      promptLines.forEach((line, i) => {
        doc.text(line, 28, stepY + 22 + (i * 4.5));
      });

      // ─── Page 3: Architecture + Agents ───
      doc.addPage();
      doc.setFillColor(7, 11, 18);
      doc.rect(0, 0, 210, 297, 'F');
      doc.setFillColor(249, 115, 22);
      doc.rect(0, 0, 210, 3, 'F');

      doc.setFontSize(20);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(240, 244, 255);
      doc.text('Los 10 Agentes + Orchestrator', 20, 25);

      doc.setFontSize(9);
      doc.setTextColor(148, 163, 184);
      doc.text('Cada agente tiene un trabajo unico. Nadie hace el trabajo de otro.', 20, 34);

      const agents = [
        { id: '00', name: 'Orchestrator', role: 'Coordina el flujo completo. Nivel ALTO.', phase: 'Coordinacion', color: [239, 68, 68] },
        { id: '01', name: 'Classifier', role: 'Detecta tipo de tarea y disena el flujo.', phase: 'Entender', color: [59, 130, 246] },
        { id: '02', name: 'Explorer', role: 'Lee contexto existente sin modificar.', phase: 'Entender', color: [59, 130, 246] },
        { id: '03', name: 'Planner', role: 'Disena estrategia y pasos concretos.', phase: 'Planificar', color: [249, 115, 22] },
        { id: '04', name: 'Spec Writer', role: 'Genera spec ejecutable y verificable.', phase: 'Planificar', color: [249, 115, 22] },
        { id: '05', name: 'Implementer', role: 'Ejecuta la spec aprobada.', phase: 'Ejecutar', color: [34, 197, 94] },
        { id: '06', name: 'Reviewer', role: 'Valida calidad y coherencia del output.', phase: 'Validar', color: [168, 85, 247] },
        { id: '07', name: 'Critic', role: 'Busca fallas que el reviewer no vio.', phase: 'Validar', color: [168, 85, 247] },
        { id: '08', name: 'Synthesizer', role: 'Resume y comunica resultados.', phase: 'Cerrar', color: [20, 184, 166] },
        { id: '09', name: 'Archiver', role: 'Destila aprendizaje permanente.', phase: 'Cerrar', color: [20, 184, 166] },
        { id: '10', name: 'Librarian', role: 'Mantiene skills, templates e indices.', phase: 'Cerrar', color: [20, 184, 166] },
      ];

      let agentY = 45;
      agents.forEach(agent => {
        // Colored line
        doc.setDrawColor(...agent.color);
        doc.setLineWidth(2);
        doc.line(20, agentY, 20, agentY + 14);

        // ID
        doc.setFontSize(8);
        doc.setFont('courier', 'bold');
        doc.setTextColor(...agent.color);
        doc.text(agent.id, 25, agentY + 5);

        // Name
        doc.setFontSize(10);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(240, 244, 255);
        doc.text(agent.name, 38, agentY + 5);

        // Phase tag
        doc.setFontSize(7);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(...agent.color);
        doc.text('[' + agent.phase + ']', 38, agentY + 11);

        // Role
        doc.setFontSize(8);
        doc.setTextColor(148, 163, 184);
        doc.text(agent.role, 70, agentY + 11);

        agentY += 20;
      });

      // ─── Page 4: Memory & Tips ───
      doc.addPage();
      doc.setFillColor(7, 11, 18);
      doc.rect(0, 0, 210, 297, 'F');
      doc.setFillColor(34, 197, 94);
      doc.rect(0, 0, 210, 3, 'F');

      doc.setFontSize(20);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(240, 244, 255);
      doc.text('Sistema de Memoria', 20, 25);

      // Memory layers
      const layers = [
        { name: 'Skills', desc: 'Protocolos de ejecucion reutilizables. Se activan automaticamente cuando detectan una tarea compatible.', icon: 'agents/skills/', color: [59, 130, 246] },
        { name: 'Learnings', desc: 'Conocimiento destilado de cada ciclo completado. El _index.md permite carga bajo demanda.', icon: 'agents/learnings/', color: [249, 115, 22] },
        { name: 'Clusters', desc: 'Etiquetas dinamicas que agrupan learnings por dominio. Se crean automaticamente.', icon: 'agents/projects/', color: [34, 197, 94] },
      ];

      let layerY = 40;
      layers.forEach(layer => {
        doc.setFillColor(13, 17, 23);
        doc.roundedRect(20, layerY, 170, 30, 4, 4, 'F');
        doc.setDrawColor(...layer.color);
        doc.setLineWidth(0.3);
        doc.roundedRect(20, layerY, 170, 30, 4, 4, 'S');

        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(...layer.color);
        doc.text(layer.name, 28, layerY + 12);

        doc.setFontSize(8);
        doc.setFont('courier', 'normal');
        doc.setTextColor(75, 85, 99);
        doc.text(layer.icon, 28, layerY + 18);

        doc.setFont('helvetica', 'normal');
        doc.setTextColor(148, 163, 184);
        const descLines = doc.splitTextToSize(layer.desc, 130);
        doc.text(descLines, 28, layerY + 24);

        layerY += 38;
      });

      // Pro tips section
      doc.setFontSize(16);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(240, 244, 255);
      doc.text('Consejos Pro para ' + profile, 20, layerY + 20);

      const tips = [
        'Se especifico en tus tareas — cuanto mas contexto, mejor resultado.',
        'Lee las specs antes de aprobar — 30 segundos te ahorran 30 minutos.',
        'Deja que el sistema archive — cada learning es una inversion.',
        'Tu primer ciclo sera el mas lento — a partir del segundo, el sistema ya tiene contexto.',
        'Usa skills para tareas recurrentes — documenta tus procesos.',
      ];

      let tipY = layerY + 30;
      tips.forEach((tip, i) => {
        doc.setFillColor(249, 115, 22);
        doc.setGState(new doc.GState({ opacity: 0.15 }));
        doc.circle(27, tipY + 3, 5, 'F');
        doc.setGState(new doc.GState({ opacity: 1 }));

        doc.setFontSize(9);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(249, 115, 22);
        doc.text(String(i + 1), 25, tipY + 5);

        doc.setFont('helvetica', 'normal');
        doc.setFontSize(9);
        doc.setTextColor(148, 163, 184);
        const tipLines = doc.splitTextToSize(tip, 148);
        doc.text(tipLines, 40, tipY + 5);

        tipY += 8 + (tipLines.length * 4);
      });

      // Resources
      doc.setFontSize(12);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(59, 130, 246);
      doc.text('Recursos', 20, tipY + 15);

      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(148, 163, 184);
      doc.text('Obsidian: obsidian.md/download', 20, tipY + 24);
      doc.text('OpenCode: github.com/anomalyco/opencode/releases', 20, tipY + 32);
      doc.text('Documentacion: AGENTS.md en tu vault', 20, tipY + 40);

      // Footer all pages
      const totalPages = doc.internal.getNumberOfPages();
      for (let i = 1; i <= totalPages; i++) {
        doc.setPage(i);
        doc.setFontSize(7);
        doc.setTextColor(75, 85, 99);
        doc.text(name + ' Brain — Guia generada por Brain Academy', 105, 290, { align: 'center' });
        doc.text('Pagina ' + i + ' de ' + totalPages, 190, 290, { align: 'right' });
      }

      // Save
      const safeName = name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
      doc.save(safeName + '-brain-guia.pdf');
      showXPNotification('PDF generado!');
      awardXP(100);

    } catch (err) {
      console.error('PDF error:', err);
      showXPNotification('Error PDF');
    }
  }

  // ── State persistence ──────────────────────────────────────
  function saveState() {
    const data = {
      userName: STATE.userName,
      userProfile: STATE.userProfile,
      profileId: STATE.profileId,
      currentModule: STATE.currentModule,
      completedModules: Array.from(STATE.completedModules),
      quizAnswers: STATE.quizAnswers,
      quizResults: STATE.quizResults,
      correctAnswers: STATE.correctAnswers,
      totalQuestions: STATE.totalQuestions,
      timerSeconds: STATE.timerSeconds,
      xp: STATE.xp,
      level: STATE.level,
      badges: STATE.badges,
      startTime: STATE.startTime,
    };
    localStorage.setItem('brainacademy_state_v3', JSON.stringify(data));
  }

  // Restore session from localStorage (returns true if restored)
  async function loadState() {
    const raw = localStorage.getItem('brainacademy_state_v3');
    if (!raw) return false;

    try {
      const data = JSON.parse(raw);
      if (!data.userName || !data.profileId || !data.userProfile) return false;

      // Restore STATE
      STATE.userName = data.userName;
      STATE.userProfile = data.userProfile;
      STATE.profileId = data.profileId;
      STATE.currentModule = data.currentModule || 0;
      STATE.completedModules = new Set(data.completedModules || []);
      STATE.quizAnswers = data.quizAnswers || {};
      STATE.quizResults = data.quizResults || {};
      STATE.correctAnswers = data.correctAnswers || 0;
      STATE.totalQuestions = data.totalQuestions || 0;
      STATE.timerSeconds = data.timerSeconds || 5400;
      STATE.xp = data.xp || 0;
      STATE.level = data.level || 1;
      STATE.badges = data.badges || [];
      STATE.startTime = data.startTime || Date.now();

      // Load profiles.json so STATE.profiles is available
      try {
        const resp = await fetch('profiles.json');
        if (resp.ok) STATE.profiles = await resp.json();
      } catch (e) { /* non-critical */ }

      // Jump to learning screen
      $$('.screen').forEach(s => s.classList.remove('active'));
      $('#screen-learning').classList.add('active');

      await loadModules();
      return true;
    } catch (err) {
      console.warn('Failed to restore state:', err);
      localStorage.removeItem('brainacademy_state_v3');
      return false;
    }
  }

  // ── Boot ───────────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
