---
name: freehands-architecture
description: "Arquitectura completa del proyecto FreeHands — control del PC sin manos: mirada + gestos + voz. Módulos, flujos de datos y patrón para añadir nuevas funcionalidades."
version: 4.0.0
author: Ntizar
tags: [mastermind, freehands, gaze, gestures, voice]

---

# FreeHands — Arquitectura del Proyecto

Proyecto de control del PC sin manos: **gaze tracking + gestos de mano + comandos de voz**. PyQt6 + MediaPipe FaceMesh + pyautogui.

## 📁 Estructura del proyecto

```
src/freehands/
├── __main__.py              # Entry point: freehands CLI
├── main.py                  # run_system() — orquestador principal
├── config.py                # Constantes globales (FPS, dwell, thresholds)
├── gaze/
│   ├── __init__.py          # Exporta GazeTracker, GazeRegressor, DeadZoneClamper
│   ├── tracker.py           # GazeTracker — MediaPipe FaceMesh → GazeFeatures (6-d)
│   ├── calibration.py       # GazeRegressor — ridge regression → coordenadas pantalla
│   ├── dead_zones.py        # DeadZoneClamper — recorte de bordes de pantalla
│   └── head_pose.py         # HeadPose — estimación 6DoF desde FaceMesh landmarks
├── gestures/
│   ├── hand_tracker.py      # MediaPipe Hands → gesture classification
│   ├── face_tracker.py      # Expresiones faciales (AUs)
│   └── stabilizer.py        # Debounce + stability frames para gestos
├── fusion/
│   ├── fusion.py            # MultimodalFusion — estado, dwell, bindings
│   ├── state_machine.py     # StateMachine — IDLE → ACTIVE → CONFIRMING → COOLDOWN
│   └── channel_priority.py  # Priorización dinámica: gesto vs voz cuando compiten
├── actions/
│   └── dispatcher.py        # ActionDispatcher — pyautogui (click, scroll, zoom...)
├── voice/
│   ├── whisper_listener.py  # Faster-Whisper ASR → acciones de voz
│   └── continuous_dictation.py  # Transcripción continua con feedback visual
├── plugins/
│   ├── base.py              # FreeHandsPlugin base class — 7 pipeline hooks
│   ├── loader.py            # PluginLoader — discovery, priority, lifecycle
│   └── example_cursor_trail.py  # Ejemplo: trail de cursor
├── profiles/
│   ├── store.py             # Profile (Pydantic) — JSON persistence, migration
│   └── __init__.py          # Gestos, bindings, thresholds por defecto
├── capture/
│   ├── camera.py            # OpenCV webcam capture
│   └── __init__.py
└── ui/
    ├── overlay.py           # GazeOverlay — widget PyQt6 transparente
    ├── theme.py             # Estilos CSS (azul #1E5BFF + naranja #FF7A1A)
    ├── calibration_game.py  # Juego de calibración 9 puntos
    └── camera_selector.py   # Selector de cámara
tests/
├── test_dead_zones.py       # Tests dead zones
├── test_fusion.py           # Tests multimodal fusion
├── test_state_machine.py    # Tests state machine
├── test_profiles.py         # Tests profiles
├── test_hand_tracker.py     # Tests hand tracker
├── test_stabilizer.py       # Tests gesture stabilizer
├── test_voice_commands.py   # Tests voice commands
└── test_head_pose.py        # Tests head pose estimation
```

## 🔄 Flujo de datos principal

```
Camera ──frame──▶ GazeTracker ──GazeFeatures──▶ GazeRegressor ──cursor (x,y)
                                                        │
                                                    DeadZoneClamper ──cursor_clamped
                                                        │
                                               FineAimPointer ──cursor_smooth
                                                        │
HandTracker ──gesture──▶ GestureStabilizer ──confirmed_gesture
                                                        │
                              ┌─────────────────────────┘
                              ▼
                        MultimodalFusion
                        (state machine + dwell + bindings)
                              │
                              ▼
                        FusionResult {cursor_xy, state, dwell, fired_action}
                              │
                              ▼
                        PluginPipeline (hooks: on_gaze, on_action, ...)
                              │
                              ▼
                        ActionDispatcher ──pyautogui events
```

