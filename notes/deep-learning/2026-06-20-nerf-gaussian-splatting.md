# NeRF y 3D Gaussian Splatting — Reconstrucción 3D con Redes Neuronales

> **Tema:** Neural Radiance Fields (NeRF) y 3D Gaussian Splatting
> **Fecha:** 2026-06-20
> **Categoría:** Visión por computador / Generación de contenido 3D

---

## 1. Concepto Central

**Problema:** Dadas N imágenes 2D de una escena desde diferentes ángulos, ¿cómo renderizar la escena desde una posición de cámara completamente nueva?

**Solución NeRF (2020):** Codificar la escena como una función continua representada por un MLP:
```
(x, y, z, θ, φ) → (r, g, b, σ)
```
donde (x,y,z) son coordenadas espaciales, (θ,φ) son coordenadas esféricas de la dirección de visión, r,g,b es el color y σ es la densidad de opacidad.

**Solución 3D Gaussian Splatting (2023):** Representar la escena como N gaussianas 3D con parámetros optimizables, renderizar mediante "splatting" diferenciable.

---

## 2. NeRF — El Paper Fundamental

### 2.1 Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                   INPUT: (x,y,z, θ,φ)                │
├──────────────────────┬──────────────────────────────┤
│  Position Encoding   │  View Direction Encoding     │
│  (15 octaves × 2)    │  (4 octaves × 2)             │
│  60D → 277D          │  16D → 54D                   │
├──────────────────────┴──────────────────────────────┤
│              Position Network (4 layers)             │
│              → 1024D → σ (densidad)                  │
│              → 512D → feature vector (256D)          │
├──────────────────────────────────────────────────────┤
│              View Direction Network (3 layers)       │
│              feature(256D) + dir(54D) → 512D         │
│              → 3D color (r,g,b)                      │
└─────────────────────────────────────────────────────┘
```

### 2.2 Volume Rendering

El color renderizado sigue la ecuación de volume rendering clásica:

```
C(r) = ∫_{t_n}^{t_f} T(t) · σ(r(t)) · c(r(t)) · dt
```

Donde:
- `r(t) = o + td` es el rayo desde cámara `o` en dirección `d`
- `T(t) = exp(-∫_{t_n}^t σ(r(s)) ds)` es la acumulación de transparencia
- En forma discreta: `C(r) = Σ_{i=1}^n T_i · (1 - exp(-σ_i · δ_i)) · c_i`

### 2.3 Implementación Práctica — NeRF desde Cero

```python
"""
NeRF implementation — core components
Paper: Mildenhall et al., ECCV 2020
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class PositionalEncoding(nn.Module):
    """
    Positional encoding usado en NeRF.
    Divide la dimensión en frecuencias logarítmicamente crecientes.
    """
    def __init__(self, num_octaves=15, include_input=True):
        super().__init__()
        self.num_octaves = num_octaves
        self.include_input = include_input

    def forward(self, x):
        """
        Args:
            x: tensor de forma (*, D) — coordenadas (x,y,z) o direcciones (θ,φ)
        Returns:
            tensor de forma (*, D * (1 + 2*num_octaves * 2))
            para position encoding: (~277D desde 3D)
            para direction encoding: (~54D desde 2D)
        """
        scales = 2 ** torch.arange(
            self.num_octaves, device=x.device, dtype=x.dtype
        )
        # Generar frecuencias: sin(x), sin(2x), sin(4x), ...
        shaped = x[..., None] * scales[None]  # (*, D, num_octaves)
        shaped = shaped.view(*x.shape[:-1], -1)  # (*, D * num_octaves)
        encoded = torch.sin(torch.cat([shaped, shaped + torch.pi / 2], dim=-1))

        if self.include_input:
            return torch.cat([x, encoded], dim=-1)
        return encoded


class NeRFModel(nn.Module):
    """
    Modelo NeRF completo.
    
    Arquitectura:
    - Position network: input(277D) → 1024 → 1024 → 1024 → 1024 → σ(1D) + features(256D)
    - Color network: features(256D) + direction(54D) → 512 → 512 → color(3D)
    """
    def __init__(
        self,
        xyz_dim=3,
        direction_dim=3,
        num_octaves=15,
        num_octaves_dir=4,
        D=8,
        W=256,
        skips=[4],
    ):
        super().__init__()
        
        # Encodings
        self.pos_encoding = PositionalEncoding(num_octaves, include_input=True)
        self.dir_encoding = PositionalEncoding(num_octaves_dir, include_input=True)
        
        # Calcular dimensiones después del encoding
        pos_encoded_dim = self.pos_encoding(torch.zeros(1, xyz_dim)).shape[-1]
        dir_encoded_dim = self.dir_encoding(torch.zeros(1, direction_dim)).shape[-1]
        
        # Position network
        self.D = D
        self.W = W
        self.skips = skips
        
        # Capas del position network
        self.linears = nn.ModuleList([nn.Linear(pos_encoded_dim, W)])
        for i in range(1, D):
            if i in skips:
                self.linears.append(nn.Linear(W + pos_encoded_dim, W))
            else:
                self.linears.append(nn.Linear(W, W))
        
        # Output layers
        self.sigma_linear = nn.Linear(W, 1)  # densidad
        self.feature_linear = nn.Linear(W, 256)  # feature vector
        
        # Color network
        self.color_input_dim = 256 + dir_encoded_dim
        self.color_net = nn.Sequential(
            nn.Linear(self.color_input_dim, W),
            nn.ReLU(),
            nn.Linear(W, W),
            nn.ReLU(),
            nn.Linear(W, 3),  # RGB
        )
        
        # Init: bias en sigma para aprender escenas oscuras primero
        nn.init.constant_(self.sigma_linear.bias, -2.0)

    def forward(self, x):
        """
        Args:
            x: tensor de forma (*, 6) — concat de (xyz, direction)
        Returns:
            rgb: tensor (*, 3) — color RGB
            sigma: tensor (*, 1) — densidad/opacidad
        """
        xyz = x[..., :3]
        direction = x[..., 3:]
        
        # Encode
        xyz_encoded = self.pos_encoding(xyz)
        direction_encoded = self.dir_encoding(direction)
        
        # Position network
        h = xyz_encoded
        for i, linear in enumerate(self.linears):
            h = linear(h)
            h = F.relu(h)
            if i in self.skips:
                h = torch.cat([h, xyz_encoded], dim=-1)
        
        # Extraer sigma y features
        sigma = self.sigma_linear(h)
        features = self.feature_linear(h)
        
        # Color network
        h_color = torch.cat([features, direction_encoded], dim=-1)
        for i, layer in enumerate(self.color_net):
            h_color = layer(h_color)
            if i < len(self.color_net) - 1:  # ReLU excepto en output
                h_color = F.relu(h_color)
        
        # Sigmoid para RGB (0-1)
        rgb = torch.sigmoid(h_color)
        
        return rgb, sigma


class NeRFRenderer:
    """
    Renderer de NeRF usando volume rendering diferenciable.
    
    Muestrea puntos a lo largo de rayos y usa volume rendering
    para calcular el color final de cada píxel.
    """
    def __init__(
        self,
        near=2.0,
        far=6.0,
        N_samples=64,
        N_importance=64,
        use_inverse_depth=True,
    ):
        self.near = near
        self.far = far
        self.N_samples = N_samples
        self.N_importance = N_importance
        self.use_inverse_depth = use_inverse_depth

    def sample_depths(self, batch_size, N_samples):
        """
        Muestrear profundidades a lo largo del rayo.
        
        Usa muestreo uniforme + muestreo centrado en los picos de densidad.
        """
        # Profundidades uniformes
        t_vals = torch.linspace(0.0, 1.0, N_samples, device='cuda')
        if not self.use_inverse_depth:
            z_vals = self.near * (1.0 - t_vals) + self.far * t_vals
        else:
            # Inverse depth: más muestras cerca de la cámara
            z_vals = 1.0 / (1.0 / self.near * (1.0 - t_vals) + 1.0 / self.far * t_vals)
        
        return z_vals

    @staticmethod
    def volume_render(rgb, sigma, z_vals):
        """
        Volume rendering diferenciable.
        
        C = Σ_i T_i · (1 - exp(-σ_i · δ_i)) · c_i
        T_i = exp(-Σ_{j<i} σ_j · δ_j)
        
        Args:
            rgb: (batch, N_samples, 3) — color en cada muestra
            sigma: (batch, N_samples, 1) — densidad en cada muestra
            z_vals: (batch, N_samples) — profundidades
        Returns:
            rgb_rendered: (batch, 3) — color final por rayo
            depth: (batch, 1) — profundidad esperada
            weights: (batch, N_samples, 1) — pesos de muestreo
        """
        # Distancias entre muestras consecutivas
        dists = z_vals[..., 1:] - z_vals[..., :-1]  # (batch, N_samples-1)
        dists = torch.cat([dists, torch.tensor([1e10], device=z_vals.device).expand_as(dists[..., :1])], dim=-1)
        
        # α = 1 - exp(-σ · δ)
        alpha = 1.0 - torch.exp(-sigma.squeeze(-1) * dists)  # (batch, N_samples)
        
        # Transparencia acumulada T
        T = torch.cumprod(1.0 - alpha + 1e-10, dim=-1)  # (batch, N_samples)
        T = torch.cat([torch.ones_like(T[..., :1]), T[..., :-1]], dim=-1)
        
        # Pesos de muestreo
        weights = alpha * T  # (batch, N_samples)
        
        # Color renderizado
        rgb_rendered = torch.sum(weights[..., None] * rgb, dim=-2)  # (batch, 3)
        
        # Profundidad esperada
        depth = torch.sum(weights * z_vals, dim=-1, keepdim=True)  # (batch, 1)
        
        return rgb_rendered, depth, weights

    @staticmethod
    def sample_pdf(bins, weights, N_importance, det=False, eps=1e-5):
        """
        Muestreo adaptativo (importance sampling) para segunda pasada.
        
        Muestrea más densamente en regiones donde la densidad σ es alta.
        Paper: NeRF, sección 5.2
        """
        # Pesos normalizados
        weights = weights + 1e-5  # Evitar ceros
        pdf = weights / torch.sum(weights, dim=-1, keepdim=True)  # (batch, N_samples-1)
        cdf = torch.cumsum(pdf, dim=-1)  # (batch, N_samples-1)
        cdf = torch.cat([torch.zeros_like(cdf[..., :1]), cdf], dim=-1)  # (batch, N_samples)
        
        # Muestrear uniformemente en [0,1] y encontrar bins correspondientes
        if det:
            u = torch.linspace(0.0, 1.0, N_importance, device=bins.device)
            u = u.expand(cdf.shape)
        else:
            u = torch.rand(cdf.shape, device=cdf.device)
        
        # Invertir CDF para encontrar índices
        u = u.contiguous()
        inds = torch.searchsorted(cdf, u, right=True)  # (batch, N_importance)
        
        # Muestrear dentro de los bins
        below = torch.clamp(inds - 1, min=0)
        above = torch.clamp(inds, max=cdf.shape[-1] - 1)
        inds_squeezed = inds - 1  # Para indexar en cdf
        f = cdf[below] - cdf[above] + 1e-5
        inds_f = (u - cdf[below]) / f
        inds_f = inds_f.clamp(0.0, 1.0)
        
        bins_g = bins[below] + inds_f * (bins[above] - bins[below])
        
        return bins_g


def create_ray_batch(H, W, focal, c2w, near=2.0, far=6.0, N_samples=64):
    """
    Crear un batch de rayos para toda la imagen.
    
    Args:
        H, W: altura y ancho de imagen
        focal: distancia focal
        c2w: matriz camera-to-world (4x4)
        near, far: planos de clipping
        N_samples: muestras por rayo
    Returns:
        rays_o: (H*W, 3) — orígenes de rayos
        rays_d: (H*W, 3) — direcciones de rayos
        z_vals: (H*W, N_samples) — profundidades muestreadas
    """
    # Coordenadas de píxeles centradas
    i, j = torch.meshgrid(
        torch.arange(W, device=c2w.device),
        torch.arange(H, device=c2w.device),
        indexing='xy'
    )
    
    # Dirección de cada rayo en coordenadas de cámara
    dirs = torch.stack([
        (i - W * 0.5) / focal,
        -(j - H * 0.5) / focal,
        -torch.ones_like(i)
    ], dim=-1)  # (H, W, 3)
    
    # Rotar a coordenadas del mundo
    R = c2w[:3, :3]
    dirs = (dirs.view(-1, 1, 3) @ R.transpose(0, 1)).view(-1, 3)  # (H*W, 3)
    
    # Origen de rayos
    origins = torch.zeros_like(dirs)
    origins[..., :3] = c2w[:3, 3]  # Posición de cámara
    
    # Profundidades muestreadas
    t_vals = torch.linspace(0.0, 1.0, N_samples, device=c2w.device)
    z_vals = near * (1.0 - t_vals) + far * t_vals  # (N_samples,)
    z_vals = z_vals.expand(H * W, -1)  # (H*W, N_samples)
    
    return origins, dirs, z_vals


def train_step(model, ray_batch, target_color, optimizer):
    """
    Un paso de entrenamiento de NeRF.
    
    Args:
        model: NeRFModel
        ray_batch: dict con 'rays_o' (N,3), 'rays_d' (N,3), 'z_vals' (N, M)
        target_color: tensor (N, 3) — color objetivo del píxel
        optimizer: optimizer de PyTorch
    Returns:
        loss: escalar — pérdida del paso
    """
    optimizer.zero_grad()
    
    # Concatenar orígenes y direcciones
    xyz = torch.cat([ray_batch['rays_o'], ray_batch['rays_d']], dim=-1)  # (N, 6)
    
    # Forward pass
    rgb, sigma = model(xyz)  # (N, 3), (N, 1)
    
    # Volume rendering
    renderer = NeRFRenderer()
    rgb_rendered, depth, weights = renderer.volume_render(
        rgb, sigma, ray_batch['z_vals']
    )
    
    # Loss: MSE + pérdida de opacidad en fondo
    rgb_loss = F.mse_loss(rgb_rendered, target_color)
    
    # Regularización: forzar fondo transparente
    bg_loss = torch.mean(torch.relu(1.0 - weights[..., -1]))
    
    loss = rgb_loss + 0.1 * bg_loss
    
    loss.backward()
    optimizer.step()
    
    return loss.item()


# === Ejemplo de uso ===
if __name__ == "__main__":
    # Configurar escena simple
    H, W = 400, 400
    focal = 400.0
    N_samples = 128
    
    # Modelo NeRF
    model = NeRFModel(
        xyz_dim=3,
        direction_dim=3,
        num_octaves=10,      # Reducido para demo
        num_octaves_dir=4,
        D=8,
        W=256,
        skips=[4],
    )
    
    print(f"Parámetros del modelo: {sum(p.numel() for p in model.parameters()):,}")
    
    # Simular pose de cámara
    c2w = torch.eye(4)
    c2w[2, 3] = 4.0  # Cámara a z=4
    
    # Crear batch de rayos
    rays_o, rays_d, z_vals = create_ray_batch(H, W, focal, c2w, N_samples=N_samples)
    
    ray_batch = {
        'rays_o': rays_o,
        'rays_d': rays_d,
        'z_vals': z_vals,
    }
    
    # Forward pass
    xyz = torch.cat([rays_o, rays_d], dim=-1)
    rgb, sigma = model(xyz)
    
    # Renderizado
    rgb_rendered, depth, weights = NeRFRenderer.volume_render(
        rgb, sigma, z_vals
    )
    
    print(f"RGB renderizado shape: {rgb_rendered.shape}")  # (160000, 3)
    print(f"Depth shape: {depth.shape}")  # (160000, 1)
    print(f"Color range: [{rgb_rendered.min():.3f}, {rgb_rendered.max():.3f}]")
```

---

## 3. 3D Gaussian Splatting — La Revolución

### 3.1 ¿Por qué 3DGS es diferente?

| Aspecto | NeRF | 3D Gaussian Splatting |
|---------|------|----------------------|
| Representación | MLP continuo | N gaussianas 3D discretas |
| Training time | Horas | Minutos |
| Inference | Ray marching lento | Splatting en GPU (100+ fps) |
| Calidad | Alta (suave) | Alta (con aliasing controlado) |
| Memoria | MLP pequeño (~10MB) | Lista de gaussianas (~GB) |
| Editable | No (modelo negro) | Sí (manipular gaussianas) |

### 3.2 Representación con Gaussianas 3D

Cada gaussiana G_i se define por 11 parámetros optimizables:

```
G_i = {μ_i (3D), Σ_i (3x3 covarianza), o_i (opacity), c_i (color)}
```

Descomposición de la covarianza:
```
Σ = RSS^T R^T
```
- S (3D): escala de la gaussiana
- R (3x3 rotación, cuaternión): orientación
- o_i: opacidad (0-1)
- c_i: color (SH de grado 0 → 3 coeficientes RGB)

### 3.3 Pipeline de Entrenamiento

```
┌──────────────────────────────────────────────────────────┐
│  1. Inicialización (de punto nube SfM)                    │
│     • μ = posición del punto                              │
│     • Σ = escala basada en densidad de vecinos            │
│     • c = color promedio de imágenes visibles             │
│     • o = opacidad inicial (0.1)                          │
├──────────────────────────────────────────────────────────┤
│  2. Densificación (cada 100 steps)                        │
│     • Clonar gaussianas con error > threshold             │
│     • Duplicar gaussianas con gradiente > threshold       │
│     • Reset opacidad de clonados a 0.005                  │
├──────────────────────────────────────────────────────────┤
│  3. Renderizado (por batch)                               │
│     • Proyectar gaussianas a 2D (Jacobiana de Σ)         │
│     • Ordenar por profundidad                              │
│     • Splatting: pintar gaussianas en framebuffer        │
│     • Alpha blending diferenciable                        │
├──────────────────────────────────────────────────────────┤
│  4. Loss y optimización                                   │
│     • L1 loss (color) + λ·SSIM loss                      │
│     • Adam optimizer (lr=1.6e-4 inicial)                 │
│     • Densificación cada 100 steps × 3000 steps           │
└──────────────────────────────────────────────────────────┘
```

### 3.4 Implementación — 3D Gaussian Splatting Core

```python
"""
3D Gaussian Splatting — implementación core
Paper: Kerbl et al., SIGGRAPH 2023
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class Gaussian3D:
    """
    Representación de una gaussiana 3D con parámetros optimizables.
    
    Parámetros:
        position: (3,) — centro de la gaussiana
        scale: (3,) — escala en cada eje (log-space)
        rotation: (4,) — cuaternión (w, x, y, z)
        opacity: (1,) — opacidad (sigmoid de valor aprendible)
        sh_coeffs: (K, 3) — coeficientes de spherical harmonics
    """
    def __init__(self, position, scale, rotation, opacity, sh_coeffs):
        self.position = position  # Optimizable
        self.scale = scale  # Optimizable (log-space)
        self.rotation = rotation  # Optimizable (cuaternión)
        self.opacity = opacity  # Optimizable (sigmoid)
        self.sh_coeffs = sh_coeffs  # Optimizable

    def get_covariance(self, device):
        """
        Construir matriz de covarianza 3x3 a partir de scale y rotation.
        
        Σ = R · S · S^T · R^T
        
        Donde S = diag(scale) y R es la matriz de rotación del cuaternión.
        """
        # Escala
        S = torch.diag_embed(torch.exp(self.scale))  # (3, 3)
        
        # Rotación desde cuaternión
        R = self._quaternion_to_rotation(self.rotation)  # (3, 3)
        
        # Covarianza: R · S · S^T · R^T
        cov = R @ S @ S.T @ R.T
        
        return cov

    @staticmethod
    def _quaternion_to_rotation(q):
        """Convertir cuaternión (w, x, y, z) a matriz de rotación 3x3."""
        w, x, y, z = q.unbind(-1)
        return torch.stack([
            1 - 2*(y**2 + z**2),  2*(x*y - z*w),      2*(x*z + y*w),
            2*(x*y + z*w),        1 - 2*(x**2 + z**2), 2*(y*z - x*w),
            2*(x*z - y*w),        2*(y*z + x*w),       1 - 2*(x**2 + y**2),
        ], dim=0).T

    def evaluate(self, point):
        """
        Evaluar la densidad de la gaussiana en un punto.
        
        G(x) = exp(-0.5 · (x-μ)^T · Σ^(-1) · (x-μ))
        """
        diff = point - self.position  # (3,)
        cov = self.get_covariance(point.device)
        cov_inv = torch.linalg.inv(cov)  # (3, 3)
        
        exponent = -0.5 * diff @ cov_inv @ diff
        density = torch.exp(exponent)
        
        return density


