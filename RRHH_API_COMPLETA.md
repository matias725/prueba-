# 📊 API REST de Gestión de Recursos Humanos - v2.0

## 🎯 Descripción General

Sistema profesional de gestión de Recursos Humanos implementado con **Django REST Framework**. Incluye:

- ✅ **4 Modelos completos**: Departamentos, Empleados, Proyectos, Registros de Tiempo
- ✅ **CRUD completo** en todos los modelos
- ✅ **20+ Endpoints** con funcionalidades avanzadas
- ✅ **Filtros, búsquedas y ordenamiento** en todos los recursos
- ✅ **Validaciones personalizadas** de negocio
- ✅ **Dashboard con estadísticas** en tiempo real
- ✅ **Relaciones anidadas** entre modelos
- ✅ **Documentación interactiva** (Browsable API)

---

## 📁 Estructura de la API

```
/api/rrhh/
├── departamentos/              # Gestión de departamentos
├── empleados/                  # Gestión de empleados
├── proyectos/                  # Gestión de proyectos
├── registros-tiempo/           # Gestión de registros de tiempo
└── dashboard/                  # Estadísticas y métricas
```

---

## 🔌 Endpoints Principales

### 1️⃣ DEPARTAMENTOS

#### Listar todos
```
GET /api/rrhh/departamentos/
Parámetros: ?activo=true&search=Desarrollo&ordering=nombre
```

#### Ver detalles
```
GET /api/rrhh/departamentos/{id}/
```

#### Crear departamento
```
POST /api/rrhh/departamentos/
{
  "nombre": "Desarrollo",
  "descripcion": "Equipo de desarrollo",
  "gerente": 1,
  "presupuesto": 50000,
  "activo": true
}
```

#### Actualizar
```
PUT /api/rrhh/departamentos/{id}/
PATCH /api/rrhh/departamentos/{id}/
```

#### Eliminar
```
DELETE /api/rrhh/departamentos/{id}/
```

#### 🔗 Endpoints relacionados
```
GET /api/rrhh/departamentos/{id}/empleados/      # Empleados del departamento
GET /api/rrhh/departamentos/{id}/proyectos/      # Proyectos del departamento
GET /api/rrhh/departamentos/{id}/estadisticas/   # Estadísticas detalladas
```

---

### 2️⃣ EMPLEADOS

#### Listar todos
```
GET /api/rrhh/empleados/
Parámetros: ?estado=activo&departamento=1&search=Juan&ordering=user__first_name
```

#### Ver detalle completo (incluye registros recientes)
```
GET /api/rrhh/empleados/{id}/
```

#### Crear empleado
```
POST /api/rrhh/empleados/
{
  "user": 1,
  "numero_empleado": "001",
  "puesto": "Desarrollador Senior",
  "departamento": 1,
  "salario": 35000,
  "fecha_contratacion": "2022-01-15",
  "telefono": "555-1234",
  "direccion": "Calle Principal 123"
}
```

#### Actualizar empleado
```
PUT /api/rrhh/empleados/{id}/
PATCH /api/rrhh/empleados/{id}/
```

#### Eliminar empleado
```
DELETE /api/rrhh/empleados/{id}/
```

#### 🔗 Endpoints relacionados
```
GET /api/rrhh/empleados/{id}/registros_tiempo/   # Registros de tiempo
GET /api/rrhh/empleados/{id}/estadisticas/       # Estadísticas de trabajo
GET /api/rrhh/empleados/por_departamento/        # Agrupación por departamento
```

---

### 3️⃣ PROYECTOS

#### Listar todos
```
GET /api/rrhh/proyectos/
Parámetros: ?estado=en_progreso&departamento=1&ordering=-fecha_creacion
```

#### Ver detalle completo (incluye empleados y registros)
```
GET /api/rrhh/proyectos/{id}/
```

#### Crear proyecto
```
POST /api/rrhh/proyectos/
{
  "nombre": "Sistema de Inventario",
  "descripcion": "Desarrollo de sistema web",
  "departamento": 1,
  "gerente_proyecto": 1,
  "estado": "en_progreso",
  "presupuesto": 50000,
  "fecha_inicio": "2025-01-01",
  "fecha_fin_estimada": "2025-06-30",
  "porcentaje_completado": 45
}
```

