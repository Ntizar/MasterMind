# GazeTracking

**URL:** https://github.com/antoinelame/GazeTracking
**Categoría:** Visión/ML
**Estrellas:** 2,573
**Lenguaje:** Python

## ¿Qué hace?
GazeTracking es una librería de Python (3.10+) para **seguimiento ocular (eye tracking) basada en webcam**. Utiliza `dlib` con un predictor de landmarks faciales (68 puntos) para detectar los ojos y localizar las pupilas en tiempo real, proporcionando:

- Coordenadas exactas de las pupilas izquierda y derecha
- Dirección de la mirada (izquierda, derecha, centro)
- Razón horizontal y vertical de la mirada (0.0–1.0)
- Detección de parpadeo
- Frame anotado con las pupilas resaltadas

Internamente usa procesamiento de imagen con OpenCV (filtrado bilateral, erosión, umbralización binaria) y detección de contornos para localizar el iris y calcular el centroide de la pupila. Incluye un sistema de calibración automática que determina el mejor umbral de binarización para cada usuario.

## Casos de uso
1. **Control por mirada**: Interfaces sin manos donde la dirección de la mirada controla cursor, botones o menús en aplicaciones.
2. **Análisis de atención**: Medir cuánto tiempo mira un usuario hacia zonas específicas de una pantalla (UI testing, diseño UX).
3. **Detección de somnolencia**: Monitoreo en tiempo real de parpadeo y dirección de la mirada para alertar conductores o operadores.
4. **Accesibilidad**: Herramientas de control alternativo para personas con movilidad reducida.
5. **Investigación en psicología/cognición**: Estudios sobre fijación visual, patrones de lectura o respuestas emocionales.

## Snippets útiles

### Demo básico (detectar dirección de la mirada)
```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    new_frame = gaze.annotated_frame()
    text = ""

    if gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
    cv2.imshow("Demo", new_frame)

    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
```

### Obtener coordenadas de pupilas y ratios
```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    if gaze.pupils_located:
        left_pupil = gaze.pupil_left_coords()   # (x, y)
        right_pupil = gaze.pupil_right_coords() # (x, y)

        h_ratio = gaze.horizontal_ratio()  # 0.0=extremo derecho, 0.5=centro, 1.0=extremo izquierdo
        v_ratio = gaze.vertical_ratio()    # 0.0=arriba, 0.5=centro, 1.0=abajo

        if gaze.is_blinking():
            print("Blink detected!")

    cv2.imshow("Gaze", gaze.annotated_frame())
    if cv2.waitKey(1) == 27:
        break
```

### Control de cursor por mirada
```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

screen_w, screen_h = 1920, 1080

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    if gaze.pupils_located:
        h_ratio = gaze.horizontal_ratio()
        v_ratio = gaze.vertical_ratio()

        # Mapear ratio a coordenadas de pantalla
        cursor_x = int(h_ratio * screen_w)
        cursor_y = int(v_ratio * screen_h)

        # Dibujar cursor en el frame
        cv2.circle(frame, (cursor_x, cursor_y), 10, (0, 255, 0), -1)
        cv2.putText(frame, f"({cursor_x}, {cursor_y})", (cursor_x + 15, cursor_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow("Gaze Cursor", frame)
    if cv2.waitKey(1) == 27:
        break
```

## Cómo integrarlo en proyectos

### 1. Instalación

**Opción A — pip (recomendada):**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Opción B — pip directo desde PyPI (si está disponible):**
```bash
pip install gaze-tracking
```

**Opción C — uv:**
```bash
uv venv
uv pip install -e .
```

**Opción D — Docker:**
```bash
./build_and_run.sh
```

### 2. Dependencias
- **Python 3.10+**
- **dlib>=20.0** — predictor de landmarks faciales (shape_predictor_68_face_landmarks.dat)
- **opencv-python>=4.10** — procesamiento de imágenes
- **numpy>=2.0** — operaciones con arrays

> **Nota:** Si `dlib` falla al compilar, instala primero: `sudo apt install cmake build-essential` (Ubuntu) o `brew install cmake` (macOS).

### 3. Estructura del paquete
```
gaze_tracking/
├── __init__.py          # Exporta GazeTracking
├── gaze_tracking.py     # Clase principal: API pública
├── eye.py               # Aísla cada ojo y calcula ratio de parpadeo
├── pupil.py             # Detecta iris y calcula centroide de pupila
├── calibration.py       # Calibración automática del umbral de binarización
└── trained_models/
    └── shape_predictor_68_face_landmarks.dat  # Modelo dlib pre-entrenado
```

### 4. API principal (clase `GazeTracking`)

| Método | Retorna | Descripción |
|---|---|---|
| `gaze.refresh(frame)` | — | Analiza un frame (numpy.ndarray) |
| `gaze.pupil_left_coords()` | `(x, y)` o `None` | Coordenadas pupila izquierda |
| `gaze.pupil_right_coords()` | `(x, y)` o `None` | Coordenadas pupila derecha |
| `gaze.is_left()` | `bool` | Mirando a la izquierda |
| `gaze.is_right()` | `bool` | Mirando a la derecha |
| `gaze.is_center()` | `bool` | Mirando al centro |
| `gaze.horizontal_ratio()` | `float` 0.0–1.0 | Dirección horizontal (0=derecha, 1=izquierda) |
| `gaze.vertical_ratio()` | `float` 0.0–1.0 | Dirección vertical (0=arriba, 1=abajo) |
| `gaze.is_blinking()` | `bool` | Parpadeo detectado |
| `gaze.annotated_frame()` | `numpy.ndarray` | Frame con pupilas resaltadas |
| `gaze.pupils_located` | `bool` | Si las pupilas fueron localizadas |

### 5. Tips de integración
- **Rendimiento**: Ejecuta `gaze.refresh()` en un loop con `cv2.VideoCapture`. El procesamiento es ligero pero depende de la resolución del frame.
- **Calibración**: El umbral de binarización se calibra automáticamente en los primeros 20 frames. No requiere intervención manual.
- **Multi-usuario**: El predictor de landmarks funciona con una sola cara en el frame. Para múltiples usuarios, se necesitaría adaptar el código.
- **Sin webcam**: Funciona con frames de video (`.mp4`, `.avi`) pasando cada frame a `gaze.refresh()`.

## Fecha de aprendizaje: 2026-05-27
