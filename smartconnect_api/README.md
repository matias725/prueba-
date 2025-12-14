# SmartConnect API - Sistema de Control de Acceso Inteligente

API RESTful desarrollada con Django Rest Framework para gestionar sensores RFID, usuarios, departamentos y eventos de acceso.

## Características

- ✅ Autenticación con JWT
- ✅ Gestión de sensores RFID (Tarjetas y Llaveros)
- ✅ Control de departamentos y zonas
- ✅ Registro de eventos de acceso
- ✅ Control de barreras de acceso
- ✅ Roles y permisos (Admin/Operador)
- ✅ Validaciones completas
- ✅ Manejo profesional de errores
- ✅ Desplegado en AWS EC2

## Requisitos

- Python 3.8+
- pip
- Virtual Environment

## Instalación

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd smartconnect_api
```

### 2. Crear virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```
SECRET_KEY=tu-secret-key-aqui
DEBUG=False
ALLOWED_HOSTS=tu-ip-aws,tu-dominio.com
```

### 5. Realizar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

## Estructura del Proyecto

```
smartconnect_api/
├── smartconnect/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── admin.py
│   └── __init__.py
├── manage.py
└── requirements.txt
```

## Modelos

### Departamento
- `nombre` (string, único)
- `descripcion` (texto)
- `ubicacion` (string)
- `activo` (booleano)
- `creado_en`, `actualizado_en` (datetime)

### Sensor
- `uid` (string, único)
- `nombre` (string, mínimo 3 caracteres)
- `tipo` (tarjeta, llavero)
- `estado` (activo, inactivo, bloqueado, perdido)
- `usuario_asignado` (FK Usuario)
- `departamento` (FK Departamento)
- `creado_en`, `actualizado_en` (datetime)

### Barrera
- `nombre` (string)
- `departamento` (OneToOne)
- `estado` (abierta, cerrada)
- `modo_manual` (booleano)

### Evento
- `sensor` (FK Sensor)
- `departamento` (FK Departamento)
- `tipo` (acceso_intento, acceso_permitido, acceso_denegado, barrera_abierta, barrera_cerrada)
- `resultado` (permitido, denegado)
- `descripcion` (texto)
- `usuario` (FK Usuario)
- `creado_en` (datetime)

## Endpoints

### Autenticación

#### Obtener Token
```
POST /api/token/
Content-Type: application/json

{
    "username": "admin",
    "password": "password"
}

Respuesta:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refrescar Token
```
POST /api/token/refresh/
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Información de la API

```
GET /api/info/

Respuesta:
{
    "autor": ["Tu Nombre Completo"],
    "asignatura": "Programación Back End",
    "proyecto": "SmartConnect - Sistema de Control de Acceso Inteligente",
    "descripcion": "API RESTful para gestionar sensores RFID...",
    "version": "1.0"
}
```

### Departamentos

```
GET /api/departamentos/              # Listar todos
GET /api/departamentos/{id}/         # Obtener detalle
POST /api/departamentos/             # Crear (Admin)
PUT /api/departamentos/{id}/         # Actualizar (Admin)
PATCH /api/departamentos/{id}/       # Actualizar parcial (Admin)
DELETE /api/departamentos/{id}/      # Eliminar (Admin)
GET /api/departamentos/activos/      # Listar solo activos
```

### Sensores

```
GET /api/sensores/                   # Listar todos
GET /api/sensores/{id}/              # Obtener detalle
POST /api/sensores/                  # Crear (Admin)
PUT /api/sensores/{id}/              # Actualizar (Admin)
PATCH /api/sensores/{id}/            # Actualizar parcial (Admin)
DELETE /api/sensores/{id}/           # Eliminar (Admin)
POST /api/sensores/registrar_acceso/ # Registrar intento de acceso
POST /api/sensores/{id}/bloquear/    # Bloquear sensor (Admin)
POST /api/sensores/{id}/marcar_perdido/ # Marcar como perdido (Admin)
```

### Barreras

```
GET /api/barreras/                   # Listar todas
GET /api/barreras/{id}/              # Obtener detalle
POST /api/barreras/                  # Crear (Admin)
PUT /api/barreras/{id}/              # Actualizar (Admin)
PATCH /api/barreras/{id}/            # Actualizar parcial (Admin)
DELETE /api/barreras/{id}/           # Eliminar (Admin)
POST /api/barreras/{id}/abrir/       # Abrir manualmente (Admin)
POST /api/barreras/{id}/cerrar/      # Cerrar manualmente (Admin)
```

### Eventos

```
GET /api/eventos/                    # Listar todos
GET /api/eventos/{id}/               # Obtener detalle
GET /api/eventos/ultimos/            # Últimos 10 eventos
GET /api/eventos/por_sensor/?sensor_id=1  # Eventos de un sensor
```

## Códigos de Estado HTTP

- **200** - OK
- **201** - Creado
- **400** - Error de validación
- **401** - Sin autenticación
- **403** - Sin permisos
- **404** - No encontrado

## Autenticación

Todos los endpoints requieren un token JWT válido en el header:

```
Authorization: Bearer <tu-token-aqui>
```

## Permisos

- **Admin**: CRUD completo en todas las entidades
- **Operador/Usuario Normal**: Solo lectura

## Validaciones

- UID de sensor: mínimo 3 caracteres, único
- Nombre: mínimo 3 caracteres
- Estado de sensor: activo, inactivo, bloqueado, perdido
- Estado de barrera: abierta, cerrada

## Despliegue en AWS

### Pasos para desplegar en EC2:

1. Conectar a la instancia
2. Instalar dependencias del sistema
3. Clonar el repositorio
4. Crear virtual environment
5. Instalar dependencias Python
6. Configurar variables de entorno
7. Ejecutar migraciones
8. Configurar Gunicorn y Nginx
9. Iniciar servicios

## Testing

Usar Postman o Apidog para probar los endpoints. Incluir el token JWT en el header Authorization.

## Autor

Tu Nombre Completo

## Licencia

MIT
