# Caso Kit72h — decisiones y datos concretos (agosto 2026)

## Origen
El usuario vio un tuit viral (Argona, "Grok Bot / Mogul", ~27M views) proponiendo bots que construyen sitios directorio y negocian afiliaciones solos. Evaluación honesta: el pitch es engagement bait (venden un PDF); el SEO de nichos nuevos en 2026 está roto para contenido AI masivo (Core Updates marzo y mayo 2026 desindexan plantillas sin datos únicos; AI Overviews cortan CTR ~58%). Lo real: patrón de publicación autónoma + nicho con utilidad real + monetización sin negociar (programas de afiliación existentes).

## Elección del nicho (entre 5 propuestas: comparador técnico, kits de compra, pSEO geográfico, viajes, kits de emergencia)
Ganó **kits de emergencia 72h** porque: fuente de verdad oficial (UE + Protección Civil), alta conversión (ticket <50€, decisión rápida), estacionalidad real (DANAs, apagón abril 2025, ola de calor), baja competencia seria en castellano. Monetización elegida: solo Amazon Afiliados al inicio. Automatización: cron nocturno + informe Telegram.

## Nombre
"KitsEmergencia.es" ya existía como web → proceso: bucle `nslookup -type=NS` sobre ~30 candidatos. Ganó **kit72h.es** (DNS libre, verificado en registrador pendiente de compra por el usuario). Alternativas libres que quedaron en la mesa: kitdeemergencia.es, kitseguro.es, kitdeurgencia.es, kitde72horas.es, kitparatodo.es. Ocupados: kitemergencia.es, kitlisto.es, listo.es, kitsupervivencia.es, kit72horas.es, kitdeemergencias.es, mislistas.es.

## Fuentes oficiales citadas en el contenido
- UE: Estrategia de Preparación (marzo 2025), Comunicación JOIN(2025) 90 — "bolsa de resiliencia", autonomía 72h. Es RECOMENDACIÓN, no obligación (verificado vía maldita.es para evitar el bulo).
- España: proteccioncivil.es/gestion-riesgos/recomendaciones (páginas por riesgo: lluvias-intensas, altas-temperaturas...). El contenido textual se saca mejor con curl + grep de p/li/h2/h3; la página de índice lista títulos duplicados sin enlaces útiles.
- Contexto apagón: apagón ibérico del 28 de abril de 2025 (sin luz 12h+ en la península) — motivo del kit apagón.

## Datos del sitio v1
- 8 kits: kit-basico-72h, dana, apagon, coche, hogar, montana, calor, evacuacion
- 85 productos, todos con descripcion + precio_aprox (rango € orientativo) + prioridad (esencial/recomendado/extra)
- Enriquecimiento masivo: dict Python keyword→(descripcion, precio, prioridad) con match por substring sobre el nombre del producto; 4 faltantes retocados a mano con dict exacto por nombre.
- Enlaces afiliado: placeholders `AMAZON-URL-<NOMBRE>` — David pasará los enlaces reales cuando aprueben su cuenta de Amazon Afiliados (exigen sitio con contenido ya publicado: cumplido).
- Diseño Mad Max: canvas Three.js fijo (dunas wireframe cobre x2, sol sprite radial, 700 partículas polvo, 12 chatarras girando, cámara con seno), overlay grano SVG feTurbulence + manchas radial-gradient, tipografías Rubik Dirt + Barlow Condensed, print limpia en blanco y negro.

## Infra
- Repo: Ntizar/Kit72h (local ~/Projects/kit72h). Páginas workflow moderno deploy-pages@v4. URL: https://ntizar.github.io/Kit72h/
- Cron `kit72h-vigilante` (job e518c0973b6a, 0 3 * * *, deliver telegram): revisa fuentes, actualiza data/kits.json (nunca borrar kits, citar fuente+fecha), push, informe.
- Pendiente usuario: comprar kit72h.es y pasar enlaces afiliado reales.
