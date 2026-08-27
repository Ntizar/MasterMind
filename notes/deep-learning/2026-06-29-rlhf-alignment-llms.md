# RLHF y Técnicas de Alineación de Modelos de Lenguaje

## 1. Introducción

Los modelos de lenguaje grandes (LLMs) preentrenados con objetivo de next-token prediction son poderosos pero carecen de alineación con las intenciones humanas. RLHF (Reinforcement Learning from Human Feedback) y sus alternativas modernas son el conjunto de técnicas que transforman un modelo base genérico en un asistente útil, honesto y seguro.

### ¿Por qué es necesario alinear?

Un modelo preentrenado puede:
- Generar respuestas incorrectas o alucinadas
- Producir contenido dañino o sesgado
- No seguir instrucciones
- Ser demasiado verboso o insuficiente

La alineación ajusta el modelo para que sus salidas coincidan con las preferencias humanas.

---

## 2. Pipeline Clásico de RLHF (InstructGPT, 2022)

El pipeline de RLHF consta de **4 fases secuenciales**:

```
┌─────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌──────────────┐
│  SFT Phase   │───▶│  Reward Modeling │───▶│  RL Training │───▶│  Deploy Model │
│ (fine-tune)  │    │  (train reward)  │    │  (PPO)       │    │   (aligned)  │
└─────────────┘    └──────────────────┘    └──────────────┘    └──────────────┘
```

### Fase 1: Supervised Fine-Tuning (SFT)

Se fine-tuna el modelo base con un dataset de instrucciones de alta calidad:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

# Cargar modelo base y tokenizer
model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Dataset de ejemplo (instruction-response pairs)
train_data = [
    {"instruction": "¿Qué es la fotosíntesis?", "response": "La fotosíntesis es el proceso..."},
    {"instruction": "Escribe un poema sobre el mar", "response": "En la inmensidad oceánica..."},
]

# Tokenizar
def tokenize_function(examples):
    texts = [f"{e['instruction']}\n\n{e['response']}" for e in examples]
    return tokenizer(texts, truncation=True, padding="max_length", max_length=512)
```

### Fase 2: Reward Modeling (RM)

Se entrena un modelo separado (Reward Model) que predice qué tan bien una respuesta alinea con las preferencias humanas.

```python
# Dataset de pares ordenados: (chosen, rejected)
# "chosen" = respuesta preferida por humanos
# "rejected" = respuesta no preferida
reward_data = [
    {"prompt": "¿Qué es la fotosíntesis?", "chosen": respuesta_experta, "rejected": respuesta_vaga},
    # ... miles de ejemplos
]

# El Reward Model aprende a maximizar la diferencia:
# Loss = -log(σ(r(x, y_chosen) - r(x, y_rejected)))
# donde r es la función de recompensa aprendida
```

El Reward Model típicamente es un transformer con head de clasificación binaria.

### Fase 3: Reinforcement Learning (PPO)

Se usa el Reward Model para optimizar el modelo con Proximal Policy Optimization (PPO):

```python
# Flujo de PPO en RLHF:
# 1. Generar respuestas con el modelo policy (actor)
# 2. Evaluar con el Reward Model (scoring)
# 3. Calcular advantage con GAE (Generalized Advantage Estimation)
# 4. Actualizar policy con PPO loss
# 5. Regularizar con KL penalty para no desviarse del modelo SFT

# PPO Loss simplificado:
# L = E[min(ratio * advantage, clip(ratio, 1-ε, 1+ε) * advantage)]
# donde ratio = π_θ(a|s) / π_ref(a|s)
# Y se añade KL penalty: L_total = L_PPO - β * KL(π_θ || π_SFT)
```

**Problemas del pipeline RLHF clásico:**
- Requiere 4 modelos distintos (SFT, RM, Actor, Critic)
- PPO es inestable y difícil de tunearear
- Coste computacional enorme
- El Reward Model puede aprender recompensas incorrectas (reward hacking)

---

## 3. DPO — Direct Preference Optimization (Rafael et al., 2023)

**Paper original:** ["DPO: Direct Preference Optimization"](https://arxiv.org/abs/2305.18290)

DPO elimina la necesidad del Reward Model y PPO, optimizando directamente la política de preference con una única función de pérdida.

### Idea central

DPO demuestra que el problema de optimización de RLHF puede reformularse como una **optimización directa sobre preferencias**:

```
Maximizar: E[log π_θ(y|xs)] - β * KL(π_θ || π_ref)
Sujeto a: π_Preference = argmax E[r_φ(x,y)]
```

La clave: **no necesitas un reward model**. La función de recompensa puede derivarse analíticamente de la política.

### La pérdida DPO

```python
import torch
import torch.nn.functional as F

