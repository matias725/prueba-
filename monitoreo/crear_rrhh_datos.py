import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoreo.settings')
django.setup()

from django.contrib.auth.models import User
from rrhh.models import Departamento, Empleado, Proyecto, RegistroTiempo
from datetime import datetime, timedelta
import random

print("🚀 Creando datos de prueba para RRHH...\n")

# Crear departamentos
depts = []
for nombre in ["Desarrollo", "Recursos Humanos", "Ventas", "Finanzas"]:
    d, _ = Departamento.objects.get_or_create(nombre=nombre, defaults={"presupuesto": 50000})
    depts.append(d)
    print(f"✓ Departamento: {nombre}")

# Crear empleados
emps = []
for i, (fname, lname, puesto) in enumerate([
    ("Juan", "García", "Desarrollador Senior"),
    ("María", "López", "Desarrolladora"),
    ("Carlos", "Rodríguez", "Gerente RRHH"),
    ("Ana", "Martínez", "Ejecutiva Ventas"),
    ("Miguel", "Sánchez", "Contador"),
], 1):
    u, _ = User.objects.get_or_create(username=f"{fname.lower()}.{lname.lower()}", 
                                        defaults={"first_name": fname, "last_name": lname, "email": f"{fname.lower()}@emp.com"})
    e, _ = Empleado.objects.get_or_create(user=u, defaults={
        "numero_empleado": f"00{i}",
        "departamento": depts[i % len(depts)],
        "puesto": puesto,
        "salario": 25000 + (i*5000),
        "fecha_contratacion": datetime.now().date() - timedelta(days=200)
    })
    emps.append(e)
    print(f"✓ Empleado: {fname} {lname}")

# Crear proyectos
proyectos = []
for nombre, desc in [
    ("Sistema Inventario", "Sistema web"),
    ("App Móvil", "App para clientes"),
    ("Campaña Marketing", "Q1 2025"),
]:
    p, _ = Proyecto.objects.get_or_create(nombre=nombre, defaults={
        "descripcion": desc,
        "departamento": depts[0],
        "gerente_proyecto": emps[0],
        "presupuesto": 50000,
        "estado": "en_progreso",
        "fecha_inicio": datetime.now().date() - timedelta(days=90),
        "fecha_fin_estimada": datetime.now().date() + timedelta(days=90),
        "porcentaje_completado": random.randint(30, 90)
    })
    proyectos.append(p)
    print(f"✓ Proyecto: {nombre}")

# Crear registros de tiempo
count = 0
for p in proyectos:
    for emp in emps[:3]:
        for d in range(20):
            try:
                RegistroTiempo.objects.create(
                    empleado=emp,
                    proyecto=p,
                    fecha=datetime.now().date() - timedelta(days=d),
                    horas=round(random.uniform(4, 8), 1),
                    descripcion="Trabajo en proyecto",
                    validado=random.choice([True, False])
                )
                count += 1
            except:
                pass

print(f"✓ Registros: {count}")

print("\n" + "="*50)
print("✅ Datos creados!")
print("="*50)
print(f"Departamentos: {Departamento.objects.count()}")
print(f"Empleados: {Empleado.objects.count()}")
print(f"Proyectos: {Proyecto.objects.count()}")
print(f"Registros: {RegistroTiempo.objects.count()}")
print("\n🌐 API: http://localhost:8000/api/rrhh/")
print("="*50)
