# 📋 CHECKLIST: Desplegar EcoEnergy API en AWS Lambda

## ✅ ANTES DE EMPEZAR

### Requerimientos
- [ ] Cuenta AWS activa (con tarjeta de crédito)
- [ ] AWS CLI instalado: `pip install awscli`
- [ ] Zappa instalado: `pip install zappa`
- [ ] Credenciales AWS configuradas: `aws configure`
- [ ] Python 3.12 o 3.11 (Lambda requiere Python 3.9+)

### Verificar instalación

```bash
# En PowerShell (Windows)
aws --version
zappa --version
python --version

# Verificar credenciales
aws sts get-caller-identity
```

---

## 🔧 PASO 1: Configurar variables de entorno

### 1.1 Crear archivo .env

```bash
cd monitoreo

# Copiar template
cp example.env .env

# O crear manualmente con estos valores:
DJANGO_SECRET_KEY=tu-clave-super-segura-aqui-min-50-caracteres
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Para desarrollo (sin RDS)
DB_ENGINE=sqlite3
DB_NAME=db.sqlite3

# Para producción con RDS (después)
# DB_ENGINE=mysql
# DB_NAME=ecoenergy
# DB_USER=admin
# DB_PASSWORD=TuContraseña123!
# DB_HOST=tu-rds-endpoint.us-east-1.rds.amazonaws.com
# DB_PORT=3306
```

### 1.2 Generar DJANGO_SECRET_KEY segura

```bash
# En PowerShell
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Copiar el resultado a .env
```

---

## 🚀 PASO 2: Desplegar a Lambda (Opción A: Bash)

```bash
# En terminales Linux/Mac/WSL
bash deploy_lambda.sh dev

# Para producción
bash deploy_lambda.sh production
```

**¿Qué hace?**
1. ✓ Verifica AWS CLI y credenciales
2. ✓ Crea S3 bucket para Zappa
3. ✓ Instala dependencias Python
4. ✓ Ejecuta migraciones
5. ✓ Despliega en Lambda
6. ✓ Muestra URL de API

---

## 🚀 PASO 2 (ALTERNATIVA): Desplegar a Lambda (Opción B: PowerShell)

```powershell
# En Windows PowerShell
.\deploy_lambda.ps1 -Environment dev

# Para producción
.\deploy_lambda.ps1 -Environment production
```

---

## 🚀 PASO 2 (ALTERNATIVA): Despliegue Manual

Si los scripts no funcionan, haz esto manualmente:

### Paso A: Preparar ambiente

```bash
cd monitoreo

# Crear virtual environment
python -m venv venv_lambda
source venv_lambda/bin/activate  # En Windows: venv_lambda\Scripts\activate

# Instalar dependencias
pip install -r requirements-lambda.txt
```

### Paso B: Configurar AWS S3

```bash
# Crear bucket para Zappa (donde guardará despliegues)
aws s3 mb s3://ecoenergy-zappa-deployments-dev --region us-east-1
```

### Paso C: Desplegar

```bash
# Primera vez (crea nueva función Lambda)
zappa deploy dev

# Próximas veces (actualiza función existente)
zappa update dev

# Ver logs
zappa tail dev --since 10m

# Ver estado
zappa status dev
```

---

## 📊 PASO 3: Verificar que funcionó

### 3.1 Obtener URL de API

```bash
zappa status dev | grep "API Gateway URL"

# Salida esperada:
# API Gateway URL: https://xxxxxxxx.execute-api.us-east-1.amazonaws.com
```

### 3.2 Probar endpoints

```bash
# Guardar la URL
API_URL="https://xxxxxxxx.execute-api.us-east-1.amazonaws.com"

# Probar API root
curl -i $API_URL/api/rrhh/

# Probar empleados
curl -i $API_URL/api/rrhh/empleados/

# Probar departamentos
curl -i $API_URL/api/rrhh/departamentos/

# Respuesta esperada: 200 OK con JSON
```

### 3.3 Verificar logs

