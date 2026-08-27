#!/usr/bin/env bash
# ============================================================
# 🏭 Generador de Cron Maestro para Pipeline
# Genera el comando para crear el cron job automáticamente
# ============================================================

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }

generar_prompt() {
    local nombre="$1"
    local project_dir="/root/workspace/proyectos/${nombre}"
    local deliver="${2:-telegram}"

    cat << EOF
Eres el orquestador del pipeline de producción del proyecto "${nombre}".

📁 Ubicación: ${project_dir}

INSTRUCCIONES:
1. Lee pipeline-status.json y backlog.json
2. Busca siguiente tarea pending sin dependencias bloqueadas
3. Si hay tarea:
   - Actualiza backlog.json → estado "in-progress"
   - Ejecuta la tarea (crea/modifica archivos)
   - Si éxito: marca "done", agrega al historial
   - Si falla: incrementa intentos, si >=3 marca "failed"
4. Actualiza métricas en pipeline-status.json
5. Entrega resumen: qué se hizo, progreso (X/Y), siguiente tarea

REGLAS:
- Tareas atómicas (max 1-2 archivos)
- Máx 15 min por tarea
- NUNCA dejes archivos a mitad
- JSON siempre válido
- Si proyecto completo → marca estado "done"
EOF
}

show_help() {
    echo "🏭 Generador de Cron Maestro para Pipeline"
    echo ""
    echo "Uso: $0 <nombre-proyecto> [deliver] [schedule]"
    echo ""
    echo "Ejemplo:"
    echo "  $0 mi-dashboard telegram '0 */2 * * *'"
    echo ""
}

if [[ $# -lt 1 ]]; then
    show_help
    exit 1
fi

NOMBRE="$1"
DELIVER="${2:-telegram}"
SCHEDULE="${3:-0 */2 * * *}"
PROJECT_DIR="/root/workspace/proyectos/${NOMBRE}"

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "❌ Error: No se encontró el proyecto '${NOMBRE}'"
    echo "   Ubicación esperada: ${PROJECT_DIR}"
    exit 1
fi

if [[ ! -f "${PROJECT_DIR}/pipeline-status.json" ]]; then
    echo "❌ Error: Falta pipeline-status.json"
    exit 1
fi

PROMPT=$(generar_prompt "$NOMBRE" "$DELIVER")

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "📋 COMANDO PARA CREAR EL CRON MAESTRO"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "hermes cron create \\"
echo "  --name '${NOMBRE}-pipeline' \\"
echo "  --schedule '${SCHEDULE}' \\"
echo "  --deliver '${DELIVER}' \\"
echo "  --prompt '${PROMPT}'"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📌 Frecuencia: ${schedule}"
echo "   Entrega: ${deliver}"
echo ""
