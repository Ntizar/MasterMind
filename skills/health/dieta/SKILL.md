---
name: dieta
version: "4.1.0"
description: "Sistema completo de base de datos de dieta — peso, comidas, deporte, pasos, agua. Dashboard HTML interactivo con Chart.js + Aurora. Scripts CLI de registro rápido. Proyecciones y análisis de déficit. v4.1.0 — hora editable en todos los registros, preview-edit-confirm en estimaciones IA, navegación entre días en resumen, InBody y Progreso 3D ocultados."
tags: [dieta, nutrición, kcal, seguimiento, salud, dashboard, fitness, sqlite, sql.js, agua, hidratación]
---

# Dieta v3 — Sistema de Base de Datos + Dashboard

## Arquitectura

```
/root/workspace/dieta-masterfit/
├── data/
│   └── database.json        ← Base de datos central (JSON estructurado)
├── scripts/
│   └── registro.py          ← CLI para registrar peso/comida/deporte/pasos
├── peso.sh                  ← Atajo: ./peso.sh 96.5
├── comida.sh                ← Atajo: ./comida.sh cena 'huevos' 300
├── deporte.sh               ← Atajo: ./deporte.sh 'Pierna' 45 alta
├── dashboard.html           ← Dashboard interactivo (Chart.js + Aurora)
├── server.js                ← Express backend con APIs REST + IA
├── .env                     ← NAN_API token (NO en git)
├── Dockerfile               ← NaN Builders deploy
├── SEGUIMIENTO.md           ← Legacy (mantener por compatibilidad)
└── README.md
```

**Repo GitHub:** `github.com/Ntizar/dieta` (remote ya configurado)
**URL NaN:** `dieta-ntizar-ntizar.apps.nan.builders`

## Base de datos (database.json)

Estructura del JSON:

```json
{
  "meta": {
    "nombre": "David Antizar",
    "altura_cm": 174,
    "peso_inicial_kg": 98.6,
    "peso_objetivo_kg": 78.5,
    "fecha_inicio": "2026-06-03",
    "version": "3.1.0",
    "features": ["peso", "comidas", "deporte", "pasos", "inbody", "entrenamientos", "progreso_3d", "hidratacion", "dark_mode"]
  },
  "perfil": {
    "edad": 36,
    "genero": "masculino",
    "altura_cm": 174,
    "nivel_actividad": "activo",
    "notas": "Entrena 4x/semana, 10k pasos objetivo. InBody 04/06: score 70, visceral 14, TMB 1810. Edad REAL: 36."
  },
  "peso": [...],
  "comidas": [...],
  "entrenamientos": [...],
  "pasos": [...],
  "entrenamientos": [...],
  "inbody_history": [...]
}
```

### Perfil dinámico (CRÍTICO)

Los endpoints de estimación IA y el coach (Amadeo) **leen el perfil y el peso actual de la DB**, nunca valores hardcodeados. Si el usuario cambia de peso, las estimaciones se ajustan automáticamente.

Helpers en server.js:
- `perfilUsuario(db)` → `{nombre, edad, genero, altura_cm, peso_kg, peso_objetivo, nivel_actividad}`
- `contextoPerfil(db)` → string descriptivo para prompts IA

**Regla:** NUNCA hardcodear peso, edad ni altura en prompts IA. Siempre leer de `db.perfil` + `db.peso[-1]`.

## Multi-usuario (v4.0.1)

El sistema soporta múltiples usuarios con aislamiento total de datos.

### Backend
- **Tabla `usuarios`**: `id, nombre, activo, created_at`
- **GET /api/auth/usuarios**: lista usuarios activos → `{ok:true, usuarios:[{id,nombre}]}`
- **POST /api/auth/login**: si el usuario no existe, lo crea con perfil vacío (sin valores por defecto) → el onboarding IA los pregunta
- **Cada tabla de datos** tiene `usuario_id` como clave foránea → datos aislados por usuario

### Frontend
- Pantalla de login muestra botones de usuarios existentes (👤 Nombre) + campo de texto para nuevos nombres
- `loadUsers()` se llama al iniciar → muestra selector si hay usuarios
- `_onboardingPaso` se resetea en logout
- `doLogout()` limpia `appState.chatMessages` y `_onboardingPaso = -1`

### Regla
- NUNCA hardcodear nombre de usuario. Siempre leer de sesión activa.
- Cuando se crea un usuario nuevo, el perfil se crea vacío → el onboarding IA obliga a rellenarlo.
- NO poner valores por defecto al crear usuario (edad=30, genero='masculino') → dejar NULL para que el onboarding los pregunte.

## Onboarding IA (v4.0.1)

Cuando un usuario nuevo entra, **Amadeo (coach IA) le entrevista paso a paso** para rellenar su perfil. No se muestran valores por defecto.

### Backend
- **GET /api/onboarding/status**: verifica si perfil completo o devuelve siguiente paso pendiente
- **POST /api/onboarding/step**: guarda respuesta, actualiza perfil o tabla peso, devuelve siguiente paso
- **5 pasos**: edad → altura → peso actual → peso objetivo → nivel actividad

### Pasos definidos en server.js (`ONBOARDING_STEPS`)
```javascript
const ONBOARDING_STEPS = [
  { campo: 'edad', pregunta: '¿Cuántos años tienes?', tipo: 'numero', tabla: 'perfil' },
  { campo: 'altura_cm', pregunta: '¿Cuánto mides (en cm)?', tipo: 'numero', tabla: 'perfil' },
  { campo: 'peso_actual_kg', pregunta: '¿Cuánto pesas ahora (kg)?', tipo: 'numero', tabla: 'peso' },
  { campo: 'peso_objetivo_kg', pregunta: '¿A qué peso quieres llegar?', tipo: 'numero', tabla: 'perfil' },
  { campo: 'nivel_actividad', pregunta: 'Nivel de actividad:', tipo: 'select', opciones: ['sedentario','ligero','activo','muy_activo'], tabla: 'perfil' },
];
```

### Flujo frontend
1. Al entrar a tab coach → `checkOnboarding()` llama a `/api/onboarding/status`
2. Si `!completo` → `sendOnboardingStep(0)` muestra primera pregunta de Amadeo
3. Usuario responde → `sendChat()` intercepta si `_onboardingPaso >= 0` → llama `sendOnboardingAnswer(respuesta)`
4. Backend guarda en tabla correcta (`perfil` o `peso`) → frontend muestra confirmación
5. Si hay más pasos → `setTimeout` envía siguiente pregunta a los 500ms
6. Al completar → mensaje 🎉 de bienvenida, `_onboardingPaso = -1`

### Pitfall: peso_actual_kg va en tabla `peso`, NO en `perfil`
La columna `peso_actual_kg` NO existe en la tabla `perfil` de SQLite. El paso 3 del onboarding debe INSERTAR en la tabla `peso` con fecha/hora actual, no UPDATE en `perfil`. El backend determina la tabla con `stepDef.tabla`.

### Pitfall: no values por defecto al crear usuario
Cuando el login crea un usuario nuevo, el perfil se INSERTA con `genero='no definido'` y todos los demás campos NULL. Si se ponen valores por defecto (edad=30, altura=174), `perfilCompleto()` devuelve true y el onboarding se salta.

## Trigger del usuario

- **`Dieta.`** al inicio del mensaje → el usuario quiere registrar algo
- **`Dieta. peso 96.5`** → registrar peso
- **`Dieta. comida cena huevos 300`** → registrar comida
- **`Dieta. deporte pierna 45 alta`** → registrar deporte
- **`Dieta. resumen`** → mostrar resumen del día
- **`Dieta.`** + corrección de datos faltantes → añadir datos históricos que se pasaron por alto

### 🔥 CRÍTICO: LladosApp usa SQLite, NO database.json

