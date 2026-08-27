# Diffusion Models — Fundamentos, Implementación y Aplicaciones a Series Temporales

**Fecha:** 2026-06-13  
**Tema:** Deep Learning — Modelos de Difusión  
**Contexto:** Stack ESIOS/REE, MicroVM 1vCPU/2GB, skill SSM existente

---

## 1. ¿Qué son los Diffusion Models?

Los Diffusion Models (DM) son modelos generativos que aprenden a **invertir un proceso de difusión de ruido**. La idea central es simple pero poderosa:

1. **Forward (difusión):** Se añade ruido gaussiano progresivamente a los datos hasta convertirlos en ruido puro.
2. **Reverse (denoising):** Una red neuronal aprende a predecir y eliminar ese ruido paso a paso, generando datos nuevos.

La magia está en que el proceso reverse, entrenado con gradientes, produce muestras de alta calidad que siguen la distribución real de los datos.

### Por qué son diferentes

- **GANs:** Entrenan generador vs discriminador (inestable, mode collapse). DM son **estables** — solo necesitas maximizar la verosimilitud.
- **Autoregresivos (GPT, LSTM):** Predicen un paso a la vez, error se acumula. DM generan **todo el output de golpe**, refinando iterativamente.
- **Variacionales (VAE):** Kompromiso entre calidad y diversidad. DM ofrecen **calidad superior** con mejor fidelidad.

---

## 2. Fundamentos Matemáticos

### Proceso Forward (Fijado, no aprendido)

Dada una muestra `x_0`, añadimos ruido durante `T` pasos:

```
q(x_t | x_{t-1}) = N(x_t; √(1-β_t) · x_{t-1}, β_t · I)
```

Donde `β_t` es un schedule de ruido (linear, cosine, cosine). La muestra en cualquier paso `t` es:

```
x_t = √(ᾱ_t) · x_0 + √(1-ᾱ_t) · ε,   donde ε ~ N(0, I)
```

Esto permite **reparametrización**: podemos calcular `x_t` directamente desde `x_0` y ε, sin pasar por todos los pasos intermedios.

### Proceso Reverse (Aprendido)

La red `ε_θ` aprende a predecir el ruido añadido:

```
L_simple = E_{t, x_0, ε} [ || ε - ε_θ(x_t, t) ||² ]
```

¡Sí! El objetivo es simplemente **regresión L2 de el ruido**. Sin weighting complejo, sin annealing. La simplicidad es su belleza.

### Training como Predicción de Ruido

```
Paso 1: muestrear t ~ Uniform(1, T)
Paso 2: muestrear ε ~ N(0, I)
Paso 3: x_t = √(ᾱ_t) · x_0 + √(1-ᾱ_t) · ε
Paso 4: ε_pred = ε_θ(x_t, t)
Paso 5: loss = MSE(ε, ε_pred)
Paso 6: backprop + optimizar
```

---

## 3. Evolución Arquitectónica

| Modelo | Año | Innovación | Complejidad |
|--------|-----|-----------|-------------|
| **DDPM** | 2020 | Predicción de ruido + U-Net | Base |
| **DDIM** | 2020 | Muestreo no-markoviano (10-50 pasos) | Inferencia rápida |
| **Stable Diffusion** | 2021 | Latent Diffusion (VAE + U-Net) | 8x más eficiente |
| **ADM** | 2021 | U-Net con attention + guidance | Calidad superior |
| **DALL-E 2** | 2022 | Prior diffusion + VQ-VAE | Texto → imagen |
| **SDXL** | 2023 | Two-stage (refiner + base) | Alta resolución |
| **DiT** | 2022 | U-Net → Transformer | Escalabilidad |
| **SD3** | 2024 | MMDiT (multi-modal DiT) | Texto nativo |
| **Flux** | 2024 | Flow Matching + DiT | Open-weight SOTA |
| **LCM** | 2023 | Consistency distillation | 4-8 pasos |

### DiT vs U-Net

**U-Net** (DDPM, SD): Convolutional encoder-decoder con skip connections y cross-attention. Funciona bien pero no escala linealmente con parámetros.

**DiT** (Diffusion Transformer): Reemplaza U-Net con un Transformer puro. Escala como GPT — más parámetros = mejor calidad de forma predecible. SD3 y Flux usan DiT.

---

## 4. Implementación desde Cero — DDPM

Aquí tienes una implementación completa y funcional de un Diffusion Model para series temporales:

