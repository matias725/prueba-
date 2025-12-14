#!/bin/bash

# Script de despliegue rápido para SmartConnect API en AWS EC2
# Uso: ./deploy_aws.sh

set -e

echo "========================================="
echo "SmartConnect API - Despliegue AWS EC2"
echo "========================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Error: No se encuentra manage.py${NC}"
    echo "Asegúrate de ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

# 1. Activar entorno virtual
echo -e "${YELLOW}[1/8] Activando entorno virtual...${NC}"
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi
source venv/bin/activate
echo -e "${GREEN}✓ Entorno virtual activado${NC}"
echo ""

# 2. Instalar/Actualizar dependencias
echo -e "${YELLOW}[2/8] Instalando dependencias...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✓ Dependencias instaladas${NC}"
echo ""

# 3. Verificar archivo .env
echo -e "${YELLOW}[3/8] Verificando configuración...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}¡Advertencia! No se encuentra archivo .env${NC}"
    echo "Copiando .env.example a .env..."
    cp .env.example .env
    echo -e "${YELLOW}Por favor, edita el archivo .env con tus configuraciones${NC}"
    read -p "Presiona Enter cuando hayas configurado el archivo .env..."
fi
echo -e "${GREEN}✓ Configuración verificada${NC}"
echo ""

# 4. Ejecutar migraciones
echo -e "${YELLOW}[4/8] Ejecutando migraciones de base de datos...${NC}"
python manage.py makemigrations
python manage.py migrate
echo -e "${GREEN}✓ Migraciones completadas${NC}"
echo ""

# 5. Recopilar archivos estáticos
echo -e "${YELLOW}[5/8] Recopilando archivos estáticos...${NC}"
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Archivos estáticos recopilados${NC}"
echo ""

# 6. Crear superusuario (opcional)
echo -e "${YELLOW}[6/8] ¿Deseas crear un superusuario? (s/n)${NC}"
read -p "" crear_superusuario
if [ "$crear_superusuario" = "s" ] || [ "$crear_superusuario" = "S" ]; then
    python manage.py createsuperuser
    echo -e "${GREEN}✓ Superusuario creado${NC}"
else
    echo "Saltando creación de superusuario"
fi
echo ""

# 7. Cargar datos iniciales (opcional)
echo -e "${YELLOW}[7/8] ¿Deseas cargar datos de prueba iniciales? (s/n)${NC}"
read -p "" cargar_datos
if [ "$cargar_datos" = "s" ] || [ "$cargar_datos" = "S" ]; then
    if [ -f "fixtures/initial_data.json" ]; then
        python manage.py loaddata fixtures/initial_data.json
        echo -e "${GREEN}✓ Datos iniciales cargados${NC}"
    else
        echo -e "${YELLOW}No se encontró archivo de fixtures${NC}"
    fi
else
    echo "Saltando carga de datos iniciales"
fi
echo ""

# 8. Verificar configuración
echo -e "${YELLOW}[8/8] Verificando configuración de Django...${NC}"
python manage.py check
echo -e "${GREEN}✓ Configuración verificada${NC}"
echo ""

# Resumen
echo -e "${GREEN}========================================="
echo "¡Despliegue completado exitosamente!"
echo "=========================================${NC}"
echo ""
echo "Pasos siguientes:"
echo "1. Para modo desarrollo:"
echo "   python manage.py runserver 0.0.0.0:9000"
echo ""
echo "2. Para producción con Gunicorn:"
echo "   gunicorn --workers 4 --bind 0.0.0.0:9000 smartconnect.wsgi:application"
echo ""
echo "3. Para producción en background:"
echo "   nohup python manage.py runserver 0.0.0.0:9000 > django.log 2>&1 &"
echo ""
echo "4. Acceder a:"
echo "   - API Info: http://98.88.189.220:9000/api/info/"
echo "   - Admin: http://98.88.189.220:9000/admin/"
echo "   - API Docs: Importa SmartConnect_Postman_Collection.json en Postman"
echo ""
echo -e "${YELLOW}Nota: Asegúrate de que el puerto 9000 esté abierto en el Security Group de AWS${NC}"
