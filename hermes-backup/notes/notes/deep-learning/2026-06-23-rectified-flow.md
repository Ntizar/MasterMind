# Rectified Flow — De SDEs a ODEs Líneales para Generación de Alta Calidad

## Resumen Ejecutivo

**Rectified Flow** es un método de generación que rectifica (endereza) las trayectorias de transporte entre distribuciones, transformando las trayectorias curvas de los diffusion models en trayectorias casi rectas. Esto permite **muy pocos pasos de inferencia** (incluso 1 paso con Consistency Distillation) y **calidad comparable o superior** a los diffusion models tradicionales.

Es la base de **FLUX** (Black Forest Labs, 25K+ stars), **Stable Diffusion 3**, y muchos de los modelos de generación más avanzados de 2024-2026.

---

## 1. Contexto: ¿Por qué Rectified Flow?

### El problema de los Diffusion Models

Los diffusion models tradicionales (DDPM, Ho et al. 2020) tienen dos problemas fundamentales:

1. **Inferencia lenta**: Requieren 50-1000 pasos de Euler-Maruyama para generar una imagen
2. **Trayectorias curvas**: La interpolación lineal en espacio de ruido no corresponde a la ruta óptima en el espacio de datos

### La intuición de Rectified Flow

> Si en lugar de interpolarse linealmente entre ruido y datos, interpolamos de forma que el campo de velocidad sea lo más recto posible, la ODE se integra con mucho menos pasos.

**Analogía**: Imagina que quieres ir de Madrid a Barcelona. Un diffusion model va en curva (Madrid → Zaragoza → Lérida → Barcelona). Rectified Flow encuentra la ruta casi recta (Madrid → Barcelona directo).

---

## 2. Fundamentos Teóricos

### 2.1 Flow Matching

El framework general de **Flow Matching** (Lipman et al., 2023) define un campo de velocidad $u_t(x)$ que transporta una distribución fuente $p_0$ (normal) a una distribución objetivo $p_1$ (datos):

$$\frac{dx_t}{dt} = u_t(x_t), \quad x_0 \sim p_0, \quad x_1 \sim p_1$$

La red neuronal aprende a predecir el campo de velocidad $u_t(x)$.

### 2.2 Rectified Flow (Liu et al., 2022/2023)

Rectified Flow es una variante específica de Flow Matching con una intuición clave:

**Paso 1 — Rectificación**: Dadas muestras emparejadas $(x_0, x_1)$, interpolamos linealmente:

$$x_t = (1-t)x_0 + t x_1, \quad t \sim U[0,1]$$

La velocidad "ground truth" es: $v = x_1 - x_0$

**Paso 2 — Entrenamiento**: Entrenamos una red $v_\theta(x_t, t)$ para predecir esta velocidad:

$$\mathcal{L}(\theta) = \mathbb{E}_{t,x_0,x_1}[\|v_\theta((1-t)x_0 + tx_1, t) - (x_1 - x_0)\|^2]$$

**Paso 3 — Rectificación iterativa**: Una vez entrenada la red, generamos nuevas trayectorias usando la ODE resuelta con $v_\theta$, y usamos esas trayectorias rectas para re-entrenar. Esto se repite iterativamente:

```
Iteración 0: x_t = (1-t)x_0 + t*x_1  (interpolación lineal)
Iteración k: x_t = (1-t)x_0^k + t*x_1^k  (trayectorias de la ODE de v_{θ_{k-1}})
```

Cada iteración endereza más las trayectorias → menos pasos de inferencia necesarios.

### 2.3 Relación con otros métodos

| Método | Inferencia | Base teórica |
|--------|-----------|-------------|
| DDPM | 50-1000 pasos | SDE (score matching) |
| DPM-Solver | 10-20 pasos | SDE → ODE + solver avanzado |
| Flow Matching | 4-12 pasos | Optimal transport |
| **Rectified Flow** | **1-4 pasos** | **ODE con trayectorias rectas** |
| InstaFlow | **1 paso** | Rectified Flow + Consistency Distillation |

---

## 3. Implementación Práctica

### 3.1 Implementación Mínima de Rectified Flow

