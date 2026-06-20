# Comparativa de Arquitecturas Subcuadráticas: xLSTM vs Mamba-2 vs Gated DeltaNet

> **Fecha:** 2026-06-14
> **Fuente principal:** Hartl et al. (2026) — "On Subquadratic Architectures: From Applications to Principles"
> [arXiv:2606.12364](https://arxiv.org/abs/2606.12364)

---

## Contexto

Los Transformers dominan el modelado de secuencias, pero su atención cuadrática $O(n^2)$ se convierte en cuello de botella para secuencias largas. Las arquitecturas subcuadráticas ($O(n)$ o $O(n \log n)$) ofrecen alternativa escalable.

**2005+ papers** mencionan "mamba" en arXiv (junio 2026). El campo está madurando rápidamente.

---

## Las Tres Arquitecturas Comparadas

### Mamba-2 (State Space Duality — SSD)

**Paper:** Gu & Dao, 2024 — arXiv:2405.21060

SSD unifica SSMs con Linear Attention:
```
SSD: y = Σ_{k=1}^{t} (Π_{j=k+1}^{t} B_j C_j) · B_k · C_k · x_k
```
Se calcula en paralelo via matriz triangular acumulada, no secuencialmente.

- **Inference:** O(N) en recurrent mode
- **Training:** Parallel scan en chunk mode (como linear attention)
- **Hardware:** Solo multiplicaiones de matriz → ideal para NPUs

**Limitaciones conocidas:**
- State sink: tokens de boundary dominan el estado recurrente (análogo a attention sink)
- Probes de single-bucket pierden la mitad del circuito (2606.00930)
- Task-dependent encoding: la misma arquitectura invierte su perfil según la tarea (2606.00926)

### xLSTM (Extended LSTM)

**Paper:** Beck et al., 2024 — arXiv:2406.05184

Extiende LSTM clásica con:
1. Expanding LSTM cell — gate de expansión para mayor capacidad
2. Element-wise gating — no solo multiplicación punto a punto
3. Temporal mixing layer — con convolución y SSM-like operations

**Por qué xLSTM gana (Hartl et al. 2026):**
- Gating scheme más flexible para corrección de estado
- State tracking más estable en tareas con dependencias complejas
- Acumulación de memoria más robusta en length-generalization

### Gated DeltaNet (GDN)

**Paper:** Tay et al., 2023 — arXiv:2207.00749

Linear Attention con gating:
```
h_t = W · (Σ_{k=1}^{t} g_k · x_k · Π_{j=k+1}^{t} λ_j)
```

- **Inference:** O(1) por step en recurrent mode
- **Hardware:** Compatible con NPUs (inversión por sustitución hacia adelante)
- **Limitación:** Menos capacidad de tracking de estado que xLSTM

---

## Resultados de Hartl et al. (2026)

Evalúan en 3 tareas con dependencias complejas:

| Tarea | xLSTM | Mamba-2 | Gated DeltaNet | Transformer |
|-------|-------|---------|----------------|-------------|
| Code pre-training | **Mejor** | 2º | 3º | Referencia |
| Distilación de código | **Mejor** | 2º | 3º | Referencia |
| Time-series FM | **Mejor** | 2º | 3º | Referencia |
| Latencia inference | 2º | **Mejor** | **Mejor** | Peor |
| Memoria inference | 2º | **Mejor** | **Mejor** | Peor |

**Conclusión:** xLSTM gana en rendimiento general. Mamba-2 sigue siendo el rey en eficiencia.

---

## Papers Clave Adicionales (Junio 2026)

### Zamba2-VL (2606.00390)
Hybrid VLM: Mamba2 + bloques transformer compartidos. Competitivo con Molmo2, Qwen3-VL, InternVL3.5. Patrón: la mayoría de capas son Mamba-2 (eficiente), pocas son Transformer (preciso).

### State Sink en Mamba-2 (2606.00930)
Probes de single-bucket recuperan solo la capa de ejecución, perdiendo la capa de detección. El state sink se descompone en dos conjuntos funcionales de head. Interpretabilidad mecánica en Mamba-2 requiere análisis multi-bucket.

### Task-Dependent Encoding (2606.00926)
Parity task: estado concentrado al final en Mamba, gradual en Transformer. Dyck-k: patrón se invierte. El encoding de estado NO es un trait arquitectónico fijo.

### CogScale Benchmark (2605.19758)
14 tareas sintéticas escalables para evaluar procesamiento de secuencias sin coste de pre-training masivo.

### Single-Layer Language Model (2605.10643)
GPN: un solo vector de estado revisitado por un recurrent block (un FFN, una matriz de memoria compartida). A 130M params, un modelo de 1-layer hace language modeling.

---

## Patrón Hybrid Mamba+Transformer

Patrón probado en Zamba2-VL:
```
[ Mamba-2 Block × N ] → [ Transformer Block × M ] → Norm

N ≈ 8-16 (long-range eficiente)
M ≈ 2-4 (refinamiento local)
```

Efectivo para:
- Vision-language models (Zamba2-VL)
- Code models (Hartl et al. 2026)
- Time series (SPDM, 2606.09917)
- Graph Mamba (2606.09432)

---

## Recursos

### Repositorios
- **Mamba paper list:** https://github.com/Event-AHU/Mamba_State_Space_Model_Paper_List (753⭐)
- **simple-mamba:** https://github.com/Marshajennifer/simple-mamba (PyTorch CIFAR-10)
- **A2Mamba:** https://github.com/LMMMEng/A2Mamba (Attention-augmented SSM for vision)

### Benchmarks
- **CogScale:** 14 tareas sintéticas escalables para sequence processing
