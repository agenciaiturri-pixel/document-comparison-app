#!/bin/bash

# Script de despliegue automatizado
# Uso: ./deploy.sh [local|production]

set -e

ENVIRONMENT=${1:-local}

echo "🚀 Iniciando despliegue en modo: $ENVIRONMENT"

# Función para verificar dependencias
check_dependencies() {
    echo "📋 Verificando dependencias..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker no está instalado"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose no está instalado"
        exit 1
    fi
    
    echo "✅ Dependencias verificadas"
}

# Función para configurar variables de entorno
setup_env() {
    echo "⚙️ Configurando variables de entorno..."
    
    if [ ! -f "backend/.env" ]; then
        echo "📝 Creando archivo .env desde template..."
        cp backend/.env.example backend/.env
        
        if [ "$ENVIRONMENT" = "production" ]; then
            echo "⚠️ IMPORTANTE: Edita backend/.env con tus configuraciones de producción"
            echo "   - Cambia SECRET_KEY por una clave segura"
            echo "   - Configura DATABASE_URL si usas base de datos externa"
            echo "   - Actualiza ALLOWED_ORIGINS con tu dominio"
            read -p "Presiona Enter cuando hayas terminado de editar .env..."
        fi
    else
        echo "✅ Archivo .env ya existe"
    fi
}

# Función para construir imágenes
build_images() {
    echo "🔨 Construyendo imágenes Docker..."
    docker-compose build --no-cache
    echo "✅ Imágenes construidas"
}

# Función para iniciar servicios
start_services() {
    echo "🚀 Iniciando servicios..."
    
    if [ "$ENVIRONMENT" = "production" ]; then
        docker-compose up -d
    else
        docker-compose up -d
    fi
    
    echo "⏳ Esperando que los servicios estén listos..."
    sleep 10
    
    # Verificar que los servicios estén corriendo
    if docker-compose ps | grep -q "Up"; then
        echo "✅ Servicios iniciados correctamente"
        echo ""
        echo "🌐 Aplicación disponible en:"
        echo "   Frontend: http://localhost:3000"
        echo "   Backend API: http://localhost:8000"
        echo "   Documentación API: http://localhost:8000/docs"
        
        if [ "$ENVIRONMENT" = "local" ]; then
            echo "   Base de datos: localhost:5432"
        fi
    else
        echo "❌ Error al iniciar servicios"
        docker-compose logs
        exit 1
    fi
}

# Función para mostrar logs
show_logs() {
    echo "📋 Mostrando logs de los servicios..."
    docker-compose logs -f
}

# Función para limpiar
cleanup() {
    echo "🧹 Limpiando recursos..."
    docker-compose down
    docker system prune -f
    echo "✅ Limpieza completada"
}

# Función para mostrar ayuda
show_help() {
    echo "Script de despliegue del Sistema de Comparación de Documentos"
    echo ""
    echo "Uso: $0 [COMANDO] [OPCIONES]"
    echo ""
    echo "Comandos:"
    echo "  local       Despliegue local (por defecto)"
    echo "  production  Despliegue de producción"
    echo "  logs        Mostrar logs de los servicios"
    echo "  stop        Detener servicios"
    echo "  clean       Limpiar recursos Docker"
    echo "  help        Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 local          # Despliegue local"
    echo "  $0 production     # Despliegue de producción"
    echo "  $0 logs           # Ver logs"
    echo "  $0 stop           # Detener servicios"
}

# Función principal
main() {
    case $ENVIRONMENT in
        "local"|"production")
            check_dependencies
            setup_env
            build_images
            start_services
            ;;
        "logs")
            show_logs
            ;;
        "stop")
            echo "🛑 Deteniendo servicios..."
            docker-compose down
            echo "✅ Servicios detenidos"
            ;;
        "clean")
            cleanup
            ;;
        "help")
            show_help
            ;;
        *)
            echo "❌ Comando no reconocido: $ENVIRONMENT"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main