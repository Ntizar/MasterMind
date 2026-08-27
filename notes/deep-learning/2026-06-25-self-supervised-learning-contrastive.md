# Self-Supervised Learning: Contrastive, Masked, y Self-Distillation

**Fecha:** 2026-06-25
**Autor:** Mastermind (David Antizar)

---

## Resumen Ejecutivo

El aprendizaje autosupervisado (SSL) es el paradigma de pre-entrenamiento que ha democratizado los modelos de visión por computadora. En lugar de necesitar datasets etiquetados manualmente, los modelos SSL aprenden representaciones útiles directamente de datos sin etiquetar — millones de imágenes, en algunos casos — y luego se fine-tunean en tareas específicas con muy pocas etiquetas.

**Por qué importa para el stack:**
- Las imágenes satelitales de Esios no están etiquadas con bounding boxes ni segmentation masks
- SSL permite crear embeddings de imágenes satelitales sin etiquetar
- Los features de DINOv2 se usan como backbone para detección, segmentación y clasificación downstream
- Con microVM (1 CPU, 2GB RAM), los modelos pre-entrenados con SSL son ligeros y eficientes

---

## Panorama General: Los Tres Pilares del SSL

El SSL moderno se organiza en tres paradigmas principales:

### 1. Contrastive Learning (Aprendizaje Contrastivo)

**Idea central:** Aumentar la misma imagen de dos formas distintas → los embeddings resultantes deben ser similares (positivos). Imágenes distintas → embeddings deben ser distintos (negativos).

```
Imagen original → Augmentation α → Vista positiva 1 (z₁)
                      → Augmentation β → Vista positiva 2 (z₂)

Imagen distinta    → Augmentation γ → Vista negativa 1 (z₃)
```

**El truco:** El modelo se entrena para maximizar la similitud entre z₁ y z₂, y minimizarla con todos los demás embeddings del batch (negativos).

### 2. Masked Image Modeling (Modelado con Máscaras)

**Idea central:** Enmascarar regiones aleatorias de la imagen → el modelo debe predecirlas. Similar a BERT pero con imágenes.

```
Imagen:  ████████
         ██▓▓▓▓██     ▓ = enmascarado (pixel=0)
         ██▓▓▓▓██
         ██▓▓▓▓██

Entrada: ██0000██
         ██0000██  →  Transformer  →  Predicción: ████████
         ██0000██
         ██0000██
```

### 3. Self-Distillation (Auto-Distilación)

**Idea central:** Dos vistas de la misma imagen producen dos "maestros" que se distilan mutuamente — sin necesidad de negativos ni etiquetas.

```
Imagen → Teacher (augmentación fuerte) → Soft labels (T alto)
         Student (augmentación fuerte) → Distil contra teacher loss
```

---

## SimCLR: El Marco Contrastivo Fundacional

**Paper:** "A Simple Framework for Contrastive Learning of Visual Representations" (Chen et al., 2020)
**Repositorio:** github.com/google-research/simclr

### Conceptos Clave

- **Augmentaciones:** Rotación, color jitter, crop aleatorio, flip horizontal, blur
- **Loss:** NT-Xent (Normalized Temperature-scaled Cross Entropy)
- **Batch grande necesario:** 4096 ejemplos para tener suficientes negativos

### Loss NT-Xent

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class NTXentLoss(nn.Module):
    """
    Loss de SimCLR: contrastivo con temperatura.
    
    Para cada par (z_i, z_j) de vistas de la misma imagen:
    - Numerador: exp(sim(z_i, z_j) / τ) — similitud del positivo
    - Denominador: numerador + Σ exp(sim(z_i, z_k) / τ) — todos los negativos
    
    El modelo maximiza la probabilidad de que los positivos sean más similares
    que cualquier negativo.
    """
    def __init__(self, batch_size, temperature=0.5):
        super().__init__()
        self.batch_size = batch_size
        self.temperature = temperature
        # Los positivos están en posiciones (i, i + batch_size) del concatenated batch
        self.negative_masks = (1 - torch.eye(batch_size * 2, batch_size * 2).repeat(1, 1))
        # Ignorar auto-similitud y similitud con la vista complementaria
        self.mask = self.negative_masks.clone()
        self.mask.diagonal(0).fill_(0)
        self.mask.diagonal(self.batch_size).fill_(0)
        self.mask.diagonal(-self.batch_size).fill_(0)
        
    def forward(self, z_i, z_j):
        """
        Args:
            z_i: embeddings de vista 1 (batch_size x dim)
            z_j: embeddings de vista 2 (batch_size x dim)
        Returns:
            loss escalar
        """
        # Concatenar: [z_1^1, z_1^2, z_2^1, z_2^2, ..., z_n^1, z_n^2]
        z = torch.cat([z_i, z_j], dim=0)  # (2*batch_size, dim)
        
        # Similaridad por coseno
        sim = torch.matmul(z, z.T) / self.temperature  # (2B, 2B)
        
        # Mask de negativos (excluyendo positives y auto-similitud)
        similarities = sim * self.mask
        # Máximo para estabilidad numérica
        max_sim = torch.max(similarities, dim=1)[0].unsqueeze(1)
        similarities = similarities - max_sim.detach()
        
        # Numerador: similitud del positivo
        positive_sim = torch.exp(sim.diagonal())  # (B,)
        
        # Denominador: positivo + todos los negativos
        numerator = torch.exp(similarities.diagonal())  # positivo
        denominator = torch.sum(torch.exp(similarities), dim=1)
        
        # Loss promedio
        loss = -torch.log(numerator / denominator + 1e-8).mean()
        return loss