## 🔑 Conceptos clave

### GazeFeatures (6-dimensional)
Vector compacto extraído por frame:
- `l_rel[0:2]` — iris izquierdo normalizado por ancho/alto ojo izq
- `r_rel[0:2]` — iris derecho normalizado por ancho/alto ojo der
- `head[0:2]` — proxy de pose de cabeza (nariz vs centro ojos)

### State Machine
Estados: `IDLE → ACTIVE → CONFIRMING → COOLDOWN → ACTIVE`
- **IDLE**: sistema pausado (palma abierta → resume)
- **ACTIVE**: esperando mirada estable
- **CONFIRMING**: mirada estable durante dwell_time_ms
- **COOLDOWN**: tras acción, cooldown de COOLDOWN_MS_AFTER_ACTION

### Palm-scroll
Gestos de scroll por palma (palm_scroll_up/down) son **instantáneos** — bypass del state machine, disparan directamente scroll_up/scroll_down.

### Dead Zones
Recorte de coordenadas del cursor para que no alcance bordes extremos de pantalla. Por defecto 5% de margen en cada lado, mínimo 40px.

### Channel Priority (priorización dinámica)
Cuando gesto y voz proponen acciones diferentes en el mismo frame, `decide_channel_priority()` resuelve el conflicto:
1. **Comandos de sistema** (volume, screenshot, show_desktop) → voz siempre gana
2. **Mismas acciones** en ambos → gesto gana (modalidad primaria)
3. **Acciones diferentes no-sistema** → gesto gana (tiene contexto espacial)
- `voice_should_bypass_fusion()` identifica acciones que no pasan por el state machine.
- Ver `references/channel-priority-pattern.md` para detalles completos.

### Head Pose (6DoF coarse displacement)
El módulo `gaze/head_pose.py` estima rotación de cabeza (yaw, pitch, roll) desde landmarks de FaceMesh:
- **Yaw**: vector nariz-ojo en plano XZ con `arctan2`
- **Pitch**: eje frente-mentón relativo a línea horizontal ojo
- **Roll**: inclinación lateral
- Se aplica como desplazamiento "coarse" en la capa de fusión, complementando el pointer "fine" de gaze
- Dead zone por defecto: ±5° para evitar jitter en pose neutral
- Ver `references/head-pose-estimation-pattern.md` para patrón completo.

### Control de volumen por posición Y de mano
Módulo `gestures/volume_control.py` — detector de volumen basado en la posición vertical del centroid de la mano en el frame. Es un **gesto de posición de zona**, distinto de palm-scroll (motion-based) y expresiones faciales (state-based):
- **Zona superior** (Y < 0.35) → `volume_up`
- **Zona inferior** (Y > 0.65) → `volume_down`
- **Zona neutra** (0.35 ≤ Y ≤ 0.65) → sin acción
- Usa centroid (promedio 21 landmarks) en lugar de muñeca sola → más estable
- Cooldown de 15 frames (~0.5s) para evitar disparos continuos
- Se ejecuta directamente vía `dispatcher.execute()`, sin pasar por gesture bindings
- Ver `references/volume-control-pattern.md` para patrón completo.

### Fusión bimanual (HandFusion)
Módulo `gestures/hand_fusion.py` — asigna roles complementarios cuando ambas manos están visibles:
- **Mano derecha** → offset de cursor fino (±10px basado en posición relativa al centro)
- **Mano izquierda** → scroll vertical (barrido) + zoom (pinch open/close)
- Con una sola mano visible → no-op, comportamiento normal
- Se integra en `tick()` después de `volume_control`, antes de `fusion.step_and_voice()`
- Ver `references/bimanual-fusion-pattern.md` para patrón completo de integración.

### Integración de widgets UI overlay (patrón radial-menu)