LladosApp (el dashboard que usa David) se alimenta de `data/masterfit.db` (SQLite), **NO** de `data/database.json` (legacy JSON).

**Procedimiento correcto para registrar comida/peso/deporte:**

1. **Siempre escribir en SQLite** (`masterfit.db`) — es la fuente de verdad de LladosApp
2. Usar `sqlite3` o `import sqlite3` para INSERTar directamente en las tablas (`comidas`, `peso`, `entrenamientos`, `pasos`)
3. **NO editar database.json** — es un formato legacy que LladosApp no lee en producción
4. El endpoint `POST /api/comida` en server.js INSERTa en SQLite, no en JSON
5. Commit y push de `data/masterfit.db` tras cada mutación

**Pitfall real (2026-06-16):** Se metieron datos en database.json y el usuario dijo "no estás poniendo los datos al usuario David Antizar cuando te lo digo… en LladosApp". La app no veía los datos porque leen de SQLite, no de JSON.

**Siempre verificar la DB real de la app ANTES de escribir datos.**

## Dashboard

Abrir `dashboard.html` en navegador para ver:
- 📈 Evolución de peso con media móvil de 7 días
- 🔥 Calorías diarias vs TDEE
- 🥗 Macros (proteínas, hidratos, grasas) vs objetivo
- 💧 Hidratación del día (contador de vasos con localStorage)
- 🚶 Pasos diarios
- 📊 Déficit calórico
- 🔮 Proyecciones a peso objetivo (5 ritmos, incluido el real basado en últimos 7 días)
- 🍽️ Lista completa de comidas
- 🏋️ Timeline de entrenamientos
- 🤖 Asistente IA "Amadeo Llados" (coach fitness directo)
- 🤖 Estimación automática de kcal (comida y ejercicio)
- 🔬 Progreso 3D con InBody

## Exportación CSV

Cuando el usuario pida "los datos en CSV", generar 7 archivos estructurados desde database.json:

### Archivos generados

```
data/csv/
├── historico_diario.csv     ← 1 fila/día: peso, kcal, macros, pasos, entreno
├── historico_peso.csv       ← cada toma de peso (mañana/tarde)
├── historico_comidas.csv    ← cada comida con macros detallados
├── historiansico_pasos.csv   ← pasos diarios
├── historico_entrenamientos.csv ← sesiones de entrenamiento
├── historico_inbody.csv     ← mediciones InBody
└── perfil.csv               ← datos personales (clave:valor)
```

### Patrón de generación (Python)

Usar `execute_code` con Python estándar (json+csv):

```python
import json, csv, os
from collections import defaultdict

with open('data/database.json') as f:
    db = json.load(f)

OUT_DIR = 'data/csv'
os.makedirs(OUT_DIR, exist_ok=True)

# Para cada array en db: peso, comidas, pasos, entrenamientos, inbody_history
# Generar CSV con DictWriter y fieldnames explícitos
# Para historico_diario: cruzar todos los arrays por fecha
```

### historico_diario — el máster

Cruzar todos los datos por fecha en UNA fila por día:

```python
peso_by_day = defaultdict(list)  # fecha → [{peso_kg, hora}]
comidas_by_day = defaultdict(list)  # fecha → [{kcal, proteinas_g, ...}]
pasos_by_day = {}  # fecha → {pasos, distancia_km}
entrenos_by_day = defaultdict(list)  # fecha → [{duracion_min, kcal_estimadas}]

# Iterar todas las fechas únicas
for fecha in all_dates:
    row = {
        'fecha': fecha,
        'peso_manana_kg': peso_manana_or_empty,
        'kcal_totales': sum(c.kcal for c in comidas_hoy),
        'proteinas_g': sum(c.proteinas_g for c in comidas_hoy),
        'pasos': pasos_hoy.get('pasos', ''),
        'entreno': 'SÍ' if entrenos_hoy else '',
        'min_entreno': sum(e.duracion_min for e in entrenos_hoy),
        'kcal_ejercicio': sum(e.kcal_estimadas for e in entrenos_hoy),
    }
```

### Detección de alcohol en comidas

Para la columna `kcal_alcohol` en historico_diario, detectar comidas que contengan alcohol por tipo o descripción:

```python
alcohol_kcal = sum(c['kcal'] for c in comidas_hoy 
    if 'bebida' in c.get('tipo','') or 
       any(w in c['descripcion'].lower() 
           for w in ['vino','cerveza','gintonic','alcohol','volldamm','botella','copa']))
```

### Columns estándar por CSV

**historico_diario:** fecha, peso_mañana_kg, peso_tarde_kg, peso_medio_kg, kcal_totales, proteinas_g, hidratos_g, grasas_g, num_comidas, kcal_alcohol, pasos, distancia_km, kcal_pasos, entreno, min_entreno, kcal_ejercicio, tipo_entreno

**historico_peso:** fecha, hora, peso_kg, notas
**historico_comidas:** fecha, hora, tipo, descripcion, kcal, proteinas_g, hidratos_g, grasas_g, notas
**historico_pasos:** fecha, pasos, distancia_km, kcal, notas
**historico_entrenamientos:** fecha, hora, tipo, grupo_muscular, descripcion, series, reps_totales, duracion_min, intensidad, rpe, kcal_estimadas, notas
**historico_inbody:** fecha, hora, peso_kg, masa_grasa_kg, porcentaje_grasa, masa_muscular_kg, agua_L, proteinas_kg, minerales_kg, imc, inbody_score, tmb_kcal, grasa_visceral, relacion_cintura_cadera, grado_obesidad, control_grasa_kg, control_muscular_kg, notas

### Orden de las columnas

Siempre `fecha` primero, luego métricas cuantitativas de más a menos importante, luego notas al final. Separador CSV: coma estándar. Encoding: UTF-8.

## Media Móvil en Gráficos de Peso

**Patrón:** suavizar series temporales de peso con media móvil de N días. Se adapta automáticamente si hay menos datos que N.

```javascript
// En renderPesoChart() y renderPesoEvoChart():
var windowSize = Math.min(7, data.length);
var maData = [];
for (var i = 0; i < data.length; i++) {
  var start = Math.max(0, i - windowSize + 1);
  var slice = data.slice(start, i + 1);
  var sum = 0;
  for (var j = 0; j < slice.length; j++) sum += slice[j];
  maData.push(Math.round(sum / slice.length * 10) / 10);
}
// Añadir como dataset adicional con borderColor: '#f97316', tension: 0.4
```

**Generalizable a cualquier serie temporal en Chart.js:**
1. `windowSize = Math.min(N, data.length)`
2. Calcular media de ventana deslizante para cada índice
3. Añadir dataset con color distinto, `tension: 0.4`, `pointRadius: 3`

## Estimación IA automática

### Patrón general

Ambos endpoints (`/api/estimar-comida` y `/api/estimar-ejercicio`) siguen el mismo flujo:

1. **Frontend:** al hacer blur en el campo de descripción → llama al endpoint
2. **Backend:** lee perfil + peso actual de DB → construye prompt → llama qwen3.6
3. **Frontend:** recibe JSON con estimación → rellena campos automáticamente
4. **Badge visual:** "🤖 Estimando..." → "✅ IA: 450 kcal" (se borra a los 5s)
5. **Override:** si el campo ya tiene un valor manual, NO sobreescribe

### Endpoint `/api/estimar-comida`

```javascript
POST /api/estimar-comida
Body: { descripcion: "pechuga pollo + arroz", tipo: "comida" }
Response: { estimado: true, kcal: 420, proteinas_g: 38, hidratos_g: 45, grasas_g: 8 }
```

Prompt: nutricionista experto que estima kcal/macros. Usa `contextoPerfil(db)` para el perfil.

### Endpoint `/api/estimar-ejercicio`

