#!/bin/bash
# Embebe una librería CDN dentro de un HTML
# Uso: bash embeber-cdn.sh archivo.html "https://cdn.../lib.min.js"
#
# Resultado: reemplaza <script src="CDN_URL"></script> por <script>contenido</script>

HTML_FILE="$1"
CDN_URL="$2"

if [ -z "$HTML_FILE" ] || [ -z "$CDN_URL" ]; then
    echo "Uso: bash embeber-cdn.sh archivo.html 'https://cdn.../lib.min.js'"
    exit 1
fi

# Descargar librería
LIB_CONTENT=$(curl -sL "$CDN_URL")
if [ -z "$LIB_CONTENT" ]; then
    echo "❌ No se pudo descargar: $CDN_URL"
    exit 1
fi

# Calcular tamaño
LIB_SIZE=${#LIB_CONTENT}
echo "📦 Librería descargada: ${LIB_SIZE} bytes ($((LIB_SIZE / 1024)) KB)"

# Reemplazar tag CDN por versión inline
# Escapar / y & para sed
ESCAPED_URL=$(echo "$CDN_URL" | sed 's/[\/&]/\\&/g')
sed -i "s|<script src=\"${ESCAPED_URL}\"></script>|<script>\n${LIB_CONTENT}\n</script>|" "$HTML_FILE"

HTML_SIZE=$(wc -c < "$HTML_FILE")
echo "✅ HTML actualizado: ${HTML_SIZE} bytes ($((HTML_SIZE / 1024)) KB)"
echo "🔗 CDN eliminado: $CDN_URL"
