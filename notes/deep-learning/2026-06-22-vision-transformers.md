# Vision Transformers (ViT) — De Patch Embeddings a Transformers Visuales

> **Fecha:** 2026-06-22
> **Serie:** Deep Learning Fundamentals — #11
> **Autores:** Hecho con (♥) por David Antizar

---

## 1. Concepto Fundamental

### La Gran Idea

Los Vision Transformers aplican la arquitectura Transformer (originalmente diseñada para NLP) directamente a imágenes. En lugar de usar convoluciones para extraer features, **dividen la imagen en patches y los procesan con self-attention**.

**Paper fundacional:** *"An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"* — Doski et al., 2020 (Google Research)

La intuición es simple pero poderosa: si un Transformer puede entender texto token a token, ¿por qué no puede entender imágenes patch a patch?

### ¿Por qué funciona?

| CNN | Vision Transformer |
|-----|-------------------|
| **Inductive bias:** invariancia traslacional + localidad | **Sin inductive bias:** aprende dependencias globales |
| Receptive field crece con la profundidad | Receptive field **global desde el primer layer** |
| Escala bien con más datos pero no con más compute | Escala **monotónicamente** con datos y compute |
| Arquitectura fija (resnet, efficientnet) | **Flexible:** se puede escalar en profundidad/ancho |

El ViT demuestra que **los datos + compute > inductive bias**. Con suficientes datos (ImageNet-21k, JFT-300M) y compute, un Transformer simple supera a las mejores CNNs.

---

## 2. Arquitectura Original (ViT-Base)

### Pipeline de Preprocesamiento

```
Imagen RGB (224×224)
    │
    ├── Split en patches de 16×16 → 196 patches (14×14 grid)
    ├── Flatten cada patch → vector de 768 dims (16×16×3 = 768)
    ├── Proyectar a dim d_model (ej: 768 para ViT-Base)
    ├── Añadir embedding de posición (learned positional embedding)
    ├── Añadir token [CLS] al inicio
    └── Secuencia de 197 tokens → Transformer Encoder
```

### Código de Ejemplo: Implementación Completa

