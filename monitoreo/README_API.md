# API REST - EcoEnergy Monitoring System

## 🚀 Descripción

API REST completa para el sistema de monitoreo energético EcoEnergy. Permite gestionar dispositivos, mediciones, alertas y zonas a través de endpoints RESTful.

## 📋 Características Implementadas

### ✅ Modelos con API Completa
- **Organizaciones** (solo lectura)
- **Zonas** (CRUD completo)
- **Dispositivos** (CRUD completo)
- **Mediciones** (CRUD completo)
- **Alertas** (CRUD completo)

### ✅ Funcionalidades Avanzadas
- Paginación automática (10 elementos por página)
- Filtros por múltiples criterios
- Búsqueda por texto
- Ordenamiento flexible
- Endpoints personalizados para estadísticas
- Validaciones completas en serializers
- Respuestas detalladas con datos relacionados

### ✅ Endpoints Personalizados
- `/api/dispositivos/{id}/consumo_total/` - Consumo total y promedio
- `/api/dispositivos/por_categoria/` - Agrupación por categoría
- `/api/zonas/{id}/estadisticas/` - Estadísticas por zona
- `/api/mediciones/estadisticas_generales/` - Estadísticas globales
- `/api/alertas/criticas/` - Solo alertas graves
- `/api/alertas/por_gravedad/` - Agrupación por gravedad
- `/api/organizaciones/{id}/resumen/` - Resumen completo

## 🛠️ Instalación y Configuración

### 1. Instalar Dependencias
```bash
cd monitoreo
pip install -r requirements.txt
```

### 2. Ejecutar Migraciones
```bash
python manage.py migrate
```

### 3. Crear Datos de Prueba (Opcional)
```bash
python manage.py crear_datos_demo
```

### 4. Iniciar el Servidor
```bash
python manage.py runserver
```

## 🔗 Acceso a la API

- **URL Base**: `http://localhost:8000/api/`
- **Navegador de API**: `http://localhost:8000/api/` (interfaz interactiva)
- **Admin Django**: `http://localhost:8000/admin/`

## 📖 Documentación Completa

Ver archivo [API_DOCUMENTATION.md](../API_DOCUMENTATION.md) para:
- Lista completa de endpoints
- Ejemplos de uso con curl
- Parámetros de consulta disponibles
- Formato de respuestas
- Manejo de errores

## 🧪 Pruebas

### Prueba Automática
```bash
python test_api.py
```

### Prueba Manual con curl

**Listar dispositivos:**
```bash
curl http://localhost:8000/api/dispositivos/
```

**Crear medición:**
```bash
curl -X POST http://localhost:8000/api/mediciones/ \
  -H "Content-Type: application/json" \
  -d '{"dispositivo": 1, "consumo": 15.5}'
```

**Obtener estadísticas de zona:**
```bash
curl http://localhost:8000/api/zonas/1/estadisticas/
```

## 📊 Estructura de la API

```
api/
├── serializers.py      # Serializers para todos los modelos
├── views.py            # ViewSets con lógica de negocio
├── urls.py             # Configuración de rutas
└── models.py           # (vacío - usa modelos de dispositivos)
```

## 🔐 Autenticación

Por defecto, la API es pública (`AllowAny`). Para producción, considera:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## 📝 Ejemplos de Respuestas

### Dispositivo Detallado
```json
{
  "id": 1,
  "nombre": "Sensor Principal",
  "categoria": "Sensor",
  "zona": 1,
  "zona_nombre": "Planta Baja",
  "organizacion_nombre": "EcoEnergy Corp",
  "watts": 5.5,
  "mediciones_recientes": [...],
  "alertas_recientes": [...],
  "consumo_total": 245.80
}
```

### Estadísticas de Zona
```json
{
  "zona": "Planta Baja",
  "total_dispositivos": 15,
  "consumo_total_kwh": 1250.75,
  "alertas_graves": 3,
  "watts_promedio": 85.33
}
```

## 🎯 Casos de Uso

1. **Monitoreo en tiempo real**: Crear mediciones periódicas
2. **Análisis de consumo**: Obtener estadísticas por zona/dispositivo
3. **Sistema de alertas**: Crear y consultar alertas por gravedad
4. **Gestión de dispositivos**: CRUD completo con validaciones
5. **Dashboard**: Endpoints de estadísticas para gráficos

## 🐛 Solución de Problemas

### Error: Module 'rest_framework' not found
```bash
pip install djangorestframework
```

### Error: No such table
```bash
python manage.py migrate
```

### Error: Connection refused
Verifica que el servidor esté corriendo:
```bash
python manage.py runserver
```

## 👨‍💻 Desarrollado por

Matias - Evaluación Sumativa 4 Back End

## 📅 Fecha

Diciembre 2024
