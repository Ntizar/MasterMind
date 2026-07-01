# Normalizing Flows: De Density Estimation a Flow Matching

> **Fecha:** 2026-07-01
> **Categoría:** Deep Learning → Modelos Generativos
> **Nivel:** Intermedio-Avanzado

---

## 1. Concepto Fundamental

Un **Normalizing Flow** es una transformación invertible y diferenciable $z = f_\theta(x)$ que mapea una distribución simple (prior) $p_z$ a una distribución compleja $p_x$:

$$p_x(x) = p_z(f_\theta(x)) \left| \det \frac{\partial f_\theta(x)}{\partial x} \right|^{-1}$$

El término clave es el **log-determinante jacobiano** (log-det-Jacobian):

$$\log p_x(x) = \log p_z(z) - \log \left| \det \frac{\partial f}{\partial x} \right|$$

### ¿Por qué son especiales?

| Propiedad | Descripción |
|-----------|-------------|
| **Likelihood exacto** | No requiere variational bound ni MCMC |
| **Inferencia exacta** | $q(z|x)$ se puede calcular analíticamente |
| **Sampling perfecto** | $x = f^{-1}(z)$ donde $z \sim p_z$ |
| **Invertible** | $x = f^{-1}(z)$ sin aproximaciones |

**El reto:** Calcular $\log |\det J|$ es $O(d^3)$ para matrices densas de dimensión $d$. Los flows usan estructuras especiales para hacerlo $O(d)$.

---

## 2. Evolución Histórica

### 2.1 NICE (Dinh et al., 2014)

Primera propuesta. Usa una descomposición aditiva con maskings:

$$z_i = x_i + \mathcal{N}(x_{j<i}) \quad \text{o} \quad z_i = x_i + \mathcal{N}(x_{j>i})$$

El Jacobiano es triangular → determinante = producto de diagonales = 1.

**Limitación:** Solo modela covarianzas de orden 1, no correlaciones complejas.

### 2.2 RealNVP (Dinh et al., 2017)

Mejora NICE con transformaciones **invertibles por bloques** (coupling layers):

```python
def real_nvp_coupling(x, s_t, net):
    """RealNVP coupling layer.
    
    Args:
        x: input tensor [batch, dim]
        s_t: tuple (scale, shift) from neural net
        net: neural network taking half-dim -> 2*half_dim (scale + shift)
    
    Returns:
        z: output tensor [batch, dim]
    """
    x1, x2 = x[:, :dim//2], x[:, dim//2:]
    
    # Net takes x1 and produces scale+shift for x2
    s, t = net(x1)  # [batch, dim//2], [batch, dim//2]
    
    # Invertible transformation
    z1 = x1  # identity for first half
    z2 = (x2 - t) * torch.exp(s)  # affine scaling
    
    return torch.cat([z1, z2], dim=-1)
```

**Log-det simplificado:** $\log |\det J| = \sum \log |s(x_1)|$ → $O(d)$ en vez de $O(d^3)$.

### 2.3 GLOW (Kingma & Dhariwal, 2018)

Añade dos ingredientes clave:

1. **1x1 convoluciones invertibles** — mezcla canales antes del coupling
2. **Invertible 1x1 conv** — matriz $W$ tal que $\det(W)$ se puede calcular eficientemente

```python
class Invertible1x1Conv(nn.Module):
    """Invertible 1x1 convolution using QR decomposition."""
    
    def __init__(self, dim):
        super().__init__()
        # Start with random orthogonal matrix
        W = torch.tensor(np.random.randn(dim, dim))
        Q, _ = torch.qr(W)
        # Ensure det > 0 for invertibility
        if torch.det(Q) < 0:
            Q[:, 0] = -Q[:, 0]
        self.Q = nn.Parameter(Q)
    
    def forward(self, x):
        # x: [batch, channels, height, width]
        W = self.Q
        log_det = torch.log(torch.abs(W).det())
        
        # Apply convolution
        B, C, H, W_dim = x.shape
        x_flat = x.permute(0, 2, 3, 1).reshape(B * H * W_dim, C)
        z_flat = x_flat @ W.T
        z = z_flat.reshape(B, H, W_dim, C).permute(0, 3, 1, 2)
        
        return z, log_det
    
    def invert(self, z):
        W = self.Q
        W_inv = W.inverse()
        B, C, H, W_dim = z.shape
        z_flat = z.permute(0, 2, 3, 1).reshape(B * H * W_dim, C)
        x_flat = z_flat @ W_inv.T
        x = x_flat.reshape(B, H, W_dim, C).permute(0, 3, 1, 2)
        return x
```

