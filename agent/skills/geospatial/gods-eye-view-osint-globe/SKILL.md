---
name: gods-eye-view-osint-globe
version: "1.0.0"
description: "Globo OSINT en navegador: aviones, barcos y cámaras en vivo."
tags: [osint, 3d-globe, realtime, browser, satellite, cams]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [osint, 3d-globe, realtime, browser]
    related_skills: [osint-live-globe, threejs-3d-maps, cctv-yolo]
---
# God's Eye View — Globo 3D OSINT

## Resumen
Sitio de "espionaje" con *data pública real*: globo 3D fotorrealista con aviones, barcos, satélites, terremotos, tráfico y cámaras públicas en tiempo real. Control por voz (agente IA en tiempo real). Sin claves/signup/config inicial: las claves son "power-ups" opcionales pegados después. Tráfico simulado sobre carreteras reales con datos agregados de localización; poses de CCTV y trayectorias de lanzamiento son estimaciones aproximadas.

## Uso (comandos reales del README)
```bash
# Instalación y arranque
npm install
npm run dev
```
- Las claves de API son "power-ups" que se pegan en la app más tarde.
- También instalable en un clic vía Pinokio (pinokio.computer).

## Patrones / Arquitectura
- **Vista de cockpit**: viaja dentro de un vuelo rastreado; la cámara sujeta el terreno bajo ti.
- **Contactos**: roster de 250 km con todo lo cercano al objetivo — avanza entre aviones y salta a cualquier cockpit.
- **Click-to-track**: la cámara se bloquea, dibuja estela progresiva y muestra metadata completa; un incendio o buque enlaza con la cámara en vivo más cercana.
- **Pizarra por voz**: anota sobre el mundo con polígonos, marcas y rutas reales.
- **Hangar 3D**: modelos reales por clase (787, ATR-72, etc.).

## Pitfalls
- Muchos feeds son en vivo o refrescados con regularidad; tráfico y trayectorias de cohetes son estimaciones.
- Los datos son señal pública (transponders, balizas de barcos, elementos orbitales, sismógrafos, cámaras públicas). Aunque parezca cockpit "prohibido", todo es inspeccionable.

## Verificación
- `npm run dev` sirve el globo en el navegador; confirmar capas en vivo (aviones/barcos/cámaras) cargando.

## Referencia
- Repo: https://github.com/bilawalsidhu/gods-eye-view (antes "WorldView"). Proyecto de la serie viral God's Eye View (Billal Sidhu).
