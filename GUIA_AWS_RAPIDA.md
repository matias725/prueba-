# 🔑 PASO-A-PASO: Obtener Credenciales AWS

## 1. Ir a AWS Console
https://console.aws.amazon.com/

## 2. Crear Access Keys
1. Click en tu nombre (arriba derecha)
2. Click "Security credentials"
3. Scroll down a "Access keys"
4. Click "Create access key"
5. Selecciona "Command Line Interface (CLI)"
6. Check "I understand..."
7. Click "Create access key"
8. **¡IMPORTANTE!** Copia y guarda:
   - Access key ID (ejemplo: AKIAIOSFODNN7EXAMPLE)
   - Secret access key (ejemplo: wJalrXUtnFEMI/K7MDENG/...)
   
⚠️ **La secret key solo se muestra UNA VEZ**

## 3. Guardar las keys
Cópialas en un archivo temporal o déjalas abiertas.

---

# 🚀 INSTALACIÓN Y DESPLIEGUE

## Paso 1: Instalar AWS CLI
```powershell
pip install awscli
```

## Paso 2: Configurar credenciales
```powershell
aws configure
```

Te preguntará:
```
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/...
Default region name [None]: us-east-1
Default output format [None]: json
```

## Paso 3: Verificar que funciona
```powershell
aws sts get-caller-identity
```

Si muestra tu Account ID, ¡funciona! ✅

## Paso 4: Instalar Zappa
```powershell
cd C:\Users\matia\Documents\1111\unidad1-DMpython-MZ\monitoreo
pip install zappa
```

## Paso 5: Desplegar
```powershell
# Opción A: Usar mi script automático
cd ..
.\deploy_lambda.ps1 -Environment dev

# Opción B: Manual
cd monitoreo
zappa deploy dev
```

## Paso 6: Ver URL
```powershell
zappa status dev
```

Te mostrará algo como:
```
API Gateway URL: https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev
```

## Paso 7: Probar
```powershell
# Copia la URL y agrega /api/rrhh/
# Ejemplo:
https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev/api/rrhh/
```

---

# ⚠️ PROBLEMAS COMUNES

## "Access Denied"
- Verifica que copiaste bien las keys
- Vuelve a ejecutar `aws configure`

## "Timeout"
- Aumenta timeout en zappa_settings.json a 60 segundos
- Vuelve a desplegar: `zappa update dev`

## "No module named django"
- Asegúrate de estar en monitoreo/
- Ejecuta: `pip install -r requirements-lambda.txt`

---

# 💰 COSTO
Con AWS Free Tier (primer año): **$0**
Después: ~$15-20/mes para uso pequeño

---

¿Ya tienes cuenta AWS? Empezamos con las credenciales.
