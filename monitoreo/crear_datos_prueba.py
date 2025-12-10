"""
Script para crear datos de prueba para la API de EcoEnergy
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoreo.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import Organizacion, Perfil
from dispositivos.models import Zona, Dispositivo, Medicion, Alerta
from datetime import datetime, timedelta
import random

def crear_datos():
    print("🚀 Creando datos de prueba...")
    
    # 1. Crear organizaciones
    print("\n📊 Creando organizaciones...")
    org1, created = Organizacion.objects.get_or_create(
        nombre="EcoEnergy Corp"
    )
    org2, created = Organizacion.objects.get_or_create(
        nombre="Green Power SA"
    )
    print(f"✅ Organizaciones: {org1.nombre}, {org2.nombre}")
    
    # 2. Crear zonas
    print("\n🏢 Creando zonas...")
    zonas_data = [
        ("Planta Baja", org1),
        ("Primer Piso", org1),
        ("Sala de Servidores", org1),
        ("Oficinas Administrativas", org2),
        ("Área de Producción", org2),
    ]
    zonas = []
    for nombre, org in zonas_data:
        zona, created = Zona.objects.get_or_create(
            nombre=nombre,
            organizacion=org
        )
        zonas.append(zona)
        print(f"  - {zona.nombre} ({zona.organizacion.nombre})")
    
    # 3. Crear dispositivos
    print("\n💡 Creando dispositivos...")
    dispositivos_data = [
        ("Sensor Temperatura Principal", "Sensor", zonas[0], 5.5),
        ("Aire Acondicionado 1", "Actuador", zonas[0], 2500),
        ("Iluminación LED Oficina", "General", zonas[0], 150),
        ("Sensor Humedad", "Sensor", zonas[1], 4.2),
        ("Ventilador Industrial", "Actuador", zonas[1], 750),
        ("Servidor Principal", "General", zonas[2], 500),
        ("UPS Backup", "Actuador", zonas[2], 1200),
        ("Sensor Movimiento", "Sensor", zonas[3], 3.0),
        ("Calefacción Central", "Actuador", zonas[3], 3000),
        ("Motor Bomba Agua", "Actuador", zonas[4], 1800),
    ]
    
    dispositivos = []
    for nombre, categoria, zona, watts in dispositivos_data:
        disp, created = Dispositivo.objects.get_or_create(
            nombre=nombre,
            defaults={
                'categoria': categoria,
                'zona': zona,
                'watts': watts
            }
        )
        dispositivos.append(disp)
        print(f"  - {disp.nombre} ({disp.categoria}, {disp.watts}W)")
    
    # 4. Crear mediciones
    print("\n📈 Creando mediciones...")
    total_mediciones = 0
    for dispositivo in dispositivos:
        # Crear 10-20 mediciones por dispositivo
        num_mediciones = random.randint(10, 20)
        for i in range(num_mediciones):
            # Consumo basado en los watts del dispositivo
            consumo_base = (dispositivo.watts / 1000) * random.uniform(0.5, 2.0)
            Medicion.objects.create(
                dispositivo=dispositivo,
                consumo=round(consumo_base, 2)
            )
            total_mediciones += 1
    print(f"✅ {total_mediciones} mediciones creadas")
    
    # 5. Crear alertas
    print("\n⚠️ Creando alertas...")
    alertas_data = [
        (dispositivos[1], "Consumo excesivo detectado", "Alta"),
        (dispositivos[1], "Temperatura anormal en el equipo", "Grave"),
        (dispositivos[5], "Sobrecarga del servidor", "Grave"),
        (dispositivos[6], "UPS en modo batería", "Media"),
        (dispositivos[8], "Consumo fuera de rango normal", "Alta"),
        (dispositivos[9], "Vibración anormal detectada", "Media"),
    ]
    
    for dispositivo, mensaje, gravedad in alertas_data:
        Alerta.objects.create(
            dispositivo=dispositivo,
            mensaje=mensaje,
            gravedad=gravedad
        )
        print(f"  - [{gravedad}] {mensaje} - {dispositivo.nombre}")
    
    # 6. Crear usuario administrador (si no existe)
    print("\n👤 Verificando usuario administrador...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@ecoenergy.com',
            password='admin123'
        )
        print("✅ Usuario admin creado (usuario: admin, password: admin123)")
    else:
        print("✅ Usuario admin ya existe")
    
    # Resumen
    print("\n" + "="*60)
    print("🎉 ¡Datos de prueba creados exitosamente!")
    print("="*60)
    print(f"📊 Organizaciones: {Organizacion.objects.count()}")
    print(f"🏢 Zonas: {Zona.objects.count()}")
    print(f"💡 Dispositivos: {Dispositivo.objects.count()}")
    print(f"📈 Mediciones: {Medicion.objects.count()}")
    print(f"⚠️ Alertas: {Alerta.objects.count()}")
    print("\n🌐 Accede a la API en: http://localhost:8000/api/")
    print("🔐 Admin en: http://localhost:8000/admin/ (admin / admin123)")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        crear_datos()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
