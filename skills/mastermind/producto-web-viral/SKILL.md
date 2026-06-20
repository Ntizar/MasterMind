---
name: producto-web-viral
version: "1.0.0"
description: Patrón para crear productos web virales — conceptos absurdos que escalean, mecánicas de juego, pagos, legal EU, Three.js. Lo que todo el mundo necesita y paga 1€/semana.
tags: [viral, web, threejs, pagos, juego, viralidad, producto]
triggers: [producto viral, web viral, chorrada, idea viral, pixel website, mecánica de juego, sorteo, sweepstakes, pagos web]
---

# Producto Web Viral

Patrón para construir productos web con potencial viral: conceptos simples, mecánicas adictivas, pagos de bajo coste, y legal EU compliant.

## Filosofía

David lo resumió: **"Quiero algo que no exists aún. Una chorrada como lo del chico que vendía 1 pixel a 1€"**.

Lo que funciona:
- **Concepto de 2 segundos** — lo entiendes y te ríes
- **Urgencia visual** — ves algo desapareciendo o creciendo
- **Progreso colectivo** — cada acción afecta a todos
- **Precio tan bajo que no piensas** — 1€, 5€, 10€
- **Compartibilidad** — la gente lo cuenta porque es gracioso

Lo que NO funciona:
- Negocios "serios" con modelo de negocio complejo
- Nichos demasiado específicos
- Productos que resuelven problemas que la gente no sabe que tiene

## Flujo de construcción

### 1. Concepto (la chorrada)
- Idea absurda pero con mecánica real
- Debe caber en una frase: "Cada € = 1 grano de arena. La última gota gana"
- Test: ¿se lo contarías a un amigo en un bar?

### 2. Mecánica de juego
- Dos fases si hay temporalidad (antes/después de un evento)
- Recompensa clara = % del bote
- Determinismo verificable (SHA-256) para transparencia
- Giro/Spinner como elemento de engagement

### 3. Stack rápido
- **Frontend:** Three.js (si hay 3D) + HTML vanilla + CSS
- **Backend:** Node.js + Express + SQLite (escalar a Postgres)
- **Pagos:** PayPal Checkout (bajo fricción, QR incluido)
- **Real-time:** WebSocket para updates en vivo
- **Deploy:** GitHub Pages (estático) → NaN.builders (con backend)

### 4. Legal EU (sweepstakes, NO gambling)
- Es "promoción participativa", no apuesta
- Donación voluntaria + posibilidad de premio
- 18+ UE/EEE
- Hash verificable público
- Ver references/legal-template-eu.md

### 5. Design
- Estilo elegante (mármol griego, serif, dorado)
- Responsive SIEMPRE (mobile-first)
- QR de pago visible
- Footer: "Hecho con ❤️ por David Antizar"

## Three.js — Patrones reutilizables

Ver references/threejs-hourglass-patterns.md para:
- LatheGeometry para formas suaves
- Instanced particles (BufferGeometry + PointsMaterial)
- Materiales procedural (marble, gold)
- Oscilación + parallax con ratón
- Animaciones de spin con easing

## Pitfalls

- **NO hardcodear hex en CSS** — usar variables CSS
- **NO hacer el repo privado si quieres GitHub Pages gratis**
- **NO olvidar responsive** — probar en 380px, 640px, 900px
- **NO usar const en charts/animaciones globales** — usar var (window scope)
- **Three.js r128 NO soporta** `thickness` en MeshPhysicalMaterial
- **GitHub Pages tiene CDN cache** — usar query param `?v=N` para forzar refresh
- **PayPal QR** — incluir imagen + enlace directo, no solo botón
- **Legal** — siempre咨询ar abogado para texto final. El template es base, no definitivo