def dpo_loss(policy_chosen, policy_rejected, ref_chosen, ref_rejected, beta=0.1):
    """
    Pérdida DPO (Direct Preference Optimization)
    
    Args:
        policy_chosen: log-probs del policy para chosen
        policy_rejected: log-probs del policy para rejected
        ref_chosen: log-probs del modelo de referencia (SFT) para chosen
        ref_rejected: log-probs del modelo de referencia para rejected
        beta: temperatura de regularización KL
    
    Returns:
        Scalar loss
    """
    # Diferencia de log-probs
    chosen_log_ratios = policy_chosen - ref_chosen
    rejected_log_ratios = policy_rejected - ref_rejected
    
    # DPO Loss: maximize margin between chosen and rejected
    # L_DPO = -E[log(σ(β * log(π(y_chosen|x)/π_ref(y_chosen|x)) - β * log(π(y_rejected|x)/π_ref(y_rejected|x))))]
    losses = -F.logsigmoid(beta * (chosen_log_ratios - rejected_log_ratios))
    
    return losses.mean()

# Ejemplo de entrenamiento:
# for batch in dataloader:
#     chosen_log_probs = model(batch.prompt, batch.chosen, return_logits=True)
#     rejected_log_probs = model(batch.prompt, batch.rejected, return_logits=True)
#     ref_chosen = ref_model(batch.prompt, batch.chosen, return_logits=True)
#     ref_rejected = ref_model(batch.prompt, batch.rejected, return_logits=True)
#     loss = dpo_loss(chosen_log_probs, rejected_log_probs, 
#                     ref_chosen, ref_rejected, beta=0.1)
#     loss.backward()
#     optimizer.step()
```

### Ventajas de DPO sobre RLHF clásico:
- ✅ Elimina Reward Model → 1 modelo en vez de 4
- ✅ Elimina PPO → SGD simple
- ✅ Más estable y reproducible
- ✅ Menor coste computacional
- ✅ No necesita critic model

### Desventajas:
- ❌ Requiere datos de preferencia (chosen/rejected)
- ❌ La optimización es más restrictiva que PPO
- ❌ Puede tener peor rendimiento en algunos benchmarks

---

## 4. ORPO — Odds Ratio Preference Optimization (Menon et al., 2024)

**Paper:** ["ORPO: Monolithic Preference Optimization with Reference Model-Free Training and Language Modeling Losses"](https://arxiv.org/abs/2402.01714)

ORPO va un paso más allá: elimina el modelo de referencia y combina SFT + DPO en una sola fase.

```python
def orpo_loss(policy_chosen, policy_rejected, beta=0.1):
    """
    ORPO Loss — combina SFT loss con preference optimization
    sin modelo de referencia.
    """
    # Odds ratio: P(chosen) / P(rejected)
    log_odds = policy_chosen - policy_rejected
    
    # ORPO combines:
    # 1. NLL loss for chosen (SFT-like)
    # 2. Preference loss without reference model
    # Loss = -log(σ(log_odds - β)) - β * (π_ref/π) + ...
    
    # Simplificado:
    losses = -(F.logsigmoid(log_odds - beta) - beta * policy_chosen)
    
    return losses.mean()
