from django.urls import path

from .api_views import *

urlpatterns = [
    path('procesadores', procesador_list, name='procesadores'),  # Ruta para la lista de procesadores
    path('procesadores-mejorados', procesadores_mejorados, name='procesadores-mejorados'),  # Ruta para procesadores mejorados
]



