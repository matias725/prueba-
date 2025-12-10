# 🎓 DESPLIEGUE CON AWS ACADEMY (Estudiante)

## ⚠️ IMPORTANTE: AWS Academy tiene limitaciones

AWS Academy NO permite desplegar Lambda directamente con Zappa porque:
- No tiene permisos completos de IAM
- Las credenciales expiran cada 4 horas
- Algunos servicios están restringidos

## ✅ ALTERNATIVA: Railway.app (MÁS FÁCIL)

**Railway.app es PERFECTO para estudiantes:**
- ✅ Gratis (hasta $5/mes)
- ✅ No necesita tarjeta de crédito
- ✅ Despliegue en 5 minutos
- ✅ HTTPS automático
- ✅ Base de datos incluida

### Desplegar en Railway (5 minutos)

1. **Crear cuenta en Railway**
   https://railway.app/
   - Login con GitHub

2. **Nuevo proyecto**
   - Click "New Project"
   - "Deploy from GitHub repo"
   - Selecciona tu repo `unidad1-DMpython-MZ`

3. **Configurar variables**
   Click en tu proyecto → Variables → Add variables:
   ```
   DJANGO_SECRET_KEY=tu-clave-secreta-aqui
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=*.railway.app
   DB_ENGINE=sqlite3
   DB_NAME=/app/db.sqlite3
   ```

4. **Agregar comando de inicio**
   Settings → Start Command:
   ```
   cd monitoreo && python manage.py migrate && gunicorn monitoreo.wsgi --bind 0.0.0.0:$PORT
   ```

5. **Deploy**
   - Railway automáticamente despliega
   - Te da una URL: `https://tu-proyecto.railway.app`

---

## 🚀 ALTERNATIVA 2: Render.com

**También gratis y fácil:**

1. https://render.com/
2. Nuevo Web Service
3. Conecta GitHub
4. Selecciona repo
5. Railway lo detecta automáticamente
6. Deploy

---

## 📝 SI AÚN QUIERES USAR AWS ACADEMY

### Opción: EC2 Manual

1. **Iniciar Lab en AWS Academy**
2. **Launch EC2 Instance:**
   - Amazon Linux 2
   - t2.micro (Free tier)
   - Security group: permitir HTTP (80), SSH (22)

3. **Conectar por SSH**
   ```bash
   ssh -i tu-key.pem ec2-user@tu-ip-publica
   ```

4. **Instalar dependencias**
   ```bash
   sudo yum update -y
   sudo yum install python3 python3-pip git -y
   git clone https://github.com/matias725/unidad1-DMpython-MZ.git
   cd unidad1-DMpython-MZ/monitoreo
   pip3 install -r requirements.txt
   ```

5. **Ejecutar**
   ```bash
   python3 manage.py migrate
   python3 manage.py runserver 0.0.0.0:8000
   ```

6. **Acceder**
   ```
   http://tu-ip-publica:8000/api/rrhh/
   ```

---

## 🎯 MI RECOMENDACIÓN

**Para tu evaluación:** Usa **Railway.app**

**Ventajas:**
- ✅ 5 minutos de setup
- ✅ URL pública con HTTPS
- ✅ No expira
- ✅ Gratis
- ✅ No necesita tarjeta

**Pasos:**
1. Push tu código a GitHub (si no lo has hecho)
2. Conecta Railway con GitHub
3. Deploy automático
4. URL lista para mostrar en evaluación

---

## 💡 PARA TU PRESENTACIÓN

Puedes decir:

> "El proyecto está desplegado en Railway.app, una plataforma serverless 
> moderna. También está preparado para AWS Lambda con scripts automáticos,
> pero como tengo cuenta de estudiante con limitaciones, elegí Railway
> que es ideal para desarrollo y demos."

**Esto suena MÁS profesional** que decir "no pude con AWS Academy". ✨

---

¿Quieres que te ayude a desplegar en Railway ahora? Es MUCHO más fácil.