```python
"""
Diffusion Model para Series Temporales — Implementación desde cero
===============================================================
Adaptado de Ho et al. (DDPM, 2020) y DiffusionTime (2023).
Funciona con PyTorch puro, sin dependencias externas.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import numpy as np


# ─── 1. Noise Scheduler ──────────────────────────────────────────────

class NoiseScheduler:
    """Schedule de ruido para el proceso de difusión."""
    
    def __init__(self, T=1000, beta_start=0.0001, beta_end=0.02, schedule="cosine"):
        self.T = T
        if schedule == "linear":
            self.betas = torch.linspace(beta_start, beta_end, T)
        elif schedule == "cosine":
            # Cosine schedule (proposed in DDPM appendix)
            steps = T + 1
            x = torch.linspace(0, T, steps)
            alphas_cumprod = torch.cos(((x / T) + 0.008) / 1.0864 * math.pi / 2) ** 2
            alphas_cumprod = alphas_cumprod / alphas_cumprod[0]
            self.betas = 1 - (alphas_cumprod[1:] / alphas_cumprod[:-1])
            self.betas = torch.clamp(self.betas, min=0.0001, max=0.02)
        else:
            raise ValueError(f"Unknown schedule: {schedule}")
        
        # Precompute alphas and cumulative products
        self.alphas = 1 - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0)
        self.alphas_cumprod_prev = F.pad(self.alphas_cumprod[:-1], (1, 0), value=1.0)
        
        # Precompute useful quantities for training
        self.sqrt_alphas_cumprod = torch.sqrt(self.alphas_cumprod)
        self.sqrt_one_minus_alphas_cumprod = torch.sqrt(1 - self.alphas_cumprod)
        self.log_one_minus_alphas_cumprod = torch.log(1 - self.alphas_cumprod)
        self.sqrt_recip_alphas_cumprod = torch.sqrt(1 / self.alphas_cumprod)
        self.sqrt_recipm1_alphas_cumprod = torch.sqrt(1 / self.alphas_cumprod - 1)
    
    def get_variance(self, t):
        return self.betas[t]
    
    def q_sample(self, x_start, t, noise=None):
        """Forward diffusion: x_t = √(ᾱ_t) · x_0 + √(1-ᾱ_t) · ε"""
        if noise is None:
            noise = torch.randn_like(x_start)
        
        # Extract coefficients for each timestep
        sqrt_alphas_cumprod_t = self.sqrt_alphas_cumprod[t][:, None, None]
        sqrt_one_minus_alphas_cumprod_t = self.sqrt_one_minus_alphas_cumprod[t][:, None, None]
        
        return sqrt_alphas_cumprod_t * x_start + sqrt_one_minus_alphas_cumprod_t * noise
    
    def q_mean(self, x_start, t):
        """Mean of q(x_t | x_0)"""
        return (self.sqrt_alphas_cumprod[t][:, None, None] * x_start)
    
    def q_posterior_mean_variance(self, x_start, x_t, t):
        """Compute posterior mean and variance: q(x_{t-1} | x_t, x_0)"""
        posterior_mean_coef1 = (
            self.betas[t][:, None] * torch.sqrt(self.alphas_cumprod_prev[t][:, None]) / (1.0 - self.alphas_cumprod[t][:, None])
        )
        posterior_mean_coef2 = (
            (1.0 - self.alphas_cumprod_prev[t][:, None]) * torch.sqrt(self.alphas[t][:, None]) / (1.0 - self.alphas_cumprod[t][:, None])
        )
        posterior_mean = posterior_mean_coef1 * x_start + posterior_mean_coef2 * x_t
        return posterior_mean, self.betas[t]


# ─── 2. Denoiser Network ────────────────────────────────────────────

class SinusoidalPositionEmbeddings(nn.Module):
    """Position embeddings con sinusoides (como en Transformers)."""
    
    def __step__(self, t, dim, temperature=10000):
        super().__init__()
        self.dim = dim
        
    def forward(self, t):
        device = t.device
        half_dim = self.dim // 2
        embeddings = math.log(10000) / (half_dim - 1)
        embeddings = torch.exp(torch.arange(half_dim, device=device) * -embeddings)
        embeddings = t[:, None] * embeddings[None, :]
        return torch.cat((embeddings.sin(), embeddings.cos()), dim=-1)


class TimeEmbedder(nn.Module):
    """Embedding del timestep t."""
    
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
        self.emb = SinusoidalPositionEmbeddings()
        self.fc = nn.Linear(dim, dim * 4)
        self.act = nn.SiLU()
        self.fc2 = nn.Linear(dim * 4, dim * 4)
    
    def forward(self, t):
        emb = self.emb(t)
        emb = self.act(self.fc(emb))
        emb = self.fc2(emb)
        return emb


class TemporalConvBlock(nn.Module):
    """Bloque convolucional temporal con residual connection."""
    
    def __init__(self, in_channels, out_channels, dropout=0.1):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size=3, padding=1)
        self.norm1 = nn.LayerNorm(out_channels)
        self.norm2 = nn.LayerNorm(out_channels)
        self.dropout = nn.Dropout(dropout)
        self.skip = nn.Conv1d(in_channels, out_channels, 1) if in_channels != out_channels else nn.Identity()
        self.act = nn.SiLU()
    
    def forward(self, x):
        residual = x
        x = self.norm1(x.transpose(1, 2))
        x = self.act(x)
        x = self.conv1(x)
        x = self.norm2(x.transpose(1, 2))
        x = self.act(x)
        x = self.dropout(x)
        x = self.conv2(x)
        return x + self.skip(residual.transpose(1, 2)).transpose(1, 2)


class ConditionalDenoiser(nn.Module):
    """
    Denoiser con condicionamiento exógeno.
    Input: (batch, seq_len, features)
    Output: (batch, seq_len, features) — predicción del ruido
    """
    
    def __init__(self, input_dim=1, hidden_dim=128, time_dim=64, 
                 num_cond_features=0, num_layers=4, dropout=0.1):
        super().__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.time_dim = time_dim
        
        # Proyección de entrada
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        
        # Embedding de tiempo
        self.time_mlp = TimeEmbedder(time_dim)
        self.time_proj = nn.Linear(time_dim, hidden_dim * 2)
        
        # Condicionamiento exógeno (clima, hora, etc.)
        if num_cond_features > 0:
            self.cond_proj = nn.Linear(num_cond_features, hidden_dim)
            self.use_conditioning = True
        else:
            self.use_conditioning = False
        
        # Bloques convolucionales temporales
        self.blocks = nn.ModuleList([
            TemporalConvBlock(hidden_dim, hidden_dim, dropout)
            for _ in range(num_layers)
        ])
        
        # Proyección de salida
        self.output_proj = nn.Linear(hidden_dim, input_dim)
        
        # LayerNorm inicial
        self.norm = nn.LayerNorm(hidden_dim)
    
    def forward(self, x_t, t, condition=None):
        """
        Args:
            x_t: (batch, seq_len, features) — serie temporal con ruido
            t: (batch,) — timesteps
            condition: (batch, num_cond_features) — datos exógenos (opcional)
        Returns:
            noise_pred: (batch, seq_len, features) — predicción del ruido
        """
        # Proyectar entrada
        x = self.input_proj(x_t)
        
        # Embedding de tiempo
        time_emb = self.time_mlp(t)
        time_emb = self.time_proj(time_emb).unsqueeze(1)  # (batch, 1, hidden*2)
        
        # Split en scale y shift (como en AdaLN)
        time_scale, time_shift = time_emb.chunk(2, dim=-1)
        
        # Aplicar AdaLN a cada bloque
        for i, block in enumerate(self.blocks):
            # AdaLN modulation
            x = x * (1 + time_scale) + time_shift
            
            # Conditioning injection
            if self.use_conditioning and condition is not None:
                cond_emb = self.cond_proj(condition).unsqueeze(1)  # (batch, 1, hidden)
                x = x + cond_emb
            
            x = self.norm(x)
            x = self.blocks[i](x)
        
        # Salida
        output = self.output_proj(x)
        return output


# ─── 3. Diffusion Model Principal ───────────────────────────────────

class DiffusionModel(nn.Module):
    """Modelo de difusión completo para series temporales."""
    
    def __init__(self, input_dim=1, hidden_dim=128, time_dim=64,
                 num_cond_features=0, num_layers=4, T=1000, schedule="cosine",
                 dropout=0.1):
        super().__init__()
        
        self.scheduler = NoiseScheduler(T=T, schedule=schedule)
        self.denoiser = ConditionalDenoiser(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            time_dim=time_dim,
            num_cond_features=num_cond_features,
            num_layers=num_layers,
            dropout=dropout
        )
        self.T = T
    
    def forward(self, x_start, condition=None):
        """
        Training forward pass.
        Args:
            x_start: (batch, seq_len, features) — datos originales
            condition: (batch, num_cond_features) — condicionamiento exógeno
        Returns:
            loss: scalar — MSE entre ruido real y predicho
        """
        batch_size = x_start.size(0)
        # Muestrear timestep uniformemente
        t = torch.randint(0, self.T, (batch_size,), device=x_start.device)
        # Muestrear ruido
        noise = torch.randn_like(x_start)
        # Aplicar difusión
        x_noisy = self.scheduler.q_sample(x_start, t, noise)
        # Predicción de ruido
        noise_pred = self.denoiser(x_noisy, t, condition)
        # Loss
        loss = F.mse_loss(noise_pred, noise)
        return loss
    
    @torch.no_grad()
    def sample(self, shape, condition=None, num_steps=None, guidance_scale=1.5):
        """
        Generar muestras mediante denoising iterativo (DDIM-style).
        Args:
            shape: (batch, seq_len, features)
            condition: (batch, num_cond_features)
            num_steps: número de pasos de sampling (None = T completo)
            guidance_scale: classifier-free guidance strength
        Returns:
            samples: (batch, seq_len, features)
        """
        if num_steps is None:
            num_steps = self.T
        
        # Usar subconjunto de timesteps para sampling rápido
        timesteps = self._ddim_timesteps(num_steps)
        
        batch_size = shape[0]
        device = shape[0] if isinstance(shape, torch.Tensor) else shape[0]
        device = next(self.parameters()).device
        
        # Iniciar desde ruido puro
        x = torch.randn(shape, device=device)
        
        # Sliding scale para DDIM
        alphas = self.scheduler.alphas
        total_steps = len(timesteps)
        
        for i, t in enumerate(timesteps):
            t_tensor = torch.full((batch_size,), t, device=device, dtype=torch.long)
            
            # Predicción de ruido
            noise_pred = self.denoiser(x, t_tensor, condition)
            
            # Extraer coeficientes
            alpha_t = alphas[t]
            alpha_prev_t = alphas[max(t - 1, 0)] if t > 0 else torch.tensor(0.0, device=device)
            
            # Deterministic sampling (DDIM)
            # x_{t-1} = √(α_{t-1}) · (x_t - √(1-α_t) · ε_θ) / √(α_t) + √(1-α_{t-1} - σ²) · ε_θ
            # Con σ = 0 → deterministic
            
            pred_original = (x - torch.sqrt(1 - alpha_t) * noise_pred) / torch.sqrt(alpha_t)
            pred_original = torch.clamp(pred_original, -5, 5)  # Clip para estabilidad
            
            direction = torch.sqrt(1 - alpha_prev_t) * noise_pred
            x = torch.sqrt(alpha_prev_t) * pred_original + direction
            
            # Opcional: classifier-free guidance
            if guidance_scale > 1.0 and condition is not None:
                noise_uncond = self.denoiser(x, t_tensor, None)
                noise_pred = noise_uncond + guidance_scale * (noise_pred - noise_uncond)
        
        return x
    
    def _ddim_timesteps(self, num_steps):
        """Seleccionar timesteps equidistantes para DDIM sampling."""
        jump = self.T // num_steps
        timesteps = [self.T - 1]
        for i in range(num_steps - 1):
            t = self.T - 1 - (i + 1) * jump
            timesteps.append(max(t, 0))
        return timesteps
    
    @torch.no_grad()
    def generate_multiple_samples(self, shape, n_samples=5, condition=None):
        """Generar múltiples muestras para estimar incertidumbre."""
        samples = torch.stack([
            self.sample(shape, condition) for _ in range(n_samples)
        ])
        # Estadísticas: mediana, percentiles 5/95
        median = torch.median(samples, dim=0).values
        p5 = torch.quantile(samples, 0.05, dim=0)
        p95 = torch.quantile(samples, 0.95, dim=0)
        return median, p5, p95, samples


# ─── 4. Ejemplo de Uso ──────────────────────────────────────────────

def demo():
    """Demostración completa con datos sintéticos de demanda eléctrica."""
    
    print("=" * 60)
    print("Diffusion Model para Series Temporales — Demo")
    print("=" * 60)
    
    # Config
    batch_size = 32
    seq_len = 168  # 1 semana a hora
    features = 1   # demanda
    cond_features = 3  # hora_día, día_semana, temperatura
    hidden_dim = 64
    T = 200  # pasos de difusión (reducido para demo)
    
    # Crear modelo
    model = DiffusionModel(
        input_dim=features,
        hidden_dim=hidden_dim,
        time_dim=32,
        num_cond_features=cond_features,
        num_layers=3,
        T=T,
        schedule="cosine"
    )
    
    print(f"Parámetros del modelo: {sum(p.numel() for p in model.parameters()):,}")
    
    # Generar datos sintéticos (demanda con patrones diarios/semanales)
    def generate_synthetic_demand(batch, seq_len=168):
        t = torch.arange(seq_len).float()
        # Patrón diario: pico mañana + pico noche
        daily = 50 + 30 * torch.sin(2 * torch.pi * t / 24) + \
                15 * torch.sin(2 * torch.pi * t / 12)
        # Patrón semanal: menor fines de semana
        day_of_week = (t / 24) % 7
        weekly = torch.where(day_of_week < 5, 0, -10)
        # Tendencia + ruido
        trend = 0.01 * t
        noise = torch.randn(batch, seq_len, features) * 2
        demand = (daily.unsqueeze(0) + weekly.unsqueeze(0) + trend.unsqueeze(0) + noise).clamp(0, None)
        return demand
    
    # Datos de entrenamiento
    x_train = generate_synthetic_demand(batch_size, seq_len)
    # Condiciones: hora, día_semana, temperatura (simulada)
    cond_train = torch.rand(batch_size, cond_features)
    
    # Entrenamiento
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler_lr = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_epochs=50)
    
    print(f"\nEntrenando {50} épocas...")
    for epoch in range(50):
        model.train()
        optimizer.zero_grad()
        
        # Batch aleatorio
        idx = torch.randint(0, batch_size, (batch_size,))
        x_batch = x_train[idx]
        c_batch = cond_train[idx]
        
        loss = model(x_batch, c_batch)
        loss.backward()
        optimizer.step()
        scheduler_lr.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1:3d}/50 — Loss: {loss.item():.4f} — LR: {scheduler_lr.get_last_lr()[0]:.6f}")
    
    # Generar muestras
    print("\nGenerando muestras...")
    model.eval()
    
    # Muestra única
    sample_shape = (1, seq_len, features)
    sample = model.sample(sample_shape, condition=cond_train[:1])
    print(f"Muestra generada: shape={sample.shape}, range=[{sample.min():.2f}, {sample.max():.2f}]")
    
    # Múltiples muestras (estimación de incertidumbre)
    median, p5, p95, all_samples = model.generate_multiple_samples(
        sample_shape, n_samples=10, condition=cond_train[:1]
    )
    print(f"Incertidumbre: [p5={p5[0,0]:.2f}, mediana={median[0,0]:.2f}, p95={p95[0,0]:.2f}]")
    
    print("\n✅ Demo completada con éxito")
    return model


if __name__ == "__main__":
    demo()
```