class GaussianRasterizer:
    """
    Rasterizador de gaussianas 3D a framebuffer 2D.
    
    Implementa el "splatting" diferenciable:
    1. Proyectar gaussianas 3D a 2D usando Jacobiana de la proyección
    2. Ordenar por profundidad
    3. Pintar en orden con alpha blending
    """
    
    @staticmethod
    def project_gaussians(gaussians, view_matrix, proj_matrix, image_width, image_height, camera_angle_x):
        """
        Proyectar gaussianas 3D a coordenadas de imagen.
        
        Args:
            gaussians: dict con positions (N,3), covariances (N,3,3), etc.
            view_matrix: (4,4) — matriz de vista (world → camera)
            proj_matrix: (4,4) — matriz de proyección
            image_width, image_height: dimensiones de imagen
            camera_angle_x: ángulo horizontal de la cámara (radianes)
        
        Returns:
            projected: (N, 2) — coordenadas 2D de centros
            radii: (N,) — radios de las gaussianas proyectadas
            conics: (N, 3, 3) — conica inversa para rasterizado
            depths: (N,) — profundidades en cámara
        """
        positions = gaussians['positions']  # (N, 3)
        cov3D = gaussians['cov3D']  # (N, 3, 3)
        
        # Transformar a coordenadas de cámara
        cam_pos = torch.inverse(view_matrix)[:3, 3]  # Posición cámara en world
        view_dir = positions - cam_pos  # (N, 3)
        
        # Profundidad (z en espacio de cámara)
        depths = view_dir @ view_matrix[:2, :2] @ view_matrix[:2, 3]
        
        # Proyección perspectiva
        fx = image_width / (2 * torch.tan(camera_angle_x / 2))
        fy = image_height / (2 * torch.tan(camera_angle_x / 2))
        
        proj = torch.tensor([
            [fx, 0, 0, 0],
            [0, fy, 0, 0],
            [0, 0, 0, 0],
            [0, 0, -1, 0],
        ], device=positions.device)
        
        # Transformar covarianza al espacio de cámara
        W = view_matrix[:3, :3]
        cov_cam = (W @ cov3D @ W.transpose(-1, -2))
        
        # Jacobiana de la proyección
        J = torch.zeros_like(proj)
        J[0, 0] = fx
        J[1, 1] = fy
        J[2, 2] = -1
        
        # Covarianza proyectada (2D)
        T = J @ view_matrix[:3, :3]
        cov2D = T @ cov3D @ T.transpose(-1, -2)
        
        # Asegurar positividad (regularización)
        cov2D[..., 0, 0] += 0.3
        cov2D[..., 1, 1] += 0.3
        
        # Inversa de la covarianza 2D (para el splatting)
        conics = torch.linalg.inv(cov2D)  # (N, 2, 2)
        
        # Centroides proyectados
        projected = proj @ torch.cat([positions, torch.ones_like(positions[:, :1])], dim=-1).unsqueeze(-1)
        projected = projected.squeeze(-1)[:, :2] / (-projected[:, 2:3] + 1e-6)
        
        # Radios aproximados (2σ)
        trace = cov2D[..., 0, 0] + cov2D[..., 1, 1]
        discriminant = trace**2 - 4 * cov2D[..., 0, 0] * cov2D[..., 1, 1]
        discriminant = torch.clamp(discriminant, min=0)
        eigenvalues = 0.5 * (trace + torch.sqrt(discriminant))
        radii = (2.0 * torch.sqrt(eigenvalues)).int()
        
        return projected, radii, conics, depths

    @staticmethod
    def rasterize_gaussians(image_width, image_height, projected, radii, conics, 
                             depths, opacities, colors):
        """
        Rasterizar gaussianas proyectadas al framebuffer.
        
        Algoritmo:
        1. Para cada gaussiana, determinar bounding box en píxeles
        2. Para cada píxel en el bounding box, evaluar la gaussiana 2D
        3. Acumular con alpha blending en orden de profundidad
        
        Args:
            image_width, image_height: dimensiones
            projected: (N, 2) — centros 2D
            radii: (N,) — radios
            conics: (N, 2, 2) — conicas inversas
            depths: (N,) — profundidades (para ordenar)
            opacities: (N, 1) — opacidades
            colors: (N, 3) — colores
        
        Returns:
            color: (H, W, 3) — framebuffer RGB
            alpha: (H, W, 1) — framebuffer alpha
        """
        # Ordenar por profundidad (far to near)
        order = torch.argsort(depths, descending=True)
        projected = projected[order]
        radii = radii[order]
        conics = conics[order]
        depths = depths[order]
        opacities = opacities[order]
        colors = colors[order]
        
        N = projected.shape[0]
        color = torch.zeros(image_height, image_width, 3, device=projected.device)
        alpha = torch.zeros(image_height, image_width, 1, device=projected.device)
        
        # Para cada gaussiana (ordenada por profundidad)
        for i in range(N):
            center = projected[i]  # (2,)
            radius = radii[i].item()
            conic = conics[i]  # (2, 2)
            opacity = opacities[i]  # (1,)
            color_i = colors[i]  # (3,)
            
            # Bounding box
            x_min = max(0, int(center[0] - radius))
            x_max = min(image_width, int(center[0] + radius + 1))
            y_min = max(0, int(center[1] - radius))
            y_max = min(image_height, int(center[1] + radius + 1))
            
            # Evaluar en cada píxel del bounding box
            grid_x = torch.arange(x_min, x_max, device=projected.device)
            grid_y = torch.arange(y_min, y_max, device=projected.device)
            xx, yy = torch.meshgrid(grid_x, grid_y, indexing='ij')
            
            # Vector desde centro
            dx = (xx.float() - center[0]).unsqueeze(-1)  # (H_box, W_box, 1)
            dy = (yy.float() - center[1]).unsqueeze(-1)
            
            # Evaluar gaussiana 2D: exp(-0.5 · x^T · C · x)
            # C = conic = Σ^(-1)
            exponent = -0.5 * (
                dx**2 * conic[0, 0] + 
                2 * dx * dy * conic[0, 1] + 
                dy**2 * conic[1, 1]
            ).squeeze(-1)  # (H_box, W_box)
            
            # Alpha de esta gaussiana en cada píxel
            pixel_alpha = torch.exp(exponent) * opacity  # (H_box, W_box)
            
            # Alpha blending
            # color_nuevo = color_antiguo + pixel_alpha * (color_gaussiana - color_antiguo)
            new_color = color[y_min:y_max, x_min:x_max]
            new_alpha = alpha[y_min:y_max, x_min:x_max]
            
            contribution = pixel_alpha.unsqueeze(-1) * (color_i - new_color)
            
            color[y_min:y_max, x_min:x_max] += contribution
            alpha[y_min:y_max, x_min:x_max] += pixel_alpha.unsqueeze(-1) * (1.0 - new_alpha)
        
        return color, alpha


