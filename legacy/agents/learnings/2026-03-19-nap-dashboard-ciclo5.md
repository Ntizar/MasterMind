---
fecha: 2026-03-19
tarea: nap-dashboard-ciclo5
tipo: software
complejidad: alta
clusters: [arquitectura-software]
proyecto: nap-dashboard
patron: api-proxy-with-client-key
---

# NAP Dashboard — ciclo 5: API Key Modal + GTFS Viewer v1

## Decisión clave
CORS bloquea toda llamada directa al NAP API desde el browser.
La solución obligatoria es un proxy server-side en Vercel Functions (`api/nap/proxy.ts`).
La API key nunca va al repo: vive en `localStorage` en el cliente y viaja
como header `X-Api-Key` al proxy, que la reenvía como `ApiKey` al NAP.

## Patrón reutilizable
sí → **api-proxy-with-client-key**
Cuando una API pública tiene CORS bloqueado y requiere API key:
1. Proxy Vercel Function recibe la key como header del cliente
2. Proxy reenvía al destino con el header correcto del proveedor
3. Cliente almacena la key en `localStorage` — nunca en código ni `.env` del repo
4. Un modal bloqueante (ApiKeyModal) fuerza el flujo antes de cualquier llamada

## Qué funcionó
- `ApiKeyContext` con `localStorage` — persistencia sin fricción en siguientes sesiones
- Modal bloqueante como gate de entrada — el usuario no puede saltárselo
- Proxy Vercel unificado para todos los endpoints NAP — un solo archivo mantiene
  la lógica de transformación de headers

## Qué evitar
- No asumir que el proxy siempre devuelve JSON — el endpoint `downloadLink`
  devuelve texto plano; el proxy debe detectarlo y responder con `Content-Type: text/plain`
- No leer `.json()` en el cliente sin verificar el Content-Type de respuesta

## Skills usados
- software-dev.md
- dashboard-dev.md

## Tests/criterios que validaron esto
REVIEWER PASS — commit a01cf69 pushed.
Funcionalidad: modal aparece en primera visita, key persiste en reload,
proxy reenvía correctamente headers.

## Dashboard: datos del proyecto
fuente: nap.transportes.gob.es
encoding_encontrado: UTF-8 (GTFS) / JSON (API REST)
problema_principal: CORS bloqueado en NAP API
solucion_aplicada: Vercel proxy server-side + localStorage API key gate
tipo_artefacto: React SPA + Vercel Functions

## Conexiones
**Cluster:** #arquitectura-software
**Proyecto:** [[nap-dashboard]]
**Aprendizajes relacionados:** [[2026-03-19-nap-dashboard-ciclo6]]
