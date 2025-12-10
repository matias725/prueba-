# Configuración AWS para EcoEnergy API

## Variables de Entorno Necesarias para AWS

```bash
# Django
DJANGO_SECRET_KEY=tu-clave-super-secreta-aqui
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=api.ecoenergy.com,*.execute-api.us-east-1.amazonaws.com

# Base de Datos RDS MySQL
DB_ENGINE=mysql
DB_NAME=ecoenergy
DB_USER=admin
DB_PASSWORD=TuContraseñaSuperSegura123!
DB_HOST=ecoenergy-prod.c9akciq32.us-east-1.rds.amazonaws.com
DB_PORT=3306

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# S3 para archivos estáticos
AWS_STORAGE_BUCKET_NAME=ecoenergy-prod-static
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=d111111abcdef8.cloudfront.net

# CloudFront CDN
CLOUDFRONT_DISTRIBUTION_ID=E1234EXAMPLE

# CORS
CORS_ALLOWED_ORIGINS=https://api.ecoenergy.com,https://tu-dominio.com
```

## AWS Parameter Store (Más Seguro)

En lugar de variables de entorno, usa AWS Systems Manager Parameter Store:

```bash
# Guardar en Parameter Store
aws ssm put-parameter \
  --name /ecoenergy/django-secret-key \
  --value "tu-clave-secreta" \
  --type SecureString \
  --region us-east-1

aws ssm put-parameter \
  --name /ecoenergy/db-password \
  --value "TuContraseña" \
  --type SecureString \
  --region us-east-1

aws ssm put-parameter \
  --name /ecoenergy/db-host \
  --value "ecoenergy-prod.c9akciq32.us-east-1.rds.amazonaws.com" \
  --type String \
  --region us-east-1
```

Luego en zappa_settings.json referéncialos:

```json
{
  "production": {
    "aws_environment_variables": {
      "DJANGO_SECRET_KEY": "${ssm:/ecoenergy/django-secret-key}",
      "DB_PASSWORD": "${ssm:/ecoenergy/db-password}",
      "DB_HOST": "${ssm:/ecoenergy/db-host}"
    }
  }
}
```

## Crear RDS MySQL en AWS

### Opción 1: CLI

```bash
# Crear instancia RDS
aws rds create-db-instance \
  --db-instance-identifier ecoenergy-prod \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --engine-version 8.0 \
  --master-username admin \
  --master-user-password TuContraseñaSuperSegura123! \
  --allocated-storage 20 \
  --storage-type gp2 \
  --publicly-accessible false \
  --no-multi-az \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00" \
  --preferred-maintenance-window "mon:04:00-mon:05:00" \
  --enable-cloudwatch-logs-exports '["error","general","slowquery"]' \
  --region us-east-1

# Esperar a que esté disponible (toma ~5 minutos)
aws rds wait db-instance-available \
  --db-instance-identifier ecoenergy-prod \
  --region us-east-1

# Obtener endpoint
aws rds describe-db-instances \
  --db-instance-identifier ecoenergy-prod \
  --region us-east-1 \
  --query 'DBInstances[0].Endpoint.Address'
```

### Opción 2: AWS Console

1. RDS → Databases → Create database
2. Engine options: MySQL 8.0
3. DB instance identifier: `ecoenergy-prod`
4. Credentials: admin / TuContraseña
5. Instance class: db.t3.micro
6. Storage: 20 GB, gp2
7. Connectivity: Private (no public access)
8. Backup: 7 days retention
9. Create

## Configurar Security Group de RDS

```bash
# Obtener SG de Lambda
LAMBDA_SG=$(aws ec2 describe-security-groups \
  --filters Name=group-name,Values=lambda-rds \
  --query 'SecurityGroups[0].GroupId' \
  --output text)

# Obtener SG de RDS
RDS_SG=$(aws ec2 describe-security-groups \
  --filters Name=group-name,Values=rds-sg \
  --query 'SecurityGroups[0].GroupId' \
  --output text)

# Permitir conexión desde Lambda a RDS
aws ec2 authorize-security-group-ingress \
  --group-id $RDS_SG \
  --protocol tcp \
  --port 3306 \
  --source-security-group-id $LAMBDA_SG \
  --region us-east-1
```

## Desplegar en Lambda con Zappa

### Paso 1: Instalar dependencias

```bash
cd monitoreo
python -m venv venv_lambda
source venv_lambda/bin/activate  # En Windows: venv_lambda\Scripts\activate

pip install -r requirements-lambda.txt
```

### Paso 2: Configurar AWS Credentials

