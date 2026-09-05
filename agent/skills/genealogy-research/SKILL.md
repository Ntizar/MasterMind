---
name: genealogy-research
description: Usa al investigar genealogía de familias españolas o vascas.
version: 1.0.0
author: Mastermind
license: CC BY 4.0
tags: [genealogia, apellidos, espana, euskadi, archivos, esquelas]
related_skills: [blocked-page-recovery, google-workspace]
---

# Investigación genealógica (España / País Vasco)

## Cuándo usar
- Pedir el árbol/linaje de una familia o apellido español o vasco.
- Buscar el origen, distribución o heráldica de un apellido.
- Reconstruir la conexión entre ramas de una misma familia.

## Convenciones de apellidos españoles (clave)
- Apellido compuesto = **paterno + materno**. Ej: `Antizar-Fernández` = padre Antizar, madre Fernández; `Antizar-Ladislao` = padre Antizar, madre Ladislao.
- Esto permite conectar ramas: si un antepasado de apellido A casó con una mujer de apellido B, sus hijos llevan `A-B`.
- Los apellidos vascos suelen ser toponímicos (caseríos) y terminan en -endi, -ar, -a, -aga (ej: Otamendi, de Gipuzkoa/Bizkaia, vinculado a ferrerías).

## Cómo anclar el árbol (empezar por lo moderno y verificado)
1. **Esquelas/obituarios** en prensa regional: El Diario Montañés (Cantabria), Deia (País Vasco), esquelasdecantabria.com. Dan el núcleo familiar (esposo/a, hijos, nietos) y la localidad.
2. **LinkedIn / perfiles públicos**: para identificar portadores vivos del apellido y su zona.
3. **Listas de candidaturas municipales** (BOC/BOP, vLex): los apellidos raros aparecen en elecciones locales.
4. **Bases de datos de la Guerra Civil** para antepasados: euskalmemoria.eus (fichas por id), intxorta.org (víctimas del franquismo), combatientes.es, Centro Documental de la Memoria Histórica.
5. **Datos del apellido** (frecuencia, heráldica): historiaapellidos.com, wikiapellidos.com, apellidos.net, coatofarmsof.com.

## Archivos/registros que contienen el linaje (dónde buscar el pasado)
- **AHEB-BEHA** (Archivo Histórico Eclesiástico de Bizkaia, Derio): 2,28 M de partidas sacramentales (bautismo/matrimonio/defunción) de las parroquias de **Bizkaia**, 1501-2019. Buscador online `internet.aheb-beha.org`.
- **Archivo Diocesano de Santander**: parroquias de Cantabria.
- **Archivo Histórico Provincial de Cantabria**: padrones (Padrón/Censo de 1824, Catastro del Marqués de la Ensenada).
- **Registro Civil** (desde 1871): actas de nacimiento/matrimonio/defunción.
- **FamilySearch**: registros parroquiales de España (Vizcaya, Santander, etc.). **Requiere cuenta gratuita.**
- **Geneanet**: árboles y archivos de usuarios. **Requiere cuenta.**
- **MyHeritage / Ancestry**: de pago.
- **ASCAGEN** (Asociación Cántabra de Genealogía): publicaciones y proyectos sobre genealogía cántabra.

## Técnica técnica
- Los buscadores de estos archivos cargan los datos con **JavaScript** y a menudo están protegidos (Incapsula/WAF). `curl` suele fallar o devolver una página vacía (o un challenge JS).
- Usa un navegador headless con **Playwright** para renderizar y extraer:
  ```
  python3.12 -m pip install playwright
  python3.12 -m playwright install chromium
  ```
  luego `playwright.chromium.launch(headless=True, args=["--no-sandbox"])`; setea `locale="es-ES"` (no hay parámetro `accept_language` en `new_context`).
- Muchos archivos piden **login** para ver el registro completo; a veces la búsqueda misma está detrás de cuenta. Si es así, pide credenciales al usuario o indícale la consulta manual.

## Reglas
- **NO fabricar genealogía.** Cada individuo citado debe tener fuente; marca como **hipótesis** los enlaces entre ramas no confirmados.
- La rareza del apellido NO implica que los registros estén indexados en la web pública — los registros parroquiales viven en los archivos del apartado anterior.

## Referencias
- `references/antizar-cantabria.md`: caso Antizar (Cantabria/Bizkaia) — ramas verificadas y fuentes.