class SphericalHarmonics:
    """
    Coeficientes de Spherical Harmonics para color dependiente de vista.
    
    NeRF usa dirección de vista para colorear. 3DGS usa SH de grado 0-3
    (45 coeficientes por canal) para capturar reflectancia anisotrópica.
    
    Para grado 0 (usado en 3DGS base): 3 coeficientes por canal RGB
    c = SH_0 · d^0 = SH_0 (constante)
    
    Para grado 1: 12 coeficientes por canal
    c = SH_0 + SH_1 · d  (d = dirección normalizada)
    """
    
    @staticmethod
    def evaluate_sh(sh_coeffs, direction, degree=0):
        """
        Evaluar spherical harmonics en una dirección dada.
        
        Args:
            sh_coeffs: (N, K, 3) — coeficientes SH por gaussiana
            direction: (N, 3) — dirección normalizada
            degree: grado SH (0-3)
        Returns:
            color: (N, 3) — color en la dirección dada
        """
        # Normalizar dirección
        direction = F.normalize(direction, dim=-1)
        
        if degree == 0:
            # Solo coeficientes constantes
            return sh_coeffs[:, 0]  # (N, 3)
        
        elif degree == 1:
            # SH grado 0 + grado 1
            x, y, z = direction.unbind(-1)
            
            # Grado 0: constante
            sh0 = sh_coeffs[:, 0]  # (N, 3)
            
            # Grado 1: 3 funciones base
            # f1 = -y, f2 = z, f3 = -x
            sh1 = sh_coeffs[:, 1:4]  # (N, 3, 3)
            bases = torch.stack([-y, z, -x], dim=-1)  # (N, 3)
            sh1_val = torch.sum(sh1 * bases.unsqueeze(-1), dim=-2)  # (N, 3)
            
            return sh0 + sh1
        
        elif degree == 3:
            # Grado completo (15 coeficientes por canal)
            x, y, z = direction.unbind(-1)
            
            # Funciones base para grados 0-3
            # Grado 0: 1
            # Grado 1: y, z, x  (3)
            # Grado 2: yz, xz, x²-y², xy, z²  (5)
            # Grado 3: y(3x²-y²), y(5z²-r²), x(5z²-r²), xyz, x(x²-3y²), z(2z²-3x²-3y²)  (7)
            
            r2 = x**2 + y**2 + z**2
            
            bases_0 = torch.ones_like(x)
            bases_1 = torch.stack([y, z, x], dim=-1)
            bases_2 = torch.stack([y*z, x*z, x**2-y**2, x*y, 0.5*(3*z**2-r2)], dim=-1)
            bases_3 = torch.stack([
                y*(3*x**2-y**2),
                y*(5*z**2-r2),
                x*(5*z**2-r2),
                x*y*z,
                x*(x**2-3*y**2),
                z*(2*z**2-x**2-y**2)
            ], dim=-1)
            
            all_bases = torch.cat([
                bases_0.unsqueeze(-1),
                bases_1,
                bases_2,
                bases_3
            ], dim=-1)  # (N, 16)
            
            # sh_coeffs: (N, 16, 3)
            color = torch.sum(sh_coeffs * all_bases.unsqueeze(-1), dim=-2)
            
            # Clamp a [0, 1]
            return torch.clamp(color + 0.5, 0.0, 1.0)


