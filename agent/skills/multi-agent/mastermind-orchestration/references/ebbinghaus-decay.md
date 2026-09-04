# Sistema de Memoria con Decaimiento Ebbinghaus

Implementado 2026-06-10. Script `ebbinghaus-decay.py` en `scripts/`.

## Fórmula

R(t) = a / (log(t+1))^b + c

## 4 Perfiles de Decay

| Perfil | a | b | c | Relevancia a 30d | Relevancia a 180d | Qué incluye |
|---|---|---|---|---|---|---|
| Permanente | 1.0 | 0.0 | 0.0 | 100% | 100% | SOUL.md, reglas del sistema, arquitectura fundamental |
| Lento | 1.0 | 0.5 | 0.0 | 71% | 48% | Skills, patrones técnicos reutilizables, referencias |
| Normal | 1.0 | 1.0 | 0.0 | 52% | 29% | Soluciones a problemas específicos, guías de proyecto |
| Rápido | 1.0 | 2.0 | 0.0 | 30% | 12% | Fixes puntuales, contexto temporal, resultados de sesión |

## Clasificación Automática

- **Permanente:** contiene "soul.md", "arquitectura", "patrón fundamental", "regla del sistema"
- **Rápido:** contiene "fix", "error temporal", "urgente", "hoy", "resultado de sesión"
- **Lento:** contiene "skill", "patrón reutilizable", "arquitectura", "diseño", "referencia"
- **Normal:** todo lo demás

## Ejecución

```bash
python3 /hermes-home/scripts/ebbinghaus-decay.py
```

- Notas con score < 0.2 → se mueven a `notes/archive/`
- Informe JSON → `learning/ebbinghaus-decay-report.json`
- **No se pierden datos**, solo se archivan

## Skills Classification

- mastermind/ → permanente
- software-development, backend, infraestructura → lento
- resto → normal

## Primera Ejecución (2026-06-10)

- 65 notas analizadas
- 58 mantenidas, 7 archivadas
- 194 skills clasificadas (11 permanente, 22 lento, 161 normal)
