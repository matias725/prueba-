# 🚀 Despliegue en AWS Lambda con API Gateway

## Opción 1: Zappa (Recomendado - Más Simple)

### Paso 1: Instalar dependencias

```bash
cd monitoreo
pip install zappa
pip install -r requirements-lambda.txt
```

### Paso 2: Inicializar Zappa

```bash
zappa init
# Responde las preguntas:
# - environment name: dev
# - s3 bucket: ecoenergy-zappa-deployments (o tu bucket)
# - django settings module: monitoreo.settings
```

### Paso 3: Desplegar a Lambda

```bash
# Primera vez (crea la función Lambda y API Gateway)
zappa deploy dev

# Actualizaciones futuras
zappa update dev
```

### Paso 4: Configurar variables de entorno

```bash
# Edita zappa_settings.json con tus valores de AWS
zappa status dev
zappa logs dev --since 1h
```

---

## Opción 2: AWS RDS + EC2 (Ya configurado)

Si prefieres una arquitectura más tradicional:

```bash
# 1. Crear instancia EC2 Debian 12
# 2. Crear RDS MySQL
# 3. Ejecutar deploy_debian12.sh

bash deploy_debian12.sh
```

---

## Opción 3: Serverless Framework + Lambda

### Paso 1: Instalar Serverless

```bash
npm install -g serverless
npm install serverless-python-requirements --save-dev
```

### Paso 2: Configurar serverless.yml

```yaml
service: ecoenergy-api

provider:
  name: aws
  runtime: python3.12
  region: us-east-1
  environment:
    DJANGO_DEBUG: false
    DB_HOST: ${ssm:/ecoenergy/db_host}
    DB_PASSWORD: ${ssm:/ecoenergy/db_password}

functions:
  api:
    handler: monitoreo.wsgi.application
    events:
      - httpApi:
          path: /{proxy+}
          method: ANY

plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    dockerizePip: true
```

### Paso 3: Desplegar

```bash
serverless deploy
```

---

## Configuración de RDS MySQL

### Desde AWS Console:

1. **RDS → Create database**
   - Engine: MySQL 8.0
   - Instance class: db.t3.micro
   - Storage: 20 GB
   - Publicly accessible: No (solo desde EC2/Lambda)

2. **Security Group**
   - Inbound: Port 3306 desde Lambda/EC2 security group
   - Outbound: Allow all

3. **Parameter Group**
   ```sql
   character_set_client = utf8mb4
   collation_connection = utf8mb4_unicode_ci
   ```

### Variables de entorno (.env):

```bash
DB_ENGINE=mysql
DB_NAME=ecoenergy
DB_USER=admin
DB_PASSWORD=TU_CONTRASEÑA_SEGURA
DB_HOST=ecoenergy.XXXXX.us-east-1.rds.amazonaws.com
DB_PORT=3306

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key

# Django
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=tu_secret_key_segura
ALLOWED_HOSTS=api.tu-dominio.com,*.execute-api.us-east-1.amazonaws.com
```

---

## Configuración de Lambda para CORS

**Agregar a monitoreo/settings.py:**

```python
# CORS para API Gateway
INSTALLED_APPS += ['corsheaders']

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... resto de middleware
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://api.ecoenergy.com",
    "https://*.execute-api.us-east-1.amazonaws.com",
]

CORS_ALLOW_CREDENTIALS = True
```

---

## Verificar despliegue

```bash
# Listar función Lambda
aws lambda list-functions --region us-east-1

# Ver logs
aws logs tail /aws/lambda/ecoenergy-api --follow

# Probar endpoint
curl https://tu-api-gateway-url/api/rrhh/

# Monitorar CloudWatch
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --start-time 2025-12-09T00:00:00Z \
  --end-time 2025-12-09T23:59:59Z \
  --period 3600 \
  --statistics Average
```

---

## Troubleshooting

### Error: "No module named 'django'"
```bash
# Asegúrate que zappa instale las dependencias
zappa deploy dev --requirements monitoreo/requirements-lambda.txt
```

### Error: "Database connection refused"
```bash
# Verifica Security Group de RDS
# Agregua security group de Lambda a inbound rules de RDS
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxx \
  --protocol tcp \
  --port 3306 \
  --source-security-group-id sg-yyyyyyy
```

### Cold start > 30 segundos
```bash
# Aumenta memoria en zappa_settings.json
"memory_size": 1024
```

---

## Estructura en AWS

```
API Gateway
    ↓
Lambda Function (Python + Django)
    ↓
RDS MySQL (Database)
    ↓
S3 (Media/Static files con CloudFront)
```

---

## Pasos siguientes

1. ✅ Crear S3 bucket para archivos estáticos
2. ✅ Configurar CloudFront CDN
3. ✅ Agregar SSL/TLS certificate
4. ✅ Configurar auto-scaling
5. ✅ Agregar monitoring con CloudWatch
6. ✅ Configurar backups automáticos en RDS
7. ✅ Agregar WAF (Web Application Firewall)

