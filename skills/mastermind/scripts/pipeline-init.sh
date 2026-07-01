#!/usr/bin/env bash
# ============================================================
# 🏭 Micro-Crons Pipeline - Script de Inicialización
# Crea la estructura de un proyecto y configura los cron jobs
# ============================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BASE_DIR="/root/workspace/proyectos"

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

crear_proyecto() {
    local nombre="$1"
    local tipo="${2:-generico}"
    local descripcion="${3:-Proyecto sin descripción}"
    local project_dir="${BASE_DIR}/${nombre}"

    if [[ -d "$project_dir" ]]; then
        log_error "El proyecto '${nombre}' ya existe en ${project_dir}"
        return 1
    fi

    log_info "Creando proyecto: ${nombre}"
    mkdir -p "${project_dir}"/{src,tests,docs,scripts}

    cat > "${project_dir}/pipeline-status.json" << EOF
{
  "proyecto": "${nombre}",
  "version": "1.0.0",
  "tipo": "${tipo}",
  "descripcion": "${descripcion}",
  "estado": "planning",
  "fase_actual": "inicializacion",
  "tarea_actual": null,
  "metricas": {
    "tareas_totales": 0,
    "tareas_completadas": 0,
    "tareas_en_curso": 0,
    "tareas_pendientes": 0,
    "tasa_exito": 100,
    "ultima_ejecucion": null,
    "proxima_ejecucion": null
  },
  "historial": [],
  "configuracion": {
    "frecuencia_horas": 2,
    "max_intentos_por_tarea": 3,
    "timeout_minutos": 30,
    "auto_validar": true
  }
}
EOF

    cat > "${project_dir}/backlog.json" << EOF
{
  "proyecto": "${nombre}",
  "tareas": []
}
EOF

    echo "" > "${project_dir}/.pipeline.lock"

    cat > "${project_dir}/README.md" << EOF
# ${descripcion}

## Estado del Pipeline
- **Estado:** Planning
- **Tipo:** ${tipo}
- **Creado:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Estructura
\`\`\`
${nombre}/
├── pipeline-status.json
├── backlog.json
├── src/
├── tests/
├── docs/
└── scripts/
\`\`\`

**Autor:** David Antizar
EOF

    log_success "Proyecto '${nombre}' creado en ${project_dir}"
    echo ""
    log_info "Estructura creada:"
    tree "$project_dir" 2>/dev/null || ls -la "$project_dir"
    echo ""
    log_info "Próximos pasos:"
    echo "  1. Agregar tareas al backlog.json"
    echo "  2. Crear cron job maestro con pipeline-generar-cron.sh"
    echo ""
    return 0
}

agregar_tarea() {
    local proyecto="$1"
    local tarea_json="$2"
    local backlog_file="${BASE_DIR}/${proyecto}/backlog.json"

    if [[ ! -f "$backlog_file" ]]; then
        log_error "No se encontró backlog para '${proyecto}'"
        return 1
    fi

    local temp_file=$(mktemp)
    jq --argjson tarea "$tarea_json" '.tareas += [$tarea]' "$backlog_file" > "$temp_file"
    mv "$temp_file" "$backlog_file"

    log_success "Tarea agregada al backlog de '${proyecto}'"

    local status_file="${BASE_DIR}/${proyecto}/pipeline-status.json"
    local temp_status=$(mktemp)
    jq --argjson total "$(jq '.tareas | length' "$backlog_file")" \
       '.metricas.tareas_totales = $total | .metricas.tareas_pendientes = $total' \
       "$status_file" > "$temp_status"
    mv "$temp_status" "$status_file"
    return 0
}

ver_estado() {
    local proyecto="$1"
    local project_dir="${BASE_DIR}/${proyecto}"

    if [[ ! -d "$project_dir" ]]; then
        log_error "No se encontró el proyecto '${proyecto}'"
        return 1
    fi

    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "📊 Estado del Pipeline: ${proyecto}"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    jq '.' "${project_dir}/pipeline-status.json"
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "📋 Backlog"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    jq '.tareas[] | "\(.id) [\(.estado)] \(.descripcion)"' "${project_dir}/backlog.json" -r
    echo ""
    return 0
}

ejecutar_iteracion() {
    local proyecto="$1"
    local project_dir="${BASE_DIR}/${proyecto}"
    local lock_file="${project_dir}/.pipeline.lock"

    if [[ -s "$lock_file" ]]; then
        log_warning "Pipeline bloqueado por otro proceso"
        cat "$lock_file"
        return 1
    fi

    echo "$$" > "$lock_file"
    trap 'rm -f "$lock_file"' EXIT

    log_info "Ejecutando iteración del pipeline '${proyecto}'"
    local estado=$(jq -r '.estado' "${project_dir}/pipeline-status.json")

    if [[ "$estado" == "done" ]]; then
        log_success "Proyecto completado"
        return 0
    fi

    local tarea=$(jq -r '.tareas[] | select(.estado == "pending") | .id' "${project_dir}/backlog.json" | head -1)

    if [[ -z "$tarea" ]]; then
        log_warning "No hay tareas pendientes"
        return 0
    fi

    log_info "Tarea seleccionada: ${tarea}"
    local now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    local temp_backlog=$(mktemp)
    jq --arg id "$tarea" \
       '(.tareas[] | select(.id == $id)).estado = "in-progress"' \
       "${project_dir}/backlog.json" > "$temp_backlog"
    mv "$temp_backlog" "${project_dir}/backlog.json"

    local temp_status=$(mktemp)
    jq --arg tarea "$tarea" --arg now "$now" \
       '.estado = "in-progress" | .tarea_actual.id = $tarea | .metricas.ultima_ejecucion = $now' \
       "${project_dir}/pipeline-status.json" > "$temp_status"
    mv "$temp_status" "${project_dir}/pipeline-status.json"

    rm -f "$lock_file"
    trap - EXIT
    log_success "Iteración iniciada. Tarea ${tarea} en progreso."
    return 0
}

show_help() {
    echo "🏭 Micro-Crons Pipeline - Gestor de Proyectos"
    echo ""
    echo "Uso: $0 <comando> [argumentos]"
    echo ""
    echo "Comandos:"
    echo "  crear <nombre> [tipo] [descripcion]  - Crear nuevo proyecto"
    echo "  estado <proyecto>                     - Ver estado del pipeline"
    echo "  iterar <proyecto>                     - Ejecutar una iteración"
    echo "  agregar <proyecto> <json_tarea>       - Agregar tarea al backlog"
    echo ""
    echo "Tipos: web | backend | documento | generico"
    echo ""
    echo "Ejemplo:"
    echo "  $0 crear mi-app web 'Dashboard interactivo'"
    echo ""
}

if [[ $# -lt 1 ]]; then
    show_help
    exit 1
fi

mkdir -p "$BASE_DIR"

case "$1" in
    crear)
        [[ $# -lt 2 ]] && { log_error "Uso: $0 crear <nombre> [tipo] [descripcion]"; exit 1; }
        crear_proyecto "$2" "${3:-generico}" "${4:-Proyecto ${2}}"
        ;;
    estado)
        [[ $# -lt 2 ]] && { log_error "Uso: $0 estado <proyecto>"; exit 1; }
        ver_estado "$2"
        ;;
    iterar)
        [[ $# -lt 2 ]] && { log_error "Uso: $0 iterar <proyecto>"; exit 1; }
        ejecutar_iteracion "$2"
        ;;
    agregar)
        [[ $# -lt 3 ]] && { log_error "Uso: $0 agregar <proyecto> <json_tarea>"; exit 1; }
        agregar_tarea "$2" "$3"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Comando desconocido: $1"
        show_help
        exit 1
        ;;
esac