```python
"""
Rectified Flow — Implementación mínima desde cero
Entrenamiento + inferencia para distribución 1D
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torchdiffeq import odeint  # pip install torchdiffeq


class VelocityNet(nn.Module):
    """Red neuronal que predice el campo de velocidad v_t(x).
    
    Architecture: MLP con sinusoidal embedding de tiempo.
    """
    def __init__(self, input_dim=1, hidden_dim=128, n_layers=4):
        super().__init__()
        self.time_embed = nn.Sequential(
            nn.Linear(1, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        layers = []
        for _ in range(n_layers):
            layers.extend([
                nn.Linear(hidden_dim + 1, hidden_dim),  # +1 para x
                nn.SiLU(),
                nn.LayerNorm(hidden_dim),
            ])
        layers.append(nn.Linear(hidden_dim, input_dim))
        self.net = nn.Sequential(*layers)
    
    def forward(self, x, t):
        """
        Args:
            x: (batch, input_dim) — posición en el espacio
            t: (batch, 1) — tiempo normalizado [0, 1]
        Returns:
            v: (batch, input_dim) — velocidad predicha
        """
        t_emb = self.time_embed(t)  # (batch, hidden)
        xt = torch.cat([x, t], dim=-1)  # (batch, input_dim + 1)
        h = self.net[0](xt)  # primera capa: input_dim+1 → hidden
        h = h + t_emb  # residual connection con tiempo
        for layer in self.net[1:]:
            if isinstance(layer, nn.Linear):
                h = layer(h)
            else:
                h = layer(h)
        return h


def rectify_velocity_field(data_samples, n_iterations=3, n_steps=256):
    """
    Entrenamiento iterativo de Rectified Flow.
    
    Args:
        data_samples: tensor (N, dim) — muestras de la distribución objetivo
        n_iterations: número de iteraciones de rectificación
        n_steps: pasos de integración para la ODE
    
    Returns:
        velocity_net: red entrenada
    """
    dim = data_samples.shape[1]
    device = data_samples.device
    
    # Inicializar red
    net = VelocityNet(input_dim=dim, hidden_dim=256, n_layers=6).to(device)
    optimizer = torch.optim.AdamW(net.parameters(), lr=3e-4, weight_decay=1e-4)
    
    N = len(data_samples)
    
    for iteration in range(n_iterations):
        print(f"\n=== Iteración {iteration + 1}/{n_iterations} ===")
        
        for step in range(500):  # 500 steps de entrenamiento por iteración
            # Muestrear batch
            idx = torch.randint(N, (N,))
            x0 = data_samples[idx].to(device)  # muestra fuente (datos)
            
            # Muestrear ruido como distribución fuente
            x1 = torch.randn_like(x0)  # distribución gaussiana
            
            # Muestrear tiempo
            t = torch.rand(N, 1, device=device)
            
            # Interpolación: x_t = (1-t)*x0 + t*x1
            # Nota: x0 es datos, x1 es ruido
            # En la convención de Liu et al., x0 = ruido, x1 = datos
            # Invertimos para que t=0 → ruido, t=1 → datos
            x_t = (1 - t) * x1 + t * x0
            
            # Velocidad ground truth
            v_true = x0 - x1
            
            # Predicción de la red
            v_pred = net(x_t, t)
            
            # Loss MSE
            loss = F.mse_loss(v_pred, v_true)
            
            # Backprop
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
            optimizer.step()
            
            if step % 100 == 0:
                print(f"  Step {step}: loss = {loss.item():.6f}")
        
        # --- Rectificación: generar trayectorias con la ODE ---
        print(f"  Rectificando trayectorias...")
        # Generar nuevas muestras de datos usando la red actual
        # (en la práctica, esto se hace con un subset de datos reales)
        # Para este ejemplo simplificado, mantenemos los datos originales
    
    return net


def sample_with_ode(net, n_samples=100, dim=1, n_eval_steps=100):
    """
    Generar muestras resolviendo la ODE inversa.
    
    Args:
        net: red de velocidad entrenada
        n_samples: número de muestras a generar
        dim: dimensión del espacio
        n_eval_steps: pasos de integración
    
    Returns:
        samples: (n_samples, dim) — muestras generadas
    """
    device = next(net.parameters()).device
    
    # Iniciar desde ruido gaussiano (t=0)
    x0 = torch.randn(n_samples, dim, device=device)
    t_span = torch.linspace(0, 1, n_eval_steps, device=device)
    
    # Resolver ODE inversa: dx/dt = v(x, t)
    # Para ir de t=0 (ruido) a t=1 (datos)
    def ode_fn(t, x):
        return net(x, t * torch.ones_like(x[..., :1]))
    
    # torchdiffeq resuelve dx/dt = f(t, x)
    # x tiene forma (n_samples, dim)
    x0_ode = x0.reshape(n_samples, dim)
    
    with torch.no_grad():
        trajectory = odeint(ode_fn, x0_ode, t_span, method='euler')
    
    # La última posición son las muestras generadas
    samples = trajectory[-1]
    return samples


def sample_one_step(net, n_samples=100, dim=1):
    """
    Generación con un solo paso (consistency-style).
    
    Si las trayectorias están suficientemente rectas,
    podemos saltar directamente de t=0 a t=1.
    """
    device = next(net.parameters()).device
    
    x_noise = torch.randn(n_samples, dim, device=device)
    t = torch.ones(n_samples, 1, device=device)
    
    with torch.no_grad():
        v = net(x_noise, t * 0)  # evaluar en t=0
        # Euler step: x_1 = x_0 + v * 1
        x_generated = x_noise + v
    
    return x_generated


# ============================================================
# Demo: Entrenar con una distribución bimodal 2D
# ============================================================

def create_bimodal_dataset(n_samples=5000):
    """Crear dataset bimodal 2D para demo."""
    np.random.seed(42)
    n_per_mode = n_samples // 2
    
    # Modo 1: centro en (2, 2)
    x1 = np.random.randn(n_per_mode, 2) * 0.5 + np.array([2, 2])
    # Modo 2: centro en (-2, -2)
    x2 = np.random.randn(n_samples - n_per_mode, 2) * 0.5 + np.array([-2, -2])
    
    data = np.vstack([x1, x2]).astype(np.float32)
    return torch.tensor(data)


if __name__ == "__main__":
    # Crear dataset
    data = create_bimodal_dataset(5000)
    print(f"Dataset: {data.shape}")
    
    # Entrenar
    net = rectify_velocity_field(data, n_iterations=2, n_steps=256)
    
    # Generar muestras
    samples = sample_with_ode(net, n_samples=500, dim=2, n_eval_steps=100)
    print(f"Muestras generadas: {samples.shape}")
    
    # Generar con un solo paso
    one_step_samples = sample_one_step(net, n_samples=500, dim=2)
    print(f"Muestras 1-step: {one_step_samples.shape}")
```

