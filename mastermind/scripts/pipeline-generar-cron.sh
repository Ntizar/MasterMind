#!/usr/bin/env bash
# ============================================================
# 🏭 Generador de Cron Maestro para Pipeline
# Genera el comando para crear el cron job automáticamente
# ============================================================

set -euo pipefail

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}💡 $1${NC}"; }

# ============================================================
# Generar prompt del cron maestro
# ============================================================

generar_prompt() {
    local nombre="$1"
    local project_dir="/root/workspace/proyectos/${nombre}"
    local deliver="${2:-telegram}"
    local schedule="${3:-0 */2 * * *}"
    
    cat << EOF
Eres el orquestador del pipeline de producción del proyecto "${nombre}".

📁 Ubicación del proyecto: ${project_dir}

INSTRUCCIONES:
1. Lee el estado actual:
   cat ${project_dir}/pipeline-status.json | jq .

2. Lee el backlog de tareas:
   cat ${project_dir}/backlog.json | jq .

3. Determina la siguiente tarea a ejecutar:
   - Prioriza tareas con prioridad "alta" > "media" > "baja"
   - Respeta las dependencias (no ejecutes tareas con dependencias "pending")
   - No repitas tareas con 3+ intentos fallidos
   - Si no hay tareas disponibles, indica que el proyecto está completo

4. Si hay tarea disponible:
   a. Actualiza backlog.json: cambia estado de la tarea a "in-progress"
   b. Ejecuta la tarea:
      - Lee los criterios de aceptación
      - Crea/modifica los archivos necesarios
      - Implementa la funcionalidad descrita
   c. Si éxito:
      - Marca tarea como "done" en backlog.json
      - Agrega entrada al historial en pipeline-status.json
   d. Si falla:
      - Incrementa contador de intentos
      - Si intentos >= 3, marca como "failed"
      - Describe el error para debugging

5. Actualiza pipeline-status.json:
   - metricas.ultima_ejecucion = timestamp actual
   - metricas.tareas_completadas = count de tareas "done"
   - Si todas las tareas "done", marca estado: "done"

6. Entrega un RESUMEN al usuario:
   - Qué tarea se ejecutó
   - Qué se hizo específicamente
   - Estado general del proyecto (X/Y tareas completadas)
   - Próxima tarea programada

REGLAS CRÍTICAS:
- Cada tarea debe ser ATÓMICA (máx 1-2 archivos principales)
- Máximo 15 minutos de ejecución por tarea
- NUNCA dejes archivos a mitad de escritura
- Si un archivo es muy grande, divídelo en partes
- Siempre deja el proyecto en estado consistente
- Los archivos JSON deben ser válidos (usa jq para editar)

ENTREGA:
Formato del resumen:
📊 Pipeline: ${nombre}
✅ Tarea completada: [descripción]
📁 Archivos modificados: [lista]
📈 Progreso: X/Y tareas (Z%)
⏭️ Siguiente: [próxima tarea]
EOF
}

# ============================================================
# Generar comando de creación del cron
# ============================================================

generar_comando() {
    local nombre="$1"
    local deliver="${2:-telegram}"
    local schedule="${3:-0 */2 * * *}"
    local project_dir="/root/workspace/proyectos/${nombre}"
    
    local prompt
    prompt=$(generar_prompt "$nombre" "$deliver" "$schedule")
    
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "📋 COMANDO PARA CREAR EL CRON MAESTRO"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "# Copia y pega este comando en Hermes:"
    echo ""
    echo "hermes cron create \\"
    echo "  --name '${nombre}-pipeline' \\"
    echo "  --schedule '${schedule}' \\"
    echo "  --deliver '${deliver}' \\"
    echo "  --prompt '${prompt}'"
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "📌 Notas:"
    echo "  - Frecuencia actual: ${schedule}"
    echo "  - Entrega en: ${deliver}"
    echo "  - El cron ejecuta cada vez que se cumple el schedule"
    echo "  - Puedes pausar/reanudar con:"
    echo "    hermes cron pause ${nombre}-pipeline"
    echo "    hermes cron resume ${nombre}-pipeline"
    echo ""
}

# ============================================================
# Mostrar ayuda
# ============================================================

show_help() {
    echo "🏭 Generador de Cron Maestro para Pipeline"
    echo ""
    echo "Uso: $0 <nombre-proyecto> [deliver] [schedule]"
    echo ""
    echo "Argumentos:"
    echo "  nombre-proyecto  Nombre del proyecto (debe existir en /root/workspace/proyectos/)"
    echo "  deliver          Destino del mensaje (default: telegram)"
    echo "  schedule         Cron schedule (default: 0 */2 * * *)"
    echo ""
    echo "Ejemplos:"
    echo "  $0 mi-dashboard"
    echo "  $0 mi-dashboard telegram '0 */3 * * *'"
    echo "  $0 mi-dashboard origin '0 9 * * *'"
    echo ""
    echo "Horarios comunes:"
    echo "  '0 */2 * * *'    Cada 2 horas"
    echo "  '0 */3 * * *'    Cada 3 horas"
    echo "  '0 9 * * *'      Diario a las 9:00 UTC"
    echo "  '0 9,15,21 * * *' 3 veces al día (9am, 3pm, 9pm)"
    echo ""
}

# ============================================================
# Main
# ============================================================

if [[ $# -lt 1 ]]; then
    show_help
    exit 1
fi

NOMBRE="$1"
DELIVER="${2:-telegram}"
SCHEDULE="${3:-0 */2 * * *}"
PROJECT_DIR="/root/workspace/proyectos/${NOMBRE}"

# Verificar que el proyecto existe
if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "❌ Error: No se encontró el proyecto '${NOMBRE}'"
    echo "   Ubicación esperada: ${PROJECT_DIR}"
    echo ""
    echo "💡 Primero crea el proyecto con:"
    echo "   bash /root/workspace/Mastermind/mastermind/scripts/pipeline-init.sh crear ${NOMBRE}"
    exit 1
fi

# Verificar que tiene los archivos necesarios
if [[ ! -f "${PROJECT_DIR}/pipeline-status.json" ]]; then
    echo "❌ Error: Falta pipeline-status.json en el proyecto"
    echo "   El proyecto parece estar dañado o incompleto"
    exit 1
fi

# Generar comando
generar_comando "$NOMBRE" "$DELIVER" "$SCHEDULE"