```

### Innovación clave de ORPO:
1. **No necesita modelo de referencia** — elimina la necesidad de cargar el modelo SFT durante entrenamiento
2. **Combina SFT y Preference en una sola fase** — más eficiente
3. **Incorpora language modeling loss directamente** — el modelo aprende tanto a seguir instrucciones como a preferir respuestas correctas

---

## 5. KTO — Kahneman-Tversky Optimization

**Paper:** ["KTO: Optimizing Human Preference Alignment with Kahneman-Tversky Optimization"](https://arxiv.org/abs/2402.01306)

KTO utiliza datos etiquetados individualmente (no pares), usando la teoría de la perspectiva de Kahneman-Tversky.

```python
def kto_loss(policy_output, is_desired, beta=0.1):
    """
    KTO Loss — funciona con datos binarios (desired/undesired)
    sin necesidad de pares (chosen, rejected)
    """
    if is_desired:
        # Para ejemplos deseados: penalizar desviación del reference
        # L_desired = 1 - σ(β * (log π(y|x) - log π_ref(y|x)))
        loss = 1 - F.sigmoid(beta * policy_output)
    else:
        # Para ejemplos no deseados: penalizar alta probabilidad
        # L_undesired = 1 - σ(β * (log π_ref(y|x) - log π(y|x)))
        loss = F.sigmoid(-beta * policy_output)
    
    return loss.mean()
```

### Ventajas de KTO:
- ✅ Funciona con datos no emparejados (más fácil de obtener)
- ✅ Cada ejemplo tiene su propia etiqueta
- ✅ Similar rendimiento a DPO con datos más diversos

---

## 6. Rejection Sampling

La técnica más simple y efectiva: genera múltiples respuestas y selecciona las mejores.

```python
import torch