```bash
# Ver últimos 50 logs
zappa tail dev --since 1h

# Ver solo errores
aws logs filter-log-events \
  --log-group-name /aws/lambda/ecoenergy-api-dev \
  --filter-pattern "ERROR"
```

---

## 🗄️ PASO 4: Conectar RDS MySQL (Producción)

### 4.1 Crear RDS en AWS

```bash
# Crear base de datos MySQL
aws rds create-db-instance \
  --db-instance-identifier ecoenergy-prod \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --engine-version 8.0 \
  --master-username admin \
  --master-user-password "TuContraseña123!" \
  --allocated-storage 20 \
  --publicly-accessible false \
  --backup-retention-period 7 \
  --region us-east-1

# Esperar ~5 minutos a que se cree...

# Obtener endpoint
aws rds describe-db-instances \
  --db-instance-identifier ecoenergy-prod \
  --region us-east-1 \
  --query 'DBInstances[0].Endpoint.Address'
```

### 4.2 Actualizar .env con RDS

```bash
# Editar monitoreo/.env

DB_ENGINE=mysql
DB_NAME=ecoenergy
DB_USER=admin
DB_PASSWORD=TuContraseña123!
DB_HOST=ecoenergy-prod.c9akciq32.us-east-1.rds.amazonaws.com
DB_PORT=3306
```

### 4.3 Ejecutar migraciones en Lambda

```bash
# Conectar a shell de Lambda y ejecutar migraciones
zappa shell production

# Dentro del shell:
>>> from django.core.management import execute_from_command_line
>>> execute_from_command_line(['manage.py', 'migrate'])
>>> execute_from_command_line(['manage.py', 'createsuperuser'])
>>> exit()

# O más simple:
zappa manage production "migrate"
zappa manage production "createsuperuser"
```

### 4.4 Crear datos iniciales en RDS

```bash
# Si tienes script de datos
zappa manage production "shell < crear_rrhh_datos.py"

# O manual:
zappa shell production
>>> from usuarios.models import User
>>> User.objects.create_superuser('admin', 'admin@example.com', 'password')
>>> exit()
```

---

## 🔐 PASO 5: Seguridad en Producción

### 5.1 Usar AWS Parameter Store (recomendado)

En lugar de guardar contraseñas en .env, usa Parameter Store:

```bash
# Guardar contraseña RDS
aws ssm put-parameter \
  --name /ecoenergy/db-password \
  --value "TuContraseña123!" \
  --type SecureString \
  --region us-east-1

# En zappa_settings.json:
{
  "production": {
    "aws_environment_variables": {
      "DB_PASSWORD": "${ssm:/ecoenergy/db-password}"
    }
  }
}
```

### 5.2 Agregar dominio personalizado

```bash
# En zappa_settings.json
{
  "production": {
    "domain": "api.tu-dominio.com",
    "certificate_arn": "arn:aws:acm:us-east-1:ACCOUNT_ID:certificate/CERT_ID"
  }
}

# Luego:
zappa update production
zappa certify production
```

### 5.3 Configurar CORS (si necesitas frontend)

```bash
# En monitoreo/settings.py
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...rest...]

CORS_ALLOWED_ORIGINS = [
    "https://mi-frontend.com",
    "https://app.ecoenergy.com",
]
```

---

## 📈 PASO 6: Monitoreo y Logs

### Ver logs

```bash
# Últimas 10 líneas
zappa tail dev --since 1m

# Con filtro
aws logs tail /aws/lambda/ecoenergy-api-dev --follow

# Por tipo de evento
aws logs filter-log-events \
  --log-group-name /aws/lambda/ecoenergy-api-dev \
  --filter-pattern "ERROR" \
  --limit 20
```

### Métricas en CloudWatch

