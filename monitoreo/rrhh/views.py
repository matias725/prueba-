from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from .models import Departamento, Empleado, Proyecto, RegistroTiempo
from .serializers import (
    DepartamentoSerializer,
    EmpleadoSerializer, EmpleadoDetalleSerializer,
    ProyectoSerializer, ProyectoDetalleSerializer,
    RegistroTiempoSerializer, DashboardSerializer
)


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar departamentos
    
    Operaciones disponibles:
    - GET /api/rrhh/departamentos/ - Listar todos
    - POST /api/rrhh/departamentos/ - Crear nuevo
    - GET /api/rrhh/departamentos/{id}/ - Ver detalle
    - PUT /api/rrhh/departamentos/{id}/ - Actualizar completo
    - PATCH /api/rrhh/departamentos/{id}/ - Actualizar parcial
    - DELETE /api/rrhh/departamentos/{id}/ - Eliminar
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'presupuesto', 'fecha_creacion']
    ordering = ['nombre']

    def get_queryset(self):
        queryset = Departamento.objects.select_related('gerente')
        activo = self.request.query_params.get('activo', None)
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        return queryset

    @action(detail=True, methods=['get'])
    def empleados(self, request, pk=None):
        """Obtiene todos los empleados activos del departamento"""
        departamento = self.get_object()
        empleados = departamento.empleados.filter(estado='activo')
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def proyectos(self, request, pk=None):
        """Obtiene todos los proyectos activos del departamento"""
        departamento = self.get_object()
        proyectos = departamento.proyectos.exclude(estado='cancelado')
        serializer = ProyectoSerializer(proyectos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Estadísticas del departamento"""
        departamento = self.get_object()
        empleados = departamento.empleados.filter(estado='activo')
        proyectos = departamento.proyectos.exclude(estado='cancelado')
        
        total_salarios = empleados.aggregate(Sum('salario'))['salario__sum'] or 0
        total_horas = RegistroTiempo.objects.filter(
            proyecto__departamento=departamento
        ).aggregate(Sum('horas'))['horas__sum'] or 0
        
        return Response({
            'nombre': departamento.nombre,
            'total_empleados': empleados.count(),
            'total_proyectos': proyectos.count(),
            'total_salarios': float(total_salarios),
            'presupuesto': float(departamento.presupuesto),
            'total_horas_registradas': float(total_horas),
            'proyectos_completados': proyectos.filter(estado='completado').count(),
            'proyecto_promedio_completado': proyectos.aggregate(Avg('porcentaje_completado'))['porcentaje_completado__avg'] or 0
        })


class EmpleadoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar empleados
    
    Operaciones disponibles:
    - GET /api/rrhh/empleados/ - Listar todos
    - POST /api/rrhh/empleados/ - Crear nuevo (requiere usuario asociado)
    - GET /api/rrhh/empleados/{id}/ - Ver detalle completo
    - PUT /api/rrhh/empleados/{id}/ - Actualizar completo
    - PATCH /api/rrhh/empleados/{id}/ - Actualizar parcial
    - DELETE /api/rrhh/empleados/{id}/ - Eliminar
    """
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'numero_empleado', 'departamento__nombre']
    ordering_fields = ['user__first_name', 'salario', 'fecha_contratacion']
    ordering = ['user__first_name']

    def get_queryset(self):
        queryset = Empleado.objects.select_related('user', 'departamento')
        estado = self.request.query_params.get('estado', None)
        departamento_id = self.request.query_params.get('departamento', None)
        
        if estado:
            queryset = queryset.filter(estado=estado)
        if departamento_id:
            queryset = queryset.filter(departamento_id=departamento_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmpleadoDetalleSerializer
        return EmpleadoSerializer

    @action(detail=True, methods=['get'])
    def registros_tiempo(self, request, pk=None):
        """Obtiene todos los registros de tiempo del empleado"""
        empleado = self.get_object()
        registros = empleado.registrostiempo.all()
        
        # Filtros opcionales
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')
        proyecto_id = request.query_params.get('proyecto')
        
        if fecha_desde:
            registros = registros.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            registros = registros.filter(fecha__lte=fecha_hasta)
        if proyecto_id:
            registros = registros.filter(proyecto_id=proyecto_id)
        
        serializer = RegistroTiempoSerializer(registros, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Estadísticas del empleado"""
        empleado = self.get_object()
        registros = empleado.registrostiempo.all()
        
        total_horas = registros.aggregate(Sum('horas'))['horas__sum'] or 0
        proyectos_diferentes = registros.values('proyecto').distinct().count()
        
        today = timezone.now().date()
        horas_mes_actual = registros.filter(
            fecha__year=today.year,
            fecha__month=today.month
        ).aggregate(Sum('horas'))['horas__sum'] or 0
        
        return Response({
            'nombre': empleado.user.get_full_name(),
            'numero_empleado': empleado.numero_empleado,
            'salario': float(empleado.salario),
            'total_horas_registradas': float(total_horas),
            'proyectos_asignados': proyectos_diferentes,
            'horas_mes_actual': float(horas_mes_actual),
            'antiguedad_meses': empleado.antiguedad_meses,
            'dias_trabajados': empleado.dias_trabajados
        })

    @action(detail=False, methods=['get'])
    def por_departamento(self, request):
        """Agrupa empleados por departamento"""
        empleados_por_depto = Empleado.objects.filter(
            estado='activo'
        ).values('departamento__nombre').annotate(
            total=Count('id'),
            salario_promedio=Avg('salario')
        ).order_by('departamento__nombre')
        
        return Response(list(empleados_por_depto))


class ProyectoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar proyectos
    
    Operaciones disponibles:
    - GET /api/rrhh/proyectos/ - Listar todos
    - POST /api/rrhh/proyectos/ - Crear nuevo
    - GET /api/rrhh/proyectos/{id}/ - Ver detalle completo
    - PUT /api/rrhh/proyectos/{id}/ - Actualizar completo
    - PATCH /api/rrhh/proyectos/{id}/ - Actualizar parcial
    - DELETE /api/rrhh/proyectos/{id}/ - Eliminar
    """
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion', 'departamento__nombre']
    ordering_fields = ['fecha_inicio', 'fecha_fin_estimada', 'porcentaje_completado', 'presupuesto']
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        queryset = Proyecto.objects.select_related('departamento', 'gerente_proyecto__user')
        
        estado = self.request.query_params.get('estado', None)
        departamento_id = self.request.query_params.get('departamento', None)
        
        if estado:
            queryset = queryset.filter(estado=estado)
        if departamento_id:
            queryset = queryset.filter(departamento_id=departamento_id)
        
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProyectoDetalleSerializer
        return ProyectoSerializer

    @action(detail=True, methods=['get'])
    def registros_tiempo(self, request, pk=None):
        """Obtiene todos los registros de tiempo del proyecto"""
        proyecto = self.get_object()
        registros = proyecto.registrostiempo.all()
        serializer = RegistroTiempoSerializer(registros, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Estadísticas del proyecto"""
        proyecto = self.get_object()
        registros = proyecto.registrostiempo.all()
        
        total_horas = registros.aggregate(Sum('horas'))['horas__sum'] or 0
        empleados_asignados = registros.values('empleado').distinct().count()
        
        return Response({
            'nombre': proyecto.nombre,
            'estado': proyecto.get_estado_display(),
            'porcentaje_completado': proyecto.porcentaje_completado,
            'dias_para_vencer': proyecto.dias_para_vencer,
            'total_horas_registradas': float(total_horas),
            'empleados_asignados': empleados_asignados,
            'presupuesto': float(proyecto.presupuesto),
            'fecha_inicio': proyecto.fecha_inicio,
            'fecha_fin_estimada': proyecto.fecha_fin_estimada
        })

    @action(detail=False, methods=['get'])
    def por_estado(self, request):
        """Agrupa proyectos por estado"""
        proyectos_por_estado = Proyecto.objects.values('estado').annotate(
            total=Count('id'),
            presupuesto_total=Sum('presupuesto'),
            porcentaje_promedio=Avg('porcentaje_completado')
        ).order_by('-total')
        
        return Response(list(proyectos_por_estado))

    @action(detail=False, methods=['get'])
    def criticos(self, request):
        """Proyectos en riesgo (próximos a vencer y con bajo porcentaje)"""
        today = timezone.now().date()
        proyectos_criticos = Proyecto.objects.filter(
            estado='en_progreso',
            fecha_fin_estimada__lt=today,
            porcentaje_completado__lt=100
        )
        serializer = ProyectoSerializer(proyectos_criticos, many=True)
        return Response(serializer.data)


class RegistroTiempoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar registros de tiempo
    
    Operaciones disponibles:
    - GET /api/rrhh/registros-tiempo/ - Listar todos
    - POST /api/rrhh/registros-tiempo/ - Crear nuevo
    - GET /api/rrhh/registros-tiempo/{id}/ - Ver detalle
    - PUT /api/rrhh/registros-tiempo/{id}/ - Actualizar completo
    - PATCH /api/rrhh/registros-tiempo/{id}/ - Actualizar parcial
    - DELETE /api/rrhh/registros-tiempo/{id}/ - Eliminar
    """
    queryset = RegistroTiempo.objects.all()
    serializer_class = RegistroTiempoSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['fecha', 'horas']
    ordering = ['-fecha']

    def get_queryset(self):
        queryset = RegistroTiempo.objects.select_related('empleado__user', 'proyecto')
        
        empleado_id = self.request.query_params.get('empleado')
        proyecto_id = self.request.query_params.get('proyecto')
        fecha_desde = self.request.query_params.get('fecha_desde')
        fecha_hasta = self.request.query_params.get('fecha_hasta')
        validado = self.request.query_params.get('validado')
        
        if empleado_id:
            queryset = queryset.filter(empleado_id=empleado_id)
        if proyecto_id:
            queryset = queryset.filter(proyecto_id=proyecto_id)
        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)
        if validado is not None:
            queryset = queryset.filter(validado=validado.lower() == 'true')
        
        return queryset

    @action(detail=False, methods=['get'])
    def estadisticas_generales(self, request):
        """Estadísticas generales de registros de tiempo"""
        registros = self.get_queryset()
        
        total_horas = registros.aggregate(Sum('horas'))['horas__sum'] or 0
        registros_validados = registros.filter(validado=True).count()
        
        return Response({
            'total_registros': registros.count(),
            'total_horas': float(total_horas),
            'registros_validados': registros_validados,
            'promedio_horas_por_registro': float(total_horas / registros.count() if registros.count() > 0 else 0)
        })

    @action(detail=False, methods=['post'])
    def validar_registros(self, request):
        """Valida registros de tiempo por IDs"""
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': 'No se proporcionaron IDs'}, status=status.HTTP_400_BAD_REQUEST)
        
        registros = RegistroTiempo.objects.filter(id__in=ids)
        registros.update(validado=True)
        
        return Response({
            'mensaje': f'{registros.count()} registros validados',
            'registros_actualizados': registros.count()
        })


class DashboardViewSet(viewsets.ViewSet):
    """
    Endpoint para obtener un dashboard con estadísticas generales
    """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def general(self, request):
        """Dashboard general del sistema RRHH"""
        empleados_activos = Empleado.objects.filter(estado='activo').count()
        proyectos_activos = Proyecto.objects.filter(estado='en_progreso').count()
        total_horas = RegistroTiempo.objects.aggregate(Sum('horas'))['horas__sum'] or 0
        presupuesto_total = Proyecto.objects.aggregate(Sum('presupuesto'))['presupuesto__sum'] or 0
        
        empleados_por_depto = list(Empleado.objects.filter(
            estado='activo'
        ).values('departamento__nombre').annotate(total=Count('id')).order_by('departamento__nombre'))
        
        proyectos_por_estado = list(Proyecto.objects.values('estado').annotate(total=Count('id')).order_by('-total'))
        
        return Response({
            'total_empleados': empleados_activos,
            'total_proyectos': proyectos_activos,
            'total_horas_registradas': float(total_horas),
            'presupuesto_total': float(presupuesto_total),
            'proyectos_en_riesgo': Proyecto.objects.filter(
                estado='en_progreso',
                fecha_fin_estimada__lt=timezone.now().date(),
                porcentaje_completado__lt=100
            ).count(),
            'empleados_por_departamento': empleados_por_depto,
            'proyectos_por_estado': proyectos_por_estado,
            'registros_no_validados': RegistroTiempo.objects.filter(validado=False).count()
        })

    @action(detail=False, methods=['get'])
    def info(self, request):
        """Información del proyecto/API"""
        return Response({
            'proyecto': 'Sistema de Gestión de Recursos Humanos',
            'version': '2.0',
            'autor': 'Matias',
            'descripcion': 'API REST profesional para gestión de RRHH, empleados, proyectos y registros de tiempo',
            'modulos': ['Departamentos', 'Empleados', 'Proyectos', 'Registros de Tiempo'],
            'estado': 'Operativo'
        })