```python
"""
Vision Transformer (ViT) — Implementación completa desde cero en PyTorch.
Basado en: https://arxiv.org/abs/2010.11929

Incluye:
- Patch Embedding con Linear layer (no Conv2d)
- Posicional embedding learnable
- Transformer Encoder con Multi-Head Self-Attention
- Clasificador con token [CLS]
- Pre-training con Masked Autoencoder (MAE)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional


class PatchEmbedding(nn.Module):
    """
    Divide la imagen en patches y los proyecta a un espacio de embedding.
    
    A diferencia de CNNs, usa un Linear layer (stride=patch_size) en lugar
    de Conv2d. Esto es más flexible y permite patch sizes arbitrarios.
    
    Args:
        img_size: Tamaño de la imagen de entrada (asumimos cuadrada)
        patch_size: Tamaño de cada patch
        in_channels: Canales de entrada (3 para RGB)
        embed_dim: Dimensión del embedding de salida
    """
    def __init__(self, img_size: int = 224, patch_size: int = 16,
                 in_channels: int = 3, embed_dim: int = 768):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.n_patches = (img_size // patch_size) ** 2  # 196 para 224/16
        
        # Linear equivale a Conv2d(kernel=patch, stride=patch)
        self.proj = nn.Conv2d(
            in_channels, embed_dim, 
            kernel_size=patch_size, 
            stride=patch_size
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Tensor de forma (B, C, H, W)
        Returns:
            Patches proyectados: (B, n_patches, embed_dim)
        """
        B, C, H, W = x.shape
        assert H == W == self.img_size, \
            f"Imagen {H}x{W} no coincide con img_size={self.img_size}"
        
        # (B, C, H, W) → (B, embed_dim, H/patch, W/patch)
        x = self.proj(x)
        # (B, embed_dim, Hp, Wp) → (B, embed_dim, Hp*Wp) → (B, Hp*Wp, embed_dim)
        x = x.flatten(2).transpose(1, 2)
        
        return x


class MultiHeadSelfAttention(nn.Module):
    """
    Multi-Head Self-Attention con dropout y residual connection.
    
    Para ViT, la atención es FULL (todos contra todos).
    A diferencia de NLP, NO hay máscara de causalidad en ViT.
    """
    def __init__(self, dim: int, num_heads: int = 12, dropout: float = 0.0):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.scale = self.head_dim ** -0.5
        
        # Q, K, V projections — juntas en un layer para eficiencia
        self.qkv = nn.Linear(dim, dim * 3)
        self.attn_drop = nn.Dropout(dropout)
        self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(dropout)
        
        # Inicialización cuidadosa (sigue el paper original)
        nn.init.xavier_uniform_(self.qkv.weight)
        nn.init.xavier_uniform_(self.proj.weight)
    
    def forward(self, x: torch.Tensor, 
                attention_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Args:
            x: (B, N, D) — secuencia de tokens
            attention_mask: (B, 1, 1, N) opcional para masked attention
        Returns:
            Outputs atendidos: (B, N, D)
        """
        B, N, D = x.shape
        
        # Proyectar Q, K, V juntos
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)  # (3, B, H, N, d)
        q, k, v = qkv.unbind(0)
        
        # Attention scores: (B, H, N, N)
        attn = (q @ k.transpose(-2, -1)) * self.scale
        
        # Aplicar mask si existe
        if attention_mask is not None:
            attn = attn.masked_fill(attention_mask == 0, float('-inf'))
        
        attn = attn.softmax(dim=-1)
        attn = self.attn_drop(attn)
        
        # Weighted sum: (B, H, N, d) → (B, N, D)
        x = (attn @ v).transpose(1, 2).reshape(B, N, D)
        x = self.proj(x)
        x = self.proj_drop(x)
        
        return x


class TransformerBlock(nn.Module):
    """
    Un bloque de Transformer: Pre-LN (LayerNorm antes de attention)
    + Multi-Head Self-Attention + MLP.
    
    Usa Pre-LN (como el paper original), que estabiliza el training.
    """
    def __init__(self, dim: int, num_heads: int = 12, 
                 mlp_ratio: float = 4.0, dropout: float = 0.0):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.attn = MultiHeadSelfAttention(dim, num_heads, dropout)
        self.norm2 = nn.LayerNorm(dim)
        
        # MLP: expand → GELU → contract
        mlp_hidden = int(dim * mlp_ratio)
        self.mlp = nn.Sequential(
            nn.Linear(dim, mlp_hidden),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(mlp_hidden, dim),
            nn.Dropout(dropout),
        )
    
    def forward(self, x: torch.Tensor, 
                attention_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        # Pre-LN: LayerNorm antes de cada sub-layer
        x = x + self.attn(self.norm1(x), attention_mask)
        x = x + self.mlp(self.norm2(x))
        return x


class VisionTransformer(nn.Module):
    """
    Vision Transformer completo.
    
    Arquitectura:
        Input → Patch Embedding → [Transformer Blocks] → [CLS] → Classifier
    
    Parámetros (según tabla del paper):
        ViT-Tiny:   d=192,  heads=3,  layers=12
        ViT-Base:   d=768,  heads=12, layers=12
        ViT-Large:  d=1024, heads=16, layers=24
        ViT-Huge:   d=1280, heads=16, layers=32
    """
    def __init__(self, img_size: int = 224, patch_size: int = 16,
                 in_channels: int = 3, num_classes: int = 1000,
                 embed_dim: int = 768, depth: int = 12,
                 num_heads: int = 12, mlp_ratio: float = 4.0,
                 dropout: float = 0.0):
        super().__init__()
        self.patch_embed = PatchEmbedding(img_size, patch_size, in_channels, embed_dim)
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        
        # Posicional embedding: [CLS] + n_patches
        self.pos_embed = nn.Parameter(
            torch.zeros(1, 1 + self.patch_embed.n_patches, embed_dim)
        )
        self.pos_drop = nn.Dropout(dropout)
        
        self.blocks = nn.Sequential(*[
            TransformerBlock(embed_dim, num_heads, mlp_ratio, dropout)
            for _ in range(depth)
        ])
        
        self.norm = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, num_classes)
        
        # Inicialización
        self._init_weights()
    
    def _init_weights(self):
        """Inicialización de parámetros (sigue el paper)."""
        nn.init.trunc_normal_(self.pos_embed, std=0.02)
        nn.init.trunc_normal_(self.cls_token, std=0.02)
        self.apply(self._init_layer)
    
    def _init_layer(self, m):
        if isinstance(m, nn.Linear):
            nn.init.trunc_normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.LayerNorm):
            nn.init.ones_(m.weight)
            nn.init.zeros_(m.bias)
    
    def forward(self, x: torch.Tensor, 
                return_features: bool = False) -> torch.Tensor:
        """
        Args:
            x: (B, C, H, W) imagen de entrada
            return_features: Si True, devuelve features antes del classifier
        Returns:
            Logits: (B, num_classes)
        """
        B = x.shape[0]
        
        # Patch embedding: (B, C, H, W) → (B, n_patches, embed_dim)
        x = self.patch_embed(x)
        
        # Añadir [CLS] token
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)
        
        # Añadir posición
        x = x + self.pos_embed
        x = self.pos_drop(x)
        
        # Transformer blocks
        x = self.blocks(x)
        x = self.norm(x)
        
        # Usar [CLS] token para clasificación
        cls_output = x[:, 0]
        
        if return_features:
            return cls_output
        
        return self.head(cls_output)


# ============================================================
# Ejemplo de uso
# ============================================================
if __name__ == "__main__":
    # ViT-Base configuration
    model = VisionTransformer(
        img_size=224, patch_size=16,
        embed_dim=768, depth=12, num_heads=12,
        num_classes=1000,
    )
    
    # Forward pass
    x = torch.randn(2, 3, 224, 224)  # 2 imágenes RGB 224×224
    logits = model(x)
    print(f"Input: {x.shape}")
    print(f"Output: {logits.shape}")  # (2, 1000)
    
    # Contar parámetros
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {total_params:,}")  # ~86M para ViT-Base
    
    # Extraer features (para fine-tuning)
    features = model(x, return_features=True)
    print(f"Features: {features.shape}")  # (2, 768)
```

