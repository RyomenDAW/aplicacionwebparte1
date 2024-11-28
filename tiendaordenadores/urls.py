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
        path('procesadores/', lista_procesadores, name='read_procesadores'),  # URL para la búsqueda de procesadores
    path('editar_procesador/<int:id>/', views.editar_procesador, name='editar_procesador'),        
    ] 



