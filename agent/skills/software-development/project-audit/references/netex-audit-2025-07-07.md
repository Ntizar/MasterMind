# Caso de Estudio: Auditoría NeTEx-ES 2025-07-07

## Contexto

David pidió verificar que DECISIONES.md, README, spec, generador, ejemplo XML y validador decían lo mismo tras un rewrite estructural.

## Problemas detectados

1. **README.md** mencionaba `dataObjects` en contexto de "perfil propio" — reformulado para claridad
2. **DECISIONES.md** mencionaba `PassengerStoppingArea` y `FrameDefaults` sin marcar como obsoletos — añadido `~~` para que auditorías automáticas no los detecten como "presentes"
3. **stop_rules.py** mencionaba `PassengerStoppingArea` solo en comentario — correcto, no es problema

## Correcciones aplicadas

- README: "La estructura XML (`<frames>` en vez de `<dataObjects>`) no pasa validación XSD directa" → "La estructura XML propia (`<frames>` tipados en vez de `<dataObjects>`) no pasa validación XSD directa"
- README: "frame (sin dataObjects)" → "frames tipados"
- DECISIONES.md: "FrameDefaults" → "`FrameDefaults` (término obsoleto)"
- DECISIONES.md: "PassengerStoppingArea" → "~~PassengerStoppingArea~~" en contexto de eliminación

## Resultado

84/84 tests pasan. XML generado coherente con especificación. 13 archivos del proyecto verificados.

## Script de auditoría usado

```python
import re
def grep(pattern, text): return bool(re.search(pattern, text, re.MULTILINE | re.DOTALL))
def grep_count(pattern, text): return len(re.findall(pattern, text, re.MULTILINE | re.DOTALL))

# Dimensiones a verificar
dimensions = {
    "dataObjects eliminado": {"bad": "dataObjects", "good": "perfil propio"},
    "6 frames tipados": {"good": ["ResourceFrame", "SiteFrame", "ServiceFrame", "ServiceCalendarFrame", "TimetableFrame", "FareFrame"]},
    "ScheduledStopPoint": {"good": "ScheduledStopPoint", "bad": "PassengerStoppingArea"},
    "Tariff/FSE": {"good": ["Tariff", "FareStructureElement"], "bad": ["FareStructure", "FareComponent"]},
    "ParticipantRef mayúscula": {"good": "ParticipantRef", "bad": "participantRef"},
    "Sin FrameDefaults": {"bad": "FrameDefaults"},
}

for dim, rules in dimensions.items():
    for name, text in artifacts:
        good = all(r in text for r in rules.get("good", []))
        bad = any(r in text for r in rules.get("bad", []))
        status = "✅" if good and not bad else "❌"
        print(f"  {status} {dim} en {name}")
```