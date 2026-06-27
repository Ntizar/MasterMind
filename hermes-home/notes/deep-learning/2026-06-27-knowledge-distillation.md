# Knowledge Distillation — Compresión Inteligente de Modelos

**Fecha:** 2026-06-27
**Tipo:** Aprendizaje profundo — Compresión de modelos
**Prerequisites:** Redes neuronales, overfitting, training loops

---

## 1. El Problema que Resuelve

Los modelos grandes (GPT-4, Claude, ResNet-152, ViT-L) tienen un rendimiento excelente pero requieren:
- GPU costosa (A100, V100)
- Memoria enorme (80GB+)
- Latencia alta en inferencia

**Knowledge Distillation (KD)** es el arte de transferir el conocimiento de un modelo grande (teacher) a uno pequeño (student) que pueda correr en el edge, en microVMs de 2GB, o en dispositivos móviles.

> **Analogía:** No se trata de que el estudiante memorice las respuestas del profesor, sino de que aprenda *cómo piensa* el profesor.

---

## 2. Historia y Evolución

| Año | Paper | Tipo | Contribución |
|-----|-------|------|-------------|
| 2015 | Hinton et al. "Distilling..." | Logit-based | Temperatura en softmax, soft labels |
| 2015 | Romera-Paredes (Hint Matching) | Feature-based | Hidden layer distillation |
| 2016 | Srivastava et al. (PKD) | Feature-based | Propagación de conocimiento |
| 2017 | Liu et al. (FitNets) | Feature-based | Early-layer teaching |
| 2018 | Carion et al. (CRD) | Mutual | Information-theoretic |
| 2020 | Yuan et al. (Logit Distillation) | LLM | Pre-training LLMs small |
| 2021 | Jiao et al. (TinyBERT) | LLM | BERT small via KD |
| 2023 | Ye et al. (Minillm) | LLM | LLM small efficiently |
| 2024 | Shao et al. (STaR) | LLM | Self-taught reasoning |
| 2024 | Zhao et al. (SKD) | LLM | Systematic KD survey |
| 2026 | "When Context Returns" (arXiv:2606.11627) | LLM | On-policy distillation + context internalization |
| 2026 | "OPID" (arXiv:2606.26790) | RL | On-policy skill distillation for agents |
| 2026 | CoDistill-GRPO (arXiv:2605.08873) | RL | Co-distillation para GRPO |

**Lo nuevo:** KD se ha expandido más allá de clasificación a:
- Distilación de razonamiento (STaR, DPO como KD implícito)
- Distilación de agentes (skill-conditioned, on-policy)
- Distilación multimodal (VLMs → SNNs como en VL2Spike)

---

## 3. Los 4 Paradigmas de Knowledge Distillation

### 3.1 Response-Based KD (Logit-Level)

El estudiante replica las **salidas suaves** del teacher.

**Innovación clave de Hinton 2015:** temperatura T en softmax.

```
Softmax(z/T) = exp(z_i/T) / Σ_j exp(z_j/T)
```

- T=1 → softmax normal (distribución dura)
- T>1 → distribución suave (revela conocimiento negativo: "esta imagen NO es un perro")
- T<1 → distribución más dura

**Pérdida:**
```
L_KD = T² × KL(softmax(z_s/T) || softmax(z_t/T)) + L_CE(y, z_s)
```

El factor T² es un corrector de escala para mantener la varianza estable.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class ResponseKD(nn.Module):
    """Response-based Knowledge Distillation (Hinton et al., 2015)"""
    
    def __init__(self, student, teacher, alpha=0.5, temperature=4.0):
        super().__init__()
        self.student = student
        self.teacher = teacher
        self.alpha = alpha  # weight on KD loss
        self.T = temperature
        
    def forward(self, x, labels, teacher_labels=None):
        # Forward pass
        student_logits = self.student(x)
        with torch.no_grad():
            teacher_logits = self.teacher(x)
        
        # CE loss on hard labels
        ce_loss = F.cross_entropy(student_logits, labels)
        
        # KD loss on soft labels
        student_soft = F.log_softmax(student_logits / self.T, dim=1)
        teacher_soft = F.softmax(teacher_logits / self.T, dim=1)
        kd_loss = F.kl_div(student_soft, teacher_soft, reduction='batchmean') * (self.T ** 2)
        
        # Combined
        total_loss = (1 - self.alpha) * ce_loss + self.alpha * kd_loss
        
        return {
            'total_loss': total_loss,
            'ce_loss': ce_loss,
            'kd_loss': kd_loss,
            'student_logits': student_logits,
        }
