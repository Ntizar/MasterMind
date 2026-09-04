---
name: data-claims-audit
description: "Use al auditar cifras que pregona una web."
version: 1.0.0
---

# Auditoría de veracidad de datos (data-claims audit)

Clase de tarea: el usuario enlaza un sitio (normalmente una data-viz de una sola página con datos embebidos en JS, a veces un sitio multi-archivo) y pide "ver la realidad de los números" — ¿son ciertos, de dónde salen, qué esconden? Trigger ampliado: cualquier web que afirme totales ("X casos suman Y €", "N millones en…") que deban contrastarse con su fuente declarada.

**Principio rector:** fidelidad a la fuente ≠ veracidad. Un sitio puede copiar perfectísimamente una fuente que mezcla cifras probadas, estimaciones y titulares de prensa bajo un mismo símbolo €. La auditoría tiene 4 capas independientes y hay que reportarlas separadas.

## Procedimiento

1. **Copia local + localización de la fuente.** `curl -sL -A "Mozilla/5.0 ..."` el `index.html`; `grep -oE '(src|href)="[^"]+"'` para ver qué fuente cita; localizar los arrays embebidos (`const SEED`, diccionarios de categorías, listas de excluidos). Para auditoría de texto puro, curl+regex > browser tools (browser_exec puede quedarse bloqueado esperando aprobación de remote-debugging de Chrome).
2. **Integridad de la copia.** Extraer el array con regex en Python (`open()`, nunca sobre output de `read_file` — tiene prefijos `N|`). Verificar count y SUMA EXACTA contra lo que afirman header/footer/texto de tweet.
3. **Re-bajar la fuente declarada y diff caso a caso.** Parsear bloques por registro, normalizar claves, y computar: discrepancias de importe, de categoría, inexistentes en un lado u otro.
4. **Desglose del titular.** Separar el total en capas: (a) macro-cifras que la propia web excluye por defecto vía toggles, (b) entidades que no son la categoría protagonista del gráfico, (c) lo que realmente se ve por defecto. Calcular % de cada capa. Preguntar SIEMPRE: ¿el texto precargado para compartir usa el total gordo o la vista por defecto?
5. **Spot-check externo de los 3-5 números que dominan la visualización** con `web_search` contra fuentes primarias (sentencias, organismo oficial, prensa). Clasificar cada importe: probado en sentencia / estimado por juez / volumen de negocio / cifra de otra cosa (p.ej. importe *declarado* en una amnistía fiscal, no defraudado).
6. **Informe en 4 capas** (tabla + veredicto): ① integridad técnica de la copia, ② fidelidad del claim del header, ③ realidad del titular (desglose %), ④ calidad de la fuente madre.

## Pitfalls

- **🔴 Falso "0 coincidencias" por doble prefijo.** Si la fuente genera títulos tipo `CASO X` y el visor los normaliza a `Caso Caso X`, el match crudo da 0 comunes y parece "389 casos inventados". Normalizar siempre: `re.sub(r'^caso\s+', 'Caso ', raw, flags=re.I)` y matchear por `.lower()`. Un "0 comunes" total es casi siempre bug de matching — sospechar antes de reportar.
- **🔴 Prints masivos** (listas de 389 nombres inundan el contexto): slicear `[:25]` en todo script de auditoría.
- Toggles que suman en vez de filtrar: señalar si activar una opción revela categorías ajenas al mensaje (bancos/cajas/empresas en un gráfico "por partido").
- El reparto que ve el usuario (vista por defecto) puede diferir radicalmente del reparto del total reclamado — calcular ambos y compararlos.
- `web_search` puede fallar según backend configurado → fallback: reformular consulta o `web_extract` de una URL conocida.

## Referencias

- `references/corrupcion-netlify-2026-09.md` — caso completo ejecutado: extracción del SEED, diff contra `tramas.php` de casos-aislados.com (591 casos / 389 con importe / 124.235.185.826 € exactos), desglose del titular (78,7 % macro-cifras excluidas por defecto; solo 15,1 % casos por partido visibles), spot-checks (Gürtel ✔, rescate bancario ✔, amnistía fiscal ✗ como "coste"), scripts Python concretos de cada paso.
