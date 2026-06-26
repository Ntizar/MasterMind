# Template: Auto-actualizar README con progreso

Añadir esto al prompt del cron de mejora continua, justo antes del paso de git commit:

```
### Paso 8b: Actualizar README.md
Lee README.md y actualiza la sección "🔄 Mejora Continua" con datos actuales de progress.json:

1. Lee progress.json
2. Cuenta: temas mejorados, pendientes, completados
3. Lista los temas mejorados con sus scores
4. Actualiza la tabla "Estado actual" y "Temas ya mejorados"
5. Escribe el README actualizado con write_file()
```

## Bloque README a mantener

```markdown
## 🔄 Mejora Continua (MEGA-PLAN 2)

| Métrica | Valor |
|---------|-------|
| **Temas mejorados** | {N} / 107 |
| **Temas pendientes** | {107-N} / 107 |
| **Ejecuciones totales** | {total_runs} |
| **Último tema** | `{last_improved}` |

### Temas ya mejorados

| Tema | Nivel | Ronda | Ejercicios | Texto | Visual |
|------|-------|-------|------------|-------|--------|
{for each improved topic:}
| `{filename}` | {level} | {improvement_count} | {exercises} | {text} | {visual} |
```

## Pitfall

El README tiene SECCIONES que se sobreescriben completas. Usar `patch()` con la sección entera, no intentar actualizar solo una celda de la tabla.
