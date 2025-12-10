# Configuración adicional para AWS Lambda
# Agregar esto a monitoreo/settings.py si quieres optimizar para Lambda

# ====== AWS LAMBDA SPECIFIC SETTINGS ======

import os
import sys

# Detectar si estamos en Lambda
IS_LAMBDA = os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is not None
IS_PRODUCTION = os.getenv('DJANGO_DEBUG', 'False') == 'False'

# ---- BASE CONFIGURATION ----
if IS_LAMBDA:
    # En Lambda, usar /tmp para archivos temporales
    TEMP_DIR = '/tmp'
else:
    TEMP_DIR = os.path.join(BASE_DIR, 'tmp')

# ---- DATABASE CONFIGURATION ----
# Soportar tanto SQLite (desarrollo) como MySQL (producción)

DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite3')

if DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'ecoenergy'),
            'USER': os.getenv('DB_USER', 'admin'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': int(os.getenv('DB_PORT', 3306)),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                # Connection pooling
                'pool_recycle': 280,
                'autocommit': True,
            },
            'CONN_MAX_AGE': 600,  # Persistir conexiones 10 minutos
        }
    }
else:
    # Default SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.getenv('DB_NAME', str(BASE_DIR / 'db.sqlite3')),
        }
    }

# ---- STATIC FILES CONFIGURATION ----
# Para Lambda usar S3, para desarrollo usar local

if IS_LAMBDA or IS_PRODUCTION:
    # AWS S3 Storage
    INSTALLED_APPS += ['storages']
    
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    
    # AWS S3
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'ecoenergy-static')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN', f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com')
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    
    # CloudFront CDN
    CLOUDFRONT_DISTRIBUTION_ID = os.getenv('CLOUDFRONT_DISTRIBUTION_ID', '')
    if CLOUDFRONT_DISTRIBUTION_ID:
        AWS_S3_CUSTOM_DOMAIN = f'd{CLOUDFRONT_DISTRIBUTION_ID}.cloudfront.net'
    
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    # Local development
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_ROOT = BASE_DIR / 'media'

# ---- LOGGING CONFIGURATION ----
# Logs van a CloudWatch automáticamente en Lambda

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',  # No loguear queries SQL en producción
        },
    },
}

# ---- CORS CONFIGURATION ----
# Necesario para acceso desde frontend

INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['content-type', 'authorization']

# ---- REST FRAMEWORK CONFIGURATION ----
# Optimizado para Lambda

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# ---- CACHING ----
# Para Lambda usar ElastiCache o DynamoDB como backend

if os.getenv('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.getenv('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# ---- SECURITY HEADERS ----
# Recomendado para Lambda/API Gateway

if not DEBUG:
    # HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Security headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookies
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True

# ---- TIMEOUT ----
# Aumentar para Lambda

if IS_LAMBDA:
    DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
    FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB

# ---- DISABLE UNUSED FEATURES ----
# Para reducir latencia en Lambda

if IS_LAMBDA:
    # Desactivar migrations automáticas (se hacen manualmente)
    # MIGRATION_MODULES = {app: None for app in INSTALLED_APPS}
    
    # Desactivar collectstatic warning
    STATIC_ROOT = '/tmp/staticfiles'

print(f"Django running in Lambda: {IS_LAMBDA}")
print(f"Database: {DB_ENGINE}")
print(f"Debug mode: {DEBUG}")
