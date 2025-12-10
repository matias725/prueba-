# 🎓 DESPLIEGUE EN EC2 CON AWS ACADEMY - PASO A PASO

## PASO 1: INICIAR LAB

1. Ve a tu curso en **AWS Academy**
2. Click en "**Learner Lab**"
3. Click en "**Start Lab**" (botón verde)
4. Espera hasta que el círculo se ponga **VERDE** 🟢
5. Click en "**AWS**" (te lleva a la consola)

---

## PASO 2: CREAR INSTANCIA EC2

### 2.1 Ir a EC2
1. En la consola AWS, busca "**EC2**" en el buscador
2. Click en "**EC2**"
3. Click en "**Launch Instance**" (botón naranja)

### 2.2 Configurar instancia
```
Name: ecoenergy-api
Application and OS Images: Amazon Linux 2023
Instance type: t2.micro (Free tier)
Key pair: 
  - Click "Create new key pair"
  - Name: ecoenergy-key
  - Type: RSA
  - Format: .pem
  - Download automático
```

### 2.3 Network settings
- Click "**Edit**"
- **Auto-assign public IP:** Enable
- **Firewall (security groups):** Create new
  - ☑️ Allow SSH (22) from Anywhere
  - ☑️ Allow HTTP (80) from Anywhere
  - ☑️ Add rule: Custom TCP, Port 8000, Anywhere

### 2.4 Launch
- Click "**Launch instance**"
- Espera 2 minutos

---

## PASO 3: CONECTAR POR SSH

### 3.1 Obtener IP pública
1. Click en tu instancia
2. Copia la "**Public IPv4 address**" (ejemplo: 54.123.45.67)

### 3.2 Conectar desde Windows

**Opción A: PowerShell**
```powershell
# Ir a donde descargaste la key
cd Downloads

# Cambiar permisos (solo primera vez)
icacls ecoenergy-key.pem /reset
icacls ecoenergy-key.pem /grant:r "$($env:USERNAME):(R)"
icacls ecoenergy-key.pem /inheritance:r

# Conectar (reemplaza IP)
ssh -i ecoenergy-key.pem ec2-user@54.123.45.67
```

**Opción B: PuTTY** (si no funciona SSH)
- Descarga PuTTY
- Convierte .pem a .ppk con PuTTYgen
- Conecta con PuTTY

---

## PASO 4: INSTALAR DEPENDENCIAS EN EC2

Una vez conectado por SSH, ejecuta estos comandos:

```bash
# Actualizar sistema
sudo yum update -y

# Instalar Python 3 y Git
sudo yum install python3 python3-pip git -y

# Verificar instalación
python3 --version
git --version
```

---

## PASO 5: CLONAR TU PROYECTO

```bash
# Clonar desde GitHub
git clone https://github.com/matias725/unidad1-DMpython-MZ.git

# Entrar al proyecto
cd unidad1-DMpython-MZ/monitoreo

# Ver archivos
ls
```

---

## PASO 6: INSTALAR DEPENDENCIAS PYTHON

```bash
# Instalar dependencias
pip3 install -r requirements.txt --user

# Verificar Django
python3 -c "import django; print(django.get_version())"
```

---

## PASO 7: CONFIGURAR .ENV

```bash
# Crear archivo .env
nano .env
```

Copia esto:
```
DJANGO_SECRET_KEY=tu-clave-super-secreta-change-this
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*
DB_ENGINE=sqlite3
DB_NAME=db.sqlite3
```

Guardar: `Ctrl+O`, Enter, `Ctrl+X`

---

## PASO 8: EJECUTAR MIGRACIONES

```bash
# Crear base de datos
python3 manage.py migrate

# Crear superuser
python3 manage.py createsuperuser
# Usuario: admin
# Email: admin@example.com
# Password: admin123

# Crear datos de prueba
python3 crear_rrhh_datos.py
```

---

## PASO 9: INICIAR SERVIDOR

```bash
# Iniciar servidor (accesible desde Internet)
python3 manage.py runserver 0.0.0.0:8000
```

**¡LISTO!** Tu API está en:
```
http://54.123.45.67:8000/api/rrhh/
```
(Reemplaza con tu IP pública)

---

## PASO 10: VERIFICAR

Desde tu navegador en Windows:
```
http://TU-IP-PUBLICA:8000/api/rrhh/
http://TU-IP-PUBLICA:8000/admin/
```

---

## 🔧 MANTENER CORRIENDO (Opcional)

Si quieres que siga corriendo cuando cierres SSH:

```bash
# Instalar screen
sudo yum install screen -y

# Iniciar screen
screen -S django

# Iniciar servidor
python3 manage.py runserver 0.0.0.0:8000

# Salir de screen (deja corriendo)
Ctrl+A, luego D

# Volver a conectar después
screen -r django
```

---

## 🎯 PARA PRODUCCIÓN (Opcional avanzado)

Si quieres usar Gunicorn + Nginx:

```bash
# Instalar Gunicorn
pip3 install gunicorn --user

# Instalar Nginx
sudo yum install nginx -y

# Iniciar con Gunicorn
gunicorn monitoreo.wsgi:application --bind 0.0.0.0:8000
```

---

## ⚠️ IMPORTANTE: APAGAR INSTANCIA

**AWS Academy tiene límite de horas.** Cuando termines:

1. Ve a EC2 Console
2. Selecciona tu instancia
3. "**Instance state**" → "**Stop instance**"

Para volver a usar:
1. "**Instance state**" → "**Start instance**"
2. ⚠️ **La IP pública cambiará**
3. Vuelve a conectar con la nueva IP

---

## 📝 RESUMEN DE COMANDOS

```bash
# Conectar
ssh -i ecoenergy-key.pem ec2-user@TU-IP

# Ir al proyecto
cd unidad1-DMpython-MZ/monitoreo

# Iniciar servidor
python3 manage.py runserver 0.0.0.0:8000

# URL: http://TU-IP:8000/api/rrhh/
```

---

## 🎓 PARA TU EVALUACIÓN

Puedes decir:

> "Desplegué la API en una instancia EC2 de AWS. Configuré el servidor,
> instalé dependencias, ejecuté migraciones y está corriendo en producción.
> La API es accesible públicamente en http://[tu-ip]:8000/api/rrhh/"

Luego muestras tu navegador con la URL funcionando. ✨

---

¿Listo para empezar? Empieza con el **PASO 1** en AWS Academy.
