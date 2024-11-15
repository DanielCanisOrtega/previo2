from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Orden
from .serializers import OrdenSerializer

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