```bash
# En Windows PowerShell
[System.Environment]::SetEnvironmentVariable("AWS_ACCESS_KEY_ID", "AKIAIOSFODNN7EXAMPLE", "User")
[System.Environment]::SetEnvironmentVariable("AWS_SECRET_ACCESS_KEY", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY", "User")
[System.Environment]::SetEnvironmentVariable("AWS_DEFAULT_REGION", "us-east-1", "User")

# En Linux/Mac
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_DEFAULT_REGION="us-east-1"
```

### Paso 3: Preparar .env para Lambda

```bash
# Crear archivo .env en monitoreo/
DJANGO_SECRET_KEY=tu-clave-secreta-aqui
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=api.ecoenergy.com,*.execute-api.us-east-1.amazonaws.com
DB_ENGINE=mysql
DB_NAME=ecoenergy
DB_USER=admin
DB_PASSWORD=TuContraseñaSuperSegura123!
DB_HOST=ecoenergy-prod.c9akciq32.us-east-1.rds.amazonaws.com
DB_PORT=3306
```

### Paso 4: Desplegar

```bash
# Inicializar Zappa (primera vez)
zappa init
# Responde:
# - Environment: dev (o production)
# - S3 bucket: ecoenergy-zappa-deployments
# - Django settings: monitoreo.settings

# Desplegar a Lambda
zappa deploy dev

# Salida esperada:
# Deploying API Gateway...
# Creating Lambda function...
# API Gateway URL: https://xxxxxxxx.execute-api.us-east-1.amazonaws.com
```

### Paso 5: Ejecutar migraciones en Lambda

```bash
# Conectar a Lambda para ejecutar migraciones
zappa shell dev

>>> from django.core.management import execute_from_command_line
>>> execute_from_command_line(['manage.py', 'migrate'])
>>> exit()

# O en terminal:
zappa manage dev "migrate"
zappa manage dev "createsuperuser"
```

## Monitorear en CloudWatch

```bash
# Ver logs en tiempo real
aws logs tail /aws/lambda/ecoenergy-api --follow

# Ver errores
aws logs filter-log-events \
  --log-group-name /aws/lambda/ecoenergy-api \
  --filter-pattern "ERROR" \
  --region us-east-1

# Métricas de Lambda
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=ecoenergy-api \
  --start-time 2025-12-09T00:00:00Z \
  --end-time 2025-12-09T23:59:59Z \
  --period 3600 \
  --statistics Average,Maximum
```

## Estructura Final en AWS

```
┌─────────────────────────────────────────┐
│        Route 53 / CloudFlare            │
│     (DNS: api.ecoenergy.com)           │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  CloudFront CDN     │  (Cachea respuestas)
        │  (Distribución)     │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   API Gateway       │  (Enruta peticiones)
        │ (HTTPS endpoint)    │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │ Lambda Function     │  (Ejecuta Django)
        │ (ecoenergy-api)     │  (Python 3.12)
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   RDS MySQL 8.0     │  (Base de datos)
        │ (ecoenergy-prod)    │
        └─────────────────────┘
        
        ┌─────────────────────┐
        │   S3 + CloudFront   │  (Archivos estáticos)
        │  (Media/Static)     │
        └─────────────────────┘
        
        ┌─────────────────────┐
        │  CloudWatch Logs    │  (Monitoreo)
        │  CloudWatch Alarms  │  (Alertas)
        └─────────────────────┘
```

## Validar Despliegue

```bash
# 1. Verificar que Lambda está corriendo
aws lambda get-function \
  --function-name ecoenergy-api \
  --region us-east-1

# 2. Probar API
curl -i https://xxxxxxxx.execute-api.us-east-1.amazonaws.com/api/rrhh/

# Respuesta esperada (200 OK):
# {
#   "departamentos": "https://...",
#   "empleados": "https://...",
#   "proyectos": "https://...",
#   "registros-tiempo": "https://...",
#   "dashboard": "https://..."
# }

# 3. Verificar base de datos está conectada
curl -i https://xxxxxxxx.execute-api.us-east-1.amazonaws.com/api/rrhh/empleados/

# Respuesta esperada (200 OK con empleados):
# {
#   "count": 5,
#   "next": null,
#   "previous": null,
#   "results": [...]
# }
```

## Troubleshooting

### Error: "No module named 'mysqlclient'"
```bash
pip install mysqlclient==2.2.0
# O si estás en Windows:
pip install mysql-connector-python==8.0.33
```

### Error: "Access Denied for user 'admin'@'10.0.0.1'"
- Verificar que RDS Security Group permite tráfico desde Lambda
- Verificar credenciales en .env
- Verificar que RDS está en la misma VPC que Lambda

### Error: "Connect timeout"
- RDS no es accesible desde Lambda
- Verificar VPC security groups
- Verificar que RDS está publicly accessible = false (correcto para privada)

### Lambda timeout (> 60 segundos)
```bash
# Aumentar timeout en zappa_settings.json
"timeout": 120
# Y aumentar memoria
"memory_size": 1024
```

