# ControlNet & Conditional Diffusion Control

**Fecha:** 2026-07-05
**Tema:** #21 de la serie Deep Learning Fundamentals
**Papers clave:** ControlNet (Zhang et al., 2023), ControlNet++, T2I-Adapter, IP-Adapter
**Repositorios:** lllyasviel/ControlNet (34k★), TencentARC/T2I-Adapter, diffusers/controlnet

---

## 1. El Problema Fundamental

Los modelos text-to-image (Stable Diffusion, DALL·E, Midjourney) generan imágenes impresionantes pero carecen de **control espacial fino**. No puedes especificar:

- La pose exacta de una persona
- El layout de una habitación
- Los bordes de un objeto
- El mapa de profundidad de una escena

Escribir prompts detallados es como intentar pintar un cuadro describiéndolo a un ciego: posible, pero terriblemente ineficiente.

**ControlNet** (Zhang, Rao & Agrawala, Stanford 2023) resuelve esto añadiendo un **controlador condicional** que guía la generación sin destruir el conocimiento preentrenado del modelo base.

---

## 2. Arquitectura — La Idea Elegante

### 2.1 Estructura Principal

```
                    ┌─────────────────────────────────┐
                    │      Pretrained Diffusion       │
                    │      (LOCKED - no training)     │
                    │                                   │
  Condition ──► [Encoder] ──► ZeroConv ──┐            │
                    │                     │            │
                    │          [ZeroConv] ─┼──► Add ──►│ Decoder (denoising)
                    │                     │            │
                    │    [ZeroConv] ──────┼──► Add ────┤
                    │                     │            │
                    │ [ZeroConv] ─────────┼──► Add ────┤
                    │                     │            │
                    └─────────────────────┘            │
                                                       │
                                              ┌────────┴────────┐
                                              │   Text Prompt    │
                                              │   (cross-attn)   │
                                              └─────────────────┘
```

**Los 3 componentes clave:**

1. **Locked backbone:** El modelo diffusion preentrenado se congela (gradientes = 0). Preserva todo el conocimiento de LAION-5B.

2. **Trainable copy del encoder:** Se copia el encoder del diffusion model. Este copy es entrenable y recibe la condición (edge map, depth, pose...).

3. **Zero Convolutions:** Las capas de convolución que conectan el copy con el modelo original se inicializan a **cero**. Esto significa que al inicio del training:

   ```
   output = frozen_model + ZeroConv(trainable_copy)
          = frozen_model + 0
          = frozen_model
   ```

   El modelo empieza siendo **idéntico** al original. Los pesos de ZeroConv crecen progresivamente desde cero durante el training. Esto es crítico: evita **catastrophic forgetting** y noise injection.

### 2.2 Zero Convolution — El Truco

Una convolución normal:
```
y = W * x + b
```

Zero Convolution:
```
W inicial = 0 (todos los pesos a cero)
b inicial = 0

y = W * x + b  (empieza siendo 0)
```

Durante training, los pesos de ZeroConv crecen gradualmente. Al final, si el training fue bueno:
- ZeroConv aprende a añadir información condicional útil
- El modelo frozen sigue intacto
- No hay catastrophic forgetting

**¿Por qué funciona?** Porque el modelo diffusion ya "sabe" generar imágenes de alta calidad. ControlNet solo necesita aprender a **modificar ligeramente** el proceso de denoising para respetar la condición.

---

## 3. Tipos de Condiciones

ControlNet acepta **cualquier tipo de condición espacial**:

| Condición | Extractor | Dataset típico | Uso |
|-----------|-----------|----------------|-----|
| **Canny Edges** | OpenCV Canny | COCO, LVIS | Control de bordes |
| **Depth** | MiDaS, DPT | NYU Depth, KITTI | Control de profundidad |
| **Pose** | OpenPose, MMPose | COCO Pose, MPII | Control de pose humana |
| **Segmentation** | DeepLab, Mask2Former | ADE20K, COCO-Stuff | Control semántico |
| **Normal Maps** | MiDaS Normal | ScanNet | Control de superficies 3D |
| **Hough Lines** | OpenCV Hough | — | Control de líneas rectas |
| **Scribbles** | Manual / SAM | — | Bocetos a mano |
| **Sket**ch | ControlNet-Sketch | — | Sketches reales |
| **Tile** | — | — | Upscale + denoise |

