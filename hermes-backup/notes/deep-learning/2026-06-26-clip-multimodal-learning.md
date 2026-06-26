# CLIP y Aprendizaje Multimodal Contrastivo

**Fecha:** 2026-06-26  
**Tema:** Multi-modal Learning — Contrastive Language-Image Pretraining  
**Nivel:** Avanzado  
**Estado:** Aprendido y documentado

---

## 1. Contexto y Motivación

CLIP (Contrastive Language-Image Pretraining) de OpenAI (2021) demostró que un modelo preentrenado con **aprendizaje auto-supervisado** en grandes pares imagen-texto puede transferir su conocimiento a tareas de visión por computador **sin fine-tuning** (zero-shot), superando a modelos entrenados específicamente para esas tareas.

**Paper original:** *"Learning Transferable Visual Models From Natural Language Supervision"* — Radford et al., OpenAI, 2021.

El insight clave: en lugar de entrenar un modelo de clasificación con etiquetas manuales, entrenar un modelo para **predecir qué pareja imagen-texto es correcta** entre miles de candidatos. Esto aprende representaciones ricas que capturan semántica visual y lingüística de forma conjunta.

---

## 2. Arquitectura CLIP

### 2.1 Estructura Dual

CLIP usa un **par de codificadores**:
- **Vision Encoder** (ViT-B/32, ViT-L/14, ResNet-50): convierte imagen → vector en R^D
- **Text Encoder** (Transformer de 12 capas): convierte texto → vector en R^D

Ambos producen embeddings en el **mismo espacio de dimensiones D** (512, 768 o 1024).

### 2.2 Normalización por Temperatura

Los embeddings se normalizan y se escala el producto escalar con una temperatura:

```
similarity = exp(similarity / τ) / Σ exp(similarity / τ)
```

Donde τ (tau) es un parámetro aprendible que controla la "agudeza" de la distribución de probabilidad.

### 2.3 Función de Pérdida InfoNCE

La pérdida es **contrastiva**: para cada batch de N parejas (imagen, texto):

```python
def contrastive_loss(image_embeds, text_embeds, temperature):
    """
    Pérdida InfoNCE para CLIP.
    
    image_embeds: (N, D) - embeddings de imágenes
    text_embeds: (N, D) - embeddings de texto
    temperature: escalar τ
    
    Returns: scalar loss
    """
    # Similaridades entre TODOS los pares imagen-texto en el batch
    # (N, N) - matriz de similarities
    logits = torch.matmul(image_embeds, text_embeds.T) / temperature
    
    # Las parejas correctas están en la diagonal (i, i)
    labels = torch.arange(len(image_embeds)).to(image_embeds.device)
    
    # Pérdida cross-entropy
    loss_i2t = F.cross_entropy(logits, labels)
    loss_t2i = F.cross_entropy(logits.T, labels)
    
    return (loss_i2t + loss_t2i) / 2
```

**Intuición:** cada imagen compite con todos los textos del batch. La pérdida fuerza a que la imagen correcta tenga la puntuación más alta. Es un problema de clasificación N-class donde N = tamaño del batch.

---

## 3. Pipeline de Entrenamiento

### 3.1 Dataset: LAION-400M

CLIP se entrenó en ~400 millones de parejas imagen-texto scraped de internet. Los textos son los **alt-text** (descripciones alternativas) de las imágenes.

### 3.2 Augmentaciones

- **Imágenes:** RandAugment, RandomResizedCrop, ColorJitter
- **Texto:** sin augmentación significativa (los textos de alt son los datos reales)

### 3.3 Escalado

| Modelo | Vision Encoder | Text Encoder | Dim |
|--------|---------------|-------------|-----|
| ViT-B/32 | Vision Transformer B/32 | Transformer 12L, 768d | 512 |
| ViT-B/16 | Vision Transformer B/16 | Transformer 12L, 768d | 512 |
| ViT-L/14 | Vision Transformer L/14 | Transformer 24L, 1024d | 768 |
| ViT-L/14@336px | ViT-L/14@336 | Transformer 24L, 1024d | 768 |

El ViT-L/14@336px fue el mejor: 65.5% en ImageNet zero-shot classification.

---