class GaussianScene:
    """
    Escena de gaussianas 3D completa.
    
    Gestiona la lista de gaussianas, densificación y renderizado.
    """
    def __init__(self, point_cloud_path=None):
        self.gaussians = []
        self.num_gaussians = 0
        
        if point_cloud_path:
            self._initialize_from_point_cloud(point_cloud_path)
    
    def _initialize_from_point_cloud(self, path):
        """
        Inicializar gaussianas a partir de punto nube SfM (COLMAP).
        
        Cada punto SfM se convierte en una gaussiana 3D con:
        - position = posición del punto
        - scale = basada en densidad local
        - rotation = identidad (o alineada con normales)
        - opacity = valor inicial bajo
        - sh_coeffs = color promedio de las imágenes donde es visible
        """
        # Cargar punto nube (formato .ply de COLMAP)
        # ... implementación simplificada ...
        pass
    
    def densify(self, grad_threshold=0.0001, min_opacity=0.005, step=0):
        """
        Densificación adaptativa de gaussianas.
        
        Cada 100 steps:
        1. Clonar gaussianas con gradiente > threshold
        2. Duplicar gaussianas con posición en regiones densas
        3. Resetear opacidad de clonados
        4. Eliminar gaussianas con opacidad < threshold
        """
        if step % 100 != 0:
            return
        
        # Obtener gradientes de posición
        grads = torch.norm(self.positions.grad, dim=-1)  # (N,)
        
        # Clonar gaussianas con alto gradiente
        clone_mask = grads > grad_threshold
        n_clones = clone_mask.sum().item()
        
        if n_clones > 0:
            # Clonar posiciones, escalas, rotaciones
            new_positions = self.positions[clone_mask].clone()
            # Añadir ruido a los clones para diversidad
            new_positions += torch.randn_like(new_positions) * 0.001
            
            # Resetear opacidad
            new_opacities = torch.full((n_clones, 1), min_opacity, device=self.opacities.device)
            
            # Concatenar
            self.positions = torch.cat([self.positions, new_positions])
            self.opacities = torch.cat([self.opacities, new_opacities])
            # ... (más parámetros)
    
    def prune(self, opacity_threshold=0.005):
        """Eliminar gaussianas con opacidad muy baja."""
        keep = self.opacities.squeeze(-1) > opacity_threshold
        # ... filtrar todos los parámetros ...
        self.num_gaussians = keep.sum().item()
    
    def render(self, camera_params):
        """
        Renderizar la escena desde la cámara actual.
        
        Args:
            camera_params: dict con view_matrix, proj_matrix, etc.
        Returns:
            color: (H, W, 3) — imagen renderizada
        """
        # 1. Proyectar gaussianas
        projected, radii, conics, depths = GaussianRasterizer.project_gaussians(
            {
                'positions': self.positions,
                'cov3D': self.cov3D,
            },
            camera_params['view_matrix'],
            camera_params['proj_matrix'],
            camera_params['width'],
            camera_params['height'],
            camera_params['angle_x'],
        )
        
        # 2. Evaluar colores con SH
        direction = self.positions - camera_params['camera_position']
        colors = SphericalHarmonics.evaluate_sh(
            self.sh_coeffs, direction, degree=self.sh_degree
        )
        
        # 3. Rasterizar
        color, alpha = GaussianRasterizer.rasterize_gaussians(
            camera_params['width'],
            camera_params['height'],
            projected, radii, conics, depths,
            self.opacities, colors,
        )
        
        return color