Para añadir un nuevo widget PyQt6 overlay al pipeline principal:

1. **Crear el módulo** en `ui/` con clase principal heredando de `QtWidgets.QWidget`
2. **Configurar flags Qt**: `FramelessWindowHint | WindowStaysOnTopHint | Tool` + `WA_TranslucentBackground` + `WA_TransparentForMouseEvents`
3. **Exportar en `ui/__init__.py`** para acceso desde `main.py`
4. **Integrar en `main.py`**:
   - Importar la clase + constantes necesarias (ej: `MENU_OPEN_DURATION_MS`)
   - Instanciar en `run_system()` con variables de estado (hold frames, gesture tracking)
   - Conectar señales con `pyqtSignal` → función de callback en scope de `run_system`
   - En el loop `tick()`:
     - `nonlocal` variables de estado del menú
     - Detectar trigger (ej: palm-hold sostenido)
     - Llamar `widget.update_dwell(cursor_xy)` si visible
     - Llamar `widget.close()` en transición a IDLE
5. **Verificar sintaxis** con `ast.parse()` antes de commit
6. **Commit + push** a ambos repos (FreeHands + Mastermind plan)

Ver `references/radial-menu-integration.md` para ejemplo completo.

### Patrón para widgets que siguen al cursor (magnifier overlay)

Algunos widgets no se abren/cierran con gestos sino que siguen al cursor de mirada de forma continua. Patrón diferente al de radial-menu:

1. **Crear el módulo** en `ui/` con clase principal que capture la pantalla (`QScreen.grabWindow`) y la escale.
2. **Método `update_cursor(cursor)`**: si cursor es None → hide; si no → show + update.
3. **Timer de refresh** interno (~80ms) para recapturar la pantalla sin depender del tick principal.
4. **Integrar en `main.py`**:
   - Instanciar con `zoom_factor` y `radius` configurables.
   - Variable de estado `magnifier_visible` (bool) declarada en `nonlocal` en `tick()`.
   - En `handle_voice_action()`: interceptar comandos como `"zoom_in"`/`"zoom_out"` ANTES de llegar al dispatcher, para repurposarlos como toggle del widget en lugar de `Ctrl++`/`Ctrl--`.
   - En el loop `tick()`: si `magnifier_visible`, llamar `magnifier.update_cursor(result.cursor_xy)`; si no y widget visible, llamar `update_cursor(None)`.
   - En `State.IDLE`: cerrar el widget y resetear `magnifier_visible = False`.
5. **Importante**: usar `overlay.flash_action()` para feedback visual, NO `magnifier.flash_action()` (el magnifier no tiene ese método).
6. **Verificar balance de braces/parens/brackets** con Python tras los cambios en main.py.

Ver `references/magnifier-overlay-pattern.md` para patrón completo.

### Teclado virtual dual layout por ojos (Keyboard-Typing-with-Eyes)

Teclado dividido en mitades izquierda/derecha; se muestra solo la mitad donde está el cursor de mirada. Reduce el espacio de búsqueda a la mitad.

- Clase `LayoutSide` (enum: BOTH, LEFT, RIGHT)
- Cada tecla marcada con `is_left_key: bool`
- `get_visible_keys()` filtra dinámicamente
- `update_layout_side(cursor_x)` detecta lado del cursor
- `process_blink(blink)` soporta blink-to-select
- Signal `layout_changed` para audio feedback
- Ver `references/dual-layout-keyboard-pattern.md` para patrón completo.

### Detección de intención multimodal (gaze dwell + voz)

Patrón para activar funcionalidades de dictado por voz mediante **detección multimodal**: el usuario debe mirar una región de texto (dwell) Y decir un comando de voz. Esto evita activaciones accidentales y da control preciso sobre dónde se inserta el texto dictado.

- Clase `DictationIntentDetector` en `voice/dictation_intent.py`
- Estado: `idle → gazing → ready → activate → reset`
- Dwell configurable (default 500ms), debounce configurable (default 300ms)
- Feedback visual: anillo pulsante naranja + badge "🎙 DICTANDO"
- Integrado en `main.py` tick loop, independiente de `gaze_text_sel`
- Ver `references/multimodal-dictation-intent-pattern.md` para patrón completo.