### 3.2 Rectified Flow con Latent Space (como FLUX/Stable Diffusion)

En la práctica, los modelos de generación de imágenes trabajan en **espacio latente** (como Latent Diffusion), no en pixel space:

```python
"""
Rectified Flow en espacio latente — Patrón FLUX/Stable Diffusion 3
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class RectifiedFlowTransformer(nn.Module):
    """
    Transformer para Rectified Flow en espacio latente.
    
    Inspirado en FLUX.1 (Black Forest Labs):
    - DiT (Diffusion Transformer) con AdaLN-Zero
    - Text conditioning con CLIP/LLM embeddings
    - Timestep embedding con sinusoidal + learnable
    
    Args:
        in_channels: canales del latente (4 para VAE latente)
        vec_in_dim: dimensión del timestep embedding
        context_in_dim: dimensión del contexto (texto)
        hidden_size: dimensión del transformer
        depth: número de capas transformer
        heads: número de attention heads
        mlp_ratio: ratio de la capa MLP
    """
    def __init__(
        self,
        in_channels=4,
        vec_in_dim=768,
        context_in_dim=4096,
        hidden_size=1024,
        depth=12,
        heads=8,
        mlp_ratio=4.0,
    ):
        super().__init__()
        self.in_channels = in_channels
        self.hidden_size = hidden_size
        heads = hidden_size // 64  # head_dim = 64
        self.heads = heads
        
        # Timestep embedding
        self.time_embed = nn.Sequential(
            nn.Linear(vec_in_dim, hidden_size),
            nn.SiLU(),
            nn.Linear(hidden_size, hidden_size),
        )
        
        # Text context embedding (proviene de CLIP/LLM)
        self.context_embed = nn.Sequential(
            nn.Linear(context_in_dim, hidden_size),
            nn.SiLU(),
            nn.Linear(hidden_size, hidden_size),
        )
        
        # Input projection
        self.input_proj = nn.Linear(in_channels, hidden_size)
        
        # Transformer blocks con AdaLN-Zero
        self.blocks = nn.ModuleList([
            DiTBlock(
                hidden_size=hidden_size,
                heads=heads,
                mlp_ratio=int(mlp_ratio),
            )
            for _ in range(depth)
        ])
        
        # Output projection
        self.output_proj = nn.Linear(hidden_size, in_channels)
        
        # Final normalization
        self.norm = nn.LayerNorm(hidden_size)
    
    def forward(self, x, t, context=None):
        """
        Args:
            x: (batch, channels, height, width) — latente + padding
            t: (batch,) — timestep scalar [0, 1]
            context: (batch, seq_len, context_dim) — texto embebido
        
        Returns:
            predicted_velocity: (batch, channels, height, width)
        """
        batch, channels, height, width = x.shape
        
        # Embed timestep
        t_emb = self.time_embed(sinusoidal_embedding(t, self.hidden_size))
        
        # Embed context
        if context is not None:
            c_emb = self.context_embed(self.context_embed_seq(context))
        else:
            c_emb = None
        
        # Patchify input (como ViT)
        x_flat = self.input_proj(x.flatten(2).transpose(1, 2))  # (B, HW, C)
        
        # Concatenate timestep embedding
        x_flat = x_flat + t_emb.unsqueeze(1)
        
        # Transformer blocks
        for block in self.blocks:
            x_flat = block(x_flat, c_emb)
        
        # Unpatchify
        x_flat = self.norm(x_flat)
        output = self.output_proj(x_flat)  # (B, HW, C)
        output = output.transpose(1, 2).reshape(batch, channels, height, width)
        
        return output


class DiTBlock(nn.Module):
    """
    DiT Block: Attention + MLP con Adaptive Layer Normalization (AdaLN-Zero).
    
    AdaLN-Zero ajusta la normalización condicionalmente en el timestep,
    permitiendo que el modelo aprenda cuándo activar/desactivar capas.
    """
    def __init__(self, hidden_size, heads, mlp_ratio=4.0):
        super().__init__()
        self.norm1 = nn.LayerNorm(hidden_size, elementwise_affine=False)
        self.attn = nn.MultiheadAttention(
            hidden_size, heads, batch_first=True
        )
        self.norm2 = nn.LayerNorm(hidden_size, elementwise_affine=False)
        
        mlp_hidden = int(hidden_size * mlp_ratio)
        self.mlp = nn.Sequential(
            nn.Linear(hidden_size, mlp_hidden),
            nn.GELU(approximate="tanh"),
            nn.Linear(mlp_hidden, hidden_size),
        )
        
        # AdaLN-Zero gates
        self.modulation = nn.Sequential(
            nn.SiLU(),
            nn.Linear(hidden_size, hidden_size * 6),  # 6 gates
        )
    
    def forward(self, x, context=None):
        batch = x.shape[0]
        
        # AdaLN-Zero: generar shifts, scales y gates desde el timestep
        mod = self.modulation(x.mean(dim=1))  # (B, hidden)
        shift_msa, scale_msa, gate_msa, shift_mlp, scale_mlp, gate_mlp = (
            mod.chunk(6, dim=-1)
        )
        
        # Self-attention con AdaLN
        norm_x = self.norm1(x)
        norm_x = (1 + scale_msa) * norm_x + shift_msa
        attn_out = self.attn(norm_x, norm_x, norm_x)[0]
        x = x + gate_msa.unsqueeze(1) * attn_out
        
        # MLP con AdaLN
        norm_x = self.norm2(x)
        norm_x = (1 + scale_mlp) * norm_x + shift_mlp
        mlp_out = self.mlp(norm_x)
        x = x + gate_mlp.unsqueeze(1) * mlp_out
        
        return x


def sinusoidal_embedding(t, dim):
    """Embedding sinusoidal para timestep (como en transformers)."""
    if dim % 2 != 0:
        raise ValueError("dim must be even")
    half = dim // 2
    t = t.unsqueeze(-1)  # (B, 1)
    device = t.device
    emb = torch.log(torch.tensor(10000.0, device=device)) / (half - 1)
    emb = torch.exp(torch.arange(half, device=device, dtype=torch.float32) * -emb)
    emb = t * emb.unsqueeze(0)  # (B, half)
    emb = torch.cat([torch.sin(emb), torch.cos(emb)], dim=-1)  # (B, dim)
    return emb


def consistency_distillation(
    velocity_net,
    data_loader,
    n_distill_steps=1000,
    lr=1e-4
):
    """
    Consistency Distillation para Rectified Flow.
    
    Entrena un modelo de consistencia que mapea directamente
    ruido → datos en un solo paso.
    
    Basado en: "Consistency Models" (Saharia et al., 2022)
    y "InstaFlow" (ICLR 2024).
    
    Args:
        velocity_net: red de velocidad entrenada (teacher)
        data_loader: DataLoader con muestras de datos
        n_distill_steps: pasos de distilación
        lr: learning rate
    
    Returns:
        consistency_net: modelo de consistencia entrenado
    """
    device = next(velocity_net.parameters()).device
    consistency_net = VelocityNet(
        input_dim=velocity_net.input_dim if hasattr(velocity_net, 'input_dim') else 4,
        hidden_dim=256,
        n_layers=6
    ).to(device)
    
    optimizer = torch.optim.AdamW(consistency_net.parameters(), lr=lr)
    
    velocity_net.eval()
    consistency_net.train()
    
    for step in range(n_distill_steps):
        # Muestrear x_t y t
        x1 = next(iter(data_loader)).to(device)  # datos reales
        x0 = torch.randn_like(x1)  # ruido
        t = torch.rand(len(x1), 1, device=device)
        
        x_t = (1 - t) * x0 + t * x1
        
        # Teacher: un paso de Euler desde x_t usando v_t
        with torch.no_grad():
            v_t = velocity_net(x_t, t)
            x_teacher = x_t + v_t * (1 - t)  # un paso hasta t=1
        
        # Student: predecir directamente x_1 desde x_t
        x_student = consistency_net(x_t, t)
        
        # Loss: el student debe predecir lo mismo que el teacher
        loss = F.mse_loss(x_student, x_teacher.detach())
        
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(consistency_net.parameters(), 1.0)
        optimizer.step()
        
        if step % 100 == 0:
            print(f"  Distillation step {step}: loss = {loss.item():.6f}")
    
    return consistency_net
```

