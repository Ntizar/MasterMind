# Taxonomía de Severidad y Tipología — Accidentes Ferroviarios (España)

## Marco normativo
- **Directiva (UE) 2016/798** — Seguridad ferroviaria
- **RD 929/2022** — Modifica RD 623/2014 (CIAF)
- **RD 664/2015** — Condiciones de seguridad

## Clasificación de sucesos

### Accidentes ferroviarios
| Criterio | Muy grave | Grave | Menor |
|----------|-----------|-------|-------|
| Fallecidos | ≥1 persona | — | — |
| Lesiones graves | ≥1 persona | ≥1 persona | — |
| Evacuación viajeros | — | Sí | — |
| Daños materiales | Importantes (reparación mayor) | Significativos | Leves |
| Daño infraestructura | Reparación mayor | Significativo | Leve |
| Daño medio ambiente | Grave | Significativo | — |

### Incidentes ferroviarios
| Tipo | Criterio |
|------|----------|
| **Incidente grave** | Alto potencial de riesgo de accidente. Incluye: aproximación indebida, rebase de señal con riesgo, descarrilamiento evitado, colisión evitada |
| **Incidente menor** | Eventos operacionales sin riesgo directo de accidente |

## Tipología de suceso (normalizada para CIAF)

### Accidentes
1. `descarrilamiento` — Descarrilamiento de tren
2. `colision_trenes` — Colisión entre trenes (frontal, lateral, alcance)
3. `colision_vehiculo` — Colisión tren ↔ vehículo de carretera
4. `colision_obstaculo` — Colisión con obstáculos en vía (rocas, barrera, etc.)
5. `arrollamiento_persona` — Arrollamiento de persona/peatón
6. `arrollamiento_vehiculo` — Arrollamiento de vehículo por tren
7. `arrollamiento_ciclista` — Arrollamiento de ciclista/motocicleta
8. `paso_nivel` — Accidente en paso a nivel
9. `incendio` — Incendio de material rodante
10. `rotura_eje` — Rotura de eje en tren
11. `fallo_cargamento` — Fallo de cargamento

### Incidentes
12. `rebase_senal` — Rebase indebido de señal (incluye rebase en rojo)
13. `escape_material` — Escape de material / tren a la deriva
14. `fallo_senalizacion` — Fallo de señalización
15. `fallo_seguridad` — Fallo en instalaciones de seguridad
16. `conato_colision` — Conato de colisión (sin contacto)
17. `retroceso_no_autorizado` — Retroceso no autorizado
18. `otro` — Otros eventos

## Mapeo Excel → Normalizado (valores típicos del Excel CIAF)

| Valor Excel | Normalizado |
|-------------|-------------|
| Descarrilamiento / Descarrilamiento de tren / descarrilamiento | `descarrilamiento` |
| Colisión de trenes / Colisión frontal / Colisión lateral / Colisión por alcance | `colision_trenes` |
| Colisión entre tren y vehículo de carretera / Arrollamiento de vehículo por tren | `colision_vehiculo` |
| Colisión con roca / Colisión con desprendimiento de rocas | `colision_obstaculo` |
| Arrollamiento de persona / Arrollamiento de peatón / Arrollamiento | `arrollamiento_persona` |
| Arrollamiento de ciclista / Arrollamiento de motocicleta por tren | `arrollamiento_ciclista` |
| Accidente en paso a nivel | `paso_nivel` |
| Incendio de material rodante / Incendio en locomotora / Incendio en tren | `incendio` |
| Rotura de eje en tren de viajeros | `rotura_eje` |
| Fallo de cargamento | `fallo_cargamento` |
| Rebase de señal / Rebase indebido de señal / Rebase de señal en rojo | `rebase_senal` |
| Escape de material / Escape de tren a la deriva | `escape_material` |
| Fallo de señalización / Fallo en las instalaciones de seguridad | `fallo_senalizacion` |
| Incidente Operacional - Retroceso no autorizado | `retroceso_no_autorizado` |
| Conato de colisión / Conato de colisión entre trenes / Conato de colisión por alcance | `conato_colision` |
| Accidente ferroviario (genérico) | Requiere revisión del informe para clasificar |
| Incidente ferroviario (genérico) | Requiere revisión del informe para clasificar |
| Incidente operacional | `otro` (revisar contexto) |
| Accidente grave por descarrilamiento | `descarrilamiento` + severidad = muy grave |