### Perfiles (Pydantic)
- `gesture_bindings`: dict → mapea gesture_name → action_name
- `gesture_thresholds`: dict → stability_frames + confidence_min por gesture
- Migraciones automáticas en `load_profile()` para compatibilidad con versiones anteriores

### Sistema de Plugins (mejora #16)
Arquitectura extensible para inyectar lógica custom en cada etapa del pipeline:

```
Camera → [on_frame] → Gaze → [on_gaze] → Filter → [on_filter]
→ Gesture → [on_gesture] → Fusion → [on_fusion] → Action → [on_action]
→ Overlay → [on_overlay]
```

**API principal:**
- `FreeHandsPlugin` — clase base con 7 hooks (todos opcionales, passthrough por defecto)
- `PluginContext` — dataclass con frame, cursor, gesture, action, blink, metadata
- `PluginLoader` — descubrimiento automático desde directorio, registro manual, orden por priority
- `plugins_dir` en Profile para configurar ruta de plugins

**Patrón para crear un plugin:**
```python
from freehands.plugins import FreeHandsPlugin, PluginContext

class MiPlugin(FreeHandsPlugin):
    name = "mi_plugin"
    version = "1.0.0"
    description = "Descripción"
    priority = 50  # menor = ejecuta antes

    def on_gaze(self, cursor, ctx):
        # Modificar cursor antes de llegar a fusion
        return modified_cursor

    def on_action(self, action, ctx):
        # Interceptar acción antes de dispatch
        return suppressed_or_modified_action
```

**Reglas:**
- Hooks no implementados se saltan silenciosamente (no override)
- Excepciones en hooks se capturan y loguean, no rompen el pipeline
- `ctx.metadata` es un dict compartido entre todos los plugins del frame
- `loader.run_all(ctx)` modifica el contexto en-place, se aplica al main loop

Ver `references/plugin-system-pattern.md` para API completa y ejemplos.

### Calibración con Gaussian Process (auto-calibración continua)

Módulo adicional `gaze/calibration.py` que añade un modelo GP alongside el Ridge regression:

- `GPGazeModel` — modelo serializable (kernel RBF/Matern, lengthscale, noise_level, training data sliding window)
- `GPGazeRegressor` — predictor con Kalman smoothing, API idéntica a `GazeRegressor`
- `fit_gp_model()` — entrena GP desde samples de calibración
- `update_gp_model()` — añade muestras y reentrena con ventana deslizante (max 200 samples)
- Auto-calibración en `main.py`: durante uso normal en estado ACTIVE, cuando cursor es estable (<15px movimiento) y confianza >0.7, se recopilan muestras implícitas
- Reentrenamiento cada 30 frames, guardado al perfil cada 5 min
- Ver `references/gp-auto-calibration-pattern.md` para patrón completo.

## 🛠️ Patrón para añadir un nuevo módulo

Cuando se añade una funcionalidad nueva a FreeHands:

1. **Crear el módulo** en el subdirectorio correspondiente (`gaze/`, `gestures/`, `fusion/`, `voice/`, `ui/`, `actions/`)
2. **Exportar en `__init__.py`** del subdirectorio
3. **Integrar en `main.py`**:
   - Importar la nueva clase/módulo
   - Instanciar en `run_system()` con los parámetros adecuados
   - Aplicar en el loop `tick()` en el punto correcto del pipeline
4. **Añadir tests** en `tests/test_{modulo}.py`
5. **Actualizar perfil** si hay nuevas configuraciones (`profiles/store.py`)
6. **Verificar sintaxis** antes de commit: `python3 -c "import py_compile; py_compile.compile('path/to/file.py', doraise=True)"`
7. **Commit + push**: `git add -A && git commit -m "9009: mejora #N: descripción" && git push`

### Patrón para detector de intención multimodal (gaze + voz)

