---
nombre: Dashboard Control Center
tipo: skill
descripcion: Gestión y mantenimiento del NaN Dashboard con Aurora Liquid Glass. Arquitectura, deployment, y cómo añadir nuevas secciones.
modelos: deepseek-v4-flash
tags: [dashboard, aurora, nan, control-center]
---

# Dashboard Control Center

El NaN Dashboard es el panel de control visual de la infraestructura personal de Ntizar. Corre en el microVM de NaN.builders, puerto 4000, expuesto en `ntizar.apps.nan.builders`.

## Arquitectura

- **Backend**: Node.js + Express (`/persist/nan-dashboard/server.js`)
- **Frontend**: HTML single-page con CSS de Ntizar-Aurora (Liquid Glass, azul+naranja)
- **Auth**: Basic Auth sobre HTTPS, contraseña personal
- **CDN**: Aurora CSS servido desde jsdelivr (`ntizar.css`)
- **Puerto**: 4000 (única exposición HTTP del microVM; resto de servicios van por proxy de path)

## Estructura de archivos

```
/persist/nan-dashboard/
├── server.js          # Backend Express (APIs + auth + file manager)
├── public/
│   └── index.html     # Frontend completo (Aurora Liquid Glass)
├── audit.log          # Registro de acciones del dashboard
├── package.json
└── node_modules/
```

## Endpoints API

| Endpoint | Método | Auth | Descripción |
|----------|--------|------|-------------|
| `/api/system` | GET | Basic | CPU, RAM, discos, uptime, procesos |
| `/api/apis` | GET | Basic | APIs configuradas (solo nombres) |
| `/api/skills` | GET | Basic | Lista skills + notas del repo Mastermind |
| `/api/skills/read?path=` | GET | Basic | Contenido de una skill específica |
| `/api/services` | GET | Basic | Puertos abiertos + procesos activos |
| `/api/github` | GET | Basic | Repos de GitHub via API |
| `/api/config` | GET | Basic | Config de Hermes (raw) |
| `/api/files?path=` | GET | Basic | Listar directorio |
| `/api/files/mkdir` | POST | Basic+ReAuth | Crear carpeta |
| `/api/files/write` | POST | Basic+ReAuth | Crear/editar archivo |
| `/api/files/delete` | POST | Basic+ReAuth | Borrar archivo/carpeta |
| `/api/files/read?path=` | GET | Basic | Leer contenido archivo |
| `/api/audit` | GET | Basic | Log de actividades |
| `/api/env/add` | POST | Basic+ReAuth | Añadir variable de entorno |

## Seguridad

- **Auth básica**: middleware `app.use('/api', ...)` solo protege endpoints API
- **Página HTML**: se sirve sin auth para que cargue el formulario de login
- **Re-autenticación**: operaciones destructivas requieren header `X-Auth-Confirm` con la contraseña
- **Rutas seguras**: file manager solo permite `/persist`, `/root`, `/hermes-home`
- **Protecciones**: no se puede borrar proyectos principales ni sobreescribir server.js/index.html
- **Audit log**: todas las acciones quedan registradas en `/persist/nan-dashboard/audit.log`

## Cómo añadir una nueva sección

1. **Backend**: crear endpoint en `server.js` con `app.get('/api/mi-seccion', ...)`
2. **Frontend**: añadir card en HTML y crear función JS que llame al API y pinte el contenido
3. **Diseño**: usar clases Aurora: `nz-card nz-card--glass` o `nz-card--glass-strong`
4. **Refresco**: añadir la llamada en la función `render()` que se ejecuta cada 30s

## Aurora Design System

El dashboard usa Ntizar-Aurora v4.2+ desde CDN:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.css">
```

Tema oscuro con `data-nz-theme="dark"` sobre el contenedor `.nz`.

Clases principales usadas:
- `.nz-container` — contenedor de página
- `.nz-card`, `.nz-card--glass`, `.nz-card--glass-strong`, `.nz-card--glass-brand` — tarjetas
- `.nz-grid`, `.nz-grid--2` — rejillas responsive
- `.nz-btn`, `.nz-btn--primary`, `.nz-btn--accent` — botones
- `.nz-text-sm`, `.nz-text-xs`, `.nz-text-lg` — tamaños de texto
- `.glass-header` — header con gradiente azul+naranja
- `.skill-tag` — pills para skills clickeables

Colores identidad:
- Azul brand: `#2563eb`
- Naranja accent: `#f97316`
- Fondo: `#0a0e1c` (azul marino oscuro)
- Fondo tarjetas: glass translúcido con backdrop-filter blur

## Mantenimiento

```bash
# Arrancar servidor
cd /persist/nan-dashboard && source /root/.env 2>/dev/null && node server.js

# Matar servidor
kill $(ps aux | grep "node server.js" | grep -v grep | awk '{print $2}')

# Ver logs
tail -f /persist/nan-dashboard/audit.log

# Ver puerto
curl -s -u "admin:\$Nan603060" http://localhost:4000/api/system
```

## Próximas features planeadas

- [ ] Config: modelo activo, proveedor, TTS/STT en vivo
- [ ] Multi-agente: selector de agente activo + cambio de modelo
- [ ] Cron jobs: ver y gestionar tareas programadas
- [ ] Editor de texto en navegador (para archivos pequeños)
- [ ] Subida de archivos drag&drop

## Notas

- La contraseña se define en el código como default `$Nan603060` y se puede sobreescribir con env var `DASH_PASSWORD`
- El audit.log se limpia automáticamente (solo últimas 50 entradas en el frontend)
- El servidor necesita `source /root/.env` para cargar GITHUB_TOKEN y otros secrets