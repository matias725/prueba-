# 🎯 EVALUACIÓN SUMATIVA 4 - API REST ECOENERGY

## ✅ IMPLEMENTACIÓN COMPLETADA

Se ha implementado una **API REST completa** para el sistema de monitoreo energético EcoEnergy usando Django REST Framework.

## 📁 Archivos Creados/Modificados

### Nuevos Archivos:
1. **`monitoreo/api/serializers.py`** (122 líneas)
   - Serializers para todos los modelos (Zona, Dispositivo, Medicion, Alerta, Organizacion)
   - Validaciones personalizadas
   - Campos de solo lectura con información relacionada
   - Serializer detallado con mediciones y alertas recientes

2. **`monitoreo/api/views.py`** (290 líneas)
   - 5 ViewSets completos con CRUD
   - 12 endpoints personalizados
   - Filtros avanzados y búsquedas
   - Endpoints de estadísticas

3. **`API_DOCUMENTATION.md`** (Documentación completa)
4. **`monitoreo/README_API.md`** (Guía de uso)
5. **`monitoreo/test_api.py`** (Script de prueba)

### Archivos Modificados:
1. **`monitoreo/api/urls.py`** - Router de DRF con todos los endpoints
2. **`monitoreo/monitoreo/settings.py`** - Configuración de REST_FRAMEWORK
3. **`monitoreo/requirements.txt`** - Dependencia djangorestframework

## 🚀 CÓMO EJECUTAR

### Paso 1: Instalar Dependencias
```powershell
cd C:\Users\matia\Documents\1111\unidad1-DMpython-MZ\monitoreo
pip install djangorestframework
```

### Paso 2: Aplicar Migraciones (si es necesario)
```powershell
python manage.py migrate
```

### Paso 3: Crear Datos de Prueba (opcional)
```powershell
python manage.py crear_datos_demo
```

### Paso 4: Iniciar el Servidor
```powershell
python manage.py runserver
```

### Paso 5: Acceder a la API
- **Navegador de API**: http://localhost:8000/api/
- **Info del proyecto**: http://localhost:8000/api/info/
- **Admin Django**: http://localhost:8000/admin/

## 🧪 CÓMO PROBAR

### Opción 1: Navegador (Más Fácil)
Abre en tu navegador: `http://localhost:8000/api/`

Verás una interfaz interactiva donde puedes:
- Ver todos los endpoints
- Hacer peticiones GET/POST/PUT/DELETE
- Ver las respuestas en tiempo real

### Opción 2: Script Automático
```powershell
cd monitoreo
python test_api.py
```

### Opción 3: PowerShell/curl
```powershell
# Listar dispositivos
Invoke-WebRequest -Uri "http://localhost:8000/api/dispositivos/" | Select-Object -Expand Content

# Ver estadísticas
Invoke-WebRequest -Uri "http://localhost:8000/api/mediciones/estadisticas_generales/" | Select-Object -Expand Content

# Crear medición
$body = @{
    dispositivo = 1
    consumo = 15.5
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/mediciones/" -Method POST -Body $body -ContentType "application/json"
```

## 📊 ENDPOINTS PRINCIPALES

### CRUD Completo (5 recursos):
1. **Dispositivos**: `/api/dispositivos/`
2. **Mediciones**: `/api/mediciones/`
3. **Alertas**: `/api/alertas/`
4. **Zonas**: `/api/zonas/`
5. **Organizaciones**: `/api/organizaciones/` (solo lectura)

### Endpoints Personalizados (12+):
- `/api/dispositivos/{id}/consumo_total/`
- `/api/dispositivos/{id}/mediciones/`
- `/api/dispositivos/{id}/alertas/`
- `/api/dispositivos/por_categoria/`
- `/api/zonas/{id}/dispositivos/`
- `/api/zonas/{id}/estadisticas/`
- `/api/mediciones/estadisticas_generales/`
- `/api/alertas/criticas/`
- `/api/alertas/por_gravedad/`
- `/api/organizaciones/{id}/zonas/`
- `/api/organizaciones/{id}/resumen/`

## ✨ FUNCIONALIDADES IMPLEMENTADAS

### ✅ Operaciones CRUD
- CREATE (POST): Crear nuevos recursos
- READ (GET): Listar y ver detalles
- UPDATE (PUT/PATCH): Actualizar completo o parcial
- DELETE: Eliminar recursos

### ✅ Filtros y Búsquedas
- Filtrar por categoría, zona, organización
- Filtrar por rango de fechas
- Filtrar por gravedad de alertas
- Búsqueda de texto en múltiples campos

### ✅ Paginación
- 10 elementos por página automáticamente
- Navegación next/previous

### ✅ Validaciones
- Validación de datos en serializers
- Mensajes de error descriptivos
- Validación de valores negativos
- Validación de longitud mínima

### ✅ Estadísticas
- Consumo total por dispositivo
- Estadísticas por zona
- Agrupación por categoría
- Conteo de alertas graves

### ✅ Relaciones
- Datos relacionados en respuestas
- Nombres de zona y organización incluidos
- Mediciones y alertas recientes

## 📝 EJEMPLOS DE USO

### Ver Todos los Dispositivos
GET http://localhost:8000/api/dispositivos/

### Ver un Dispositivo Específico con Detalles
GET http://localhost:8000/api/dispositivos/1/

### Crear una Nueva Medición
POST http://localhost:8000/api/mediciones/
```json
{
  "dispositivo": 1,
  "consumo": 12.5
}
```

### Crear una Alerta
POST http://localhost:8000/api/alertas/
```json
{
  "dispositivo": 1,
  "mensaje": "Consumo excesivo detectado",
  "gravedad": "Alta"
}
```

### Ver Estadísticas de una Zona
GET http://localhost:8000/api/zonas/1/estadisticas/

### Filtrar Alertas Graves
GET http://localhost:8000/api/alertas/?gravedad=Grave

## 🎓 CUMPLIMIENTO DE REQUISITOS

✅ **API REST completa con Django REST Framework**
✅ **Serializers para todos los modelos**
✅ **ViewSets con operaciones CRUD**
✅ **Endpoints personalizados con lógica de negocio**
✅ **Filtros y búsquedas avanzadas**
✅ **Validaciones completas**
✅ **Paginación automática**
✅ **Documentación detallada**
✅ **Scripts de prueba**
✅ **Configuración en settings.py**
✅ **URLs correctamente configuradas**

## 📚 DOCUMENTACIÓN ADICIONAL

- **API_DOCUMENTATION.md**: Documentación completa de todos los endpoints
- **monitoreo/README_API.md**: Guía de instalación y uso
- **Browsable API**: Interfaz interactiva en http://localhost:8000/api/

## 🏆 RESULTADO

API REST profesional, completa y funcional lista para usar en producción o evaluación.

---
**Desarrollado por**: Matias
**Fecha**: Diciembre 2024
**Proyecto**: EcoEnergy Monitoring System
