# Diffusion Transformers (DiT) — De U-Net a Transformers Puros para Generación

## Fecha: 2026-07-02

---

## 1. Contexto: ¿Por qué DiT?

Los modelos de difusión para generación de imágenes se basaron durante años en **U-Nets con atención** (DDPM, Stable Diffusion). La U-Net es excelente para imágenes, pero tiene limitaciones de escalabilidad:

1. **Atención 2D limitada**: La atención en U-Net opera en espacios 2D, no escala bien a resoluciones muy altas.
2. **Arquitectura fija**: La U-Net tiene una estructura encoder-decoder fija con skip connections.
3. **Escalado no lineal**: Al crecer el modelo, la U-Net no escala tan bien como los transformers puros.

El paper **"Scalable Diffusion Models with Transformers"** (Dhariwal & Nichol, 2023) demostró que **reemplazar la U-Net por un transformer puro** (el DiT) produce:
- Mejor calidad (FID más bajo) a igual compute
- Escalado más predecible y lineal con el tamaño del modelo
- Arquitectura más simple y uniforme

> **Idea central**: Tratar patches de imagen como tokens de texto. Un transformer sobre patches de imagen es más escalable que una U-Net.

---

## 2. Arquitectura DiT — Anatomía

### 2.1. Patch Embedding

```
Imagen RGB (H×W×3)
    ↓
Patchify (patch_size=2×2)
    ↓
Tokens: (B, N, C)  donde N = (H/2)×(W/2), C = 3×2×2 = 12
    ↓
Linear Projection → (B, N, D)  donde D = dim_model
```

A diferencia de los LLMs que usan tokenización discreta (BPE), DiT usa **patch embeddings continuos**. Cada patch se proyecta linealmente a un vector de dimensión D.

### 2.2. Transformer Blocks

Cada bloque DiT contiene:
- **Self-Attention** (full attention sobre patches)
- **MLP** (GELU, como en ViT)
- **LayerNorm** (post-norm o pre-norm)
- **Cross-Attention** (condicionado por texto/clase)
- **AdaLN** (Adaptive Layer Normalization con timestep embedding)

### 2.3. Timestep Embedding — El corazón del diffusion

```python
import torch
import torch.nn as nn
import math

class TimestepEmbedder(nn.Module):
    """
    Embede escalar de timestep (t) a vector de dimensión D
    usando sinusoides + proyección MLP.
    """
    def __init__(self, dim: int, half_dim: int = 256):
        super().__init__()
        self.dim = dim
        self.half_dim = half_dim
        self.mlp = nn.Sequential(
            nn.Linear(half_dim, dim),
            nn.SiLU(),
            nn.Linear(dim, dim),
        )

    def forward(self, t: torch.Tensor):
        # t shape: (B,)
        half_dim = self.half_dim
        emb = math.log(10000) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim, device=t.device) * -emb)
        emb = t.float().unsqueeze(1) * emb.unsqueeze(0)
        emb = self.mlp(emb)
        return emb
```

### 2.4. AdaLN-Zero (Adaptive Layer Normalization con shift/scale/gate)

```python
class AdaLNZero(nn.Module):
    """
    Adaptive Layer Normalization con zero initialization.
    Genera 6 escalas (shift, scale para x, gate para attn)
    que modulan la capa según el timestep embedding.
    """
    def __init__(self, dim: int):
        super().__init__()
        self.silu = nn.SiLU()
        self.linear = nn.Linear(dim, dim * 6)  # 6 proyecciones
        self.norm = nn.LayerNorm(dim, elementwise_affine=False)

        # Zero initialization: al inicio, shift=0, scale=0, gate=0
        nn.init.zeros_(self.linear.weight)
        nn.init.zeros_(self.linear.bias)

    def forward(self, x: torch.Tensor, emb: torch.Tensor) -> tuple:
        """
        x: (B, N, D)  — features
        emb: (B, D)   — timestep + class embedding
        Returns: 6 tensors modulados
        """
        emb = self.linear(self.silu(emb))[:, None, :]  # (B, 1, D)
        shift_msa, scale_msa, gate_msa, shift_mlp, scale_mlp, gate_mlp = emb.chunk(6, dim=2)

        # Modulación de la entrada
        x = self.norm(x) * (1 + scale_msa) + shift_msa
        return x, gate_msa, shift_mlp, scale_mlp, gate_mlp
```

### 2.5. Bloque DiT Completo