```

### Augmentaciones Clave

```python
import torchvision.transforms as transforms

def get_simclr_transforms(size=224):
    """Transformaciones de SimCLR."""
    transform_list = [
        # Random crop y resize (variación de escala y posición)
        transforms.RandomResizedCrop(size, scale=(0.2, 1.0)),
        transforms.RandomHorizontalFlip(0.5),  # Flip aleatorio
        
        # Color augmentation (variación de color, contraste, brillo)
        transforms.RandomApply([
            transforms.ColorJitter(0.4, 0.4, 0.4, 0.1)
        ], p=0.8),
        transforms.RandomGrayscale(p=0.2),
        transforms.RandomGaussianBlur(kernel_size=3, sigma=(0.1, 2.0)),
        
        # Normalización
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225]),
    ]
    return transforms.Compose(transform_list)
```

---

## MoCo: Momentum Contrast — Negativos Eficientes

**Paper:** "Momentum Contrast for Unsupervised Visual Representations" (He et al., 2020)
**Innovación:** Colas de memoria (memory queue) + encoder momentum → negativos consistentes en batchs pequeños

### ¿Por qué funciona?

- SimCLR necesita batch de 4096 para tener suficientes negativos → costoso
- MoCo usa una cola de memoria que almacena embeddings del batch anterior
- El encoder de negativos tiene momentum del encoder positivo → representaciones estables
- Con batch de 256 y cola de 65536, MoCo > SimCLR con batch de 4096

### Implementación

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MoCoLoss(nn.Module):
    """
    Loss de MoCo v3.
    
    A diferencia de SimCLR:
    - Batch pequeño (256) en vez de 4096
    - Cola de memoria almacena negativos de batchs anteriores
    - Encoder de negativos tiene momentum update del positivo
    """
    def __init__(self, dim=128, queue_size=65536, temperature=0.07):
        super().__init__()
        self.dim = dim
        self.queue_size = queue_size
        self.temperature = temperature
        
        # Cola de memoria: embeddings de vistas negativas
        self.register_buffer("queue", torch.randn(dim, queue_size))
        self.queue = F.normalize(self.queue, dim=0)
        self.queue_ptr = nn.Parameter(torch.tensor(0), persistent=False)
        
    def forward(self, q, k):
        """
        Args:
            q: queries del batch actual (B x dim) — vista positiva 1
            k: keys del batch actual (B x dim) — vista positiva 2
            
        Returns:
            loss
        """
        B = q.shape[0]
        dim_k = k.shape[1]
        
        # Concatenar cola con keys actuales
        l_pos = torch.einsum('nc,nc->n', q, k).unsqueeze(-1)  # (B, 1)
        l_neg = torch.einsum('nc,ck->nk', q, self.queue.clone().detach())  # (B, queue_size)
        
        # Logits: [positivo, negativos]
        logits = torch.cat([l_pos, l_neg], dim=1)  # (B, 1 + queue_size)
        
        # Loss: el índice del positivo siempre es 0
        labels = torch.zeros(B, dtype=torch.long).to(q.device)
        loss = F.cross_entropy(logits / self.temperature, labels)
        
        # Update cola: FIFO (First In, First Out)
        with torch.no_grad():
            indices = self.queue_ptr % self.queue_size
            # Insertar keys actuales en la cola
            self.queue[:, indices] = F.normalize(k, dim=1).t()
            self.queue_ptr = self.queue_ptr + B
            
        return loss
```

---

## BYOL: Bootstrap Your Own Latent — Sin Negativos