```

### 3.2 Feature-Based KD (Intermediate-Level)

El estudiante alinea sus **representaciones intermedias** con las del teacher.

**Mecanismo:** Proyector lineal P que mapea feature_maps_student → feature_maps_teacher, luego MSE o L2.

```python
class FeatureKD(nn.Module):
    """Feature-based Knowledge Distillation (PKD / FitNets)"""
    
    def __init__(self, student, teacher, alpha=0.5, temperature=2.0):
        super().__init__()
        self.student = student
        self.teacher = teacher
        self.alpha = alpha
        self.T = temperature
        
        # Proyectores para mapear features del student a dim del teacher
        # Se definen según la arquitectura específica
        self.projectors = nn.ModuleDict({
            'layer1': nn.Linear(256, 512),  # example
            'layer2': nn.Linear(512, 1024),
        })
        
    def forward(self, x, labels, target_features):
        # Teacher features (sin gradiente)
        with torch.no_grad():
            teacher_features = self.teacher.extract_features(x)
        
        # Student features
        student_features = self.student.extract_features(x)
        
        # CE loss
        student_logits = self.student.classifier(x)
        ce_loss = F.cross_entropy(student_logits, labels)
        
        # Feature matching loss (por cada capa)
        feature_loss = 0
        for layer_name in student_features:
            projected = self.projectors[layer_name](student_features[layer_name])
            target = target_features[layer_name]
            feature_loss += F.mse_loss(projected, target)
        
        # Combined
        total_loss = (1 - self.alpha) * ce_loss + self.alpha * feature_loss
        
        return {
            'total_loss': total_loss,
            'ce_loss': ce_loss,
            'feature_loss': feature_loss,
        }
```

**Variante FitNets (2016):** Usa errores de pseudo-inversa como guía de *qué capa enseñar primero*. Capas con mayor error reciben más atención del teacher.

### 3.3 Relation-Based KD

El estudiante aprende las **relaciones entre muestras y entre features**, no solo las features individuales.

```python
class RelationKD(nn.Module):
    """Relation-based Knowledge Distillation (Lee & Hwang, 2018)"""
    
    def __init__(self, student, teacher, alpha=0.5):
        super().__init__()
        self.student = student
        self.teacher = teacher
        self.alpha = alpha
        
    def compute_relation_matrix(self, features):
        """Matriz de atención normalizada por fila (por columna también)."""
        # A = relu(F^T @ F) → relación entre samples
        att = F.relu(features.T @ features)
        return att / (att.sum(dim=1, keepdim=True) + 1e-6)
    
    def forward(self, x, labels):
        # Forward passes
        student_features = self.student.extract_features(x)
        with torch.no_grad():
            teacher_features = self.teacher.extract_features(x)
        
        # CE loss
        ce_loss = F.cross_entropy(self.student.classifier(x), labels)
        
        # Relation matrices
        student_att = self.compute_relation_matrix(student_features)
        teacher_att = self.compute_relation_matrix(teacher_features)
        
        # Relation loss
        relation_loss = F.kl_div(
            F.log_softmax(student_att, dim=1),
            F.softmax(teacher_att, dim=1),
            reduction='batchmean'
        )
        
        total_loss = (1 - self.alpha) * ce_loss + self.alpha * relation_loss
        
        return {'total_loss': total_loss, 'ce_loss': ce_loss, 'relation_loss': relation_loss}
```

### 3.4 Self-Distillation

El modelo se distila **a sí mismo**, usando diferentes augmentations, inicializaciones o épocas como teacher/student pair.

```python
class SelfDistillation(nn.Module):
    """
    Self-distillation: el modelo es su propio teacher.
    Dos variantes:
    1. Ensemble temporal: modelo en época t teacher → modelo en época t+1 student
    2. Augmentation ensembled: misma imagen con aug不同的 → mismo modelo
    """
    
    def __init__(self, model, alpha=0.3, temperature=4.0, 
                 aug1=None, aug2=None):
        super().__init__()
        self.model = model
        self.alpha = alpha
        self.T = temperature
        self.aug1 = aug1
        self.aug2 = aug2
        
    def forward(self, x1, x2, labels):
        """
        x1, x2 = misma imagen con diferentes augmentations
        """
        logits1 = self.model(x1)
        logits2 = self.model(x2)
        
        # CE en augmentation más fuerte (o ambas)
        ce_loss = F.cross_entropy(logits1, labels)
        
        # KD entre augmentations (auto-distillation)
        soft1 = F.log_softmax(logits1 / self.T, dim=1)
        soft2 = F.softmax(logits2 / self.T, dim=1)
        kd_loss = F.kl_div(soft1, soft2, reduction='batchmean') * (self.T ** 2)
        
        # Nota: las dos losses son simétricas
        soft2_inv = F.log_softmax(logits2 / self.T, dim=1)
        soft1_inv = F.softmax(logits1 / self.T, dim=1)
        kd_loss += F.kl_div(soft2_inv, soft1_inv, reduction='batchmean') * (self.T ** 2)
        
        total_loss = (1 - self.alpha) * ce_loss + self.alpha * kd_loss
        
        return {'total_loss': total_loss, 'ce_loss': ce_loss, 'kd_loss': kd_loss}
