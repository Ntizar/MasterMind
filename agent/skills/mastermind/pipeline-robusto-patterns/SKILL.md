---
name: pipeline-robusto-patterns
description: "Aplicar patrones de pipeline robusto en pipelines de datos."
version: "0.1.0"
tags: [mastermind, pipeline, patrones, robustez, arquitectura]
---

# Pipeline Robusto — Patrones (de helmcode-whisper)

Lecciones transferibles del repo helmcode/helmcode-whisper que aplican a los pipelines de datos de Ntizar. El repo es un grabador/transcriptor de reuniones self-hosted; lo valioso no es lo que hace, sino cómo está pensado: cada decisión reduce el trabajo del paso difícil en lugar de añadirle complejidad.

## When to Use

- Diseñar o revisar un pipeline de datos (fetch → normalizar → procesar → salida).
- Cuando un paso de un pipeline es "caro o impreciso" y se busca que lo sea menos resolviendo un problema aguas arriba.
- Al tocar código que consume APIs externas (límites de concurrencia, hosts permitidos).
- Cuando el output debe tener forma estable y el sistema degradar en vez de romperse.
- Escribir/editar prompts que generan salida estructurada de un LLM.

No usar para: documentar este repo concreto; para eso va una nota en `notes/`.

## Los patrones

### 1. Resolver el problema en la captura, no en el modelo
helmcode-whisper graba micrófono y audio de sistema en DOS pistas separadas: "near vs far" se decide por el archivo, y pyannote solo tiene que desenredar al remoto. Idea clave: *particiona el problema en el origen* para que el paso difícil se vuelva trivial.

**Cómo aplicarlo:** si en un pipeline ya conoces la partición por construcción (isócronas por transporte, GTFS por dirección/agencia, series por fuente), sepárala en la fuente de datos en vez de dejar que el modelo lo adivine. Ante un paso caro o impreciso, pregunta primero: ¿se puede conocer esto ANTES, a partir de cómo capturo/particiono los datos?

### 2. Tests que imponen invariantes de arquitectura
`tests/test_no_egress.py` rompe el build si aparece cualquier host que no sea el de la API. No es una promesa en un README, es una regla verificada por CI.

**Cómo aplicarlo:** invariantes de arquitectura ("solo estos endpoints", "estas tablas son read-only") se imponen con un test, no con disciplina. En pipelines que tocan APIs externas: whitelist de hosts permitidos + test que falle el build si algo sale a otro lado.

### 3. Degradación en escalera con contrato de salida fijo
Nunca falla en duro. Si `json_schema` falla → baja a modos más laxos. Si pyannote no va → `Me, Others`. Si no hay audio de sistema → solo micrófono y avisa una vez. **La forma del output es fija; la ruta degrada.**

**Cómo aplicarlo:** define el contrato de salida de forma estable; en caso de fallo el pipeline se simplifica (calidad), pero el consumer nunca ve un resultado con forma distinta. Es la regla "no reemplazar funcional por roto": degradar, nunca romper.

### 4. Prompt como artefacto, modelo intercambiable, salida fijada
`templates/notes.md` es un fichero del repo (editable, versionado) con placeholders `{{VAR}}`, usando `.replace()` (no `.format()` — coincide con la nota de qwen NaN). El LLM es una variable (`HCW_NOTES_MODEL`) desacoplada de la forma del output (fijada por un JSON schema).

**Cómo aplicarlo:** separa el contrato de datos de salida (schema) del modelo que lo produce (config). Los prompts viven como archivos versionados en el repo, con placeholders reemplazables por `.replace()` — nunca `.format()`.

### 5. Un solo pool compartido + conocer el límite de la API
4 requests concurrentes a través de un MISMO pool que cubre ambas tracks (un pool por track dejaría al micro esperando al sistema). Y 4, no más: la API permite 5 en paralelo y hace 429 al sexto.

**Cómo aplicarlo:** conoce el límite de concurrencia del proveedor (NaN = max 5 en paralelo) y deja margen (usa 4). Comparte el pool de conexiones en vez de fragmentarlo por fuente. Si un cron lanza sub-agentes en paralelo, los lanza SECUENCIALMENTE para no sobrepasar el límite.

### 6. Honestidad radical sobre "testeado vs no testeado"
Marca macOS como "implemented, not yet tested", admite que los números del benchmark vienen de audio SINTETIZADO, y que las instrucciones de BlackHole no se validaron en una máquina.

**Cómo aplicarlo:** normaliza decir qué se ha probado y qué no, y de dónde salen las cifras. Evita demos alucinados y builds que parecen más sólidos de lo que son.

## Pitfalls

- Confundir "degradar" con "fallar silenciosamente": la degradación debe avisar (un WARN) y quedar registrada en `meta.json` con el `mode` usado, como hace el repo.
- Fragmentar pools por fuente "por claridad" → un recurso espera a otro. Comparte el pool.
- `.format()` en prompts con llaves JSON → KeyError. Usar `.replace('{var}', ...)`.
- Poner el tope en el límite exacto de la API (5 de 5) → 429. Dejar margen.
- Chunking: mantener chunks por SILENCIO (VAD), no solo por límite de tamaño; cortar por silencio confina el daño en la detección de idioma por request.

## Verification

- El pipeline degrada y lo registra (meta/mode), no revienta.
- El test de invariante pasa (hosts permitidos, etc.).
- Contrato de salida estable, modelo intercambiable.
