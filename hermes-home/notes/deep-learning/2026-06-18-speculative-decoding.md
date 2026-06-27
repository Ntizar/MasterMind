# Speculative Decoding — Aceleración de Inferencia LLM

> **Fecha:** 2026-06-18  
> **Tema:** 7 de la serie Deep Learning Fundamentals  
> **Autor:** David Antizar (Ntizar)

---

## 1. Concepto Central

El **speculative decoding** (también llamado *speculative sampling*) es una técnica que permite generar **múltiples tokens por forward pass** del modelo objetivo, sin sacrificar la distribución exacta de salida.

**Idea clave:** Un modelo pequeño y rápido (draft/modelo borrador) genera N tokens candidatos en paralelo. El modelo grande (target/verificador) los verifica en un solo forward pass paralelo. Los tokens que coinciden con la distribución del target se aceptan; los que no, se rechazan y se muestrea uno correcto.

**Resultado:** En teoría, con aceptación perfecta de N tokens, se logra un speedup de N×. En la práctica, speedups de 2-4× son típicos.

### Analogía intuitiva

Imagina que un profesor (modelo grande) dicta una frase palabra por palabra. Un estudiante (modelo pequeño) puede predecir las próximas 5 palabras rápidamente. El profesor solo necesita revisar si las 5 palabras del estudiante son correctas — si lo son, las acepta todas de golpe. Si la palabra 3 es incorrecta, el profesor la corrige y sigue.

---

## 2. Fundamentos Matemáticos

### 2.1 Algoritmo Original (Leviathan et al., 2022)

El paper fundacional introduce dos componentes:

1. **Spec-Drafter:** Modelo independiente optimizado para drafting eficiente
2. **Spec-Verification:** Verificación paralela de tokens draftados

**Algoritmo:**

```
Para cada paso de decoding:
  1. Drafter genera γ tokens candidatos: t₁, t₂, ..., tγ
  2. Target model calcula P_target(t₁...tγ | context) en un solo forward
  3. Para cada token tᵢ:
     - Si P_target(tᵢ) / P_draft(tᵢ) ≥ U ~ Uniform(0,1):
       → Aceptar tᵢ
     - Si P_target(tᵢ) / P_draft(tᵢ) < U:
       → Rechazar tᵢ, muestrear tᵢ' ~ max(0, P_target - P_draft), normalizar
       → Terminar el batch
  4. Si todos aceptados: muestrear siguiente token del target
```

**Propiedad fundamental:** La distribución de salida es **exactamente idéntica** a la del modelo target. No hay aproximación, no hay pérdida de calidad.

### 2.2 Teorema de Corrección

Para cada token tᵢ en el batch draftado:

```
P_accept(tᵢ) = min(1, P_target(tᵢ) / P_draft(tᵢ))
```

Si se rechaza tᵢ, el token de reemplazo se muestrea de:

```
Q(t) = max(0, P_target(t) - P_draft(t)) / Z
```

donde Z = 1 - Σ min(1, P_target(tⱼ)/P_draft(tⱼ)) es la constante de normalización.

**Esto garantiza que la distribución marginal de salida es exactamente P_target.**

### 2.3 Análisis de Speedup

El speedup teórico viene dado por:

```
Speedup ≈ γ × α
```

donde γ es el número de tokens draftados y α es la tasa de aceptación.

**Ejemplo:** Si γ=5 y α=0.6, el speedup es 3×.

Pero hay overhead de cómputo del drafter y del target (que aún necesita calcular el hidden state del último token aceptado). El speedup efectivo es:

```
Speedup_efectivo = (γ × α) / (1 + overhead)
```

---

## 3. Evolución: De Draft Externo a Auto-Draft

### 3.1 Fase 1: Draft con Modelo Externo (Leviathan et al., 2022)

- Modelo pequeño independiente (ej: GPT-2 small para GPT-2 large)
- Requiere entrenar/desplegar dos modelos
- Overhead de comunicación entre drafter y target

### 3.2 Fase 2: Medusa — Múltiples Heads Internos (Cai et al., 2024)

**Paper:** [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774)

**Idea:** En lugar de un modelo externo, añadir K heads de decodificación adicionales sobre las capas internas del propio modelo.