### 3.3 Entrenamiento Completo con DataLoader

```python
"""
Pipeline completo de entrenamiento de Rectified Flow
con DataLoader, checkpointing, y evaluación.
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from torchdiffeq import odeint
import matplotlib.pyplot as plt
import numpy as np


class RectifiedFlowTrainer:
    """
    Entrenamiento completo de Rectified Flow.
    
    Uso:
        trainer = RectifiedFlowTrainer(
            net=VelocityNet(input_dim=4),
            data_loader=train_loader,
            n_iterations=3,
            lr=3e-4
        )
        trainer.train()
        samples = trainer.sample(n_samples=64, steps=4)
    """
    
    def __init__(self, net, data_loader, n_iterations=3, lr=3e-4, device='cuda'):
        self.net = net.to(device)
        self.data_loader = data_loader
        self.n_iterations = n_iterations
        self.device = device
        self.optimizer = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=1e-4)
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=n_iterations * 500
        )
    
    def train_iteration(self, n_steps=500):
        """Entrenar una iteración de rectificación."""
        self.net.train()
        total_loss = 0
        
        for step in range(n_steps):
            # Obtener batch de datos
            try:
                x1 = next(self.data_iter)
            except:
                self.data_iter = iter(self.data_loader)
                x1 = next(self.data_iter)
            
            x1 = x1.to(self.device)
            x0 = torch.randn_like(x1)  # ruido
            
            t = torch.rand(len(x1), 1, device=self.device)
            x_t = (1 - t) * x0 + t * x1
            
            v_pred = self.net(x_t, t)
            v_true = x1 - x0
            
            loss = F.mse_loss(v_pred, v_true)
            
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.net.parameters(), 1.0)
            self.optimizer.step()
            self.scheduler.step()
            
            total_loss += loss.item()
        
        return total_loss / n_steps
    
    def rectify(self, n_eval_steps=256):
        """Rectificar trayectorias usando la ODE del modelo actual."""
        self.net.eval()
        rectified_data = []
        
        with torch.no_grad():
            for x1 in self.data_loader:
                x1 = x1.to(self.device)
                x0 = torch.randn_like(x1)
                t_span = torch.linspace(0, 1, n_eval_steps, device=self.device)
                
                def ode_fn(t, x):
                    return self.net(x, t * torch.ones(len(x), 1, device=self.device))
                
                trajectory = odeint(ode_fn, x0, t_span, method='euler')
                x_rect = trajectory[-1]  # posición en t=1
                rectified_data.append(x_rect.cpu())
        
        return torch.cat(rectified_data, dim=0)
    
    def train(self):
        """Entrenamiento completo con rectificación iterativa."""
        self.data_iter = iter(self.data_loader)
        
        for iteration in range(self.n_iterations):
            print(f"\n=== Iteración {iteration + 1}/{self.n_iterations} ===")
            avg_loss = self.train_iteration()
            print(f"  Loss: {avg_loss:.6f}")
            
            if iteration < self.n_iterations - 1:
                # Rectificar datos para la siguiente iteración
                print("  Rectificando...")
                rectified = self.rectify()
                self.data_loader = DataLoader(
                    TensorDataset(rectified),
                    batch_size=self.data_loader.batch_size,
                    shuffle=True
                )
                self.data_iter = iter(self.data_loader)
    
    def sample(self, n_samples, latent_dim=4, steps=4):
        """Generar muestras con la ODE."""
        self.net.eval()
        x0 = torch.randn(n_samples, latent_dim).to(self.device)
        t_span = torch.linspace(0, 1, steps + 1, device=self.device)
        
        def ode_fn(t, x):
            return self.net(x, t * torch.ones(len(x), 1, device=self.device))
        
        with torch.no_grad():
            trajectory = odeint(ode_fn, x0, t_span, method='euler')
        
        return trajectory[-1].cpu()
    
    def save(self, path):
        """Guardar checkpoint."""
        torch.save({
            'model_state': self.net.state_dict(),
            'optimizer_state': self.optimizer.state_dict(),
            'scheduler_state': self.scheduler.state_dict(),
        }, path)
    
    def load(self, path):
        """Cargar checkpoint."""
        checkpoint = torch.load(path, map_location=self.device)
        self.net.load_state_dict(checkpoint['model_state'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state'])
        self.scheduler.load_state_dict(checkpoint['scheduler_state'])
```

