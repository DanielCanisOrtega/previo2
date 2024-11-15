from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrdenViewSet, ProyectoViewSet

router = DefaultRouter()
router.register(r'ordenes', OrdenViewSet, basename='orden')
router.register(r'proyectos', ProyectoViewSet, basename='proyecto')


urlpatterns = [
    path('', include(router.urls)),
]