```
Modelo original:    Input → [Layers] → LM_Head → Output
Medusa:             Input → [Layers] → LM_Head → Output_0
                                  ↓
                           Auxiliary_Head_1 → Output_1
                                  ↓
                           Auxiliary_Head_2 → Output_2
                                  ↓
                           ...
                           Auxiliary_Head_K → Output_K
```

**Clave:** Cada auxiliary head predice el token en la posición i+1, i+2, ..., i+K dado el hidden state en la posición i.

**Ventajas:**
- Mismo modelo, sin necesidad de drafter externo
- Los heads se entrenan con un paso de gradiente adicional sobre los hidden states
- Compatible con cualquier LLM

**Desventaja:** Los heads profundos tienen menor precisión porque predicen más tokens adelante.

### 3.3 Fase 3: EAGLE — Draft en el Espacio de Features (Li et al., 2024)

**Paper:** [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077)

**Idea revolucionaria:** En lugar de hacer autoregression sobre tokens (discretos), hacerla sobre **features** (continuos, del penúltimo layer).

```
Antes (token-level):
  h_t → LM_Head → P(t_{t+1}) → sample t_{t+1} → repeat

EAGLE (feature-level):
  h_t → Feature Drafter → h_{t+1}, h_{t+2}, ... → LM_Head → verify
```

**Por qué funciona mejor:**
1. El espacio de features es continuo → la autoregression es más suave y predecible
2. Se reutiliza el KV cache del target → sin overhead de memoria extra
3. El feature drafter es mucho más pequeño que un modelo de tokens completo

**Resultados reportados:**
- Llama-2-7B: 2.2× speedup con EAGLE-2
- Mistral-7B: 2.5× speedup
- Aceptación rate > 70% en tareas generales

### 3.4 Fase 4: Tree Speculative Decoding (EAGLE-2, EAGLE-3)

**Idea:** En lugar de un solo path lineal de γ tokens, construir un **árbol de drafts** donde cada nodo tiene múltiples hijos.

```
        [root]
       /   |   \
      A    B    C
     / \   |    \
    A1  A2  B1   C1

Verificación: un solo forward del target sobre todos los nodos del árbol.
```

**Ventaja:** El target verifica múltiples ramas en paralelo, aumentando drásticamente la tasa de aceptación efectiva.

**EAGLE-3** (2025): Mejora EAGLE-2 con:
- Dynamic tree depth (profundidad adaptativa por paso)
- Better feature-level drafting con más capas de info
- Tree attention optimization

### 3.5 Fase 5: Self-Speculative Decoding (SWIFT, ICLR 2025)

