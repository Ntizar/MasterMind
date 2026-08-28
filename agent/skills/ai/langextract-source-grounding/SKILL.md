---
name: langextract-source-grounding
version: "1.0.0"
description: "Use al extraer datos estructurados de texto con LLMs."
tags: [llm, extraction, structured-data, grounding, nlp, gemini, ollama, visualization]
---

# LangExtract — Extracción estructurada con grounding a la fuente

## Resumen

[LangExtract](https://github.com/google/langextract) (⭐38K, Apache-2.0, Google) extrae información estructurada de texto no estructurado con LLMs. Su diferencia clave: **cada extracción se mapea a su posición exacta en el texto fuente** (`char_interval`), lo que permite verificar y resaltar visualmente cada dato extraído.

## Cuándo usar

- Extraer campos estructurados (entidades, atributos, relaciones) de documentos largos
- Pipelines donde la trazabilidad importa: cada dato debe apuntar a su cita textual
- Informes a partir de notas/reportes (ej. estructurar informes médicos, actas, PDFs convertidos)
- Alternativa a prompt engineering ad-hoc: validación de schema + few-shot sin fine-tuning

## Uso básico

```bash
pip install langextract
```

```python
import langextract as lx
import textwrap

# 1. Prompt con reglas de extracción
prompt = textwrap.dedent("""\
    Extracta caracteres, emociones y relaciones en orden de aparición.
    Usa el texto exacto para las extracciones, no parafrasees ni superpongas entidades.""")

# 2. Ejemplos few-shot (extraction_text VERBATIM del ejemplo)
examples = [lx.data.ExampleData(
    text="ROMEO. But soft! What light through yonder window breaks?",
    extractions=[
        lx.data.Extraction(extraction_class="character", extraction_text="ROMEO",
                           attributes={"emotional_state": "wonder"}),
    ],
)]

# 3. Extraer
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-3.5-flash",   # u openai/gpt-..., o Ollama local
    api_key="...",                  # o env LANGEXTRACT_API_KEY
)
```

## Documentos largos

```python
result = lx.extract(
    text_or_documents="https://url/texto.txt",  # acepta URLs directas
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-3.5-flash",
    extraction_passes=3,    # múltiples pasadas → mayor recall
    max_workers=20,         # procesamiento paralelo de chunks
    max_char_buffer=1000,   # chunks pequeños → mejor precisión
)
```

## Visualización interactiva

```python
lx.io.save_annotated_documents([result], output_name="resultados.jsonl", output_dir=".")
html = lx.visualize("resultados.jsonl")
with open("visualizacion.html", "w", encoding="utf-8") as f:
    f.write(html.data if hasattr(html, "data") else html)
```

Genera un HTML autónomo con las entidades resaltadas en contexto — útil para revisión humana.

## Grounding: filtrar alucinaciones

Las extracciones que el LLM no puede localizar en el texto fuente llegan con `char_interval = None`. Filtrarlas SIEMPRE:

```python
grounded = [e for e in result.extractions if e.char_interval]
```

## Proveedores

- Gemini (recomendado: `gemini-3.5-flash`; flash-lite para volumen; Pro para tareas complejas)
- OpenAI y cualquier API OpenAI-compatible (custom providers)
- Ollama para modelos locales sin API key
- Vertex AI Batch API para grandes volúmenes con descuento: `language_model_params={"vertexai": True, "batch": {"enabled": True}}`

## Integración con otros skills

- **marker-pdf-conversion**: PDF → markdown con Marker → extracción estructurada con LangExtract (pipeline documental completo)
- **rag-knowledge-base**: LangExtract como capa de enriquecimiento previa a la indexación
- **ai-report-generation**: datos extraídos con citas verificables → informes auditables

## Pitfalls

- **Ejemplos mal alineados**: si los `extraction_text` de los few-shot no son verbatim, LangExtract lanza warnings de "Prompt alignment" — resolverlos, degradan calidad
- **Extracciones no grounded**: sin filtrar `char_interval = None`, los resultados incluyen texto inventado
- **Modelos Gemini retirables**: los IDs de modelo tienen lifecycle; consultar docs oficiales antes de fijar uno en producción
- **Rate limits en tier gratuito**: para producción usar tier de pago o batch API
- **Windows**: la visualización requiere escribir el HTML a archivo (en Jupyter devuelve objeto distinto)

## Verificación

```bash
pip show langextract && python -c "import langextract as lx; print(lx.__version__)"
```

---
**Hecho con ❤️ por David Antizar**