#### Actualizar proyecto
```
PUT /api/rrhh/proyectos/{id}/
PATCH /api/rrhh/proyectos/{id}/
```

#### Eliminar proyecto
```
DELETE /api/rrhh/proyectos/{id}/
```

#### 🔗 Endpoints relacionados
```
GET /api/rrhh/proyectos/{id}/registros_tiempo/   # Registros del proyecto
GET /api/rrhh/proyectos/{id}/estadisticas/       # Estadísticas del proyecto
GET /api/rrhh/proyectos/por_estado/              # Agrupación por estado
GET /api/rrhh/proyectos/criticos/                # Proyectos en riesgo
```

---

### 4️⃣ REGISTROS DE TIEMPO

#### Listar todos
```
GET /api/rrhh/registros-tiempo/
Parámetros: ?empleado=1&proyecto=1&validado=true&fecha_desde=2025-01-01
```

#### Ver detalle
```
GET /api/rrhh/registros-tiempo/{id}/
```

#### Crear registro
```
POST /api/rrhh/registros-tiempo/
{
  "empleado": 1,
  "proyecto": 1,
  "fecha": "2025-01-15",
  "horas": 8,
  "descripcion": "Desarrollo de módulo de usuarios",
  "validado": false
}
```

#### Actualizar registro
```
PUT /api/rrhh/registros-tiempo/{id}/
PATCH /api/rrhh/registros-tiempo/{id}/
```

#### Eliminar registro
```
DELETE /api/rrhh/registros-tiempo/{id}/
```

#### 🔗 Endpoints relacionados
```
GET /api/rrhh/registros-tiempo/estadisticas_generales/  # Stats globales
POST /api/rrhh/registros-tiempo/validar_registros/      # Validar múltiples
```

---

### 5️⃣ DASHBOARD

#### Información del proyecto
```
GET /api/rrhh/dashboard/info/

Respuesta:
{
  "proyecto": "Sistema de Gestión de Recursos Humanos",
  "version": "2.0",
  "autor": "Matias",
  "descripcion": "API REST profesional para gestión de RRHH",
  "modulos": ["Departamentos", "Empleados", "Proyectos", "Registros de Tiempo"],
  "estado": "Operativo"
}
```

#### Dashboard general
```
GET /api/rrhh/dashboard/general/

Respuesta:
{
  "total_empleados": 8,
  "total_proyectos": 5,
  "total_horas_registradas": 1250.75,
  "presupuesto_total": 190000.00,
  "proyectos_en_riesgo": 2,
  "empleados_por_departamento": [...],
  "proyectos_por_estado": [...],
  "registros_no_validados": 45
}
```

---

## 🎓 Características Avanzadas

### ✨ Validaciones Automáticas

- Salario no puede ser negativo
- Horas de trabajo máx 24 por día
- Fechas no pueden ser en el futuro
- Presupuesto no puede ser negativo
- Unicidad de registros (empleado + proyecto + fecha)
- Fecha de inicio anterior a fecha fin

### 📊 Campos Calculados (Solo Lectura)

**Empleado:**
- `antiguedad_meses`: Meses desde contratación
- `dias_trabajados`: Días desde contratación
- `total_horas_mes`: Total de horas trabajadas en el mes actual

**Proyecto:**
- `dias_para_vencer`: Días restantes hasta fecha estimada
- `total_horas_registradas`: Total de horas registradas
- `estado_display`: Estado en formato legible

**RegistroTiempo:**
- `costo_hora`: Costo aproximado basado en salario del empleado

### 🔍 Búsquedas y Filtros

**Departamentos:**
- Búsqueda: nombre, descripción
- Filtro: activo (true/false)

**Empleados:**
- Búsqueda: nombre, número de empleado
- Filtros: estado, departamento

**Proyectos:**
- Búsqueda: nombre, descripción
- Filtros: estado, departamento

**Registros:**
- Filtros: empleado, proyecto, fecha_desde, fecha_hasta, validado

---

## 📋 Ejemplos Completos

### Crear un empleado nuevo

