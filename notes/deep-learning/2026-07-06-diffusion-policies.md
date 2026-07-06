# Diffusion Policies — Control y Robótica con Diffusion Models

**Fecha:** 2026-07-06  
**Tema:** Aplicación de diffusion models a políticas de decisión/robótica  
**Nivel:** Técnico-práctico

---

## 1. Concepto Central

**Diffusion Policy** (Chen et al., 2023, CoRL 2023) es un paradigm shift en control robotico: en lugar de usar RL tradicional (PPO, SAC) para aprender políticas de actuación, se entrena un **modelo de difusión condicional** para modelar la distribución completa de acciones futuras dado el estado del agente y el entorno.

La intuición clave: las políticas de robótica suelen ser **multimodales** — hay múltiples acciones igualmente válidas en un estado dado (ej: alrededor de un obstáculo, puedes ir por la izquierda o por la derecha). Los métodos RL clásicos (que optimizan una política paramétrica puntual) tienden a colapsar a una sola moda. Los diffusion models, por su naturaleza de proceso generativo, **capturan naturalmente la multimodalidad**.

### Paper fundacional

- **"Diffusion Policies as an Expressive Policy for Robots"** — Yuxiao Chen et al., MIT & Stanford, CoRL 2023
- DOI: arXiv:2303.04137
- Código: https://github.com/real-stable-baselines/diffusion_policy

### Papers siguientes clave

- **Diffuser** (Ajay et al., 2022): Primer trabajo en usar diffusion para planificación secuencial
- **Decision Transformer** (Chen et al., 2021): Modelo transformers para RL, predecesor conceptual
- **DT-2 / RT-2** (Team RT-1, 2023-2024): Extensiones a visión-language-action
- **Diffusion-VP** (Sadhukhan et al., 2024): Variantes de score matching
- **RoboFlow** (Luo et al., 2024): Diffusion policies para manipulación en vídeo

---

## 2. Fundamento Matemático

### 2.1. Formulación como aprendizaje de comportamiento

En lugar de optimizar una política π(a|s) directamente, Diffusion Policy aprende a **denoising** una distribución sobre tramos de acciones (horizon H):

```
a_t, a_{t+1}, ..., a_{t+H} ~ π*(· | s_t, obs_t)
```

Donde obs_t puede ser imagen + estado cinemático.

### 2.2. Condicionamiento por estado

El proceso de difusión se entrena para predecir acciones "limpias" a partir de ruido:

```
q(a_{t-k} | a_t) = N(a_{t-k}; √α_{t-k} a_t, (1-α_{t-k})I)  — forward
p_θ(a_{t-k-1} | a_t, a_{t-k}, obs) = N(a_{t-k-1}; μ_θ(...), Σ_θ(...))  — reverse
```

La clave: **obs** (observaciones/estado) condensa la trayectoria reverse process.

### 2.3. U-Net con cross-attention

La red central es un **U-Net 1D** (operando sobre tramos de acción) con cross-attention sobre las observaciones:

```
CrossAttn(query=action_features, key=value=obs_features)
```

Las observaciones (imágenes, states) se codifican con un backbone (ResNet + MLP) y se inyectan como contexto mediante cross-attention layers.

---

## 3. Implementación Práctica

