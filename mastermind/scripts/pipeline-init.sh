#!/usr/bin/env bash
# ============================================================
# 🏭 Micro-Crons Pipeline - Script de Inicialización
# Crea la estructura de un proyecto y configura los cron jobs
# ============================================================

set -euo pipefail

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Directorio base
BASE_DIR="/root/workspace/proyectos"

# ============================================================
# Funciones auxiliares
# ============================================================

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# ============================================================
# Crear proyecto
# ============================================================

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
    
    # Crear estructura de directorios
    mkdir -p "${project_dir}"/{src,tests,docs,scripts}
    
    # Generar pipeline-status.json
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
    
    # Generar backlog.json vacío
    cat > "${project_dir}/backlog.json" << EOF
{
  "proyecto": "${nombre}",
  "tareas": []
}
EOF
    
    # Generar lock file inicial (no bloqueado)
    echo "" > "${project_dir}/.pipeline.lock"
    
    # Generar README.md
    cat > "${project_dir}/README.md" << EOF
# ${descripcion}

## Estado del Pipeline

- **Estado:** Planning
- **Tipo:** ${tipo}
- **Creado:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Estructura

\`\`\`
${nombre}/
├── pipeline-status.json  # Estado actual
├── backlog.json         # Tareas pendientes
├── src/                 # Código fuente
├── tests/               # Tests
├── docs/                # Documentación
└── scripts/             # Scripts auxiliares
\`\`\`

## Comandos

- Ver estado: \`cat pipeline-status.json | jq .\`
- Ver backlog: \`cat backlog.json | jq .\`

---

**Autor:** David Antizar
EOF
    
    log_success "Proyecto '${nombre}' creado en ${project_dir}"
    
    # Mostrar estructura
    echo ""
    log_info "Estructura creada:"
    tree "$project_dir" 2>/dev/null || ls -la "$project_dir"
    
    echo ""
    log_info "Próximos pasos:"
    echo "  1. Agregar tareas al backlog.json"
    echo "  2. Crear cron job maestro con:"
    echo "     hermes cron create --name '${nombre}-pipeline' \\"
    echo "       --schedule '0 */2 * * *' \\"
    echo "       --prompt 'Orquesta el pipeline de ${nombre}'"
    echo ""
    
    return 0
}

# ============================================================
# Agregar tarea al backlog
# ============================================================

agregar_tarea() {
    local proyecto="$1"
    local tarea_json="$2"  # JSON con la tarea
    
    local backlog_file="${BASE_DIR}/${proyecto}/backlog.json"
    
    if [[ ! -f "$backlog_file" ]]; then
        log_error "No se encontró backlog para '${proyecto}'"
        return 1
    fi
    
    # Agregar tarea al array usando jq
    local temp_file=$(mktemp)
    jq --argjson tarea "$tarea_json" '.tareas += [$tarea]' "$backlog_file" > "$temp_file"
    mv "$temp_file" "$backlog_file"
    
    log_success "Tarea agregada al backlog de '${proyecto}'"
    
    # Actualizar métricas
    local project_dir="${BASE_DIR}/${proyecto}"
    local status_file="${project_dir}/pipeline-status.json"
    local temp_status=$(mktemp)
    
    jq --argjson total "$(jq '.tareas | length' "$backlog_file")" \
       '.metricas.tareas_totales = $total | .metricas.tareas_pendientes = $total' \
       "$status_file" > "$temp_status"
    mv "$temp_status" "$status_file"
    
    return 0
}

# ============================================================
# Ver estado del proyecto
# ============================================================

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

# ============================================================
# Ejecutar iteración (para testing manual)
# ============================================================

ejecutar_iteracion() {
    local proyecto="$1"
    
    local project_dir="${BASE_DIR}/${proyecto}"
    local lock_file="${project_dir}/.pipeline.lock"
    
    # Verificar lock
    if [[ -s "$lock_file" ]]; then
        log_warning "Pipeline bloqueado por otro proceso"
        cat "$lock_file"
        return 1
    fi
    
    # Crear lock
    echo "$$" > "$lock_file"
    
    # Trap para limpiar lock al salir
    trap 'rm -f "$lock_file"' EXIT
    
    log_info "Ejecutando iteración del pipeline '${proyecto}'"
    
    # Leer estado actual
    local status=$(jq '.' "${project_dir}/pipeline-status.json")
    local estado=$(echo "$status" | jq -r '.estado')
    
    if [[ "$estado" == "done" ]]; then
        log_success "Proyecto completado"
        return 0
    fi
    
    # Buscar siguiente tarea
    local tarea=$(jq -r '.tareas[] | select(.estado == "pending") | .id' "${project_dir}/backlog.json" | head -1)
    
    if [[ -z "$tarea" ]]; then
        log_warning "No hay tareas pendientes"
        return 0
    fi
    
    log_info "Tarea seleccionada: ${tarea}"
    
    # Aquí iría la lógica de ejecución real
    # Por ahora solo actualizamos el estado
    
    local now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Actualizar tarea a in-progress
    local temp_backlog=$(mktemp)
    jq --arg id "$tarea" \
       '(.tareas[] | select(.id == $id)).estado = "in-progress"' \
       "${project_dir}/backlog.json" > "$temp_backlog"
    mv "$temp_backlog" "${project_dir}/backlog.json"
    
    # Actualizar estado del pipeline
    local temp_status=$(mktemp)
    jq --arg tarea "$tarea" --arg now "$now" \
       '.estado = "in-progress" | .tarea_actual.id = $tarea | .metricas.ultima_ejecucion = $now' \
       "${project_dir}/pipeline-status.json" > "$temp_status"
    mv "$temp_status" "${project_dir}/pipeline-status.json"
    
    # Limpiar lock
    rm -f "$lock_file"
    trap - EXIT
    
    log_success "Iteración iniciada. Tarea ${tarea} en progreso."
    
    return 0
}

# ============================================================
# Main
# ============================================================

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
    echo "Tipos de proyecto:"
    echo "  web        - Proyecto HTML/JS/CSS"
    echo "  backend    - Proyecto Node.js/Backend"
    echo "  documento  - Artículo/Documento"
    echo "  generico   - Proyecto genérico (default)"
    echo ""
    echo "Ejemplo:"
    echo "  $0 crear mi-app web 'Dashboard interactivo'"
    echo ""
}

# Verificar argumentos
if [[ $# -lt 1 ]]; then
    show_help
    exit 1
fi

# Crear directorio base si no existe
mkdir -p "$BASE_DIR"

# Ejecutar comando
case "$1" in
    crear)
        if [[ $# -lt 2 ]]; then
            log_error "Uso: $0 crear <nombre> [tipo] [descripcion]"
            exit 1
        fi
        crear_proyecto "$2" "${3:-generico}" "${4:-Proyecto ${2}}"
        ;;
    estado)
        if [[ $# -lt 2 ]]; then
            log_error "Uso: $0 estado <proyecto>"
            exit 1
        fi
        ver_estado "$2"
        ;;
    iterar)
        if [[ $# -lt 2 ]]; then
            log_error "Uso: $0 iterar <proyecto>"
            exit 1
        fi
        ejecutar_iteracion "$2"
        ;;
    agregar)
        if [[ $# -lt 3 ]]; then
            log_error "Uso: $0 agregar <proyecto> <json_tarea>"
            exit 1
        fi
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
