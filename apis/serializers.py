from rest_framework import serializers
from .models import Orden, DetalleOrden

class DetalleOrdenSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = DetalleOrden
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()


class OrdenSerializer(serializers.ModelSerializer):
    detalles = DetalleOrdenSerializer(many=True, read_only=True)

    class Meta:
        model = Orden
        fields = ['id', 'numero_orden', 'fecha', 'estado', 'total', 'detalles']