Cuando la mejora requiere activar una funcionalidad por **mirada + voz simultáneamente**:

1. **Crear detector** en `voice/` con estado: `idle → gazing → ready → activate → reset`
2. **Hit-test** contra regiones de texto (coordenadas relativas al centro del overlay)
3. **Dwell configurable** + debounce para evitar falsos positivos por glitches de MediaPipe
4. **Integrar en main.py tick()**: actualizar detector con regiones, check voice commands si `ready_to_activate`
5. **Feedback visual** en overlay: anillo pulsante cuando `ready`, badge cuando activo
6. **Consume el estado** con `consume_ready()` para evitar activaciones repetidas

## 📐 Convenciones de código

- `from __future__ import annotations` en todos los archivos
- Dataclasses con `frozen=True` para configuraciones inmutables
- Type hints en todos los parámetros y retornos
- Docstrings en inglés, comentarios en castellano
- Líneas máx: 100 caracteres (ruff config)
- Tests: nombre `test_{funcionalidad}.py`, funciones `test_{descripción}()`
- No usar `pytest` como dependencia — los tests pueden correr sin él (import directo)

## 📚 Referencias

| Archivo | Descripción |
|---------|-------------|
| `references/channel-priority-pattern.md` | Priorización dinámica de canales: reglas de prioridad gesto vs voz |
| `references/audio-feedback-pattern.md` | Patrón para añadir feedback auditivo (beeps) en gestos y voz |
| `references/dead-zones-pattern.md` | Patrón para dead zones en bordes de pantalla |
| `references/blink-detection-ear.md` | Detección de parpadeo via Eye Aspect Ratio (EAR) — mejora #5 |
| `references/external-gesture-profiles.md` | Perfiles de gestos externos JSON: carga, merge, pitfall de `_repair_essential_bindings` |
| `references/asr-backend-pattern.md` | Patrón para añadir nuevos backends ASR (Vosk, whisper.cpp, etc.) a VoiceListener |
| `references/radial-menu-integration.md` | Patrón para integrar widgets overlay PyQt6 (radial menu, OSD) en el pipeline principal |
| `references/dual-layout-keyboard-pattern.md` | Teclado virtual dual-layout: split izq/der basado en posición del cursor, blink-to-select |
| `references/overlay-enhancement-pattern.md` | Patrón para mejorar GazeOverlay: halo radial, pens cosméticos, soporte multi-monitor |
| `references/plugin-system-pattern.md` | API completa del sistema de plugins: FreeHandsPlugin, PluginContext, PluginLoader, hooks, ejemplos |
| `references/head-pose-estimation-pattern.md` | Estimación 6DoF head pose desde FaceMesh: algoritmo yaw/pitch/roll, dead zones, coarse displacement |
| `references/volume-control-pattern.md` | Control de volumen por posición Y de mano: gesto de posición de zona, cooldown, centroid vs muñeca |
| `references/multimodal-dictation-intent-pattern.md` | Detección de intención multimodal: gaze dwell en región de texto + comando de voz para activar dictado sin falsos positivos |
| `references/air-scroll-pattern.md` | Air-scroll / swipe: detección de barrido vertical con cualquier pose de mano, umbral de desplazamiento |
| `references/gp-auto-calibration-pattern.md` | Patrón GP auto-calibración: modelo serializable, regressor con Kalman, sample collection en tick(), ventana deslizante |

## Algoritmos y Procesamiento de Señal (FreeHands)

### Patrón: Refinamiento Iterativo de Algoritmos de Estimación

Ciclo de desarrollo para algoritmos de estimación geométrica, sensorial o de visión por computadora donde los datos de entrada son simulados pero deben reproducir comportamientos del mundo real.

**Cuándo aplicar:** Estimación de pose desde landmarks, cálculo de ángulos/rotaciones desde coordenadas 3D, estimación de distancia/profundidad.

