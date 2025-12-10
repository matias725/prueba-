#!/bin/bash

# Script de despliegue a AWS Lambda para EcoEnergy API
# Uso: bash deploy_lambda.sh [dev|production]

ENVIRONMENT="${1:-dev}"
REGION="us-east-1"

echo "🚀 Iniciando despliegue de EcoEnergy API en AWS Lambda ($ENVIRONMENT)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar AWS CLI
echo -e "${YELLOW}[1/7] Verificando AWS CLI...${NC}"
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI no está instalado. Instálalo con: pip install awscli${NC}"
    exit 1
fi
echo -e "${GREEN}✓ AWS CLI encontrado${NC}"

# 2. Verificar credenciales AWS
echo -e "${YELLOW}[2/7] Verificando credenciales AWS...${NC}"
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${RED}❌ Credenciales AWS no configuradas${NC}"
    echo "Configura con: aws configure"
    exit 1
fi
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
echo -e "${GREEN}✓ Credenciales válidas (Account: $ACCOUNT_ID)${NC}"

# 3. Crear S3 bucket si no existe
echo -e "${YELLOW}[3/7] Preparando S3 bucket...${NC}"
BUCKET_NAME="ecoenergy-zappa-deployments-$ENVIRONMENT"
if aws s3 ls "s3://$BUCKET_NAME" 2>&1 | grep -q 'NoSuchBucket'; then
    echo "Creando bucket $BUCKET_NAME..."
    aws s3 mb "s3://$BUCKET_NAME" --region $REGION
    echo -e "${GREEN}✓ Bucket creado${NC}"
else
    echo -e "${GREEN}✓ Bucket $BUCKET_NAME ya existe${NC}"
fi

# 4. Instalar dependencias Python
echo -e "${YELLOW}[4/7] Instalando dependencias Python...${NC}"
cd monitoreo
if [ ! -d "venv_lambda" ]; then
    python -m venv venv_lambda
fi

source venv_lambda/bin/activate 2>/dev/null || source venv_lambda/Scripts/activate 2>/dev/null

pip install -q -r requirements-lambda.txt
echo -e "${GREEN}✓ Dependencias instaladas${NC}"

# 5. Verificar variables de entorno
echo -e "${YELLOW}[5/7] Verificando variables de entorno...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Archivo .env no encontrado${NC}"
    echo "Copia .env.example a .env y completa los valores:"
    echo "  cp example.env .env"
    exit 1
fi
echo -e "${GREEN}✓ .env encontrado${NC}"

# 6. Ejecutar migraciones locales (testing)
echo -e "${YELLOW}[6/7] Preparando migraciones...${NC}"
python manage.py makemigrations > /dev/null 2>&1
python manage.py migrate --noinput > /dev/null 2>&1
echo -e "${GREEN}✓ Migraciones preparadas${NC}"

# 7. Desplegar con Zappa
echo -e "${YELLOW}[7/7] Desplegando en AWS Lambda...${NC}"

if [ "$ENVIRONMENT" = "dev" ]; then
    if zappa status dev > /dev/null 2>&1; then
        echo "Actualizando Lambda..."
        zappa update dev
    else
        echo "Creando nueva función Lambda..."
        zappa deploy dev
    fi
elif [ "$ENVIRONMENT" = "production" ]; then
    if zappa status production > /dev/null 2>&1; then
        echo "Actualizando Lambda en producción..."
        zappa update production
    else
        echo "Creando nueva función Lambda en producción..."
        zappa deploy production
    fi
else
    echo -e "${RED}❌ Entorno inválido. Usa: dev o production${NC}"
    exit 1
fi

# 8. Obtener URL de API
echo -e "\n${GREEN}✅ Despliegue completado!${NC}\n"
echo -e "${YELLOW}Información del despliegue:${NC}"
zappa status $ENVIRONMENT

# Obtener URL
API_URL=$(zappa status $ENVIRONMENT | grep "API Gateway URL" | awk '{print $NF}')
echo -e "\n${GREEN}🌐 API disponible en: ${API_URL}${NC}"
echo -e "Endpoints:\n"
echo "  GET    ${API_URL}api/rrhh/"
echo "  GET    ${API_URL}api/rrhh/departamentos/"
echo "  GET    ${API_URL}api/rrhh/empleados/"
echo "  GET    ${API_URL}api/rrhh/proyectos/"
echo "  GET    ${API_URL}api/rrhh/registros-tiempo/"

# Ver logs
echo -e "\n${YELLOW}Para ver logs en tiempo real:${NC}"
echo "  zappa tail $ENVIRONMENT --since 10m"

# Ver errores
echo -e "\n${YELLOW}Para ver errores:${NC}"
echo "  aws logs filter-log-events --log-group-name /aws/lambda/ecoenergy-api --filter-pattern ERROR"

# Deactivate venv
deactivate 2>/dev/null || true

echo -e "\n${GREEN}¡Listo para usar! 🎉${NC}"
