---
name: autoencoder-diffusion
description: "Autoencoders para diffusion: VAE, VQ-VAE, VQGAN, DAE, autoencoders jerárquicos. Reglas de diseño, métricas, y selección del autoencoder correcto."
version: "1.0.0"
author: mastermind
tags: [autoencoder, vae, vqvae, vqgan, diffusion, latent, compression]
---

# Autoencoders para Diffusion

## Resumen

Los autoencoders son **el motor oculto** de la generación de imágenes con diffusion. Todo modelo difusivo moderno (Stable Diffusion, DALL-E, Flux) opera en un espacio latente comprimido por un autoencoder.

## Tipos de Autoencoder

### 1. VAE (Variational Autoencoder)
- Espacio latente continuo: z ~ N(μ, σ²)
- Usado en: Stable Diffusion 1.x/2.x, SDXL
- Compresión típica: 8× (512×512→64×64)
- Canales: 4

### 2. VQ-VAE (Vector Quantized VAE)
- Espacio latente discreto: K embeddings en códigobook
- Usado en: DALL-E 1/2, Parti
- Compresión: 8× pero tokens discretos
- Canales post-cuantización: 1 token/posición

### 3. VQGAN
- VQ-VAE + GAN + Perceptual Loss (VGG)
- Calidad fotorealista para la reconstrucción
- Usado en: DALL-E 1, StyleGAN integration

### 4. DAE (Diffusion Autoencoder)
- Diffusion como decoder: p(x|z)
- Compresión extrema: 32×-128×
- Calidad superior: el decoder es probabilístico

### 5. Hierarchical Autoencoder (HF 1/2×1/32)
- Multi-escala con códigobook por nivel
- Compresión: ~10,000×
- Latent: 16×16×16 para 512px

## Reglas de Diseño (HuggingFace 2024)

1. Compresión >= 8x es minimo
2. 4 canales para compresion 8x, 16 para 32x
3. Usar strided conv (no pooling)
4. Skip connections obligatorias
5. BatchNorm training -> GroupNorm inference
6. SiLU > ReLU > GELU
7. Dropout bajo (0.1), weight decay (1e-4)

## Selección del Autoencoder

| Uso | Calidad | Recomendacion |
|-----|---------|---------------|
| Imagen gen | alta | HF 1/2x1/32 |
| Imagen gen | balance | SD 2.x |
| Video gen | alta | DAE 3D |
| Realtime | rapida | SD 1.x |
| Controlnet | balance | SD 1.x |

## Métricas

- PSNR: >30 dB = bueno
- SSIM: >0.9 = bueno
- LPIPS: <0.1 = bueno (menos = mejor)

## Recursos

- Nota completa: /hermes-home/notes/deep-learning/2026-07-16-variational-autoencoders-vae-vqgan-diffusion.md
- Paper VAE: arXiv:1312.6114
- Paper VQGAN: arXiv:2112.10752
- Paper DAE: arXiv:2403.12372