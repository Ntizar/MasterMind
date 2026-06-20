"""
Diffusion Model para Series Temporales — Implementación desde cero
===============================================================
Adaptado de Ho et al. (DDPM, 2020) y DiffusionTime (2023).
PyTorch puro, sin dependencias externas.

Clases principales:
- NoiseScheduler: schedule de ruido (linear/cosine)
- ConditionalDenoiser: red que predice ruido con AdaLN + conditioning exógeno
- DiffusionModel: modelo completo con training + sampling DDIM + multi-sample uncertainty
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class NoiseScheduler:
    """Schedule de ruido para el proceso de difusión."""
    
    def __init__(self, T=1000, beta_start=0.0001, beta_end=0.02, schedule="cosine"):
        self.T = T
        if schedule == "linear":
            self.betas = torch.linspace(beta_start, beta_end, T)
        elif schedule == "cosine":
            steps = T + 1
            x = torch.linspace(0, T, steps)
            alphas_cumprod = torch.cos(((x / T) + 0.008) / 1.0864 * math.pi / 2) ** 2
            alphas_cumprod = alphas_cumprod / alphas_cumprod[0]
            self.betas = 1 - (alphas_cumprod[1:] / alphas_cumprod[:-1])
            self.betas = torch.clamp(self.betas, min=0.0001, max=0.02)
        else:
            raise ValueError(f"Unknown schedule: {schedule}")
        
        self.alphas = 1 - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0)
        self.alphas_cumprod_prev = F.pad(self.alphas_cumprod[:-1], (1, 0), value=1.0)
        self.sqrt_alphas_cumprod = torch.sqrt(self.alphas_cumprod)
        self.sqrt_one_minus_alphas_cumprod = torch.sqrt(1 - self.alphas_cumprod)
    
    def q_sample(self, x_start, t, noise=None):
        """Forward diffusion: x_t = √(ᾱ_t) · x_0 + √(1-ᾱ_t) · ε"""
        if noise is None:
            noise = torch.randn_like(x_start)
        sqrt_ac = self.sqrt_alphas_cumprod[t][:, None, None]
        sqrt_1_ac = self.sqrt_one_minus_alphas_cumprod[t][:, None, None]
        return sqrt_ac * x_start + sqrt_1_ac * noise


class SinusoidalPositionEmbeddings(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
        
    def forward(self, t):
        device = t.device
        half_dim = self.dim // 2
        emb = math.log(10000) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim, device=device) * -emb)
        emb = t[:, None] * emb[None, :]
        return torch.cat((emb.sin(), emb.cos()), dim=-1)


class TimeEmbedder(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.emb = SinusoidalPositionEmbeddings()
        self.fc = nn.Sequential(
            nn.Linear(dim, dim * 4),
            nn.SiLU(),
            nn.Linear(dim * 4, dim * 4)
        )
    
    def forward(self, t):
        return self.fc(self.emb(t))


class TemporalConvBlock(nn.Module):
    def __init__(self, in_ch, out_ch, dropout=0.1):
        super().__init__()
        self.conv1 = nn.Conv1d(in_ch, out_ch, 3, padding=1)
        self.conv2 = nn.Conv1d(out_ch, out_ch, 3, padding=1)
        self.norm1 = nn.LayerNorm(out_ch)
        self.norm2 = nn.LayerNorm(out_ch)
        self.dropout = nn.Dropout(dropout)
        self.skip = nn.Conv1d(in_ch, out_ch, 1) if in_ch != out_ch else nn.Identity()
        self.act = nn.SiLU()
    
    def forward(self, x):
        r = x
        x = self.norm1(x.transpose(1, 2))
        x = self.act(self.conv1(x))
        x = self.norm2(x.transpose(1, 2))
        x = self.act(self.dropout(self.conv2(x)))
        return x + self.skip(r.transpose(1, 2)).transpose(1, 2)


class ConditionalDenoiser(nn.Module):
    """
    Denoiser con condicionamiento exógeno.
    Input: (batch, seq_len, features)
    Output: (batch, seq_len, features) — predicción del ruido
    
    Usa AdaLN (Adaptive Layer Normalization) para inyectar el timestep.
    Conditioning exógeno (clima, hora, tipo día) se suma como bias.
    """
    
    def __init__(self, input_dim=1, hidden_dim=128, time_dim=64, 
                 num_cond_features=0, num_layers=4, dropout=0.1):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        self.time_mlp = TimeEmbedder(time_dim)
        self.time_proj = nn.Linear(time_dim, hidden_dim * 2)
        
        if num_cond_features > 0:
            self.cond_proj = nn.Linear(num_cond_features, hidden_dim)
            self.use_conditioning = True
        else:
            self.use_conditioning = False
        
        self.blocks = nn.ModuleList([
            TemporalConvBlock(hidden_dim, hidden_dim, dropout)
            for _ in range(num_layers)
        ])
        self.output_proj = nn.Linear(hidden_dim, input_dim)
        self.norm = nn.LayerNorm(hidden_dim)
    
    def forward(self, x_t, t, condition=None):
        x = self.input_proj(x_t)
        time_emb = self.time_mlp(t)
        time_emb = self.time_proj(time_emb).unsqueeze(1)
        time_scale, time_shift = time_emb.chunk(2, dim=-1)
        
        for block in self.blocks:
            x = x * (1 + time_scale) + time_shift
            if self.use_conditioning and condition is not None:
                x = x + self.cond_proj(condition).unsqueeze(1)
            x = self.norm(x)
            x = block(x)
        
        return self.output_proj(x)


class DiffusionModel(nn.Module):
    """Modelo de difusión completo para series temporales."""
    
    def __init__(self, input_dim=1, hidden_dim=128, time_dim=64,
                 num_cond_features=0, num_layers=4, T=1000, schedule="cosine",
                 dropout=0.1):
        super().__init__()
        self.scheduler = NoiseScheduler(T=T, schedule=schedule)
        self.denoiser = ConditionalDenoiser(
            input_dim=input_dim, hidden_dim=hidden_dim, time_dim=time_dim,
            num_cond_features=num_cond_features, num_layers=num_layers, dropout=dropout
        )
        self.T = T
    
    def forward(self, x_start, condition=None):
        """Training forward pass: muestrea t, añade ruido, predice ε."""
        bs = x_start.size(0)
        t = torch.randint(0, self.T, (bs,), device=x_start.device)
        noise = torch.randn_like(x_start)
        x_noisy = self.scheduler.q_sample(x_start, t, noise)
        noise_pred = self.denoiser(x_noisy, t, condition)
        return F.mse_loss(noise_pred, noise)
    
    @torch.no_grad()
    def sample(self, shape, condition=None, num_steps=None, guidance_scale=1.5):
        """DDIM-style sampling con clipping para estabilidad."""
        if num_steps is None:
            num_steps = self.T
        timesteps = self._ddim_timesteps(num_steps)
        bs = shape[0]
        device = next(self.parameters()).device
        x = torch.randn(shape, device=device)
        alphas = self.scheduler.alphas
        
        for t in timesteps:
            t_tensor = torch.full((bs,), t, device=device, dtype=torch.long)
            noise_pred = self.denoiser(x, t_tensor, condition)
            
            alpha_t = alphas[t]
            alpha_prev = alphas[max(t - 1, 0)] if t > 0 else torch.tensor(0.0, device=device)
            
            # Deterministic DDIM
            pred_orig = (x - torch.sqrt(1 - alpha_t) * noise_pred) / torch.sqrt(alpha_t)
            pred_orig = torch.clamp(pred_orig, -5, 5)  # CLIP CRÍTICO para estabilidad
            
            x = torch.sqrt(alpha_prev) * pred_orig + torch.sqrt(1 - alpha_prev) * noise_pred
            
            # Classifier-free guidance
            if guidance_scale > 1.0 and condition is not None:
                noise_uc = self.denoiser(x, t_tensor, None)
                noise_pred = noise_uc + guidance_scale * (noise_pred - noise_uc)
        
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
        """Generar múltiples muestras para estimar incertidumbre (mediana, p5, p95)."""
        samples = torch.stack([self.sample(shape, condition) for _ in range(n_samples)])
        return (torch.median(samples, dim=0).values,
                torch.quantile(samples, 0.05, dim=0),
                torch.quantile(samples, 0.95, dim=0),
                samples)


# Demo
def demo():
    print("=" * 60)
    print("Diffusion Model para Series Temporales — Demo")
    print("=" * 60)
    
    model = DiffusionModel(input_dim=1, hidden_dim=64, time_dim=32,
                           num_cond_features=3, num_layers=3, T=200, schedule="cosine")
    print(f"Parámetros: {sum(p.numel() for p in model.parameters()):,}")
    
    # Datos sintéticos (demanda con patrones diarios/semanales)
    t = torch.arange(168).float()
    daily = 50 + 30 * torch.sin(2 * torch.pi * t / 24) + 15 * torch.sin(2 * torch.pi * t / 12)
    dow = (t / 24) % 7
    weekly = torch.where(dow < 5, 0, -10)
    x_train = (daily.unsqueeze(0).expand(32, -1, 1) + weekly.unsqueeze(0).expand(32, -1, 1)
               + torch.randn(32, 168, 1) * 2).clamp(0, None)
    cond = torch.rand(32, 3)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler_lr = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_epochs=50)
    
    for epoch in range(50):
        model.train()
        optimizer.zero_grad()
        idx = torch.randint(0, 32, (32,))
        loss = model(x_train[idx], cond[idx])
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler_lr.step()
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1:3d}/50 — Loss: {loss.item():.4f}")
    
    model.eval()
    sample = model.sample((1, 168, 1), condition=cond[:1])
    print(f"Muestra: range=[{sample.min():.2f}, {sample.max():.2f}]")
    
    med, p5, p95, _ = model.generate_multiple_samples((1, 168, 1), n_samples=10, condition=cond[:1])
    print(f"Incertidumbre: [p5={p5[0,0]:.2f}, med={med[0,0]:.2f}, p95={p95[0,0]:.2f}]")
    print("✅ Demo completada")
    return model