**Paper:** "Bootstrap Your Own Latent (BYOL)" (Grill et al., 2020)
**Idea revolucionaria:** ¡No necesitas negativos! Dos redes que se distilan mutuamente con un predictor.

### Arquitecturas

```
                    ┌─────────────────────────────────────────┐
                    │              Teacher (θ)                  │
                    │  • Encoder f_θ (con momentum)            │
                    │  • Projector g_θ                         │
                    └─────────────────────────────────────────┘
                                         ↑
                                    momentum update
                                 θ ← τ·θ + (1-τ)·ϕ
                                        
                    ┌─────────────────────────────────────────┐
                    │              Student (ϕ)                 │
                    │  • Encoder f_ϕ                         │
                    │  • Projector g_ϕ                       │
                    │  • Predictor p_ϕ                       │
                    └─────────────────────────────────────────┘
```

### Implementación Completa

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import copy

class BYOL(nn.Module):
    """
    Bootstrap Your Own Latent (BYOL).
    
    Arquitectura triple:
    1. Student: encoder + projector + predictor (trainable)
    2. Teacher: encoder + projector (trainable via momentum)
    3. Predictor: MLP que proyecta el embedding del student
    
    Key insight: La red de predicción evita el colapso trivial
    (donde todas las salidas serían 0).
    """
    
    def __init__(self, encoder_dim=768, proj_dim=256, pred_dim=256, momentum=0.999):
        super().__init__()
        self.momentum = momentum
        
        # Student
        self.student_encoder = nn.Sequential(
            nn.Linear(encoder_dim, encoder_dim),
            nn.BatchNorm1d(encoder_dim),
            nn.ReLU(),
            nn.Linear(encoder_dim, proj_dim),
            nn.BatchNorm1d(proj_dim),
            nn.ReLU(),
        )
        self.student_predictor = nn.Sequential(
            nn.Linear(proj_dim, pred_dim),
            nn.BatchNorm1d(pred_dim),
            nn.ReLU(),
            nn.Linear(pred_dim, proj_dim),
        )
        
        # Teacher: copia profunda del encoder y projector del student
        self.teacher_encoder = copy.deepcopy(self.student_encoder)
        self._update_teacher()
        self._freeze_teacher()
        
    def _freeze_teacher(self):
        for param in self.teacher_encoder.parameters():
            param.requires_grad = False
            
    def _update_teacher(self):
        """Update teacher with EMA of student weights."""
        for student_param, teacher_param in zip(
            self.student_encoder.parameters(), self.teacher_encoder.parameters()
        ):
            teacher_param.data = self.momentum * teacher_param.data + \
                               (1.0 - self.momentum) * student_param.data
                               
    def forward_student(self, x1, x2):
        """Forward pass del student con ambas vistas."""
        # Vista 1: encode → project → predict
        z1 = self.student_encoder(x1)
        h1 = self.student_predictor(z1)
        z1 = F.normalize(z1, dim=-1)
        h1 = F.normalize(h1, dim=-1)
        
        # Vista 2: encode → project (sin predict)
        z2 = self.student_encoder(x2)
        z2 = F.normalize(z2, dim=-1)
        
        return z2, h1
        
    def forward_teacher(self, x1, x2):
        """Forward pass del teacher con ambas vistas."""
        with torch.no_grad():
            z1_t = self.teacher_encoder(x1)
            z1_t = F.normalize(z1_t, dim=-1)
            z2_t = self.teacher_encoder(x2)
            z2_t = F.normalize(z2_t, dim=-1)
        return z1_t, z2_t
    
    def loss(self, x1, x2):
        """
        Loss de BYOL: similitud entre predicción del student y 
        el embedding directo del teacher.
        
        loss = -2 * cos(h_student, z_teacher) + constante
        """
        # Student
        z2_s, h1_s = self.forward_student(x1, x2)
        
        # Teacher (sin gradientes)
        z1_t, z2_t = self.forward_teacher(x1, x2)
        
        # Loss asimétrico: h1_s predice z1_t, z2_s predice z2_t
        loss_1 = 2 - 2 * F.cosine_similarity(h1_s, z1_t.detach(), dim=-1).mean()
        loss_2 = 2 - 2 * F.cosine_similarity(z2_s, z2_t.detach(), dim=-1).mean()
        
        # Update teacher
        self._update_teacher()
        
        return (loss_1 + loss_2) / 2
