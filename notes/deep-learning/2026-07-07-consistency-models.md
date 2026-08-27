---
title: "Consistency Models — Generación de Imágenes en 1 Paso"
date: 2026-07-07
tags: [deep-learning, diffusion, consistency-models, generative-ai, one-step-generation]
category: deep-learning
status: published
---

# Consistency Models — Generación de Imágenes en 1 Paso

## Resumen Ejecutivo

Los **Consistency Models (CM)** son una familia de modelos generativos que aprenden a mapear
cualquier punto de ruido inicial directamente a una muestra de datos, eliminando la necesidad
de iteraciones de difusión en inference. Donde los diffusion models requieren 50-1000 pasos,
los CM generan en **1 paso** manteniendo calidad competitiva.

**Impacto:** 1000x más rápido que DDPM en inference. Clave para generación en tiempo real,
edge deployment y video generation.

---

## 1. Fundamentos Teóricos

### El Problema de los Diffusion Models

Los DDPM son los reyes de calidad visual pero su inference es secuencial y lento:

```
x_T ~ N(0,I) → paso 1 → x_{T-1} → paso 2 → ... → x_0
(50-1000 pasos secuenciales, cada uno requiere forward pass)
```

Para imágenes de alta resolución, esto puede ser segundos o minutos por imagen.

### Idea Central de Consistency Models

Song et al. (2023) observaron que la EDO de la difusión puede invertirse y que existe una
**trayectoria de consistencia** donde todos los puntos intermedios pueden mapearse directamente
al target:

```
x_T ~ N(0,I) → 1 paso → x_0
```

El modelo aprende una función de consistencia f(x, t) tal que para cualquier x_t en la
trayectoria de difusión, f(x_t, t) ≈ x_0.

### Teorema de Consistencia

Dada una EDO de probabilidad flow (probability flow ODE):

```
dx/dt = f(x,t) - g(t)² ∇_x log p_t(x)
```

Una función de consistencia f: ℝⁿ × [0,1] → ℝⁿ satisface:

- **Condición de consistencia:** ∂f/∂t + (∂f/∂x)·f = 0 (EDO de transporte)
- **Condición de borde:** f(x, 1) = x (identidad en el ruido)
- **Condición de target:** f(x_0, 0) = x_0 (identidad en los datos)

Esto significa que si dos puntos x_t y x_s están en la misma trayectoria de flow,
entonces f(x_t, t) = f(x_s, s) = x_0.

---

## 2. Evolución de la Familia

### 2.1 Consistency Distillation (Song et al., 2023)

