from django.db import models

# Create your models here.

class Orden(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Enviado', 'Enviado'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
    ]
    numero_orden = models.CharField(max_length=20, unique=True)
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Orden #{self.numero_orden} - {self.estado}"


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, related_name='detalles', on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto} - {self.cantidad} unidades"
    
class Proyecto(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Progreso', 'En Progreso'),
        ('Completado', 'Completado'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return self.nombre


class TareaProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, related_name='tareas', on_delete=models.CASCADE)
    nombre_tarea = models.CharField(max_length=100)
    responsable = models.CharField(max_length=100)
    fecha_limite = models.DateField()
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"Tarea: {self.nombre_tarea} - Proyecto: {self.proyecto.nombre}"
    
class Sala(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    capacidad = models.PositiveIntegerField()
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    sala = models.ForeignKey(Sala, related_name='reservas', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('sala', 'fecha', 'hora_inicio', 'hora_fin')

    def __str__(self):
        return f"Reserva de {self.sala.nombre} el {self.fecha} de {self.hora_inicio} a {self.hora_fin}"
    
class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    año = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.año})"


class Inventario(models.Model):
    vehiculo = models.OneToOneField(Vehiculo, related_name='inventario', on_delete=models.CASCADE)
    cantidad_disponible = models.PositiveIntegerField()

    def __str__(self):
        return f"Inventario de {self.vehiculo.marca} {self.vehiculo.modelo}"