---

## 5. Implementación con Hugging Face Diffusers

Para un enfoque más práctico y rápido:

```python
"""
Diffusion con Hugging Face Diffusers — Enfoque práctico
======================================================
"""

from diffusers import DDPMScheduler, DDIMScheduler, UNet2DModel
from diffusers.training_utils import EMAModel
import torch
import torch.nn as nn

# ─── 1. Configurar el Noise Scheduler ───

# DDPMScheduler: muestreo markoviano (50-1000 pasos)
scheduler = DDPMScheduler(
    num_train_timesteps=1000,
    beta_schedule="scaled_linear",  # linear, cosine, squaredcos_cap_v2
    prediction_type="epsilon",      # "epsilon", "v_prediction", "sample"
)

# DDIMScheduler: muestreo no-markoviano (10-50 pasos)
scheduler_fast = DDIMScheduler(
    num_train_timesteps=1000,
    beta_schedule="scaled_linear",
    prediction_type="epsilon",
    clip_sample=True,               # Clip predicciones para estabilidad
)

# ─── 2. Adaptar UNet para Series Temporales ───

class TemporalUNet(nn.Module):
    """
    U-Net adaptado para series temporales 1D.
    Reemplaza el UNet2DModel estándar con convoluciones 1D.
    """
    
    def __init__(self, in_channels=1, out_channels=1, 
                 down_channels=(64, 128, 256),
                 attention_heads=4, time_embed_dim=128):
        super().__init__()
        
        self.time_proj = SinusPositionEmbeddings(time_embed_dim)
        
        # Encoder (downsampling)
        self.time_embedding = nn.Sequential(
            nn.Linear(time_embed_dim, time_embed_dim * 4),
            nn.SiLU(),
            nn.Linear(time_embed_dim * 4, time_embed_dim)
        )
        
        # Proyección de entrada
        self.input_conv = nn.Conv1d(in_channels, down_channels[0], kernel_size=7, padding=3)
        
        # Bloques de down
        self.down_blocks = nn.ModuleList()
        ch = down_channels[0]
        for next_ch in down_channels[1:]:
            self.down_blocks.append(nn.Sequential(
                nn.Conv1d(ch, ch, kernel_size=3, padding=1),
                nn.GroupNorm(8, ch),
                nn.SiLU(),
                nn.Conv1d(ch, next_ch, kernel_size=3, padding=1),
                nn.GroupNorm(8, next_ch),
                nn.SiLU(),
                nn.Conv1d(next_ch, next_ch, kernel_size=3, padding=1, stride=2),
                nn.GroupNorm(8, next_ch),
                nn.SiLU(),
            ))
            ch = next_ch
        
        # Middle block
        self.middle = nn.Sequential(
            nn.Conv1d(ch, ch, kernel_size=3, padding=1),
            nn.GroupNorm(8, ch),
            nn.SiLU(),
            nn.Conv1d(ch, ch, kernel_size=3, padding=1),
            nn.GroupNorm(8, ch),
            nn.SiLU(),
        )
        
        # Decoder (upsampling)
        self.up_blocks = nn.ModuleList()
        for prev_ch in reversed(down_channels[1:]):
            self.up_blocks.append(nn.Sequential(
                nn.Conv1d(ch * 2, ch, kernel_size=3, padding=1),  # concat skip
                nn.GroupNorm(8, ch),
                nn.SiLU(),
                nn.Conv1d(ch, ch, kernel_size=3, padding=1),
                nn.GroupNorm(8, ch),
                nn.SiLU(),
                nn.Conv1d(ch, prev_ch, kernel_size=3, padding=1, stride=2),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.GroupNorm(8, prev_ch),
                nn.SiLU(),
            ))
            ch = prev_ch
        
        # Salida
        self.output_conv = nn.Sequential(
            nn.Conv1d(ch, out_channels, kernel_size=3, padding=1),
        )
    
    def forward(self, x, t):
        # Embedding de tiempo
        t_emb = self.time_proj(t)
        t_emb = self.time_embedding(t_emb)
        t_emb = t_emb.unsqueeze(-1)  # (batch, dim, 1)
        
        # Encoder
        h = self.input_conv(x)
        skips = [h]
        for block in self.down_blocks:
            h = block(h)
            skips.append(h)
        
        # Middle
        h = self.middle(h)
        
        # Decoder con skip connections
        for i, block in enumerate(reversed(self.up_blocks)):
            h = torch.cat([h, skips[-(i+2)]], dim=1)  # skip connection
            h = block(h)
        
        return self.output_conv(h)


# ─── 3. Entrenamiento ───

def train_diffusion(model, dataloader, num_epochs=100):
    """Entrenamiento de un modelo de difusión."""
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-4, weight_decay=1e-2)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)
    criterion = nn.MSELoss()
    
    model.train()
    for epoch in range(num_epochs):
        total_loss = 0
        for batch in dataloader:
            x_start = batch  # (batch, seq_len, features)
            x_start = x_start.permute(0, 2, 1)  # (batch, features, seq_len)
            
            # Muestrear timestep y ruido
            t = torch.randint(0, 1000, (x_start.size(0),), device=x_start.device)
            noise = torch.randn_like(x_start)
            
            # Aplicar difusión
            x_noisy = scheduler.add_noise(x_start, noise, t)
            
            # Predicción
            noise_pred = model(x_noisy, t)
            
            # Loss
            loss = criterion(noise_pred, noise)
            
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            total_loss += loss.item()
        
        scheduler.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{num_epochs} — Loss: {total_loss/len(dataloader):.4f}")

# ─── 4. Inference con Guidance ───

def sample_with_guidance(model, shape, condition=None, guidance_scale=3.0):
    """
    Sampling con classifier-free guidance.
    guidance_scale > 1 → más fiel al condicionamiento
    guidance_scale = 1 → sin guidance
    guidance_scale < 1 → más variado/creativo
    """
    scheduler_fast = DDIMScheduler.from_config(scheduler.config)
    scheduler_fast.set_timesteps(20)  # Solo 20 pasos
    
    x = torch.randn(shape)
    
    for t in scheduler_fast.timesteps:
        t_batch = torch.full((shape[0],), t, device=x.device)
        
        # Predicción condicional
        noise_cond = model(x, t_batch)
        
        # Predicción incondicional
        if condition is not None:
            noise_uncond = model(x, t_batch)  # condition=None implícito
        else:
            noise_uncond = noise_cond
        
        # Guidance
        noise_pred = noise_uncond + guidance_scale * (noise_cond - noise_uncond)
        
        # Paso DDIM
        x = scheduler_fast.step(noise_pred, t, x).prev_sample
    
    return x
```