```

---

## DINOv2: Self-Distillation con No-Looks

**Paper:** "DINOv2: Learning Robust Visual Features" (Oquab et al., 2023, Meta AI)
**Resultados:** SOTA en 11 benchmarks de transfer learning con ViT-B/16

### ¿Por qué funciona?

1. **Multi-Crop:** 2 crops grandes + 4 crops pequeños → el student ve las pequeñas, el teacher las grandes
2. **Soft labels:** Teacher produce distribuciones suaves (softmax con temperatura)
3. **Sin negatives ni batchs grandes:** Solo distillation loss
4. **Loss de distillation:** KL divergence entre distribución teacher y student

### Arquitectura Multi-Crop

```
Imagen original
├── Crop grande A → Teacher → Distribución suave (T=0.045)
├── Crop pequeño A1 → Student → Debe coincidir con teacher
├── Crop pequeño A2 → Student
├── Crop grande B → Teacher (otro forward)
├── Crop pequeño B1 → Student
└── Crop pequeño B2 → Student

Loss = -mean[log(student_score_Aj / teacher_score_Aj)]
```

### Implementación

```python
import torch
import torch.nn as nn

class DINOLoss(nn.Module):
    """
    Loss de DINOv2.
    
    Multi-crop: teacher ve crops grandes, student ve crops grandes + pequeños.
    El student debe producir las mismas distribuciones suaves que el teacher.
    """
    def __init__(self, out_dim, nfrops, student_temp=0.1, teacher_temp=0.045, 
                 center_momentum=0.9):
        super().__init__()
        self.student_temp = student_temp
        self.teacher_temp = teacher_temp
        self.center_momentum = center_momentum
        self.nfrops = nfrops  # número de crops pequeños
        
        # Centro móvil de las distribuciones del teacher
        self.register_buffer("center", torch.zeros(1, out_dim))
        
    def forward(self, student_output, teacher_output):
        """
        Args:
            student_output: (n_crops * batch_size, out_dim)
            teacher_output: (batch_size, out_dim)
        """
        # Student: softmax de su propio output
        student_logits = student_output / self.student_temp
        student_probs = torch.softmax(student_logits, dim=-1)  # (B*(1+n), D)
        
        # Teacher: softmax de su output
        teacher_logits = teacher_output / self.teacher_temp
        teacher_probs = torch.softmax(teacher_logits.detach(), dim=-1)  # (B, D)
        
        # Center móvil
        with torch.no_grad():
            center = torch.mean(teacher_probs, dim=0, keepdim=True)
            self.center = self.center * self.center_momentum + center * (1 - self.center_momentum)
        
        # KL divergence: student_probs vs teacher_probs
        # -sum(teacher_probs * log(student_probs))
        loss = -torch.sum(teacher_probs * torch.log(student_probs + 1e-8), dim=-1)
        
        # Mean sobre todos los crops
        loss = loss.mean()
        
        return loss


class DINOv2Train(nn.Module):
    """
    DINOv2 completo con multi-crop.
    
    Meta-AI: 14 millones de imágenes, 315M de parámetros, ViT-L/14
    """
    def __init__(self, teacher_model, student_model, patch_size=14):
        super().__init__()
        self.teacher = teacher_model
        self.student = student_model
        
        # teacher no tiene gradientes
        for param in self.teacher.parameters():
            param.requires_grad = False
            
        # EMA update
        self.ema_momentum = 0.993
            
    def train_step(self, large_crops, small_crops, momentum=0.993):
        """
        Args:
            large_crops: lista de 2 tensors (batch, 3, 224, 224)
            small_crops: lista de 4 tensors (batch, 3, 96, 96)
        """
        # Teacher: crops grandes, sin gradientes
        with torch.no_grad():
            teacher_large = torch.cat([self.teacher(lc) for lc in large_crops], dim=1)
            teacher_out = torch.chunk(teacher_large, 2, dim=1)
            
        # Student: crops grandes + pequeños, con gradientes
        student_outputs = []
        for lc in large_crops + small_crops:
            out = self.student(lc)
            student_outputs.append(out)
            
        # Loss entre teacher (large crops) y student (todos los crops)
        loss = 0.0
        for i in range(2):  # 2 large crops
            for j in range(6):  # 2 large + 4 small
                if i != j:
                    loss += F.kl_div(
                        torch.log_softmax(student_outputs[j] / 0.1, dim=-1),
                        torch.softmax(teacher_out[i] / 0.045, dim=-1).detach(),
                        reduction='batchmean'
                    )
                    
        loss = loss / (2 * 5)  # 2 teacher crops, 5 student crops cada uno
            
        # Update teacher con EMA
        with torch.no_grad():
            for param_q, param_k in zip(
                self.student.parameters(), self.teacher.parameters()
            ):
                param_k.data = momentum * param_k.data + (1 - momentum) * param_q.data
                
        return loss
