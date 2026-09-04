---
name: aemet-llm-report-pipeline
version: "1.0.0"
description: "Pipeline meteorológico AEMET, Python, LLM y Quarto."
tags: [aemet, meteorology, pipeline, llm, ollama, quarto, report]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [aemet, meteorology, pipeline, ollama, quarto]
    related_skills: [esios-telegram-report, static-digest-pipeline, document-conversion, html-to-pdf-report-pipeline]
---
# Pipeline Meteorológico AEMET + LLM + Quarto

## Resumen
Pipeline automatizado de análisis meteorológico: descarga datos de la **API de AEMET**, los procesa con Python y compara el **histórico (últimos 50 años)** vs el **mes actual**. Genera un resumen con un **LLM local** (Ollama) y un informe final en HTML/PDF usando **Quarto**. Se centra en un único mes (elegido por el usuario) y una única estación (por defecto Sevilla, idema **5783**).

## Requisitos
- Python 3.9+ y Quarto.
- Acceso a la API de AEMET (requiere token).
- Ollama instalado y en ejecución, con el modelo `llama3.1:8b` descargado.
- Librerías Python:
```bash
pip install python-dotenv requests pandas matplotlib
```
- Hardware: CPU Intel i5/i7 + 32 GB RAM; no se necesita GPU NVIDIA (el LLM puede correr en CPU, aunque más lento).

## Configuración del token
- El script tiene una línea `TOKEN = "INSERTE TOKEN AQUI"` — sustituir por el token personal.
- **Opción recomendada**: crear un archivo `.env` con `TOKEN_AEMET=tu_token_aqui` y cargarlo con `python-dotenv`, para no exponer el token en el repo.

## Ejecución
El script solicita por consola:
- **Mes (1-12)**
- **ID de estación (opcional, por defecto 5783)**

Si no se introduce estación, usa automáticamente la de Sevilla. Al introducir los datos el proceso se ejecuta completo.

## Patrones / Arquitectura
El flujo completo:
1. Descarga datos históricos (50 años) y actuales desde la API de AEMET.
2. Calcula estadísticas diarias (media, mínimo y máximo) separando histórico vs año actual.
3. Genera un prompt estructurado para un LLM local.
4. Obtiene el resumen en lenguaje natural del comportamiento del mes.
5. Genera gráficos comparativos.
6. Construye un informe en formato Quarto (pdf o html) y lo renderiza automáticamente.

Resultado final: datos en CSV, resumen en Markdown, gráficos en PNG e informe final PDF/HTML.

## Estructura de salida
Al finalizar la ejecución se generan: `datos.csv` (datos procesados), `resumen_llm.md` (texto del modelo), `scatter.png`, `tmax.png`, `tmin.png` (gráficos), `reporte.qmd` (plantilla del informe) y el informe renderizado por Quarto (`.html` o `.pdf`).

## Pitfalls
- El tiempo total depende principalmente del modelo LLM; al no requerir GPU, tarda ~5 minutos en ejecutarse.
- Si se usa otro modelo local, hay que modificar el nombre del modelo en el código.
- El token de AEMET no debe ir en el repo (usar `.env`).

## Verificación
- Ejecutar con mes y estación, confirmar `datos.csv`, `resumen_llm.md`, los PNG y el informe Quarto renderizado.

## Referencia
- Repo: https://github.com/fenris123/Analisis-de-Datos-Meteorologicos-Automatizado-API-LLM-Quarto
