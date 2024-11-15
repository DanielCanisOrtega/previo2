from rest_framework import serializers
from .models import Orden, DetalleOrden, Proyecto, TareaProyecto, Sala, Reserva, Vehiculo, Inventario

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

class TareaProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareaProyecto
        fields = ['id', 'nombre_tarea', 'responsable', 'fecha_limite', 'completado']


class ProyectoSerializer(serializers.ModelSerializer):
    tareas = TareaProyectoSerializer(many=True, read_only=True)
    progreso = serializers.SerializerMethodField()

    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado', 'tareas', 'progreso']

    def get_progreso(self, obj):
        total_tareas = obj.tareas.count()
        if total_tareas == 0:
            return 0
        tareas_completadas = obj.tareas.filter(completado=True).count()
        return round((tareas_completadas / total_tareas) * 100, 2)

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['id', 'nombre', 'capacidad', 'disponibilidad']


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'sala', 'fecha', 'hora_inicio', 'hora_fin']

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['id', 'marca', 'modelo', 'año', 'precio', 'disponibilidad']


class InventarioSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSerializer(read_only=True)

    class Meta:
        model = Inventario
        fields = ['id', 'vehiculo', 'cantidad_disponible']