```

---

## MAE: Masked Autoencoders — Predicción de Píxeles

**Paper:** "Masked Autoencoders Are Scalable Vision Learners" (He et al., 2021, Meta AI)
**Idea simple pero poderosa:** Enmascarar 75% de patches → el modelo debe reconstruirlos

### ¿Por qué funciona?

1. **Alto ratio de enmascaramiento:** 75% fuerza al modelo a aprender estructura semántica, no memorizar
2. **Encoder asimétrico:** Solo procesa patches visibles → eficiente (25% patches a 75% throughput)
3. **Reconstrucción directa:** Predice píxeles objetivo (no features intermedias)

### Implementación

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class VisionTransformerEncoder(nn.Module):
    """Encoder de patches con positional embedding."""
    def __init__(self, img_size=224, patch_size=16, in_chans=3, embed_dim=768, 
                 depth=12, num_heads=12):
        super().__init__()
        self.patch_embed = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, 
                                     stride=patch_size)
        num_patches = (img_size // patch_size) ** 2
        self.num_patches = num_patches
        
        # Token cls + positional embedding
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, embed_dim))
        self.pos_drop = nn.Dropout(0.1)
        
        # Transformer blocks
        self.blocks = nn.ModuleList([
            nn.Sequential(
                nn.LayerNorm(embed_dim),
                nn.MultiheadAttention(embed_dim, num_heads, batch_first=True),
                nn.Dropout(0.1),
                nn.Linear(embed_dim, 4 * embed_dim),
                nn.GELU(),
                nn.Dropout(0.1),
                nn.Linear(4 * embed_dim, embed_dim),
            )
            for _ in range(depth)
        ])
        self.norm = nn.LayerNorm(embed_dim)
        
        nn.init.trunc_normal_(self.pos_embed, std=0.02)
        
    def forward(self, x, mask=None):
        """
        Args:
            x: (B, 3, H, W)
            mask: boolean mask (B, num_patches) — True = visible
        """
        B = x.shape[0]
        x = self.patch_embed(x)  # (B, embed_dim, H/16, W/16)
        x = x.flatten(2).transpose(1, 2)  # (B, num_patches, embed_dim)
        
        # cls_token
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)
        x = x + self.pos_embed
        x = self.pos_drop(x)
        
        if mask is not None:
            # Solo procesar patches visibles (excluyendo cls_token)
            # mask: (B, num_patches), True = visible
            visible_mask = F.pad(mask, (1, 0), value=True)  # cls siempre visible
            batch_indices = torch.arange(B).unsqueeze(-1).expand(-1, visible_mask.shape[1])
            x = x[batch_indices, visible_mask]
            
            for block in self.blocks:
                x, _ = block[0](x, x, x, key_padding_mask=~visible_mask)
                x = x + block[1](x)
            x = self.norm(x)
        else:
            for block in self.blocks:
                norm_x = block[0](x)[0]
                attn_out, _ = block[1](norm_x, norm_x, norm_x)
                x = x + attn_out + block[2](x)
                
        return x
```

```python
class MAELoss(nn.Module):
    """
    Loss de reconstrucción MAE: MSE entre patches originales y predichos.
    
    Solo en patches enmascarados → eficiencia computacional.
    """
    def __init__(self, norm_pix_loss=True):
        super().__init__()
        self.norm_pix_loss = norm_pix_loss  # Normalizar patches por patch
        
    def forward(self, target, pred, mask):
        """
        Args:
            target: patches originales (B, num_masked, patch_size²*3)
            pred: patches predichos (B, num_masked, patch_size²*3)
            mask: boolean (B, num_masked) — True = enmascarado
        """
        if self.norm_pix_loss:
            mean = target.mean(dim=-1, keepdim=True)
            var = target.var(dim=-1, keepdim=True)
            target = (target - mean) / (var + 1e-6) ** 0.5
            
        loss = (pred - target) ** 2
        loss = loss.mean(dim=-1)  # Mean over patch channels
        loss = (loss * mask).sum() / mask.sum()  # Mean over masked patches
        return loss
```