---

## 4. Estado del Arte (2024-2026)

### 4.1 Modelos de Producción

| Modelo | Organización | Año | Estrellas | Notas |
|--------|-------------|-----|----------|-------|
| **FLUX.1** | Black Forest Labs | 2024 | 25K+ | Rectified Flow Transformer, SOTA open-source |
| **Stable Diffusion 3** | Stability AI | 2024 | — | Usa Flow Matching + Diffusion Transformer |
| **TripoSG** | VAST AI | 2025 | 1.7K+ | 3D shape synthesis con Rectified Flow |
| **FluxMusic** | — | 2025 | 1.7K+ | Text-to-Music con Rectified Flow Transformers |
| **InstaFlow** | — | 2024 | 1.4K+ | One-step Stable Diffusion con Rectified Flow |

### 4.2 Líneas de Investigación Recientes

1. **Variational Rectified Flow** (Guo & Schwing, 2025) — Modela campos de velocidad multi-modal usando mezclas de Gaussianas
2. **Hierarchical Rectified Flow** (2025) — Acopla múltiples ODEs jerárquicamente para capturar campos de velocidad completos
3. **RAC** (2026) — Rectified Flow Auto Coder que reemplaza VAEs tradicionales con decodificación multi-paso corregible
4. **FluxSpace** (2024) — Edición disentangled en modelos Rectified Flow Transformers
5. **Statistical Properties of Rectified Flow** (2025) — Análisis teórico: convergencia, existencia, unicidad