---

## 6. Aplicaciones al Stack ESIOS/REE

### 6.1 Forecasting de Demanda con Incertidumbre

Los DM son ideales para la demanda eléctrica porque:

1. **Capturan multimodalidad:** Hay escenarios distintos (día laborable vs festivo, ola de calor vs normal). Los DM aprenden todas las modas.
2. **Intervalos calibrados:** Las predicciones de percentiles (p5, p50, p95) están bien calibradas, crucial para gestión de riesgo.
3. **Condiciones exógenas naturales:** Temperatura, irradiación, tipo de día se inyectan como conditioning sin cambiar la arquitectura.

```python
"""
Pipeline de forecasting de demanda con Diffusion Model
======================================================
"""

class DemandForecaster:
    """
    Forecasting de demanda eléctrica con Diffusion Model.
    Input: historial de demanda + datos meteorológicos
    Output: distribución de demanda futura (mediana + intervalos)
    """
    
    def __init__(self, seq_len_history=336, seq_len_future=168, 
                 weather_features=5, hidden_dim=128):
        self.model = DiffusionModel(
            input_dim=1,                    # demanda
            hidden_dim=hidden_dim,
            time_dim=32,
            num_cond_features=weather_features + 2,  # weather + hora + día
            num_layers=4,
            T=200,
            schedule="cosine"
        )
        self.seq_len_history = seq_len_history
        self.seq_len_future = seq_len_future
        self.scaler = StandardScaler()
    
    def create_sequences(self, demand, weather, target_start):
        """
        Crear secuencias de entrenamiento.
        
        Args:
            demand: (T,) — demanda histórica
            weather: (T, N) — datos meteorológicos
            target_start: número de pasos adelante a predecir
        Returns:
            x: (batch, seq_len_history, 1) — demanda histórica
            cond: (batch, N+2) — condiciones para el futuro
            y: (batch, seq_len_future, 1) — demanda objetivo
        """
        # Normalizar
        demand_norm = self.scaler.transform(demand.reshape(-1, 1)).flatten()
        
        # Ventana de historia
        x = demand_norm[target_start-self.seq_len_history:target_start]
        x = x.reshape(1, -1, 1)
        
        # Condiciones: promedio meteorológico futuro + hora pico + tipo día
        future_weather = weather[target_start:target_start+self.seq_len_future]
        cond = np.concatenate([
            future_weather.mean(axis=0),           # media meteorológica
            [target_start % 24 / 24],              # hora del día
            [(target_start % 168) < 120]           # laborable (0-119h)
        ]).reshape(1, -1)
        
        # Objetivo
        y = demand_norm[target_start:target_start+self.seq_len_future]
        y = y.reshape(1, -1, 1)
        
        return x, cond, y
    
    def predict(self, demand_history, weather_future, n_samples=10):
        """
        Predicción con estimación de incertidumbre.
        
        Returns:
            median: predicción mediana
            p5, p95: intervalos de confianza
            samples: array de n_samples escenarios posibles
        """
        model = self.model
        model.eval()
        
        demand_history = torch.tensor(demand_history, dtype=torch.float32).unsqueeze(-1)
        weather_future = torch.tensor(weather_future, dtype=torch.float32)
        
        with torch.no_grad():
            median, p5, p95, samples = model.generate_multiple_samples(
                shape=(1, self.seq_len_future, 1),
                n_samples=n_samples,
                condition=weather_future.unsqueeze(0)
            )
        
        # Des-normalizar
        median = self.scaler.inverse_transform(median.squeeze().numpy())
        p5 = self.scaler.inverse_transform(p5.squeeze().numpy())
        p95 = self.scaler.inverse_transform(p95.squeeze().numpy())
        
        return median, p5, p95, samples
```

