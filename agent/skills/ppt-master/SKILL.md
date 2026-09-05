---
name: ppt-master
description: "Usa a generar PowerPoints PPTx con PPT-Master."
version: "2.0.0"
tags: [presentations, powerpoint, pptx, ppt-master, python, seguridad, ppts]
related_skills: [ppt-master, powerpoint, consulting-slide-rulebook]
---

# PPT-Master — generación de presentaciones con estructura

> ⚠️ Corrección 2026-09-05 (auditoría): `pip install ppt-master` instala un paquete PyPI NO relacionado. La instalación correcta es clonar el repo y `pip install -r requirements.txt`.

**Repo:** `https://github.com/hugohe3/ppt-master` (Python, ~52K⭐).

## When to Use

- Cuando pidas **generar presentaciones PowerPoint (PPTX)** con estructura, diapositivas y temas consistentes.

## Uso

```bash
git clone https://github.com/hugohe3/ppt-master.git
cd ppt-master
pip install -r requirements.txt
```

*(NO `pip install ppt-master` — ese nombre es de un paquete PyPI distinto de generación de SVG.)*

## Pitfalls

- Instalación correcta = **clonar + `pip install -r requirements.txt`**, no `pip install ppt-master`.
- El nombre de PyPI colisiona con un paquete no relacionado — no confiar en el nombre del paquete.

## Verificación

- Producir un deck de prueba y abrir el `.pptx`; comprobar que las diapositivas/tema salen íntegros.