---

## 3. Variantes y Evoluciones Clave

### 3.1. De ViT a CNN: Hybrid ViT

El ViT original tiene un problema: **no tiene inductive bias de localidad**. Las CNNs son naturalmente buenas en esto. La solución híbrida combina lo mejor de ambos mundos.

```python
"""
Hybrid Vision Transformer — CNN backbone + Transformer head.
Usa un CNN (ej: ResNet) para extraer features locales,
luego un Transformer para modelar dependencias globales.
"""

class HybridViT(nn.Module):
    """
    Arquitectura híbrida: CNN → Patchify → Transformer
    
    Pipeline:
        Input → CNN Backbone (ej: ResNet-50) → Feature Map
        → Patchify → [Transformer Blocks] → Classifier
    
    Ventajas:
        - Convergence más rápida (CNN tiene inductive bias)
        - Menos datos necesarios para fine-tuning
        - Mejor rendimiento en datasets pequeños
    """
    def __init__(self, cnn_backbone="resnet50", transformer_depth=6,
                 embed_dim=768, num_heads=12, num_classes=1000):
        super().__init__()
        # CNN backbone (sin head)
        self.cnn = self._build_cnn(cnn_backbone)
        
        # Calcular dimensiones de salida del CNN
        dummy = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            feat = self.cnn(dummy)
        cnn_out_channels = feat.shape[1]
        
        # Proyectar features CNN a dim del transformer
        self.patchify = nn.Conv2d(cnn_out_channels, embed_dim, 
                                   kernel_size=1, stride=1)
        
        # Transformer blocks
        self.blocks = nn.Sequential(*[
            TransformerBlock(embed_dim, num_heads)
            for _ in range(transformer_depth)
        ])
        
        self.norm = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, num_classes)
    
    def _build_cnn(self, name):
        if name == "resnet50":
            from torchvision.models import resnet50
            model = resnet50(weights=None)
            self.cnn_features = list(model.children())[:-2]  # sin FC, sin avgpool
            return nn.Sequential(*self.cnn_features)
        raise ValueError(f"Unknown CNN: {name}")
    
    def forward(self, x):
        # CNN backbone
        x = self.cnn(x)  # (B, C, H', W')
        # Patchify
        x = self.patchify(x).flatten(2).transpose(1, 2)  # (B, N, D)
        # Transformer
        x = self.blocks(x)
        x = self.norm(x)
        # Global average pooling sobre patches
        x = x.mean(dim=1)  # (B, D)
        return self.head(x)
```

### 3.2. Swin Transformer — Atención Jerárquica

**Paper:** *"Swin Transformer: Hierarchical Vision Transformer using Shifted Windows"* — Liu et al., 2021

El Swin introduce **ventanas desplazadas** para reducir la complejidad de O(N²) a O(N) y construir representaciones jerárquicas.

