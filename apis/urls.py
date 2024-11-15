from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrdenViewSet, ProyectoViewSet, ReservaViewSet, VehiculoViewSet, InventarioViewSet

router = DefaultRouter()
router.register(r'ordenes', OrdenViewSet, basename='orden')
router.register(r'proyectos', ProyectoViewSet, basename='proyecto')
router.register(r'reservas', ReservaViewSet, basename='reserva')
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculo')
router.register(r'inventario', InventarioViewSet, basename='inventario')



urlpatterns = [
    path('', include(router.urls)),
]