```python
class MAE(nn.Module):
    """
    Masked Autoencoder (MAE) para pre-entrenamiento.
    
    Pipeline:
    1. Patchear imagen → (B, N, D) patches
    2. Mascarar 75% de patches aleatoriamente
    3. Encoder procesa solo 25% visibles
    4. Decoder reconstruye todos los patches
    """
    def __init__(self, img_size=224, patch_size=16, encoder_dim=768, encoder_depth=12,
                 decoder_dim=512, decoder_depth=8, mask_ratio=0.75):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.mask_ratio = mask_ratio
        num_patches = (img_size // patch_size) ** 2
        self.num_patches = num_patches
        
        # Encoder (asimétrico: solo procesa patches visibles)
        self.encoder = VisionTransformerEncoder(
            img_size, patch_size, in_chans=3, embed_dim=encoder_dim,
            depth=encoder_depth, num_heads=encoder_dim // 64
        )
        
        # Decoder: todos los patches (visibles + enmascarados)
        self.decoder_embed = nn.Linear(encoder_dim, decoder_dim)
        self.mask_token = nn.Parameter(torch.zeros(1, 1, decoder_dim))
        self.decoder_pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, decoder_dim))
        
        # Decoder blocks
        self.decoder_blocks = nn.ModuleList([
            nn.Sequential(
                nn.LayerNorm(decoder_dim),
                nn.MultiheadAttention(decoder_dim, 8, batch_first=True),
                nn.Dropout(0.1),
                nn.Linear(decoder_dim, 4 * decoder_dim),
                nn.GELU(),
                nn.Dropout(0.1),
                nn.Linear(4 * decoder_dim, decoder_dim),
            )
            for _ in range(decoder_depth)
        ])
        self.decoder_norm = nn.LayerNorm(decoder_dim)
        
        # Output: patches → píxeles
        self.decoder_pred = nn.Linear(decoder_dim, patch_size * patch_size * 3, bias=True)
        
        # Inicializaciones
        nn.init.normal_(self.mask_token, std=0.02)
        nn.init.normal_(self.decoder_pos_embed, std=0.02)
        
    def random_masking(self, B):
        """Mascarar mask_ratio patches aleatoriamente."""
        # No mascarar el cls_token
        len_keep = int(self.num_patches * (1 - self.mask_ratio))
        
        noise = torch.rand(B, self.num_patches, device=self.mask_token.device)
        
        # Ordenar y tomar los primeros len_keep
        noise_argsort = noise.argsort(dim=1)  # (B, N), ascending
        mask = noise_argsort < len_keep  # True = visible
        return mask
    
    def forward(self, x):
        """
        Forward pass completo de MAE.
        
        Args:
            x: (B, 3, H, W) — imagen original
        Returns:
            loss de reconstrucción
        """
        B = x.shape[0]
        
        # 1. Enmascarar
        mask = self.random_masking(B)  # (B, N) — True = visible
        
        # 2. Encoder (solo patches visibles)
        encoder_out = self.encoder(x, mask)
        
        # 3. Decoder: insertar mask tokens donde faltan patches
        decoder_pos = F.pad(self.mask_token.expand(B, self.num_patches, -1), (1, 0))
        decoder_pos = decoder_pos + self.decoder_pos_embed
        
        # Seleccionar patches visibles y concat con mask tokens para los enmascarados
        visible_patches = encoder_out[:, 1:]  # Excluir cls_token
        
        # Reordenar según mask
        idx = torch.arange(self.num_patches, device=x.device).unsqueeze(0).expand(B, -1)
        idx_all = torch.cat([idx[:, :1], idx[:, 1:][mask]], dim=1)  # Visible patches
        idx_mask = torch.cat([idx[:, :1], idx[:, 1:][~mask]], dim=1)  # Mask patches
        
        decoder_input = decoder_pos[idx_all]  # Visible + cls
        decoder_input = torch.cat([decoder_input, decoder_pos[idx_mask]], dim=1)
        
        decoder_input = self.decoder_embed(decoder_input)
        
        # 4. Decoder blocks
        for block in self.decoder_blocks:
            norm_input = block[0](decoder_input)
            attn, _ = block[1](norm_input, norm_input, norm_input)
            decoder_input = decoder_input + attn + block[2](decoder_input)
            
        decoder_out = self.decoder_norm(decoder_input)
        
        # 5. Predicción de patches
        pred = self.decoder_pred(decoder_out)  # (B, N+1, patch_size²*3)
        
        # 6. Loss en patches enmascarados
        target = self.get_target_patches(x, mask)
        loss = F.mse_loss(pred[:, 1:], target)  # Excluir cls_token
        
        return loss
    
    def get_target_patches(self, x, mask):
        """Extraer patches originales correspondientes a los enmascarados."""
        x = x.unfold(2, self.patch_size, self.patch_size).unfold(3, self.patch_size, self.patch_size)
        x = x.reshape(x.shape[0], x.shape[1], -1, self.patch_size * self.patch_size * 3)
        # Filtrar patches enmascarados
        return x[:, :, ~mask[:, 1:]]  # (B, N_masked, C*P*P)
```