# === Ejemplo de uso ===
if __name__ == "__main__":
    # Crear escena con 1000 gaussianas
    scene = GaussianScene()
    
    # Inicialización (simplificada)
    N = 1000
    scene.num_gaussians = N
    scene.positions = torch.randn(N, 3) * 2.0  # (N, 3)
    scene.scales = torch.zeros(N, 3)  # (N, 3)
    scene.rotations = torch.zeros(N, 4)
    scene.rotations[:, 0] = 1.0  # Identidad
    scene.opacities = torch.full((N, 1), 0.1)
    scene.sh_coeffs = torch.randn(N, 1, 3)  # Grado 0
    scene.sh_degree = 0
    
    # Calcular covarianzas
    scene.cov3D = torch.stack([
        g.get_covariance(scene.positions.device)
        for g in [type('G', (), {
            'position': scene.positions[i],
            'scale': scene.scales[i],
            'rotation': scene.rotations[i]
        })() for i in range(N)]
    ])
    
    print(f"Escena: {N} gaussianas 3D")
    print(f"Posiciones: {scene.positions.shape}")
    print(f"Covarianzas: {scene.cov3D.shape}")
    
    # Renderizar desde cámara
    camera = {
        'view_matrix': torch.eye(4),
        'proj_matrix': torch.eye(4),
        'width': 512,
        'height': 512,
        'angle_x': 1.0,
        'camera_position': torch.tensor([0, 0, 5.0]),
    }
    
    color = scene.render(camera)
    print(f"Imagen renderizada: {color.shape}")  # (512, 512, 3)