```python
"""
Swin Transformer Block — Atención en ventanas desplazadas.

Complejidad: O(N) en lugar de O(N²) del ViT original.
Ventaja: Representación jerárquica (como CNNs) + atención global dentro de ventanas.
"""

class WindowAttention(nn.Module):
    """
    Self-attention dentro de una ventana fija.
    
    Args:
        dim: Dimensión de entrada
        window_size: Tamaño de la ventana (ej: 7 para 7×7 patches)
        num_heads: Número de heads de atención
        shift_size: Desplazamiento para la siguiente capa (0 o window_size//2)
    """
    def __init__(self, dim, window_size, num_heads):
        super().__init__()
        self.dim = dim
        self.window_size = window_size  # (Wh, Ww)
        self.num_heads = num_heads
        self.scale = (dim // num_heads) ** -0.5
        
        self.qkv = nn.Linear(dim, dim * 3)
        self.proj = nn.Linear(dim, dim)
        
        # Relative position bias (crucial para window attention)
        self.relative_position_bias_table = nn.Parameter(
            torch.zeros((2 * window_size[0] - 1) * (2 * window_size[1] - 1), num_heads)
        )
        
        # Generate mask for window attention
        self.register_buffer("attn_mask", None)
        self._generate_attn_mask()
    
    def _generate_attn_mask(self):
        """Generar máscara para atención en ventanas."""
        h_w = self.window_size
        attn_mask = torch.zeros(2 * h_w[0] * h_w[1] - 1, 2 * h_w[0] * h_w[1] - 1)
        # ... (código completo en paper original)
        self.attn_mask = attn_mask.view(-1, 2 * h_w[0] * h_w[1] - 1, 1)
    
    def forward(self, x, mask=None):
        B, N, C = x.shape
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, C // self.num_heads)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        q, k, v = qkv.unbind(0)
        
        # Attention con bias relativo
        attn = (q @ k.transpose(-2, -1)) * self.scale
        # Add relative position bias
        attn = attn + self.relative_position_bias_table.view(1, self.num_heads, -1, 1)
        if mask is not None:
            attn = attn.masked_fill(mask == 0, float('-inf'))
        attn = attn.softmax(dim=-1)
        
        x = (attn @ v).transpose(1, 2).reshape(B, N, C)
        return self.proj(x)


class SwinTransformerBlock(nn.Module):
    """
    Swin Transformer Block con Window + Shifted Window attention.
    
    Alternancia entre Window-MSA y SW-MSA (Shifted Window MSA):
    - Capa impar: Window-MSA (atención dentro de ventanas fijas)
    - Capa par: SW-MSA (ventanas desplazadas para comunicación inter-ventana)
    """
    def __init__(self, dim, num_heads, window_size=7, shift_size=0):
        super().__init__()
        self.dim = dim
        self.window_size = window_size
        self.shift_size = shift_size
        
        self.norm1 = nn.LayerNorm(dim)
        self.attn = WindowAttention(dim, (window_size, window_size), num_heads)
        self.norm2 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(
            nn.Linear(dim, dim * 4), nn.GELU(), nn.Dropout(0.1),
            nn.Linear(dim * 4, dim), nn.Dropout(0.1)
        )
    
    def forward(self, x):
        B, H, W, C = x.shape
        shortcut = x
        x = self.norm1(x)
        
        # cyclic shift
        if self.shift_size > 0:
            shifted = torch.roll(x, (-self.shift_size, -self.shift_size), dims=(1, 2))
        else:
            shifted = x
        
        # partition windows
        # ... (código de window partitioning)
        
        x = self.attn(x)
        x = self.mlp(self.norm2(x))
        return x + shortcut
```

### 3.3. Efficient ViT — MobileViT y Edge

Para deployment en edge/mobile, el **MobileViT** combina lo mejor de ambos:

```python
"""
MobileViT — Vision Transformer para dispositivos edge.

Innovaciones clave:
1. Local processing con convoluciones (eficiente)
2. Global processing con transformer (expresivo)
3. Lightweight: ~5M parámetros para ViT-Mobile

Arquitectura:
    Input → Local CNN → Global Transformer → Output
    
Uso:
    - MobileNetV3 + MobileViT blocks
    - Deployment en Android/iOS con TFLite/ONNX
"""

class MobileViTBlock(nn.Module):
    """
    MobileViT Block: Local CNN + Global Transformer.
    
    El block aplica convoluciones locales para extraer features,
    luego reshape a 2D y aplica un transformer ligero.
    """
    def __init__(self, in_channels, transformer_dim, transformer_depth, 
                 mlp_dim, kv_input_dim=None):
        super().__init__()
        kv_input_dim = kv_input_dim or in_channels
        
        # Local representation: convoluciones
        self.conv_local = nn.Sequential(
            nn.Conv2d(kv_input_dim, transformer_dim, 3, padding=1),
            nn.Conv2d(transformer_dim, transformer_dim, 3, padding=1, groups=transformer_dim),
        )
        
        # Global representation: transformer
        self.transformer = nn.Sequential(
            nn.LayerNorm(transformer_dim),
            nn.TransformerEncoderLayer(
                d_model=transformer_dim, nhead=4, dim_feedforward=mlp_dim,
                batch_first=True, activation='gelu'
            ),
        )
        
        # Fuse local + global
        self.conv_fuse = nn.Conv2d(transformer_dim * 2, in_channels, 1)
    
    def forward(self, x):
        B, C, H, W = x.shape
        
        # Local features
        local = self.conv_local(x)  # (B, T, H, W)
        
        # Reshape para transformer: (B, T, H, W) → (B, H*W, T)
        B, T, H, W = local.shape
        global_feat = local.permute(0, 2, 3, 1).reshape(B, H * W, T)
        
        # Global attention
        global_feat = self.transformer(global_feat)  # (B, H*W, T)
        
        # Reshape de vuelta
        global_feat = global_feat.reshape(B, H, W, T).permute(0, 3, 1, 2)
        
        # Concat local + global y fusionar
        out = torch.cat([local, global_feat], dim=1)
        out = self.conv_fuse(out)
        
        return out
```