---

## iBOT: Image BERT — Masked Patch Prediction

**Paper:** "iBOT: Image BERT Pre-Training with Online Tokenizer" (Chen et al., 2022, Meta AI)
**Idea:** Extender DINO con masked patch prediction → cada patch predice otros patches

### Innovación

1. **Máscara en espacio de patches (token space):** No en píxeles, sino en tokens de patch
2. **Token predictor:** Predice las "palabras" del tokenizer aprendido
3. **DINO + MAE:** Combina auto-distillation con masked patch prediction

---

## SigLIP: Sigmoid Loss para Language-Image

**Paper:** "SigLIP: Sigmoid Loss for Language Image Pre-Training" (Zhai et al., 2023, Google)
**Innovación:** Pairwise sigmoid loss en vez de softmax cross-entropy

### ¿Por qué sigmoid en vez de softmax?

- **Softmax:** Compara TODAS las imágenes del batch → batch size depende del vocabulario
- **Sigmoid:** Compara PA A PA → independiente del batch size → mejor escalabilidad

```python
class SigLIPLoss(nn.Module):
    """
    SigLIP loss: binary cross-entropy por par.
    
    Cada par (imagen, texto) tiene un score positivo.
    Cada par (imagen_i, texto_j) con i≠j es negativo.
    
    Loss = -log(sigmoid(score_positiva - score_negativa))
    """
    def __init__(self, logit_scale_init=1/0.07):
        super().__init__()
        self.logit_scale = nn.Parameter(torch.ones([]) * np.log(logit_scale_init))
        
    def forward(self, image_features, text_features, labels=None):
        """
        Args:
            image_features: (B, D)
            text_features: (B, D)
        Returns:
            loss escalar
        """
        # Similaridad por coseno escalada
        logit_scale = torch.clamp(self.logit_scale, max=np.log(100))
        logits = torch.matmul(image_features, text_features.T) * torch.exp(logit_scale)
        
        # Labels diagonales (par imagen_i ↔ texto_i)
        labels = torch.arange(len(logits), device=logits.device)
        
        # Loss: BCE con logits
        pos_logits = torch.diag(logits)  # Pares positivos
        neg_logits = logits - torch.diag(torch.diag(logits))  # Excluir diagonal
        
        # Para cada positivo: max(0, -pos + neg) + max(0, pos - neg - margin)
        # Versión simplificada: BCE entre positives y all others
        loss = F.binary_cross_entropy_with_logits(
            pos_logits, torch.ones_like(pos_logits)
        ) + F.binary_cross_entropy_with_logits(
            neg_logits, torch.zeros_like(neg_logits)
        )
        
        return loss.mean()
```

---

## Comparación de Paradigmas

| Método | Paradigma | Negativos | Batch Size | Key Idea |
|--------|-----------|-----------|------------|----------|
| **SimCLR** | Contrastivo | Sí | 4096 | Augmentaciones + NT-Xent |
| **MoCo** | Contrastivo | Memoria queue | 256 + 65536 | Encoder momentum |
| **BYOL** | Distillation | No | 256 | Dual networks + predictor |
| **DINO/DINOv2** | Self-distillation | No | 256 | Multi-crop + soft labels |
| **MAE** | Masked modeling | No | 4096 | Reconstruir 75% patches |
| **iBOT** | Masked + Distill | No | 4096 | DINO + token prediction |
| **SigLIP** | Contrastivo | No | Flexible | Sigmoid loss binario |

---

## Aplicaciones al Stack Esios

### 1. Imágenes Satelitales Sin Etiquetar

```python
# Usar DINOv2 para extraer features de imágenes satelitales
import torch
import torch.nn.functional as F

def extract_satellite_features(image_path, model, device='cpu'):
    """
    Extraer embeddings de imágenes satelitales con DINOv2.
    
    Aplicaciones:
    - Clustering de regiones geográficas
    - Detección de cambios temporales
    - Búsqueda semántica de imágenes satelitales
    """
    # Pre-procesar imagen
    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize(224),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        ),
    ])
    
    image = transform(Image.open(image_path)).unsqueeze(0).to(device)
    
    # Extraer features
    with torch.no_grad():
        features = model(image)  # (B, 768) para ViT-B/14
        features = F.normalize(features, dim=-1)
        
    return features

# Batch de imágenes satelitales → embeddings para clustering
satellite_embeddings = extract_satellite_features_batch(image_paths, model)
# Usar sklearn para clustering (KMeans, DBSCAN)
from sklearn.cluster import DBSCAN
clusters = DBSCAN(eps=0.1, min_samples=5).fit_predict(satellite_embeddings)
```

