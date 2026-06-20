# Tab Progreso 3D — InBody con Three.js

## Concepto

Nueva tab "Progreso" en el dashboard MasterFit que muestra un modelo 3D del cuerpo humano que evoluciona según los datos reales de composición corporal del usuario.

## Arquitectura

- **Three.js** para renderizado 3D en el navegador
- **Geometría procedural** — no assets externos, todo generado por código
- **Segmentos escalables** — cada parte del cuerpo (brazos, tronco, piernas) se escala según % grasa y masa muscular
- **Slider antes/después** — compara estado actual con objetivo
- **Datos en tiempo real** — lee de database.json vía API del server

## Modelo 3D — Geometría procedural

Cada segmento del cuerpo se representa con primitivas Three.js escalables:

| Segmento | Geometría | Escala basada en |
|---|---|---|
| Cabeza | Sphere | Peso total (ligero) |
| Tronco superior | Cylinder + Sphere | % grasa + masa muscular |
| Tronco inferior | Cylinder | % grasa + masa muscular |
| Brazo derecho | Cylinder | MME brazo + grasa segmental |
| Brazo izquierdo | Cylinder | MME brazo + grasa segmental |
| Pierna derecha | Cylinder | MME pierna + grasa segmental |
| Pierna izquierda | Cylinder | MME pierna + grasa segmental |

### Escalado de grasa

- **Estado actual:** segmentos escalados según datos reales de InBody
- **Estado objetivo:** segmentos escalados según peso objetivo (78.5 kg)
- **Slider:** interpolación entre ambos estados (0% = actual, 100% = objetivo)
- **Tronco:** se reduce más rápido (donde hay más grasa: 17,5 kg)
- **Piernas:** mantienen volumen muscular (MME al 97.7%)

### Colores

- **Grasa:** tonos naranjas/rojos (#f97316)
- **Músculo:** tonos azules (#2563eb)
- **Hueso:** tonos grises
- **Overlay:** sección transversal mostrando distribución grasa/músculo

## Datos necesarios

```json
{
  "inbody": [
    {
      "peso_kg": 98.1,
      "masa_grasa_kg": 31.4,
      "porcentaje_grasa": 32.0,
      "masa_muscular_esquelética_kg": 38.3,
      "agua_corporal_L": 48.9,
      "proteinas_kg": 13.4,
      "minerales_kg": 4.40,
      "inbody_score": 70,
      "peso_objetivo_kg": 78.5,
      "control_grasa_kg": -19.6,
      "control_muscular_kg": 0.0,
      "grasa_visceral": 14,
      "segmental_fat": {
        "brazo_izq_kg": 2.2,
        "brazo_der_kg": 2.2,
        "pierna_izq_kg": 4.0,
        "pierna_der_kg": 4.1,
        "tronco_kg": 17.5
      },
      "segmental_lean": {
        "brazo_izq_kg": 4.09,
        "brazo_der_kg": 4.11,
        "pierna_izq_kg": 10.08,
        "pierna_der_kg": 10.06,
        "tronco_kg": 31.1
      }
    }
  ]
}
```

## Historial de entrenamientos

### Estructura mejorada

```json
{
  "entrenamientos": [
    {
      "fecha": "2026-06-04",
      "tipo": "fuerza",
      "grupo muscular": "pierna",
      "series": 12,
      "duracion_min": 45,
      "intensidad": "alta",
      "rpe": 9,
      "volumen_total_kg": 5400,
      "notas": "DOMS notable al día siguiente"
    }
  ]
}
```

### Métricas calculadas

- **Días entrenados/semana** — calendario visual con color por tipo
- **Volumen semanal** — suma de (series × peso × reps) por semana
- **Frecuencia por grupo muscular** — cuántas veces/semana se entrena cada grupo
- **Evolución de volumen** — gráfico Chart.js de volumen semanal
- **RPE promedio** — intensidad media semanal

### Calendario visual

- Cuadrícula mensual con días coloreados
- Verde = fuerza, azul = cardio, gris = descanso
- Tooltip al hover mostrando detalles del entreno
- Contador de días entrenados en el mes

## API endpoints necesarios

```javascript
// Obtener datos InBody actuales
GET /api/inbody/current

// Obtener historial InBody
GET /api/inbody/history

// Obtener datos para visualización 3D
GET /api/progress/body-3d

// Obtener historial de entrenamientos
GET /api/progress/training-history

// Métricas de entrenos
GET /api/progress/training-stats
```

## Interacción 3D

- **Rotación:** click + arrastrar para rotar el modelo
- **Zoom:** scroll para zoom in/out
- **Info al hover:** tooltip con datos del segmento al pasar el ratón
- **Slider antes/después:** slider horizontal para interpolar entre estado actual y objetivo
- **Modo corte:** sección transversal del tronco mostrando grasa vs músculo

## Implementación

1. Añadir `<canvas id="body3d"></canvas>` en la tab Progreso
2. Cargar Three.js desde CDN: `https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js`
3. Crear escena con OrbitControls
4. Construir modelo procedural con geometría escalable
5. Conectar con API `/api/progress/body-3d`
6. Añadir slider antes/después
7. Añadir tooltips informativos

## Pitfalls

- **Three.js desde CDN:** usar versión específica (no @latest) para evitar breaking changes
- **OrbitControls:** necesita import separado desde CDN — `three@0.160.0/examples/js/controls/OrbitControls.js`
- **Performance:** no usar más de 5000 triángulos — el modelo procedural es ligero pero hay que evitar overkill
- **Responsive:** el canvas debe redimensionarse con resize observer
- **Mobile:** touch events para rotación/zoom en móvil
- **Datos reales:** NUNCA inventar datos para el modelo — si no hay InBody, mostrar empty state

## Cron de mejora

Para evolucionar esta feature hasta que sea "top":
- Semana 1: modelo básico 3D con segmentos escalables
- Semana 2: slider antes/después + tooltips
- Semana 3: historial de entrenamientos con calendario visual
- Semana 4: modo corte transversal del tronco
- Semana 5: gráficos de evolución de composición corporal
- Semana 6: sistema de auth básico (usuario/contraseña)
- Semana 7: multi-usuario preparado