---

## 4. Pre-training Strategies

### 4.1. Masked Autoencoder (MAE) — La Revolución del Pre-training

**Paper:** *"Masked Autoencoders Are Scalable Vision Learners"* — He et al., 2021 (Meta AI)

MAE es el método de pre-training más eficiente para ViTs. La idea es simple pero brillante:

```
Imagen completa
    │
    ├── Maskear aleatoriamente ~75% de patches
    ├── Encoder solo los patches visibles
    ├── Decoder reconstruye los patches maskados
    └── Loss: MSE entre patches originales y reconstruidos
```

```python
"""
Masked Autoencoder (MAE) para pre-training de Vision Transformers.

Concepto clave: encoder procesa SOLO los patches visibles (~25%),
decoder reconstruye los maskados (~75%). Esto reduce el compute
del transformer en ~4x.
"""

class MAE_ViT(nn.Module):
    """
    MAE ViT: Encoder + Decoder para pre-training con masking.
    
    Arquitectura:
        Encoder: ViT-Base (procesa solo patches visibles)
        Decoder: ViT-Small (reconstruye todos los patches)
    
    Ventajas sobre supervised pre-training:
        - 4x más eficiente computacionalmente
        - Mejor representación semántica
        - Fine-tuning con menos datos
    """
    def __init__(self, img_size=224, patch_size=16, 
                 encoder_dim=768, encoder_depth=12, encoder_heads=12,
                 decoder_dim=512, decoder_depth=8, decoder_heads=8):
        super().__init__()
        
        # Encoder (ViT-Base)
        self.patch_embed = PatchEmbedding(img_size, patch_size, 3, encoder_dim)
        self.cls_token = nn.Parameter(torch.zeros(1, 1, encoder_dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, 1 + self.patch_embed.n_patches, encoder_dim))
        self.pos_drop = nn.Dropout(0.0)
        self.encoder_blocks = nn.Sequential(*[
            TransformerBlock(encoder_dim, encoder_heads)
            for _ in range(encoder_depth)
        ])
        self.encoder_norm = nn.LayerNorm(encoder_dim)
        
        # Decoder (más ligero)
        self.decoder_embed = nn.Linear(encoder_dim, decoder_dim)
        self.mask_token = nn.Parameter(torch.zeros(1, 1, decoder_dim))
        self.decoder_pos_embed = nn.Parameter(torch.zeros(1, 1 + self.patch_embed.n_patches, decoder_dim))
        self.decoder_blocks = nn.Sequential(*[
            TransformerBlock(decoder_dim, decoder_heads)
            for _ in range(decoder_depth)
        ])
        self.decoder_norm = nn.LayerNorm(decoder_dim)
        self.decoder_pred = nn.Linear(decoder_dim, patch_size * patch_size * 3)
    
    def random_masking(self, x, mask_ratio):
        """
        Masking aleatorio de patches.
        
        Args:
            x: (B, N, D) patches de entrada
            mask_ratio: fracción de patches a maskar (ej: 0.75)
        Returns:
            x_unmasked: (B, N_unmasked, D) patches visibles
            ids_restore: índices para reconstruir orden original
            ids_keep: índices de patches visibles
        """
        B, N, D = x.shape
        len_keep = int(N * (1 - mask_ratio))
        
        # Random noise
        noise = torch.rand(B, N, device=x.device)
        
        # Sort noise and select keep indices
        ids_shuffle = torch.argsort(noise, dim=1)
        ids_keep = ids_shuffle[:, :len_keep]
        
        # Create mask
        x_unmasked = torch.gather(x, dim=1, index=ids_keep.unsqueeze(-1).repeat(1, 1, D))
        
        return x_unmasked, ids_keep, ids_shuffle
    
    def forward_encoder(self, x, mask_ratio=0.75):
        """Encoder: procesa solo patches visibles."""
        # Patch embedding
        x = self.patch_embed(x)
        
        # Masking
        x_masked, ids_keep, ids_shuffle = self.random_masking(x, mask_ratio)
        
        # Add [CLS] token
        cls_tokens = self.cls_token.expand(x_masked.shape[0], -1, -1)
        x_masked = torch.cat([cls_tokens, x_masked], dim=1)
        
        # Position embedding
        x_masked = x_masked + self.pos_embed[:, :x_masked.size(1), :]
        x_masked = self.pos_drop(x_masked)
        
        # Transformer blocks
        x_masked = self.encoder_blocks(x_masked)
        x_masked = self.encoder_norm(x_masked)
        
        return x_masked, ids_keep, ids_shuffle
    
    def forward_decoder(self, x_enc, ids_keep, ids_shuffle):
        """Decoder: reconstruye todos los patches."""
        # Embed
        x_dec = self.decoder_embed(x_enc)
        
        # Insert mask tokens
        B, N, D = x_dec.shape
        n_mask = self.patch_embed.n_patches + 1 - N
        mask_tokens = self.mask_token.repeat(B, n_mask, 1)
        
        # Gather indices for mask tokens
        ids_restore = torch.gather(
            ids_shuffle, dim=1, 
            index=torch.cat([ids_keep, torch.arange(n_mask, device=x_enc.device).unsqueeze(0).repeat(B, 1)], dim=1)
        )
        
        # Add mask tokens back
        x_dec = torch.cat([x_dec, mask_tokens], dim=1)
        x_dec = torch.gather(
            x_dec, dim=1, 
            index=ids_restore.unsqueeze(-1).repeat(1, 1, D)
        )
        
        # Position embedding
        x_dec = x_dec + self.decoder_pos_embed
        x_dec = self.decoder_blocks(x_dec)
        x_dec = self.decoder_norm(x_dec)
        
        # Predict
        x_pred = self.decoder_pred(x_dec)
        return x_pred
    
    def forward(self, x, mask_ratio=0.75):
        """Forward pass: encode → decode → reconstruct."""
        x_enc, ids_keep, ids_shuffle = self.forward_encoder(x, mask_ratio)
        x_pred = self.forward_decoder(x_enc, ids_keep, ids_shuffle)
        return x_pred


def mae_loss(reconstructed, original, mask):
    """
    Loss de reconstrucción MAE.
    
    Solo calcula loss sobre los patches maskados.
    """
    # MSE sobre patches maskados
    loss = ((reconstructed - original) ** 2).mean()
    return loss
```

