[regla-critical] NUNCA crear repos sin verificar primero si existen. SIEMPRE intentar git clone primero, si falla → crear. Nombres sensibles a una letra.
§
[proyecto-nogal9] Repositorio privado Ntizar/nogal9. Presupuesto referencia: 523.705€ (CYPE PEM, 27 capítulos). JSON en presupuesto_referencia.json. Para comparar futuras ofertas de constructoras.
§
[proyecto-nogal9] Repos Ntizar/nogal9 (privado). GLAM: 1.218.453€ (28 capítulos), Trevicon: 1.098.001€. HTML: ntizar.github.io/nogal9-web.
§
[aurora-liquid-glass] "Aurora limpio" estilo iOS 26: fondo blanco #ffffff, glass REAL con 4 capas (base translúcida rgba 255,255,255,0.72→0.62 + backdrop-filter blur(24px) saturate(180%) + dual inset shadow + borde cromático ::before specular + ::after chromatic edge). Números compactos KPIs 1.125–1.25rem. Mobile-first: base 1 col ≤600px, tablet 2 col 601–900px, desktop 3+ col ≥901px. Touch targets 44px mínimo. Sin gradientes radiales intrusivos, sin orbs flotantes, sin mesh aurora intrusivo. Colores: azul #2563eb + naranja #f97316. Sin violeta/morado.
§
[proyecto-timeineco] Repo Ntizar/TimeIneco (privado). Original, completo. server.mjs 941 líneas. JS v0.9. Último commit 1f48d81 (22/06): fixes CSV bug, docx vendor lib, ORS timeout 25s, .env.example. Deploy NaN: https://timeineco-ntizar-ntizar.apps.nan.builders/ . NAP_API_KEY debe configurarse en NaN Dashboard > Env. TimeIneco2 borrado (solo local).
§
[skill-ref] `frontend-dashboard-patterns` reference: `references/cdn-abortcontroller-ux-patterns.md`. CDN MIME (jsdelivr .cjs → application/node, unpkg → text/javascript). AbortController timeout para fetch externos. UI progresivo: paneles antes de cálculo.
§
NAP API (transportes.gob.es) devuelve enlace S3 temporal (900s), no datos directos. POST /api/v2/fichero/{id}/descarga con header ApiKey → JSON con enlaceDescarga → HTTPS GET → ZIP GTFS. Ciudades: Sevilla(1567), Valencia(1568), Zaragoza(1569), Málaga(1570), Bilbao(1571). Endpoint metadata puede dar 404.