### 3.1. Estructura del modelo

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class DiffusionPolicy(nn.Module):
    """
    Diffusion Policy simplificada para control robotico.
    
    Architecture:
    - Visual encoder: ResNet-18 para imágenes
    - State encoder: MLP para states cinemáticos
    - Fusion: concat + MLP
    - Diffusion backbone: 1D U-Net con cross-attention
    """
    
    def __init__(self, 
                 action_dim=7,      # dimensión de la acción (ej: 6 DOF + gripper)
                 horizon=16,         # horizonte de planificación (tramo)
                 n_timesteps=20,     # pasos de denoising
                 hidden_dim=128,
                 image_size=(64, 64),
                 state_dim=12):
        super().__init__()
        
        self.action_dim = action_dim
        self.horizon = horizon
        self.n_timesteps = n_timesteps
        self.action_seq_dim = action_dim * horizon
        
        # --- Visual encoder (ResNet backbone) ---
        self.visual_encoder = ResNetVisualEncoder(
            input_ch=3, 
            output_dim=hidden_dim,
            image_size=image_size
        )
        
        # --- State encoder ---
        self.state_encoder = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
        )
        
        # --- Observación fusionada ---
        self.obs_proj = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
        )
        
        # --- Diffusion U-Net (1D temporal) ---
        self.diffusion = DiffusionUNet1D(
            input_dim=action_seq_dim,
            cond_dim=hidden_dim,
            n_timesteps=n_timesteps,
            hidden_dim=hidden_dim,
        )
        
        # --- Schedule ---
        self.schedule = cosine_beta_schedule(n_timesteps)
        
    def forward(self, obs_images, obs_states, t):
        """
        Forward pass: predice el ruido para loss de difusión.
        
        Args:
            obs_images: (B, T_v, C, H, W) — imágenes de cámara(s)
            obs_states: (B, T_s) — estados cinemáticos
            t: (B,) — timestep de difusión actual
        """
        B = obs_images.shape[0]
        
        # Codificar observaciones
        visual_feat = self.visual_encoder(obs_images)  # (B, hidden_dim)
        state_feat = self.state_encoder(obs_states)     # (B, hidden_dim)
        
        obs_cond = self.obs_proj(torch.cat([visual_feat, state_feat], dim=-1))
        
        # Generar tramo de acción con ruido
        clean_actions = torch.randn(B, self.action_seq_dim, device=obs_images.device)
        noise = torch.randn_like(clean_actions)
        
        # Aplicar ruido en timestep t
        alpha_cumprod = self.schedule.cumprod(t)  # (B,)
        noisy_actions = (
            torch.sqrt(alpha_cumprod).view(B, 1) * clean_actions
            + torch.sqrt(1 - alpha_cumprod).view(B, 1) * noise
        )
        
        # Predicción de ruido con U-Net
        predicted_noise = self.diffusion(noisy_actions, t, obs_cond)
        
        return predicted_noise, noise
    
    @torch.no_grad()
    def sample_actions(self, obs_images, obs_states, n_samples=1, device='cpu'):
        """
        Sample actions from the learned diffusion policy.
        
        Args:
            obs_images: (B, T_v, C, H, W)
            obs_states: (B, T_s)
            n_samples: número de muestras (para explotar multimodalidad)
            
        Returns:
            actions: (B, horizon, action_dim) — primeras H acciones
        """
        B = obs_images.shape[0]
        
        # Codificar observaciones
        visual_feat = self.visual_encoder(obs_images)
        state_feat = self.state_encoder(obs_states)
        obs_cond = self.obs_proj(torch.cat([visual_feat, state_feat], dim=-1))
        
        # Iniciar desde ruido puro
        x = torch.randn(B, self.action_seq_dim, n_samples, device=device)
        
        # Reverse process (DPM-Solver para eficiencia)
        for i in reversed(range(self.n_timesteps)):
            t = torch.full((B,), i, device=device, dtype=torch.long)
            
            # Predicción de ruido
            noise_pred = self.diffusion(x.transpose(1, 2).reshape(B*self.n_samples, -1), 
                                         t, obs_cond.unsqueeze(1))
            noise_pred = noise_pred.reshape(B, -1, n_samples)
            
            # Actualizar con schedule
            alpha = self.schedule[i]
            beta = self.schedule[i:i+1]
            
            x = (x - (1-alpha).sqrt() * noise_pred) / alpha.sqrt()
            if i > 0:
                x = x + beta.sqrt() * torch.randn_like(x)
        
        # Extraer acción (primera moda, o la que tenga mayor probabilidad)
        actions = x[:, :, 0].reshape(B, self.horizon, self.action_dim)
        
        return actions  # (B, H, action_dim)