## 4. Implementación Práctica Completa

### 4.1 Código Base CLIP

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize

class CLIPModel(nn.Module):
    """Implementación simplificada de CLIP."""
    
    def __init__(
        self,
        embed_dim: int = 512,
        image_width: int = 224,
        text_width: int = 768,
        vision_layers: tuple = (3, 4, 6, 3),
        vision_width: int = 768,
        vision_head_width: int = 64,
        text_layers: int = 12,
        text_width: int = 512,
        text_heads: int = 8,
    ):
        super().__init__()
        
        self.embed_dim = embed_dim
        self.temperature = nn.Parameter(torch.tensor(0.07))
        
        # Vision encoder (simplificado: ResNet o ViT)
        self.visual = VisionTransformer(
            image_width=image_width,
            width=vision_width,
            layers=vision_layers,
            heads=vision_width // vision_head_width,
            embed_dim=embed_dim,
        )
        
        # Text encoder
        self.text = TextTransformer(
            width=text_width,
            layers=text_layers,
            heads=text_heads,
            embed_dim=embed_dim,
        )
        
        # Logit scale learnable
        self.logit_scale = nn.Parameter(torch.tensor(2.6592))  # log(1/0.07)
    
    def encode_image(self, x):
        """Encode image to embedding."""
        return self.visual(x)
    
    def encode_text(self, text):
        """Encode text to embedding."""
        return self.text(text)
    
    def forward(self, images, texts):
        image_embeds = self.encode_image(images)
        text_embeds = self.encode_text(texts)
        
        # Normalizar L2
        image_embeds = F.normalize(image_embeds, dim=-1)
        text_embeds = F.normalize(text_embeds, dim=-1)
        
        # Similaridad escalada
        logit_scale = self.logit_scale.exp()
        logits_per_image = torch.matmul(image_embeds, text_embeds.T) * logit_scale
        logits_per_text = logits_per_image.T
        
        return logits_per_image, logits_per_text


class VisionTransformer(nn.Module):
    """Vision Transformer (simplificado)."""
    
    def __init__(self, image_width=224, width=768, layers=(3,4,6,3), 
                 heads=12, embed_dim=512):
        super().__init__()
        self.embed_dim = embed_dim
        
        # Patch embedding: dividir imagen en patches 16x16
        patch_size = image_width // 16
        self.patch_conv = nn.Conv2d(3, width, kernel_size=16, stride=16)
        
        # Positional embedding
        num_patches = (image_width // 16) ** 2
        self.pos_embed = nn.Parameter(torch.randn(1, num_patches + 1, width))
        self.cls_token = nn.Parameter(torch.randn(1, 1, width))
        
        # Layers
        self.layers = nn.ModuleList([
            TransformerBlock(width, heads) for _ in range(sum(layers) * 4)
        ])
        
        # Projection
        self.ln_post = LayerNorm(width)
        self.proj = nn.Parameter(torch.randn(width, embed_dim))
    
    def forward(self, x):
        B, C, H, W = x.shape
        
        # Patch embedding
        x = self.patch_conv(x)  # (B, width, 14, 14)
        x = x.flatten(2).transpose(1, 2)  # (B, 196, width)
        
        # CLS token
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)  # (B, 197, width)
        
        # Positional embedding
        x = x + self.pos_embed
        
        # Transformer layers
        for layer in self.layers:
            x = layer(x)
        
        # CLS token + projection
        x = self.ln_post(x[:, 0, :])  # (B, width) - token CLS
        x = x @ self.proj  # (B, embed_dim)
        
        return x


class TextTransformer(nn.Module):
    """Text Transformer (simplificado)."""
    
    def __init__(self, width=512, layers=12, heads=8, embed_dim=512):
        super().__init__()
        self.width = width
        
        # Token embedding + position
        self.token_embedding = nn.Embedding(49408, width)  # vocab_size de CLIP
        self.positional_embedding = nn.Parameter(torch.randn(77, width))
        self.cls_token = nn.Parameter(torch.randn(width))
        
        # Transformer layers
        self.layers = nn.ModuleList([
            TransformerBlock(width, heads) for _ in range(layers)
        ])
        
        self.ln_final = LayerNorm(width)
        self.text_projection = nn.Parameter(torch.randn(width, embed_dim))
    
    def forward(self, text):
        B, L = text.shape  # (B, 77) - max seq length de CLIP
        
        # Token embedding
        x = self.token_embedding(text)  # (B, 77, width)
        
        # Positional embedding
        x = x + self.positional_embedding
        
        # CLS token
        cls_tokens = self.cls_token.unsqueeze(0).expand(B, -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)
        
        # Transformer
        for layer in self.layers:
            x = layer(x)
        
        # CLS token projection
        x = self.ln_final(x[:, 0, :])
        x = x @ self.text_projection
        
        return x