```javascript
POST /api/estimar-ejercicio
Body: { descripcion: "Gym pecho y tríceps", duracion_min: 60, intensidad: "alta" }
Response: { estimado: true, kcal_estimadas: 480, duracion_sugerida: 60, intensidad_detectada: "alta", tipo: "pesas" }
```

Prompt: experto en fisiología del ejercicio. Usa `contextoPerfil(db)` para el perfil. Factores por tipo:
- Gym/pesas: 6-8 kcal/kg/hora
- Cardio: 8-12 kcal/kg/hora
- HIIT: 10-14 kcal/kg/hora
- Caminar: 3-5 kcal/kg/hora
- Natación: 7-10 kcal/kg/hora

### Hora por defecto: siempre Madrid

El campo `<input type="time">` debe iniciarse con la hora actual de Madrid, no vacío:

```javascript
function setHoraMadrid() {
  var ahora = new Date();
  var hora = ahora.toLocaleTimeString('es-ES', { hour:'2-digit', minute:'2-digit', timeZone:'Europe/Madrid', hour12:false });
  var el = document.getElementById('comidaHora');
  if (el && !el.value) el.value = hora;
}
// Llamar al cargar página Y tras resetear el formulario
loadData();
setHoraMadrid();
```

Tras `formComida.reset()`, volver a llamar `setHoraMadrid()` para reestablecer la hora.

### Frontend: auto-estimación

```javascript
// En el HTML, añadir onblur al campo de descripción:
<input id="comidaDesc" onblur="estimarComida()" ...>
<button type="button" onclick="estimarComida()">🤖 Estimar</button>

function estimarComida() {
  var desc = document.getElementById('comidaDesc').value.trim();
  var kcal = parseInt(document.getElementById('comidaKcal').value) || 0;
  if (!desc || desc.length < 3 || kcal > 0) return; // skip si ya tiene kcal manuales
  // fetch → rellenar campos → badge visual
}
```

### Pitfall: peso hardcodeado

**NUNCA** escribir "94kg" o "45 años" en prompts IA. Siempre usar `contextoPerfil(db)` que lee el peso actual de `db.peso[-1]` y el perfil de `db.perfil`. El peso cambia cada día → las estimaciones deben cambiar con él.

## Tracker de Agua (v4.0.1)

**NUEVO en v4.0.1:** Tracker de hidratación completo con UI en tab Registrar.

### Backend
- `GET /api/agua?fecha=YYYY-MM-DD` → retorna registros del día
- `POST /api/agua` → `{ ml: 250 }` → añade registro
- `DELETE /api/agua/:index` → elimina registro por índice

### Frontend (tab Registrar)
- Tarjeta 💧 con input personalizado + botones rápidos (100, 200, 250, 500 ml)
- `loadAguaStrip()` → muestra botones rápidos + progreso (total/2000ml)
- `registrarAgua()` → POST con ml personalizado
- `quickAgua(ml)` → POST con ml predefinido
- Chip 💧 en resumen de hoy (junto a kcal, prot, pasos)
- Icono cambia: 💧 (naranja <50%) → 💧 (azul ≥50%) → 🎉 (verde ≥100%)

### Meta diaria
- Objetivo: 2000 ml (8 vasos de 250ml)
- Se resetea automáticamente cada día (filtrado por fecha en backend)

### Pitfall: backend API sin frontend
El backend de agua (`/api/agua`) existía desde antes de v4.0.1 pero no había UI. **Regla:** cuando se añade un endpoint backend, verificar que existe su UI en el frontend. Si no existe, añadirlo en el mismo commit.

## Tracker de Hidratación (Legacy — localStorage)

**Patrón:** contador de vasos con persistencia diaria en localStorage. Se resetea automáticamente cada día (la clave incluye la fecha).

```javascript
var _waterGoal = 8;
var _waterPerGlass = 250; // ml

function hoyServer() {
  return new Date().toLocaleDateString('sv-SE', { timeZone: 'Europe/Madrid' });
}

function getWaterCount() {
  try {
    var w = localStorage.getItem('mf_water_' + hoyServer());
    return w ? parseInt(w) : 0;
  } catch(e) { return 0; }
}

function setWaterCount(n) {
  try { localStorage.setItem('mf_water_' + hoyServer(), n); } catch(e) {}
}

function addWater() {
  var count = getWaterCount() + 1;
  setWaterCount(count);
  updateWaterUI();
  if (count >= _waterGoal) showToast('¡Hidratación completada!', ...);
  else showToast('Vaso registrado', count * _waterPerGlass + ' ml', 'info');
}
```

**Pitfalls:**
- Envolver localStorage en try/catch (puede estar deshabilitado)
- La clave incluye la fecha → reseteo automático diario
- Llamar `updateWaterUI()` al cargar la página
- No persistir en database.json → localStorage es suficiente

## Proyecciones (framework)

Ver `references/weight-analysis.md` para el framework completo.

### Escenarios de proyección

El dashboard muestra 5 escenarios en la tabla y el chart:

| Escenario | Ritmo | Cálculo |
|-----------|-------|---------|
| 📈 **Real (últ. 7d)** | Dinámico | Media real de bajada de los últimos 7 días de peso |
| 🌱 Sostenible | 0,3 kg/sem | Déficit ~230 kcal/día |
| 🚶 Normal | 0,5 kg/sem | Déficit ~380 kcal/día |
| 🔥 Acelerado | 0,7 kg/sem | Déficit ~550 kcal/día (recomendado) |
| ⚡ Agresivo | 1,0 kg/sem | Déficit ~770 kcal/día |

### Cálculo del ritmo real (últimos 7 días)

```javascript
function calcularRitmoReal(peso) {
  var peso7d = peso.slice(-7);
  if(peso7d.length < 2) return 0.3; // fallback a sostenible
  var pInicio = peso7d[0].peso_kg;
  var pFin = peso7d[peso7d.length-1].peso_kg;
  var dias = (new Date(peso7d[peso7d.length-1].fecha) - new Date(peso7d[0].fecha)) / 86400000;
  if(dias <= 0) return 0.3;
  return Math.max(0, (pInicio - pFin) / dias * 7);
}
```

### Patrón: añadir nuevo escenario al dashboard