```

### 3.2. Backbone Visual Encoder

```python
class ResNetVisualEncoder(nn.Module):
    """ResNet-18 adaptado para features visuales."""
    
    def __init__(self, input_ch=3, output_dim=128, image_size=(64, 64)):
        super().__init__()
        
        from torchvision import models
        resnet = models.resnet18(weights=None)
        
        # Adaptar primer layer si es necesario
        if input_ch != 3:
            resnet.conv1 = nn.Conv2d(input_ch, 64, kernel_size=7, stride=2, padding=3, bias=False)
        
        # Eliminar layers de clasificación
        self.backbone = nn.Sequential(*list(resnet.children())[:-2])  # output: (B, 512, 4, 4)
        
        # Projection a dim objetivo
        self.projection = nn.Sequential(
            nn.Flatten(),
            nn.Linear(512 * 4 * 4, output_dim),
            nn.LayerNorm(output_dim),
        )
        
    def forward(self, x):
        return self.projection(self.backbone(x))
```

### 3.3. U-Net 1D con Cross-Attention

```python
class DiffusionUNet1D(nn.Module):
    """
    U-Net 1D para diffusion sobre secuencias temporales de acción.
    
    Con cross-attention para condicionar sobre observaciones.
    """
    
    def __init__(self, input_dim, cond_dim, n_timesteps, hidden_dim):
        super().__init__()
        
        self.time_embed = nn.Sequential(
            SinusoidalPositionEmbedding(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        
        # Encoder (downsampling)
        self.enc_blocks = nn.ModuleList([
            ResBlock1D(hidden_dim, cond_dim, cross_attn=True),
            ResBlock1D(hidden_dim, cond_dim, cross_attn=True),
            ResBlock1D(hidden_dim * 2, cond_dim, cross_attn=True),
        ])
        self.downsamplers = nn.ModuleList([
            nn.Conv1d(hidden_dim, hidden_dim, 3, 2, 1),  # half length
            nn.Conv1d(hidden_dim, hidden_dim*2, 3, 2, 1),
        ])
        
        # Bottleneck
        self.bottleneck = nn.Sequential(
            ResBlock1D(hidden_dim * 2, cond_dim, cross_attn=True),
            ResBlock1D(hidden_dim * 2, cond_dim, cross_attn=True),
        )
        
        # Decoder (upsampling)
        self.upsamplers = nn.ModuleList([
            nn.ConvTranspose1d(hidden_dim * 2, hidden_dim, 3, 2, 1, 1),
            nn.ConvTranspose1d(hidden_dim, hidden_dim, 3, 2, 1, 1),
        ])
        self.dec_blocks = nn.ModuleList([
            ResBlock1D(hidden_dim * 2, cond_dim, cross_attn=True),
            ResBlock1D(hidden_dim, cond_dim, cross_attn=True),
            ResBlock1D(hidden_dim, cond_dim, cross_attn=True),
        ])
        
        self.output_proj = nn.Sequential(
            nn.LayerNorm(hidden_dim),
            nn.Conv1d(hidden_dim, input_dim, 1),
        )
        
    def forward(self, x, t, cond):
        """
        Args:
            x: (B, input_dim, L) — acción con ruido, forma channel-first
            t: (B,) — timesteps
            cond: (B, cond_dim) — features de observación
        """
        B, L = x.shape[0], x.shape[-1]
        
        # Time embedding
        t_emb = self.time_embed(t)  # (B, hidden_dim)
        
        # Skip connections
        skips = []
        
        # Encoder
        x = self.input_proj(x.transpose(1, 2)).transpose(1, 2)  # (B, H, L)
        for enc, down in zip(self.enc_blocks, self.downsamplers):
            x = enc(x, t_emb, cond)
            skips.append(x)
            x = down(x)
        
        # Bottleneck
        x = self.bottleneck(x, t_emb, cond)
        
        # Decoder
        for up, dec in zip(self.upsamplers, self.dec_blocks):
            x = up(x)
            skip = skips.pop()
            x = torch.cat([x, skip], dim=1)
            x = dec(x, t_emb, cond)
        
        return self.output_proj(x).transpose(1, 2)  # (B, input_dim, L)


class SinusoidalPositionEmbedding(nn.Module):
    """Sinusoidal positional encoding para timesteps de difusión."""
    
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
        
    def forward(self, t):
        device = t.device
        half_dim = self.dim // 2
        emb = math.log(10000) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim, device=device) * -emb)
        emb = t.unsqueeze(1) * emb.unsqueeze(0)
        emb = torch.cat((emb.sin(), emb.cos()), dim=-1)
        return emb