**Multi-Control:** ControlNet permite combinar múltiples condiciones simultáneamente:
- Pose + Depth → persona en posición específica con profundidad correcta
- Edges + Segmentation → objeto en lugar específico con forma exacta

---

## 4. Implementación con Hugging Face Diffusers

### 4.1 Instalación

```bash
pip install diffusers transformers accelerate torch
```

### 4.2 ControlNet Básico

```python
import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, EulerDiscreteScheduler
from PIL import Image
import cv2
import numpy as np

# 1. Cargar ControlNet (pre-entrenado para la condición que quieras)
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11f1p_sd15_depth",  # Depth condition
    torch_dtype=torch.float16
)

# 2. Cargar Stable Diffusion + ControlNet
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)

# 3. Preparar condición (depth map, edge map, etc.)
condition_image = Image.open("scene_depth.png").resize((512, 512))

# 4. Generar con control
image = pipe(
    prompt="a beautiful landscape with mountains and a river",
    image=condition_image,
    num_inference_steps=50,
    guidance_scale=7.5,
    controlnet_conditioning_scale=0.8,  # ⚠️ Parámetro clave
).images[0]

image.save("output.png")
```

### 4.3 Controlnet con Múltiples Condiciones

```python
from diffusers import MultiControlNetModel

# Cargar múltiples ControlNets
depth_controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11f1p_sd15_depth", torch_dtype=torch.float16
)
pose_controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_pose", torch_dtype=torch.float16
)

# Combinar en un solo MultiControlNet
multi_controlnet = MultiControlNetModel(
    [depth_controlnet, pose_controlnet]
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=multi_controlnet,
    torch_dtype=torch.float16,
).to("cuda")

# Generar con múltiples condiciones
depth_map = load_depth("scene.png")      # Extractor MiDaS
pose_map = load_pose("scene.png")        # Extractor OpenPose

image = pipe(
    prompt="a person sitting on a chair in a room",
    image=[depth_map, pose_map],
    controlnet_conditioning_scale=[0.7, 0.9],  # Pesos diferentes por condición
    num_inference_steps=50,
    guidance_scale=7.5,
).images[0]
```

### 4.4 Entrenar tu Propio ControlNet

```python
import torch
from diffusers import ControlNetModel, DDPGTrainer
from datasets import load_dataset
from torchvision import transforms

# 1. Preparar dataset: pares (condition_image, target_image)
# Ejemplo: pares (edge_map, foto_original)
dataset = load_dataset("my_edge_photo_pairs")

# 2. Cargar modelo base
base_model = "runwayml/stable-diffusion-v1-5"
controlnet = ControlNetModel.from_pretrained(
    base_model,
    subfolder="controlnet",  # Si existe
)

# Si no existe subfolder, se crea desde cero:
# controlnet = ControlNetModel.from_pretrained(base_model)

# 3. Configuración de training
from diffusers import StableDiffusionControlNetTrainingConfig

config = StableDiffusionControlNetTrainingConfig(
    learning_rate=1e-5,
    train_batch_size=4,
    gradient_accumulation_steps=4,
    max_train_steps=10000,
    checkpointing_steps=1000,
)

# 4. Training loop básico
from accelerate import Accelerator

accelerator = Accelerator()
model, optimizer, scheduler, dataloader = accelerator.prepare(
    controlnet, optimizer, scheduler, dataloader
)

for epoch in range(num_epochs):
    for batch in dataloader:
        condition = batch["condition"]  # edge/depth/pose map
        target = batch["target"]        # imagen objetivo
        
        # Forward pass del diffusion model con condición
        noise = torch.randn_like(target)
        timesteps = torch.randint(0, 1000, (target.shape[0],))
        
        # ... training loop estándar de diffusion
        # con las features de controlnet inyectadas
        
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

# 5. Guardar
controlnet.save_pretrained("./my-controlnet")
```

### 4.5 Extracción de Condiciones en Tiempo Real