### 2. Fine-tuning Eficiente en MicroVM

```python
def efficient_finetune(base_model, dataset, device='cpu'):
    """
    Fine-tuning eficiente para MicroVM (1 vCPU, 2GB RAM).
    
    Estrategia:
    1. Congelar los primeros 8 blocks del ViT
    2. Solo fine-tunear los últimos 4 blocks + classifier
    3. Learning rate bajo (1e-4)
    """
    # Congelar capas
    for i, block in enumerate(base_model.blocks):
        if i < 8:  # Primeros 8 blocks congelados
            for param in block.parameters():
                param.requires_grad = False
    
    # Classifier ligero
    classifier = nn.Sequential(
        nn.LayerNorm(768),
        nn.Linear(768, 256),
        nn.GELU(),
        nn.Dropout(0.1),
        nn.Linear(256, num_classes),
    ).to(device)
    
    # Optimizar solo capas no congeladas
    trainable_params = [
        p for n, p in base_model.named_parameters() 
        if p.requires_grad
    ]
    trainable_params.extend(classifier.parameters())
    
    optimizer = torch.optim.AdamW(trainable_params, lr=1e-4, weight_decay=0.01)
    
    return base_model, classifier, optimizer
```

### 3. Retrieval de Imágenes con Embeddings

```python
import faiss

def build_image_retriever(embeddings, index_type='IVF'):
    """
    Construir indexador FAISS para retrieval de imágenes.
    
    Útil para:
    - Buscar imágenes satelitales similares
    - Detección de cambios comparando embeddings
    """
    dim = embeddings.shape[1]
    n = embeddings.shape[0]
    
    if index_type == 'IVF':
        nlist = min(4 * int(np.sqrt(n)), 1000)
        quantizer = faiss.IndexFlatIP(dim)  # Inner product (cosine)
        index = faiss.IndexIVFFlat(quantizer, dim, nlist)
        index.train(embeddings.astype('float32'))
    else:
        index = faiss.IndexFlatIP(dim)  # Exact nearest neighbor
        
    index.add(embeddings.astype('float32'))
    return index

def retrieve_similar(index, query_embedding, k=10):
    """Buscar las k imágenes más similares."""
    query = query_embedding.reshape(1, -1).astype('float32')
    distances, indices = index.search(query, k)
    return indices[0], distances[0]
```

---

## Recursos de Aprendizaje

### Papers Fundacionales
- **SimCLR:** https://arxiv.org/abs/2002.05709
- **MoCo:** https://arxiv.org/abs/1911.05722
- **BYOL:** https://arxiv.org/abs/2006.07733
- **DINO:** https://arxiv.org/abs/2104.14256
- **DINOv2:** https://arxiv.org/abs/2304.07193
- **MAE:** https://arxiv.org/abs/2111.06377
- **iBOT:** https://arxiv.org/abs/2111.07832
- **SigLIP:** https://arxiv.org/abs/2303.15343

### Implementaciones de Referencia
- **DINOv2 oficial:** github.com/facebookresearch/dinov2
- **MAE oficial:** github.com/facebookresearch/mae
- **BYOL PyTorch:** github.com/lucidrains/byol-pytorch
- **SimCLR:** github.com/google-research/simclr
- **HuggingFace Transformers:** tiene DINOv2, MAE, MoCo implementados

### Benchmarks
- **Oxford-IIIT Pet:** 37 clases, 7400 imágenes
- **CIFAR-100:** 100 clases, 50000 imágenes
- **Places365:** Escenas, 182 clases, 1.8M imágenes

---

## Tema Siguiente Propuesto

**Chain-of-Thought Reasoning & System 2 Thinking**

Por qué:
- Complementa el stack de visión con razonamiento en LLMs
- Esios tiene análisis de datos que podrían beneficiarse de razonamiento paso a paso
- Conecta con los temas de LLMs (LoRA/PEFT de la sesión anterior)
- Papers recientes de DeepSeek-R1, Qwen-2.5, y Kimi muestran el estado del arte en reasoning

Alternativas:
- **Diffusion Transformers (DiT):** SD3, Flux — evolución de diffusion models
- **Multi-Modal Models:** CLIP, BLIP — para análisis de imágenes satelitales con texto

<tool_call>
<function=todo>