class TransformerBlock(nn.Module):
    """Transformer block con attention y FFN."""
    
    def __init__(self, width, heads):
        super().__init__()
        self.attn = nn.MultiheadAttention(width, heads)
        self.ln_1 = LayerNorm(width)
        self.mlp = nn.Sequential(
            nn.Linear(width, 4 * width),
            nn.GELU(),
            nn.Linear(4 * width, width),
        )
        self.ln_2 = LayerNorm(width)
    
    def forward(self, x):
        # Self-attention
        x = x + self.attn(self.ln_1(x), self.ln_1(x), self.ln_1(x))[0]
        # FFN
        x = x + self.mlp(self.ln_2(x))
        return x


class LayerNorm(nn.LayerNorm):
    """LayerNorm con soporte para fp16."""
    
    def forward(self, x):
        return super().forward(x.float()).type(x.dtype)
```

### 4.2 Inferencia: Text-to-Image Search

```python
class CLIPImageSearch:
    """Search engine de imágenes basado en CLIP embeddings."""
    
    def __init__(self, clip_model, device='cuda'):
        self.model = clip_model.to(device)
        self.device = device
        self.image_embeds = None
        self.image_paths = []
    
    def add_images(self, image_paths, preprocess_fn, batch_size=64):
        """Embed y almacena imágenes para búsqueda."""
        self.image_paths = image_paths
        embeddings = []
        
        self.model.eval()
        with torch.no_grad():
            for i in range(0, len(image_paths), batch_size):
                batch = [preprocess_fn(image_paths[i:j]) 
                        for j in min(i + batch_size, len(image_paths))]
                batch_tensor = torch.stack(batch).to(self.device)
                emb = self.model.encode_image(batch_tensor)
                embeddings.append(emb.cpu())
        
        self.image_embeds = torch.cat(embeddings, dim=0)
        print(f"✓ {len(image_paths)} imágenes indexadas")
    
    def search(self, query_text, top_k=10):
        """Buscar las top-K imágenes para un query textual."""
        self.model.eval()
        
        # Preprocesar texto (CLIP espera tokens)
        text_tokens = encode_text([query_text]).to(self.device)
        
        with torch.no_grad():
            text_emb = self.model.encode_text(text_tokens)
            text_emb = F.normalize(text_emb, dim=-1)
            img_emb = F.normalize(self.image_embeds.to(self.device), dim=-1)
            
            # Similaridad coseno
            scores = torch.matmul(text_emb, img_emb.T).squeeze()
            
            # Top-K
            top_indices = torch.topk(scores, top_k).indices
        
        results = [(self.image_paths[idx], scores[idx].item()) 
                   for idx in top_indices]
        return results
    
    def search_by_image(self, image_tensor, top_k=10):
        """Buscar por imagen (visual query)."""
        self.model.eval()
        
        with torch.no_grad():
            img_emb = self.model.encode_image(image_tensor)
            img_emb = F.normalize(img_emb, dim=-1)
            db_emb = F.normalize(self.image_embeds.to(self.device), dim=-1)
            
            scores = torch.matmul(img_emb, db_emb.T).squeeze()
            top_indices = torch.topk(scores, top_k).indices
        
        return [(self.image_paths[idx], scores[idx].item()) 
                for idx in top_indices]
