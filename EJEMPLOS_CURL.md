# 🧪 Ejemplos CURL - API RRHH

## Base URL
```
http://13.221.112.151:8000/api/rrhh
```

---

## 📁 DEPARTAMENTOS

### Listar todos los departamentos
```bash
curl -X GET "http://13.221.112.151:8000/api/rrhh/departamentos/" \
  -H "Content-Type: application/json"
```

### Crear un nuevo departamento
```bash
curl -X POST "http://13.221.112.151:8000/api/rrhh/departamentos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Departamento IT",
    "descripcion": "Departamento de Tecnología e Infraestructura",
    "responsable": "Carlos Rodriguez"
  }'
```

### Obtener departamento por ID
```bash
curl -X GET "http://13.221.112.151:8000/api/rrhh/departamentos/1/" \
  -H "Content-Type: application/json"
```

### Actualizar departamento (PUT)
```bash
curl -X PUT "http://13.221.112.151:8000/api/rrhh/departamentos/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Departamento IT Actualizado",
    "descripcion": "Departamento de Tecnología - Actualizado",
    "responsable": "Carlos Rodriguez"
  }'
```

### Actualizar parcialmente (PATCH)
```bash
curl -X PATCH "http://13.221.112.151:8000/api/rrhh/departamentos/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Departamento IT - Nuevo Nombre"
  }'
```

### Eliminar departamento
```bash
curl -X DELETE "http://13.221.112.151:8000/api/rrhh/departamentos/1/" \
  -H "Content-Type: application/json"
```

---

## 👥 EMPLEADOS

### Listar todos los empleados
```bash
curl -X GET "http://13.221.112.151:8000/api/rrhh/empleados/" \
  -H "Content-Type: application/json"
```

### Crear un nuevo empleado
```bash
curl -X POST "http://13.221.112.151:8000/api/rrhh/empleados/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Pedro",
    "apellido": "González",
    "email": "pedro.gonzalez@empresa.com",
    "telefono": "555-6789",
    "puesto": "Senior Developer",
    "departamento": 1,
    "proyecto": 1
  }'
```

### Obtener empleado por ID
```bash
curl -X GET "http://13.221.112.151:8000/api/rrhh/empleados/1/" \
  -H "Content-Type: application/json"
```

### Actualizar empleado (PUT)
```bash
curl -X PUT "http://13.221.112.151:8000/api/rrhh/empleados/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido": "García Actualizado",
    "email": "juan.garcia@empresa.com",
    "telefono": "555-1111",
    "puesto": "Lead Developer",
    "departamento": 1,
    "proyecto": 1
  }'
```

### Actualizar parcialmente (PATCH)
```bash
curl -X PATCH "http://13.221.112.151:8000/api/rrhh/empleados/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "puesto": "Senior Lead Developer",
    "telefono": "555-9999"
  }'
```

### Eliminar empleado
```bash
curl -X DELETE "http://13.221.112.151:8000/api/rrhh/empleados/1/" \
  -H "Content-Type: application/json"
```

---

## 🚀 PROYECTOS

### Listar todos los proyectos
```bash
curl -X GET "http://13.221.112.151:8000/api/rrhh/proyectos/" \
  -H "Content-Type: application/json"
```

### Crear un nuevo proyecto
```bash
curl -X POST "http://13.221.112.151:8000/api/rrhh/proyectos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Portal Cliente Web",
    "descripcion": "Desarrollo de portal web para clientes",
    "estado": "En Desarrollo",
    "fecha_inicio": "2025-01-15",
    "fecha_fin_estimada": "2025-06-30"
  }'
```

### Obtener proyecto por ID
```bash
curl -X GET "http://13.221.112.151:8000/api/rrhh/proyectos/1/" \
  -H "Content-Type: application/json"
```

### Actualizar proyecto (PUT)
```bash
curl -X PUT "http://13.221.112.151:8000/api/rrhh/proyectos/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Portal Cliente Web v2",
    "descripcion": "Desarrollo de portal web para clientes - Versión 2",
    "estado": "En Desarrollo",
    "fecha_inicio": "2025-01-15",
    "fecha_fin_estimada": "2025-07-31"
  }'
```

### Actualizar parcialmente (PATCH)
```bash
curl -X PATCH "http://13.221.112.151:8000/api/rrhh/proyectos/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "Completado",
    "fecha_fin_estimada": "2025-05-30"
  }'
```