### 2.4 Neural Spline Flows (Durkan et al., 2019) — **CDFLows**

Usa **Rational Quadratic Splines** para hacer las transformaciones **monotónicas y aprendibles**.

```python
class RationalQuadraticSpline(nn.Module):
    """Rational quadratic spline coupling layer.
    
    Key idea: Learn a monotonic transformation by parameterizing
    the derivatives at knots, then integrate to get the CDF.
    
    This gives much more expressive flows than affine coupling.
    """
    
    def __init__(self, n_bins=8, tail_bound=3.0):
        super().__init__()
        self.n_bins = n_bins
        self.tail_bound = tail_bound
        
        # For each bin: width (positive), height (positive), derivative (positive)
        self.bin_widths = nn.Parameter(torch.ones(n_bins))
        self.bin_heights = nn.Parameter(torch.ones(n_bins))
        self.bin_derivatives = nn.Parameter(torch.ones(n_bins + 1))
    
    def forward(self, x):
        """Forward and log determinant."""
        # Normalize to [-tail_bound, tail_bound]
        x_norm = torch.tanh(x / self.tail_bound) * self.tail_bound
        
        # Compute cumulative sums for bin positions and heights
        width_cum = torch.cumsum(
            F.pad(self.bin_widths, (1, 0)), dim=0
        )
        height_cum = torch.cumsum(
            F.pad(self.bin_heights, (1, 0)), dim=0
        )
        deriv_cum = torch.cumsum(
            F.pad(self.bin_derivatives, (1, 0)), dim=0
        )
        
        # Find which bin each x falls into
        bin_idx = torch.searchsorted(width_cum[:-1], x_norm)
        
        # Get bin parameters
        w = width_cum[bin_idx]
        h = height_cum[bin_idx]
        d_left = deriv_cum[bin_idx]
        d_right = deriv_cum[bin_idx + 1]
        
        # Rational quadratic spline evaluation
        # ... (full implementation in nflows library)
        
        return y, log_det
```

**Ventaja:** Las splines racionales pueden aproximar cualquier distribución continua con error arbitrario (teorema de aproximación universal para flows).

### 2.5 FFJORD (Grathwohl et al., 2018) — **Continuous Normalizing Flows**

En vez de una composición discreta de transformaciones, usa una **EDO continua**:

$$\frac{dz(t)}{dt} = f(z(t), t, \theta), \quad t \in [0, 1]$$