**Ciclo (4 pasos):**
1. **Prototipar** — implementación más simple que "suene" correcta
2. **Testear** — datos simulados que reproduzcan comportamientos reales (neutral face es el caso más importante)
3. **Diagnosticar** — analizar por qué falla la geometría (denominador cerca de cero → usar arctan2, vector con offset anatómico → cambiar referencia)
4. **Corregir y retestear** — aplicar corrección específica, re-ejecutar TODOS los tests

**Reglas de oro:**
- Neutral primero: el caso neutral debe pasar SIEMPRE
- Testear simetrías: yaw +30° funciona → yaw -30° también
- Los tests son la verdad: si un test falla, el algoritmo es incorrecto
- Documentar por qué se eligió cada fórmula

### Kalman Cursor Smoothing

Reemplaza suavizado exponencial (EMA) por filtro de Kalman 2-D con modelo de velocidad constante para tracking de cursor (gaze, gestos, etc.).

**Diseño recomendado:** Estado [x, y, vx, vy] (4 elementos), modelo de velocidad constante.

**Parámetros configurables:**
- `process_noise`: 25.0 (medio) → equilibrio recomendado
- `measurement_noise`: 400.0 → más suave, más latencia
- `initial_uncertainty`: 1000.0

**Ventaja principal de Kalman:** estimación de velocidad + mejor tradeoff latencia-suavizado.

**Pitfalls:** Clamping fuera del filtro, primer frame retorna medición cruda, reset al reconectar, FPS variable → ajustar dt dinámicamente.

### Serialización de Modelos ML (Serializable ML Models)

Serializar modelos ML instance-based (KNN) y paramétricos (Ridge) en schemas Pydantic con tipos Union para compatibilidad.

**Patrón clave:** `weights_x: list[float] | list[list[float]]` (Union), NO `list[float]`. Pydantic v2 valida estrictamente.

**Pitfalls:** Pydantic strict validation con Union types, np.array() con listas de listas crea 2D, bias como Union, no mezclar tipos entre modelo KNN y paramétrico.

### Referencias
- `references/head-pose-estimation-pattern.md` para patrón de estimación 6DoF
- `references/kalman-cursor-freehands.md` para implementación Kalman en FreeHands
- `references/knn-gaze-implementation.md` para implementación KNN en FreeHands

## 📋 Mejoras implementadas (9009)

| # | Mejora | Estado |
|---|---|---|
| 1 | Scroll por gesto con palma abierta | ✅ |
| 2 | Dead zones en bordes de pantalla | ✅ |
| 3 | Feedback auditivo de confirmación | ✅ |
| 4 | Comandos de sistema por voz | ✅ |
| 5 | Clic por guiño (blink via EAR) | ✅ |
| 6 | Configuración de gestos vía JSON | ✅ |
| 7 | Vosk offline como backend de voz | ✅ |
| 8 | Priorización dinámica de canales | ✅ |
| 9 | Snap-to-grid UI | ✅ |
| 10 | Menú OSD radial | ✅ |
| 11 | Calibración 9 puntos con regresión polinomial | ✅ |
| 12 | Overlay transparente PyQt6 sobre escritorio | ✅ |
| 13 | Doble parpadeo = clic, prolongado = drag | ✅ |
| 14 | Fusión multimodal con operador AND | ✅ |
| 15 | Filtro Kalman predictivo | ✅ |
| 16 | Sistema de plugins Python | ✅ |
| 17 | 6DoF head pose para desplazamiento grueso | ✅ |
| 18 | Unidades de acción facial (sonrisa, ceño, sorpresa) | ✅ |
| 19 | Teclado virtual con selección por mirada | ✅ |
| 20 | Modo dictado (mirar campo + decir "escribe" + dictar) | ✅ |
| 21 | OCR integrado + gaze typing (talon-gaze-ocr) | ✅ |
| 22 | Teclado virtual dual layout por ojos (Keyboard-Typing-with-Eyes) | ✅ |
| 23 | Calibración con Gaussian Process (auto-calibración continua) | ✅ |
| 24 | Control bimanual (mano derecha cursor, izquierda scroll/zoom) | ✅ |