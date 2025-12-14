# Pruebas en Postman/Apidog

## 1. Obtener Token JWT

**Método**: POST  
**URL**: http://98.88.189.220/api/token/  
**Body** (JSON):
```json
{
    "username": "admin",
    "password": "tu-password"
}
```

**Respuesta Esperada** (201):
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Copiar el valor de `access` para usarlo en las siguientes pruebas.

---

## 2. Consultar Info de la API

**Método**: GET  
**URL**: http://98.88.189.220/api/info/  
**Headers**: Sin autenticación necesaria

**Respuesta Esperada** (200):
```json
{
    "autor": ["Tu Nombre Completo"],
    "asignatura": "Programación Back End",
    "proyecto": "SmartConnect - Sistema de Control de Acceso Inteligente",
    "descripcion": "API RESTful para gestionar sensores RFID...",
    "version": "1.0"
}
```

---

## 3. Crear Departamento (CRUD - CREATE)

**Método**: POST  
**URL**: http://98.88.189.220/api/departamentos/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
Content-Type: application/json
```

**Body**:
```json
{
    "nombre": "Recepción",
    "descripcion": "Área de recepción principal",
    "ubicacion": "Piso 1",
    "activo": true
}
```

**Respuesta Esperada** (201):
```json
{
    "id": 1,
    "nombre": "Recepción",
    "descripcion": "Área de recepción principal",
    "ubicacion": "Piso 1",
    "activo": true,
    "creado_en": "2024-12-14T10:30:00Z",
    "actualizado_en": "2024-12-14T10:30:00Z",
    "sensores_count": 0
}
```

---

## 4. Listar Departamentos (CRUD - READ)

**Método**: GET  
**URL**: http://98.88.189.220/api/departamentos/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
```

**Respuesta Esperada** (200):
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "nombre": "Recepción",
            "descripcion": "Área de recepción principal",
            "ubicacion": "Piso 1",
            "activo": true,
            "creado_en": "2024-12-14T10:30:00Z",
            "actualizado_en": "2024-12-14T10:30:00Z",
            "sensores_count": 0
        }
    ]
}
```

---

## 5. Obtener Detalle de Departamento (CRUD - READ Detail)

**Método**: GET  
**URL**: http://98.88.189.220/api/departamentos/1/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
```

**Respuesta Esperada** (200):
```json
{
    "id": 1,
    "nombre": "Recepción",
    "descripcion": "Área de recepción principal",
    "ubicacion": "Piso 1",
    "activo": true,
    "creado_en": "2024-12-14T10:30:00Z",
    "actualizado_en": "2024-12-14T10:30:00Z",
    "sensores_count": 0
}
```

---

## 6. Actualizar Departamento (CRUD - UPDATE)

**Método**: PUT  
**URL**: http://98.88.189.220/api/departamentos/1/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
Content-Type: application/json
```

**Body**:
```json
{
    "nombre": "Recepción Principal",
    "descripcion": "Área de recepción principal del edificio",
    "ubicacion": "Piso 1 - Entrada",
    "activo": true
}
```

**Respuesta Esperada** (200):
```json
{
    "id": 1,
    "nombre": "Recepción Principal",
    "descripcion": "Área de recepción principal del edificio",
    "ubicacion": "Piso 1 - Entrada",
    "activo": true,
    "creado_en": "2024-12-14T10:30:00Z",
    "actualizado_en": "2024-12-14T10:35:00Z",
    "sensores_count": 0
}
```

---

## 7. Eliminar Departamento (CRUD - DELETE)

**Método**: DELETE  
**URL**: http://98.88.189.220/api/departamentos/1/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
```

**Respuesta Esperada** (204): Sin contenido

---

## 8. Crear Sensor (CRUD - CREATE)

Primero crear un departamento si no existe:

**Método**: POST  
**URL**: http://98.88.189.220/api/sensores/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
Content-Type: application/json
```

**Body**:
```json
{
    "uid": "UID-001-ABC",
    "nombre": "Tarjeta Juan",
    "tipo": "tarjeta",
    "estado": "activo",
    "usuario_asignado": 1,
    "departamento": 1
}
```

**Respuesta Esperada** (201):
```json
{
    "id": 1,
    "uid": "UID-001-ABC",
    "nombre": "Tarjeta Juan",
    "tipo": "tarjeta",
    "estado": "activo",
    "usuario_asignado": 1,
    "usuario_asignado_username": "juan",
    "departamento": 1,
    "departamento_nombre": "Recepción",
    "creado_en": "2024-12-14T10:45:00Z",
    "actualizado_en": "2024-12-14T10:45:00Z"
}
```

---

## 9. Registrar Acceso con Sensor

**Método**: POST  
**URL**: http://98.88.189.220/api/sensores/registrar_acceso/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
Content-Type: application/json
```

**Body**:
```json
{
    "uid": "UID-001-ABC",
    "departamento_id": 1
}
```

**Respuesta Esperada** (200):
```json
{
    "mensaje": "Acceso permitido",
    "sensor": {
        "id": 1,
        "uid": "UID-001-ABC",
        "nombre": "Tarjeta Juan",
        "tipo": "tarjeta",
        "estado": "activo",
        "usuario_asignado": 1,
        "usuario_asignado_username": "juan",
        "departamento": 1,
        "departamento_nombre": "Recepción",
        "creado_en": "2024-12-14T10:45:00Z",
        "actualizado_en": "2024-12-14T10:45:00Z"
    },
    "evento_id": 1
}
```

---

## 10. Registrar Acceso Denegado (Sensor Bloqueado)