El log-det se calcula con **trace estimator** (Hutchinson's trace):

$$\log |\det J(1)| = \int_0^1 \text{Tr}\left(\frac{\partial f}{\partial z}(z(t), t)\right) dt$$

```python
class NeuralODE(nn.Module):
    """Continuous Normalizing Flow using Neural ODE solver.
    
    z(1) = z(0) + ∫₀¹ f(z(t), t, θ) dt
    
    Uses adjoint method for memory-efficient backprop.
    """
    
    def __init__(self, net, solver='dopri5'):
        super().__init__()
        self.net = net  # Neural network: (z, t) -> dz/dt
        self.solver = solver
    
    def forward(self, z0, log_det_jac=True):
        """Forward pass: z0 ~ p(z) -> z1 ~ p(x).
        
        Args:
            z0: initial latent [batch, dim]
            log_det_jac: whether to compute log-det Jacobian
        
        Returns:
            z1: transformed sample
            log_det: log determinant of Jacobian
        """
        from torchdiffeq import odeint
        
        def ode_func(t, z):
            # z shape: [batch*dim, 1] for odeint
            z_reshaped = z.reshape(-1, self.net.dim)
            dzdt = self.net(z_reshaped, t)
            return dzdt.reshape(-1, 1)
        
        ts = torch.tensor([0.0, 1.0])
        solution = odeint(ode_func, z0, ts, method=self.solver)
        z1 = solution[1]  # z at t=1
        
        log_det = self._compute_log_det(z0, z1) if log_det_jac else 0.0
        
        return z1, log_det
    
    def _compute_log_det(self, z0, z1):
        """Hutchinson's trace estimator for log-det Jacobian."""
        # log |det J| ≈ E[εᵀ J ε] where ε ~ N(0, I)
        eps = torch.randn_like(z0)
        # Jacobian-vector product
        grads = torch.autograd.grad(
            z1.sum(), z0, create_graph=True, retain_graph=True
        )[0]
        trace = (eps * grads).sum(dim=-1)
        return trace
```

### 2.6 Flow Matching (Lipman et al., 2023; Tong et al., 2023) — **Estado del Arte 2024-2026**

La evolución natural de los flows: en vez de forzar invertibilidad, aprende un **campo de flujo vectorial** que transporta la distribución prior a la data:

$$\frac{dx_t}{dt} = v_t(x_t)$$

Donde $v_t$ se entrena con **Conditional Flow Matching** (CFM):

$$\mathcal{L}(\theta) = \mathbb{E}_{t, x_0, x_1} \left[ \| v_t(x_t, t) - v^*(x_t | x_0, x_1) \|^2 \right]$$

La velocidad objetivo $v^*$ tiene solución cerrada para transportes lineales (rectified flow):

$$x_t = (1-t)x_0 + t x_1$$

**Conexión con Diffusion:** Flow matching es conceptualmente similar a score-based diffusion pero con:
- **Sampling más rápido** (menos pasos, ODE directo)
- **Training más estable** (no requiere annealing de ruido)
- **Traectorias más rectas** (menos curvas que diffusion)

---

## 3. Implementación Práctica Completa

### 3.1 RealNVP con PyTorch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class MaskedLinear(nn.Module):
    """Masked linear layer for RealNVP coupling."""
    
    def __init__(self, in_dim, out_dim, half=True):
        super().__init__()
        self.fc = nn.Linear(in_dim, out_dim)
        
        # Create mask: first half gets 0, second half gets 1 (or vice versa)
        mask = torch.zeros(out_dim, in_dim)
        if half:
            mask[:, :in_dim//2] = 1.0  # second half depends on first half
        else:
            mask[:, in_dim//2:] = 1.0  # first half depends on second half
        
        self.register_buffer('mask', mask)
    
    def forward(self, x):
        return self.fc(x) * self.mask


class CouplingLayer(nn.Module):
    """RealNVP coupling layer with affine transformation."""
    
    def __init__(self, dim, hidden_dim=128):
        super().__init__()
        half_dim = dim // 2
        
        # Network for scale (s) and shift (t)
        self.net = nn.Sequential(
            MaskedLinear(half_dim, hidden_dim, half=True),
            nn.ReLU(),
            MaskedLinear(hidden_dim, hidden_dim, half=False),
            nn.ReLU(),
            MaskedLinear(hidden_dim, half_dim * 2, half=False),
        )
    
    def forward(self, x, log_det_jac=None):
        x1, x2 = x[:, :self.dim//2], x[:, self.dim//2:]
        
        # Generate scale and shift from x1
        params = self.net(x1)  # [batch, dim//2 * 2]
        s = params[:, :self.dim//2]
        t = params[:, self.dim//2:]
        
        # Apply inverse transformation for sampling
        # z2 = (x2 - t) / (1 + eps) * exp(s)  →  x2 = t + z2 * exp(s)
        # For likelihood: x2 = t + z2 * exp(s)
        # For sampling: z2 = (x2 - t) * exp(-s)
        
        # Forward (for likelihood computation): x -> z
        z2 = (x2 - t) * torch.exp(-s)
        z1 = x1
        
        # Log determinant: sum of -s for each dimension
        log_det = -s.sum(dim=-1)
        
        z = torch.cat([z1, z2], dim=-1)
        
        if log_det_jac is not None:
            log_det_jac.add_(log_det)
        
        return z
    
    def sample(self, z):
        """Sample from the flow: z -> x."""
        z1, z2 = z[:, :self.dim//2], z[:, self.dim//2:]
        
        params = self.net(z1)
        s = params[:, :self.dim//2]
        t = params[:, self.dim//2:]
        
        x2 = t + z2 * torch.exp(s)
        x1 = z1
        
        return torch.cat([x1, x2], dim=-1)


class RealNVP(nn.Module):
    """RealNVP model with multiple coupling layers.
    
    Architecture:
    - K coupling layers (alternating masks)
    - Invertible 1x1 conv between blocks (optional, from GLOW)
    - Gaussian prior
    """
    
    def __init__(self, dim, n_coupling_layers=6, hidden_dim=128):
        super().__init__()
        self.dim = dim
        self.n_coupling_layers = n_coupling_layers
        
        # Alternating coupling layers
        self.coupling_layers = nn.ModuleList([
            CouplingLayer(dim, hidden_dim) 
            for _ in range(n_coupling_layers)
        ])
    
    def forward(self, x, log_det_jac=None):
        """Compute log-likelihood of x under the model.
        
        Args:
            x: data points [batch, dim]
            log_det_jac: accumulator for log-det Jacobian
        
        Returns:
            log_prob: log probability of x
            z: transformed latent
        """
        if log_det_jac is None:
            log_det_jac = torch.zeros(x.shape[0], device=x.device)
        
        z = x
        for layer in self.coupling_layers:
            z = layer(z, log_det_jac)
        
        # Log probability under standard normal prior
        log_pz = self._gaussian_log_prob(z)
        log_px = log_pz + log_det_jac
        
        return log_px, z
    
    def _gaussian_log_prob(self, z):
        """Log probability under standard normal."""
        log_p = -0.5 * z.pow(2) - 0.5 * np.log(2 * np.pi)
        return log_p.sum(dim=-1)
    
    @torch.no_grad()
    def sample(self, n_samples=100):
        """Sample from the model."""
        z = torch.randn(n_samples, self.dim)
        x = z
        for layer in reversed(self.coupling_layers):
            x = layer.sample(x)
        return x
    
    @torch.no_grad()
    def log_likelihood(self, x, n_mc=1):
        """Estimate log-likelihood with MC sampling."""
        log_probs = []
        for _ in range(n_mc):
            log_prob, _ = self(x)
            log_probs.append(log_prob)
        return torch.stack(log_probs).mean(dim=0)


# === Training Loop ===
def train_realnvp(model, dataloader, n_epochs=100, lr=1e-3):
    """Train RealNVP on a dataset."""
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    
    for epoch in range(n_epochs):
        for x_batch, _ in dataloader:
            # Forward pass
            log_prob, _ = model(x_batch)
            
            # Negative log-likelihood loss
            nll = -log_prob.mean()
            
            # Backward pass
            optimizer.zero_grad()
            nll.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            optimizer.step()
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch}: NLL = {nll.item():.4f}")


# === Example: 2D Moons Dataset ===
if __name__ == "__main__":
    from sklearn.datasets import make_moons
    
    # Generate 2D data
    X, _ = make_moons(n_samples=5000, noise=0.1, random_state=42)
    X = (X - X.mean(axis=0)) / X.std(axis=0)  # Standardize
    
    X_tensor = torch.FloatTensor(X)
    
    # Create and train model
    model = RealNVP(dim=2, n_coupling_layers=8, hidden_dim=64)
    
    from torch.utils.data import TensorDataset, DataLoader
    loader = DataLoader(TensorDataset(X_tensor), batch_size=256, shuffle=True)
    
    train_realnvp(model, loader, n_epochs=50, lr=3e-4)
    
    # Sample from the model
    samples = model.sample(2000)
    print(f"Sampled {samples.shape[0]} samples from the flow")
    print(f"Sample mean: {samples.mean(dim=0).detach().numpy()}")
    print(f"Sample std: {samples.std(dim=0).detach().numpy()}")
```

### 3.2 Neural Spline Flow con `nflows`

```python
# pip install nflows
from nflows.distributions.normal import StandardNormal
from nflows.flows.base import Flow
from nflows.transforms.autoregressive import MaskedAffineAutoregressiveTransform
from nflows.transforms.base import CompositeTransform
from nflows.transforms.permutations import ReversePermutation
from nflows.distributions import DiagonalNormal
from nflows.nn import nets
import nflows

# Using the high-level API
flow = nflows.flows.MaskedAffineFlow(
    distribution=DiagonalNormal(input_shape=[784]),  # MNIST
    transform=nets.MaskedAffineAutoregressiveTransform(
        features=784,
        hidden_features=256,
        context_features=None,
        num_blocks=2,
        use_residual_blocks=True,
        random_mask=False,
        activation=torch.nn.functional.relu,
        dropout_probability=0.0,
        batch_normalization=True
    )
)

# Training
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Lambda(lambda x: x.view(-1))  # Flatten
])

train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)

# Compute log-likelihood
def compute_nll(flow, data_loader):
    total_log_prob = 0.0
    total_samples = 0
    with torch.no_grad():
        for batch, _ in data_loader:
            batch = batch.view(batch.size(0), -1)
            log_prob = flow.log_prob(batch)
            total_log_prob += (log_prob * batch.size(0)).sum().item()
            total_samples += batch.size(0)
    return -total_log_prob / total_samples

nll = compute_nll(flow, train_loader)
print(f"Negative log-likelihood: {nll:.4f}")
```

### 3.3 Flow Matching con `torchcfm`

```python
# pip install torchcfm
import torch
import torchcfm
from torchcfm.conditional_flow_matching import ConditionalFlowMatcher

# Conditional Flow Matcher (CFM)
cfm = ConditionalFlowMatcher(sigma=0.0)  # Rectified Flow (sigma=0)

# Define a simple neural network for the velocity field
class VelocityNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(2 + 1, 128),  # x + t concatenation
            torch.nn.ReLU(),
            torch.nn.Linear(128, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 2),       # velocity in 2D
        )
    
    def forward(self, t, x):
        """t: [batch], x: [batch, 2] -> velocity: [batch, 2]"""
        t_expanded = t.unsqueeze(-1)
        return self.net(torch.cat([t_expanded, x], dim=-1))

# Training loop for Flow Matching
velocity_net = VelocityNet()
optimizer = torch.optim.Adam(velocity_net.parameters(), lr=1e-3)

# Sample from data and prior
x0 = torch.randn(256, 2)  # prior (standard normal)
x1 = sample_from_data(256, 2)  # data samples

for step in range(1000):
    t = torch.rand(256)  # t ~ Uniform[0, 1]
    
    # Linear interpolation: xt = (1-t)*x0 + t*x1
    xt = (1 - t.unsqueeze(-1)) * x0 + t.unsqueeze(-1) * x1
    
    # Target velocity: v* = x1 - x0 (for linear OT)
    v_target = x1 - x0
    
    # Predicted velocity
    v_pred = velocity_net(t, xt)
    
    # CFM loss: MSE between predicted and target velocity
    loss = ((v_pred - v_target) ** 2).mean()
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if step % 100 == 0:
        print(f"Step {step}: Loss = {loss.item():.4f}")

# Sampling: solve ODE dx/dt = v_t(x)
from torchdiffeq import odeint

@torch.no_grad()
def sample_flow_matching(velocity_net, n_samples=1000, solver='euler', steps=50):
    """Sample from flow matching model by solving the ODE."""
    x0 = torch.randn(n_samples, 2)
    
    def ode_func(t, x):
        return velocity_net(t * torch.ones(1), x)
    
    ts = torch.linspace(0, 1, steps)
    solution = odeint(ode_func, x0, ts, method=solver)
    
    return solution[-1]  # x at t=1

samples = sample_flow_matching(velocity_net, n_samples=2000)
print(f"Generated {samples.shape[0]} samples via flow matching ODE")
```

---

## 4. Comparativa: Flows vs Diffusion vs GANs vs VAEs

| Característica | Normalizing Flows | Diffusion | GANs | VAEs |
|---------------|-------------------|-----------|------|------|
| **Likelihood** | ✅ Exacto | ❌ Aproximado | ❌ Ninguno | ❌ Variacional |
| **Sampling** | ✅ Directo (1 paso) | ❌ Iterativo (100-1000) | ✅ Directo | ✅ Directo |
| **Inferencia** | ✅ Exacta | ❌ Aproximada | ❌ Ninguna | ✅ Variacional |
| **Calidad** | Media | Alta | Alta | Media |
| **Escalabilidad** | Limitada (dim alta) | Alta | Alta | Alta |
| **Training estable** | ✅ Sí | ✅ Sí | ❌ Inestable | ✅ Sí |
| **Dimensión alta** | ❌ Difícil (>1000) | ✅ Excelente | ✅ Excelente | ✅ Bueno |

**Conclusión práctica:**
- **Flows** → Ideal para dimensiones medias (tabular, secuencias cortas, density estimation)
- **Diffusion** → Ideal para imágenes de alta resolución
- **Flow Matching** → El mejor de ambos mundos: calidad de diffusion + sampling rápido

---

## 5. Aplicaciones Prácticas

### 5.1 Density Estimation (Anomaly Detection)

```python
class AnomalyDetector:
    """Normalizing flow for anomaly detection.
    
    Train on normal data. Low likelihood → anomaly.
    """
    
    def __init__(self, dim, n_layers=8):
        self.flow = RealNVP(dim, n_coupling_layers=n_layers)
    
    def fit(self, normal_data, epochs=100, lr=1e-3):
        """Train on normal data only."""
        data = torch.FloatTensor(normal_data)
        loader = DataLoader(TensorDataset(data), batch_size=64, shuffle=True)
        train_realnvp(self.flow, loader, n_epochs=epochs, lr=lr)
    
    def score(self, x):
        """Return log-likelihood. Low = anomalous."""
        log_prob, _ = self.flow(x)
        return log_prob
    
    def detect(self, x, threshold=-100):
        """Binary anomaly detection."""
        scores = self.score(x)
        return scores < threshold
```

### 5.2 Invertible Image Transformations

```python
# GLOW-style image generation with invertible 1x1 conv
from nflows.transforms.linear import ElementwiseAffine
from nflows.transforms.coupling import CouplingMap

# Invertible image transformations:
# - PixelCNN-style coupling
# - Invertible 1x1 convolutions (GLOW)
# - Squeezing operation (multi-scale)
# - Affine coupling with spline transforms
```

### 5.3 Flow Matching para Generación Rápida

```python
# Flow matching permite sampling en 4-8 pasos (vs 100-1000 de diffusion)
# Ideal para aplicaciones en tiempo real

# Key advantage: straight trajectories → fewer ODE solver steps needed
# torchcfm + torchdiffeq = production-ready flow matching

# Use cases:
# - Real-time image generation
# - Fast video synthesis
# - Edge deployment (fewer steps = less compute)
```

---

## 6. Estado del Arte (2024-2026)

### 6.1 Flow Matching Dominance

Los **Flow Matching** methods han superado a los flows clásicos en varios aspectos:

| Método | Repo | Stars | Key Idea |
|--------|------|-------|----------|
| **FM** (Lipman et al., 2023) | `facebookresearch/flow_matching` | 4580 | OT-based flow matching |
| **CFM** (Tong et al., 2023) | `atong01/conditional-flow-matching` | 2512 | Conditional flow matching |
| **LFM** (VinAI, 2024) | `VinAIResearch/LFM` | 354 | Flow matching in latent space |
| **StyleFlow** (Abdal et al.) | `RameenAbdal/StyleFlow` | 2445 | Attribute-conditioned StyleGAN + flows |

### 6.2 Flow Matching vs Diffusion

**Flow matching** es esencialmente diffusion con:
- **Traectorias rectas** (rectified flow) → menos pasos de ODE
- **Training directo del campo vectorial** → más estable
- **Sampling en 4-8 pasos** vs 100-1000 de diffusion

**Conexión teórica:**
- Score-based diffusion → SDE → Flow matching como ODE limit
- Rectified flow → straight-line transport → optimal transport approximation

### 6.3 Librerías Actuales

| Librería | Descripción | Stars |
|----------|-------------|-------|
| **nflows** (Bayesiains) | Flows en PyTorch | 1018 |
| **normalizing-flows** (Stimper) | Flows en PyTorch | 956 |
| **pytorch-normalizing-flows** (karpathy) | Educativo | 916 |
| **flow_matching** (Meta) | Flow matching production | 4580 |
| **torchcfm** | Conditional flow matching | 2512 |

---

## 7. Referencias Clave

### Papers Fundamentales

1. **NICE** — Dinh et al., "Density estimation using Rectified Neural Networks", ICLR 2015
2. **RealNVP** — Dinh et al., "NICE: Non-linear Independent Components Estimation", ICLR 2015
3. **GLOW** — Kingma & Dhariwal, "Glow: Generative Flow with Invertible 1x1 Convolutions", NeurIPS 2018
4. **NSF** — Durkan et al., "Neural Spline Flows", NeurIPS 2019
5. **FFJORD** — Grathwohl et al., "FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models", ICLR 2019
6. **CFM** — Tong et al., "Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport", 2023
7. **Flow Matching** — Lipman et al., "Flow Matching for Generative Modeling", ICLR 2024

### Implementaciones

- **nflows**: https://github.com/bayesiains/nflows
- **normalizing-flows** (Stimper): https://github.com/VincentStimper/normalizing-flows
- **pytorch-normalizing-flows** (karpathy): https://github.com/karpathy/pytorch-normalizing-flows
- **flow_matching** (Meta): https://github.com/facebookresearch/flow_matching
- **torchcfm**: https://github.com/atong01/conditional-flow-matching
- **awesome-normalizing-flows**: https://github.com/janosh/awesome-normalizing-flows

---

## 8. Lecciones Clave

1. **El log-det jacobiano es el cuello de botella** — toda la arquitectura de flows gira en torno a hacerlo eficiente ($O(d)$ en vez de $O(d^3)$)

2. **Coupling layers son el workhorse** — RealNVP coupling + spline transforms = combinación más práctica para dimensión media

3. **FFJORD/Neural ODEs son elegantes pero costosos** — requieren solver numérico y adjoint method, difícil de escalar

4. **Flow matching es el futuro** — combina lo mejor de flows (sampling directo, likelihood) con la escalabilidad de diffusion

5. **Para producción**: usa `torchcfm` o `facebookresearch/flow_matching` — están activos, bien mantenidos, y con ejemplos prácticos

6. **Para dimensión alta (>1000)**: flows clásicos no escalan bien. Diffusion/flow matching son la opción correcta.

7. **Para density estimation y anomaly detection**: flows son insuperables — likelihood exacto + inferencia exacta

---

*Nota: Este tema complementa los ya cubiertos de Diffusion Models (2026-06-13), Vision Transformers (2026-06-22), y Rectified Flow (2026-06-23). La evolución natural es de flows clásicos → flow matching, que conecta directamente con los modelos de difusión.*
