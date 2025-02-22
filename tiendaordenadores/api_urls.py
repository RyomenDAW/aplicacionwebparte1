from django.urls import path

from .api_views import *

urlpatterns = [
    path('procesadores', procesador_list, name='procesadores'),  # Ruta para la lista de procesadores
    path('procesadores-mejorados/', procesadores_mejorados, name='procesadores-mejorados'),  # Ruta para procesadores mejorados
    path('graficas/', grafica_list, name='graficas'),  # Ruta para la lista graficas
    path('fuentes/', fuente_list, name='fuentes'),  # Ruta para la lista de fuentes de alimentación
    path('rams/', ram_list, name='rams'),  # Ruta para la lista de RAMs
    path('procesador_busqueda/', procesador_busqueda, name='procesador_busqueda'), # Búsqueda Simple
    
    #De aqui en adelante busquedas avanzadas, tienes todo en readme explicado
    
    path('procesador_busqueda_avanzada', procesador_busqueda_avanzada, name='procesador_busqueda_avanzada'),
    path('grafica_busqueda', grafica_busqueda_avanzada_api, name='grafica_busqueda_avanzada_api'),
    path('fuente_busqueda', fuente_busqueda_avanzada_api, name='fuente_busqueda_avanzada_api'),
    path('ram_busqueda', ram_busqueda_avanzada_api, name='ram_busqueda_avanzada_api'),
    path('grafica_busqueda_avanzada/', grafica_busqueda_avanzada_api, name='grafica_busqueda_avanzada_api'),
    path('ram_busqueda_avanzada/', ram_busqueda_avanzada_api, name='ram_busqueda_avanzada_api'),
    path('fuente_busqueda_avanzada/', fuente_busqueda_avanzada_api, name='fuente_busqueda_avanzada_api'),
]
