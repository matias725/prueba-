# 📋 Guía de Pruebas - SmartConnect API

## Opción 1: Script Python (más fácil)

```bash
python3 test_smartconnect_api.py
```

Este script:
✓ Valida conexión al API
✓ Prueba login (admin y operador)
✓ Lista todos los recursos (usuarios, sensores, barreras, eventos, etc.)
✓ Prueba control manual de barreras
✓ Valida permisos por rol

---

## Opción 2: Postman (más detallado)

1. Abre Postman
2. **File** → **Import** → Selecciona `SmartConnect_API_Tests.postman_collection.json`
3. Ejecuta las pruebas en orden:

### Flujo recomendado:
1. **Info API** - Verifica que el API está vivo
2. **Login Admin** - Obtén token y cópialo en la variable `{{access_token}}`
3. **Listar Usuarios** - Confirma usuarios con roles
4. **Listar Sensores** - Valida sensores RFID
5. **Listar Barreras** - Verifica barreras creadas
6. **Listar Eventos** - Comprueba registro de eventos
7. **Control Barrera** - Abre/cierra manualmente

---

## Opción 3: cURL (línea por línea)

### 1. Info del API
```bash
curl http://98.88.189.220/api/smartconnect/info/
```

### 2. Login y obtener token
```bash
TOKEN=$(curl -s -X POST http://98.88.189.220/api/smartconnect/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | grep -o '"access":"[^"]*' | cut -d'"' -f4)

echo "Token: $TOKEN"
```

### 3. Listar sensores con token
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://98.88.189.220/api/smartconnect/sensores/
```

### 4. Listar usuarios
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://98.88.189.220/api/smartconnect/usuarios/
```

### 5. Listar barreras
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://98.88.189.220/api/smartconnect/barreras/
```

### 6. Listar eventos
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://98.88.189.220/api/smartconnect/eventos/
```

### 7. Control manual - Abrir barrera
```bash
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"accion": "abrir"}' \
  http://98.88.189.220/api/smartconnect/barreras/1/control/
```

### 8. Control manual - Cerrar barrera
```bash
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"accion": "cerrar"}' \
  http://98.88.189.220/api/smartconnect/barreras/1/control/
```

---

## Credenciales de Prueba

| Usuario | Contraseña | Rol | Permisos |
|---------|-----------|-----|----------|
| admin | admin123 | Admin | Acceso total |
| operador | operador123 | Operador | Ver sensores, control manual |
| empleado | empleado123 | Empleado | Solo lectura |

---

## Qué validar

✅ **Usuarios & Roles:**
- Existen 3 usuarios con roles diferentes
- Admin tiene acceso completo
- Operador solo puede controlar barreras
- Empleado tiene acceso limitado

✅ **Sensores RFID:**
- Al menos 4 sensores registrados
- Cada sensor tiene UID único
- Estados: activo, inactivo, etc.

✅ **Barreras:**
- Al menos 2 barreras creadas
- Control manual: abrir/cerrar funciona
- Estados se actualizan correctamente

✅ **Eventos:**
- Se registran eventos cuando se intenta acceso
- Incluye usuario, sensor, barrera, resultado

✅ **Departamentos:**
- Al menos 1 departamento definido
- Sensores vinculados a departamentos

---

## Respuesta esperada (ejemplo)

```json
{
  "id": 1,
  "uid": "5F3D42C1",
  "estado": "activo",
  "tipo": "tarjeta",
  "usuario": "admin",
  "departamento": "IT"
}
```
