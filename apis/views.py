from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Orden, Proyecto, Sala, Reserva, Vehiculo, Inventario
from .serializers import OrdenSerializer, ProyectoSerializer, ReservaSerializer, SalaSerializer, VehiculoSerializer, InventarioSerializer

# Create your views here.


class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

    @action(detail=True, methods=['patch'], url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        orden = self.get_object()
        nuevo_estado = request.data.get('estado')
        if nuevo_estado not in dict(Orden.ESTADO_CHOICES):
            return Response({'error': 'Estado no válido.'}, status=status.HTTP_400_BAD_REQUEST)
        orden.estado = nuevo_estado
        orden.save()
        return Response({'message': f'Estado cambiado a {nuevo_estado}'})
    
class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

    @action(detail=True, methods=['get'], url_path='progreso')
    def progreso_proyecto(self, request, pk=None):
        proyecto = self.get_object()
        total_tareas = proyecto.tareas.count()
        if total_tareas == 0:
            progreso = 0
        else:
            tareas_completadas = proyecto.tareas.filter(completado=True).count()
            progreso = round((tareas_completadas / total_tareas) * 100, 2)
        return Response({'progreso': f'{progreso}% de tareas completadas'})

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        sala_id = data.get('sala')
        fecha = data.get('fecha')
        hora_inicio = data.get('hora_inicio')
        hora_fin = data.get('hora_fin')

        # Verificar si la sala está disponible
        conflictos = Reserva.objects.filter(
            sala_id=sala_id,
            fecha=fecha,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio
        )
        if conflictos.exists():
            return Response(
                {'error': 'La sala no está disponible en el horario solicitado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='disponibilidad')
    def disponibilidad_salas(self, request):
        fecha = request.query_params.get('fecha')
        hora_inicio = request.query_params.get('hora_inicio')
        hora_fin = request.query_params.get('hora_fin')

        if not fecha or not hora_inicio or not hora_fin:
            return Response(
                {'error': 'Debe proporcionar fecha, hora_inicio y hora_fin como parámetros de consulta.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        salas_disponibles = Sala.objects.exclude(
            reservas__fecha=fecha,
            reservas__hora_inicio__lt=hora_fin,
            reservas__hora_fin__gt=hora_inicio
        )

        serializer = SalaSerializer(salas_disponibles, many=True)
        return Response(serializer.data)
    
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    @action(detail=True, methods=['post'], url_path='verificar-disponibilidad')
    def verificar_disponibilidad(self, request, pk=None):
        vehiculo = self.get_object()
        cantidad = int(request.data.get('cantidad', 1))  # Vehículos solicitados

        try:
            inventario = vehiculo.inventario
            if inventario.cantidad_disponible >= cantidad:
                return Response({'mensaje': 'Vehículo disponible'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje': 'No hay suficientes vehículos disponibles'}, status=status.HTTP_400_BAD_REQUEST)
        except Inventario.DoesNotExist:
            return Response({'mensaje': 'El inventario de este vehículo no está configurado'}, status=status.HTTP_404_NOT_FOUND)


class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer


