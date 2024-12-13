from django.urls import path, re_path
from . import views
from .views import *
urlpatterns = [
    path('home/', views.inicio, name ='inicio'),
    path('', views.inicio, name='inicio'),  # Página de inicio
    path ('procesadores/', views.lista_procesadores, name='lista_procesadores'),
    path ('procesadores/<int:numero_hilos>', views.lista_procesadores_segunhilos, name='lista_procesadores_segunhilos'),
    path ('procesadores/<nombre_familia>', views.lista_procesadores_segunfamilia, name='lista_procesadores_segunfamilia'),
    re_path(r'^graficas/(?P<nombre_familia>[-\w]+)/(?P<cantidad_vram>[-\w\.]+)/$', views.lista_graficas_segunfamilia_y_vram, name='lista_graficas_segunfamilia_y_vram'),
    path('procesadores/promedio-nucleos/', views.promedio_nucleos, name='promedio_nucleos'),
    path('graficas/filtrargraficas_segunvram', views.filtrargraficas_segunfecha, name ='filtrargraficas_segunvram'),
    path('ssd/primeros_5_ssd', views.primeros_5_ssd, name='primeros_5_ssd'),
    path('intermedia/graficas_sin_cuello_de_botella' ,views.graficas_sin_cuello_de_botella, name='graficas_sin_cuello_de_botella'),
    path('reverse/procesadores_segun_grafica/<int:grafica_id>', views.procesadores_segun_grafica, name='procesadores_segun_grafica'),
    path('graficas/lista_graficas.html', views.lista_graficas, name='lista_graficas'),
    path('procesadores/crear_procesador/', views.crear_procesador, name='crear_procesador'),
    #path('procesadores/', lista_procesadores, name='read_procesadores'),  # URL para la búsqueda de procesadores
    path('editar_procesador/<int:id_procesador>/', views.editar_procesador, name='editar_procesador'),
    path('procesadores/eliminar_procesador/<int:id_procesador>/', views.eliminar_procesador, name='eliminar_procesador'),    
    path('procesadores/read_procesadores/', views.read_procesadores, name='read_procesadores'),
        path('procesadores/crear_grafica/', views.crear_grafica, name='crear_grafica'),
    path('procesadores/read_graficas/', views.read_graficas, name='read_graficas'),
    path('editar_grafica/<int:id_grafica>/', views.editar_grafica, name='editar_grafica'),
        path('graficas/eliminar_grafica/<int:id_grafica>/', views.eliminar_grafica, name='eliminar_grafica'),    
        path('monitores/crear_monitor/', views.crear_monitor, name='crear_monitor'),
        path('monitores/read_monitor/', views.read_monitor, name='read_monitor'),
    path('monitores/editar_monitor/<int:id_monitor>/', views.editar_monitor, name='editar_monitor'),
        path('monitores/eliminar_monitor/<int:id_monitor>/', views.eliminar_monitor, name='eliminar_monitor'),    
        path('fuentes/crear_fuente/', views.crear_fuente, name='crear_fuente'),
        path('monitores/read_fuente/', views.read_fuente, name='read_fuente'),


    ] 