```

### 4.3 Few-Shot Classification con CLIP

```python
def few_shot_clip_classifier(clip_model, image_dataset, label_templates, 
                               class_names, preprocess_fn, device='cuda'):
    """
    Clasificador zero-shot / few-shot basado en CLIP.
    
    Args:
        clip_model: Modelo CLIP
        image_dataset: Dataset de imágenes
        label_templates: Templates de texto por clase
            Ej: {"perro": ["un perro", "una foto de un perro", "un perro hermoso"]}
        class_names: Lista de nombres de clase
        preprocess_fn: Función de preprocesamiento de imagen
        device: Dispositivo
    """
    clip_model.eval()
    clip_model.to(device)
    
    all_templates = []
    for class_name in class_names:
        for template in label_templates:
            text = template.format(class_name)
            all_templates.append(encode_text([text]).to(device))
    
    # Embed de todos los templates
    with torch.no_grad():
        text_embeds = []
        for i in range(0, len(all_templates), 32):
            batch = torch.cat(all_templates[i:i+32], dim=0)
            emb = clip_model.encode_text(batch)
            text_embeds.append(F.normalize(emb, dim=-1))
        text_embeds = torch.cat(text_embeds, dim=0)  # (num_templates * num_classes, D)
    
    # Clasificar imágenes
    predictions = []
    with torch.no_grad():
        for image_path in image_dataset:
            img = preprocess_fn(image_path).unsqueeze(0).to(device)
            img_emb = clip_model.encode_image(img)
            img_emb = F.normalize(img_emb, dim=-1)
            
            # Scores por template
            logits = (100.0 * img_emb @ text_embeds.T).squeeze()
            
            # Reorganizar: (num_classes, num_templates)
            logits = logits.view(len(class_names), -1).mean(dim=1)
            
            pred = torch.argmax(logits).item()
            predictions.append(pred)
    
    return predictions
```

---

## 5. Evolución Post-CLIP

### 5.1 Modelos Derivados Clave

| Modelo | Año | Contribución |
|--------|-----|-------------|
| **ALIGN** (Google) | 2021 | Escalar a 4000M de parejas, zero-shot state-of-the-art |
| **ALBEF** (Microsoft) | 2021 | Alchemy Between Language and Visual Features |
| **FLIP** (Meta) | 2021 | Fast Language-Image Pretraining |
| **DALL-E** | 2021 | CLIP + autoregressive transformer para generación |
| **DALL-E 2** | 2022 | CLIP + prior + VAE para generación de alta calidad |
| **Stable Diffusion** | 2022 | CLIP + U-Net diffusion model + latent space |
| **Flamingo** (DeepMind) | 2022 | Visual-language model con few-shot capabilities |
| **BLIP-2** (Salesforce) | 2023 | Q-Former bridge entre vision y language model |
| **Florence** (Microsoft) | 2023 | Unified vision-language pretraining con 230M imágenes |
| **OpenCLIP** | 2022 | Implementación open-source reproducible de CLIP |

### 5.2 Stable Diffusion: CLIP como Text Encoder

Stable Diffusion usa CLIP como codificador de texto:

```
Prompt text → CLIP Text Encoder → embeddings → U-Net diffusion guidance
```

El texto se convierte en un embedding que guía el proceso de denoising del U-Net. Este es uno de los usos más populares de CLIP en la práctica.

```python
# Ejemplo: CLIP como parte de un pipeline de Stable Diffusion
import torch
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cuda")

# El CLIP text encoder está integrado en el pipeline
# Pero podemos usarlo directamente para extraer embeddings

clip_text_encoder = pipe.text_encoder
clip_tokenizer = pipe.tokenizer

def get_clip_text_embedding(prompt):
    """Extraer embedding de texto de CLIP integrado en SD."""
    with torch.no_grad():
        inputs = clip_tokenizer([prompt], padding="max_length", 
                               max_length=clip_tokenizer.model_max_length,
                               truncation=True, return_tensors="pt")
        embeddings = clip_text_encoder(inputs.input_ids.to("cuda"))[0]
    return embeddings

embedding = get_clip_text_embedding("a beautiful sunset over the ocean")
print(f"Embedding shape: {embedding.shape}")  # (1, 77, 768)
```

### 5.3 OpenCLIP: Implementación Open-Source

```bash
# Instalar OpenCLIP
pip install open-clip-torch

# Usar modelos pre-entrenados
import open_clip

