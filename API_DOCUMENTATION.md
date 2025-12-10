# Documentación de la API REST - EcoEnergy

## Endpoints Disponibles

### Información del Proyecto
- **GET** `/api/info/` - Información básica del proyecto

### Organizaciones
- **GET** `/api/organizaciones/` - Listar organizaciones
- **GET** `/api/organizaciones/{id}/` - Detalle de organización
- **GET** `/api/organizaciones/{id}/zonas/` - Zonas de la organización
- **GET** `/api/organizaciones/{id}/resumen/` - Resumen completo con estadísticas

### Zonas
- **GET** `/api/zonas/` - Listar zonas
- **POST** `/api/zonas/` - Crear zona
- **GET** `/api/zonas/{id}/` - Detalle de zona
- **PUT** `/api/zonas/{id}/` - Actualizar zona completa
- **PATCH** `/api/zonas/{id}/` - Actualizar zona parcial
- **DELETE** `/api/zonas/{id}/` - Eliminar zona
- **GET** `/api/zonas/{id}/dispositivos/` - Dispositivos de la zona
- **GET** `/api/zonas/{id}/estadisticas/` - Estadísticas de la zona

**Parámetros de consulta:**
- `organizacion` - Filtrar por ID de organización
- `search` - Buscar por nombre
- `ordering` - Ordenar (nombre, id)

### Dispositivos
- **GET** `/api/dispositivos/` - Listar dispositivos
- **POST** `/api/dispositivos/` - Crear dispositivo
- **GET** `/api/dispositivos/{id}/` - Detalle completo del dispositivo
- **PUT** `/api/dispositivos/{id}/` - Actualizar dispositivo completo
- **PATCH** `/api/dispositivos/{id}/` - Actualizar dispositivo parcial
- **DELETE** `/api/dispositivos/{id}/` - Eliminar dispositivo
- **GET** `/api/dispositivos/{id}/mediciones/` - Mediciones del dispositivo
- **GET** `/api/dispositivos/{id}/alertas/` - Alertas del dispositivo
- **GET** `/api/dispositivos/{id}/consumo_total/` - Consumo total y estadísticas
- **GET** `/api/dispositivos/por_categoria/` - Agrupación por categoría

**Parámetros de consulta:**
- `categoria` - Filtrar por categoría (Sensor, Actuador, General)
- `zona` - Filtrar por ID de zona
- `watts_min` - Filtrar por watts mínimos
- `watts_max` - Filtrar por watts máximos
- `search` - Buscar por nombre o categoría
- `ordering` - Ordenar (nombre, categoria, watts, id)

### Mediciones
- **GET** `/api/mediciones/` - Listar mediciones
- **POST** `/api/mediciones/` - Crear medición
- **GET** `/api/mediciones/{id}/` - Detalle de medición
- **PUT** `/api/mediciones/{id}/` - Actualizar medición
- **PATCH** `/api/mediciones/{id}/` - Actualizar medición parcial
- **DELETE** `/api/mediciones/{id}/` - Eliminar medición
- **GET** `/api/mediciones/estadisticas_generales/` - Estadísticas globales

**Parámetros de consulta:**
- `dispositivo` - Filtrar por ID de dispositivo
- `zona` - Filtrar por ID de zona
- `fecha_desde` - Filtrar desde fecha (YYYY-MM-DD)
- `fecha_hasta` - Filtrar hasta fecha (YYYY-MM-DD)
- `ordering` - Ordenar (fecha, consumo)

### Alertas
- **GET** `/api/alertas/` - Listar alertas
- **POST** `/api/alertas/` - Crear alerta
- **GET** `/api/alertas/{id}/` - Detalle de alerta
- **PUT** `/api/alertas/{id}/` - Actualizar alerta
- **PATCH** `/api/alertas/{id}/` - Actualizar alerta parcial
- **DELETE** `/api/alertas/{id}/` - Eliminar alerta
- **GET** `/api/alertas/por_gravedad/` - Agrupación por gravedad
- **GET** `/api/alertas/criticas/` - Solo alertas graves

**Parámetros de consulta:**
- `dispositivo` - Filtrar por ID de dispositivo
- `zona` - Filtrar por ID de zona
- `gravedad` - Filtrar por gravedad (Grave, Alta, Media)
- `search` - Buscar en mensaje o gravedad
- `ordering` - Ordenar (fecha, gravedad)

## Ejemplos de Uso

### Crear un Dispositivo
```bash
curl -X POST http://localhost:8000/api/dispositivos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Sensor Temperatura",
    "categoria": "Sensor",
    "zona": 1,
    "watts": 5.5
  }'
```

### Crear una Medición
```bash
curl -X POST http://localhost:8000/api/mediciones/ \
  -H "Content-Type: application/json" \
  -d '{
    "dispositivo": 1,
    "consumo": 12.5
  }'
```

### Crear una Alerta
```bash
curl -X POST http://localhost:8000/api/alertas/ \
  -H "Content-Type: application/json" \
  -d '{
    "dispositivo": 1,
    "mensaje": "Consumo excesivo detectado en el dispositivo",
    "gravedad": "Alta"
  }'
```

### Obtener Estadísticas de una Zona
```bash
curl http://localhost:8000/api/zonas/1/estadisticas/
```

### Obtener Consumo Total de un Dispositivo
```bash
curl http://localhost:8000/api/dispositivos/1/consumo_total/
```

### Filtrar Dispositivos por Categoría
```bash
curl http://localhost:8000/api/dispositivos/?categoria=Sensor
```

### Buscar Alertas Graves
```bash
curl http://localhost:8000/api/alertas/?gravedad=Grave
```

### Obtener Mediciones de un Período
```bash
curl "http://localhost:8000/api/mediciones/?fecha_desde=2024-01-01&fecha_hasta=2024-12-31"
```

## Formato de Respuestas

### Paginación
Todas las listas están paginadas (10 elementos por página por defecto):
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/dispositivos/?page=2",
  "previous": null,
  "results": [...]
}
```

### Errores de Validación
```json
{
  "nombre": ["Este campo es requerido."],
  "watts": ["El consumo en watts no puede ser negativo"]
}
```

### Errores Generales
```json
{
  "detail": "No encontrado."
}
```

## Configuración

La API está configurada con:
- Paginación: 10 elementos por página
- Autenticación: Session y Basic (sin restricciones por defecto)
- Permisos: AllowAny (público)
- Formatos: JSON y Browsable API

## Navegador de API
Accede a `http://localhost:8000/api/` en tu navegador para explorar la API de forma interactiva.