```python
class DiTBlock(nn.Module):
    """Un bloque transformer con cross-attention y AdaLN."""
    def __init__(self, dim: int, n_heads: int, mlp_ratio: float = 4.0):
        super().__init__()
        self.dim = dim
        self.n_heads = n_heads
        head_dim = dim // n_heads

        # AdaLN
        self.adaln = AdaLNZero(dim)

        # Self-attention
        self.attn = nn.MultiheadAttention(
            dim, n_heads, batch_first=True,
            kdim=dim, vdim=dim
        )

        # Cross-attention (para conditioning)
        self.cross_attn = nn.MultiheadAttention(
            dim, n_heads, batch_first=True
        )

        # MLP
        mlp_dim = int(dim * mlp_ratio)
        self.mlp = nn.Sequential(
            nn.Linear(dim, mlp_dim),
            nn.GELU(approximate='tanh'),
            nn.Linear(mlp_dim, dim),
        )

        # Gate post-MLP
        self.gate_post = nn.Parameter(torch.zeros(dim))

    def forward(
        self,
        x: torch.Tensor,           # (B, N, D) visual tokens
        cond: torch.Tensor,         # (B, L, D) conditioning (texto)
        emb: torch.Tensor,          # (B, D) timestep embedding
    ) -> torch.Tensor:
        # AdaLN modulation
        x, gate_msa, shift_mlp, scale_mlp, gate_mlp = self.adaln(x, emb)

        # Self-attention con gate
        attn_out, _ = self.attn(x, x, x)
        attn_out = gate_msa * attn_out
        x = x + attn_out

        # Cross-attention (condicionado)
        x = x + self.cross_attn(x, cond, cond)[0]

        # MLP con modulación
        h = self.mlp(x) * (1 + scale_mlp) + shift_mlp
        h = gate_mlp * h
        x = x + h

        return x
```

---

## 3. El Pipeline de Difusión con DiT

```
1. Forward diffusion (Q):
   q(x_t | x_{t-1}) = N(x_t; √(1-β_t)·x_{t-1}, β_t·I)

2. Model training (predicción de ruido):
   ε_θ(x_t, t) = DiT(x_t, t, c)
   donde:
     - x_t: imagen ruidosa en timestep t
     - t: timestep (escalar → embedding)
     - c: conditioning (texto, clase, etc.)
     - ε: ruido añadido

3. Loss:
   L = E_{t, x_0, ε} [‖ε - ε_θ(x_t, t, c)‖²]

4. Sampling (DPM-Solver, DDIM, Euler):
   x_{t-1} = x_t - α_t·ε_θ(x_t, t, c) + σ_t·z
```

### 3.1. Entrenamiento Completo (simplificado)

```python
class DiT(nn.Module):
    """
    Diffusion Transformer completo.
    Reemplaza la U-Net en Stable Diffusion.
    """
    def __init__(
        self,
        image_size: int = 32,
        patch_size: int = 2,
        in_channels: int = 4,      # Latent space (SD) o 3 (RGB)
        dim: int = 1024,
        n_heads: int = 16,
        n_blocks: int = 20,
        cond_dim: int = 512,       # conditioning dimension
        cond_token_len: int = 77,  # tokens de texto (CLIP)
    ):
        super().__init__()
        self.patch_size = patch_size
        self.n_patches = (image_size // patch_size) ** 2
        self.in_channels = in_channels

        # Proyección de patches
        self.x_embedder = nn.Linear(
            in_channels * patch_size ** 2, dim
        )

        # Timestep embedding
        self.t_embedder = TimestepEmbedder(dim)

        # Class embedding (opcional, para imagenet)
        self.y_embedder = nn.Embedding(1000, dim)

        # Transformer blocks
        self.blocks = nn.ModuleList([
            DiTBlock(dim, n_heads)
            for _ in range(n_blocks)
        ])

        # Final projection
        self.norm = nn.LayerNorm(dim, elementwise_affine=False)
        self.proj = nn.Linear(dim, patch_size ** 2 * in_channels)

        # Cross-attention conditioning projection
        self.cond_proj = nn.Linear(cond_dim, dim)

    def forward(
        self,
        x: torch.Tensor,      # (B, C, H, W) — latents o imagen
        t: torch.Tensor,       # (B,) — timesteps
        cond: torch.Tensor,    # (B, L, D_cond) — conditioning
    ) -> torch.Tensor:
        B, C, H, W = x.shape
        N = H // self.patch_size
        M = W // self.patch_size

        # Patchify: (B, C, H, W) → (B, N*M, C*P*P)
        x = self.x_embedder(
            x.unfold(1, self.patch_size, self.patch_size)
             .unfold(2, self.patch_size, self.patch_size)
             .reshape(B, N * M, -1)
        )

        # Timestep embedding
        emb = self.t_embedder(t)

        # Conditioning projection
        cond = self.cond_proj(cond)

        # Transformer blocks
        for block in self.blocks:
            x = block(x, cond, emb)

        # Final projection
        x = self.norm(x)
        x = self.proj(x)  # (B, N*M, C*P*P)

        # Unpatchify: (B, N*M, C*P*P) → (B, C, H, W)
        x = x.reshape(B, N, M, C, self.patch_size, self.patch_size)
        x = x.permute(0, 3, 1, 4, 2, 5).reshape(B, C, H, W)

        return x
```

