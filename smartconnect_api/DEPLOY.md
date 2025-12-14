# Guía de Despliegue en AWS EC2

## Información de la Instancia

- **IP Pública**: 98.88.189.220
- **Usuario**: ec2-user o ubuntu (según AMI)
- **Puerto SSH**: 22
- **Clave**: ultimapruebabakend.pem

## Pasos de Despliegue

### 1. Conectar a la Instancia

```bash
ssh -i ultimapruebabakend.pem ec2-user@98.88.189.220
```

Si es Amazon Linux 2, usa `ec2-user`. Si es Ubuntu, usa `ubuntu`.

### 2. Actualizar Sistema

```bash
sudo yum update -y  # Amazon Linux
# o
sudo apt update && sudo apt upgrade -y  # Ubuntu
```

### 3. Instalar Dependencias del Sistema

```bash
# Amazon Linux
sudo yum install python3 python3-pip python3-devel -y
sudo yum install gcc postgresql-devel -y

# Ubuntu
sudo apt install python3 python3-pip python3-dev -y
sudo apt install build-essential postgresql-client -y
```

### 4. Clonar el Repositorio

```bash
cd ~
git clone <tu-repositorio-url>
cd smartconnect_api
```

### 5. Crear Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 6. Instalar Dependencias Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 7. Configurar Variables de Entorno

```bash
cat > .env << EOF
SECRET_KEY=tu-secret-key-super-seguro
DEBUG=False
ALLOWED_HOSTS=98.88.189.220,tu-dominio.com
DATABASES_NAME=smartconnect_db
DATABASES_USER=smartconnect_user
DATABASES_PASSWORD=tu-password-seguro
DATABASES_HOST=localhost
DATABASES_PORT=5432
EOF
```

### 8. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 9. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 10. Recopilar Archivos Estáticos

```bash
python manage.py collectstatic --no-input
```

### 11. Probar Servidor Localmente

```bash
python manage.py runserver 0.0.0.0:8000
```

### 12. Configurar Gunicorn

Crear archivo de servicio:

```bash
sudo nano /etc/systemd/system/smartconnect.service
```

Agregar:

```ini
[Unit]
Description=SmartConnect API
After=network.target

[Service]
Type=notify
User=ec2-user
WorkingDirectory=/home/ec2-user/smartconnect_api
ExecStart=/home/ec2-user/smartconnect_api/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 smartconnect.wsgi:application
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### 13. Iniciar Servicio

```bash
sudo systemctl daemon-reload
sudo systemctl start smartconnect
sudo systemctl enable smartconnect
sudo systemctl status smartconnect
```

### 14. Configurar Nginx (Opcional pero Recomendado)

```bash
sudo yum install nginx -y  # o sudo apt install nginx -y
```

Crear configuración:

```bash
sudo nano /etc/nginx/conf.d/smartconnect.conf
```

```nginx
server {
    listen 80;
    server_name 98.88.189.220;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ec2-user/smartconnect_api/staticfiles/;
    }
}
```

Iniciar Nginx:

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 15. Configurar Grupo de Seguridad en AWS

En la consola de AWS:
- Permitir HTTP (80)
- Permitir HTTPS (443)
- Permitir SSH (22) solo desde tu IP

### 16. Probar la API

```bash
curl http://98.88.189.220/api/info/
```

## Troubleshooting

### Ver logs
```bash
sudo journalctl -u smartconnect -f
```

### Ver permisos de archivos
```bash
ls -la /home/ec2-user/smartconnect_api/
```

### Reiniciar servicio
```bash
sudo systemctl restart smartconnect
```

## URLs Importantes

- **API**: http://98.88.189.220/api/
- **Info**: http://98.88.189.220/api/info/
- **Admin**: http://98.88.189.220/admin/
- **Token**: http://98.88.189.220/api/token/

## Monitoreo

Monitorear logs en tiempo real:
```bash
tail -f /var/log/nginx/access.log
sudo journalctl -u smartconnect -f
```

## Backup de Base de Datos

```bash
python manage.py dumpdata > backup.json
```

## Restaurar Base de Datos

```bash
python manage.py loaddata backup.json
```