```python
import cv2
import numpy as np
from PIL import Image

def extract_canny(image_path, low_thresh=100, high_thresh=200):
    """Extracción de bordes Canny."""
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img, low_thresh, high_thresh)
    return Image.fromarray(edges)

def extract_depth(image_path):
    """Extracción de profundidad con MiDaS."""
    import torch
    from transformers import pipeline
    
    depth_estimator = pipeline(
        "depth-estimation",
        device="cuda" if torch.cuda.is_available() else "cpu"
    )
    result = depth_estimator(image_path)
    return result["depth"]

def extract_pose(image_path):
    """Extracción de pose con MMPose/OpenPose."""
    import cv2
    import numpy as np
    
    # Usar MediaPipe (más ligero que OpenPose)
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    
    image = cv2.imread(image_path)
    with mp_pose.Pose(min_detection_confidence=0.5) as pose:
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Crear mapa de pose
        pose_map = np.zeros_like(image)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                pose_map, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )
        return Image.fromarray(pose_map)

def extract_normal(image_path):
    """Normal maps con MiDaS."""
    import torch
    from transformers import pipeline
    
    normal_estimator = pipeline(
        "depth-estimation",
        model="LiheYoung/depth-anything-large-hf",
        device="cuda" if torch.cuda.is_available() else "cpu"
    )
    # MiDaS puede generar normal maps con post-procesamiento
    result = normal_estimator(image_path)
    return result["depth"]  # Convertir a normal map
```

### 4.6 ControlNet con SDXL

```python
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel

# SDXL ControlNet (más potente, más lento)
controlnet = ControlNetModel.from_pretrained(
    "diffusers/controlnet-canny-sdxl-1.0",
    variant="fp16",
    torch_dtype=torch.float16,
)

pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    controlnet=controlnet,
    variant="fp16",
    torch_dtype=torch.float16,
).to("cuda")

# SDXL usa 1024x1024 por defecto
image = pipe(
    prompt="a futuristic cityscape at sunset",
    image=canny_edges,
    controlnet_conditioning_scale=0.5,
    num_inference_steps=50,
    guidance_scale=7.5,
).images[0]
```

---

## 5. Variantes y Evolución

### 5.1 T2I-Adapter (Tencent ARC, 2023)

**Problema de ControlNet:** Duplica el encoder → 2x memoria.

**Solución T2I-Adapter:**
- Encoder ligero y **completamente entrenable** (no copia del diffusion)
- Más eficiente en memoria (~1/4 de parámetros de ControlNet)
- Se integra en el cross-attention en lugar de en el UNet
- No necesita zero convolutions

```python
from diffusers import StableDiffusionAdapterPipeline, T2IAdapter

adapter = T2IAdapter.from_pretrained(
    "TencentARC/t2iadapter_depth_sd14v1",
    torch_dtype=torch.float16
)

pipe = StableDiffusionAdapterPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    adapter=adapter,
    torch_dtype=torch.float16,
).to("cuda")
```

**Comparativa ControlNet vs T2I-Adapter:**

| | ControlNet | T2I-Adapter |
|---|---|---|
| Parámetros | ~400M (copia encoder) | ~50M (encoder ligero) |
| Memoria GPU | Alta | Baja |
| Calidad | Ligeramente mejor | Muy buena |
| Velocidad | Más lento | ~20% más rápido |
| Multi-control | Sí (MultiControlNet) | Limitado |
| Training | ZeroConv necesario | Standard |

### 5.2 ControlNet++ (Tencent ARC, 2023)

**Problema:** Usar múltiples ControlNets requiere entrenar cada uno por separado. Si combinamos 3 ControlNets entrenados por separado, la calidad cae.

**Solución ControlNet++:**
- **Unificado:** Un solo modelo que maneja múltiples condiciones
- **Training pipeline unificado:** Entrenar todas las condiciones juntas
- **Better compositionality:** Las condiciones se combinan mejor

### 5.3 IP-Adapter (Huawei, 2024)

**Problema:** ControlNet controla estructura pero no estilo/identidad.

**Solución IP-Adapter:**
- Controla la **identidad visual** (cara, estilo artístico)
- Usa CLIP image encoder como condicionante
- Sin training necesario (training-free)
- Se integra en el cross-attention