```bash
# 1. Primero crear usuario (en /admin/)
# 2. Luego crear empleado
curl -X POST http://localhost:8000/api/rrhh/empleados/ \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "numero_empleado": "009",
    "puesto": "Desarrollador",
    "departamento": 1,
    "salario": 28000,
    "fecha_contratacion": "2024-01-15",
    "telefono": "555-9999",
    "direccion": "Calle Nueva 456"
  }'
```

### Registrar tiempo de trabajo

```bash
curl -X POST http://localhost:8000/api/rrhh/registros-tiempo/ \
  -H "Content-Type: application/json" \
  -d '{
    "empleado": 1,
    "proyecto": 1,
    "fecha": "2025-01-15",
    "horas": 8.5,
    "descripcion": "Desarrollo de API REST",
    "validado": false
  }'
```

### Obtener estadísticas de empleado

```bash
curl http://localhost:8000/api/rrhh/empleados/1/estadisticas/
```

### Validar múltiples registros

```bash
curl -X POST http://localhost:8000/api/rrhh/registros-tiempo/validar_registros/ \
  -H "Content-Type: application/json" \
  -d '{
    "ids": [1, 2, 3, 4, 5]
  }'
```

---

## 🚀 Instalación Rápida

### 1. Crear migraciones
```bash
python manage.py makemigrations rrhh
python manage.py migrate
```

### 2. Cargar datos de prueba
```bash
python crear_datos_rrhh.py
```

### 3. Iniciar servidor
```bash
python manage.py runserver
```

### 4. Acceder a la API
- **Navegador**: http://localhost:8000/api/rrhh/
- **Admin**: http://localhost:8000/admin/

---

## 📊 Modelos de Datos

### Departamento
- `id`: PK
- `nombre`: CharField (único)
- `descripcion`: TextField
- `gerente`: FK a User
- `presupuesto`: DecimalField
- `activo`: BooleanField
- `fecha_creacion`: DateTime (auto)

### Empleado
- `id`: PK
- `user`: OneToOne a User
- `departamento`: FK a Departamento
- `numero_empleado`: CharField (único)
- `puesto`: CharField
- `salario`: DecimalField
- `estado`: Choice (activo, inactivo, licencia, despedido)
- `fecha_contratacion`: DateField
- `telefono`: CharField
- `direccion`: CharField
- `fecha_creacion`: DateTime (auto)

### Proyecto
- `id`: PK
- `nombre`: CharField
- `descripcion`: TextField
- `departamento`: FK a Departamento
- `gerente_proyecto`: FK a Empleado
- `estado`: Choice (planificación, en progreso, pausado, completado, cancelado)
- `presupuesto`: DecimalField
- `fecha_inicio`: DateField
- `fecha_fin_estimada`: DateField
- `fecha_fin_real`: DateField (nullable)
- `porcentaje_completado`: IntegerField (0-100)
- `fecha_creacion`: DateTime (auto)

### RegistroTiempo
- `id`: PK
- `empleado`: FK a Empleado
- `proyecto`: FK a Proyecto
- `fecha`: DateField
- `horas`: DecimalField
- `descripcion`: TextField
- `validado`: BooleanField
- `fecha_creacion`: DateTime (auto)
- `unique_together`: (empleado, proyecto, fecha)

---

## 🔐 Seguridad

- Validaciones en todos los campos
- Permisos granulares (lista de acceso)
- Contraseñas no se devuelven en la API
- HTTPS recomendado en producción
- CORS configurado según necesidades

---

## 📈 Rendimiento

- Selección de campos relacionados (`select_related`, `prefetch_related`)
- Paginación automática
- Índices en campos de búsqueda
- Caching posible en estadísticas

---

## 🐛 Solución de Problemas

### Error: Modelo no existe
```bash
python manage.py makemigrations rrhh
python manage.py migrate
```

### Error: No se encuentra la app
Verifica que `'rrhh'` esté en `INSTALLED_APPS` en settings.py

### Error: Campos requeridos
Revisa la documentación del endpoint en esta guía

---

## 👨‍💻 Desarrollado por

**Matias** - Evaluación Sumativa Back End  
**Tecnologías**: Django, Django REST Framework, SQLite/MySQL  
**Fecha**: Diciembre 2024  
**Estado**: ✅ Producción-Ready

---

## 📞 Soporte

Para reportar problemas o sugerencias, contacta al desarrollador o revisa la documentación en `/api/rrhh/`

