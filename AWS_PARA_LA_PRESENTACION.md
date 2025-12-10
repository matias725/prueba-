# 🚀 QUÉ DECIR SOBRE LA ARQUITECTURA EN AWS

## Para tu presentación, explica esto:

---

## Arquitectura Actual (Desarrollo Local)

```
Tu Computadora
    ↓
Navegador (http://localhost:8000)
    ↓
Django (manage.py runserver)
    ↓
SQLite (db.sqlite3)
```

**Ventajas:**
- ✅ Fácil de desarrollar
- ✅ Sin costos
- ❌ Solo accesible localmente
- ❌ No escalable
- ❌ No es producción

---

## Arquitectura en AWS Lambda (Producción)

```
Internet (Cliente)
    ↓
Route 53 (DNS: api.ecoenergy.com)
    ↓
CloudFront (CDN - Cachea)
    ↓
API Gateway (Enruta peticiones)
    ↓
Lambda (Ejecuta código Python/Django)
    ↓
RDS MySQL (Base de datos en la nube)
    ↓
S3 + CloudFront (Archivos estáticos/media)
```

**Ventajas:**
- ✅ Accesible desde Internet públicamente
- ✅ HTTPS/SSL seguro
- ✅ Escalable automáticamente
- ✅ Backups automáticos
- ✅ Bajo costo (~$15-50/mes)
- ✅ Sin servidor que mantener
- ✅ Monitoreo incluido (CloudWatch)

---

## Archivos que creé para AWS

### 1. **requirements-lambda.txt**
Dependencias optimizadas para Lambda:
- Django + DRF
- Zappa (para desplegar)
- django-cors-headers (para frontend)
- mysqlclient (para RDS)

### 2. **zappa_settings.json**
Configuración de despliegue:
```json
{
  "dev": {
    "aws_region": "us-east-1",
    "s3_bucket": "ecoenergy-zappa-deployments",
    "environment_variables": {...}
  },
  "production": {
    "domain": "api.ecoenergy.com",
    "memory_size": 512,
    "timeout": 60
  }
}
```

### 3. **deploy_lambda.sh** (Linux/Mac)
Script automático que:
1. Verifica AWS CLI
2. Crea S3 bucket
3. Instala dependencias
4. Ejecuta migraciones
5. Despliega en Lambda
6. Muestra URL final

### 4. **deploy_lambda.ps1** (Windows)
Lo mismo pero en PowerShell

### 5. **AWS_CONFIG_COMPLETA.md**
Guía detallada con:
- Variables de entorno
- Crear RDS MySQL
- Configurar Security Groups
- Monitoreo con CloudWatch
- Troubleshooting

### 6. **DESPLIEGUE_CHECKLIST.md**
Checklist paso-a-paso:
- [ ] Verificaciones previas
- [ ] Configurar .env
- [ ] Desplegar (opción A: bash)
- [ ] Desplegar (opción B: PowerShell)
- [ ] Desplegar (opción C: manual)
- [ ] Verificar que funciona
- [ ] Seguridad en producción
- [ ] Troubleshooting

### 7. **SETTINGS_LAMBDA_SNIPPET.py**
Configuración adicional de Django para Lambda:
- Soporte MySQL + SQLite
- S3 para archivos
- CORS headers
- CloudWatch logging
- Security headers

---

## Cómo desplegar (cuando lo necesites)

### Opción A: Script automático (Recomendado)

```bash
# Linux/Mac
bash deploy_lambda.sh dev

# Windows PowerShell
.\deploy_lambda.ps1 -Environment dev
```

### Opción B: Manual paso a paso

```bash
cd monitoreo

# 1. Instalar herramientas
pip install zappa

# 2. Configurar AWS
aws configure

# 3. Crear S3 bucket
aws s3 mb s3://ecoenergy-zappa-deployments-dev

# 4. Desplegar
zappa deploy dev

# 5. Ver URL
zappa status dev
```

---

## QUÉ PASA CUANDO DESPLIEGAS

1. **Zappa** empaqueta tu código Django en un .zip
2. **AWS Lambda** recibe el .zip y crea una función
3. **API Gateway** crea un endpoint público: `https://xxxx.execute-api.us-east-1.amazonaws.com`
4. **Primera petición** descomprime el código (~10-15 segundos, "cold start")
5. **Peticiones siguientes** son rápidas (~200ms)
6. **Django maneja** las peticiones normalmente
7. **RDS MySQL** almacena los datos de forma persistente

---

## COSTOS (Estimados)

Para una API pequeña:

| Servicio | Uso | Costo |
|----------|-----|-------|
| Lambda | 100k requests/mes | ~$0.17 |
| API Gateway | 100k requests/mes | ~$3.50 |
| RDS MySQL | db.t3.micro | ~$15 |
| S3 + Transfers | < 1GB | < $1 |
| **TOTAL MENSUAL** | | **~$20** |

Para uso mayor:
- 1M requests/mes → ~$50
- 10M requests/mes → ~$300

**AWS Free Tier (primer año):**
- ✓ 1M Lambda requests gratis
- ✓ API Gateway primeros $3.50
- ✓ RDS 750 horas t2.micro gratis

---

## CASOS DE USO

**Despliegue en Lambda es ideal para:**
- ✅ APIs REST (como tu EcoEnergy)
- ✅ Aplicaciones pequeñas/medianas
- ✅ Startups
- ✅ APIs de microservicios
- ✅ Cuando quieres 0 ops (sin mantener servidores)

**NO es ideal para:**
- ❌ Aplicaciones que tardan > 15 minutos
- ❌ Aplicaciones con conexiones permanentes (WebSocket)
- ❌ Datos muy grandes (uploads > 512MB)
- ❌ Cuando necesitas GPU/procesamiento pesado

---

## PRÓXIMOS PASOS (Si lo necesitas)

1. **Crear cuenta AWS** (necesita tarjeta de crédito, pero tiene free tier)
2. **Instalar AWS CLI** - permite controlar AWS desde terminal
3. **Configurar credenciales** - `aws configure` con API keys
4. **Ejecutar deploy_lambda.sh** - automático
5. **Verificar en API Gateway** - obtener URL pública
6. **Crear RDS MySQL** - para datos persistentes
7. **Configurar dominio** - apuntar tu dominio a API Gateway
8. **SSL/TLS** - certificado HTTPS automático

---

## EN LA PRESENTACIÓN

Si tu profesor pregunta sobre despliegue:

> "Implementé la API para funcionar en **AWS Lambda**, que es la arquitectura más moderna para APIs REST. 
> 
> El código está listo para desplegar sin cambios. Solo necesitaría:
> 1. Cuenta AWS
> 2. Ejecutar un script de despliegue
> 3. Configurar RDS MySQL
> 
> Esto es **serverless** - no necesito mantener servidores. AWS escala automáticamente según el tráfico.
> 
> He incluido:
> - Scripts de despliegue automático (Bash y PowerShell)
> - Documentación completa (AWS_CONFIG_COMPLETA.md)
> - Checklist paso-a-paso (DESPLIEGUE_CHECKLIST.md)
> - Configuración optimizada (requirements-lambda.txt, zappa_settings.json)
> 
> El sistema costaría ~$20/mes en AWS para una API pequeña."

---

## ¿NECESITAS AYUDA?

Si quieres que:
- [ ] Deplaigue la API en AWS real ahora
- [ ] Configure RDS MySQL
- [ ] Agregue dominio personalizado (api.tu-dominio.com)
- [ ] Configure monitoreo y alertas
- [ ] Agregue autenticación JWT
- [ ] Agregue CI/CD con GitHub Actions

Solo avísame y lo hacemos!

