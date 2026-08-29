# Frontend del visor — diseño validado con David (era-visor, 2026-08-28)

## La petición del slider de años, decodificada

Evolución de la petición y qué significaba realmente:
1. "el rango de años es feo" → dos sliders separados "Año desde"/"Año hasta" NO.
2. "cambia lo de la etiqueta de años y que sea solamente una barra" → UNA barra,
   pero con **DOS puntos (tiradores)**: "lo de alos años tiene que tener dos puntos
   en vez de uno". Barra única + dual-handle.

Implementación validada (CSS puro, sin librerías):
- Contenedor `.dual-range` (position:relative, height ~20-22px) con:
  `.dual-track` (barra gris #e5e7eb), `.dual-fill` (azul #2563eb entre pulgars),
  y dos `input[type=range]` absolutos superpuestos, transparentes y con
  `pointer-events:none` en el input y `pointer-events:auto` solo en el thumb.
- JS: en `oninput` de cualquiera de los dos, `lo=min(v1,v2)`, `hi=max(v1,v2)`,
  fill con `left=(lo-amin)/span*100%` y `right=(amax-hi)/span*100%`; label
  "todos" cuando cubre el rango completo.
- Filtro: `a1=min`, `a2=max` (por si el usuario cruza los tiradores).

## Sistema de diseño aceptado

- Tokens: `--primario:#2563eb`, `--rojo:#dc2626`, `--ambar:#d97706`,
  `--verde:#059669`, `--bg:#f6f7f9`, `--card:#fff`, `--borde:#e5e7eb`,
  texto `#111827/#4b5563/#9ca3af`, sombras `0 1px 2px + 0 1px 3px rgba(16,24,40,.05/.06)`,
  hover `translateY(-2px)` + sombra mayor, radio 8px.
- Header BLANCO con borde inferior (no gradiente). Tabs subrayado activo.
- KPIs: tarjeta blanca con borde, valor grande color según métrica. Sin border-left.
- Tabla: th gris claro uppercase sticky, hover de fila azul muy suave.
- Panel detalle: header blanco con borde (no azul sólido), botón cerrar gris que
  se enrojece en hover.
- Charts (Chart.js): unificar con la paleta — escala azul #1e40af/#3b82f6/#60a5fa/
  #93c5fd + rojo #dc2626 + ámbar #d97706. NO mezclar con azules de otro sistema
  (#1A4488, #3463AC, #6B96CF).

## Checklist de validación (sin navegador del usuario)

```bash
node -e "const html=require('fs').readFileSync('index.html','utf8');
const s=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
s.forEach((x,i)=>{try{new Function(x);console.log('script '+i+' OK')}
catch(e){console.log('script '+i+' ERROR: '+e.message)}});"
```
1. Sintaxis de todos los scripts inline.
2. Cada id usado por el JS existe en el HTML (sliders, filtros nuevos).
3. Tras reemplazar el `<style>` completo, `grep kz-` y colores hex viejos: los
   estilos inline del body (`style="color:var(--kz-azul)"`) sobreviven al
   reemplazo y quedan rotos si no se grepean.
4. curl al servidor local para confirmar 200.
5. Reemplazo de bloque `<style>` entero con Python (`html[:i0]+nuevo+html[i1:]`)
   es más fiable que N parches cuando el rediseño es grande.
