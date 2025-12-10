# 📋 Guía: Importar y Usar Colección Postman en ApiDog

## 1️⃣ Descargar la Colección

Ya tienes el archivo: `API_RRHH_Postman_Collection.json`

## 2️⃣ Importar en Postman

### Opción A: Desde la web (Postman online)
1. Ve a https://web.postman.co/ y loguéate
2. Click en **"Import"** (arriba a la izquierda)
3. Selecciona **"Upload Files"**
4. Carga el archivo `API_RRHH_Postman_Collection.json`
5. Click en **"Import"**

### Opción B: Desde Postman Desktop
1. Abre Postman
2. Click en **"File"** → **"Import"**
3. Selecciona el archivo `API_RRHH_Postman_Collection.json`
4. Click en **"Open"**

## 3️⃣ Importar en ApiDog

1. Ve a https://apidog.com/ y loguéate (o crea cuenta gratis)
2. Click en **"Import"** (botón verde)
3. Selecciona **"OpenAPI/Postman"**
4. Carga el archivo `API_RRHH_Postman_Collection.json`
5. Click en **"Import"**

## 4️⃣ Estructura de la Colección

La colección incluye **4 carpetas principales**:

### 📁 DEPARTAMENTOS
- `GET /departamentos/` → Listar todos
- `POST /departamentos/` → Crear uno nuevo
- `GET /departamentos/{id}/` → Obtener por ID
- `PUT /departamentos/{id}/` → Actualizar completamente
- `PATCH /departamentos/{id}/` → Actualizar parcialmente
- `DELETE /departamentos/{id}/` → Eliminar

### 👥 EMPLEADOS
- `GET /empleados/` → Listar todos (actualmente 5)
- `POST /empleados/` → Crear nuevo
- `GET /empleados/{id}/` → Obtener por ID
- `PUT /empleados/{id}/` → Actualizar completamente
- `PATCH /empleados/{id}/` → Actualizar parcialmente
- `DELETE /empleados/{id}/` → Eliminar

### 🚀 PROYECTOS
- `GET /proyectos/` → Listar todos (actualmente 3)
- `POST /proyectos/` → Crear nuevo
- `GET /proyectos/{id}/` → Obtener por ID
- `PUT /proyectos/{id}/` → Actualizar completamente
- `PATCH /proyectos/{id}/` → Actualizar parcialmente
- `DELETE /proyectos/{id}/` → Eliminar

### ⏱️ REGISTROS DE TIEMPO
- `GET /registros-tiempo/` → Listar todos (actualmente 180)
- `POST /registros-tiempo/` → Crear nuevo registro
- `GET /registros-tiempo/{id}/` → Obtener por ID
- `PUT /registros-tiempo/{id}/` → Actualizar completamente
- `PATCH /registros-tiempo/{id}/` → Actualizar parcialmente
- `DELETE /registros-tiempo/{id}/` → Eliminar

## 5️⃣ URL Base (Variable de Entorno)

**Está preconfigurada automáticamente:**
```
baseUrl = http://98.88.189.220:8000/api/rrhh
```

Todos los requests la usan como `{{baseUrl}}`, así que puedes cambiarla de una vez.

## 6️⃣ Flujo de Demostración Sugerido

### Paso 1: Verificar datos existentes
```
GET /departamentos/
GET /empleados/
GET /proyectos/
GET /registros-tiempo/
```

### Paso 2: Crear un nuevo departamento
```
POST /departamentos/
Body:
{
  "nombre": "Departamento IT",
  "descripcion": "Departamento de Tecnología",
  "responsable": "Carlos Rodriguez"
}
```

### Paso 3: Crear un nuevo empleado
```
POST /empleados/
Body:
{
  "nombre": "Pedro",
  "apellido": "González",
  "email": "pedro@empresa.com",
  "telefono": "555-6789",
  "puesto": "Developer",
  "departamento": 1,
  "proyecto": 1
}
```

### Paso 4: Crear un registro de tiempo
```
POST /registros-tiempo/
Body:
{
  "empleado": 1,
  "proyecto": 1,
  "fecha": "2025-12-10",
  "horas": 8.5,
  "descripcion": "Desarrollo de funcionalidades",
  "tipo_actividad": "Desarrollo"
}
```

### Paso 5: Actualizar un empleado
```
PATCH /empleados/1/
Body:
{
  "puesto": "Senior Developer",
  "telefono": "555-9999"
}
```

### Paso 6: Eliminar un registro
```
DELETE /registros-tiempo/1/
```

## 7️⃣ Respuestas Esperadas

### GET exitoso (200 OK)
```json
{
  "id": 1,
  "nombre": "Juan García",
  "apellido": "García",
  "email": "juan@empresa.com",
  ...
}
```

### POST exitoso (201 Created)
```json
{
  "id": 6,
  "nombre": "Pedro",
  "apellido": "González",
  "email": "pedro@empresa.com",
  ...
}
```

### DELETE exitoso (204 No Content)
Sin cuerpo de respuesta.

### Error (400 Bad Request)
```json
{
  "email": ["Esta dirección de correo ya está en uso."],
  "nombre": ["Este campo es obligatorio."]
}
```

## 8️⃣ Notas Importantes

- **Autenticación**: NO hay autenticación configurada actualmente. Los endpoints están abiertos.
- **Headers automáticos**: `Content-Type: application/json` se envía automáticamente en POST/PUT/PATCH.
- **IDs válidos**: 
  - Departamentos: 1-4
  - Empleados: 1-5
  - Proyectos: 1-3
  - Registros: 1-180 (inicialmente)
- **Campos requeridos en POST**:
  - Departamentos: `nombre`
  - Empleados: `nombre`, `apellido`, `email`, `departamento`
  - Proyectos: `nombre`, `estado`
  - Registros: `empleado`, `proyecto`, `fecha`, `horas`

## 9️⃣ Troubleshooting

### Error: "Connection refused"
- Verifica que el servidor EC2 está corriendo en AWS
- Confirma la IP: `13.221.112.151`
- Comprueba que el puerto 8000 está abierto en el Security Group

### Error: 404 Not Found
- Verifica que el ID existe (por ejemplo, empleado con ID 10 podría no existir)
- Usa GET para listar todos antes de hacer PUT/DELETE

### Error: 400 Bad Request
- Valida el JSON del body (brackets, comillas, etc.)
- Asegúrate de enviar todos los campos requeridos en POST

## 🔟 Exportar Resultados

En Postman/ApiDog puedes:
1. Hacer screenshots de los requests y respuestas
2. Exportar colección con resultados (generate report)
3. Guardar ejemplos de requests/responses para tu presentación

---

**¡Listo para demostrar tu API RRHH completamente funcional!** 🚀
