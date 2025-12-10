# Script de despliegue a AWS Lambda para EcoEnergy API (Windows PowerShell)
# Uso: .\deploy_lambda.ps1 -Environment dev

param(
    [Parameter(Mandatory=$false)]
    [string]$Environment = "dev"
)

# Colors
$Green = [System.ConsoleColor]::Green
$Red = [System.ConsoleColor]::Red
$Yellow = [System.ConsoleColor]::Yellow

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor $Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor $Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️ $Message" -ForegroundColor $Yellow
}

Write-Host "🚀 Iniciando despliegue de EcoEnergy API en AWS Lambda ($Environment)" -ForegroundColor $Green

# 1. Verificar AWS CLI
Write-Info "[1/7] Verificando AWS CLI..."
try {
    $awsVersion = aws --version
    Write-Success "AWS CLI encontrado: $awsVersion"
} catch {
    Write-Error-Custom "AWS CLI no está instalado"
    Write-Host "Instálalo con: pip install awscli"
    exit 1
}

# 2. Verificar credenciales AWS
Write-Info "[2/7] Verificando credenciales AWS..."
try {
    $AccountId = aws sts get-caller-identity --query 'Account' --output text
    Write-Success "Credenciales válidas (Account: $AccountId)"
} catch {
    Write-Error-Custom "Credenciales AWS no configuradas"
    Write-Host "Configura con: aws configure"
    exit 1
}

# 3. Crear S3 bucket
Write-Info "[3/7] Preparando S3 bucket..."
$BucketName = "ecoenergy-zappa-deployments-$Environment"
$Region = "us-east-1"

try {
    aws s3 ls "s3://$BucketName" 2>&1 | Out-Null
    Write-Success "Bucket $BucketName ya existe"
} catch {
    Write-Host "Creando bucket $BucketName..."
    aws s3 mb "s3://$BucketName" --region $Region
    Write-Success "Bucket creado"
}

# 4. Instalar dependencias Python
Write-Info "[4/7] Instalando dependencias Python..."
$VenvPath = "monitoreo\venv_lambda"

if (-not (Test-Path $VenvPath)) {
    Write-Host "Creando virtual environment..."
    python -m venv $VenvPath
}

# Activar venv
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
& $ActivateScript

pip install -q -r "monitoreo\requirements-lambda.txt"
Write-Success "Dependencias instaladas"

# 5. Verificar .env
Write-Info "[5/7] Verificando variables de entorno..."
$EnvFile = "monitoreo\.env"

if (-not (Test-Path $EnvFile)) {
    Write-Error-Custom "Archivo .env no encontrado"
    Write-Host "Copia example.env a .env y completa los valores"
    exit 1
}
Write-Success ".env encontrado"

# 6. Ejecutar migraciones
Write-Info "[6/7] Preparando migraciones..."
Push-Location "monitoreo"
python manage.py makemigrations > $null 2>&1
python manage.py migrate --noinput > $null 2>&1
Pop-Location
Write-Success "Migraciones preparadas"

# 7. Desplegar con Zappa
Write-Info "[7/7] Desplegando en AWS Lambda..."
Push-Location "monitoreo"

$ZappaStatus = zappa status $Environment 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "Actualizando Lambda..."
    zappa update $Environment
} else {
    Write-Host "Creando nueva función Lambda..."
    zappa deploy $Environment
}

# Obtener estado
Write-Host ""
Write-Success "Despliegue completado!`n"
Write-Info "Información del despliegue:"
zappa status $Environment

# Obtener URL
$ApiUrl = zappa status $Environment 2>&1 | Select-String "API Gateway URL" | ForEach-Object { $_.ToString().Split()[-1] }

if ($ApiUrl) {
    Write-Host ""
    Write-Host "🌐 API disponible en: $ApiUrl" -ForegroundColor $Green
    Write-Host "Endpoints:" -ForegroundColor $Yellow
    Write-Host "  GET    ${ApiUrl}api/rrhh/"
    Write-Host "  GET    ${ApiUrl}api/rrhh/departamentos/"
    Write-Host "  GET    ${ApiUrl}api/rrhh/empleados/"
    Write-Host "  GET    ${ApiUrl}api/rrhh/proyectos/"
    Write-Host "  GET    ${ApiUrl}api/rrhh/registros-tiempo/"
}

Write-Host ""
Write-Info "Para ver logs en tiempo real:"
Write-Host "  zappa tail $Environment --since 10m" -ForegroundColor Gray

Write-Info "Para ver errores:"
Write-Host "  aws logs filter-log-events --log-group-name /aws/lambda/ecoenergy-api --filter-pattern ERROR" -ForegroundColor Gray

Pop-Location

Write-Host "`n¡Listo para usar! 🎉" -ForegroundColor $Green
