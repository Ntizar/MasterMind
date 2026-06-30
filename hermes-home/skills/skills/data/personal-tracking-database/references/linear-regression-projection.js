/**
 * linear-regression-projection.js
 * ================================
 * Implementación de regresión lineal para proyecciones en dashboards de tracking.
 * 
 * Origen: MasterFit (dieta-masterfit) — dashboard.html
 * Técnica: mínimos cuadrados sobre pesajes de mañana para suavizar fluctuaciones.
 */

// ===== 1. Helper: ritmo real por regresión lineal =====
// Solo usa registros de 'mañana' para consistencia
// Devuelve kg/semana y un icono según la velocidad
function calcRitmoLineal(peso) {
  var mananas = peso.filter(function(p){ return p.hora === 'mañana'; });
  if(mananas.length < 2) return {ritmo:0, icon:'🐢', label:'sin datos'};

  var n = mananas.length, sumX = 0, sumY = 0, sumXY = 0, sumXX = 0;
  var ref = new Date(mananas[0].fecha);  // día 0 = primer registro

  mananas.forEach(function(p){
    var x = (new Date(p.fecha) - ref) / 86400000;  // días desde ref
    var y = p.peso_kg;
    sumX += x; sumY += y; sumXY += x*y; sumXX += x*x;
  });

  // pendiente = (n·Σxy - Σx·Σy) / (n·Σxx - Σx·Σx)
  var pendiente = (n*sumXY - sumX*sumY) / (n*sumXX - sumX*sumX) || 0;
  var ritmo = Math.max(0, -pendiente * 7);  // kg/semana (negativo = pérdida)

  var icon = ritmo >= 1.0 ? '🔥' : ritmo >= 0.5 ? '📈' : ritmo >= 0.2 ? '🐢' : '🆘';
  return {ritmo:ritmo, icon:icon, label:icon+' Regresión ('+ritmo.toFixed(2)+' kg/sem)'};
}


// ===== 2. Render proyecciones (tabla) =====
function renderProyecciones(pesoActual, objetivo, ritmoReal) {
  var ritmos = [
    {nombre:'Real (regresión lineal)', ks:ritmoReal>0?ritmoReal:0.3, badge:'brand', label:'📈'},
    {nombre:'Sostenible', ks:0.3, badge:'success', label:'🌱'},
    {nombre:'Normal', ks:0.5, badge:'accent', label:'🚶'},
    {nombre:'Acelerado', ks:0.7, badge:'brand', label:'🔥'},
    {nombre:'Agresivo', ks:1.0, badge:'danger', label:'⚡'}
  ];

  var falta = pesoActual - objetivo;
  var html = '<div style="background:linear-gradient(135deg,#eff6ff,#fef3c7);border-radius:12px;padding:1rem;border:1px solid #bfdbfe;">';
  html += '<h4 style="margin:0 0 0.5rem;font-size:0.85rem;font-weight:600;color:#1e40af;">📅 Fechas estimadas para alcanzar '+objetivo+' kg</h4>';

  ritmos.forEach(function(r){
    var sem = falta / r.ks;
    var f = new Date();
    f.setDate(f.getDate() + Math.round(sem * 7));
    html += '<div style="display:flex;justify-content:space-between;align-items:center;padding:0.4rem 0;border-bottom:1px solid rgba(0,0,0,0.05);font-size:0.85rem;">' +
      '<span style="font-weight:600;color:#334155;">'+r.label+' '+r.nombre+'</span>' +
      '<span>'+r.ks+' kg/sem</span>' +
      '<span style="color:#2563eb;font-weight:600;">'+f.toLocaleDateString('es-ES')+'</span>' +
      '<span class="nz-badge nz-badge--'+r.badge+'">'+Math.round(sem)+' sem</span></div>';
  });

  html += '</div>';
  html += '<div style="margin-top:0.75rem;padding:0.75rem;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0;">' +
    '<h4 style="margin:0 0 0.5rem;font-size:0.85rem;font-weight:600;color:#334155;">📊 Datos de Referencia</h4>' +
    '<div style="font-size:0.85rem;color:#64748b;">' +
    '<div>TMB: <strong>~1.840 kcal/día</strong></div><div>TDEE: <strong>~2.530 kcal/día</strong></div>' +
    '<div>Déficit 0,7 kg/sem: <strong>~550 kcal/día</strong></div>' +
    '<div>Ingesta: <strong>~1.700-1.800 kcal/día</strong></div>' +
    '<div style="margin-top:0.5rem;color:#2563eb;">💡 10k pasos + gym 4x/sem + proteína 140-160g</div></div></div>';

  document.getElementById('proyeccionesContainer').innerHTML = html;
}


// ===== 3. Chart de proyecciones =====
function renderProyeccionChart(pesoActual, objetivo, ritmoReal) {
  var ctx = document.getElementById('chartProyeccion').getContext('2d');
  var hoy = new Date();
  var labels = [], dS = [], dN = [], dA = [], dAg = [], dR = [];

  for(var i = 0; i <= 20; i++) {
    var f = new Date(hoy);
    f.setDate(f.getDate() + i * 7);
    labels.push(f.toLocaleDateString('es-ES', {day:'2-digit', month:'2-digit'}));
    dS.push(Math.max(objetivo, pesoActual - i * 0.3));
    dN.push(Math.max(objetivo, pesoActual - i * 0.5));
    dA.push(Math.max(objetivo, pesoActual - i * 0.7));
    dAg.push(Math.max(objetivo, pesoActual - i * 1.0));
    dR.push(Math.max(objetivo, pesoActual - i * (ritmoReal > 0 ? ritmoReal : 0.3)));
  }

  if(charts.proyeccion) charts.proyeccion.destroy();

  charts.proyeccion = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        // REAL — siempre primero, más grueso, con puntos
        {label:'📈 Real (regresión) ' + (ritmoReal > 0 ? ritmoReal.toFixed(2) : '--') + ' kg/sem',
         data: dR, borderColor: '#7c3aed', borderWidth: 3,
         pointRadius: 3, pointBackgroundColor: '#7c3aed'},
        // Escenarios fijos (discontinuos / finos)
        {label:'Sostenible (0,3)', data: dS, borderColor: '#94a3b8',
         borderDash: [3,3], pointRadius: 0, borderWidth: 1.5},
        {label:'Normal (0,5)', data: dN, borderColor: '#f97316',
         borderDash: [4,4], pointRadius: 0, borderWidth: 1.5},
        {label:'Acelerado (0,7)', data: dA, borderColor: '#2563eb',
         pointRadius: 0, borderWidth: 2.5},
        {label:'Agresivo (1,0)', data: dAg, borderColor: '#ef4444',
         borderDash: [5,5], pointRadius: 0, borderWidth: 1.5},
        // Línea objetivo
        {label:'Objetivo ' + objetivo + ' kg',
         data: Array(labels.length).fill(objetivo),
         borderColor: '#22c55e', borderDash: [8,4], pointRadius: 0, borderWidth: 2}
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'top' } },
      scales: {
        y: { min: 85, max: pesoActual + 1, title: { display: true, text: 'kg' } }
      }
    }
  });
}