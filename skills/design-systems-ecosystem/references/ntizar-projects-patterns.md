# Patrones de Proyectos Ntizar con Aurora

> **Fecha:** 2026-05-29
> **Fuente:** Exploración autónoma de repos GitHub del usuario Ntizar

## Proyectos Propios que Usan Aurora

### 1. solmad (⭐3) — Buscador de Terrazas con Sol en Madrid
- **Stack:** Vite + React + TypeScript + Leaflet + SunCalc + Web Workers + Comlink + Three.js + Zustand + Tailwind
- **Patrón clave:** Web Workers + Comlink para cálculos de sombras solares sin bloquear UI
- **Datos:** Censo oficial de terrazas Madrid + OSM + SunCalc
- **Deploy:** Vercel (solmad.vercel.app)
- **Lección:** Para cálculos intensivos en navegador, usar Web Workers con Comlink es el patrón correcto

### 2. XVLegislatura — Atlas Orgánico del Gobierno de España
- **Stack:** D3.js v7 + Ntizar CSS + HTML/CSS/JS vanilla
- **Datos:** RD 1009/2023, BOE, 22 ministerios, 300+ órganos
- **Visualización:** Mapa radial D3.js, organigramas expandibles, buscador instantáneo
- **Deploy:** GitHub Pages
- **Lección:** Para visualizaciones complejas con datos públicos, D3.js + vanilla es suficiente

### 3. nap-dashboard (⭐1) — Transporte Público de España
- **Stack:** React + Vite + TypeScript + GTFS
- **Feature estrella:** Selector de semana en GTFS Viewer con lógica completa del estándar GTFS
- **Datos:** Ministerio de Transportes España, 2.594 operadores
- **Lección:** Lógica de negocio compleja (GTFS weekday logic) en frontend es viable

### 4. FreeHands (⭐0) — Control sin manos
- **Stack:** Python 3.11+, webcam, Windows first
- **Tecnologías:** Gaze tracking, gesture recognition, voice commands
- **Seguridad:** Kill switch con palma abierta derecha (2 segundos)
- **Web:** Duck test en GitHub Pages (no abre cámara)
- **Lección:** Herramientas de accesibilidad pueden ser locales sin cloud

### 5. FamilyTree (⭐0) — Editor de Árbol Genealógico
- **Stack:** HTML/CSS/JS vanilla + Ntizar Aurora
- **Export:** JSON + Excel
- **Deploy:** GitHub Pages
- **Lección:** Para apps de datos relacionales simples, vanilla + JSON export es suficiente

### 6. empleady (⭐0) — Simulador de Rentabilidad de Empleados
- **Stack:** HTML/CSS/JS vanilla + Ntizar Aurora
- **Funcionalidad:** Dashboard interactivo de curva de aprendizaje y break-even
- **Deploy:** GitHub Pages
- **Lección:** Calculadoras financieras interactivas funcionan bien en vanilla JS

### 7. Ntizar-Aurora — Sistema de Diseño CSS (⭐)
- **Stack:** CSS-only, 11 packs + next, ~170KB total
- **Arquitectura:** Namespace `.nz`, stateless packs, 6 skins, multi-axis theming
- **Mejora continua:** Pipeline nocturno automático (Aurora Nightly) — 4 jobs diarios que investigan, analizan y mejoran el CSS
- **CDN:** jsDelivr público
- **Deploy:** GitHub Pages (via CDN)
- **Lección:** Un sistema de diseño CSS modular y bien documentado puede servir como base para TODOS los proyectos Ntizar

## Patrón Común: Vanilla First

Ntizar usa una regla implícita de decisión:
- **Proyectos simples** → HTML/CSS/JS vanilla (FamilyTree, XVLegislatura, empleady)
- **Proyectos complejos** → Vite + React + TypeScript (solmad, nap-dashboard)
- **NUNCA Angular/Vue** — preferencia clara por React o vanilla

## Patrón Común: GitHub Pages Deploy

Todos los proyectos estáticos se deployan en GitHub Pages:
- Sin build step en el deploy
- Sin servidor backend
- Sin tokens de API en frontend (datos públicos)

## Patrón Común: Datos Públicos Españoles

Fuentes de datos recurrentes:
- **BOE** — Gobierno de España (XVLegislatura)
- **Ministerio de Transportes** — GTFS (nap-dashboard)
- **Ayuntamiento de Madrid** — Terrazas (solmad)
- **Bicimad API** — Estaciones de bicis
- **ESIOS/REE** — Mercado eléctrico

## Lección Clave: Web Workers + Comlink

Solmad usa este patrón para cálculos de sombras solares:
```javascript
// Worker hace los cálculos pesados
// Comlink expone funciones del worker al main thread
// UI nunca se bloquea
import { wrap, unwrap } from 'comlink';
const worker = new Worker('./shadow-calculator.js');
const calc = wrap(worker);
const result = await calc.computeSunPosition(lat, lng, date);
```