**Método**: POST  
**URL**: http://98.88.189.220/api/sensores/registrar_acceso/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
Content-Type: application/json
```

**Body**:
```json
{
    "uid": "UID-BLOQUEADA",
    "departamento_id": 1
}
```

Primero debes actualizar el sensor para establecer estado bloqueado:

**Método**: PATCH  
**URL**: http://98.88.189.220/api/sensores/1/  
**Body**:
```json
{
    "estado": "bloqueado"
}
```

**Respuesta Esperada** (403):
```json
{
    "error": "Acceso denegado. Sensor bloqueado."
}
```

---

## 11. Bloquear Sensor (Acción Custom)

**Método**: POST  
**URL**: http://98.88.189.220/api/sensores/1/bloquear/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
```

**Respuesta Esperada** (200):
```json
{
    "mensaje": "Sensor bloqueado"
}
```

---

## 12. Marcar Sensor como Perdido

**Método**: POST  
**URL**: http://98.88.189.220/api/sensores/1/marcar_perdido/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
```

**Respuesta Esperada** (200):
```json
{
    "mensaje": "Sensor marcado como perdido"
}
```

---

## 13. Crear Barrera

**Método**: POST  
**URL**: http://98.88.189.220/api/barreras/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
Content-Type: application/json
```

**Body**:
```json
{
    "nombre": "Barrera Entrada",
    "departamento": 1,
    "estado": "cerrada"
}
```

**Respuesta Esperada** (201):
```json
{
    "id": 1,
    "nombre": "Barrera Entrada",
    "departamento": 1,
    "departamento_nombre": "Recepción",
    "estado": "cerrada",
    "modo_manual": false,
    "creado_en": "2024-12-14T10:50:00Z",
    "actualizado_en": "2024-12-14T10:50:00Z"
}
```

---

## 14. Abrir Barrera Manualmente

**Método**: POST  
**URL**: http://98.88.189.220/api/barreras/1/abrir/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
```

**Respuesta Esperada** (200):
```json
{
    "mensaje": "Barrera abierta",
    "estado": "abierta"
}
```

---

## 15. Cerrar Barrera Manualmente

**Método**: POST  
**URL**: http://98.88.189.220/api/barreras/1/cerrar/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
```

**Respuesta Esperada** (200):
```json
{
    "mensaje": "Barrera cerrada",
    "estado": "cerrada"
}
```

---

## 16. Listar Eventos

**Método**: GET  
**URL**: http://98.88.189.220/api/eventos/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
```

**Respuesta Esperada** (200):
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "sensor": 1,
            "sensor_nombre": "Tarjeta Juan",
            "departamento": 1,
            "departamento_nombre": "Recepción",
            "tipo": "barrera_abierta",
            "resultado": "permitido",
            "descripcion": "Barrera abierta manualmente",
            "usuario": 1,
            "usuario_username": "admin",
            "creado_en": "2024-12-14T10:52:00Z"
        },
        {
            "id": 2,
            "sensor": 1,
            "sensor_nombre": "Tarjeta Juan",
            "departamento": 1,
            "departamento_nombre": "Recepción",
            "tipo": "acceso_permitido",
            "resultado": "permitido",
            "descripcion": "Acceso permitido",
            "usuario": 1,
            "usuario_username": "juan",
            "creado_en": "2024-12-14T10:47:00Z"
        },
        {
            "id": 1,
            "sensor": 1,
            "sensor_nombre": "Tarjeta Juan",
            "departamento": 1,
            "departamento_nombre": "Recepción",
            "tipo": "acceso_intento",
            "resultado": null,
            "descripcion": null,
            "usuario": null,
            "usuario_username": null,
            "creado_en": "2024-12-14T10:45:00Z"
        }
    ]
}
```

---

## 17. Test Sin Token (Debe fallar)

**Método**: GET  
**URL**: http://98.88.189.220/api/departamentos/  
**Headers**: Ninguno

**Respuesta Esperada** (401):
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## 18. Test sin Permisos (Usuario no Admin)

Crear un usuario normal (no es_staff):

**Método**: POST  
**URL**: http://98.88.189.220/api/departamentos/  
**Headers**: 
```
Authorization: Bearer <token-usuario-normal>
Content-Type: application/json
```

**Body**:
```json
{
    "nombre": "Test",
    "activo": true
}
```

**Respuesta Esperada** (403):
```json
{
    "detail": "You do not have permission to perform this action."
}
```

---

## 19. Listar Últimos Eventos

**Método**: GET  
**URL**: http://98.88.189.220/api/eventos/ultimos/  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
```

**Respuesta Esperada** (200): Lista de últimos 10 eventos

---

## 20. Obtener Eventos por Sensor

**Método**: GET  
**URL**: http://98.88.189.220/api/eventos/por_sensor/?sensor_id=1  
**Headers**: 
```
Authorization: Bearer <tu-token-access>
```

**Respuesta Esperada** (200): Lista de eventos del sensor especificado

---

## Errores Comunes

| Código | Significado | Solución |
|--------|-------------|----------|
| 400 | Bad Request | Validar JSON y datos requeridos |
| 401 | Unauthorized | Token inválido o expirado, obtener nuevo token |
| 403 | Forbidden | Usuario no tiene permisos, debe ser admin |
| 404 | Not Found | Recurso no existe |
| 500 | Server Error | Revisar logs del servidor |

---

## Tips de Testing

1. Siempre incluir el header `Authorization: Bearer <token>`
2. El token expira en 1 hora, usar `/api/token/refresh/` para renovar
3. Guardar valores de respuesta para usarlos en siguientes pruebas
4. Validar códigos HTTP esperados
5. Probar casos de error (UID duplicado, nombre vacío, etc.)
