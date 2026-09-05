---
name: docuseal
description: "Usa a gestionar firmas electrónicas con DocuSeal."
version: "2.0.0"
tags: [docuseal, firma, e-signature, rubi, rails, documentos, self-host]
related_skills: [docuseal, document-conversion, docx, xlsx]
---

# DocuSeal — plataforma de firma electrónica (self-host)

> ⚠️ Corrección 2026-09-05 (auditoría): es **Ruby (Rails)**, no TypeScript/Node; es una plataforma de **e-signature** (crear, rellenar y firmar documentos, alternativa a DocuSign) — no "generación de documentos con IA". No existe una librería JS `docuseal.createDocument()`/`doc.addSignature()`.

**Repo:** `https://github.com/docusealco/docuseal` (Ruby/Rails, ~18K⭐).

## When to Use

- Cuando pidas **firma y gestión de documentos** (subir plantilla, rellenar campos, firmar, enviar a firmar) autoalojada o vía SaaS.

## Qué es

Plataforma **de firma electrónica**: subes un documento/plantilla, defines campos-firma (field-tags) y los firmantes los rellenan y firman. Alternativa open-source a DocuSign.

## Uso (API)

- **API REST** + **HTML API** con field-tags para plantillas (define campos con etiquetas en el HTML del documento).
- *(No hay librería JS oficial `docuseal`; se habla con la API REST o se usa la UI.)*

```bash
# self-host (Docker)
docker run -e DATABASE_URL=... docuseal/docuseal
# o vía su servicio cloud en docuseal.com
```

## Pitfalls

- Lenguaje: **Ruby (Rails)**, no TypeScript/Node.
- Reencuadre: **firma electrónica**, no "generación de documentos con IA".
- API: **REST + field-tags**; no hay `docuseal.createDocument()`/`doc.addSignature()` (inventado).

## Verificación

- Subir una plantilla con field-tags, crear un documento y enviarlo a firmar; comprobar que el firmante rellena y firma.
