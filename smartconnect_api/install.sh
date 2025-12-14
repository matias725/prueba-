#!/bin/bash

# Script de instalación rápida para AWS EC2
# Uso: ./install.sh

echo "=========================================="
echo "SmartConnect API - Instalación en AWS EC2"
echo "=========================================="

# Detectar el sistema operativo
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "No se puede detectar el sistema operativo"
    exit 1
fi

echo "Sistema detectado: $OS"

# Actualizar sistema
echo "Actualizando sistema..."
if [ "$OS" = "amzn" ] || [ "$OS" = "amazonlinux" ]; then
    sudo yum update -y
elif [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    sudo apt update -y
    sudo apt upgrade -y
fi

# Instalar dependencias del sistema
echo "Instalando dependencias..."
if [ "$OS" = "amzn" ] || [ "$OS" = "amazonlinux" ]; then
    sudo yum install -y python3 python3-pip python3-devel gcc
else
    sudo apt install -y python3 python3-pip python3-dev build-essential
fi

# Crear directorio del proyecto (si no existe)
echo "Preparando directorio del proyecto..."
PROJECT_DIR="/opt/smartconnect"
if [ ! -d "$PROJECT_DIR" ]; then
    sudo mkdir -p $PROJECT_DIR
    sudo chown $USER:$USER $PROJECT_DIR
fi

cd $PROJECT_DIR

# Clonar repositorio (comentado, ajustar)
# git clone <tu-repo-url> .

# Crear virtual environment
echo "Creando virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias Python
echo "Instalando dependencias Python..."
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edita .env con tus valores:"
    echo "   nano .env"
fi

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate

# Crear superusuario (interactivo)
echo ""
echo "Crear superusuario:"
python manage.py createsuperuser

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --no-input

# Crear directorio para logs
mkdir -p logs

echo ""
echo "=========================================="
echo "✅ Instalación completada"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo ""
echo "1. Editar .env con tus valores:"
echo "   nano .env"
echo ""
echo "2. Probar servidor localmente:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver 0.0.0.0:8000"
echo ""
echo "3. Configurar Gunicorn y Nginx"
echo "   (Ver DEPLOY.md para instrucciones)"
echo ""
echo "URL de la API: http://$(hostname -I | awk '{print $1}')/api/"
echo ""
