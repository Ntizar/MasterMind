---
name: infinite-ocr
description: Baidu Unlimited OCR — OCR gratuito de alta calidad sin límites de uso.
category: data-pipeline
---

# Baidu Unlimited OCR — OCR Sin Límites

## Qué es

Baidu Unlimited OCR es un servicio de reconocimiento óptico de caracteres (OCR) gratuito:
- **Sin límites** — gratis y sin límites de uso
- **Alta calidad** — motor OCR de Baidu, muy preciso
- **Multi-idioma** — soporta chino, inglés y más
- **API REST** — fácil integración

## Instalación

```python
# API directa
import requests

def ocr_image(image_path):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            'https://api.unlimitedocr.com/api/ocr',
            files=files
        )
    return response.json()
```

## Casos de uso para David

- **Document processing** — extraer texto de imágenes/PDFs
- **Integration** — usar con Marker para pipeline completo
- **Satellite imagery** — OCR en imágenes satelitales
- **Data extraction** — extraer datos de documentos escaneados

## Pitfalls

- API de Baidu — verificar disponibilidad en Europa
- Depende de conexión a internet
- Calidad variable con imágenes de baja resolución
- No es OCR especializado — genérico

## Referencias

- Repo: `github.com/baidu/Unlimited-OCR` (13K⭐)