### Eliminar proyecto
```bash
curl -X DELETE "http://13.221.112.151:8000/api/rrhh/proyectos/1/" \
  -H "Content-Type: application/json"
```

---

## ⏱️ REGISTROS DE TIEMPO

### Listar todos los registros de tiempo
```bash
curl -X GET "http://13.221.112.151:8000/api/rrhh/registros-tiempo/" \
  -H "Content-Type: application/json"
```

### Crear un nuevo registro de tiempo
```bash
curl -X POST "http://13.221.112.151:8000/api/rrhh/registros-tiempo/" \
  -H "Content-Type: application/json" \
  -d '{
    "empleado": 1,
    "proyecto": 1,
    "fecha": "2025-12-10",
    "horas": 8.5,
    "descripcion": "Desarrollo de funcionalidad de autenticación",
    "tipo_actividad": "Desarrollo"
  }'
```

### Obtener registro de tiempo por ID
```bash
curl -X GET "http://13.221.112.151:8000/api/rrhh/registros-tiempo/1/" \
  -H "Content-Type: application/json"
```

### Actualizar registro de tiempo (PUT)
```bash
curl -X PUT "http://13.221.112.151:8000/api/rrhh/registros-tiempo/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "empleado": 1,
    "proyecto": 1,
    "fecha": "2025-12-10",
    "horas": 9.0,
    "descripcion": "Desarrollo de funcionalidad de autenticación - Actualizado",
    "tipo_actividad": "Desarrollo"
  }'
```

### Actualizar parcialmente (PATCH)
```bash
curl -X PATCH "http://13.221.112.151:8000/api/rrhh/registros-tiempo/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "horas": 8.0,
    "descripcion": "Revisión de código y testing"
  }'
```

### Eliminar registro de tiempo
```bash
curl -X DELETE "http://13.221.112.151:8000/api/rrhh/registros-tiempo/1/" \
  -H "Content-Type: application/json"
```

---

## 🔍 Flujo Completo de Demostración

```bash
# 1. Ver datos existentes
curl -X GET "http://13.221.112.151:8000/api/rrhh/departamentos/" -H "Content-Type: application/json"

curl -X GET "http://13.221.112.151:8000/api/rrhh/empleados/" -H "Content-Type: application/json"

curl -X GET "http://13.221.112.151:8000/api/rrhh/proyectos/" -H "Content-Type: application/json"

curl -X GET "http://13.221.112.151:8000/api/rrhh/registros-tiempo/" -H "Content-Type: application/json"

# 2. Crear nuevo departamento
curl -X POST "http://13.221.112.151:8000/api/rrhh/departamentos/" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Soporte", "descripcion": "Equipo de soporte técnico", "responsable": "Ana"}'

# 3. Crear nuevo empleado
curl -X POST "http://13.221.112.151:8000/api/rrhh/empleados/" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Luis", "apellido": "Pérez", "email": "luis@empresa.com", "telefono": "555-1234", "puesto": "QA Engineer", "departamento": 1, "proyecto": 1}'

# 4. Crear registro de tiempo
curl -X POST "http://13.221.112.151:8000/api/rrhh/registros-tiempo/" \
  -H "Content-Type: application/json" \
  -d '{"empleado": 1, "proyecto": 1, "fecha": "2025-12-10", "horas": 7.5, "descripcion": "Testing del sistema", "tipo_actividad": "QA"}'

# 5. Editar parcialmente un empleado
curl -X PATCH "http://13.221.112.151:8000/api/rrhh/empleados/1/" \
  -H "Content-Type: application/json" \
  -d '{"puesto": "Senior QA Engineer"}'

# 6. Eliminar un registro
curl -X DELETE "http://13.221.112.151:8000/api/rrhh/registros-tiempo/1/" \
  -H "Content-Type: application/json"
```

---

## 📊 Códigos de Estado Esperados

- **200 OK**: GET exitoso, respuesta con datos
- **201 Created**: POST exitoso, recurso creado
- **204 No Content**: DELETE/PATCH exitoso, sin cuerpo de respuesta
- **400 Bad Request**: Error en validación de datos
- **404 Not Found**: Recurso no existe
- **500 Internal Server Error**: Error en el servidor

---

**¡Listo para probar tu API!** 🚀