```

**Auto-KD (Wang et al., 2020):** Usa pseudo-labels del modelo entrenado como teacher, luego re-entrenar con esas pseudo-labels suavizadas. Mejora el accuracy ~2-3% sin teacher externo.

---

## 4. KD para LLMs (Lo Más Caliente)

Los LLMs introducen desafíos únicos:

### 4.1 Logit Distillation (Pre-training Level)

```python
class LLMLogitDistillation(nn.Module):
    """
    Distilación de logits para LLMs — el teacher genera
    soft targets en todo el vocabulario.
    
    Problema: vocabularios pueden ser muy grandes (32K-100K tokens),
    el cálculo de softmax sobre todo el vocab es O(V).
    """
    
    def __init__(self, student, teacher, alpha=0.5, temperature=2.0):
        super().__init__()
        self.student = student
        self.teacher = teacher
        self.alpha = alpha
        self.T = temperature
        
    def forward(self, input_ids, labels):
        # Student
        student_out = self.student(input_ids=input_ids, labels=labels)
        student_logits = student_out.logits  # [B, T, V]
        
        # Teacher (frozen, sin gradiente)
        with torch.no_grad():
            teacher_out = self.teacher(input_ids=input_ids)
            teacher_logits = teacher_out.logits
        
        # KL divergence sobre vocab
        student_log_probs = F.log_softmax(
            student_logits.view(-1, student_logits.size(-1)) / self.T, dim=-1
        )
        teacher_probs = F.softmax(
            teacher_logits.view(-1, teacher_logits.size(-1)) / self.T, dim=-1
        )
        
        kd_loss = F.kl_div(
            student_log_probs, teacher_probs, reduction='batchmean'
        ) * (self.T ** 2)
        
        # Ce sobre labels
        ce_loss = student_out.loss
        
        total = (1 - self.alpha) * ce_loss + self.alpha * kd_loss
        
        return {'total': total, 'ce': ce_loss, 'kd': kd_loss}
```

### 4.2 On-Policy Distillation (Training-Level)

Más potente que logit distillation: el teacher genera **trayectorias completas** (acciones, no solo logits).

```python
def on_policy_distillation(student, teacher, prompts, alpha=0.5, temperature=1.0):
    """
    On-policy KD: el teacher genera trayectorias completas,
    el student aprende de las acciones del teacher.
    
    Similar a DPO, pero el teacher es un modelo más grande,
    no preferencias humanas.
    """
    # 1. Teacher genera trajectories (sin gradiente)
    teacher_trajectories = []
    with torch.no_grad():
        for prompt in prompts:
            tokens = encode(prompt)
            trajectory = []
            current = tokens
            while not is_complete(current):
                logits = teacher(current).logits
                action = sample_from_soft(logits[:, -1, :], temperature=temperature)
                trajectory.append(action)
                current = torch.cat([current, action.unsqueeze(0)], dim=1)
            teacher_trajectories.append(trajectory)
    
    # 2. Student imita las trayectorias del teacher
    student_loss = 0
    for prompt, teacher_traj in zip(prompts, teacher_trajectories):
        tokens = encode(prompt)
        # Loss sobre las acciones del teacher
        student_logits = student(tokens + torch.tensor(teacher_traj).unsqueeze(0)).logits
        student_loss += F.cross_entropy(
            student_logits.view(-1, student_logits.size(-1)),
            (tokens + torch.tensor(teacher_traj)).view(-1)
        )
    
    # 3. Combine con KL regularización contra el modelo base
    base_logits = base_model(prompts + trajectories).logits
    kl_loss = F.kl_div(
        F.log_softmax(student_logits / temperature, dim=-1),
        F.softmax(base_logits / temperature, dim=-1),
        reduction='batchmean'
    )
    
    return student_loss + kl_loss
```

### 4.3 DPO como KD Implícito (Muy Importante)

El paper "Direct Preference Optimization" (Rafailov et al., 2023) puede interpretarse como **distilación implícita**:

```
DPO optimiza: log σ(β log(π_θ/π_ref) - β log(π_ref_w/π_ref_l))

Esto es equivalente a maximizar la probabilidad de acciones preferidas
por el teacher (modelo grande con rewards) sobre el student.

→ DPO es KD donde las preferencias vienen de un modelo, no de humanos.
```

### 4.4 STaR (Self-Taught Reasoner)

Zelikman et al. 2022 — el modelo genera sus propios datos de reasoning:

1. Entrenar modelo base en datos con reasoning
2. El modelo genera reasoning para problemas que no sabe
3. Filtra los que son correctos pero difíciles
4. Re-entrena con solo los reasoning generados correctos
5. Iterar

```python
# STaR pseudocódigo (simplificado)
def star_iteration(model, hard_questions, iterations=3):
    for it in range(iterations):
        # 1. Generar reasoning para hard questions
        generated_reasoning = []
        for q in hard_questions:
            try:
                reasoning = sample_with_chain_of_thought(model, q)
                if is_correct(reasoning, q):
                    generated_reasoning.append((q, reasoning))
            except:
                pass
        
        # 2. Re-entrenar con reasoning generados
        model = train_on_reasoning(model, generated_reasoning)
        
        # 3. Las preguntas "fáciles" ahora son hard para el nuevo modelo
        hard_questions = find_hard_questions(model, dataset)
        
        print(f"Iteration {it}: {len(generated_reasoning)} reasoning generados")
    
    return model