---

## 4. DiT vs U-Net: Comparación Directa

| Aspecto | U-Net (SD) | DiT |
|---------|-----------|-----|
| **Arquitectura** | Encoder-decoder con skip connections | Transformer puro |
| **Atención** | Local / self-attention en features | Full attention sobre patches |
| **Escalado** | No lineal, difícil de escalar | Lineal, predecible |
| **Tokens** | Features espaciales | Patches como tokens |
| **Parámetros** | Más por skip connections | Más eficiente en parámetros |
| **Calidad/FID** | Buena | Mejor a igual compute |
| **Inferencia** | Optimizada (cuantización madura) | Menos optimizada |
| **Ventaja clave** | Madurez, herramientas | Escalabilidad, simplicidad |

---

## 5. Aplicaciones Más Allá de Imágenes

### 5.1. DiT para Video

- **Video DiT**: Extiende patches a 3D (spatial + temporal)
- **TimeSformer + Diffusion**: Patches temporales como tokens extra
- **Sora-style**: Tokens de video → patches 3D → transformer diffusion

### 5.2. DiT para Series Temporales

Esto es **muy relevante** para nuestro stack (ESIOS, energía, forecasting):

- **Time-Series-DiT**: Tratar puntos temporales como patches
- **Forecasting como generación**: En vez de predecir un valor, generar una distribución completa
- **Probabilistic forecasting**: La naturaleza probabilística del diffusion es ideal para intervalos de predicción

```python
class TimeSeriesDiT(nn.Module):
    """
    DiT adaptado para series temporales multivariante.
    - Input: (B, T, F) — batch, tiempo, features
    - Output: distribución sobre valores futuros
    """
    def __init__(
        self,
        seq_len: int = 96,
        pred_len: int = 24,
        n_features: int = 7,  # precio, demanda, etc.
        dim: int = 512,
        n_heads: int = 8,
        n_blocks: int = 12,
    ):
        super().__init__()
        self.seq_len = seq_len
        self.pred_len = pred_len

        # Proyección de features a dim
        self.input_proj = nn.Linear(n_features, dim)

        # Timestep embedding para diffusion steps
        self.t_embedder = TimestepEmbedder(dim)

        # Positional encoding temporal
        self.pos_encoder = nn.Parameter(
            torch.randn(1, seq_len + pred_len, dim) * 0.02
        )

        # Transformer blocks
        self.blocks = nn.ModuleList([
            DiTBlock(dim, n_heads) for _ in range(n_blocks)
        ])

        self.norm = nn.LayerNorm(dim)
        self.output_proj = nn.Linear(dim, n_features)

    def forward(
        self,
        x: torch.Tensor,    # (B, seq_len + pred_len, n_features)
        t: torch.Tensor,     # (B,) — diffusion timestep
    ) -> torch.Tensor:
        B = x.shape[0]

        # Proyectar features
        x = self.input_proj(x)

        # Añadir positional encoding
        x = x + self.pos_encoder[:, :x.shape[1], :]

        # Timestep embedding
        emb = self.t_embedder(t)

        # Transformer blocks (sin cross-attn para forecasting no condicional)
        for block in self.blocks:
            x = block(x, x, emb)  # self-conditioning

        x = self.norm(x)
        return self.output_proj(x)
```

### 5.3. DiT para Audio

- **AudioLDM 2**: DiT para generación de audio a partir de texto
- **MAGNeT**: Modelado autoregresivo de espectrogramas con DiT
- **MusicGen**: Generación musical con transformers + diffusion

---

## 6. Optimizaciones Recientes (2024-2026)

Basado en los papers encontrados en arXiv:

### 6.1. DyDiT — Dynamic Diffusion Transformer (Oct 2024)
- **Problema**: Computación redundante en timesteps y regiones espaciales
- **Solución**: Timestep-wise Dynamic Width (TDW) + Spatial-wise Dynamic Token (SDT)
- **Resultado**: 51% menos FLOPs en DiT-XL, 1.73x más rápido, FID=2.07 en ImageNet
- **Repo**: `NUS-HPC-AI-Lab/Dynamic-Diffusion-Transformer`

### 6.2. PiT — Progressive Diffusion Transformer (May 2025)
- **Problema**: Transformers isotrópicos con costo cuadrático
- **Solución**: Arquitectura progresiva — early layers con atención local, late layers con atención global
- **Analogía**: Similar a cómo los LLMs usan sliding window attention

### 6.3. Post-Training Quantization for DiT (Mar 2025)
- **Problema**: DiT es grande y costoso para inferencia
- **Solución**: Agrupación de timesteps jerárquica para cuantización INT8/INT4
- **Relevancia**: Muy útil para deploy en NaN (MicroVM 2GB RAM)