class CrossAttention(nn.Module):
    """Cross-attention para diffusion U-Net."""
    
    def __init__(self, dim, n_heads=8):
        super().__init__()
        self.attn = nn.MultiheadAttention(dim, n_heads, batch_first=True)
        self.norm = nn.LayerNorm(dim)
        
    def forward(self, x, cond):
        """
        Args:
            x: (B, L, dim) — action sequence
            cond: (B, C, dim) — condensed obs (C=1 para MLP, C>1 para seq)
        """
        x_norm = self.norm(x)
        # cond: (B, C, D) -> (B, C, D) como key/value
        # x_norm: (B, L, D) como query
        out, _ = self.attn(x_norm, cond.transpose(1, 2), cond.transpose(1, 2))
        return x + out


class ResBlock1D(nn.Module):
    """Residual block con opcional cross-attention."""
    
    def __init__(self, dim, cond_dim, cross_attn=True):
        super().__init__()
        
        self.blocks = nn.Sequential(
            nn.LayerNorm(dim),
            nn.GELU(),
            nn.Conv1d(dim, dim, 3, padding=1),
            nn.LayerNorm(dim),
            nn.GELU(),
            nn.Conv1d(dim, dim, 3, padding=1),
        )
        
        # Time embedding modulation
        self.time_mlp = nn.Sequential(
            nn.GELU(),
            nn.Linear(cond_dim, dim),
        )
        
        self.cross_attn = CrossAttention(dim) if cross_attn else None
        
    def forward(self, x, t_emb, cond):
        """
        x: (B, D, L) channel-first for conv
        """
        residual = x
        
        # Modulate con time embedding
        scale = self.time_mlp(t_emb).unsqueeze(-1)  # (B, D, 1)
        
        out = self.blocks(x)
        out = out * (1 + scale)  # adaptive layer norm style
        
        # Cross-attention
        if self.cross_attn is not None:
            out = self.cross_attn(out.transpose(1, 2), cond).transpose(1, 2)
        
        return out + residual
```

### 3.4. Schedule y Training Loop

```python
def cosine_beta_schedule(timesteps, s=0.008):
    """
    Schedule β(t) de la difusión con enfoque coseno.
    
    Basado en: "Improved Diffusion Models" (Nichol & Dhariwal, 2021)
    """
    steps = timesteps + 1
    x = torch.linspace(0, timesteps, steps)
    alphas_cumprod = torch.cos(((x / timesteps) + s) / (1 + s) * math.pi * 0.5) ** 2
    alphas_cumprod = alphas_cumprod / alphas_cumprod[0]
    betas = 1 - (alphas_cumprod[1:] / alphas_cumprod[:-1])
    return torch.clip(betas, 0.0001, 0.9999)


