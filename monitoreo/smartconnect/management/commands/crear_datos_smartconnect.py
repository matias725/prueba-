from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from smartconnect.models import Departamento, Rol, UsuarioSmartConnect, Sensor, Barrera, Evento


class Command(BaseCommand):
    help = 'Carga datos de prueba para SmartConnect'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Creando datos de prueba para SmartConnect...")

        # Crear roles
        rol_admin, _ = Rol.objects.get_or_create(nombre='admin', defaults={'descripcion': 'Administrador del sistema'})
        rol_operador, _ = Rol.objects.get_or_create(nombre='operador', defaults={'descripcion': 'Operador del sistema'})
        self.stdout.write(f"✓ Roles creados/encontrados")

        # Crear departamentos
        dept_seguridad, _ = Departamento.objects.get_or_create(
            nombre='Seguridad',
            defaults={'descripcion': 'Departamento de Seguridad Física', 'ubicacion': 'Planta Baja'}
        )
        dept_ti, _ = Departamento.objects.get_or_create(
            nombre='Tecnología',
            defaults={'descripcion': 'Departamento de TI', 'ubicacion': 'Piso 2'}
        )
        dept_admin, _ = Departamento.objects.get_or_create(
            nombre='Administración',
            defaults={'descripcion': 'Departamento Administrativo', 'ubicacion': 'Piso 3'}
        )
        self.stdout.write(f"✓ Departamentos creados/encontrados")

        # Crear usuarios
        user_admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@smartconnect.com', 'first_name': 'Admin', 'last_name': 'System'}
        )
        UsuarioSmartConnect.objects.get_or_create(
            user=user_admin,
            defaults={'rol': rol_admin, 'departamento': dept_seguridad}
        )

        user_operador, _ = User.objects.get_or_create(
            username='operador',
            defaults={'email': 'operador@smartconnect.com', 'first_name': 'Juan', 'last_name': 'Operador'}
        )
        UsuarioSmartConnect.objects.get_or_create(
            user=user_operador,
            defaults={'rol': rol_operador, 'departamento': dept_seguridad}
        )

        user_empleado, _ = User.objects.get_or_create(
            username='empleado',
            defaults={'email': 'empleado@smartconnect.com', 'first_name': 'Carlos', 'last_name': 'Empleado'}
        )
        UsuarioSmartConnect.objects.get_or_create(
            user=user_empleado,
            defaults={'rol': rol_operador, 'departamento': dept_ti}
        )

        # Establecer contraseñas
        if user_admin.check_password('admin123') == False:
            user_admin.set_password('admin123')
            user_admin.save()
        if user_operador.check_password('operador123') == False:
            user_operador.set_password('operador123')
            user_operador.save()
        if user_empleado.check_password('empleado123') == False:
            user_empleado.set_password('empleado123')
            user_empleado.save()

        self.stdout.write(f"✓ Usuarios creados/encontrados con contraseñas")

        # Crear sensores
        sensores_data = [
            {'uid_mac': 'RFID001', 'descripcion': 'Tarjeta de acceso Juan', 'usuario': user_empleado, 'departamento': dept_ti},
            {'uid_mac': 'RFID002', 'descripcion': 'Llavero de seguridad', 'usuario': user_operador, 'departamento': dept_seguridad},
            {'uid_mac': 'RFID003', 'descripcion': 'Tarjeta de acceso Carlos', 'usuario': user_empleado, 'departamento': dept_admin},
            {'uid_mac': 'RFID004', 'descripcion': 'Tarjeta bloqueada', 'estado': 'bloqueado', 'departamento': dept_seguridad},
            {'uid_mac': 'RFID005', 'descripcion': 'Tarjeta perdida', 'estado': 'perdido', 'departamento': dept_ti},
        ]

        for sensor_data in sensores_data:
            Sensor.objects.get_or_create(
                uid_mac=sensor_data['uid_mac'],
                defaults={k: v for k, v in sensor_data.items() if k != 'uid_mac'}
            )
        self.stdout.write(f"✓ Sensores RFID creados/encontrados")

        # Crear barreras
        barrera1, _ = Barrera.objects.get_or_create(
            nombre='Puerta Principal',
            defaults={'descripcion': 'Control de acceso puerta principal', 'departamento': dept_seguridad, 'estado': 'cerrada'}
        )
        barrera2, _ = Barrera.objects.get_or_create(
            nombre='Puerta Servidor',
            defaults={'descripcion': 'Acceso a sala de servidores', 'departamento': dept_ti, 'estado': 'cerrada'}
        )
        self.stdout.write(f"✓ Barreras de acceso creadas/encontradas")

        # Crear eventos
        sensor1 = Sensor.objects.get(uid_mac='RFID001')
        sensor2 = Sensor.objects.get(uid_mac='RFID002')
        sensor_bloqueado = Sensor.objects.get(uid_mac='RFID004')

        Evento.objects.get_or_create(
            sensor=sensor1,
            tipo='acceso_permitido',
            defaults={'barrera': barrera1, 'resultado': 'permitido', 'usuario': user_empleado}
        )
        Evento.objects.get_or_create(
            sensor=sensor2,
            tipo='acceso_permitido',
            defaults={'barrera': barrera2, 'resultado': 'permitido', 'usuario': user_operador}
        )
        Evento.objects.get_or_create(
            sensor=sensor_bloqueado,
            tipo='acceso_denegado',
            defaults={'resultado': 'Sensor bloqueado'}
        )

        # Crear más eventos de ejemplo
        for i in range(5):
            Evento.objects.create(
                tipo='acceso_permitido' if i % 2 == 0 else 'acceso_denegado',
                sensor=sensor1 if i % 2 == 0 else sensor_bloqueado,
                barrera=barrera1 if i % 2 == 0 else None,
                usuario=user_empleado if i % 2 == 0 else None,
                resultado='permitido' if i % 2 == 0 else 'Sensor en mantenimiento'
            )

        self.stdout.write(f"✓ Eventos de acceso creados")

        self.stdout.write("\n" + "="*50)
        self.stdout.write("✅ Datos de prueba creados exitosamente!")
        self.stdout.write("="*50)
        self.stdout.write("\nCredenciales disponibles:")
        self.stdout.write("  Admin:    usuario=admin,     contraseña=admin123")
        self.stdout.write("  Operador: usuario=operador,  contraseña=operador123")
        self.stdout.write("  Empleado: usuario=empleado,  contraseña=empleado123")
        self.stdout.write("\n🔗 URL base: /api/smartconnect/")
        self.stdout.write("🔑 Login en: /api/smartconnect/login/")
        self.stdout.write("ℹ️  Info en: /api/smartconnect/info/")
