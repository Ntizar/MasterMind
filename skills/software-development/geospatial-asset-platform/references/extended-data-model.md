# Extended Data Model — Personnel, Maintenance, Stock, Cameras

## Personnel as Assets

Personnel are `activos` with `categoria='humano'`. Extra data via JSONB metadata:

```json
{
    "dni": "12345678A", "especialidad": "Cardiología",
    "formaciones": [
        { "curso": "Reanimación Avanzada", "fecha": "2025-06-01", "caduca": "2027-06-01" }
    ],
    "permisos": [
        { "tipo": "conducir_b", "caduca": "2028-01-15" }
    ],
    "dias_vacaciones_total": 22, "dias_vacaciones_usados": 8
}
```

### Additional tables for HR

```sql
-- Vacaciones y permisos (más consultable que JSONB)
CREATE TABLE permisos_empleado (
    id UUID PRIMARY KEY, activo_id UUID REFERENCES activos(id),
    tipo VARCHAR(50) CHECK (tipo IN ('vacaciones','libre','enfermedad','formacion','permiso_especial')),
    fecha_inicio DATE, fecha_fin DATE,
    estado VARCHAR(30) CHECK (estado IN ('solicitado','aprobado','rechazado','en_curso','completado')),
    aprobado_por UUID REFERENCES usuarios(id)
);

-- Formaciones con caducidad
CREATE TABLE formaciones (
    id UUID PRIMARY KEY, activo_id UUID REFERENCES activos(id),
    curso VARCHAR(200), fecha DATE, caduca BOOLEAN DEFAULT false,
    fecha_caducidad DATE, certificado_url VARCHAR(500),
    obligatoria BOOLEAN DEFAULT false
);
```

## Maintenance Records

```sql
CREATE TABLE mantenimientos (
    id UUID PRIMARY KEY, activo_id UUID REFERENCES activos(id),
    tipo VARCHAR(50) CHECK (tipo IN ('preventivo','correctivo','predictivo','inspeccion','calibracion')),
    proxima_revision DATE, intervalo_dias INTEGER,
    coste_mano_obra DECIMAL(10,2), coste_piezas DECIMAL(10,2), coste_total DECIMAL(10,2),
    piezas_usadas JSONB DEFAULT '[]',  -- [{codigo, nombre, cantidad, coste}]
    horas_estimadas DECIMAL(5,2), horas_reales DECIMAL(5,2),
    fotos_antes TEXT[], fotos_despues TEXT[], informe_url VARCHAR(500)
);
```

## Quality Inspections

```sql
CREATE TABLE inspecciones (
    id UUID PRIMARY KEY, activo_id UUID REFERENCES activos(id),
    tipo VARCHAR(50) CHECK (tipo IN ('visual','funcional','seguridad','ambiental','sanitaria','estructural','electrica')),
    resultado VARCHAR(30) CHECK (resultado IN ('apto','apto_con_observaciones','no_apto','pendiente')),
    puntuacion INTEGER CHECK (puntuacion BETWEEN 0 AND 100),
    hallazgos JSONB DEFAULT '[]',  -- [{seccion, estado, observacion, fotos}]
    proxima_inspeccion DATE, informe_url VARCHAR(500)
);
```

## Warehouse Stock

```sql
CREATE TABLE stock (
    id UUID PRIMARY KEY, org_id UUID REFERENCES organizaciones(id),
    codigo VARCHAR(50), nombre VARCHAR(200), categoria VARCHAR(100),
    unidad VARCHAR(20) DEFAULT 'ud',
    cantidad_actual INTEGER DEFAULT 0, cantidad_minima INTEGER DEFAULT 0,
    almacen_id UUID REFERENCES activos(id),  -- Almacén es un activo tipo "ubicacion"
    proveedor VARCHAR(200), coste_unitario DECIMAL(10,2),
    lat DECIMAL(10,7), lng DECIMAL(10,7)
);
```

## CCTV / Video Sources

```sql
CREATE TABLE fuentes_video (
    id UUID PRIMARY KEY, org_id UUID REFERENCES organizaciones(id),
    tipo VARCHAR(30) CHECK (tipo IN ('cctv_rtsp','cctv_http','youtube_live','mjpeg','snapshot')),
    url_stream VARCHAR(500), url_snapshot VARCHAR(500),
    lat DECIMAL(10,7), lng DECIMAL(10,7),
    activo_id UUID REFERENCES activos(id),  -- Asociada a farola, edificio...
    nocturna BOOLEAN DEFAULT false, ptz BOOLEAN DEFAULT false
);
```

## Shift Management

```sql
CREATE TABLE turnos (
    id UUID PRIMARY KEY, org_id UUID, perfil_id UUID REFERENCES perfiles(id),
    nombre VARCHAR(100), hora_inicio TIME, hora_fin TIME, dias_semana INTEGER[]
);

CREATE TABLE asignaciones (
    id UUID PRIMARY KEY, activo_id UUID REFERENCES activos(id), turno_id UUID REFERENCES turnos(id),
    fecha DATE, lat DECIMAL(10,7), lng DECIMAL(10,7),
    estado VARCHAR(30) CHECK (estado IN ('asignado','en_servicio','descanso','ausente','sustituido')),
    UNIQUE (activo_id, fecha, turno_id)
);
```