class DiffusionPolicyTrainer:
    """
    Training loop para Diffusion Policy.
    
    Usa dataset de demonstrations (obs, action_sequence) y entrena
    la política para predecir el ruido en el proceso de difusión.
    """
    
    def __init__(self, policy, lr=1e-4):
        self.policy = policy
        self.optimizer = torch.optim.AdamW(policy.parameters(), lr=lr, weight_decay=1e-4)
        self.loss_fn = nn.MSELoss()
        
    def train_step(self, batch):
        """
        Un paso de training.
        
        Args:
            batch: dict con keys:
                - images: (B, T, C, H, W)
                - states: (B, state_dim)
                - actions: (B, horizon, action_dim)
        """
        images = batch['images']
        states = batch['states']
        actions = batch['actions']
        
        # Muestrear timestep de difusión aleatorio
        t = torch.randint(0, self.policy.n_timesteps, (actions.shape[0],), 
                         device=actions.device)
        
        # Forward pass
        predicted_noise, target_noise = self.policy(images, states, t)
        
        # Loss: MSE entre ruido predicho y ruido real
        loss = self.loss_fn(predicted_noise, target_noise)
        
        self.optimizer.zero_grad()
        loss.backward()
        
        # Gradient clipping para estabilidad
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), max_norm=1.0)
        
        self.optimizer.step()
        
        return loss.item()
    
    def collect_demonstration_data(self, env, demo_policy, n_episodes=1000):
        """
        Recopilar demostraciones del entorno.
        
        Para datasets como DROID, Open X-Embodiment, o SIMpler.
        """
        dataset = {
            'images': [],
            'states': [],
            'actions': []
        }
        
        for ep in range(n_episodes):
            obs, done = env.reset(), False
            episode_images = []
            episode_states = []
            episode_actions = []
            
            while not done:
                # Capturar observaciones
                image = env.get_observation()  # (C, H, W)
                state = env.get_state()        # (state_dim,)
                
                # Ejecutar demostración
                action = demo_policy.act(image, state)
                
                next_obs, reward, done, info = env.step(action)
                
                episode_images.append(image)
                episode_states.append(state)
                episode_actions.append(action)
                
                obs = next_obs
            
            # Pad/truncate al horizonte
            dataset['images'].append(
                torch.tensor(np.stack(episode_images[:self.policy.horizon]))
            )
            dataset['states'].append(
                torch.tensor(np.stack(episode_states[:self.policy.horizon]))
            )
            dataset['actions'].append(
                torch.tensor(np.stack(episode_actions[:self.policy.horizon]))
            )
        
        return dataset
