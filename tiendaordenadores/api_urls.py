from django.urls import path

from .api_views import *

urlpatterns = [
    path('procesadores', procesador_list, name='procesadores'),  # Ruta para la lista de procesadores
    path('procesadores-mejorados', procesadores_mejorados, name='procesadores-mejorados'),  # Ruta para procesadores mejorados
    path('graficas', grafica_list, name='graficas'),  # Ruta para la lista graficas
    path('fuentes', fuente_list, name='fuentes'),  # Ruta para la lista de fuentes de alimentación
    path('rams', ram_list, name='rams'),  # Ruta para la lista de RAMs

    
    
]



