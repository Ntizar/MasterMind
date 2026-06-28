# Procedimiento de Re-Indexación — Detalles Operativos

## Procedimiento Completo

```bash
cd /hermes-home/scripts && NAN_API="$NAN_API" /hermes-home/chromadb-venv/bin/python indexar-skills.py --reset 2>&1
```

### Pasos internos

1. Escanea `/hermes-home/skills/` buscando `SKILL.md`
2. Conecta con ChromaDB en `localhost:8000`
3. Con `--reset`: elimina colección existente y crea nueva
4. Genera embeddings con `qwen3-embedding` (4096 dims) vía NaN API
5. Inserta en batches de 10 skills

### Métricas típicas (2026-06-28)

- **SKILL.md encontrados:** 241
- **Skills indexados:** 240 (1 duplicado: `static-digest-pipeline`)
- **Tiempo total:** ~20 minutos
- **Embeddings por skill:** ~3s promedio (rango 2-5s)
- **Lotes HTTP POST:** 24 lotes de 10

### Logs de salida

Cada skill muestra:
```
[INFO]   [N/241] nombre-del-skill...
[INFO]     ✅ (4096 dims)
```

Al final:
```
[INFO] ✅ Indexación completada: 240 skills en ChromaDB
```

### Troubleshooting

- **Si falla con "connection refused":** ChromaDB no está corriendo. Ejecutar `start-chromadb.sh`
- **Si falla con "401 Unauthorized":** `NAN_API` no está set o es inválido
- **Si indexa menos de lo esperado:** buscar nombres duplicados en `/hermes-home/skills/`
- **Si tarda >30 min:** verificar latencia de NaN API para embeddings