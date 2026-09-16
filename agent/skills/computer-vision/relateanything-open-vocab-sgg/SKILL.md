---
name: relateanything-open-vocab-sgg
description: "Usa al predecir relaciones entre objetos en tiempo real."
version: "1.0.0"
author: Mastermind (stars-explorer)
license: Apache-2.0
metadata:
  hermes:
    tags: [computer-vision, scene-graph, open-vocabulary, sgg, dinov3, onnx, tiempo-real, video]
    related_skills: [moondream-vlm, roboflow-supervision, traffic-digital-twin-cctv, satellite-ai-vision, pose-based-motion-metrics]
---

# RelateAnything — Relaciones open-vocabulary en tiempo real (OV-SGG)

**Repo:** https://github.com/Maelic/RelateAnything (112⭐, Python 3.12+, Apache-2.0, activo; arXiv:2609.12552; verificado 2026-09-16 contra README + `docs/quickstart.md` + `docs/pitfalls.md` + `deploy/render_video.py` reales). 53.2M params, ~20 ms/frame en A40.

**Cuándo usarlo:** cuando hay que extraer del vídeo/imagen triplas ⟨sujeto, predicado, objeto⟩ con un **vocabulario de predicados definido por el usuario en inferencia** (p.ej. "about to collide with", "casting a shadow on"), sin reentrenar y sin que el modelo vea nunca etiquetas de clase de objeto.

## Las 3 propiedades que lo distinguen

1. **Vocabulario de predicados en inferencia** — cualquier string vale; cambiarlo cuesta una pasada del text encoder pequeño y luego la inferencia es visión pura (sin LM en el bucle). El modelo no puede emitir nada fuera de la lista.
2. **Las clases de objeto NUNCA son input** — píxeles + regiones dentro, relaciones fuera. Se puede cambiar el detector o usar un segmenter agnóstico de clase sin tocar el modelo de relaciones.
3. **Una forward pass → un ranking o dos grafos** (espacial + semántico). Un par puede estar en ambos a la vez (coexistencia intencionada).

## API verificada

```bash
git clone https://github.com/Maelic/RelateAnything && cd RelateAnything
pip install -e ".[hub]"          # torch, transformers, huggingface_hub
pip install -e ".[deploy]"       # ONNX Runtime + demo laptop (opcional)
```

```python
from relsgg import RelateAnything

model = RelateAnything.from_pretrained("maelic/relsgg-vits16plus", device="cuda")
triplets = model.predict(image, boxes_xyxy, topk=20)   # PIL o HWC numpy; boxes [N,4] px, frame ORIGINAL
# t.subject_idx, t.predicate, t.score, t.object_idx — (person)--riding[0.91]-->(horse)

model.set_vocabulary(["about to collide with", "reflected in"])   # sin reentrenar
graphs = model.predict(image, boxes_xyxy, masks=masks, decompose=True)
graphs["spatial"]; graphs["semantic"]      # dos grafos, una pasada

model = RelateAnything.from_pretrained("maelic/relsgg-vits16plus", full_vocabulary=True)
# responde sobre los 19.103 predicados de entrenamiento (embeddings incluidos)
```

Checkpoints (`maelic/relsgg-*` en HF): `vits16` 46M, **`vits16plus` 53M ⭐ recomendado**, `vitb16` 114M. Latencia plana entre los tres a batch 1 (dispatch-bound). Publicado como un solo grafo ONNX: corre en CPU de portátil (7 FPS OpenVINO 8 hilos) y **en el navegador** (demo oficial). Datasets: RA-4M; benchmark OV-SGG-Bench (protocolo de 6 ejes para que ninguna métrica se gane por compartir vocabulario con el corpus de entrenamiento).

## Estabilización temporal para vídeo (patrón reutilizable)

El head de relaciones es por-frame y no tiene memoria: boxes con jitter, detector que alterna "man"/"person", relaciones cerca del umbral que parpadean. Los 4 fixes de `deploy/render_video.py` van FUERA del modelo:

1. **Tracking IoU** → identidades persistentes (color y label estables por sujeto).
2. **EMA** sobre coords de box y scores, con término de velocidad (EMA sola va a la zaga en lo que se mueve).
3. **Histéresis de 2 umbrales**: aparecer tras `on_thr` durante `on_frames`, irse bajo `off_thr` durante `off_frames`.
4. **Fades alfa** en entrada/salida de aristas.

Inferencia a `--stride 2` pero render de cada frame: el suavizador lleva el overlay por los huecos → asequible en CPU. `--scan footage/` rankea clips por contenido real de interacción antes de renderizar nada.

## Pitfalls (de docs/pitfalls.md — "cada uno produjo un resultado plausible y erróneo al menos una vez")

- **`box_labels` es decorativa**: no alimenta el modelo, solo hace legible el `__repr__`.
- **`box_scores` cambia el RANKING, no los scores**: ranking = conf(sub)·conf(obj)·pred_score (convención SGDet). Omitir para boxes de ground truth.
- **El coste escala cuadrático con el nº de boxes** antes del sampler → `max_boxes` (60 default) es la perilla que acota una escena abarrotada.
- **La restricción de grafo infla R@K 12–19 puntos**: comparar solo comparativas con el mismo lado del flag.
- **Los diagnósticos de entrenamiento no son resultados** (sin restricción, sobre las 19K): nunca citar un spatial≈0 del log sin el valor real graph-constrained (10–200× mayor).
- **Recall de string exacto sobre 19K vocabulario engaña**: un 0.006 suele ser fragmentación de sinónimos ("right of"), no falta de capacidad — comprobar el grupo de sinónimos antes de diagnosticar.
- **Sin flips horizontales** en entrenamiento/eval: el vocabulario contiene "to the left of"/"to the right of" — un flip invierte silenciosamente la verdad.
- El despiece espacial/semántico es regla híbrida (flag del corpus si el string es conocido, gate del checkpoint si no): el flag solo está contaminado por procedencia (`on`=0.985 espacial pero su sinónimo "resting on"=0.001).

## Comparativa de alternativas (2026-09)

- **VLMs genéricos (moondream, Qwen-VL…)**: responden relaciones en texto libre pero proponen solo 23–35% de los pares anotados (RelateAnything: 99.7%) y no dan scores calibrados ni batching a 40 FPS. Usar VLM para preguntas abiertas; usar este para grafos estructurados por frame.
- **ROBIN-3B** (SGG sobre VLM 3B): líder F1@50 frente a OvSGTR pero por detrás en todos los ejes; el orden en open-vocab depende del matcher de sinónimos.
- **OvSGTR** (baseline clásico): necesita etiquetas de objeto (que RelateAnything nunca ve) y vocabulario fijo ~150 strings.

## Encaje con proyectos de David

- CCTV/tráfico: "car_x about to collide with pedestrian_y" con predicados del dominio, ONNX en navegador.
- geo-forensics / satélite: relaciones sombra-objeto, adyacencias con frases a medida.

## Verificación

`model.predict` sobre una imagen con boxes de un detector cualquiera → si todos los scores caen bajo el umbral calibrado, revisar antes el frame de boxes (píxeles, origen arriba-izq, sin redimensionar) que al modelo.
