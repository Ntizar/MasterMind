# Arquitecturas Subcuadráticas: xLSTM vs Mamba-2 vs Gated DeltaNet

> **Fecha:** 2026-06-14
> **Tema:** Post-Transformer architectures — State Space Models, xLSTM, y alternativas subcuadráticas
> **Contexto:** Seguimiento de sesiones anteriores sobre SSMs (Mamba) y Diffusion Models

---

## 1. Contexto y Motivación

Los Transformers dominan el modelado de secuencias, pero su atención cuadrática $O(n^2)$ en memoria y cómputo se convierte en un cuello de botella para secuencias largas. Las **arquitecturas subcuadráticas** ($O(n)$ o $O(n \log n)$) ofrecen una alternativa escalable.

En junio de 2026, el paper más relevante es:

> **Hartl et al. (2026)** — *"On Subquadratic Architectures: From Applications to Principles"*
> [arXiv:2606.12364](https://arxiv.org/abs/2606.12364)
> 
> Compara **xLSTM**, **Mamba-2** y **Gated DeltaNet** en 3 tareas: pre-training de código, distilación de LLMs de código, y pre-training de modelos de series temporales. **xLSTM gana en rendimiento general** gracias a un tracking de estado y acumulación más robusto.

### Papers clave adicionales (junio 2026):

| Paper | ID | Contribución |
|-------|-----|-------------|
| Zamba2-VL Technical Report | 2606.00390 | Hybrid LM: Mamba2 + transformer blocks. Competitivo con Molmo2, Qwen3-VL, InternVL3.5 |
| Detection vs Execution: Mamba-2 State Sink | 2606.00930 | Probes de single-bucket pierden la mitad del circuito de Mamba-2 |
| Task Structure Reverses Layerwise Encoding | 2606.00926 | La misma arquitectura invierte su encoding según la tarea |
| CogScale Benchmark | 2605.19758 | 14 tareas sintéticas escalables para evaluar processing de secuencias |
| Single-Layer Model Can Do Language Modeling | 2605.10643 | GPN: un solo vector de estado revisitado por un recurrent block |

---

## 2. Las Tres Arquitecturas

### 2.1 Mamba-2 (State Space Duality)

**Paper original:** [Gu & Dao, 2024](https://arxiv.org/abs/2405.21060)

Mamba-2 introduce **State Space Duality (SSD)**, que unifica la formulación de SSMs con la de Linear Attention. La clave:

```
SSD: y = Σ_{k=1}^{t} (Π_{j=k+1}^{t} B_j C_j) · B_k · C_k · x_k
```

Esto se puede calcular en paralelo usando una **matriz triangular acumulada**, no secuencialmente.

**Ventajas:**
- Inference lineal $O(n)$ en recurrent mode
- Parallel scan en chunk mode (similar a linear attention)
- Hardware-friendly: solo multiplicaiones de matriz

**Limitaciones:**
- State sink: los tokens de boundary dominan el estado recurrente
- Detección vs ejecución: las probes pueden fallar en mechanistic interpretability

### 2.2 xLSTM (Extended LSTM)

**Paper original:** [Beck et al., 2024](https://arxiv.org/abs/2406.05184)

xLSTM extiende la LSTM clásica con:
1. **Expanding LSTM cell** — gate de expansión para mayor capacidad
2. **Element-wise gating** — en lugar de solo multiplicación punto a punto
3. **Temporal mixing layer** — con convolución y SSM-like operations

**Célula xLSTM:**
```
f_t = σ(W_f · [h_{t-1}, x_t] + b_f)  # forget gate expandido
i_t = σ(W_i · [h_{t-1}, x_t] + b_i)  # input gate
o_t = σ(W_o · [h_{t-1}, x_t] + b_o)  # output gate
c̃_t = tanh(W_c · [h_{t-1}, x_t] + b_c)  # candidate
c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t  # cell state con gating expandido
h_t = o_t ⊙ tanh(c_t)  # hidden state
```

**Por qué xLSTM gana (según Hartl et al.):**
- **Gating scheme más flexible** para corrección de estado
- **State tracking más estable** en tareas con dependencias complejas
- **Acumulación de memoria más robusta** en tareas de length-generalization

### 2.3 Gated DeltaNet (GDN)

**Paper original:** [Tay et al., 2023](https://arxiv.org/abs/2207.00749)

GDN es una formulación de **Linear Attention con gating**:
```
h_t = W · (Σ_{k=1}^{t} g_k · x_k · Π_{j=k+1}^{t} λ_j)
```
donde `g_k` es el gate y `λ_j` es el decay factor.

**Ventajas:**
- Muy hardware-friendly (solo multiplicaiones)
- Inference constante $O(1)$ por step en recurrent mode
- Compatible con NPUs (inversión de matrices por sustitución hacia adelante)

**Limitaciones:**
- Menos capacidad de tracking de estado que xLSTM
- Más sensible a errores de propagación en tareas complejas

---

## 3. Implementación Práctica en PyTorch

### 3.1 Mamba-2 Style SSD (simplified)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class Mamba2SSD(nn.Module):
    """
    Simplified Mamba-2 State Space Duality implementation.
    
    Key insight: SSMs can be computed in parallel via chunk-wise
    matrix operations, unifying them with Linear Attention.
    
    Reference: Gu & Dao, "Mamba-2 (SSD)", 2024
    """
    
    def __init__(self, d_model: int, d_state: int = 16, 
                 d_conv: int = 4, expand_factor: int = 2):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_inner = d_model * expand_factor
        
        # Projections
        self.in_proj = nn.Linear(d_model, self.d_inner * 2, bias=False)
        
        # SSM parameters
        self.dt = nn.Linear(self.d_inner, self.d_inner, bias=False)
        self.B = nn.Parameter(torch.randn(self.d_inner, d_state))
        self.C = nn.Parameter(torch.randn(self.d_inner, d_state))
        self.D = nn.Parameter(torch.ones(self.d_inner))
        
        # Output projection
        self.out_proj = nn.Linear(self.d_inner, d_model, bias=False)
        
        # LayerNorm
        self.norm = nn.LayerNorm(d_model)
        
    def _ssd_chunk_scan(self, x: torch.Tensor) -> torch.Tensor:
        """
        SSD chunk-wise parallel scan.
        
        Instead of sequential recurrence:
          s_t = A * s_{t-1} + B * x_t
          y_t = C * s_t + D * x_t
        
        We compute in chunks using matrix operations:
          Y = Δ ⊙ (B ⊗ C) * X  (parallel accumulation)
        """
        B, C = self.B, self.C
        dt = self.dt(x)  # delta/gate
        
        # Chunk-wise accumulation (simplified)
        # In full Mamba-2, this uses a triangular matrix inversion
        # for O(chunk_size^2) per chunk instead of O(seq_len)
        
        batch, seq_len, d_inner = x.shape
        chunk_size = 64
        n_chunks = (seq_len + chunk_size - 1) // chunk_size
        
        outputs = []
        for c in range(n_chunks):
            start = c * chunk_size
            end = min(start + chunk_size, seq_len)
            chunk = x[:, start:end]
            dt_chunk = dt[:, start:end]
            
            # Gate: element-wise multiplication with delta
            gated = chunk * F.silu(dt_chunk)
            
            # SSM convolution in chunk
            # B @ C^T gives the state transition (d_inner x d_inner)
            # This is the key: we accumulate state within the chunk
            state = torch.einsum('bse,si,bse->bsi', 
                                 gated, B, C)
            outputs.append(state)
        
        return torch.cat(outputs, dim=1)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with SSD computation.
        
        Args:
            x: (batch, seq_len, d_model)
        Returns:
            (batch, seq_len, d_model)
        """
        residual = x
        
        # Pre-norm
        x = self.norm(x)
        
        # Project and split
        x = self.in_proj(x)  # (batch, seq, d_inner * 2)
        x, gate = x.chunk(2, dim=-1)
        
        # SSD scan
        x = self._ssd_chunk_scan(x)
        
        # Apply gate and D skip connection
        x = F.silu(gate) * x
        x = x + self.D * x  # skip connection
        
        # Output projection
        out = self.out_proj(x)
        
        # Residual
        return out + residual


class MambaBlock(nn.Module):
    """Single Mamba block with SSD."""
    
    def __init__(self, d_model: int, d_state: int = 16):
        super().__init__()
        self.mamba = Mamba2SSD(d_model, d_state)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(approximate='tanh'),
            nn.Linear(d_model * 4, d_model)
        )
        
    def forward(self, x):
        x = self.mamba(x)
        x = x + self.ffn(x)
        return x


# Test
if __name__ == "__main__":
    model = MambaBlock(d_model=256, d_state=16)
    x = torch.randn(2, 128, 256)
    y = model(x)
    print(f"Input: {x.shape} -> Output: {y.shape}")
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
```

### 3.2 xLSTM Cell (simplified)

```python
class xLSTMCell(nn.Module):
    """
    Simplified xLSTM cell with expanding gate.
    
    Key differences from vanilla LSTM:
    1. Expanding gate: W_f projects to d_model * k (k > 1)
    2. Element-wise gating in cell state update
    3. Temporal mixing with convolutions
    
    Reference: Beck et al., "xLSTM: Extended Long Short-Term Memory", 2024
    """
    
    def __init__(self, d_model: int, d_state: int = None, 
                 expansion_factor: int = 2):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state or d_model
        self.expansion_factor = expansion_factor
        
        # Expanding forget gate (larger than input)
        self.f_gate = nn.Linear(d_model, self.d_state * expansion_factor, bias=False)
        self.i_gate = nn.Linear(d_model, self.d_state, bias=False)
        self.o_gate = nn.Linear(d_model, self.d_state, bias=False)
        self.c_candidate = nn.Linear(d_model, self.d_state, bias=False)
        
        # Temporal mixing (1D conv for local context)
        self.temporal_conv = nn.Conv1d(self.d_state, self.d_state, 
                                        kernel_size=3, padding=1, groups=self.d_state)
        
        # Output projection
        self.out = nn.Linear(self.d_state, self.d_model)
        
        # LayerNorm
        self.norm = nn.LayerNorm(d_model)
        
    def forward(self, x: torch.Tensor, 
                h_prev: torch.Tensor = None, 
                c_prev: torch.Tensor = None) -> tuple:
        """
        Single xLSTM step.
        
        Args:
            x: (batch, seq_len, d_model)
            h_prev: (batch, d_state) — previous hidden state
            c_prev: (batch, d_state) — previous cell state
        Returns:
            h_t: (batch, seq_len, d_model)
            (h_t, c_t) for next step
        """
        if h_prev is None:
            batch, seq_len, _ = x.shape
            h_prev = torch.zeros(batch, self.d_state, device=x.device)
            c_prev = torch.zeros(batch, self.d_state, device=x.device)
            
        outputs = []
        
        for t in range(seq_len):
            xt = x[:, t, :]  # (batch, d_model)
            
            # Expanding forget gate
            f = torch.sigmoid(self.f_gate(xt))  # (batch, d_state * k)
            f = f.view(batch, self.d_state, self.expansion_factor)
            f = f.mean(dim=-1)  # average expansion back to d_state
            
            # Input gate
            i = torch.sigmoid(self.i_gate(xt))
            
            # Output gate
            o = torch.sigmoid(self.o_gate(xt))
            
            # Candidate cell state
            c_tilde = torch.tanh(self.c_candidate(xt))
            
            # Cell state update with expanding gate
            c_t = f * c_prev + i * c_tilde
            
            # Temporal mixing (local context)
            c_t_reshaped = c_t.unsqueeze(1)  # (batch, 1, d_state)
            c_t_mixed = self.temporal_conv(c_t_reshaped).squeeze(1)
            
            # Hidden state
            h_t = o * torch.tanh(c_t_mixed)
            
            outputs.append(h_t)
            
            # Update states
            c_prev = c_t
            h_prev = h_t
            
        h_t = torch.stack(outputs, dim=1)  # (batch, seq_len, d_state)
        
        # Output projection
        h_out = self.out(h_t)
        
        return h_out, h_t, c_t


class xLSTMLayer(nn.Module):
    """Stacked xLSTM layer with residual connections."""
    
    def __init__(self, d_model: int, n_layers: int = 4, 
                 expansion_factor: int = 2):
        super().__init__()
        self.cells = nn.ModuleList([
            xLSTMCell(d_model, expansion_factor=expansion_factor)
            for _ in range(n_layers)
        ])
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward through stacked xLSTM layers.
        
        Args:
            x: (batch, seq_len, d_model)
        Returns:
            (batch, seq_len, d_model)
        """
        for cell in self.cells:
            x, _, _ = cell(x)
            x = x + x  # residual (input == output in stacked layers)
        return x


# Test
if __name__ == "__main__":
    model = xLSTMCell(d_model=256)
    x = torch.randn(2, 64, 256)
    y, h, c = model(x)
    print(f"Input: {x.shape} -> Output: {y.shape}")
    print(f"Hidden: {h.shape}, Cell: {c.shape}")
```

### 3.3 Hybrid Transformer-Mamba Block

```python
class HybridTransformerMamba(nn.Module):
    """
    Hybrid architecture combining Transformer attention with Mamba SSM.
    
    Design pattern from Zamba2-VL (2606.00390):
    - Most layers: Mamba-2 (efficient long-range)
    - Few layers: Transformer (local precision)
    - Shared projection layers for efficiency
    
    This pattern is particularly effective for:
    - Vision-language models (Zamba2-VL)
    - Code models (Hartl et al. 2026)
    - Time series (SPDM, 2606.09917)
    """
    
    def __init__(self, d_model: int, n_mamba_layers: int = 8, 
                 n_transformer_layers: int = 2, d_state: int = 16):
        super().__init__()
        self.d_model = d_model
        
        # Mamba layers (efficient long-range processing)
        self.mamba_blocks = nn.ModuleList([
            MambaBlock(d_model, d_state) 
            for _ in range(n_mamba_layers)
        ])
        
        # Transformer layers (precise local attention)
        transformer_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=8, dim_feedforward=d_model*4,
            batch_first=True, activation='gelu'
        )
        self.transformer_blocks = nn.ModuleList([
            transformer_layer for _ in range(n_transformer_layers)
        ])
        
        # Positional encoding (shared)
        self.pos_enc = nn.Parameter(
            torch.randn(1, 2048, d_model) * 0.02
        )
        
        # LayerNorm
        self.norm = nn.LayerNorm(d_model)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward: Mamba layers first, then Transformer refinement.
        
        Pattern: [Mamba × N] → [Transformer × M] → Norm
        """
        x = x + self.pos_enc[:, :x.size(1), :]
        
        # Phase 1: Mamba (efficient long-range)
        for block in self.mamba_blocks:
            x = block(x)
            
        # Phase 2: Transformer (precise local)
        for block in self.transformer_blocks:
            x = block(x)
            
        return self.norm(x)


# Test
if __name__ == "__main__":
    model = HybridTransformerMamba(d_model=256, n_mamba_layers=8, n_transformer_layers=2)
    x = torch.randn(2, 128, 256)
    y = model(x)
    print(f"Input: {x.shape} -> Output: {y.shape}")
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
```

---

## 4. Comparativa de Rendimiento (Hartl et al. 2026)

| Métrica | xLSTM | Mamba-2 | Gated DeltaNet | Transformer |
|---------|-------|---------|----------------|-------------|
| Code pre-training | **Mejor** | 2º | 3º | Referencia |
| Distilación de código | **Mejor** | 2º | 3º | Referencia |
| Time-series FM | **Mejor** | 2º | 3º | Referencia |
| Latencia inference | 2º | **Mejor** | **Mejor** | Peor |
| Memoria inference | 2º | **Mejor** | **Mejor** | Peor |
| State tracking | **Mejor** | 2º | 3º | Distribuido |

**Conclusión clave:** xLSTM gana en rendimiento general porque su gating scheme permite **corrección de estado más flexible y estable**, especialmente en tareas con dependencias complejas y length-generalization.

---

## 5. Insights Clave de Investigación

### 5.1 State Sink en Mamba-2 (2606.00930)

El **state sink** en Mamba-2 es análogo al attention sink en Transformers:
- Los tokens de boundary (especialmente BOS) dominan desproporcionadamente el delta-gate
- Las probes de single-bucket recuperan solo la capa de ejecución, perdiendo la capa de detección
- Esto implica que la **interpretabilidad mecánica** en Mamba-2 requiere análisis multi-bucket

### 5.2 Task-Dependent State Encoding (2606.00926)

La misma arquitectura invierte su perfil de encoding según la tarea:
- **Parity task:** estado concentrado al final en Mamba, gradual en Transformer
- **Dyck-k task:** patrón se invierte
- Esto sugiere que el encoding de estado no es un trait arquitectónico fijo

### 5.3 Hybrid Architecture Pattern

El patrón **Mamba + Transformer** (Zamba2-VL) es efectivo porque:
1. Mamba maneja el rango largo eficientemente
2. Transformer refina la atención local
3. Comparten proyecciones para eficiencia
4. Zamba2-VL compite con Molmo2, Qwen3-VL, InternVL3.5

---

## 6. Recursos y Repositorios

### Papers esenciales:
1. **Hartl et al. (2026)** — Subquadratic comparison: https://arxiv.org/abs/2606.12364
2. **Gu & Dao (2024)** — Mamba-2 (SSD): https://arxiv.org/abs/2405.21060
3. **Beck et al. (2024)** — xLSTM: https://arxiv.org/abs/2406.05184
4. **Tay et al. (2023)** — Gated DeltaNet: https://arxiv.org/abs/2207.00749
5. **Zamba2-VL (2026)** — Hybrid VLM: https://arxiv.org/abs/2606.00390

### Repositorios:
- **Mamba paper list:** https://github.com/Event-AHU/Mamba_State_Space_Model_Paper_List (753⭐)
- **simple-mamba:** https://github.com/Marshajennifer/simple-mamba (implementación PyTorch CIFAR-10)
- **A2Mamba:** https://github.com/LMMMEng/A2Mamba (Attention-augmented SSM for vision)

### Benchmarks:
- **CogScale:** 14 tareas sintéticas escalables para sequence processing (2605.19758)

---

## 7. Conclusiones

1. **xLSTM está ganando terreno** como la alternativa subcuadrática más efectiva en rendimiento general
2. **Mamba-2 sigue siendo el rey en eficiencia** (latencia + memoria en inference)
3. **Gated DeltaNet** es la opción más hardware-friendly (NPUs, edge devices)
4. **Hybrid Mamba+Transformer** es un patrón probado para VLMs y code models
5. La **interpretabilidad mecánica** en SSMs es un campo activo con hallazgos contraintuitivos (state sink, task-dependent encoding)

---

## 8. Siguiente Tema Propuesto

**Neural Radiance Fields (NeRF) y 3D Gaussian Splatting**

- NeRF: representación implícita de escenas 3D con MLPs
- 3D Gaussian Splatting: renderizado explícito y ultra-rápido
- Aplicaciones: reconstrucción 3D, VR/AR, generación de contenido
- Conexión con nuestro stack: útil para visualización 3D en navegador (Three.js), procesamiento de imágenes, y generación de assets

**Alternativa:** **Diffusion Transformers (DiT)** — cómo los transformers reemplazan a las U-Net en modelos de difusión (DALL-E 3, Sora, Stable Diffusion 3). Esto conectaría directamente con nuestra nota anterior de Diffusion Models.