### 4.3 Relación con Consistency Models

Rectified Flow y Consistency Models son complementarios:

```
Rectified Flow → Trayectorias rectas → Pocos pasos
     ↓
Consistency Distillation → Un solo paso
     ↓
InstaFlow → SD3 con 1 paso de inferencia
```

La **Consistency Distillation** entrena un modelo student que aprende a mapear directamente ruido → datos, aprovechando que las trayectorias de Rectified Flow son casi rectas.

---

## 5. Comparativa con Diffusion Models

| Aspecto | DDPM | Flow Matching | Rectified Flow |
|---------|------|--------------|----------------|
| **Formulación** | SDE | ODE con CT | ODE con trayectorias rectas |
| **Pasos inferencia** | 50-1000 | 4-12 | 1-4 |
| **Calidad FID** | Bueno | Muy bueno | Excelente |
| **Entrenamiento** | Score matching | Flow matching | Velocity matching |
| **Inferencia paralela** | No | No | Sí (trayectorias rectas) |
| **Consistency distillation** | Difícil | Fácil | Muy fácil |
| **Uso en producción** | Legacy | Creciente | Dominante (2024-2026) |

---

## 6. Aplicaciones Prácticas

### 6.1 Generación de Imágenes
- FLUX.1: el modelo open-source más popular para generación de imágenes
- Stable Diffusion 3: primer modelo de Stability AI basado en Flow Matching