```

**Lo nuevo (2026):** Los papers de arXiv muestran que la on-policy distillation para agentes (OPID, CoDistill-GRPO) está integrando reasoning distillation con RL, donde el teacher no solo da logits sino **señales de densidad para sparse rewards**.

---

## 5. Implementación Completa: Distilación Práctica

```python
"""
Knowledge Distillation — Implementación práctica completa.
Compatible con HuggingFace transformers, PyTorch.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple
import math


@dataclass
class DistillationConfig:
    """Configuración flexible para cualquier tipo de KD."""
    
    # Tipos de KD a usar
    use_response_kd: bool = True
    use_feature_kd: bool = False
    use_relation_kd: bool = False
    use_self_kd: bool = True
    
    # Pesos
    ce_weight: float = 0.5
    response_kd_weight: float = 0.3
    feature_kd_weight: float = 0.2
    relation_kd_weight: float = 0.0
    
    # Temperatura
    response_temperature: float = 4.0
    feature_temperature: float = 2.0
    relation_temperature: float = 4.0
    
    # Alpha blending
    alpha: float = 0.5
    
    # Self-distillation
    self_kd_augmentation: str = "mask"  # "mask", "crop", "mixup"
    self_kd_temperature: float = 4.0


class DistillationLoss:
    """
    Loss de distilación unificado que combina múltiples señales.
    
    Soporta:
    - Response-based (logit-level)
    - Feature-based (intermediate-level)
    - Relation-based (attention-level)
    - Self-distillation
    """
    
    def __init__(self, config: DistillationConfig):
        self.config = config
        
        # Proyectores para feature matching
        self.feature_projectors = nn.ModuleDict({})
        
        # Temperatura annealing
        self.current_response_temp = config.response_temperature
        self.current_relation_temp = config.relation_temperature
    
    def response_kd_loss(
        self, student_logits: torch.Tensor,
        teacher_logits: torch.Tensor
    ) -> torch.Tensor:
        """Response-based KD (Hinton et al., 2015)."""
        T = self.current_response_temp
        
        student_soft = F.log_softmax(student_logits / T, dim=-1)
        teacher_soft = F.softmax(teacher_logits / T, dim=-1)
        
        kd_loss = F.kl_div(
            student_soft, teacher_soft,
            reduction='batchmean'
        ) * (T * T)
        
        return kd_loss
    
    def feature_kd_loss(
        self, student_features: torch.Tensor,
        teacher_features: torch.Tensor,
        layer_name: str
    ) -> torch.Tensor:
        """Feature-based KD con proyección."""
        T = self.config.feature_temperature
        
        # Proyectar features del student a dim del teacher
        if layer_name in self.feature_projectors:
            projected = self.feature_projectors[layer_name](student_features)
        else:
            # Si no hay proyección, MSE directo (deben coincidir dim)
            projected = student_features
        
        return F.mse_loss(projected, teacher_features.detach())
    
    def relation_kd_loss(
        self, student_att: torch.Tensor,
        teacher_att: torch.Tensor
    ) -> torch.Tensor:
        """Relation-based KD."""
        T = self.current_relation_temp
        
        student_rel = F.log_softmax(student_att / T, dim=-1)
        teacher_rel = F.softmax(teacher_att / T, dim=-1)
        
        return F.kl_div(
            student_rel, teacher_rel,
            reduction='batchmean'
        )
    
    def compute(
        self,
        student_logits: torch.Tensor,
        teacher_logits: torch.Tensor,
        student_features: Optional[Dict[str, torch.Tensor]] = None,
        teacher_features: Optional[Dict[str, torch.Tensor]] = None,
        student_att: Optional[torch.Tensor] = None,
        teacher_att: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        """Computa todas las señales de distilación."""
        losses = {}
        
        # CE hard label
        if labels is not None:
            losses['ce'] = F.cross_entropy(student_logits, labels)
        else:
            losses['ce'] = torch.tensor(0.0, device=student_logits.device)
        
        # Response KD
        if self.config.use_response_kd:
            losses['response_kd'] = self.response_kd_loss(
                student_logits, teacher_logits
            )
        
        # Feature KD
        if (self.config.use_feature_kd and student_features is not None 
            and teacher_features is not None):
            feature_loss = 0
            for layer in student_features:
                if layer in teacher_features:
                    feat_loss = self.feature_kd_loss(
                        student_features[layer],
                        teacher_features[layer],
                        layer
                    )
                    feature_loss += feat_loss
            losses['feature_kd'] = feature_loss / max(len(student_features), 1)
        
        # Relation KD
        if (self.config.use_relation_kd and student_att is not None 
            and teacher_att is not None):
            losses['relation_kd'] = self.relation_kd_loss(
                student_att, teacher_att
            )
        
        # Total
        total = (
            (1 - self.config.alpha) * losses['ce']
            + self.config.alpha * losses.get('response_kd', torch.tensor(0.0))
            + self.config.alpha * losses.get('feature_kd', torch.tensor(0.0))
            + self.config.alpha * losses.get('relation_kd', torch.tensor(0.0))
        )
        losses['total'] = total
        
        return losses
    
    def anneal_temperature(self, epoch: int, max_epochs: int, 
                           min_temp: float = 1.0):
        """Annealing de temperatura: T alto al inicio, T bajo al final."""
        progress = epoch / max_epochs
        self.current_response_temp = max(
            min_temp,
            self.config.response_temperature * (1 - progress) + min_temp * progress
        )
        self.current_relation_temp = max(
            min_temp,
            self.config.relation_temperature * (1 - progress) + min_temp * progress
        )


class DistillationTrainer:
    """
    Trainer completo para knowledge distillation.
    
    Uso:
        config = DistillationConfig()
        trainer = DistillationTrainer(student, teacher, config)
        trainer.train(train_loader, val_loader, epochs=10)
    """
    
    def __init__(self, student, teacher, config: DistillationConfig,
                 device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.student = student
        self.teacher = teacher
        self.config = config
        self.device = device
        
        self.loss_fn = DistillationLoss(config)
        
        # Optimizador del student
        self.optimizer = torch.optim.AdamW(
            student.parameters(),
            lr=3e-4,
            weight_decay=0.01
        )
        
        # Scheduler
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=100
        )
        
        self.teacher.eval()
        self.student.to(device)
        self.teacher.to(device)
    
    def train_epoch(self, dataloader, epoch: int, max_epochs: int):
        self.student.train()
        self.loss_fn.anneal_temperature(epoch, max_epochs)
        
        total_loss = 0
        correct = 0
        total = 0
        
        for batch_idx, (inputs, labels) in enumerate(dataloader):
            inputs, labels = inputs.to(self.device), labels.to(self.device)
            
            # Forward
            student_out = self.student(inputs)
            with torch.no_grad():
                teacher_out = self.teacher(inputs)
            
            student_logits = student_out.logits
            teacher_logits = teacher_out.logits
            
            # Loss
            losses = self.loss_fn.compute(
                student_logits=student_logits,
                teacher_logits=teacher_logits,
                labels=labels
            )
            
            # Backward
            self.optimizer.zero_grad()
            losses['total'].backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(
                self.student.parameters(), max_norm=1.0
            )
            
            self.optimizer.step()
            
            # Metrics
            total_loss += losses['total'].item()
            pred = student_logits.argmax(dim=1)
            correct += (pred == labels).sum().item()
            total += labels.size(0)
            
            if batch_idx % 50 == 0:
                print(f"  Batch {batch_idx}/{len(dataloader)}, "
                      f"Loss: {losses['total'].item():.4f}, "
                      f"Acc: {correct/total*100:.1f}%")
        
        self.scheduler.step()
        
        return {
            'loss': total_loss / len(dataloader),
            'accuracy': correct / total,
        }
    
    @torch.no_grad()
    def evaluate(self, dataloader) -> Dict[str, float]:
        self.student.eval()
        correct = 0
        total = 0
        
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(self.device), labels.to(self.device)
            outputs = self.student(inputs)
            pred = outputs.logits.argmax(dim=1)
            correct += (pred == labels).sum().item()
            total += labels.size(0)
        
        return {'accuracy': correct / total}
    
    def train(self, train_loader, val_loader, epochs: int = 10):
        best_acc = 0
        
        for epoch in range(epochs):
            print(f"\n=== Epoch {epoch+1}/{epochs} ===")
            print(f"  Response Temp: {self.loss_fn.current_response_temp:.2f}")
            
            train_metrics = self.train_epoch(train_loader, epoch, epochs)
            val_metrics = self.evaluate(val_loader)
            
            print(f"  Train Loss: {train_metrics['loss']:.4f}, "
                  f"Acc: {train_metrics['accuracy']*100:.1f}%")
            print(f"  Val Acc: {val_metrics['accuracy']*100:.1f}%")
            
            if val_metrics['accuracy'] > best_acc:
                best_acc = val_metrics['accuracy']
                torch.save(
                    self.student.state_dict(),
                    'best_student.pt'
                )
        
        return {'best_val_accuracy': best_acc}


# ============================================================
# Self-Distillation Training (sin teacher externo)
# ============================================================

class SelfDistillationTrainer:
    """
    Self-distillation: no necesitas un teacher externo.
    El modelo se distila a sí mismo con diferentes augmentations.
    """
    
    def __init__(self, model, augmentation_fn, 
                 alpha=0.3, temperature=4.0):
        self.model = model
        self.augmentation_fn = augmentation_fn
        self.alpha = alpha
        self.temperature = temperature
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
    
    def train_batch(self, images, labels):
        # Dos augmentations diferentes de las mismas imágenes
        img1, img2 = self.augmentation_fn(images)
        
        # Forward en ambas
        logits1 = self.model(img1)
        logits2 = self.model(img2)
        
        # CE en la aug más fuerte
        ce_loss = F.cross_entropy(logits1, labels)
        
        # KD entre las dos augmentations (bidireccional)
        soft1 = F.log_softmax(logits1 / self.temperature, dim=-1)
        soft2 = F.log_softmax(logits2 / self.temperature, dim=-1)
        teacher1 = F.softmax(logits1 / self.temperature, dim=-1)
        teacher2 = F.softmax(logits2 / self.temperature, dim=-1)
        
        kd_loss = (
            F.kl_div(soft1, teacher2, reduction='batchmean') +
            F.kl_div(soft2, teacher1, reduction='batchmean')
        ) * (self.temperature ** 2)
        
        total = (1 - self.alpha) * ce_loss + self.alpha * kd_loss
        
        self.optimizer.zero_grad()
        total.backward()
        self.optimizer.step()
        
        return {'total': total.item(), 'ce': ce_loss.item(), 'kd': kd_loss.item()}


# ============================================================
# LLM Distillation con HuggingFace
# ============================================================

def llm_kd_example():
    """
    Ejemplo de KD para LLMs con transformers.
    
    Teacher: large model (ej. Llama-3-8B)
    Student: small model (ej. TinyLlama-1.1B)
    
    Estrategia: logit distillation con vocabulario filtrado.
    """
    from transformers import AutoModelForCausalLM, AutoTokenizer
    
    # Cargar modelos
    teacher = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-3-8B')
    student = AutoModelForCausalLM.from_pretrained('TinyLlama/TinyLlama-1.1B')
    
    # Freeze teacher
    for param in teacher.parameters():
        param.requires_grad = False
    teacher.eval()
    
    # Config KD
    alpha = 0.5
    temperature = 2.0
    
    # Training loop
    # for input_ids, labels in dataloader:
    #     student_out = student(input_ids=input_ids, labels=labels)
    #     with torch.no_grad():
    #         teacher_out = teacher(input_ids=input_ids)
    #     
    #     # CE loss
    #     ce_loss = student_out.loss
    #     
    #     # KD loss (logit-level)
    #     student_logits = student_out.logits
    #     teacher_logits = teacher_out.logits
    #     
    #     student_log_probs = F.log_softmax(
    #         student_logits.view(-1, student_logits.size(-1)) / temperature, dim=-1
    #     )
    #     teacher_probs = F.softmax(
    #         teacher_logits.view(-1, teacher_logits.size(-1)) / temperature, dim=-1
    #     )
    #     
    #     kd_loss = F.kl_div(
    #         student_log_probs, teacher_probs, reduction='batchmean'
    #     ) * (temperature ** 2)
    #     
    #     total_loss = (1 - alpha) * ce_loss + alpha * kd_loss
    #     total_loss.backward()
    #     optimizer.step()
    
    return teacher, student


# ============================================================
# Utilidades: Softmax con temperatura
# ============================================================

def temperature_softmax(logits, temperature):
    """Softmax con temperatura custom."""
    scaled = logits / temperature
    max_vals = scaled.max(dim=-1, keepdim=True).values
    exp_scaled = torch.exp(scaled - max_vals)  # numerical stability
    return exp_scaled / exp_scaled.sum(dim=-1, keepdim=True)


def distillation_temperature_schedule(epoch, max_epoch, start_temp=8.0, 
                                       end_temp=1.0):
    """
    Schedule de temperatura para distilación.
    
    T alto al inicio → estudiante explora el espacio de distribuciones del teacher.
    T bajo al final → estudiante refina las predicciones.
    """
    progress = epoch / max_epoch
    # Curva cosine
    return end_temp + 0.5 * (start_temp - end_temp) * (1 + math.cos(math.pi * progress))


# ============================================================
# Ejemplo de proyección de features para ViT
# ============================================================

def extract_features_with_projectors(vit_teacher, vit_student, image):
    """
    Extrae features intermedios de ViT y calcula feature matching loss.
    
    ViT expone patches + cls token en cada layer.
    Usamos layers intermedios para feature distillation.
    """
    # Teacher (sin gradiente)
    with torch.no_grad():
        teacher_output = vit_teacher(
            image, output_hidden_states=True
        )
        teacher_hidden = teacher_output.hidden_states  # tuple de Tensors
    
    # Student
    student_output = vit_student(
        image, output_hidden_states=True
    )
    student_hidden = student_output.hidden_states
    
    # Feature matching entre layers intermedios (no input ni output)
    layers_to_match = [6, 12, 18]  # ejemplo para ViT-B/16
    feature_loss = torch.tensor(0.0, device=image.device)
    
    for t_layer, s_layer in zip(layers_to_match, 
                                  [l - 2 for l in layers_to_match]):
        t_feat = teacher_hidden[t_layer]  # [B, seq_len, D_t]
        s_feat = student_hidden[s_layer]  # [B, seq_len, D_s]
        
        # Proyectar si dims diferentes
        if s_feat.size(-1) != t_feat.size(-1):
            proj = nn.Linear(s_feat.size(-1), t_feat.size(-1)).to(image.device)
            s_feat = proj(s_feat)
        
        feature_loss += F.mse_loss(s_feat, t_feat)
    
    return feature_loss


# ============================================================
# Self-Distillation con Mixed Augmentation (SD-MixAug)
# ============================================================

def sd_mixaup(student, images, labels, alpha_mix=0.2, temperature=4.0):
    """
    Self-distillation con mixup.
    
    Dos samples se mezclan y el student aprende de ambas perspectivas.
    """
    # Mixup: combinar dos samples
    batch_size = images.size(0)
    lam = torch.distributions.Beta(alpha_mix, alpha_mix).sample((batch_size, 1, 1, 1))
    lam = lam.to(images.device)
    
    idx = torch.randperm(batch_size)
    
    mixed_images = lam * images + (1 - lam) * images[idx]
    mixed_labels = lam * labels + (1 - lam) * labels[idx]
    
    # Forward
    logits = student(mixed_images)
    
    # CE con labels mezclados (suavizados)
    ce_loss = F.cross_entropy(logits, mixed_labels)
    
    # Self-distillation: el modelo también predice las mixup targets
    # como soft labels
    soft_logits = F.log_softmax(logits / temperature, dim=-1)
    mixed_labels_soft = F.log_softmax(mixed_labels / temperature, dim=-1)
    sd_loss = F.kl_div(soft_logits, mixed_labels_soft, reduction='batchmean')
    
    total = (1 - 0.3) * ce_loss + 0.3 * sd_loss
    
    return total
```

---

## 6. Prácticas Recomendadas

### Cuándo usar cada tipo de KD:

| Escenario | Tipo recomendado | ¿Por qué? |
|-----------|-----------------|-----------|
| Imagen classification | Response + Feature | Ambos dan +2-4% accuracy |
| NLP / BERT | Response-only | Feature maps difíciles de alinear en texto |
| LLM reasoning | On-policy + STaR | Reasoning es una secuencia de acciones |
| Edge deployment | Response + Relation | Preserva semántica sin features |
| Self-distillation | Self + MixAug | Sin teacher externo, solo augments |
| RL agent distillation | On-policy skill | Sparse rewards → dense signal del teacher |

### Hiperparámetros clave:

1. **Temperatura:** Empezar con T=4-8, anneal a T=1.0
2. **Alpha:** Empezar con 0.3-0.5, ajustar según cuánto quieres distilar vs. hard labels
3. **Capas para feature KD:** Layers 30-70% de profundidad (no las primeras ni las últimas)
4. **Learning rate del student:** 1/5 a 1/10 del learning rate del teacher original

### Pitfalls:

- **Teacher overfitting:** Si el teacher está sobre-entrenado, el student aprende sus errores. Usar early stopping o ensemble de teachers.
- **Capacity gap muy grande:** Si el student es demasiado pequeño, no puede aprender las representaciones del teacher. Regla: el student debe tener al menos 25-50% de la capacidad del teacher.
- **Distillation sobre logits con vocab grande:** Para LLMs con vocab 100K+, calcular softmax sobre todo el vocab es costoso. Filtrar top-K tokens (logits-top-K distillation).
- **Over-regularización:** Si KD weight es muy alto, el student se queda en el mínimo del teacher y no puede mejorar. Balancear con CE loss.

---

## 7. Benchmarks Clave

| Student | Teacher | Dataset | Original Acc | KD Acc | Gap |
|---------|---------|---------|-------------|--------|-----|
| ResNet-18 | ResNet-152 | CIFAR-10 | 93.2% | 94.8% | +1.6% |
| MobileNetV2 | ResNet-152 | ImageNet | 72.6% | 74.5% | +1.9% |
| TinyBERT | BERT-base | GLUE | 78.3% | 81.1% | +2.8% |
| DistilBERT | BERT-base | GLUE | 97% BERT | 97.5% | +0.5% (93% params) |
| Llama-3-8B | Llama-3-70B | MMLU | 66% | 71% | +5% |
| Qwen2.5-1.5B | Qwen2.5-72B | MMLU | 53% | 58% | +5% |

---

## 8. Papers de Referencia

### Fundamentales:
1. **Hinton et al. (2015)** — "Distilling the Knowledge in a Neural Network" — *El paper original. Logit distillation con temperatura.*
2. **Romera-Paredes et al. (2015)** — "Hint Matching" — *Feature distillation.*
3. **Srivastava et al. (2015)** — "Deep Fragment Embeddings for Early-Layer Teaching" — *PKD.*
4. **Sanh et al. (2019)** — "DistilBERT" — *BERT pequeño, 40% más rápido, 97% accuracy.*

### LLM KD:
5. **Jiao et al. (2020)** — "TinyBERT" — *Distilling BERT for pre-training.*
6. **Zelikman et al. (2022)** — "STaR" — *Self-taught reasoning.*
7. **Rafailov et al. (2023)** — "Direct Preference Optimization" — *DPO como KD implícito.*

### Recientes (2024-2026):
8. **Zhao et al. (2024)** — "A Comprehensive Survey on Knowledge Distillation" — *Survey exhaustiva.*
9. **arXiv:2606.11627** — "When Context Returns: Toward Robust Internalization in On-Policy Distillation" — *Context internalization.*
10. **arXiv:2606.26790** — "OPID: On-Policy Skill Distillation for Agentic RL" — *Skill distillation para agentes.*
11. **arXiv:2605.08873** — "CoDistill-GRPO: A Co-Distillation Recipe for GRPO" — *Distilación co-entrenada con RL.*

### Repositorios útiles:
- [huggingface/distillation](https://github.com/huggingface/distillation) — Herramientas oficiales HF para distilación
- [OpenAI/evaluation](https://github.com/openai/evals) — Evaluación de LLMs pequeños vs grandes
- [microsoft/DeepSpeed](https://github.com/microsoft/DeepSpeed) — DeepSpeed-Lite para distilación eficiente

---

## 9. Código Ejecutable Mínimo

```python
"""
Mini-demo autocontenido: KD en CIFAR-10 con PyTorch puro.
"""
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

# 1. Datos
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, 4),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), 
                         (0.2470, 0.2435, 0.2616)),
])

train_dataset = torchvision.datasets.CIFAR10(
    root='/tmp/data', train=True, download=True, transform=transform
)
test_dataset = torchvision.datasets.CIFAR10(
    root='/tmp/data', train=False, download=True, transform=transforms.ToTensor()
)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=128, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=128)

# 2. Modelo "Teacher" (grande)
class TeacherNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(256, 10),
        )
    
    def forward(self, x):
        return self.classifier(self.features(x))

# 3. Modelo "Student" (pequeño)
class StudentNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(32, 10),
        )
    
    def forward(self, x):
        return self.classifier(self.features(x))

# 4. Entrenamiento del teacher (normal)
teacher = TeacherNet()
teacher_optimizer = optim.Adam(teacher.parameters(), lr=1e-3)
teacher_loss_fn = nn.CrossEntropyLoss()
teacher.eval()  # Freeze durante distillation

print("=== Entrenando Teacher ===")
for epoch in range(5):
    teacher.train()
    for images, labels in train_loader:
        teacher_optimizer.zero_grad()
        out = teacher(images)
        loss = teacher_loss_fn(out, labels)
        loss.backward()
        teacher_optimizer.step()
    print(f"  Epoch {epoch+1}: loss = {loss.item():.4f}")

# 5. Knowledge Distillation
student = StudentNet()
student_optimizer = optim.AdamW(student.parameters(), lr=3e-4)
T = 4.0  # Temperatura
alpha = 0.5  # Peso de KD vs CE

print("\n=== Knowledge Distillation ===")
for epoch in range(10):
    student.train()
    for images, labels in train_loader:
        student_optimizer.zero_grad()
        
        # Forward
        student_logits = student(images)
        with torch.no_grad():
            teacher_logits = teacher(images)
        
        # CE loss (hard labels)
        ce_loss = nn.CrossEntropyLoss()(student_logits, labels)
        
        # KD loss (soft labels con temperatura)
        soft_student = torch.log_softmax(student_logits / T, dim=1)
        soft_teacher = torch.softmax(teacher_logits / T, dim=1)
        kd_loss = torch.nn.KLDivLoss(reduction='batchmean')(
            soft_student, soft_teacher
        ) * (T * T)
        
        # Loss total
        total_loss = (1 - alpha) * ce_loss + alpha * kd_loss
        total_loss.backward()
        student_optimizer.step()
    
    print(f"  Epoch {epoch+1}: CE={ce_loss.item():.4f}, KD={kd_loss.item():.4f}, Total={total_loss.item():.4f}")

# 6. Evaluación
student.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        out = student(images)
        pred = out.argmax(dim=1)
        correct += (pred == labels).sum().item()
        total += labels.size(0)

print(f"\n=== Student Accuracy: {correct/total*100:.2f}% ===")

# Compare con student sin KD (baseline)
student_baseline = StudentNet()
student_baseline_optimizer = optim.AdamW(student_baseline.parameters(), lr=3e-4)
print("\n=== Training Student Baseline (sin KD) ===")
for epoch in range(10):
    student_baseline.train()
    for images, labels in train_loader:
        student_baseline_optimizer.zero_grad()
        out = student_baseline(images)
        loss = nn.CrossEntropyLoss()(out, labels)
        loss.backward()
        student_baseline_optimizer.step()

student_baseline.eval()
correct_b = 0
total_b = 0
with torch.no_grad():
    for images, labels in test_loader:
        out = student_baseline(images)
        pred = out.argmax(dim=1)
        correct_b += (pred == labels).sum().item()
        total_b += labels.size(0)

print(f"=== Baseline Accuracy (sin KD): {correct_b/total_b*100:.2f}% ===")
print(f"=== Improvement with KD: {(correct/total - correct_b/total_b)*100:.2f}% ===")
```

---

## 10. Resumen Técnico

**Knowledge Distillation** es el método más práctico y efectivo para comprimir modelos grandes en pequeños. Sus variantes principales:

- **Response-based** (Hinton 2015): usa soft labels de softmax con temperatura. Simple, efectivo para casi todo.
- **Feature-based** (PKD/FitNets): alinea representaciones intermedias. Requiere proyectores pero captura semántica rica.
- **Relation-based**: alinea relaciones entre samples. Útil cuando las features directas no son alineables.
- **Self-distillation**: sin teacher externo, usa augmentations diferentes de los mismos datos.
- **On-policy / LLM distillation**: el nuevo frontier. El teacher genera trayectorias completas (acciones, reasoning), el student aprende del comportamiento, no solo de los logits.

**Lo más relevante para tu infraestructura (NaN MicroVM 1vCPU/2GB):**
1. Distila Qwen2.5-7B → Qwen2.5-1.5B o Qwen2.5-0.5B para tener LLMs que corran en 2GB
2. Usa response-based KD con T=4-8 y anneal a T=1
3. Para LLMs, filtrar top-K tokens del vocab en el cálculo de softmax
4. La distilación on-policy es el futuro: no solo logits, sino reasoning traces

**El próximo tema lógico:** **Structured Pruning** — otra técnica de compresión que complementa perfectamente a KD. O bien **Mixture of Experts** (ya cubierto) → **Speculative Decoding** (ya cubierto) → **Model Routing / MoE en Inference** — cómo mezclar múltiples modelos pequeños en tiempo de inferencia para imitar un modelo grande.

**Siguiente tema propuesto:** **Structured Pruning & Early Exiting** — compresión via eliminación de pesos/parámetros y salidas tempranas en redes. Complementa KD perfectamente y es orthogonal.