def rejection_sampling(model, tokenizer, prompt, n_samples=16, temperature=0.7):
    """
    Genera N respuestas y selecciona la mejor.
    Puede usarse para crear datasets de alta calidad para SFT/DPO.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    all_outputs = []
    for _ in range(n_samples):
        output = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=temperature,
            do_sample=True,
            top_p=0.9
        )
        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
        all_outputs.append(decoded)
    
    # Ordenar por alguna métrica (puede ser un reward model, 
    # heurísticas, o evaluación humana)
    # Para datasets de alta calidad:
    # scores = [reward_model(prompt, out) for out in all_outputs]
    # best = all_outputs[scores.argmax()]
    
    return all_outputs  # Devuelve todas para ranking/selección

# Rejection Sampling es la técnica usada por muchas bases de datos modernas:
# - OpenHermes 2.5: 1M samples generados por GPT-4 + rejection sampling
# - Dolphin: 2M samples con filtrado por calidad
```

---

## 7. Comparativa de Técnicas

| Técnica | Modelos | Datos | Estabilidad | Complejidad | Rendimiento |
|---------|---------|-------|-------------|-------------|-------------|
| **RLHF (PPO)** | 4 (SFT, RM, Actor, Critic) | Pares (chosen/rejected) | Baja | Muy Alta | Excelente |
| **DPO** | 1 (policy) + 1 (ref) | Pares (chosen/rejected) | Alta | Baja | Muy Bueno |
| **ORPO** | 1 (policy) | Pares (chosen/rejected) | Alta | Muy Baja | Muy Bueno |
| **KTO** | 1 (policy) + 1 (ref) | Individual (desired/undesired) | Alta | Baja | Bueno |
| **Rejection Sampling** | 1 (policy) | Múltiples respuestas | N/A | Muy Baja | Bueno (para data gen) |

### ¿Cuál elegir?

```
¿Tienes datos emparejados (chosen/rejected)?
├── Sí → ¿Necesitas rendimiento máximo sin importar complejidad?
│   ├── Sí → RLHF (PPO)
│   └── No → DPO o ORPO
│       └── ¿Quieres eliminar reference model?
│           ├── Sí → ORPO
│           └── No → DPO
└── No → ¿Tienes etiquetas individuales?
    ├── Sí → KTO
    └── No → Genera datos con rejection sampling + reward model
```

---

## 8. Implementación Práctica Completa con TRL

La librería [TRL (Transformer Reinforcement Learning)](https://github.com/huggingface/trl) de Hugging Face implementa todas estas técnicas:

```python
from trl import DPOTrainer, ORPOConfig, DPOConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

# Modelo base
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)
ref_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
tokenizer.pad_token = tokenizer.eos_token

# DPO Training con TRL
dpo_config = DPOConfig(
    beta=0.1,           # KL regularización weight
    learning_rate=5e-7,  # Learning rate muy bajo
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    max_steps=1000,
    logging_steps=10,
    save_steps=100,
    output_dir="./dpo-llama2-7b",
    bf16=True,           # Mixed precision
    remove_unused_columns=False,
)

dpo_trainer = DPOTrainer(
    model,
    ref_model,
    config=dpo_config,
    train_dataset=dataset,  # Dataset con "chosen" y "rejected"
    tokenizer=tokenizer,
)

dpo_trainer.train()
dpo_trainer.save_model("dpo-llama2-7b-final")

# ORPO Training (sin reference model)
orpo_config = ORPOConfig(
    beta=0.1,
    learning_rate=5e-7,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    output_dir="./orpo-llama2-7b",
)

orpo_trainer = DPOTrainer(
    model,
    config=orpo_config,
    train_dataset=dataset,
    tokenizer=tokenizer,
    ref_model=None,  # ¡Sin reference model!
)

orpo_trainer.train()
```

---

## 9. Aplicaciones en el Stack Actual

### Para el sistema de Mastermind / ESIOS:

1. **Generación de reportes personalizados**: Un modelo alineado puede generar informes más claros y útiles que un modelo genérico.

2. **Clasificación de anomalías**: Un DPO fine-tuned puede clasificar mejor las anomalías en datos ESIOS que un modelo genérico.

3. **Generación de insights**: Modelos alineados producen insights más accionables y menos "ruido".

### Para el stack de IA de David:

1. **Adela**: Los módulos de Adela podrían beneficiarse de models alineados para generar código más preciso y siguiendo las convenciones del proyecto.

2. **Control de calidad**: Un reward model ligero podría evaluar la calidad de respuestas generadas.

---

## 10. Referencias Clave

### Papers fundamentales:
1. **RLHF**: "Training language models to follow instructions with human feedback" (Ouyang et al., 2022) — [InstructGPT](https://arxiv.org/abs/2203.02155)
2. **DPO**: "DPO: Direct Preference Optimization" (Rafael et al., 2023) — [arXiv:2305.18290](https://arxiv.org/abs/2305.18290)
3. **ORPO**: "ORPO: Monolithic Preference Optimization" (Menon et al., 2024) — [arXiv:2402.01714](https://arxiv.org/abs/2402.01714)
4. **KTO**: "KTO: Optimizing Human Preference Alignment" (Ethayarajh et al., 2024) — [arXiv:2402.01306](https://arxiv.org/abs/2402.01306)
5. **Rejection Sampling**: "Simple Rejection Sampling Alignment" (Yuan et al., 2024)

### Implementaciones:
1. **TRL (Hugging Face)**: https://github.com/huggingface/trl
2. **Axolotl**: https://github.com/OpenAccess-AI-Collective/axolotl
3. **Axolotl**: https://github.com/OpenAccess-AI-Collective/axolotl

### Recursos educativos:
1. **"The Alignment Problem"**: Book por Brian Christian (2021)
2. **RLHF tutorial**: https://huggingface.co/docs/trl/main/en/dpo_trainer
3. **DPO explainer**: https://huggingface.co/blog/dpo-trl

---

## 11. Ejemplos de Datasets de Preferencia

| Dataset | Tamaño | Tipo | Fuente |
|---------|--------|------|--------|
| **UltraFeedback** | 1.3M | Pares + individual | Stanford |
| **UltraChat** | 1.5M | Instrucciones | BAAI |
| **RLHF-V** | 10K+ | Visual + texto | MIT |
| **hh-rlhf** | ~90K | Pares Reddit | Anthropic |
| **OpenHermes 2.5** | 1M | Instrucciones | Apple/Open |

---

## 12. Conclusión

RLHF y sus alternativas (DPO, ORPO, KTO) representan la frontera de la alineación de modelos de lenguaje. La evolución ha ido hacia técnicas **más simples** (menos modelos, menos hiperparámetros) pero **igualmente efectivas**.

**Recomendación para el stack actual**: DPO/ORPO son la mejor opción para la mayoría de casos prácticos. Son más simples, más estables, y el rendimiento es comparable al RLHF clásico. La librería TRL de Hugging Face hace la implementación trivial.

---

*Hecho con (L) por David Antizar — Mastermind es ejecutor, David es autor*
