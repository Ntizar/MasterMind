# Time — Plataforma, no proyecto

> Análisis del proyecto Time y su potencial como producto flagship de Kaizen. Sesión 2026-07-12.

## Situación actual

Time es un **producto completo**, no un prototipo. Tiene:

### Capas técnicas
- **Mapa IGN** con 4 capas (gris, topo, orto, CARTO)
- **GTFS real** de 161 datasets (NAP API) + subida ZIP directa
- **GBFS** con 74 redes de bicis en tiempo real (CityBikes API)
- **Isocronas reales** por calle (ORS walking/cycling/driving + GTFS BFS para bus/metro)
- **Datos demográficos** INE (población, salarios, vivienda por CP)

### Capas de análisis
- **Informe DOCX** de 15 secciones con interpretaciones automáticas
- **Export CSV/GeoJSON/SHP/KML** + ZIP batch
- **Escenarios teletrabajo** (5d, 3+2, 2+3, full remote)
- **Impacto CO₂** (IPCC AR6)
- **Ranking de CPs** con score compuesto (accesibilidad + coste)
- **Rutas recomendadas** con horarios por modo

### Capa de diseño
- **Kaizen Design System** — corporativo flat, azul #1A4488 + rojo #CB1823
- Sidebar 380px fijo, KPIs tiles, chips filtros, loading states
- Sin gradientes, sin glass, sin sombras pesadas

## El problema de posicionamiento

> *"Time es una herramienta que hace planes de movilidad"*

vs.

> *"Time es la plataforma de análisis de movilidad laboral más completa de España"*

La diferencia es TODO.

## Oportunidades de mercado

### 1. Planes de Movilidad al Trabajo (PMT) — OBLIGATORIOS por ley

Desde 2023, empresas con **+500 empleados** en España deben tener PMT.
- Consultoras: 3-6 meses, 50.000-200.000€
- Time: semanas, coste marginal
- **Time hace TODO lo que necesita un PMT**

### 2. Estudios de impacto de movilidad

Cuando Ineco hace estudio de nueva línea de metro, AVE, cambio de red de bus:
- Isocronas antes/después
- Análisis de accesibilidad
- Impacto demográfico
- Emisiones CO₂
- **Time hace todo en horas, no en semanas**

### 3. Planes de sostenibilidad urbana

Ayuntamientos necesitan:
- Cobertura de transporte público
- Isocronas de accesibilidad
- Emisiones por modo
- Escenarios de teletrabajo
- **Time tiene TODO**

## La propuesta

> *"Time no es un proyecto más. Es la plataforma que vamos a usar para TODOS los estudios de movilidad de Ineco. En vez de construir cada vez desde cero, tenemos un motor que ya hace el 80% del trabajo. Los otros 20% son los datos específicos del estudio."*

## Plan de 3 movimientos

### 1. El PMT demo
Elige UN departamento que esté trabajando en un PMT AHORA.
> *"Dejadme que haga el análisis completo con Time. Sin compromiso. Si os gusta, lo usamos. Si no, no pasa nada."*

### 2. Time como plataforma
Cada vez que uses Time, reutiliza los motores:
- Motor GTFS → cualquier estudio de transporte
- Motor de isocronas → cualquier análisis de accesibilidad
- Motor de informes → cualquier documento técnico
- Datos demográficos → cualquier estudio

**Time no es un producto. Es un framework.**

### 3. El whitepaper de Time
Escribe un documento técnico (no comercial) que explique:
- Qué es Time
- Qué datos usa
- Qué capacidades tiene
- Cómo se compara con métodos tradicionales
- Cuánto tiempo/coste ahorra

**No lo vendas. Compártelo.** Que lo lean los técnicos y digan "joder, esto es lo que necesitábamos".

## Estado del código

- **Repo:** `/root/workspace/Time/`
- **PLAN-TIME.md:** 542 líneas, fases 0-7 documentadas
- **Fases completadas:** 0-2 (renombrar, Kaizen CSS, mapa IGN)
- **Fases pendientes:** 3-7 (GTFS/GBFS, isocronas, informes, renta CP, estructura final)
- **Server:** `server.mjs` (53KB, Node.js con proxies)
- **Frontend:** `index.html` (7.3KB) + `js/` + `css/`

## Lección clave

> Time tiene todo lo que necesita para ser el estándar de los planes de movilidad en España. Pero está empaquetado como "una herramienta más de Kaizen". El problema no es técnico. Es posicionamiento.

*Hecho con ❤️ por David Antizar*