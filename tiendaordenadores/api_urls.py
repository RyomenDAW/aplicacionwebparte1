from django.urls import path
from .api_views import *

urlpatterns = [
    path('procesadores', procesador_list),
    path('placasbase', placabases_list, name='placasbase'),  # Ruta para la lista de procesadores
    path('procesadores/', procesador_list, name='procesadores'),  # Ruta para la lista de procesadores
    path('procesadores-mejorados', procesadores_mejorados, name='procesadores-mejorados'),  # Ruta para procesadores mejorados
    #=========================================================================================================================================
    path('graficas', grafica_list, name='graficas'),  # Ruta para la lista graficas
    path('fuentes', fuente_list, name='fuentes'),  # Ruta para la lista de fuentes de alimentación
    path('rams', ram_list, name='rams'),  # Ruta para la lista de RAMs
    #=========================================================================================================================================
    path('procesador_busqueda', procesador_busqueda, name='procesador_busqueda'), # Búsqueda Simple
    path('procesador_busqueda_avanzada', procesador_busqueda_avanzada, name='procesador_busqueda_avanzada'),
    path('grafica_busqueda/', grafica_busqueda_avanzada_api, name='grafica_busqueda_avanzada_api'),
    path('fuente_busqueda/', fuente_busqueda_avanzada_api, name='fuente_busqueda_avanzada_api'),
    path('ram_busqueda/', ram_busqueda_avanzada_api, name='ram_busqueda_avanzada_api'),
    path('grafica_busqueda_avanzada/', grafica_busqueda_avanzada_api, name='grafica_busqueda_avanzada_api'),
    path('ram_busqueda_avanzada/', ram_busqueda_avanzada_api, name='ram_busqueda_avanzada_api'),
    path('fuente_busqueda_avanzada/', fuente_busqueda_avanzada_api, name='fuente_busqueda_avanzada_api'),
    path('template-api/procesadores/', crear_procesador, name='crear-procesador'),
    path('procesadores/<int:procesador_id>/', obtener_y_actualizar_procesador, name='obtener_actualizar_procesador'),
    path('template-api/procesadores/<int:procesador_id>/eliminar/', eliminar_procesador, name='eliminar_procesador'),
    path('template-api/graficas/crear/', crear_grafica, name='crear_grafica'),
    path('template-api/graficas/<int:grafica_id>/', obtener_y_actualizar_grafica, name='obtener_actualizar_grafica'),
    path('template-api/graficas/<int:grafica_id>/actualizar-nombre/', actualizar_nombre_grafica, name='actualizar_nombre_grafica'),
    path('template-api/graficas/<int:grafica_id>/eliminar/', eliminar_grafica, name='eliminar_grafica'),
    #==========================================================================================================================================
    path('template-api/monitores-graficas/', crear_monitor_grafica, name='crear_monitor_grafica'),
    path('template-api/monitores-graficas/<int:relacion_id>/', actualizar_monitor_grafica, name='actualizar_monitor_grafica'),
    path('template-api/monitores-graficas/<int:relacion_id>/actualizar-grafica/', actualizar_grafica_en_relacion, name='actualizar_grafica_en_relacion'),
    path('template-api/monitores-graficas/<int:relacion_id>/eliminar/', eliminar_monitor_grafica, name='eliminar_monitor_grafica'),


]