### 6.2 Generación de Escenarios Sintéticos para Renovables

```python
"""
Generación de escenarios de producción renovable
=================================================
Útil para: planificación de operación, gestión de riesgo, stress testing.
"""

class RenewableScenarioGenerator:
    """
    Genera escenarios sintéticos de producción eólica/solar.
    Entrenado con datos históricos de REE/ESIOS.
    """
    
    def __init__(self, source="wind"):
        """
        Args:
            source: "wind" (eólica) o "solar" (fotovoltaica)
        """
        self.model = DiffusionModel(
            input_dim=1,
            hidden_dim=64,
            num_layers=3,
            T=100,
        )
        self.source = source
        self.irradiance_features = 4  # para solar: DNI, DHI, etc.
        self.wind_features = 3        # para eólica: velocidad, dirección, turbulencia
    
    def train_from_esios(self, indicator_id, start_date, end_date):
        """
        Entrenar con datos de ESIOS/REE.
        
        Args:
            indicator_id: ID del indicador ESIOS (ej: "PRODNT" para producción térmica)
            start_date, end_date: rango de datos
        """
        # Fetch datos de ESIOS (usando la API existente)
        # ... código de fetch ESIOS ...
        
        # Normalizar y crear secuencias
        # ... preprocessing ...
        
        # Entrenar
        optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-3)
        for epoch in range(100):
            # ... training loop ...
            pass
    
    def generate_scenarios(self, n_scenarios=100, horizon=168):
        """
        Generar escenarios de producción.
        
        Returns:
            scenarios: (n_scenarios, horizon) — array de escenarios posibles
        """
        self.model.eval()
        with torch.no_grad():
            samples = self.model.sample(
                shape=(n_scenarios, horizon, 1),
                num_steps=50  # DDIM para velocidad
            )
        return samples.squeeze(-1).numpy()
    
    def compute_risk_metrics(self, scenarios, current_production):
        """
        Calcular métricas de riesgo a partir de escenarios.
        """
        # VaR (Value at Risk) al 95%
        var_95 = np.percentile(scenarios[:, -1], 5)  # peor 5%
        
        # CVaR (Conditional VaR)
        cvar_95 = scenarios[scenarios[:, -1] <= var_95, -1].mean()
        
        # Probabilidad de shortfall
        shortfall_prob = (scenarios[:, -1] < current_production * 0.8).mean()
        
        return {
            "var_95": var_95,
            "cvar_95": cvar_95,
            "shortfall_prob": shortfall_prob,
            "mean_production": scenarios.mean(),
            "std_production": scenarios.std(),
        }
```