```python
from diffusers import IPAdapterPipeline, IPAdapterPlusImageEncoderModel

image_encoder = IPAdapterPlusImageEncoderModel.from_pretrained(
    "h94/IP-Adapter-plus",
    subfolder="image_encoder",
    torch_dtype=torch.float16,
)

pipe = IPAdapterPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    ip_adapter=image_encoder,
    torch_dtype=torch.float16,
).to("cuda")

# Generar con identidad de referencia
image = pipe(
    prompt="a portrait of this person",
    image=[reference_face_image],  # Imagen de referencia
    num_inference_steps=30,
).images[0]
```

### 5.4 ControlNet Tile (para Upscaling)

ControlNet Tile es especializado en **upscale + denoise**:
- Acepta una imagen de baja resolución
- La mejora manteniendo la estructura original
- Ideal para upscaling de imágenes generadas

### 5.5 ControlNet V2

ControlNet V2 introduce:
- Mejor arquitectura de encoder
- Soporte nativo para SDXL
- Mejor generalización a condiciones no vistas

---

## 6. Aplicaciones Prácticas

### 6.1 Generación de Arquitecturas

```python
# Input: sketch de edificio → Output: imagen fotorrealista
from PIL import Image
import cv2
import numpy as np

def sketch_to_building(sketch_path, prompt="modern minimalist building"):
    # 1. Mejorar el sketch
    sketch = cv2.imread(sketch_path, cv2.IMREAD_GRAYSCALE)
    sketch = cv2.medianBlur(sketch, 3)
    
    # 2. Extraer bordes limpios
    edges = cv2.Canny(sketch, 50, 150)
    edges = cv2.dilate(edges, None, iterations=2)
    edges = cv2.erode(edges, None, iterations=1)
    
    # 3. Generar con ControlNet
    controlnet = ControlNetModel.from_pretrained(
        "lllyasviel/control_v11p_sd15_canny",
        torch_dtype=torch.float16
    )
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        controlnet=controlnet,
        torch_dtype=torch.float16,
    ).to("cuda")
    
    result = pipe(
        prompt=prompt,
        image=Image.fromarray(edges),
        controlnet_conditioning_scale=0.8,
        num_inference_steps=50,
    ).images[0]
    
    return result
```

### 6.2 Análisis de Datos con Control Visual

Para el stack ESIOS/energy:
- **Depth maps de instalaciones solares:** Usar imágenes satelitales + MiDaS para extraer profundidad
- **Pose de turbinas eólicas:** OpenPose adaptado a palas de turbina
- **Segmentación de nubes:** DeepLab para segmentar cobertura nubosa en imágenes satelitales
- **Edge detection en mapas de carga:** Canny para detectar patrones en mapas de calor

### 6.3 Pipeline de Generación con Control

```python
class ControlNetPipeline:
    """Pipeline completo de generación con control."""
    
    def __init__(self, model_name="runwayml/stable-diffusion-v1-5"):
        self.controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/control_v11f1p_sd15_depth",
            torch_dtype=torch.float16
        )
        self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
            model_name,
            controlnet=self.controlnet,
            torch_dtype=torch.float16,
        ).to("cuda")
        
    def generate_with_depth(
        self,
        prompt: str,
        depth_image: Image.Image,
        conditioning_scale: float = 0.8,
        seed: int = None,
    ) -> Image.Image:
        if seed is not None:
            generator = torch.Generator("cuda").manual_seed(seed)
        else:
            generator = None
            
        return self.pipe(
            prompt=prompt,
            image=depth_image,
            controlnet_conditioning_scale=conditioning_scale,
            generator=generator,
            num_inference_steps=50,
            guidance_scale=7.5,
        ).images[0]
    
    def generate_with_pose(
        self,
        prompt: str,
        pose_image: Image.Image,
        conditioning_scale: float = 0.9,
        seed: int = None,
    ) -> Image.Image:
        controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/control_v11p_sd15_pose",
            torch_dtype=torch.float16
        )
        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            controlnet=controlnet,
            torch_dtype=torch.float16,
        ).to("cuda")
        
        generator = torch.Generator("cuda").manual_seed(seed) if seed else None
        return pipe(
            prompt=prompt,
            image=pose_image,
            controlnet_conditioning_scale=conditioning_scale,
            generator=generator,
            num_inference_steps=50,
            guidance_scale=7.5,
        ).images[0]
```