```

---

## 4. Comparativa Técnica Detallada

### 4.1 Complejidad Computacional

| Operación | NeRF | 3DGS |
|-----------|------|------|
| Training | O(N·M·D) donde N=rayos, M=samples, D=MLP depth | O(N·G) donde G=gaussians por píxel |
| Inference | Ray marching (128-1024 muestras/ray) | Splatting (50-200 gaussianas/píxel) |
| Memoria | ~10MB (MLP weights) | ~2-8GB (lista de gaussianas) |
| FPS | 0.01-1 fps (CPU/GPU) | 30-200+ fps (GPU) |

### 4.2 Evolución Reciente (2024-2025)

1. **Gaussian Avatars** (2023): 3DGS para personajes animados
2. **4D Gaussian Splatting** (2024): extensión a video/secuencias temporales
3. **Splatting in the Wild** (2024): entrenar con imágenes de internet (no SfM)
4. **NeRF-W / Mega-NeRF** (2022-2023): NeRF a escala ciudad
5. **Zip-NeRF** (2023): compresión 8x con codificación de frecuencia
6. **PlenOctrees** (2023): representación híbrida octree + NeRF

---

## 5. Aplicaciones Prácticas

1. **Reconstrucción 3D para AR/VR** — 3DGS permite rendering en tiempo real
2. **Patrimonio cultural** — Digitalización de sitios históricos
3. **Telepresencia** — Captura de escenas 3D para comunicación remota
4. **Robótica** — SLAM con 3DGS (SplatAM) para navegación
5. **Cine y VFX** — Captura de escenas reales para producción
6. **E-commerce** — Productos 360° a partir de fotos

---

## 6. Recursos Clave

### Papers
- [NeRF](https://arxiv.org/abs/2003.08934) — Mildenhall et al., ECCV 2020
- [3D Gaussian Splatting](https://arxiv.org/abs/2308.04079) — Kerbl et al., SIGGRAPH 2023
- [InstantNGP](https://arxiv.org/abs/2201.05987) — Müller et al., SIGGRAPH 2022
- [Zip-NeRF](https://arxiv.org/abs/2304.06706) — Antos et al., 2023
- [4D Gaussian Splatting](https://arxiv.org/abs/2310.08530) — Lu et al., 2023

### Repositorios
- [bmild/nerf](https://github.com/bmild/nerf) — NeRF original
- [NVlabs/instant-ngp](https://github.com/NVlabs/instant-ngp) — InstantNGP
- [graphdeco-inria/gaussian-splatting](https://github.com/graphdeco-inria/gaussian-splatting) — 3DGS official
- [nerfstudio-project/nerfstudio](https://github.com/nerfstudio-project/nerfstudio) — Framework modular
- [nerfstudio-project/gsplat](https://github.com/nerfstudio-project/gsplat) — Differentiable splatting GPU

### Datasets
- [Blender](https://github.com/bmild/nerf/tree/master/data_blender) — Escenas sintéticas
- [LLFF](http://grail.cs.washington.edu/projects/llff/) — Fotos de paisaje
- [DTU](https://www.doc.ic.ac.uk/~ahanda/dataset.html) — Escaneos médicos/industriales
- [Tanks & Temples](https://www.tanksandtemples.org/) — Escenas grandes

---

## 7. Lecciones Clave

1. **NeRF revolucionó la view synthesis** pero era demasiado lento para aplicaciones en tiempo real
2. **3DGS resolvió el bottleneck de inferencia** manteniendo calidad comparable
3. **La densificación adaptativa** es clave: empezar con pocos gaussianos y crecer durante el training
4. **Spherical Harmonics** permiten capturar reflectancia dependiente del ángulo de vista
5. **El trade-off memoria/calidad** es fundamental: NeRF usa MB, 3DGS usa GB
6. **El futuro es híbrido**: representar la escena de forma compacta (octrees, hashing) + renderizado eficiente (splatting)

---

*Próximo tema propuesto: [ver sección 8]*