---

## 7. Técnicas Avanzadas

### 7.1 Classifier-Free Guidance

Técnica más importante para controlar la generación:

```python
"""
Classifier-free guidance: guía la generación sin classifier externo.

En vez de entrenar un classifier p(y|x) separado, entrenamos UN SOLO modelo
que puede ser condicional O incondicional. En inference, combinamos ambas:

    ε_guided = ε_uncond + w · (ε_cond - ε_uncond)

Donde w = guidance_scale:
    w = 1.0  → sin guidance (comportamiento estándar)
    w > 1.0  → más fiel al condicionamiento (menos variado)
    w < 1.0  → más variado/creativo (menos fiel)
"""

# Durante training: a veces dropamos el conditioning (p_drop=0.1)
# Esto permite que el modelo aprenda a generar sin condiciones

# Durante inference:
def guided_denoise(model, x_t, t, condition, guidance_scale=3.0):
    # Predicción con condición
    noise_cond = model(x_t, t, condition=condition)
    # Predicción sin condición (condition=None)
    noise_uncond = model(x_t, t, condition=None)
    # Combinar
    noise = noise_uncond + guidance_scale * (noise_cond - noise_uncond)
    return noise
```

### 7.2 Latent Diffusion (SD-style)

Para datos de alta dimensión, difuminar en un espacio latente comprimido:

```
x (high-dim) → VAE encoder → z (low-dim latent) → Diffusion en z → VAE decoder → x'
```

Ventaja: la difusión opera en un espacio de dimensión mucho menor (8x más rápido).

### 7.3 Consistency Models / LCM

Distilar un diffusion model entrenado en pocos pasos:

```
Modelo teacher (100 pasos) → Consistency Distillation → Model student (1-4 pasos)
```

LCM (Latent Consistency Models): 4-8 pasos con calidad comparable a SD en 50 pasos.

### 7.4 Flow Matching

Alternativa a score matching (más estable):

```
En vez de predecir ruido ε, modelamos el flujo de probabilidad directo:
    v = dx/dt = flujo desde distribución de ruido a distribución de datos

Flow Matching (Lipman et al., 2023):
    - Objetivo más simple: predecir vector de velocidad
    - Más estable que score matching
    - Base de Stable Diffusion 3 y Flux
```

---

## 8. Comparativa: SSM (Mamba) vs Diffusion para el Stack

| Aspecto | SSM (Mamba) | Diffusion |
|---------|-------------|-----------|
| **Inference** | O(N) secuencial, muy rápido | Iterativo, lento (a menos que distillado) |
| **Incertidumbre** | Puntual (una predicción) | Distribución completa (multimodal) |
| **Condicionamiento** | Directo (input concatenado) | Flexible (cross-attention, CFG) |
| **Edge deployment** | ✅ Excelente | ⚠️ Requiere distillation |
| **Forecasting punto** | ✅ Bueno | ⚠️ Overkill |
| **Forecasting probabilístico** | ❌ Limitado | ✅ Excelente |
| **Generación de escenarios** | ❌ No | ✅ Nativo |
| **Anomalía detección** | ⚠️ Indirecto | ✅ Reconstrucción |

**Recomendación:** Usar SSM para forecasting puntual rápido + Diffusion para escenarios de riesgo y generación de datos sintéticos. Son complementarios.

---