**Paper:** [SWIFT: On-the-Fly Self-Speculative Decoding for LLM Inference Acceleration](https://arxiv.org/abs/2406.13629)

**Idea:** Usar la **heterogeneidad interna** del propio modelo como drafter. En modelos híbridos (SSM + Transformer), las subcapas SSM/linear-attention son mucho más baratas que las subcapas self-attention.

**SWIFT:**
- Aísla las subcapas baratas del modelo
- Usa esas subcapas como drafter "on-the-fly"
- Sin entrenamiento adicional necesario
- Zero overhead de memoria

---

## 4. Implementación Práctica

### 4.1 Speculative Decoding Básico (PyTorch)

```python
import torch
import torch.nn.functional as F

class SpeculativeDecoder:
    """
    Speculative decoding básico con draft model.
    
    Args:
        target_model: Modelo grande (verificador)
        draft_model: Modelo pequeño (borrador)
        max_draft: Número máximo de tokens a draftar por paso
    """
    
    def __init__(self, target_model, draft_model, max_draft=4):
        self.target = target_model
        self.draft = draft_model
        self.max_draft = max_draft
    
    @torch.no_grad()
    def decode(self, input_ids, max_new_tokens=100, temperature=1.0, top_p=1.0):
        """Decode con speculative sampling."""
        outputs = [input_ids]
        current_ids = input_ids.clone()
        
        for _ in range(max_new_tokens):
            # === FASE 1: DRAFT ===
            # El draft model genera γ tokens en paralelo
            draft_ids, draft_logits = self._draft(current_ids, self.max_draft)
            num_draft = draft_ids.size(1)
            
            # === FASE 2: VERIFY ===
            # El target model verifica todos los tokens de golpe
            target_logits = self.target(draft_ids).logits  # (batch, γ, vocab)
            
            # === FASE 3: ACCEPT/REJECT ===
            accepted_ids, accept_count = self._accept_or_reject(
                draft_ids, draft_logits, target_logits, temperature, top_p
            )
            
            # Concatenar tokens aceptados
            current_ids = torch.cat([current_ids, accepted_ids], dim=1)
            outputs.append(accepted_ids)
            
            # Si se aceptaron todos los drafts, muestrear siguiente del target
            if accept_count == num_draft:
                next_logits = self.target(current_ids[:, -1:]).logits
                next_token = self._sample(next_logits, temperature, top_p)
                current_ids = torch.cat([current_ids, next_token], dim=1)
                outputs.append(next_token)
            
            # Early stopping
            if (accepted_ids == self.target.config.eos_token_id).any():
                break
        
        return torch.cat(outputs, dim=1)
    
    def _draft(self, input_ids, num_steps):
        """Draft model genera tokens autoregresivamente."""
        draft_tokens = []
        current = input_ids.clone()
        
        for _ in range(num_steps):
            logits = self.draft(current).logits[:, -1, :]
            token = self._sample(logits, temperature=1.0, top_p=1.0)
            draft_tokens.append(token)
            current = torch.cat([current, token], dim=1)
        
        # Stack: (batch, γ)
        return torch.cat(draft_tokens, dim=1), draft_tokens
    
    def _accept_or_reject(self, draft_ids, draft_logits, target_logits, 
                          temperature, top_p):
        """
        Acepta o rechaza cada token draftado según el criterio de 
        Metropolis-Hastings.
        
        Returns:
            accepted_ids: Tokens aceptados
            accept_count: Número de tokens aceptados consecutivos
        """
        batch_size = draft_ids.size(0)
        num_draft = draft_ids.size(1)
        
        # Convertir logits a probabilidades
        draft_probs = F.softmax(draft_logits / temperature, dim=-1)
        target_probs = F.softmax(target_logits / temperature, dim=-1)
        
        # Obtener probs de los tokens draftados
        draft_probs_selected = draft_probs.gather(2, draft_ids.unsqueeze(-1)).squeeze(-1)
        target_probs_selected = target_probs.gather(2, draft_ids.unsqueeze(-1)).squeeze(-1)
        
        # Ratio de aceptación: min(1, P_target / P_draft)
        ratios = torch.where(
            draft_probs_selected > 0,
            target_probs_selected / draft_probs_selected,
            torch.zeros_like(draft_probs_selected)
        )
        accept_probs = torch.min(ratios, torch.ones_like(ratios))
        
        # Muestreo de aceptación
        U = torch.rand_like(accept_probs)
        accepted = accept_probs >= U  # (batch, γ)
        
        # Encontrar primer rechazo
        accept_count = accepted.long().sum(dim=1)
        
        # Tokens aceptados
        accepted_ids = draft_ids.clone()
        for b in range(batch_size):
            if accept_count[b] < num_draft:
                # Reemplazar token rechazado con muestreo de Q
                rejected_idx = accept_count[b]
                # Q(t) = max(0, P_target - P_draft) / Z
                Q = torch.clamp(target_probs[b] - draft_probs[b], min=0)
                Q = Q / Q.sum()
                next_token = torch.multinomial(Q, 1)
                accepted_ids[b, rejected_idx:] = -1  # Marcar como no válido
        
        # Solo devolver los aceptados consecutivos
        valid_mask = (accepted_ids >= 0)
        valid_mask[:, num_draft:] = False
        
        final_ids = []
        for b in range(batch_size):
            count = accept_count[b].item()
            final_ids.append(accepted_ids[b, :count].unsqueeze(0))
        
        return torch.cat(final_ids, dim=0), accept_count
    
    def _sample(self, logits, temperature=1.0, top_p=1.0):
        """Sampling con temperature y top-p."""
        if temperature != 1.0:
            logits = logits / temperature
        
        # Top-p filtering
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
        sorted_indices_to_remove = cumulative_probs > top_p
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = False
        logits[sorted_indices_to_remove] = float('-inf')
        
        probs = F.softmax(logits, dim=-1)
        return torch.multinomial(probs, 1)
```

### 4.2 Tree Speculative Decoding (EAGLE-2 style)

```python
class TreeSpeculativeDecoder:
    """
    Tree speculative decoding con estructura de árbol dinámica.
    
    Implementa el patrón de EAGLE-2: drafting con árbol donde
    cada nodo tiene múltiples hijos, verificación en un solo
    forward del target.
    """
    
    def __init__(self, target_model, draft_model, tree_width=4, tree_depth=4):
        self.target = target_model
        self.draft = draft_model
        self.tree_width = tree_width
        self.tree_depth = tree_depth
    
    @torch.no_grad()
    def decode(self, input_ids, max_new_tokens=100):
        """Decode con tree speculative sampling."""
        outputs = []
        current_ids = input_ids.clone()
        
        for step in range(max_new_tokens):
            # Construir árbol de drafts
            tree = self._build_draft_tree(current_ids)
            
            # Flatten tree para forward del target
            flat_ids = self._flatten_tree(tree)
            flat_positions = self._get_positions(tree)
            
            # Forward del target sobre todo el árbol
            target_outputs = self.target(flat_ids)
            target_logits = target_outputs.logits  # (num_nodes, vocab)
            
            # Verificar cada nodo del árbol
            accepted_nodes, rejected_node = self._verify_tree(
                tree, target_logits
            )
            
            # Actualizar current_ids con los nodos aceptados
            current_ids = self._apply_tree(current_ids, accepted_nodes)
            outputs.extend(accepted_nodes)
            
            # Si se rechazó un nodo, añadir el token corregido
            if rejected_node is not None:
                current_ids = torch.cat([current_ids, rejected_node], dim=1)
                outputs.append(rejected_node)
        
        return torch.cat(outputs, dim=1)
    
    def _build_draft_tree(self, input_ids):
        """
        Construir árbol de drafts usando el feature drafter.
        
        Cada nivel del árbol genera tree_width hijos por nodo.
        La profundidad es tree_depth.
        """
        tree = {'ids': input_ids.clone(), 'children': []}
        
        def build_level(node, depth):
            if depth >= self.tree_depth:
                return
            
            # Feature-level drafting: predecir múltiples continuaciones
            hidden = self.target(node['ids']).hidden_states[-2]  # Penúltimo layer
            draft_features = self.draft(hidden)  # (batch, tree_width, hidden)
            
            # Convertir features a logits
            lm_head = self.target.get_output_embeddings()
            bias = self.target.get_output_bias() if hasattr(self.target, 'get_output_bias') else None
            
            for i in range(self.tree_width):
                feat = draft_features[:, i:i+1, :]
                logits = lm_head(feat)
                if bias is not None:
                    logits = logits + bias
                token = torch.argmax(logits, dim=-1)
                
                child = {
                    'ids': torch.cat([node['ids'], token], dim=1),
                    'children': []
                }
                node['children'].append(child)
                build_level(child, depth + 1)
        
        build_level(tree, 0)
        return tree
    
    def _flatten_tree(self, tree):
        """Flatten tree de nodos a tensor (num_nodes, seq_len)."""
        nodes = [tree['ids']]
        for child in tree['children']:
            nodes.extend(self._flatten_tree(child))
        return torch.cat(nodes, dim=0)
    
    def _verify_tree(self, tree, target_logits):
        """
        Verificar cada nodo del árbol.
        
        Returns:
            accepted_nodes: Lista de tokens aceptados
            rejected_node: Token rechazado (si hay)
        """
        # Para cada nodo, verificar si el token draftado es aceptado
        # por el target model
        ...
```

### 4.3 Medusa-Style Auxiliary Heads

```python
class MedusaDecoder(torch.nn.Module):
    """
    Medusa: Multiple decoding heads para speculative decoding.
    
    Añade K heads auxiliares sobre el modelo base para predecir
    tokens a distancia 1, 2, ..., K sin necesidad de un drafter externo.
    """
    
    def __init__(self, base_model, num_heads=3, head_depth=3):
        super().__init__()
        self.base = base_model
        self.num_heads = num_heads
        
        # Obtener hidden size del modelo base
        hidden_size = base_model.config.hidden_size
        
        # Crear heads auxiliares
        # Cada head: [LayerNorm] → [Linear] → [Activation] → [Linear → LM head]
        self.aux_heads = torch.nn.ModuleList()
        for i in range(num_heads):
            head = torch.nn.Sequential(
                torch.nn.LayerNorm(hidden_size),
                torch.nn.Linear(hidden_size, hidden_size),
                torch.nn.GELU(),
                torch.nn.Linear(hidden_size, hidden_size),
                torch.nn.GELU(),
                torch.nn.Linear(hidden_size, base_model.config.vocab_size)
            )
            self.aux_heads.append(head)
        
        self.head_depth = head_depth
    
    def forward(self, input_ids, labels=None):
        """
        Forward con todos los heads.
        
        Returns:
            main_logits: Logits del head principal (posición n+1)
            aux_logits: Lista de logits de cada head auxiliar
        """
        outputs = self.base(input_ids)
        hidden = outputs.hidden_states[-1]  # (batch, seq_len, hidden)
        
        # Head principal: último token
        main_logits = self.base.lm_head(hidden[:, -1:, :])
        
        # Heads auxiliares: predicen tokens a distancia 2, 3, ...
        aux_logits = []
        for i, head in enumerate(self.aux_heads):
            # Usar hidden state de la posición i+1 para predecir posición i+2
            if i + 1 < hidden.size(1):
                h = hidden[:, i + 1:i + 2, :]
                aux_logit = head(h)
                aux_logits.append(aux_logit)
        
        return main_logits, aux_logits
    
    @torch.no_grad()
    def generate_speculative(self, input_ids, max_new_tokens=50, temperature=0.7):
        """Generate con speculative decoding usando los heads auxiliares."""
        outputs = input_ids.clone()
        
        for _ in range(max_new_tokens):
            # Obtener hidden states
            hidden = self.base(outputs).hidden_states[-1]
            
            # Generar candidatos con todos los heads
            candidates = []
            candidate_probs = []
            
            # Head principal (posición +1)
            main_logit = self.base.lm_head(hidden[:, -1:, :])
            main_token = torch.argmax(main_logit, dim=-1)
            candidates.append(main_token)
            candidate_probs.append(F.softmax(main_logit / temperature, dim=-1))
            
            # Heads auxiliares (posiciones +2, +3, ...)
            for i, head in enumerate(self.aux_heads):
                if i + 1 < hidden.size(1):
                    h = hidden[:, i + 1:i + 2, :]
                    aux_logit = head(h)
                    aux_token = torch.argmax(aux_logit, dim=-1)
                    candidates.append(aux_token)
                    candidate_probs.append(F.softmax(aux_logit / temperature, dim=-1))
            
            # Verificación con el modelo base
            # (En implementación real, se usa el LM head del base, no los aux)
            # ...
            
            # Aceptar tokens y actualizar outputs
            outputs = torch.cat([outputs, main_token], dim=1)
        
        return outputs
```

### 4.4 Ejemplo de Entrenamiento de Heads Auxiliares (Medusa)

```python
def train_medusa_heads(base_model, dataloader, num_epochs=3, lr=1e-4):
    """
    Entrenar los heads auxiliares de Medusa.
    
    Procedimiento:
    1. Congelar el modelo base
    2. Añadir K heads auxiliares
    3. Entrenar solo los heads con loss de language modeling
    """
    import torch.optim as optim
    
    # Congelar modelo base
    for param in base_model.parameters():
        param.requires_grad = False
    
    # Crear Medusa decoder
    medusa = MedusaDecoder(base_model, num_heads=3)
    
    # Solo entrenar los heads auxiliares
    optimizer = optim.Adam(
        filter(lambda p: p.requires_grad, medusa.parameters()),
        lr=lr
    )
    
    # Entrenamiento
    medusa.train()
    for epoch in range(num_epochs):
        for batch in dataloader:
            input_ids, labels = batch
            
            # Forward
            main_logits, aux_logits = medusa(input_ids)
            
            # Calcular loss para cada head
            loss = 0
            main_loss = F.cross_entropy(
                main_logits.view(-1, main_logits.size(-1)),
                labels[:, 1:].reshape(-1)
            )
            loss += main_loss
            
            for i, aux_logit in enumerate(aux_logits):
                # Labels desplazados: head i predice posición i+2
                if i + 1 < labels.size(1):
                    aux_labels = labels[:, i + 2:i + 3].reshape(-1)
                    aux_loss = F.cross_entropy(
                        aux_logit.view(-1, aux_logit.size(-1)),
                        aux_labels
                    )
                    loss += aux_loss
            
            # Backward y step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}")
    
    return medusa
```

---

## 5. Benchmarks y Resultados

### 5.1 Speedups Reportados

| Método | Modelo | Speedup | Acceptance Rate |
|--------|--------|---------|-----------------|
| Leviathan et al. (2022) | GPT-2 small → large | 2.0× | ~50% |
| Medusa (3 heads) | Llama-2-7B | 1.6-1.8× | ~60% |
| EAGLE-1 | Llama-2-7B | 2.0× | ~65% |
| EAGLE-2 | Llama-2-7B | 2.2× | ~70% |
| EAGLE-3 | Llama-2-7B | 2.5× | ~75% |
| TriForce (hierarchical) | Llama-2-70B | 2.8× | ~72% |
| SWIFT (self-speculative) | Llama-2-7B | 2.1× | ~68% |

### 5.2 Factores Clave de Éxito

1. **Similitud de representación** (EAGLE paper): La tasa de aceptación depende de qué tan similares son las representaciones del drafter y el target. Si el drafter no puede predecir bien los features del target, el acceptance rate cae.

2. **Tamaño del drafter**: Más pequeño = más rápido pero menos preciso. El sweet spot es ~1/4 del tamaño del target.

3. **Profundidad del draft**: Más tokens draftados = más paralelismo pero menor acceptance rate (los errores se acumulan).

4. **Tree vs linear**: Tree drafting puede duplicar el acceptance rate efectivo porque explora múltiples ramas.

### 5.3 Overhead Práctico

```
Time per token (ms):
┌─────────────────────────────────────────────────────────────┐
│ Target forward (single):     12ms  ████████████████████████  │
│ Draft forward (γ=4):          3ms  ████                      │
│ Target verify (γ=4):        12ms  ████████████████████████  │
│                             ───────────────────────────────  │
│ Sin speculative:            12ms/token                       │
│ Con speculative (γ=4, α=0.6): (12+3) / (4×0.6) = 6.25ms/token │
│ Speedup: ~1.9×                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Integración con vLLM

vLLM soporta speculative decoding nativamente desde la versión 0.4+:

```python
from vllm import LLM, SamplingParams

# Target model (grande)
target = LLM(model="meta-llama/Llama-2-7b-chat-hf")

# Draft model (pequeño) — mismo repo, diferente tamaño
draft = LLM(model="meta-llama/Llama-2-1b-chat-hf")

# Speculative decoding params
sampling_params = SamplingParams(
    temperature=0.7,
    max_tokens=100,
)

# Decoding con speculative
output = target.generate(
    "El mercado eléctrico español",
    sampling_params=sampling_params,
    use_speculative_decoding=True,
    draft_model=draft,
    num_speculative_tokens=4,  # γ
)
```

**Configuración avanzada en vLLM:**
- `num_speculative_tokens`: γ (número de tokens draftados)
- `speculative_model`: Modelo drafter
- `speculative_algorithm`: "EAGLE" o "Nucleus"
- `speculative_num_layers`: Capas del target para reutilizar

---

## 7. Aplicaciones al Stack Actual

### 7.1 Relevancia para MicroVM (1vCPU/2GB)

Speculative decoding es **particularmente relevante** para el stack de David porque:

1. **MicroVM tiene recursos limitados** (1vCPU, 2GB RAM) — cualquier aceleración de inference es crítica
2. **EAGLE reutiliza el KV cache** del target → sin overhead de memoria adicional
3. **Feature-level drafting** (EAGLE) es más eficiente que token-level → ideal para CPU
4. **SWIFT** (self-speculative) no necesita modelo externo → perfecto para edge deployment

### 7.2 Posible Integración

```
Escenario: Dashboard ESIOS con asistente IA

Problema actual: Inference lento en MicroVM (1vCPU)
Solución: Speculative decoding con EAGLE-3

Arquitectura propuesta:
┌─────────────────────────────────────────────┐
│  MicroVM (1vCPU, 2GB)                       │
│  ┌───────────────────────────────────────┐  │
│  │  Target: Llama-3.2-3B (INT4)          │  │
│  │  Draft:  Feature-level (EAGLE-3)      │  │
│  │  Speedup esperado: 2.5×               │  │
│  └───────────────────────────────────────┘  │
│  ┌───────────────────────────────────────┐  │
│  │  vLLM con speculative decoding nativo │  │
│  │  + FlashAttention 2                   │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### 7.3 Conexión con Otros Temas de la Serie

- **State Space Models** → SWIFT usa la heterogeneidad SSM/Transformer
- **Quantization** → INT4/INT8 del target + drafter pequeño = máximo speedup
- **FlashAttention** → Complemento directo: FlashAttention acelera el forward del target, speculative acelera el número de forwards necesarios
- **LoRA/PEFT** → El training de Medusa heads es similar en espíritu a LoRA: añadir heads ligeros sobre el modelo base

---

## 8. Papers de Referencia

| # | Paper | Año | Key Contribution |
|---|-------|-----|-----------------|
| 1 | **Fast Inference from Transformers via Speculative Decoding** (Leviathan et al.) | 2022 | Paper fundacional. Introdujo speculative sampling. |
| 2 | **Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads** (Cai et al.) | 2024 | Heads auxiliares internos. Sin drafter externo. |
| 3 | **EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty** (Li et al.) | 2024 | Feature-level autoregression. Mejor acceptance rate. |
| 4 | **Dynamic Depth Decoding** (2024) | 2024 | Tree depth adaptativo. Optimiza EAGLE-2. |
| 5 | **TriForce: Lossless Acceleration of Long Sequence Generation with Hierarchical Speculative Decoding** (COLM 2024) | 2024 | Speculative decoding jerárquico para long context. |
| 6 | **SWIFT: On-the-Fly Self-Speculative Decoding** (ICLR 2025) | 2025 | Self-speculative sin entrenamiento. Aprovecha heterogeneidad. |
| 7 | **SpecBlock: Block-Iterative Speculative Decoding with Dynamic Tree Drafting** (2026) | 2026 | Combina drafting autoregresivo y paralelo en un tree dinámico. |

### Repositorios GitHub

| Repo | Stars | Descripción |
|------|-------|-------------|
| [Infini-AI-Lab/TriForce](https://github.com/Infini-AI-Lab/TriForce) | 281 | Hierarchical speculative decoding |
| [bassrehab/speculative-decoding](https://github.com/bassrehab/speculative-decoding) | 4 | Reference impl: EAGLE, Medusa, KV-cache |
| [hemingkx/SWIFT](https://github.com/hemingkx/SWIFT) | 69 | Self-speculative decoding (ICLR 2025) |
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | 60k+ | Soporte nativo de speculative decoding |

---

## 9. Lecciones Clave

1. **La calidad del drafter importa más que su velocidad.** Un drafter 2× más lento pero con acceptance rate 10% mayor es mejor.

2. **Feature-level > Token-level.** La autoregression sobre features continuos es inherentemente más predecible que sobre tokens discretos.

3. **Tree > Linear.** Un árbol de depth=3, width=3 explora 40 nodos vs 3 lineales → acceptance rate efectivo mucho mayor.

4. **Self-speculative es el futuro.** SWIFT demuestra que puedes extraer drafter del propio modelo sin entrenamiento adicional.

5. **El bottleneck real es el target forward, no el draft.** Por eso tree speculative (un solo target forward para muchos nodos) es tan efectivo.

---

## 10. Próximos Pasos Sugeridos

1. **Implementar EAGLE-style feature drafter** en PyTorch y benchmarkear en la MicroVM
2. **Probar vLLM speculative decoding** con Llama-3.2-3B INT4
3. **Evaluar SWIFT** para modelos híbridos (SSM + Transformer)
4. **Benchmark de acceptance rate** vs tamaño del drafter para el stack ESIOS

---

## 11. Tema Siguiente Sugerido: **LoRA / PEFT**

**Por qué:**
- Complementa directamente esta nota de speculative decoding (ambos son técnicas de inference/fine-tuning eficiente)
- Esencial para customizar modelos en la MicroVM sin reentrenar desde cero
- Conexión directa con Medusa (los heads auxiliares de Medusa son esencialmente adapters)
- Alta relevancia práctica: David podría querer fine-tunar un modelo para el dashboard ESIOS

**Alternativa:** **RAG (Retrieval-Augmented Generation)** — directamente aplicable al sistema de ChromaDB existente, muy relevante para el stack actual.

---

*Hecho con (L) por David Antizar — Mastermind ejecutor*