### 6.2 Generación de Audio/Música
- **FluxMusic**: text-to-music con Rectified Flow Transformers
- Modelos de speech synthesis basados en flow matching

### 6.3 Generación 3D
- **TripoSG**: síntesis de formas 3D de alta fidelidad con Rectified Flow
- Generación de nubes de puntos y meshes

### 6.4 Autoencoders
- **RAC** (2026): reemplaza VAEs con Rectified Flow Auto Coder
- 70% menos coste computacional, mejor reconstrucción y generación

### 6.5 Series Temporales
- Conexión con el tema de Diffusion Models para series temporales (nota anterior)
- Flow matching puede modelar distribuciones temporales complejas

---

## 7. Recursos Clave

### Papers
1. **Rectified Flow** — Liu et al., ICLR 2023 Spotlight
   - arXiv:2210.02747
2. **Flow Matching for Generative Modeling** — Lipman et al., ICLR 2023
   - arXiv:2302.00410
3. **InstaFlow: One-Step Stable Diffusion with Rectified Flow** — ICLR 2024
4. **Consistency Models** — Saharia et al., ICML 2022
5. **Variational Rectified Flow Matching** — Guo & Schwing, 2025
   - arXiv:2502.09616
6. **Towards Hierarchical Rectified Flow** — 2025
   - arXiv:2502.17436
7. **RAC: Rectified Flow Auto Coder** — 2026
   - arXiv:2603.xxx

### Repositorios GitHub
- [gnobitab/RectifiedFlow](https://github.com/gnobitab/RectifiedFlow) — 1618⭐ Implementación oficial
- [gnobitab/InstaFlow](https://github.com/gnobitab/InstaFlow) — 1409⭐ One-step generation
- [black-forest-labs/flux](https://github.com/black-forest-labs/flux) — 25K⭐ FLUX inference
- [VAST-AI-Research/TripoSG](https://github.com/VAST-AI-Research/TripoSG) — 1704⭐ 3D synthesis
- [feizc/FluxMusic](https://github.com/feizc/FluxMusic) — 1712⭐ Text-to-Music
- [huggingface/diffusers](https://github.com/huggingface/diffusers) — 33K⭐ Soporta Flow Matching

### Implementaciones de referencia
- Hugging Face Diffusers: `Diffusers` soporta `FlowMatchEulerDiscreteScheduler`
- PyTorch `torchdiffeq`: para resolver ODEs con adaptative stepping

---

## 8. Conclusiones

**Rectified Flow** representa la evolución natural de los diffusion models:
- **Más eficiente**: 1-4 pasos vs 50-1000
- **Más simple**: ODE en lugar de SDE, sin score matching
- **Más escalable**: Transformers en lugar de U-Nets (FLUX)
- **Más versátil**: imágenes, audio, 3D, series temporales

Es el framework de generación dominante en 2024-2026, y su adopción continúa creciendo. Para cualquier proyecto de generación de contenido, debería ser el primer enfoque a considerar.

---

## Tema Propuesto para la Próxima Sesión

**Chain-of-Thought Reasoning en LLMs** — Un tema completamente diferente que aborda el razonamiento en modelos de lenguaje, con implementaciones prácticas de prompting, training, y evaluación. Es complementario a los temas de generación ya cubiertos y tiene aplicaciones directas en el stack actual.

Alternativa: **Contrastive Learning & Self-Supervised Learning** — Fundamentos de CLIP, SimCLR, DINO, con implementaciones prácticas. Muy relevante para el contexto de modelos multimodales.