```

---

## 4. Aplicaciones Prácticas

### 4.1. Robótica Móvil

Diffusion Policy para navegación autónoma en entornos dinámicos:
- Observaciones: cámara RGB + LiDAR range
- Acciones: velocidad lineal y angular (cmd_vel de ROS)
- Horizon: ~10 pasos → planificación a corto plazo

**Ventaja sobre RL:** Captura las múltiples rutas válidas alrededor de obstáculos, lo que mejora la exploración y robustez.

### 4.2. Manipulación Robótica

Para brazos robóticos (7-DOF + gripper):
- Observaciones: cámara overhead + estados de las juntas
- Acciones: positions/velocities de las juntas
- Horizon: 16-32 pasos para movimientos suaves

**Dataset clave:** **DROID** (337K demostraciones de 5 robots distintos, incluido uno humano) — https://droid-dataset.github.io/

### 4.3. Datasets Disponibles

| Dataset | Contenido | URL |
|---------|-----------|-----|
| **DROID** | 337K demos, 5 robots, tareas reales | droid-dataset.github.io |
| **Open X-Embodiment** | 2M+ demos de múltiples robots | https://robotics-transformer-x.github.io/ |
| **RT-X** | Extensiones de RT-1 con diffusion | Google Robotics |
| **BridgeV2** | Manipulación con visión bimodal | https://github.com/rail-berkeley/bridge_data_robot |

---

## 5. Variantes y Estado del Arte (2024-2025)

### 5.1. **Diffusion Policy + Transformers**

Combinar la capacidad de modelado de diffusion con la atención de transformers para horizon más largos:

```
Diffusion-Transformer Policy (DTP):
- Visual tokens (ViT) + state tokens → cross-attention diffusion
- Horizon de 100+ pasos (vs 16-32 de DP clásica)
- Mejor planificación a largo plazo
```

### 5.2. **Diffusion en Latent Space**

Reducir la dimensionalidad del espacio de acción antes de aplicar difusión:
- **Latent Diffusion Policy** (LDP): primero comprimir acciones con VAE, luego aplicar diffusion en el espacio latente
- Más eficiente computacionalmente y mejor generalización

### 5.3. **Zero-Shot con Foundation Models**

Integrar Diffusion Policy con foundation models (CLIP, DINOv2) para zero-shot transfer:
- Features de DINOv2 como backbone visual en lugar de ResNet entrenado
- Generalización a tareas no vistas durante el entrenamiento

---

## 6. Comparativa con Alternativas

| Método | Pros | Contras |
|--------|------|---------|
| **PPO/SAC** | Estable, bien entendido | Colapso a moda única, difícil multimodalidad |
| **BC (Behavioral Cloning)** | Simple, rápido | Error compuesto, distribución shift |
| **Diffusion Policy** | Captura multimodalidad, performance SOTA | Costo computacional en inference, muchos pasos |
| **Decision Transformer** | Contextual, no necesita recompensa | Requiere rollout de training data denso |
| **IQL (Implicit Q-Learning)** | Offline RL robusto | Menos expresivo que diffusion |

---

## 7. Tips Prácticos

1. **Horizon tuning:** Horizon corto (8-16) para manipulación rápida, largo (32-64) para navegación. Re-evaluar solo los primeros H' pasos de cada rollout (receding horizon control).

2. **Denoising steps:** 20 pasos default, pero con **DPM-Solver** (Liu et al., 2022) se puede reducir a 4-8 pasos manteniendo calidad → inference 5x más rápido.

3. **Data augmentation:** Crucial para generalización. Rotate, crop, color jitter en las imágenes. En DROID usan "ego-attention" augmentation.

4. **Multi-camera:** Fusionar múltiples vistas en el encoder visual (concat de features o attention pooling).

5. **Inference speed:** El bottleneck es el reverse process de N pasos. Optimizar con:
   - DDIM sampling (menos pasos, menos precisión)
   - DPM-Solver++ (convergencia de orden 2)
   - distillation a un modelo de 1-step

---

## 8. Referencias

1. **Diffusion Policies as an Expressive Policy for Robots** — Chen et al., CoRL 2023
   - arXiv: 2303.04137
   - https://diffusion-policy.cs.columbia.edu/

2. **Diffuser: Diffusion Models for Robotics** — Ajay et al., ICLR 2023
   - arXiv: 2212.10156

3. **RT-2: Vision-Language-Action Models for Robotics** — Brohan et al., 2023
   - https://robotics-transformer2.github.io/

4. **DROID Dataset** — 337K robot demonstrations
   - https://droid-dataset.github.io/

5. **Open X-Embodiment** — 2M+ demonstrations across robots
   - https://robotics-transformer-x.github.io/

6. **DPM-Solver: A Fast ODE Solver for Diffusion Models** — Liu et al., 2022
   - https://github.com/LiuXiaoxinPKU/DPM-Solver

7. **BridgeData V2** — Robotic manipulation dataset
   - https://rail-berkeley.github.io/bridgedata/

---

## 9. Conexión con otros temas del sistema

- **World Models (2026-07-04):** Diffusion policies son un tipo de world model simplificado — modelan la evolución del entorno en términos de acción, no de estado
- **ControlNet (2026-07-05):** Same conditioning mechanism (cross-attention) pero aplicado a control de robots en lugar de generación de imagen
- **State Space Models (2026-06-12):** Alternativa a diffusion para secuencias largas — SSMs tienen inference O(1), diffusion tiene N pasos

---

## 10. Próximos pasos recomendados

1. Probar Diffusion Policy en un simulador (Isaac Gym o MuJoCo)
2. Experimentar con DPM-Solver para inference más rápido
3. Explorar la integración con foundation models para zero-shot
4. Comparar con Decision Transformer en tasks similares

---

*Siguiente tema sugerido:* **Energy-Based Models (EBMs)** — modelo generativo alternativo a diffusion que modela directamente la energía de los datos, con aplicaciones en robustez y aprendizaje semi-supervisado.
