# Checklist de Salud del Sistema Mastermind

Ejecutar cuando el usuario pida autoauditoría o cuando se sospeche degradación.

## 1. SOUL.md

```bash
cat /hermes-home/SOUL.md
# Debe tener >100 chars y definir identidad, idioma, comunicación
```

**Si está vacío o incompleto:** usar `references/soul-template.md` como base.

## 2. Configuración

```bash
# TTS voice — debe ser español
grep "voice:" /hermes-home/config.yaml | head -3
# Esperado: es-ES-AlvaroNeural (no en-US-AriaNeural)

# Idioma display
grep "language:" /hermes-home/config.yaml | head -1
# Esperado: es (no en)

# Memoria
grep "memory_char_limit:" /hermes-home/config.yaml
grep "user_char_limit:" /hermes-home/config.yaml
```

**Corrección:**
```bash
hermes config set tts.edge.voice es-ES-AlvaroNeural
hermes config set display.language es
```

## 3. Skills

```bash
# Total
find /hermes-home/skills -name "SKILL.md" | wc -l

# Sin tags (deberían ser 0)
find /hermes-home/skills -name "SKILL.md" -exec sh -c '
  if head -1 "$1" | grep -q "^---"; then
    if ! head -10 "$1" | grep -q "^tags:"; then
      echo "NO TAGS: $1"
    fi
  fi
' _ {} \;

# Sin versión (deberían ser 0)
find /hermes-home/skills -name "SKILL.md" -exec sh -c '
  if head -1 "$1" | grep -q "^---"; then
    if ! head -10 "$1" | grep -q "^version:"; then
      echo "NO VERSION: $1"
    fi
  fi
' _ {} \;

# Demasiado grandes (>30KB → usar refs pattern)
find /hermes-home/skills -name "SKILL.md" -exec sh -c '
  size=$(wc -c < "$1")
  if [ "$size" -gt 30000 ]; then
    echo "TOO LARGE ($size bytes): $1"
  fi
' _ {} \;
```

## 4. Cron Jobs

```bash
hermes cron list
# Verificar que todos muestran "ok" en Last run
```

## 5. Memoria

```bash
hermes memory status
# Verificar que built-in está activo
# Verificar uso de caracteres (no debe superar 90%)
```

## 6. Reporte

Después de la auditoría, generar resumen con:
- Estado de cada检查 (✅/⚠️/🔴)
- Acciones correctivas tomadas
- Skills pendientes de mantenimiento

## Frecuencia

- **Semanal:** Check rápido (SOUL + config + cron)
- **Mensual:** Auditoría completa (todos los pasos)
- **Al detectar degradación:** Check inmediato