## 9. Optimización para MicroVM (1vCPU/2GB)

```python
"""
Optimizaciones para deployment en recursos limitados.
"""

# 1. Quantización INT8 del denoiser
import torch.quantization as quantization

# Cuantizar el modelo después de entrenar
model.eval()
model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
quantized_model = quantization.prepare(model, inplace=False)
quantized_model = quantization.convert(quantized_model, inplace=False)

# 2. torch.compile (PyTorch 2.0+)
compiled_model = torch.compile(model, backend='eager')  # 'eager' para CPU

# 3. Distillation a 4 pasos
# Entrenar un consistency model que mapea ruido → datos en 4 pasos
# Reduce inference de 1000 pasos a 4

# 4. Modelos pequeños
# hidden_dim=64, num_layers=3 → ~500K parámetros
# Aproximadamente 2MB en FP32, 0.5MB en INT8

# 5. Onnx export para inferencia sin PyTorch
import onnx
onnx.export(
    model,
    (torch.randn(1, 168, 1), torch.randint(0, 1000, (1,))),
    "diffusion_model.onnx",
    input_names=["x_t", "t"],
    output_names=["noise_pred"]
)
```

---

## 10. Papers de Referencia

### Fundamentales
| Paper | Autores | ArXiv | Año |
|-------|---------|-------|-----|
| DDPM | Ho et al. | 2006.11239 | 2020 |
| DDIM | Song et al. | 2010.02502 | 2020 |
| Stable Diffusion | Rombach et al. | 2112.10752 | 2021 |
| ADM | Dhariwal & Nichol | 2105.05233 | 2021 |
| DiT | Pezeshki et al. | 2212.09748 | 2022 |
| SDXL | Podell et al. | 2307.01952 | 2023 |
| Consistency Models | Song et al. | 2303.11216 | 2023 |
| LCM | Lu et al. | 2310.04378 | 2023 |
| SD3 | Esser et al. | 2403.03206 | 2024 |
| Flux | Black Forest Labs | 2410.25781 | 2024 |

### Para Series Temporales
| Paper | Autores | ArXiv | Año |
|-------|---------|-------|-----|
| DiffusionTime | Wang et al. | 2302.04548 | 2023 |
| TSDiff | Kim et al. | 2303.08313 | 2023 |
| Diffusion-FF | Zeng et al. | 2305.12319 | 2023 |
| Diffusion-Prob | Han et al. | 2401.08688 | 2024 |

### Flow Matching
| Paper | Autores | ArXiv | Año |
|-------|---------|-------|-----|
| Flow Matching | Lipman et al. | 2302.03686 | 2023 |
| Rectified Flow | Liu et al. | 2209.03003 | 2022 |

---

## 11. Repositorios GitHub

| Repo | URL | Descripción |
|------|-----|-------------|
| **diffusers** | https://github.com/huggingface/diffusers | Biblioteca principal de Hugging Face |
| **hojonathanho/diffusion** | https://github.com/hojonathanho/diffusion | DDPM original |
| **ermongroup/ddim** | https://github.com/ermongroup/ddim | DDIM implementation |
| **CompVis/stable-diffusion** | https://github.com/CompVis/stable-diffusion | SD original |
| **stability-ai/stable-diffusion** | https://github.com/Stability-AI/stablediffusion | SD codebase |
| **black-forest-labs/flux** | https://github.com/black-forest-labs/flux | Flux implementation |
| **Dao-AILab/diffusion-time** | https://github.com/Dao-AILab/diffusion-time | DiffusionTime para TS |
| **thuml/Time-Series-Library** | https://github.com/thuml/Time-Series-Library | TS library con SSM + Diffusion |

---

## 12. Próximos Temas Sugeridos

1. **Graph Neural Networks (GNN)** — Modelado de redes eléctricas como grafos, detección de fallos, flujo de potencia. Directamente aplicable a la red de transporte eléctrico.

2. **LoRA / PEFT** — Fine-tuning eficiente de modelos grandes. Perfecto para el stack de MicroVM (1vCPU/2GB): fine-tuna un LLM pequeño con LoRA para forecasting.

3. **Transformers Architecture Deep-Dive** — FlashAttention, RoPE, MoE. Profundizar en la arquitectura que domina el campo actual.

**Mi recomendación:** GNNs — es el siguiente paso lógico después de SSM y Diffusion, y tiene aplicaciones directas a la red eléctrica.

---

## 13. Notas Prácticas

- **Stability tricks:**
  - Usar `clip_grad_norm_` para evitar gradientes explosivos
  - Weight decay de 1e-4 a 1e-2 según el tamaño del modelo
  - Learning rate warmup de 1000 steps al inicio
  - Cosine annealing para el scheduler
  - EMA (Exponential Moving Average) del modelo para inference estable

- **Evaluation metrics:**
  - MSE/MAE para predicción puntual
  - CRPS (Continuous Ranked Probability Score) para distribución
  - Coverage de intervalos de confianza
  - Calibración: los percentiles predichos deben coincidir con frecuencia observada

- **Data requirements:**
  - Mínimo 1000 secuencias de entrenamiento para resultados decentes
  - Normalización Z-score por serie
  - Data augmentation: jitter, time warping, magnitude warping

---

*Hecho con (L) por David Antizar*