```bash
# Ver duración promedio de requests
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=ecoenergy-api-dev \
  --start-time 2025-12-09T00:00:00Z \
  --end-time 2025-12-09T23:59:59Z \
  --period 3600 \
  --statistics Average,Maximum

# Ver errores
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=ecoenergy-api-dev \
  --start-time 2025-12-09T00:00:00Z \
  --end-time 2025-12-09T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

---

## 🐛 Troubleshooting

### Error: "No module named 'mysqlclient'"

```bash
pip install mysqlclient==2.2.0
# En Windows puede necesitar compilador. Alternativamente:
pip install mysql-connector-python
```

### Error: "Access Denied to RDS"

1. Verificar Security Group de RDS permite tráfico desde Lambda
2. Verificar credenciales DB en .env
3. Verificar RDS está en la misma VPC que Lambda

```bash
# Obtener SG de Lambda
LAMBDA_SG=$(aws ec2 describe-security-groups \
  --filters Name=group-name,Values=default \
  --query 'SecurityGroups[0].GroupId' \
  --output text)

# Obtener SG de RDS
RDS_SG=$(aws rds describe-db-instances \
  --db-instance-identifier ecoenergy-prod \
  --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' \
  --output text)

# Permitir conexión
aws ec2 authorize-security-group-ingress \
  --group-id $RDS_SG \
  --protocol tcp \
  --port 3306 \
  --source-security-group-id $LAMBDA_SG
```

### Error: "Timeout (> 30 segundos)"

En `zappa_settings.json`:

```json
{
  "dev": {
    "timeout": 60,
    "memory_size": 512
  }
}
```

### Error: "Cold start lento"

Lambda tarda ~10 segundos en la primera ejecución. Es normal.
Para reducirlo:
- Aumentar memoria (más CPU)
- Usar Lambda Provisioned Concurrency (más caro)

---

## 📞 Comandos Útiles

```bash
# Estado de Lambda
zappa status dev

# Actualizar función
zappa update dev

# Ejecutar comando Django
zappa manage dev "migrate"
zappa manage dev "createsuperuser"

# Abrir shell interactivo
zappa shell dev

# Ver variables de entorno
zappa status dev | grep Environment

# Eliminar función Lambda
zappa undeploy dev --remove-logs

# Ver configuración guardada
cat zappa_settings.json

# Listar todas las funciones Lambda
aws lambda list-functions --region us-east-1

# Ver costos estimados
echo "Lambda suele costar ~$0.20/millón de requests"
echo "RDS micro suele costar ~$15/mes"
echo "S3 suele costar ~$0.023/GB/mes"
```

---

## 💰 Costos estimados (AWS Pricing)

| Servicio | Estimado |
|----------|----------|
| Lambda | ~$0.20 /millón requests |
| RDS MySQL | $10-20 /mes |
| S3 | $0.023 /GB/mes |
| API Gateway | $3.50 /millón requests |
| CloudFront | $0.085 /GB |
| **TOTAL** | **~$15-50 /mes** |

*Para desarrollo pequeño. Con más tráfico aumentará.*

---

## ✅ CHECKLIST FINAL

- [ ] AWS CLI configurado
- [ ] Credenciales AWS válidas
- [ ] Archivo .env completo
- [ ] S3 bucket creado
- [ ] Lambda función desplegada
- [ ] API Gateway funcionando
- [ ] RDS configurado (si usas producción)
- [ ] Migraciones ejecutadas
- [ ] Logs visibles en CloudWatch
- [ ] Endpoints retornan 200 OK
- [ ] Domain configurado (si tienes dominio)
- [ ] SSL/TLS certificado válido
- [ ] Backups automáticos habilitados
- [ ] Monitoreo configurado

---

## 🎓 Próximos pasos (Avanzado)

- [ ] Agregar CI/CD con GitHub Actions
- [ ] Configurar auto-scaling
- [ ] Agregar WAF (Web Application Firewall)
- [ ] Implementar caching con CloudFront
- [ ] Agregar autenticación JWT
- [ ] Configurar alertas en CloudWatch
- [ ] Documentación Swagger/OpenAPI
- [ ] Rate limiting con API Gateway

---

**¡Listo! Ahora tu API está en AWS Lambda con conexión a Internet pública.**

Para ver estado en cualquier momento:
```bash
zappa status dev
```

Para ver logs en vivo:
```bash
zappa tail dev --since 1h
```