**Paper:** ["Consistency Models"](https://arxiv.org/abs/2303.01469) — ICML 2024

- Entrena un modelo para predecir el punto final de cualquier punto intermedio
- Usa **ODE trajectory sampling** para generar datos de entrenamiento
- El modelo aprende la función de mapeo directo

**Training:**
1. Entrenar un diffusion model base (DDPM)
2. Muestrear trayectorias ODE del ruido a datos
3. Para cada punto intermedio x_t, el target es x_0
4. Entrenar el CM con loss: L = ‖f_ψ(x_t, t) - x_0‖²

**Inference:** 1 paso (o N pasos con predictor-corrector)

### 2.2 Progressive Consistency Distillation (PCD)

**Paper:** ["Progressive Consistency Distillation"](https://arxiv.org/abs/2310.04476)

- Problema: training directo de CM es inestable para alta resolución
- Solución: entrenar en una **serie de modelos crecientes**
- Primero CM para 32×32, luego usarlo para distilar 64×64, etc.
- Cada etapa usa el CM anterior como teacher

**Pipeline:**
```
DDPM(256²) → CM(32²) → CM(64²) → CM(128²) → CM(256²)
```

### 2.3 Rectified Flow + Consistency

**Paper:** ["Rectified Flow: A Parallel Discretization Scheme"](https://arxiv.org/abs/2209.03003) (Liu et al., 2022)

- Combina flow matching con discretización paralela
- Más estable que la EDO de difusión para training de CM
- Rectified Flow → Consistency Flow: mapeo directo data→noise

### 2.4 Latent Consistency Models (LCM)

**Paper:** ["Latent Consistency Models"](https://arxiv.org/abs/2310.04378) (Tencent, 2023)

- CM en **espacio latente** (no pixel space)
- 4 pasos en latent space ≈ calidad de 20+ pasos
- Compatible con Stable Diffusion pre-entrenado
- **LCM-LoRA:** fine-tuning ligero con 8-16 GPU steps sobre SD/SDXL

### 2.5 Consistency Flow (Meta FAIR)

- Combina flow matching con consistency
- Mejor stability en training
- Compatible con rectified flow

---

## 3. Comparación con Otros Métodos

| Método | Pasos | FID (ImageNet 256) | Velocidad | Training Cost |
|--------|-------|---------------------|-----------|---------------|
| DDPM | 1000 | 3.17 | Muy lento | ~100 GPU días |
| DDIM | 50 | ~3.5 | Lento | ~100 GPU días |
| DPM-Solver++ | 15-20 | ~3.3 | Medio | ~100 GPU días |
| Consistency Distillation | 1 | ~3.5 | **Ultra rápido** | ~100 GPU días |
| Progressive CM (PCD) | 1-2 | ~3.1 | **Ultra rápido** | ~100 GPU días |
| Diffusion Transformer (DiT) | 50 | 2.27 | Lento | ~100 GPU días |
| Consistency DiT | 1 | ~2.5 | **Ultra rápido** | ~20 GPU días |
| LCM (SDXL, 4 pasos) | 4 | ~3.0 | **Muy rápido** | ~1 GPU día |

**Key insight:** El entrenamiento es costoso (necesita DDPM base), pero el inference
es instantáneo. LCM reduce esto drásticamente: fine-tuning en ~1 GPU día.

---

## 4. Implementación Práctica

### 4.1 Consistency Model desde Cero

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm

class TimestepEmbedding(nn.Module):
    """Timestep embedding para CM."""
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
        
    def forward(self, t):
        """
        Args:
            t: timestep scalar [0, 1], shape (batch,)
        Returns:
            embedding, shape (batch, dim)
        """
        device = t.device
        half_dim = self.dim // 2
        emb_scale = torch.exp(
            -torch.log(torch.tensor(10000.0, device=device))
            * torch.arange(half_dim, device=device) / half_dim
        )
        emb = t.unsqueeze(1) * emb_scale.unsqueeze(0)
        emb = torch.cat([torch.sin(emb), torch.cos(emb)], dim=-1)
        return emb


class ConsistencyModel(nn.Module):
    """
    Consistency Model que mapea x_t → x_0 directamente.
    
    Arquitectura: UNet con timestep embedding (similar a DDPM)
    """
    def __init__(self, in_channels=3, base_dim=128, dim_mults=(1, 2, 4, 8)):
        super().__init__()
        self.time_embed = TimestepEmbedding(base_dim * 4)
        
        # Simplified UNet structure
        dims = [in_channels] + [base_dim * m for m in dim_mults]
        
        self.encoders = nn.ModuleList()
        self.decoders = nn.ModuleList()
        self.mid = nn.ModuleList()
        
        # Encoder
        for i in range(len(dims) - 1):
            self.encoders.append(nn.Sequential(
                nn.Conv2d(dims[i], dims[i+1], 3, padding=1),
                nn.GroupNorm(8, dims[i+1]),
                nn.SiLU(),
                nn.Conv2d(dims[i+1], dims[i+1], 3, padding=1),
                nn.GroupNorm(8, dims[i+1]),
                nn.SiLU()
            ))
        
        # Middle
        self.mid.append(nn.Sequential(
            nn.Conv2d(dims[-1], dims[-1], 3, padding=1),
            nn.GroupNorm(8, dims[-1]),
            nn.SiLU(),
            nn.Conv2d(dims[-1], dims[-1], 3, padding=1),
        ))
        
        # Decoder (mirrored)
        for i in reversed(range(len(dims) - 1)):
            self.decoders.append(nn.Sequential(
                nn.Conv2d(dims[i+1], dims[i], 3, padding=1),
                nn.GroupNorm(8, dims[i]),
                nn.SiLU(),
                nn.Conv2d(dims[i], dims[i], 3, padding=1),
            ))
        
        self.out_conv = nn.Conv2d(dims[1], in_channels, 1)
    
    def forward(self, x_t, t):
        """
        Args:
            x_t: noisy input at timestep t, shape (B, C, H, W)
            t: timestep [0, 1], shape (B,)
        Returns:
            pred_x0: prediction of clean data, shape (B, C, H, W)
        """
        t_emb = self.time_embed(t)  # (B, dim)
        
        # Encoder path
        skips = []
        x = x_t
        for enc in self.encoders:
            x = enc(x)
            skips.append(x)
        
        # Middle
        x = self.mid[0](x)
        x = x + t_emb.unsqueeze(2).unsqueeze(3) * 0.1  # AdaGN-like injection
        
        # Decoder path
        for i, dec in enumerate(self.decoders):
            x = dec(x)
            if i < len(skips):
                x = x + skips[-(i+1)]  # Skip connection
        
        return self.out_conv(x)
    
    @torch.no_grad()
    def sample(self, shape, steps=1, device='cpu'):
        """
        Sample en 1 paso (o N pasos con predictor-corrector).
        
        Args:
            shape: (batch, channels, height, width)
            steps: número de refinamiento (1 para más rápido)
        """
        x = torch.randn(shape, device=device)
        
        if steps == 1:
            # Single-step: direct mapping
            t = torch.ones(shape[0], device=device)
            pred = self(x, t)
            return pred
        
        # Multi-step refinement
        timesteps = torch.linspace(1.0, 0.0, steps + 1, device=device)
        for i in range(steps):
            t = timesteps[i].expand(x.shape[0])
            pred = self(x, t)
            # Euler step refinement
            t_next = timesteps[i + 1].expand(x.shape[0])
            x = pred + (t_next - t).unsqueeze(1) * (pred - x) / (t + 1e-8)
        
        return self(x, timesteps[-1].expand(x.shape[0]))


class EMAModel:
    """Exponential Moving Average para estabilidad del modelo."""
    def __init__(self, model, decay=0.9999):
        self.model = model
        self.decay = decay
        self.shadow = {
            k: v.clone().detach()
            for k, v in model.state_dict().items()
        }
        self.buffer = []
    
    def update(self, model):
        for name, param in model.state_dict().items():
            self.shadow[name] = (
                self.shadow[name] * self.decay
                + param.detach() * (1 - self.decay)
            )
    
    def apply_shadow(self):
        if self.shadow:
            self.buffer = [
                v.clone() for v in self.model.state_dict().values()
            ]
            self.model.load_state_dict(self.shadow, strict=False)
    
    def restore(self):
        if self.buffer:
            self.model.load_state_dict(dict(zip(
                self.model.state_dict().keys(), self.buffer
            )))
```

### 4.2 Training de Consistency Distillation

```python
def consistency_distillation_loss(model, x_0, t, alpha_fn=torch.sigmoid):
    """
    Loss para consistency distillation.
    
    El diffusion model genera x_t a partir de x_0.
    El CM debe predecir x_0 directamente desde x_t.
    """
    # Simulate diffusion forward: x_t = sqrt(alpha_t) * x_0 + sqrt(1 - alpha_t) * eps
    alpha = alpha_fn(t)
    noise = torch.randn_like(x_0)
    x_t = torch.sqrt(alpha) * x_0 + torch.sqrt(1 - alpha) * noise
    
    # CM predicts x_0 from x_t
    pred_x0 = model(x_t, t)
    
    # Primary loss: prediction should match x_0
    loss = F.mse_loss(pred_x0, x_0)
    
    # Consistency regularization: predictions at different t should agree
    t2 = torch.clamp(t + 0.1, max=1.0)
    alpha2 = alpha_fn(t2)
    x_t2 = torch.sqrt(alpha2) * x_0 + torch.sqrt(1 - alpha2) * noise
    pred_x0_2 = model(x_t2, t2)
    
    consistency_loss = F.mse_loss(pred_x0, pred_x0_2)
    
    return loss + 0.1 * consistency_loss


def train_consistency_model(
    model, dataloader, num_epochs=100, lr=1e-4, device='cuda'
):
    """
    Training loop para Consistency Model con distillation.
    """
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, num_epochs)
    ema = EMAModel(model, decay=0.9999)
    
    model.train()
    for epoch in range(num_epochs):
        total_loss = 0
        for x_0 in tqdm(dataloader, desc=f"Epoch {epoch+1}/{num_epochs}"):
            x_0 = x_0.to(device)
            
            # Sample random timestep
            t = torch.rand(x_0.shape[0], device=device)
            
            # Compute loss
            loss = consistency_distillation_loss(model, x_0, t)
            
            optimizer.zero_grad()
            loss.backward()
            
            # Gradient clipping for stability
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            
            optimizer.step()
            ema.update(model)
            total_loss += loss.item()
        
        scheduler.step()
        
        if (epoch + 1) % 10 == 0:
            avg_loss = total_loss / len(dataloader)
            print(f"  Epoch {epoch+1}: loss={avg_loss:.6f}")
    
    return ema
```

### 4.3 Progressive Training Pipeline

```python
class ProgressiveConsistencyTraining:
    """
    Pipeline de entrenamiento progresivo para Consistency Models.
    
    Entrena CM a resoluciones crecientes, usando el CM de resolución
    inferior como teacher para distillation.
    """
    
    def __init__(self, config):
        self.config = config
        self.sizes = [32, 64, 128, 256]
        self.teachers = {}
    
    def train_stage(self, stage_idx, num_epochs=50, lr=1e-4):
        """Train CM at current resolution using teacher from previous stage."""
        size = self.sizes[stage_idx]
        
        # Load teacher (CM from previous resolution)
        teacher = None
        if stage_idx > 0:
            teacher = self.teachers[self.sizes[stage_idx - 1]]
        
        # Initialize student
        student = ConsistencyModel(
            in_channels=3,
            base_dim=64,
            dim_mults=(1, 2, 4, 8)
        )
        
        # Progressive distillation training
        optimizer = torch.optim.AdamW(student.parameters(), lr=lr)
        
        for epoch in range(num_epochs):
            for x_0 in dataloader:
                # Scale to current resolution
                x_0 = F.interpolate(x_0, size=size, mode='bilinear')
                
                # Sample random timestep
                t = torch.rand(x_0.shape[0], device=x_0.device)
                
                if teacher is not None:
                    # Teacher distillation loss
                    # Generate pseudo-targets from teacher
                    alpha = torch.sigmoid(t)
                    noise = torch.randn_like(x_0)
                    x_t = torch.sqrt(alpha) * x_0 + torch.sqrt(1 - alpha) * noise
                    
                    # Teacher predicts x_0
                    teacher.apply_shadow()
                    with torch.no_grad():
                        teacher_pred = teacher(x_t, t)
                    
                    # Student should match teacher's output
                    student_pred = student(x_t, t)
                    loss = F.mse_loss(student_pred, teacher_pred.detach())
                else:
                    # Standard consistency distillation
                    loss = consistency_distillation_loss(student, x_0, t)
                
                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(student.parameters(), 1.0)
                optimizer.step()
            
            ema.update(student)
        
        self.teachers[size] = student
        return student
    
    @torch.no_grad()
    def sample(self, shape, size=256, steps=1):
        """Sample from the largest trained CM."""
        cm = self.teachers[self.sizes[-1]]
        return cm.sample(shape, steps=steps, device='cuda')
```

### 4.4 Comparación de Velocidad

```python
def demo_speed_comparison():
    """
    Demostración de generación en 1 paso vs DDPM.
    """
    # Simulated timing comparison (per image, A100 GPU)
    step_time_ms = 10  # ~10ms per forward pass on A100
    
    ddpm_steps = 1000
    ddim_steps = 50
    cm_steps = 1
    
    ddpm_time_s = ddpm_steps * step_time_ms / 1000  # 10 seconds
    ddim_time_s = ddim_steps * step_time_ms / 1000  # 0.5 seconds
    cm_time_s = cm_steps * step_time_ms / 1000      # 0.01 seconds
    
    print("=" * 50)
    print("COMPARACIÓN DE VELOCIDAD (por imagen, A100)")
    print("=" * 50)
    print(f"DDPM:   {ddpm_steps:4d} pasos → {ddpm_time_s:6.2f}s")
    print(f"DDIM:   {ddim_steps:4d} pasos → {ddim_time_s:6.2f}s")
    print(f"CM:        {cm_steps:4d} paso  → {cm_time_s:6.3f}s")
    print()
    print(f"Speedup CM vs DDPM: {ddpm_time_s/c_time_s:0.0f}x")
    print(f"Speedup CM vs DDIM: {ddim_time_s/cm_time_s:0.0f}x")
    
    # Typical FID comparison on ImageNet 256x256
    print()
    print("FID scores (ImageNet 256×256, lower is better):")
    print("-" * 50)
    fid_scores = [
        ("DDPM", 3.17),
        ("DDIM (50 pasos)", 3.50),
        ("DPM-Solver++ (20 pasos)", 3.30),
        ("Consistency Model (1 paso)", 3.50),
        ("Progressive CM (1 paso)", 3.10),
        ("Consistency DiT (1 paso)", 2.55),
    ]
    for method, fid in sorted(fid_scores, key=lambda x: x[1]):
        marker = " ⭐" if fid < 3.0 else ""
        print(f"  {method:35s}: {fid:.2f}{marker}")


demo_speed_comparison()
```

### 4.5 LCM (Latent Consistency Models) — Fine-tuning Práctico

```python
"""
LCM (Latent Consistency Models) — Fine-tuning de Stable Diffusion.

Este es el enfoque más práctico para producción:
1. Toma un SD/SDXL pre-entrenado
2. Aplica LCM-LoRA con ~8-16 GPU steps
3. Obtienes generación en 4 pasos con calidad de 20+ pasos

Referencia: https://github.com/luosiallen/Consistency-Adaptor
"""

def lcm_finetuning_pipeline():
    """
    Pipeline de fine-tuning LCM sobre Stable Diffusion.
    
    Pasos:
    1. Cargar SD/SDXL pre-entrenado
    2. Añadir LoRA adapter
    3. Entrenar con consistency distillation loss
    4. Exportar LoRA weights
    """
    print("LCM Fine-tuning Pipeline")
    print("=" * 50)
    print()
    print("Paso 1: Cargar modelo base")
    print("  model = StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')")
    print()
    print("Paso 2: Añadir LoRA adapter")
    print("  lora_rank = 4  # Muy bajo, solo consistency")
    print("  lora_module = 'unet.down_blocks.0.attentions.0'")
    print()
    print("Paso 3: Training con consistency distillation")
    print("  - Dataset: ~10K imágenes (pequeño)")
    print("  - Epochs: 10-20")
    print("  - LR: 1e-4 con cosine scheduler")
    print("  - Steps: ~8-16 por imagen para distillation")
    print()
    print("Paso 4: Exportar LoRA weights")
    print("  output: lcm-lora.safetensors")
    print()
    print("Resultado:")
    print("  - 4 pasos: calidad comparable a SD con 20+ pasos")
    print("  - 1 paso: usable, FID ~3.0 en ImageNet")
    print("  - Velocidad: ~10x más rápido que SD con DDIM-20")


lcm_finetuning_pipeline()
```

---

## 5. Aplicaciones Prácticas

### 5.1 Generación de Imágenes en Tiempo Real

- **Video generation:** 30fps requiere <33ms por frame
- CM en 1 paso: ~10-50ms en GPU moderna → **viable**
- Diffusion tradicional: ~10s → **imposible**

### 5.2 Fine-tuning de Modelos de Diffusion Existentes

- No necesitas reentrenar desde cero
- Puedes aplicar **consistency distillation** sobre cualquier DDPM pre-entrenado
- HuggingFace Diffusers soporta CM via `ConsistencyModelPipeline`

### 5.3 Edge Deployment

- Modelo más pequeño (1 paso = menos ops)
- Ideal para dispositivos móviles y edge
- Compatible con TensorRT, TFLite, ONNX

### 5.4 Control Conditional

- Compatible con Classifier-Free Guidance
- Compatible con ControlNet-style conditioning
- Permite editing en 1 paso (consistency editing)

---

## 6. Estado del Arte (2024-2025)

### Modelos Destacados

1. **LCM (Latent Consistency Models)** — Tencent
   - CM en espacio latente (Latent Diffusion)
   - 4 pasos en latent space ≈ calidad de 20+ pasos
   - Compatible con Stable Diffusion

2. **SDXL-LCM** — CompVis + Stability AI
   - LCM fine-tuned sobre SDXL
   - 4-8 pasos con calidad comparable a 20+ pasos
   - Disponible en HuggingFace

3. **PixArt-α Consistency** — PixArt team
   - CM basado en DiT (Diffusion Transformer)
   - FID 2.55 en ImageNet 256×256 en 1 paso
   - Arquitectura más eficiente que UNet

4. **Consistency Flow** — Meta FAIR
   - Combina flow matching con consistency
   - Mejor stability en training
   - Compatible con rectified flow

---

## 7. Limitaciones y Desafíos

### 7.1 Training Instability

- Training CM directamente es más inestable que DDPM
- Progressive distillation ayuda pero añade complejidad
- Necesita buen scheduling de learning rate

### 7.2 Calidad vs Velocidad Trade-off

- 1 paso: más rápido pero FID ligeramente peor
- 4-8 pasos: casi tan rápido como DDIM-50, FID cercano a DDPM
- El sweet spot depende del use case

### 7.3 Coverage Problem

- CM puede sufrir de mode collapse más que DDPM
- La función de consistencia debe ser suave en todo el espacio
- Las colas de la distribución son difíciles de modelar

### 7.4 Computación de Training

- Requiere DDPM pre-entrenado o trajectory sampling costoso
- Progressive training multiplica el costo de training
- No es práctico para datasets muy grandes sin infraestructura

---

## 8. Código Completo de Referencia

```python
"""
Consistency Model completo — Entrenamiento + Inference.

Este script implementa un CM mínimo funcional para MNIST/CIFAR-10.
Para producción, usar HuggingFace Diffusers con modelos pre-entrenados.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import numpy as np


def create_cifar_dataloader(batch_size=128):
    """Crea DataLoader para CIFAR-10."""
    transform = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])
    dataset = datasets.CIFAR10('./data', train=True, download=True, transform=transform)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=2)


def generate_samples(model, num_samples=16, image_size=32, device='cpu'):
    """Genera samples del CM."""
    model.eval()
    with torch.no_grad():
        shape = (num_samples, 3, image_size, image_size)
        samples = model.sample(shape, steps=1, device=device)
        # Denormalize
        samples = (samples + 1) / 2
        samples = samples.clamp(0, 1)
    return samples


if __name__ == '__main__':
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    
    # Create model
    model = ConsistencyModel(in_channels=3, base_dim=64, dim_mults=(1, 2, 4, 8))
    model = model.to(device)
    
    # Create dataloader
    dataloader = create_cifar_dataloader(batch_size=128)
    
    # Train
    ema = train_consistency_model(model, dataloader, num_epochs=50, lr=1e-4, device=device)
    
    # Generate samples
    samples = generate_samples(ema.model, num_samples=16, image_size=32, device=device)
    print(f"Generated {samples.shape[0]} samples")
```

---

## 9. Referencias Clave

1. **Song et al. (2023)** — ["Consistency Models"](https://arxiv.org/abs/2303.01469) — ICML 2024
2. **Song et al. (2023)** — ["Progressive Consistency Distillation"](https://arxiv.org/abs/2310.04476)
3. **Liu et al. (2022)** — ["Rectified Flow: A Parallel Discretization Scheme"](https://arxiv.org/abs/2209.03003)
4. **Tencent LCM** — ["Latent Consistency Models"](https://arxiv.org/abs/2310.04378)
5. **HuggingFace Diffusers** — https://github.com/huggingface/diffusers

---

## 10. ¿Qué Aprender Después?

**Siguiente tema recomendado: Neural Architecture Search (NAS)**

NAS es el campo que automatiza el diseño de arquitecturas de redes neuronales.
Con la explosión de variantes de transformers, diffusion, y state space models,
NAS puede ayudar a encontrar arquitecturas óptimas para constraints específicos
(velocidad, memoria, precisión).

**Alternativas:**
- **Meta-Learning / MAML** — Aprender a aprender: adaptación rápida con pocos ejemplos
- **Federated Learning** — Entrenamiento distribuido con privacidad
- **Continual / Lifelong Learning** — Aprendizaje sin forgetting
