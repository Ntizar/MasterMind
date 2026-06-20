# ContrataPúblico — Sesión 4 (2026-06-16)

## Estado
**Sesión 4 NO completada.** Script era placeholder (`print('Sesión 4 placeholder')`). Tab 3 y Tab 5 existen como skeleton en index.html pero están vacías ("Próximamente: ...").

## Diagnóstico
- `index.html`: 2074 líneas, 89KB. Todo inline (no hay módulos separados).
- `js/ley-data.js`: existe (Sesión 1).
- `js/app.js`: NO existe (MEGA-PLAN.md lo menciona pero no existe).
- `js/modules/`: directorio NO existe (MEGA-PLAN.md lo menciona pero no existe).
- Tabs en sidebar: 10 tabs definidas (mapa, tipos, procedimientos, actas, plazos, checklist, umbral, solvencia, texto, glosario).
- Tabs implementadas: Tab 1 (mapa), Tab 2 (tipos), Tab 9 (texto).
- Tabs vacías: Tab 3 (procedimientos), Tab 4 (actas), Tab 5 (plazos), Tab 6 (checklist), Tab 7 (umbral), Tab 8 (solvencia), Tab 10 (glosario).
- `switchTab()`: lazy-load solo para 'mapa', 'texto', 'tipos'. Las demás tabs no tienen handler.

## Estructura real vs plan
| Plan | Real |
|------|------|
| `js/app.js` | No existe |
| `js/modules/*.js` | No existe |
| Todo inline en index.html | Sí (todo en un archivo) |

## Decisiones
- Sesión 4 requiere escribir `scripts/sesion-04-procedimientos-plazos.py` completo antes de ejecutar.
- El script debe inyectar HTML + JS en `index.html` para Tab 3 y Tab 5.