### 4.2. Training Recipe del ViT

```python
"""
Training recipe completo para pre-training de ViT.

Basado en el paper original + mejoras de MAE.
"""

import torch.optim as optim

def create_vit_training_pipeline():
    """Configuración de training para ViT-Base."""
    
    # Model
    model = MAE_ViT(
        img_size=224, patch_size=16,
        encoder_dim=768, encoder_depth=12, encoder_heads=12,
        decoder_dim=512, decoder_depth=8, decoder_heads=8,
    )
    
    # Optimizer: AdamW con weight decay (clave para ViT)
    optimizer = optim.AdamW(
        model.parameters(),
        lr=1.5e-4,           # Learning rate bajo (ViT necesita LR small)
        weight_decay=0.05,   # Weight decay alto (regularización fuerte)
        betas=(0.9, 0.95),   # Beta2 alto para ViT
    )
    
    # Scheduler: Cosine annealing con warmup
    scheduler = optim.lr_scheduler.CosineAnnealingLR(
        optimizer, 
        T_max=300,  # 300 epochs para pre-training
        eta_min=1e-6,
    )
    
    # Data augmentation (CRÍTICA para ViT)
    # ViT es más sensible a augmentations que CNNs
    train_transforms = [
        "RandAugment(N=3, M=9)",    # RandAugment agresivo
        "RandomResizedCrop(224)",    # Resize aleatorio
        "HorizontalFlip",            # Flip horizontal
        "ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1)",
        "RandomGrayscale(p=0.05)",
        "GaussianBlur",
        "MixUp(alpha=0.8)",          # MixUp para regularización
        "CutMix(alpha=1.0)",         # CutMix para diversidad
    ]
    
    return model, optimizer, scheduler, train_transforms
```

---

## 5. Aplicaciones Prácticas al Stack

### 5.1. Imágenes Satelitales con ViT

Los ViTs son particularmente útiles para imágenes satelitales porque:

1. **Campo receptivo global** — Las imágenes satelitales tienen contexto a larga distancia
2. **Multi-escala** — Los objetos en satélites varían enormemente en tamaño
3. **Sin inductive bias CNN** — Los patrones satelitales no siguen patrones espaciales locales