model, _, preprocess = open_clip.create_model_and_transforms('ViT-L-14', pretrained='laion2b_s32b_b82k')
tokenizer = open_clip.get_tokenizer('ViT-L-14')

# Inferencia
image = preprocess(image).unsqueeze(0)
text = tokenizer(["a photo of a cat", "a photo of a dog"])

with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    
    # Similaridad
    logits = 100.0 * image_features @ text_features.T
    probs = logits.softmax(dim=-1)
    
    print(f"Probabilidades: {probs[0].tolist()}")
```

---

## 6. Comparación con Self-Supervised Learning

| Aspecto | CLIP (contrastivo) | SimCLR (self-supervised) | DINO (self-distillation) |
|---------|-------------------|-------------------------|-------------------------|
| Señal | Pares imagen-texto | Augmentaciones | Self-distillation |
| Supervisión | Natural language | Inversa | Sin etiquetas |
| Espacio | Imagen ↔ Texto | Solo imagen | Solo imagen |
| Transferencia | Zero-shot con prompts | Fine-tuning required | Fine-tuning required |
| Datset | Internet (alt-text) | ImageNet/Augmented | ImageNet |
| Ventaja | Semántica rica | Estructura visual | Características robustas |

**Relación con la nota de ayer:** CLIP usa contrastive learning (InfoNCE) igual que SimCLR, pero con la clave de añadir la **modalidad de texto** como señal de supervisión alternativa. Esto permite zero-shot classification sin ver nunca una etiqueta durante el entrenamiento.

---

## 7. Aplicaciones Prácticas

### 7.1 Búsqueda Semántica de Imágenes
- Google Photos (CLIP-like embeddings)
- Pinterest Visual Search
- Stock image search (Shutterstock, Adobe Stock)

### 7.2 Content Moderation
- Moderación de contenido con texto natural
- OpenAI Content Moderation API usa modelos similares

### 7.3 Zero-Shot Object Detection
- Grounding DINO: detección de objetos con descripciones textuales
- SAM (Segment Anything): usa CLIP para features

### 7.4 Generación Multimodal
- ControlNet + CLIP para control semántico
- Prompt engineering en Stable Diffusion

---

## 8. Límites y Críticas

1. **Dependencia de alt-text:** Los textos de internet son ruidosos. Un dataset limpio como LAION-2B (500M) tiene menos datos pero mejor calidad.
2. **Bias inherente:** Los alt-text reflejan sesgos del internet.
3. **No aprende composición:** CLIP no entiende bien composiciones lógicas ("un gato rojo sobre un perro azul").
4. **Computacional:** Los modelos grandes (ViT-L/14) requieren GPU potente para inferencia en tiempo real.
5. **Tokenización de texto:** CLIP usa un tokenizer BPE específico con vocabulario de ~49k tokens.

---

## 9. Referencias

- **Paper original:** Radford et al., "Learning Transferable Visual Models From Natural Language Supervision", ICML 2021 — https://arxiv.org/abs/2103.00020
- **OpenCLIP:** https://github.com/mlfoundations/open_clip
- **CLIP paper repository:** https://github.com/openai/CLIP
- **ALIGN:** "Large-Scale Image-Text Alignment" — Google, 2021
- **DALL-E 2:** "Zero-Shot Text-to-Image Generation" — Radford et al., 2022
- **Florence:** "Florence: A New Foundation for Visual Recognition" — Microsoft, 2023
- **Survey:** "Advances in Multimodal Adaptation and Generalization" — 2025, https://arxiv.org/abs/2501.18592

---

## 10. Próximos Temas Sugeridos

1. **State Space Models (Mamba)** — ya cubierto el día 12
2. **Neural ODEs** — conexión entre ecuaciones diferenciales y redes neuronales
3. **Adapters y Prompt Tuning** — más allá de LoRA: prefix tuning, P-tuning, adapter fusion
4. **Energy-Based Models** — EBMs como alternativa a VAEs/GANs/Diffusion
5. **World Models** — aprendizaje de modelos del mundo para RL (World Models de Ha & Schmidhuber)

**Siguiente recomendado:** **State Space Models (Mamba)** — ya cubierto, así que mejor **Adapters y Prompt Tuning** para complementar el tema de LoRA/PEFT del día 19.