---

## 7. Parámetros Clave

| Parámetro | Rango | Efecto |
|-----------|-------|--------|
| `controlnet_conditioning_scale` | 0.0 - 1.5 | Fuerza del control. 0.8-1.0 es típico. >1.0 puede over-constrain |
| `guidance_scale` (CFG) | 5.0 - 15.0 | Calidad/fidelidad del prompt. 7.0-7.5 es sweet spot |
| `num_inference_steps` | 20 - 100 | Más pasos = mejor calidad, más lento. 50 es estándar |
| `negative_prompt` | str | Lo que NO quieres en la imagen |
| `generator` | torch.Generator | Reproducibilidad con seed |

**Tips de tuning:**
- `controlnet_conditioning_scale` alto + `guidance_scale` alto = muy rígido
- `controlnet_conditioning_scale` bajo + `guidance_scale` alto = más creativo pero menos control
- Para pose: scale ~0.9, para depth: scale ~0.8, para canny: scale ~0.8

---

## 8. Recursos y Referencias

### Papers Fundamentales

1. **ControlNet** — Zhang, Rao & Agrawala (2023)
   - Arxiv: [2302.05543](https://arxiv.org/abs/2302.05543)
   - Stanford University
   - 3000+ citations

2. **T2I-Adapter** — Mou et al. (2023)
   - Arxiv: [2304.06847](https://arxiv.org/abs/2304.06847)
   - Tencent ARC

3. **ControlNet++** — Yang et al. (2023)
   - Arxiv: [2311.16933](https://arxiv.org/abs/2311.16933)
   - Tencent ARC

4. **IP-Adapter** — Ye et al. (2024)
   - Arxiv: [2403.06138](https://arxiv.org/abs/2403.06138)
   - Huawei

5. **Depth Anything** — Yang et al. (2024)
   - Arxiv: [2401.10891](https://arxiv.org/abs/2401.10891)
   - extractor de profundidad SOTA

### Repositorios

- [lllyasviel/ControlNet](https://github.com/lllyasviel/ControlNet) — Original (34k★)
- [TencentARC/T2I-Adapter](https://github.com/TencentARC/T2I-Adapter)
- [tencentARC/ControlNet++](https://github.com/TencentARC/ControlNet-Plus-Plus)
- [h94/IP-Adapter](https://github.com/tencent-ailab/IP-Adapter)
- [diffusers/controlnet](https://github.com/huggingface/diffusers) — Integración oficial
- [comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI) — Node-based workflows
- [lllyasviel/ControlNet-v2-11](https://github.com/lllyasviel/ControlNet-v2-11)

### Herramientas de Extracción

- **MiDaS** — Depth estimation SOTA
- **DPT** — Dense Prediction Transformers
- **OpenPose** — Human pose detection
- **MediaPipe Pose** — Pose detection (más ligero)
- **DeepLabV3** — Semantic segmentation
- **SAM (Segment Anything)** — Zero-shot segmentation
- **Canny (OpenCV)** — Edge detection

---

## 9. Conexiones con Otros Temas de la Serie

- **#2 Diffusion Models** — ControlNet opera sobre modelos diffusion
- **#11 Vision Transformers** — Extractores de condición usan ViT (DPT, SAM)
- **#15 CLIP** — IP-Adapter usa CLIP image encoder
- **#19 Diffusion Transformers (DiT)** — ControlNet se adapta a DiT
- **#20 World Models** — Control de generación condicional

---

## 10. Próximo Tema Sugerido

**DreamerV3 / Model-Based RL** — RL sample-efficient con world models en espacio latente. Conecta con World Models (#20) y es el estado del arte en planificación con muestras limitadas. Muy relevante para simulación y control en el stack ESIOS.

Otra opción de alta prioridad: **Mamba-2 / SSM Transformers** — Evolución de SSMs con atención híbrida, ideal para world models eficientes en MicroVM.