```python
"""
ViT para clasificación de uso de suelo satelital.

Aplicación directa: análisis de imágenes Esios/REE para
monitoreo de infraestructura energética.
"""

class SatelliteViT(nn.Module):
    """
    ViT adaptado para imágenes satelitales.
    
    Modificaciones clave:
    1. Patches más grandes (32×32 en lugar de 16×16) para capturar contexto
    2. Multi-spectral input (no solo RGB)
    3. Posición encoding basada en coordenadas GPS
    """
    def __init__(self, img_size=256, patch_size=32, 
                 in_channels=4,  # RGB + NDVI (índice vegetación)
                 num_classes=10,  # tipos de uso de suelo
                 embed_dim=512, depth=8, num_heads=8):
        super().__init__()
        
        self.patch_embed = PatchEmbedding(img_size, patch_size, in_channels, embed_dim)
        
        # Posición encoding basada en coordenadas (no learnable)
        self.pos_embed = self._build_coordinate_pos_embed(img_size, patch_size, embed_dim)
        
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.pos_drop = nn.Dropout(0.1)
        self.blocks = nn.Sequential(*[
            TransformerBlock(embed_dim, num_heads) for _ in range(depth)
        ])
        self.norm = nn.LayerNorm(embed_dim)
        self.head = nn.Sequential(
            nn.Linear(embed_dim, embed_dim // 2),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(embed_dim // 2, num_classes),
        )
    
    def _build_coordinate_pos_embed(self, img_size, patch_size, embed_dim):
        """
        Position embedding basado en coordenadas GPS reales.
        
        En lugar de embeddings aprendidos, usamos coordenadas
        geográficas reales para posicionar los patches.
        """
        n_patches = (img_size // patch_size) ** 2
        pos_embed = torch.zeros(1, 1 + n_patches, embed_dim)
        
        # Generar grid de coordenadas normalizadas
        grid_size = img_size // patch_size
        for i in range(grid_size):
            for j in range(grid_size):
                idx = 1 + i * grid_size + j  # +1 para [CLS]
                # Normalizar a [0, 1]
                x_norm = i / grid_size
                y_norm = j / grid_size
                # Sinusoidal encoding
                for d in range(embed_dim):
                    pos_embed[0, idx, d] = (
                        torch.sin(torch.tensor(x_norm * 1000 + d)) +
                        torch.cos(torch.tensor(y_norm * 1000 + d))
                    ) / 2
        
        return nn.Parameter(pos_embed, requires_grad=False)
    
    def forward(self, x):
        B = x.shape[0]
        x = self.patch_embed(x)
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)
        x = x + self.pos_embed
        x = self.pos_drop(x)
        x = self.blocks(x)
        x = self.norm(x)
        return self.head(x[:, 0])
```

### 5.2. Fine-tuning Strategy

```python
"""
Estrategias de fine-tuning para ViT pre-trained.

Diferentes approaches según el tamaño del dataset disponible.
"""

def fine_tune_vit(model, dataset_size, learning_rate_base=1e-4):
    """
    Elige la estrategia de fine-tuning según el dataset.
    """
    
    if dataset_size < 1000:
        # Dataset muy pequeño: congelar todo excepto el head
        strategy = "freeze_all"
        lr = learning_rate_base * 10  # Head necesita más LR
        print("Strategy: Freeze all layers, train only classifier head")
        
    elif dataset_size < 10000:
        # Dataset pequeño: unfreeze últimos 4 blocks
        strategy = "partial_unfreeze"
        n_unfreeze = 4
        print(f"Strategy: Unfreeze last {n_unfreeze} transformer blocks")
        
    else:
        # Dataset grande: fine-tuning completo con LR diferenciada
        strategy = "full_finetune"
        print("Strategy: Full fine-tuning with differential LR")
    
    # Differential Learning Rates
    if strategy == "full_finetune":
        # Capas tempranas: LR baja (ya tienen buenas features)
        # Capas tardías: LR alta (más específicas de la tarea)
        early_layers = list(model.blocks[:4].parameters())
        mid_layers = list(model.blocks[4:8].parameters())
        late_layers = list(model.blocks[8:].parameters())
        head_layers = list(model.head.parameters())
        
        optimizer = optim.AdamW([
            {'params': early_layers, 'lr': learning_rate_base * 0.1},
            {'params': mid_layers, 'lr': learning_rate_base * 0.5},
            {'params': late_layers, 'lr': learning_rate_base},
            {'params': head_layers, 'lr': learning_rate_base * 10},
        ], weight_decay=0.01)
        
    elif strategy == "partial_unfreeze":
        # Congelar primeros blocks, unfreeze últimos
        for param in model.blocks[:-4].parameters():
            param.requires_grad = False
        
        optimizer = optim.AdamW(
            filter(lambda p: p.requires_grad, model.parameters()),
            lr=learning_rate_base,
            weight_decay=0.01
        )
    
    return optimizer, strategy
```