### 6.4. Diffusion Transformer Policy (Mar 2025)
- **Aplicación**: Control robótico con DiT
- **Idea**: Modelar secuencias de acción continua con DiT en vez de heads pequeños
- **Relevancia**: Patrón aplicable a control de sistemas físicos

---

## 7. Implementación Práctica: Entrenamiento

```python
import torch
import torch.nn.functional as F

def train_dit(
    model: DiT,
    dataloader,
    num_timesteps: int = 1000,
    lr: float = 1e-4,
    epochs: int = 100,
):
    """
    Entrenamiento de DiT para generación de imágenes.
    Predicción de ruido (epsilon-parametrization).
    """
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-2)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, epochs)

    model.train()
    for epoch in range(epochs):
        for images, labels in dataloader:
            B, C, H, W = images.shape
            device = images.device

            # 1. Muestrear timesteps aleatorios
            t = torch.randint(0, num_timesteps, (B,), device=device)

            # 2. Añadir ruido: x_t = sqrt_alpha_cumprod * x_0 + sqrt(1-alpha) * noise
            sqrt_alpha_cumprod = get_sqrt_alpha_cumprod(t, num_timesteps)
            sqrt_one_minus_alpha_cumprod = get_sqrt_one_minus_alpha_cumprod(t, num_timesteps)
            noise = torch.randn_like(images)

            x_t = sqrt_alpha_cumprod * images + sqrt_one_minus_alpha_cumprod * noise

            # 3. Condicionamiento (texto o clase)
            cond = get_conditioning(labels)  # (B, 77, 512)

            # 4. Predicción de ruido
            pred_noise = model(x_t, t, cond)

            # 5. Loss MSE sobre el ruido
            loss = F.mse_loss(pred_noise, noise)

            # 6. Backprop
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            scheduler.step()

        if epoch % 10 == 0:
            print(f"Epoch {epoch}: loss = {loss.item():.4f}")
```

---

## 8. Referencias Clave

### Papers Fundamentales
1. **Dhariwal & Nichol (2023)** — "Scalable Diffusion Models with Transformers" — arXiv:2303.08774
2. **Rombach et al. (2022)** — "High-Resolution Image Synthesis with Latent Diffusion Models" (Stable Diffusion) — arXiv:2112.10752
3. **Ho et al. (2020)** — "Denoising Diffusion Probabilistic Models" (DDPM) — arXiv:2006.11239

### Optimizaciones Recientes
4. **Zhao et al. (2024)** — "Dynamic Diffusion Transformer (DyDiT)" — arXiv:2410.03456
5. **Post-Training Quantization for DiT** — arXiv:2503.06930
6. **PiT: Progressive Diffusion Transformer** — arXiv:2505.13219
7. **Diffusion Transformer Policy** — arXiv:2410.15959

### Repositorios
- **timm DiT**: `huggingface/pytorch-image-models` (implementación oficial en timm)
- **DyDiT**: `NUS-HPC-AI-Lab/Dynamic-Diffusion-Transformer`
- **HuggingFace Diffusers**: `diffusers` library (usa DiT en `StableDiffusionXLPipeline`)

---

## 9. Conclusiones y Relevancia para Nuestro Stack

### ¿Por qué importa DiT?

1. **Escalabilidad**: A diferencia de U-Nets, DiT escala de forma predecible. Más parámetros = mejor calidad linealmente. Esto es crucial para nuestro deploy en MicroVMs con recursos limitados.

2. **Generación probabilística para forecasting**: La naturaleza de generación de distribución de DiT es ideal para forecasting probabilístico en ESIOS (precios, demanda, renovables). En vez de un punto, generamos intervalos completos.

3. **Convergencia arquitectural**: DiT une dos mundos — transformers (que ya usamos en NLP/forecasting) y diffusion (que ya estudiamos). Es un puente natural.

4. **Optimizaciones recientes**: DyDiT (51% menos FLOPs) y quantización hacen viable DiT en nuestro stack de recursos limitados.

### Siguiente paso natural
- **Time-Series-DiT**: Adaptar DiT para forecasting de precios eléctricos
- **DyDiT en ESIOS**: Usar width dinámico para reducir compute en inferencia
- **Comparación con State Space Models**: Mamba ya cubierto, pero DiT + SSM es el estado del arte

---

## 10. Tema Sugerido para la Próxima Sesión

**World Models / Generative World Models** — Pi0, Genie, Juke: modelos que aprenden dinámicas del mundo y generan secuencias futuras. Es el paso natural después de DiT: de "generar imágenes" a "generar mundos". Muy relevante para simulación de sistemas energéticos y forecasting de múltiples pasos.

Alternativa: **Mamba-2 / SSM Transformers** — evolución de los state space models que ya cubrimos, con atención híbrida SSM+attention.