1. **renderProyecciones(pesoActual, objetivo, peso):** añadir el ritmoReal al array `ritmos` como primer elemento (destacado). Pasar `peso[]` para calcular.
2. **renderProyeccionChart(pesoActual, objetivo, ritmoReal):** añadir dataset `dR` con línea morada (#7c3aed), más gruesa (borderWidth:3), con puntos visibles (pointRadius:3).
3. **renderDashboard:** calcular `ritmoReal` al inicio y pasarlo a ambas funciones.
4. **Importante:** `renderProyeccionChart` también necesita recibir `ritmoReal` en su firma. NO calcular dentro de la función (código duplicado).

Ver `references/bebidas-alcoholicas.md` para macros de bebidas alcohólicas populares.

Ver `references/coach-personality.md` para el patrón de personalidad del coach IA Amadeo (humor negro, motivación extrema, lenguaje colega).
Ver `references/comidas-preparadas.md` para macros de comidas preparadas y ensaladas.
Ver `references/vinos.md` para macros de vinos (blanco, tinto, cava) y regla de cálculo por ABV.
Ver `references/dieta-nan-architecture.md` para el proyecto dieta-nan (dashboard + IA en NaN Builders).
Ver `references/template-packaging.md` para empaquetar como template público.

Ver `references/inbody-integration.md` para integrar datos de composición corporal (InBody) en la DB.
Ver `references/inbody-3d-v31.md` para la implementación v3.1: 3D con segmentos InBody reales (músculo+grasa por segmento), entrenos por zona muscular con detección automática, doughnut composición 6 componentes, media móvil en gráficos de peso, tracker de hidratación.

TMB (Mifflin-St Jeor, hombre): `10 × peso(kg) + 6.25 × altura(cm) - 5 × edad(años) + 5`
- David: ~1.892 kcal/día a 98 kg, 174 cm, 36 años

### 🔥 CRÍTICO: Verificar edad con usuario, NO asumir

**Error real:** La DB tenía edad 45, David tiene 36. Esto subestimó TMB en ~82 kcal y TDEE en ~83-150 kcal según nivel de actividad.

**Regla:** Si un dispositivo externo (InBody, báscula inteligente) reporta edad diferente a la DB, **siempre preguntar al usuario** antes de asumir. La edad puede haber cambiado, o el dispositivo puede tener datos incorrectos.

**Correcto:**
1. Leer edad de DB → si es 45 y InBody dice 36 → preguntar "¿tienes 36 o 45?"
2. Si el usuario confirma edad diferente → actualizar DB inmediatamente
3. Recalcular TMB/TDEE con la edad correcta

TDEE:
- Sedentario (x1.2): ~2.270 kcal (David 36 años)
- Ligero (x1.375): ~2.602 kcal ← usado por defecto
- Moderado (x1.55): ~2.933 kcal

Ritmos:
- 0,3 kg/sem → sostenible (déficit ~230 kcal/día)
- 0,5 kg/sem → normal (déficit ~380 kcal/día)
- 0,7 kg/sem → acelerado (déficit ~550 kcal/día) ← recomendado
- 1,0 kg/sem → agresivo (déficit ~770 kcal/día)

### Edición inline en estimación (Preview-Edit-Confirm)

Cuando se estima comida o ejercicio vía IA, el usuario debe poder **editar los valores antes de confirmar**:

1. **Estimar** → llamar a `/api/estimar-comida` o `/api/estimar-ejercicio`
2. **Mostrar preview editable** → en el `#comida-est-box` o `#ejercicio-est-box`, renderizar `<input>` en vez de `<span>` para cada campo
3. **Leer inputs al confirmar** → en `registrarComida()`/`registrarEjercicio()`, leer todos los `document.getElementById('ed-*')` y construir el body con los valores editados
4. **Hora incluida en la estimación** → el input `time` también se edita en preview

```javascript
// Patrón de caja editable (comida):
document.getElementById('comida-est-box').innerHTML =
  '<div class="estimation-box">' +
    '<div class="eb-row"><span>🕐 Hora</span><input type="time" id="ed-comida-hora" value="' + hora + '"></div>' +
    '<div class="eb-row"><span>🍽️ Descripción</span><input type="text" id="ed-comida-desc" value="' + escapeHtml(desc) + '"></div>' +
    '<div class="eb-row"><span>🔥 Calorías</span><input type="number" id="ed-comida-kcal" value="' + data.kcal + '"> kcal</div>' +
    '<div class="eb-row"><span>🥩 Proteínas</span><input type="number" id="ed-comida-prot" value="' + data.proteinas_g + '"> g</div>' +
    ...
  '</div>';

// Al confirmar, leer inputs:
function registrarComida() {
  var horaEl = document.getElementById('ed-comida-hora');
  var body = {
    hora: horaEl ? horaEl.value : (comidaEstData.hora || ''),
    kcal: parseInt(document.getElementById('ed-comida-kcal').value) || 0,
    ... // leer todos los inputs editados
  };
  await api('/api/comida', { method: 'POST', body: body });
}
```

**CSS para cajas editables:** los `.eb-row` deben usar `display:flex;align-items:center;gap:6px` en vez de `justify-content:space-between` para que los inputs se alineen bien.

### Input de hora en todos los registros

Cada formulario de registro debe incluir un `<input type="time">` para la hora:
- **Peso:** `id="peso-hora"` → enviar `hora: hora` en POST /api/peso
- **Comida:** `id="comida-hora"` → se copia a `ed-comida-hora` editable en preview
- **Ejercicio:** `id="ejercicio-hora"` → se copia a `ed-ejer-hora` editable en preview

**Backend:** El server.js debe aceptar `hora` en POST y usar `hora || ahora()` como fallback, nunca valores hardcodeados como `'mañana'`.

**Columnas PUT:** Añadir `'hora'` a los arrays `COLUMNS[table]` para peso, comidas y entrenamientos, permitiendo editar la hora via PUT.

### Navegación entre días en Resumen

El resumen del día debe permitir moverse a días anteriores/posteriores:

1. **Estado:** `appState.resumenDate` (inicializado a `today()` al primer render)
2. **Botones:** `◀` (restar 1 día) → `▶` (sumar 1 día) → `Hoy` (reset a today)
3. **Funciones:**
```javascript
function navegarResumen(delta) {
  var d = new Date(appState.resumenDate);
  d.setDate(d.getDate() + delta);
  appState.resumenDate = d.toLocaleDateString('sv-SE');
  renderResumen(); // re-renderiza con la nueva fecha
}
function irHoyResumen() {
  appState.resumenDate = today();
  renderResumen();
}
```
4. **Filtrado:** en lugar de `var d = today()`, usar `var d = appState.resumenDate` para filtrar datos

### Ocultar secciones no desarrolladas

Cuando una sección (InBody, Progreso 3D) no tiene sentido o no está desarrollada:
1. **Quitar tab-pane del HTML** → eliminar `<div class="tab-pane" id="tab-xxx">`
2. **Quitar del overflow menu** → eliminar el `<button>` correspondiente
3. **Quitar del renderTab** → eliminar `case 'xxx':`
4. **Quitar de proyecciones** → eliminar el bloque HTML y la variable que lo referencia
5. **No borrar la función render ni save** — pueden quedar como código muerto pero no rompen nada
6. **La función renderProgreso3D() puede quedar** (no se llama desde ningún lado tras los pasos 1-3) — es código muerto inofensivo

### 🔥 CRÍTICO: CSS para inputs en estimation-box

Cuando se cambia `.eb-row` de `justify-content:space-between` a `display:flex;align-items:center;gap:6px;flex-wrap:wrap`, asegurarse de que los `<span>` hijos tengan `min-width:85px` para mantener la alineación vertical incluso cuando hay inputs en vez de solo spans.

### Endpoints genéricos

```javascript
// Borrar: DELETE /api/:tipo/:index
// Tipos válidos: peso, comidas, deporte, pasos
fetch('/api/comidas/5', { method: 'DELETE' })

// Editar: PUT /api/:tipo/:index (merge de campos, no toca fecha/hora)
fetch('/api/comidas/5', {
  method: 'PUT',
  headers: {'Content-Type':'application/json'},
  body: JSON.stringify({ kcal: 500, descripcion: 'corregido' })
})
```

### Patrón de edición inline en frontend

1. Botón ✏️ en la lista → `editarComida(idx)` rellena el formulario existente
2. Cambia el botón submit a "Actualizar Comida" (cambia clase CSS)
3. `_editandoComidaIdx = idx` → al hacer submit, detecta si es POST (nuevo) o PUT (editar)
4. Tras actualizar, restaura botón y `_editandoComidaIdx = -1`

```javascript
var _editandoComidaIdx = -1;
function registrarComida(e) {
  var url = _editandoComidaIdx >= 0 ? '/api/comidas/' + _editandoComidaIdx : '/api/comida';
  var method = _editandoComidaIdx >= 0 ? 'PUT' : 'POST';
  // ... fetch(url, {method, body}) ...
  // Tras éxito: _editandoComidaIdx = -1; restaurar botón;
}
```

### Confirmación antes de borrar

Siempre `confirm('¿Seguro que quieres borrar este registro?')` antes de DELETE.

### 🔥 CRÍTICO: `function` con asignación rompe todo el script

**Error real:** `function _originalRegistrarComida = null;` → SyntaxError que detiene TODA la ejecución del `<script>`. El dashboard carga el HTML pero los KPIs quedan en "--" y los charts vacíos.

**Causa:** usar `function` donde se necesita una declaración de variable. En JS, `function` solo sirve para declarar funciones, no para asignar valores.

**Correcto:** `var _originalRegistrarComida = null;`

**Síntoma:** HTML carga, CSS aplica, pero `typeof loadData === 'undefined'`, `typeof charts === 'undefined'`. El script no ejecuta nada.

**Verificación rápida:** en DevTools, `typeof window.loadData` — si es `undefined`, hay un error de sintaxis en el script que impide su ejecución.

### 🔥 CRÍTICO: Duplicación de `const` → SyntaxError silencioso → página en blanco

**Error real (2026-06-13):** `const isDark = const isDark = body.getAttribute('data-nz-theme') === 'dark';` — duplicación de `const` que causa un SyntaxError.

**Por qué es tan peligroso:** el error es un **SyntaxError**, no un ReferenceError. Esto significa que el motor JS NUNCA llega a ejecutar NADA del script. No hay console.error, no hay stack trace, no hay nada visible. El HTML se renderiza, el CSS se aplica, pero el JS nunca se ejecuta. El dashboard aparece con todos los KPIs en "--" y los charts vacíos.

**Cómo detectarlo:**
1. **Síntoma:** HTML carga, CSS se ve bien, pero NADA funciona (no hay KPIs, no hay charts, no hay interactividad)
2. **Verificar:** `grep -n 'const.*const\|let.*let\|var.*var' dashboard.html` — busca patrones de duplicación
3. **Buscar asignaciones a `function`:** `grep -n 'function.*=.*null\|function.*=.*false' dashboard.html`
4. **Causas comunes:** copiar/pegar sin borrar, refactorizar dejando duplicados, `const x = const x = ...`

**Correcto:** siempre usar una sola asignación por variable.

**Verificación post-fix:** `grep -n 'const.*const\|let.*let\|var.*var' dashboard.html` debe devolver 0 resultados.

## Sync automático a GitHub

**Problema:** NaN containers pierden datos en redeploy. El filesystem del contenedor es volátil.

**Solución:** `syncGitHub(db)` tras cada mutación (crear/editar/borrar). Usa GitHub Contents API sin necesidad de git en el contenedor.

```javascript
async function syncGitHub(db) {
  const token = getNanToken();
  if (!token) return;
  // 1. Obtener SHA actual
  const getRes = await fetch('https://api.github.com/repos/Ntizar/dieta/contents/data/database.json', {
    headers: { 'Authorization': `Bearer ${token}`, 'Accept': 'application/vnd.github.v3+json' }
  });
  const { sha } = await getRes.json();
  // 2. Subir contenido actualizado (base64)
  const b64 = Buffer.from(JSON.stringify(db, null, 2)).toString('base64');
  await fetch('https://api.github.com/repos/Ntizar/dieta/contents/data/database.json', {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: `MasterFit: actualización ${new Date().toISOString().slice(0,19)}`,
      content: b64, sha
    })
  });
}
```

**Llamar a `syncGitHub(db)` en TODOS los endpoints de mutación:** POST peso/comida/deporte, PUT, DELETE.

**Pitfall:** si el token no tiene permisos de escritura en el repo, el sync falla silenciosamente (solo log en consola). Verificar con `curl -H "Authorization: Bearer $TOKEN" https://api.github.com/repos/Ntizar/dieta`.

### 🔥 CRÍTICO: initDB() descarga DB de GitHub al iniciar (v5.0.0+)

El deploy de NaN **reinicia el contenedor** en cada deploy. Antes de v5.0.0, `initDB()` solo leía la DB local y creaba tablas vacías si no existía → cada contenedor era una DB aislada sin datos.

**Solución actual:** `initDB()` llama a `downloadGitHubDB()` que descarga `masterfit.db` de GitHub al iniciar. Si falla, fallback a DB local.

**Token:** `downloadGitHubDB()` lee `GITHUB_TOKEN` de `process.env` primero, luego de `.env` del proyecto (`path.join(__dirname, '.env')`). **NUNCA leer de `/hermes-home/.env`** — ese archivo no existe dentro del contenedor de NaN.

**Verificación post-deploy:** Después de cada redeploy, verificar que el deploy tiene datos:
```bash
# Login y obtener session ID
curl -s -X POST -H 'Content-Type: application/json' \
  https://dieta-ntizar-ntizar.apps.nan.builders/api/auth/login \
  -d '{"nombre":"David Antizar","pin":"5101"}' | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('sessionId',''))"
# Usar session ID con X-Session-Id header para /api/datos
curl -s -H 'X-Session-Id: <session_id>' \
  https://dieta-ntizar-ntizar.apps.nan.builders/api/datos | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('comidas',[])), 'comidas')"
```

**Si el deploy devuelve 0 comidas tras redeploy:** El deploy aún se está iniciando. NaN Builders puede tardar 2-5 minutos en levantar el contenedor nuevo. Reintentar después de 2 minutos.

### 🔥 CRÍTICO: LladosApp usa SQLite, NO database.json

LladosApp (el dashboard que usa David) se alimenta de `data/masterfit.db` (SQLite), **NO** de `data/database.json` (legacy JSON).

**Procedimiento correcto para registrar comida/peso/deporte:**

1. **Siempre escribir en SQLite** (`masterfit.db`) — es la fuente de verdad de LladosApp
2. Usar `sqlite3` o `import sqlite3` para INSERTar directamente en las tablas (`comidas`, `peso`, `entrenamientos`, `pasos`)
3. **NO editar database.json** — es un formato legacy que LladosApp no lee en producción
4. El endpoint `POST /api/comida` en server.js INSERTa en SQLite, no en JSON
5. Commit y push de `data/masterfit.db` tras cada mutación

**Pitfall real (2026-06-16):** Se metieron datos en database.json y el usuario dijo "no estás poniendo los datos al usuario David Antizar cuando te lo digo… en LladosApp". La app no veía los datos porque leen de SQLite, no de JSON.

**Siempre verificar la DB real de la app ANTES de escribir datos.**

### 🔥 CRÍTICO: Verificar datos en deploy ANTES de confirmar

Cuando se registran datos en LladosApp:
1. Escribir en SQLite local (`masterfit.db`)
2. Commit + push de `masterfit.db`
3. **Verificar en el deploy** que los datos aparecen — no asumir que el push es suficiente
4. Si el deploy está vacío, puede ser que:
   - El deploy aún se está iniciando (esperar 2-5 min)
   - `downloadGitHubDB()` falló (verificar token en `.env` del proyecto)
   - El deploy tiene caché (forzar Ctrl+Shift+R)

**Verificar siempre con curl usando X-Session-Id header**, no con cookies (las cookies no se mantienen bien entre requests de curl).

### 🔥 CRÍTICO: Olvidar `readDB()` al usar `contextoPerfil(db)`

Cuando se crea un nuevo endpoint que usa `contextoPerfil(db)` o `perfilUsuario(db)`, **siempre añadir `const db = readDB();` al inicio del endpoint** antes de usar esas funciones. Sin esto, `db` no está definido → el catch devuelve `{estimado: false, error: "db is not defined"}` → el frontend muestra "⚠️ Sin estimación" sin explicación clara.

**Error real:** al refactorizar los endpoints de estimación para usar perfil dinámico, se añadió `contextoPerfil(db)` pero se olvidó `readDB()` en el scope del endpoint.

**Correcto:**
```javascript
app.post('/api/estimar-comida', async (req, res) => {
  const { descripcion, tipo } = req.body;
  if (!descripcion) return res.status(400).json({ error: 'Descripción requerida' });

  const db = readDB();  // ← OBLIGATORIO antes de contextoPerfil(db)
  const token = getNanToken();
  // ... usar contextoPerfil(db) en el prompt ...
});
```

**Verificación:** si un endpoint devuelve `"db is not defined"`, buscar si falta `readDB()`.

## Modo Oscuro/Claro (Dark Mode)

**Feature v3.1:** Toggle de tema oscuro/claro con persistencia en localStorage.

### Implementación

- Botón en header: `🌙 Oscuro` / `☀️ Claro` (función `toggleDarkMode()`)
- Clase CSS `mf-dark` en `<body>` que activa ~40 reglas de estilo oscuro
- Persistencia: `localStorage.setItem('mf-dark-mode', '1')` / `'0'`
- Al cargar, restaurar preferencia: `localStorage.getItem('mf-dark-mode') === '1'`
- El canvas 3D de Three.js cambia fondo: `#f0f4ff` (claro) ↔ `#1e293b` (oscuro)
- Aplicar `data-nz-theme="dark"` al body para que Aurora respete el tema

### CSS Dark Mode

Las reglas `body.mf-dark` cubren:
- Tarjetas glass (`.nz-card`, `[style*="rgba(255,255,255,0.7)"]`) → fondo `rgba(30,41,59,0.85)`
- KPIs, textos, badges, inputs, selects, toasts, tabs, chat IA, listas
- Progress bars dentro de KPIs (3 gradientes: proteína, hidratos, grasas)
- Botones secondary → fondo oscuro con hover

### Regla para añadir temas visuales nuevos

Siempre añadir reglas CSS con `body.mf-dark` para cada nuevo componente visual que se añada al dashboard. No dejar componentes sin cobertura dark mode.

## Mejora Iterativa — Patrón de Cron Job

**Procedimiento para cada tick del cron job de mejora iterativa:**

1. **Analizar código actual** → leer dashboard.html, server.js, database.json
2. **Verificar estado** → `node -c server.js`, `curl` healthz del deploy
3. **Priorizar** → seguir la lista de prioridades del cron (bugs → UX → features → optimización)
4. **Implementar** → solo añadir o modificar, NUNCA borrar
5. **Verificar** → sintaxis HTML/JS, sintaxis server.js, no romper Three.js
6. **Commit + push** → `git add`, `git commit -m`, `git push origin main`
7. **Actualizar versión** → `data/database.json` → `meta.version` y `meta.features`
8. **Entregar resumen** → qué se mejoró, archivos, cómo probar, siguiente mejora

### Lista de prioridades de mejora (actualizar cada vez que se complete una)

1. ✅ Bug fix — app carga en NaN
2. ✅ Toast notifications
3. ✅ Modo oscuro/claro toggle
4. ✅ Exportación de datos a CSV
5. ✅ Pulido visual Aurora glass-liquid (v3.3) — KPIs premium, tabs pill, animaciones fade-in, inputs glass, chat glass, modal export mejorado
6. ✅ Tracker de agua completo (v4.0.1) — UI en tab Registrar, quick-add buttons, progreso diario, chip en resumen
7. ✅ Fix endpoint `/api/perfil` faltante (config tab funcional)
8. ✅ Fix field name mismatch `peso_objetivo_kg` (proyecciones y config)
9. ✅ Multi-usuario: selector de perfiles, login sin restricción, endpoint /api/auth/usuarios
10. ✅ Onboarding IA: Amadeo entrevista al usuario nuevo paso a paso (5 preguntas)
11. ✅ Gráfico de progreso de macros (proteínas, hidratos, grasas) — donut chart con TDEE Mifflin-St Jeor
12. ❌ Modo oscuro/claro toggle
13. ❌ Modo offline con localStorage
14. ❌ Sistema de logros/badges
15. ❌ Comparativa con objetivos diarios
16. ❌ Mejora de accesibilidad (ARIA labels, contraste)

### 🔥 CRÍTICO: Prioridad de mejoras = diseño visual > nuevas features

**Corrección del usuario (2026-06-13):** David dijo explícitamente que las próximas mejoras deben ir por el camino de **diseño visual con Aurora glass-liquid**, no por añadir nuevas funcionalidades.

**Regla:** Cuando se hace mejora iterativa en el dashboard de dieta:
- **Primero:** pulir diseño visual (glass-liquid, espaciado, tipografía, animaciones, interacciones, sombras, bordes, hover effects)
- **Segundo:** optimizar UX (transiciones, feedback visual, consistencia)
- **Tercero:** añadir features nuevas (solo si el diseño ya está pulido)

**No añadir features nuevas mientras el diseño visual sea mejorable.** El usuario prefiere que se vea bien antes de que tenga más opciones.

### 🔥 CRÍTICO: Validar sintaxis ANTES de commit

**Procedimiento obligatorio post-modificación:**
1. `node -c server.js` → debe devolver exit 0
2. Extraer JS del `<script>` y verificar balance de braces/parens/brackets
3. `grep -n 'const.*const\|let.*let\|var.*var' dashboard.html` → debe devolver 0
4. `grep -n 'function.*=.*null' dashboard.html` → debe devolver 0
5. Si algún check falla → NO hacer commit, corregir primero

### 🔥 CRÍTICO: `const charts` vs `var charts` en frontend

En dashboard.html, SIEMPRE usar `var charts = window.charts = {};` para el objeto charts. NUNCA `const charts` ni `let charts`. Esto evita que Chart.js destruya charts al re-renderizar tabs.

### 🔥 CRÍTICO: Config save field name mismatch

**Bug encontrado (2026-06-14):** `saveConfig()` en dashboard.html usa `body.objetivo_peso_kg` pero el backend espera `body.peso_objetivo_kg`. Esto hace que el campo "objetivo peso" en configuración se guarde como un campo desconocido y se pierda.

**Regla:** Cuando se modifica un campo en el frontend, verificar que el nombre coincide EXACTAMENTE con lo que espera el backend. Si el backend usa `peso_objetivo_kg`, el frontend debe enviar `peso_objetivo_kg`.

### 🔥 CRÍTICO: Onboarding step variable scope bug

**Bug encontrado (2026-06-14):** `sendOnboardingAnswer()` referencia la variable `step` del scope exterior pero después de incrementar `_onboardingPaso++`, `step` sigue apuntando al paso anterior. Esto hace que la confirmación muestre datos incorrectos.

**Correcto:** leer el step actual desde `ONBOARDING_STEPS[_onboardingPaso]` dentro de la función, no desde una variable exterior que puede estar desincronizada.

### 🔥 CRÍTICO: Verificar deploy ANTES de reportar "hecho" en cron

**Problema real (2026-06-13):** El cron job de mejora iterativa reportó "Modo Oscuro/Claro Toggle" como mejora realizada, pero David no lo veía en la web y preguntó si realmente se había hecho.

**Verificación:** `curl -s https://dieta-ntizar-ntizar.apps.nan.builders/ | grep -o 'toggleDarkMode\|mf-dark'` confirmó que SÍ estaba en el deploy. El deploy era idéntico al local (128066 bytes).

**Causa:** El cron marcaba prioridades como ✅ pero el usuario no veía los cambios porque su navegador tenía caché antigua.

**Solución:** Cuando el cron reporta una mejora visual (UI), verificar con curl que los elementos específicos están en el HTML del deploy. Si están, informar al usuario que puede necesitar **Ctrl+Shift+R** (recarga forzada) para verlos.

**Patrón de verificación:**
```bash
# Verificar feature específica en el deploy
curl -s https://dieta-ntizar-ntizar.apps.nan.builders/ | grep -o 'NOMBRE_FEATURE'

# Verificar que deploy == local
curl -s https://dieta-ntizar-ntizar.apps.nan.builders/ | wc -c
wc -c /root/workspace/dieta-masterfit/dashboard.html
```

Si ambos dan el mismo byte count → deploy actualizado. Si el usuario no ve cambios → caché del navegador.

## Pitfalls
- **Actualizar SEGUIMIENTO.md después de database.json** para mantener consistencia
- **No borrar database.json** — es la fuente de verdad
- **Commit siempre** tras cada modificación
- **El dashboard carga database.json vía fetch** — necesita servidor HTTP local o abrir con Live Server
- **Chart.js desde CDN** — necesita internet para cargar
- **NaN containers pierden filesystem en redeploy** — por eso syncGitHub() es obligatorio en cada mutación
- **syncGitHub() es async pero no await** — se lanza en background, no bloquea la respuesta al usuario. Si falla, el dato se guarda localmente pero no en GitHub

### 🔥 CRÍTICO: Botón no funciona → verificar endpoint del backend ANTES que el frontend

**Error real (2026-06-11):** Botón "Registrar Ejercicio" no hacía nada. El frontend llamaba a `/api/deporte` pero el endpoint en server.js era `/api/entrenamiento`.

**Debugging:**
1. `search_files` en `server.js` para endpoints (`app.post|app.get|app.put`)
2. `search_files` en `dashboard.html` para ver qué endpoint llama el frontend
3. Comparar nombres — si no coinciden, ese es el bug
4. Probar con `curl` directamente para verificar

**Regla:** El 90% de "botones que no funcionan" son endpoints inexistentes o mal nombrados, NO bugs de JavaScript.

### 🔥 CRÍTICO: Frontend/Backend field name mismatch

**Error real (2026-06-13):** El frontend usaba `perfil.objetivo_peso_kg` pero el backend devolvía `perfil.peso_objetivo_kg`. Esto causaba que el tab de proyecciones mostrara el objetivo como 75 (fallback) en vez del valor real de la DB, y el tab de configuración no cargaba el valor guardado.

**Patrón:** Los nombres de campos en frontend y backend deben ser idénticos. Si el backend devuelve `peso_objetivo_kg`, el frontend debe leer `datos.perfil.peso_objetivo_kg`.

**Debugging:**
1. `curl` al endpoint `/api/datos` para ver la estructura real de la respuesta
2. Comparar cada campo que usa el frontend con la respuesta real
3. Buscar `search_files` en dashboard.html para ver qué campos lee
4. Verificar con `grep` los nombres de campos en ambos archivos

**Regla:** NUNCA asumir que los nombres de campos coinciden. Siempre verificar con `curl /api/datos` primero.

### 🔥 CRÍTICO: Endpoint faltante en backend

**Error real (2026-06-13):** El tab de configuración llamaba a `POST /api/perfil` pero ese endpoint no existía en server.js. La configuración no se guardaba y no había error visible (el toast decía "Error al guardar" pero no era obvio por qué).

**Debugging:**
1. `search_files` en server.js para ver qué endpoints existen
2. `search_files` en dashboard.html para ver qué endpoints llama el frontend
3. Si el frontend llama a un endpoint que no existe → crearlo
4. El endpoint debe seguir el patrón: `requireAuth`, leer campos del body, actualizar DB, `saveDB()`, `syncGitHub()`

**Regla:** Cuando se añade un nuevo formulario en el frontend, verificar que el endpoint backend existe. Si no, crearlo en el mismo commit.

### 🔥 CRÍTICO: Pasos del día — registrar desde la herramienta, no solo Telegram

**2026-06-11:** Se añadió un card "Pasos del Día" en la tab "Registrar" del dashboard.

**Formulario:**
- Campo obligatorio: pasos (número)
- Campos opcionales: distancia (km), kcal quemadas
- Botón "🤖 Auto" que calcula automáticamente:
  - Distancia: ~0.75m por paso (`pasos * 0.00075`)
  - Kcal: ~0.04 por paso (`pasos * 0.04`)
- Endpoint: `POST /api/pasos` con `{pasos, distancia_km, kcal}`
- Actualiza entrada del día si ya existe (no duplica)
- El endpoint acepta también `notas`

**Endpoint `/api/pasos` (actualizado 2026-06-11):**
```javascript
// Body: { pasos, distancia_km?, kcal?, notas? }
// Response: { ok: true, mensaje: "8500 pasos registrados" }
// Actualiza entrada existente si ya hay datos para hoy
```

### 🔥 CRÍTICO: Registro por voz — parsear texto hablado

Cuando el usuario dicta una comida por voz:
- **El texto transcrito tiene errores fonéticos** — "manesutinta" = "munesutinta" = pulpo de pota/cachuelo en su tinta
- **"dieta coldo e añade"** = "dieta, mastermind, añade" — ignorar "coldo e"
- **Inferir datos nutricionales** cuando el usuario solo describe comida:
  - Arroz basmati cocido: ~130 kcal/100g, 2.7p, 28h, 0.3g grasa
  - Manesutinta/pulpo de pota: ~85 kcal/100g, 18p, 0h, 1g grasa
  - Melocotón: ~60 kcal, 0p, 15h, 0g
  - Usar estimaciones razonables y registrarlas
- **Determinar tipo de comida por hora** — si no hay hora, asumir cena (21:00) si es último registro del día
- **Añadir hora "21:00" por defecto** para cenas sin hora especificada

### 🔥 CRÍTICO: Comidas futuras fantasmas

El usuario a veces añade comidas con fecha futura por error (ej: 11/06 cuando hoy es 09/06).
- **Al revisar database.json, siempre buscar entradas con fecha > hoy**
- **Si encuentra comidas futuras, preguntar antes de eliminar** — pero si el usuario dice "quítala", borrar sin dudar
- **Patrón de detección**: comidas con fecha > fecha actual + 1 día = probablemente error

### 🔥 CRÍTICO: El repo ya existe con remote y datos históricos

El repo `github.com/Ntizar/dieta.git` YA existe con remote configurado y 26+ commits históricos. **NO crear un repo nuevo ni asumir que no existe.** Pasos correctos:

1. **Verificar remote** con `git remote -v` ANTES de hacer nada
2. **Ver el log completo** con `git log --oneline --all` para ver el historial real
3. **Leer SEGUIMIENTO.md actual** — puede tener datos más recientes que database.json
4. **Migrar datos faltantes** del SEGUIMIENTO.md a database.json (no al revés)
5. **Hacer push** con `git push origin main` — no dejar commits locales sin subir

**Error cometido:** Ignoré el remote existente, no hice push del commit v2.0, y el database.json se quedó sin las últimas comidas del 09/06 que ya estaban en SEGUIMIENTO.md.

### 🔥 CRÍTICO: No dar largas al usuario

Cuando el usuario pregunta "¿cómo vas?" o "llevas mucho rato":
- **Soltar resultados inmediatamente**, no explicar lo que voy a hacer
- Si el HTML es grande, escribirlo de una vez con write_file, no planificarlo en voz alta
- No decir "voy a hacer X" sin hacer X — el usuario quiere ver progreso real, no promesas
- Priorizar entregar algo funcional aunque no sea perfecto sobre intentar hacerlo perfecto y no entregar nada

### 🔥 CRÍTICO: Bebidas alcohólicas — pedir ABV y tipo antes de estimar

Cuando el usuario menciona una bebida alcohólica, **NO asumir el tipo ni el ABV**:
- Volldamm normal (5.4% ABV) ≠ Volldamm Doble Malta (7.2% ABV) ≠ Volldamm Sin Alcohol (0%)
- **Siempre confirmar** el tipo exacto y el % ABV antes de estimar macros
- Si el usuario corrige (ej: "tiene 7.2%"), aceptar inmediatamente y ajustar
- Valores de referencia rápidos:
  - Cerveza 5% (330ml): ~150 kcal, 13g carbs
  - Volldamm Doble Malta 7.2% (330ml): ~200 kcal, 18g carbs, 24g alcohol
  - Volldamm Normal 5.4% (330ml): ~150 kcal, 13g carbs
  - Volldamm Sin Alcohol (330ml): ~65 kcal, 6g carbs
  - Vino tinto (150ml): ~125 kcal, 4g carbs
  - Gintonic: ~170 kcal, 10g carbs
  - Whisky (30ml): ~97 kcal, 0g carbs

### 🔥 CRÍTICO: Pasos duplicados o con valores legacy

Cuando se registra un día con pasos:
- **Comprobar si YA existe un entry de pasos para esa fecha** antes de añadir
- Si existe pero con un valor legacy/incorrecto (ej: 2000 que era un fallback), **actualizarlo en vez de duplicar**
- Buscar en el array `pasos` entradas con la misma `fecha` antes de añadir
- Si hay múltiples entradas para la misma fecha, mantener la más reciente y borrar las demás

Cuando el usuario dice "no incluiste los del día X" o similar:
- **NO asumir que no hay datos** — el usuario puede no haber dado el número exacto
- **Preguntar el número faltante** si no lo dio (no inventar)
- **Añadir SIEMPRE** lo que el usuario mencionó (bici, deporte, etc.) sin esperar confirmación
- **Comprobar si ya existe** la fecha en el array antes de añadir (duplicados)
- **Actualizar SEGUIMIENTO.md** en la sección correspondiente (pasos, deporte, comidas)
- **Commit + push** siempre, incluso si es solo corrección

### 🔥 CRÍTICO: Datos históricos en SEGUIMIENTO.md que no están en database.json

El archivo `SEGUIMIENTO.md` puede contener registros históricos (especialmente entrenos y pasos) que el usuario anotó antes de que existiera el sistema v3 con database.json.

**Síntoma:** el usuario dice "el 4 del 6 sí hice entreno y no está" → buscar en SEGUIMIENTO.md el texto "2026-06-04" en la sección de entrenamiento.

**Patrón de recuperación:**
1. Buscar en `SEGUIMIENTO.md` la fecha del registro faltante
2. Extraer descripción, duración, intensidad de la narrativa (ej: "2 min ski + 3x12 sentadillas + 2x20 flexiones, ~30 min, intensidad alta")
3. Crear entrada en `entrenamientos` con valores razonables:
   - `series`: contar grupos de ejercicios (ej: 5 ejercicios → series ≈ ejercicios × 2-3)
   - `reps_totales`: estimar ~120
   - `kcal_estimadas`: ~10 kcal/min para fuerza intensidad alta
   - `rpe`: 8 para alta, 5 para media, 3 para baja
4. Insertar al principio del array (orden cronológico inverso)
5. Actualizar CSVs
6. **Regenerar historico_diario.csv** para que el día muestre entreno=SÍ con las kcal correctas

## Template público — Empaquetar para distribución

Cuando se quiere compartir un proyecto de dieta con la comunidad (ej: NaN builders):

### Flujo de empaquetado

1. **Crear carpeta limpia** (ej: `dieta-template/`) — NUNCA modificar el original
2. **Limpiar database.json** → estructura vacía con campos editables (nombre placeholder, peso/altura genéricos)
3. **Limpiar server.js** → quitar referencias a personas (David, Amadeo, Koldo), hardcodear repo genérico o usar env vars
4. **Limpiar dashboard.html** → reemplazar nombres, eliminar datos personales, mantener funcionalidad
5. **Crear README.md como guía de instalación** → 10+ pasos detallados, no solo descripción
6. **Crear .env.example** → plantilla con instrucciones, NUNCA con tokens reales
7. **Crear .gitignore** → debe excluir `.env` y `node_modules`
8. **Crear index.html** → landing page con CSS puro (NO dependencias de Aurora que fallan en GitHub Pages)
9. **Verificación de seguridad** → escanear todo el proyecto en busca de API keys, nombres, emails
10. **Crear repo GitHub público** → API o `gh` CLI, sin `.git` init (dejarlo vacío)
11. **Subir archivos** → via API GitHub Contents o git clone + copy + push
12. **Activar GitHub Pages** → POST a `/repos/{owner}/{repo}/pages` con `source: {branch: 'main', path: '/'}`
13. **Esperar build** → estado cambia de `building` a `built` (1-3 min)

### Pitfalls de empaquetado

- **NUNCA incluir `.env`** → siempre `.env.example` con placeholder
- **NUNCA incluir `node_modules/`** → siempre en `.gitignore`
- **NUNCA incluir datos personales** → database.json vacía con estructura
- **CSS en landing page** → usar CSS puro, NO Aurora (falla en GitHub Pages por variables no definidas)
- **Dashboard vs Landing** → el dashboard usa Aurora (funciona con Express), la landing NO (CSS puro)
- **Token de API** → solo en `.env`, solo en variables de entorno de NaN, NUNCA en código ni docs
- **Repo template** → el `syncGitHub` del server.js debe apuntar a repo configurable vía env vars, no hardcodeado

### 🔥 CRÍTICO: CDN de Aurora — nombre del repo

El repo de Aurora se llama **`Ntizar/Ntizar-Aurora`** (con guion), NO `Ntizar/Aurora`.

- `https://cdn.jsdelivr.net/gh/Ntizar/Aurora@latest/ntizar.css` → **404** ❌
- `https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@latest/ntizar.css` → **200** ✅

Si el dashboard se ve como HTML crudo (sin estilos, sin colores, sin gráficas), verificar que TODOS los `<link>` de Aurora usan `Ntizar/Ntizar-Aurora` (con guion). El error más común: el dashboard tiene `Ntizar/Aurora` (sin guion) → 8 CSS fallan → 0 estilos → HTML plano.

**Verificación rápida:** `curl -sI https://cdn.jsdelivr.net/gh/Ntizar/Aurora@latest/ntizar.css` → si devuelve 404, cambiar a `Ntizar/Ntizar-Aurora`.

### 🔥 CRÍTICO: index.html = dashboard para GitHub Pages

Cuando se despliega en GitHub Pages, **la landing page debe ser el dashboard**, no una landing estática con CSS puro. Si el index.html es una landing page con CSS puro, se ve cutre comparado con el dashboard real.

**Solución:** Copiar `dashboard.html` como `index.html` → la landing es el dashboard con Aurora completo. La landing page estática solo tiene sentido si se sirve desde un servidor Express (que gestiona los assets), no desde GitHub Pages estático.

### Verificación de seguridad

Escanear todo el proyecto con grep para:
- Nombres propios (David, Ntizar, Antizar, Amadeo, Koldo)
- Patrones de API keys (`sk-[a-zA-Z0-9]{20,}`)
- Emails
- URLs de repos personales

Ignorar: referencias a CDN de Aurora (públicas), `.env.example` (plantilla), créditos al autor original en README.

Ver `references/template-packaging.md` para detalles del procedimiento.

Ver `references/macros-chart.md` — patrón de implementación del gráfico de macros con donut chart y cálculo TDEE Mifflin-St Jeor.
Ver `references/objetivos-diarios.md` — patrón de grid de objetivos diarios con 6 tarjetas de progreso (calorías, proteínas, agua, hidratos, grasas, pasos).

Ver `references/patch-safety-fuzzy-matching.md` — pitfall de fuzzy matching en `skill_manage(action='patch')` con archivos HTML/JS grandes. Reglas de seguridad y verificación post-patch.

Ver `references/multi-usuario-onboarding.md` — implementación multi-usuario y onboarding IA: endpoints, flujos de prueba, errores encontrados.

Ver `nan-deploy-sync` — skill para verificar y forzar sync de deploy NaN con GitHub, downloadGitHubDB, verificación post-deploy con X-Session-Id.