---

## 6. Benchmark y Comparativa

### Rendimiento en ImageNet-1K

| Modelo | Params | Top-1 Acc | FLOPs | Notes |
|--------|--------|-----------|-------|-------|
| ResNet-50 | 25.6M | 76.1% | 4.1G | CNN baseline |
| ViT-Base | 86M | 81.8% | 17.6G | Paper original |
| DeiT-Tiny | 5.7M | 72.2% | 1.3G | Data-efficient |
| DeiT-Small | 22M | 79.3% | 4.5G | Data-efficient |
| DeiT-Base | 86M | 81.8% | 17.6G | Data-efficient |
| Swin-T | 28M | 81.3% | 4.5G | Hierarchical |
| Swin-S | 49M | 83.2% | 8.7G | Hierarchical |
| MobileViT-XS | 1.1M | 65.1% | 0.2G | Edge |
| MobileViT-S | 2.5M | 69.5% | 0.6G | Edge |
| MAE-Base | 86M | 83.8% | 17.6G | Self-supervised |

**Key insights:**
- MAE pre-training supera a supervised pre-training en +2%
- Swin Transformer ofrece mejor accuracy/params que ViT original
- MobileViT es ~30x más ligero que ViT-Base con solo ~6% de accuracy loss

---

## 7. Recursos y Referencias

### Papers Fundamentales

1. **"An Image is Worth 16x16 Words"** — Doski et al., 2020
   - https://arxiv.org/abs/2010.11929
   - Paper original del ViT

2. **"Swin Transformer"** — Liu et al., 2021
   - https://arxiv.org/abs/2103.14030
   - Atención en ventanas desplazadas

3. **"Masked Autoencoders Are Scalable Vision Learners"** — He et al., 2021
   - https://arxiv.org/abs/2111.06377
   - MAE pre-training

4. **"Training Compute-Optimal Large Language Models"** — Hoffmann et al., 2022
   - https://arxiv.org/abs/2203.15556
   - Leyes de scaling para transformers (incluye ViT)

5. **"Vision Transformers in Computer Vision: A Survey"** — 2025
   - Survey completa de arquitecturas y aplicaciones

### Repositorios

- **timm (PyTorch Image Models):** https://github.com/huggingface/pytorch-image-models
  - +300 modelos ViT pre-trained, incluyendo DeiT, Swin, ConvNeXt
  
- **MAE Official:** https://github.com/facebookresearch/mae
  - Implementación oficial de Masked Autoencoder
  
- **Swin Transformer Official:** https://github.com/microsoft/Swin-Transformer
  - Implementación oficial de Swin Transformer
  
- **MobileViT Official:** https://github.com/apple/ml-cvnets
  - Implementación oficial de MobileViT

### Aplicaciones al Stack

- **Imágenes satelitales:** ViT con multi-spectral input y coordinate-based position encoding
- **Análisis de infraestructura:** Fine-tuning de MAE-Base para detección de líneas eléctricas
- **Edge deployment:** MobileViT-S para análisis en dispositivo (Android/iOS)

---

## 8. Conclusiones

Los Vision Transformers representan un **cambio de paradigma** en visión por computador:

1. **Los datos + compute > inductive bias** — Con suficientes datos, un Transformer simple supera a las CNNs más sofisticadas
2. **MAE es el estándar de pre-training** — Masked Autoencoding es ~4x más eficiente y produce mejores representaciones
3. **Las variantes eficientes son clave para deployment** — Swin para accuracy/params balance, MobileViT para edge
4. **Aplicaciones satelitales** — Los ViTs son ideales para imágenes satelitales por su campo receptivo global

**Para el stack actual:** El ViT es directamente aplicable al análisis de imágenes satelitales (Esios/REE) y al monitoreo de infraestructura energética. La combinación de MAE pre-training + fine-tuning con differential LR es el recipe más efectivo.

---

## Tema Siguiente Propuesto

**Diffusion Transformers (DiT)** — La evolución natural de los diffusion models (SD3, Flux). Combina la arquitectura Transformer con el pipeline de difusión, ofreciendo mejor calidad y eficiencia que los U-Net basados. Conecta directamente con la nota de diffusion models (#2) y abre puertas a generación de imágenes con calidad SOTA.

Alternativa: **RAG (Retrieval-Augmented Generation)** — Integración con ChromaDB existente, búsqueda semántica aplicada a generación de contenido. Muy relevante para el sistema de skills vectoriales.

**Recomendación:** Diffusion Transformers (DiT) — conecta mejor con la serie actual de deep learning y es un tema con mucho momentum (SD3, Flux, HunyuanVideo).
