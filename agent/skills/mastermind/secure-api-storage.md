---
name: secure-api-storage
description: "Gestión segura de API keys y tokens en Mastermind — dónde guardarlas, cómo usarlas, migración a NaN Cloud Env"
version: 1.0.0
author: Mastermind
tags: [security, apis, tokens, env, nan]
---

# Secure API Storage

## Filosofía
Las API keys NUNCA se incluyen en repositorios (ni públicos ni privados). Se almacenan en variables de entorno del servidor.

## Ubicaciones seguras

### 1. `/root/.env` (archivo local)
- Solo accesible por root (tú + Mastermind)
- Se carga con `source /root/.env`

### 2. NaN Cloud Env (recomendado)
- Pestaña Env en cloud.nan.builders > microVM
- **Persiste entre reinicios** del microVM
- Solo accesible desde la microVM (ni siquiera el dashboard lo muestra)

## APIs actuales

| API | Variable | Dónde está |
|-----|----------|-----------|
| GitHub (repo) | `GITHUB_TOKEN` | `/root/.env` → **migrar a NaN Env** |
| ESIOS (Red Eléctrica) | `ESIOS_API_TOKEN` | `/root/.env` → **migrar a NaN Env** |
| NAP Transportes | `NAP_API_KEY` | Pendiente de recibir |

## Cómo añadir una nueva API

1. El usuario me pasa la key por Telegram
2. La guardo en `/root/.env` con `echo 'export NOMBRE="valor"' >> /root/.env`
3. Le pido que la añada también en NaN Cloud Env (persistente)
4. Guardo en memoria que existe para poder usarla en proyectos futuros

## Cómo usar una API guardada

```bash
source /root/.env
curl -H "Authorization: Bearer $TOKEN" https://api.ejemplo.com/...
```

## Pendiente
- Migrar TODAS las keys de `/root/.env` a NaN Cloud Env tab
- El usuario debe entrar en cloud.nan.builders y pegarlas